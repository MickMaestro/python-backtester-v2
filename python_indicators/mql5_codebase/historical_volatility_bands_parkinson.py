"""Historical volatility bands - Parkinson — converted from MQL5: MQL5 Indicators/Historical Volatility Bands - Parkinson/Historical volatility bands - Parkinson.mq5

Historical volatility bands (Parkinson)
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 8, 2: 8, 3: 8}, 'colors': {1: [3329330, 6333684], 2: [3329330, 6333684], 3: [3329330, 6333684, 14474460]}, 'widths': {3: 2}, 'styles': {}, 'labels': {2: 'Lower band', 3: 'Middle value'}, 'levels': [], 'description': ['Historical volatility bands (Parkinson)'], 'name': 'Historical volatility bands - Parkinson', 'source': 'MQL5 Indicators/Historical Volatility Bands - Parkinson/Historical volatility bands - Parkinson.mq5', 'folder': 'Historical Volatility Bands - Parkinson', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Volatility bands period', 'sinput': False}, {'mql': 'inpDeviations', 'py': 'inpDeviations', 'param': 'inpDeviations', 'type': 'double', 'default': 2.0, 'label': 'Volatility  bands deviations', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Volatility bands median average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Volatility bands period
inpDeviations = _input('inpDeviations', 2.0)  # Volatility  bands deviations
inpMaMethod = _input('inpMaMethod', ma_ema)  # Volatility bands median average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
bufferUp = Arr(0, 0.0)
bufferUpc = Arr(0, 0.0)
bufferDn = Arr(0, 0.0)
bufferDnc = Arr(0, 0.0)
bufferMe = Arr(0, 0.0)
bufferMec = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, bufferUp, INDICATOR_DATA)
    SetIndexBuffer(1, bufferUpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, bufferDn, INDICATOR_DATA)
    SetIndexBuffer(3, bufferDnc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, bufferMe, INDICATOR_DATA)
    SetIndexBuffer(5, bufferMec, INDICATOR_COLOR_INDEX)
    return 0

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    _volConst = (1.0 / 4.0) * MathLog(2)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        sum_ = 0.0
        k = 0
        while k < inpPeriod and (i - k) >= 0:
            sum_ += _volConst * MathPow(MathLog(_fdiv(high[i - k], low[i - k])), 2)
            k += 1
        deviation = MathSqrt(sum_ / inpPeriod)
        bufferMe[i] = iCustomMa(inpMaMethod, price, inpPeriod, i, rates_total)
        bufferUp[i] = bufferMe[i] + (deviation * inpDeviations)
        bufferDn[i] = bufferMe[i] - (deviation * inpDeviations)
        if i > 0:
            bufferUpc[i] = bufferUpc[i - 1]
            bufferDnc[i] = bufferDnc[i - 1]
            if bufferUp[i] > bufferUp[i - 1]:
                bufferUpc[i] = 0.0
            if bufferUp[i] < bufferUp[i - 1]:
                bufferUpc[i] = 1.0
            if bufferDn[i] > bufferDn[i - 1]:
                bufferDnc[i] = 0.0
            if bufferDn[i] < bufferDn[i - 1]:
                bufferDnc[i] = 1.0
            bufferMec[i] = (0 if (bufferUpc[i] == 0 and bufferDnc[i] == 0) else 1 if (bufferUpc[i] == 1 and bufferDnc[i] == 1) else 2)
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


class HistoricalVolatilityBandsParkinson(_MQL5Indicator):
    name = 'Historical volatility bands - Parkinson'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Volatility bands period
        'inpDeviations': 2.0,  # Volatility  bands deviations
        'inpMaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=1),  # Volatility bands median average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

