"""Volatility quality - on chart — converted from MQL5: MQL5 Indicators/Volatility Quality - on chart/Volatility quality - on chart.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 16, 'indicator_plots': 3}, 'types': {1: 16, 2: 17, 3: 8}, 'colors': {1: [11119017, 9639167, 3329330], 2: [11119017, 9639167, 3329330], 3: [11119017, 9639167, 3329330]}, 'widths': {3: 2}, 'styles': {}, 'labels': {1: 'Vq bars bars', 2: 'Vq candles candles', 3: 'Vq line'}, 'levels': [], 'description': [], 'name': 'Volatility quality - on chart', 'source': 'MQL5 Indicators/Volatility Quality - on chart/Volatility quality - on chart.mq5', 'folder': 'Volatility Quality - on chart', 'inputs': [{'mql': 'PriceSmoothing', 'py': 'PriceSmoothing', 'param': 'PriceSmoothing', 'type': 'int', 'default': 5, 'label': 'Price smoothing period', 'sinput': False}, {'mql': 'PriceSmoothingMethod', 'py': 'PriceSmoothingMethod', 'param': 'PriceSmoothingMethod', 'type': 'int', 'default': 3, 'label': 'Price smoothing method', 'sinput': False}, {'mql': 'FilterInPips', 'py': 'FilterInPips', 'param': 'FilterInPips', 'type': 'double', 'default': 2.0, 'label': 'Filter (in pips)', 'sinput': False}, {'mql': 'inpDisplayStyle', 'py': 'inpDisplayStyle', 'param': 'inpDisplayStyle', 'type': 'int', 'default': 0, 'label': 'Display style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDisplayStyle
dis_automatic = 0
dis_line = 1
dis_bars = 2
dis_candles = 3
_enum('enDisplayStyle', {0: 'dis_automatic', 1: 'dis_line', 2: 'dis_bars', 3: 'dis_candles'})

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
PriceSmoothing = _input('PriceSmoothing', 5)  # Price smoothing period
PriceSmoothingMethod = _input('PriceSmoothingMethod', ma_lwma)  # Price smoothing method
FilterInPips = _input('FilterInPips', 2.0)  # Filter (in pips)
inpDisplayStyle = _input('inpDisplayStyle', dis_automatic)  # Display style
canh = Arr(0, 0.0)
canl = Arr(0, 0.0)
cano = Arr(0, 0.0)
canc = Arr(0, 0.0)
cancl = Arr(0, 0.0)
baro = Arr(0, 0.0)
barh = Arr(0, 0.0)
barl = Arr(0, 0.0)
barc = Arr(0, 0.0)
barcl = Arr(0, 0.0)
line = Arr(0, 0.0)
linecl = Arr(0, 0.0)
prices = Arr(0, 0.0)
trend = Arr(0, 0.0)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(5,))
workEma = Arr(0, 0.0, dims=(5,))
workSmma = Arr(0, 0.0, dims=(5,))
workLwma = Arr(0, 0.0, dims=(5,))

def OnInit():
    SetIndexBuffer(0, baro, INDICATOR_DATA)
    SetIndexBuffer(1, barh, INDICATOR_DATA)
    SetIndexBuffer(2, barl, INDICATOR_DATA)
    SetIndexBuffer(3, barc, INDICATOR_DATA)
    SetIndexBuffer(4, barcl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, cano, INDICATOR_DATA)
    SetIndexBuffer(6, canh, INDICATOR_DATA)
    SetIndexBuffer(7, canl, INDICATOR_DATA)
    SetIndexBuffer(8, canc, INDICATOR_DATA)
    SetIndexBuffer(9, cancl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(10, line, INDICATOR_DATA)
    SetIndexBuffer(11, linecl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(12, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, val, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, valc, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility quality Stridsman (' + _str(PriceSmoothing) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prevDisplayType
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    pipMultiplier = MathPow(10, _imod(Digits(), 2))
    limit = prev_calculated - 1
    currDisplayType = -1
    _sw1 = inpDisplayStyle
    if _sw1 == dis_line:
        currDisplayType = CHART_LINE
    elif _sw1 == dis_bars:
        currDisplayType = CHART_BARS
    elif _sw1 == dis_candles:
        currDisplayType = CHART_CANDLES
    elif _sw1 == dis_automatic:
        currDisplayType = _int(ChartGetInteger(0, CHART_MODE))
    if currDisplayType != _s_OnCalculate_prevDisplayType:
        limit = 0
        _s_OnCalculate_prevDisplayType = currDisplayType
    i = MathMax(limit, 0)
    while i < rates_total:
        cHigh = iCustomMa(PriceSmoothingMethod, high[i], PriceSmoothing, i, rates_total, 0)
        cLow = iCustomMa(PriceSmoothingMethod, low[i], PriceSmoothing, i, rates_total, 1)
        cOpen = iCustomMa(PriceSmoothingMethod, open[i], PriceSmoothing, i, rates_total, 2)
        cClose = iCustomMa(PriceSmoothingMethod, close[i], PriceSmoothing, i, rates_total, 3)
        pClose = (iCustomMa(PriceSmoothingMethod, close[i - 1], PriceSmoothing, i - 1, rates_total, 4) if (i > 0) else cClose)
        trueRange = MathMax(cHigh, pClose) - MathMin(cLow, pClose)
        range_ = cHigh - cLow
        vqi = (((_fdiv(cClose - pClose, trueRange) + _fdiv(cClose - cOpen, range_)) * 0.5) if (range_ != 0 and trueRange != 0) else val[i - 1] if (i > 0) else 0)
        val[i] = ((val[i - 1] + (MathAbs(vqi) * (cClose - pClose + cClose - cOpen) * 0.5)) if (i > 0) else 0)
        if FilterInPips > 0 and i > 0:
            if MathAbs(val[i] - val[i - 1]) < (FilterInPips * pipMultiplier * Point()):
                val[i] = val[i - 1]
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        barc[i] = EMPTY_VALUE
        barl[i] = barc[i]
        barh[i] = barl[i]
        baro[i] = barh[i]
        canc[i] = EMPTY_VALUE
        canl[i] = canc[i]
        canh[i] = canl[i]
        cano[i] = canh[i]
        line[i] = EMPTY_VALUE
        _sw2 = currDisplayType
        if _sw2 == CHART_BARS:
            barh[i] = high[i]
            barl[i] = low[i]
            barc[i] = close[i]
            baro[i] = open[i]
            barcl[i] = valc[i]
        elif _sw2 == CHART_CANDLES:
            canh[i] = high[i]
            canl[i] = low[i]
            canc[i] = close[i]
            cano[i] = open[i]
            cancl[i] = valc[i]
        elif _sw2 == CHART_LINE:
            line[i] = cClose
            linecl[i] = valc[i]
        i += 1
    return rates_total

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw3 = mode
    if _sw3 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw3 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw3 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw3 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    k = 0
    workSma[r][instanceNo + 0] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo + 0]
        k += 1
    return _fdiv(avg, k)

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
    if period <= 1:
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

# ---- static local variables
_s_OnCalculate_prevDisplayType = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityQualityOnChart(_MQL5Indicator):
    name = 'Volatility quality - on chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PriceSmoothing': 5,  # Price smoothing period
        'PriceSmoothingMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=3),  # Price smoothing method
        'FilterInPips': 2.0,  # Filter (in pips)
        'inpDisplayStyle': _Choice({0: 'Automatic display style', 1: 'Display line', 2: 'Display bars', 3: 'Display candles'}, default=0),  # Display style
    }

