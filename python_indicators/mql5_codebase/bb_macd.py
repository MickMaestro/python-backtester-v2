"""BB macd — converted from MQL5: MQL5 Indicators/BB MACD Extended/BB macd.mq5

Bollinger bands Macd
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 8, 7: 8}, 'colors': {1: [3329330], 2: [3329330], 3: [11119017], 4: [17919], 5: [17919], 6: [11119017, 32768, 3329330, 17919, 36095], 7: [11119017, 32768, 3329330, 17919, 36095]}, 'widths': {6: 3, 7: 1}, 'styles': {2: 2, 3: 2, 4: 2}, 'labels': {1: 'Level up', 2: 'Early level up', 3: 'median level', 4: 'Early level down', 5: 'Level down', 6: 'Macd value', 7: 'Macd signal'}, 'levels': [], 'description': ['Bollinger bands Macd'], 'name': 'BB macd', 'source': 'MQL5 Indicators/BB MACD Extended/BB macd.mq5', 'folder': 'BB MACD Extended', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 19, 'label': 'Fast MACD period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 39, 'label': 'Slow MACD period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpBbPeriod', 'py': 'inpBbPeriod', 'param': 'inpBbPeriod', 'type': 'int', 'default': 50, 'label': 'Bollinger bands period', 'sinput': False}, {'mql': 'inpBbDeviations', 'py': 'inpBbDeviations', 'param': 'inpBbDeviations', 'type': 'double', 'default': 2.0, 'label': 'Bollinger bands period', 'sinput': False}, {'mql': 'inpBbEarlyLevel', 'py': 'inpBbEarlyLevel', 'param': 'inpBbEarlyLevel', 'type': 'double', 'default': 0.5, 'label': 'Early level deviations', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 19)  # Fast MACD period
inpSlowPeriod = _input('inpSlowPeriod', 39)  # Slow MACD period
inpSignalPeriod = _input('inpSignalPeriod', 9)  # Signal period
inpBbPeriod = _input('inpBbPeriod', 50)  # Bollinger bands period
inpBbDeviations = _input('inpBbDeviations', 2.0)  # Bollinger bands period
inpBbEarlyLevel = _input('inpBbEarlyLevel', 0.5)  # Early level deviations
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
signalc = Arr(0, 0.0)
levelm = Arr(0, 0.0)
levelu1 = Arr(0, 0.0)
levelu2 = Arr(0, 0.0)
leveld1 = Arr(0, 0.0)
leveld2 = Arr(0, 0.0)
workEma = Arr(0, 0.0, dims=(3,))
workSma = Arr(0, 0.0, dims=(1,))
workDev = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, levelu2, INDICATOR_DATA)
    SetIndexBuffer(1, levelu1, INDICATOR_DATA)
    SetIndexBuffer(2, levelm, INDICATOR_DATA)
    SetIndexBuffer(3, leveld1, INDICATOR_DATA)
    SetIndexBuffer(4, leveld2, INDICATOR_DATA)
    SetIndexBuffer(5, val, INDICATOR_DATA)
    SetIndexBuffer(6, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, signal, INDICATOR_DATA)
    SetIndexBuffer(8, signalc, INDICATOR_COLOR_INDEX)
    for i in range(0, 5):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BB Macd (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSignalPeriod) + ',' + _str(inpBbPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = iEma(_price, inpFastPeriod, i, rates_total, 0) - iEma(_price, inpSlowPeriod, i, rates_total, 1)
        signal[i] = iEma(val[i], inpSignalPeriod, i, rates_total, 2)
        _deviation = iDeviation(val[i], inpBbPeriod, i, rates_total)
        levelm[i] = iSma(val[i], inpBbPeriod, i, rates_total, 0)
        levelu2[i] = levelm[i] + (_deviation * inpBbDeviations)
        leveld2[i] = levelm[i] - (_deviation * inpBbDeviations)
        levelu1[i] = levelm[i] + (_deviation * inpBbEarlyLevel)
        leveld1[i] = levelm[i] - (_deviation * inpBbEarlyLevel)
        valc[i] = ((2 if (val[i] > levelu2[i]) else 1 if (val[i] > levelm[i]) else 0) if (val[i] > signal[i]) else (4 if (val[i] < leveld2[i]) else 3 if (val[i] < levelm[i]) else 0) if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        signalc[i] = valc[i]
        i += 1
    return i

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

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

def iDeviation(value, length, i, bars, isSample=False):
    if ArraySize(workDev) != bars:
        ArrayResize(workDev, bars)
    workDev[i] = value
    sumx = 0.0
    sumxx = 0.0
    k = 0
    while k < length and (i - k) >= 0:
        pass
        sumx += workDev[i - k]
        sumxx += workDev[i - k] * workDev[i - k]
        k += 1
    return MathSqrt(_fdiv(sumxx - _fdiv(sumx * sumx, length), MathMax(length - isSample, 1)))

def getPrice(tprice, open, close, high, low, i, _bars):
    _sw1 = tprice
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBMacd(_MQL5Indicator):
    name = 'BB macd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 19,  # Fast MACD period
        'inpSlowPeriod': 39,  # Slow MACD period
        'inpSignalPeriod': 9,  # Signal period
        'inpBbPeriod': 50,  # Bollinger bands period
        'inpBbDeviations': 2.0,  # Bollinger bands period
        'inpBbEarlyLevel': 0.5,  # Early level deviations
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

