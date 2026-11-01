"""Average penetration bars — converted from MQL5: MQL5 Indicators/Average penetration bars/Average penetration bars.mq5

Average penetration on chart bars or candles
Custom trend calculating way by Vonasi
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 13, 'indicator_plots': 2}, 'types': {1: 16, 2: 17}, 'colors': {1: [11119017, 16760576, 6333684], 2: [11119017, 16760576, 6333684]}, 'widths': {}, 'styles': {}, 'labels': {1: 'APtrend bars', 2: 'AP trend candles'}, 'levels': [], 'description': ['Average penetration on chart bars or candles', 'Custom trend calculating way by Vonasi'], 'name': 'Average penetration bars', 'source': 'MQL5 Indicators/Average penetration bars/Average penetration bars.mq5', 'folder': 'Average penetration bars', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 63, 'label': 'Look-back period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 100, 'label': 'Average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 0, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Average price', 'sinput': False}, {'mql': 'inpCountWhat', 'py': 'inpCountWhat', 'param': 'inpCountWhat', 'type': 'int', 'default': 0, 'label': 'Count mode :', 'sinput': False}, {'mql': 'inpHistoType', 'py': 'inpHistoType', 'param': 'inpHistoType', 'type': 'int', 'default': 1, 'label': 'Histogram type', 'sinput': False}, {'mql': 'inpDisplayAs', 'py': 'inpDisplayAs', 'param': 'inpDisplayAs', 'type': 'int', 'default': 0, 'label': 'Display type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# enum enCountWhat
count_closes = 0
count_highlow = 1
_enum('enCountWhat', {0: 'count_closes', 1: 'count_highlow'})

# enum enHistoType
histo_classical = 0
histo_vonasi = 1
_enum('enHistoType', {0: 'histo_classical', 1: 'histo_vonasi'})

# enum enDisplayStyle
dis_bars = 0
dis_candles = 1
_enum('enDisplayStyle', {0: 'dis_bars', 1: 'dis_candles'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 63)  # Look-back period
inpMaPeriod = _input('inpMaPeriod', 100)  # Average period
inpMaMethod = _input('inpMaMethod', ma_sma)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Average price
inpCountWhat = _input('inpCountWhat', count_closes)  # Count mode :
inpHistoType = _input('inpHistoType', histo_vonasi)  # Histogram type
inpDisplayAs = _input('inpDisplayAs', dis_bars)  # Display type
baro = Arr(0, 0.0)
barh = Arr(0, 0.0)
barl = Arr(0, 0.0)
barc = Arr(0, 0.0)
barcl = Arr(0, 0.0)
candleo = Arr(0, 0.0)
candleh = Arr(0, 0.0)
candlel = Arr(0, 0.0)
candlec = Arr(0, 0.0)
candlecl = Arr(0, 0.0)
lineup = Arr(0, 0.0)
linedn = Arr(0, 0.0)
average = Arr(0, 0.0)
_maNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
_coNames = Arr.of(['couniting closes', 'counting high/low'], fill="")
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, baro, INDICATOR_DATA)
    SetIndexBuffer(1, barh, INDICATOR_DATA)
    SetIndexBuffer(2, barl, INDICATOR_DATA)
    SetIndexBuffer(3, barc, INDICATOR_DATA)
    SetIndexBuffer(4, barcl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, candleo, INDICATOR_DATA)
    SetIndexBuffer(6, candleh, INDICATOR_DATA)
    SetIndexBuffer(7, candlel, INDICATOR_DATA)
    SetIndexBuffer(8, candlec, INDICATOR_DATA)
    SetIndexBuffer(9, candlecl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(10, lineup, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, linedn, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, average, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Average penetration bars ' + _coNames[inpCountWhat] + ' (' + _str(inpPeriod) + ',' + _str(inpMaPeriod) + ' ' + _maNames[inpMaMethod] + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        average[i] = iCustomMa(inpMaMethod, getPrice(inpPrice, open, close, high, low, i, rates_total), inpMaPeriod, i, rates_total, 0)
        lineup[i] = 0.0
        linedn[i] = 0.0
        k = 0
        while k < inpPeriod and (i - k) >= 0:
            lineup[i] += (close[i - k] if (inpCountWhat == count_closes) else high[i - k]) > average[i - k]
            linedn[i] += (close[i - k] if (inpCountWhat == count_closes) else low[i - k]) < average[i - k]
            k += 1
        direction = (1 if (lineup[i] > linedn[i]) else -1 if (lineup[i] < linedn[i]) else 0)
        if inpHistoType == histo_vonasi:
            if (direction == 1 and i > 0) and (lineup[i] - linedn[i]) < (lineup[i - 1] - linedn[i - 1]):
                direction = -1
            if (direction == -1 and i > 0) and (linedn[i] - lineup[i]) < (linedn[i - 1] - lineup[i - 1]):
                direction = 1
        barc[i] = EMPTY_VALUE
        barl[i] = barc[i]
        barh[i] = barl[i]
        baro[i] = barh[i]
        candlec[i] = EMPTY_VALUE
        candlel[i] = candlec[i]
        candleh[i] = candlel[i]
        candleo[i] = candleh[i]
        if inpDisplayAs == dis_bars:
            baro[i] = open[i]
            barh[i] = high[i]
            barl[i] = low[i]
            barc[i] = close[i]
            barcl[i] = (1 if (direction == 1) else 2 if (direction == -1) else 0)
        else:
            candleo[i] = open[i]
            candleh[i] = high[i]
            candlel[i] = low[i]
            candlec[i] = close[i]
            candlecl[i] = (1 if (direction == 1) else 2 if (direction == -1) else 0)
    return rates_total

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    workSmma[r][instanceNo] = price
    if r > 1 and period > 1:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    if period < 1:
        return price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
        _sw2 = tprice
        if _sw2 == PRICE_CLOSE:
            return close[i]
        elif _sw2 == PRICE_OPEN:
            return open[i]
        elif _sw2 == PRICE_HIGH:
            return high[i]
        elif _sw2 == PRICE_LOW:
            return low[i]
        elif _sw2 == PRICE_MEDIAN:
            return (high[i] + low[i]) / 2.0
        elif _sw2 == PRICE_TYPICAL:
            return (high[i] + low[i] + close[i]) / 3.0
        elif _sw2 == PRICE_WEIGHTED:
            return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AveragePenetrationBars(_MQL5Indicator):
    name = 'Average penetration bars'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 63,  # Look-back period
        'inpMaPeriod': 100,  # Average period
        'inpMaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Average price
        'inpCountWhat': _Choice({0: 'Count close price for penetration', 1: 'Count high and lowe prices for penetration'}, default=0),  # Count mode :
        'inpHistoType': _Choice({0: 'Classical (higher/lower value) comparison', 1: 'Vonasi type comparison'}, default=1),  # Histogram type
        'inpDisplayAs': _Choice({0: 'Display bars', 1: 'Display candles'}, default=0),  # Display type
    }

