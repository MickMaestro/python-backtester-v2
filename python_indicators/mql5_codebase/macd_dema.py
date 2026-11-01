"""Macd DEMA — converted from MQL5: MQL5 Indicators/MACD DEMA/Macd DEMA.mq5

Macd DEMA
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 1}, 'colors': {1: [14870490, 14278143], 2: [11119017, 16748574, 3937500], 3: [255]}, 'widths': {2: 2, 3: 1}, 'styles': {}, 'labels': {1: 'Macd dema filling', 2: 'Macd value', 3: 'Macd signal'}, 'levels': [], 'description': ['Macd DEMA'], 'name': 'Macd DEMA', 'source': 'MQL5 Indicators/MACD DEMA/Macd DEMA.mq5', 'folder': 'MACD DEMA', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 19, 'label': 'Fast DEMA period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 39, 'label': 'Slow DEMA period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 19)  # Fast DEMA period
inpSlowPeriod = _input('inpSlowPeriod', 39)  # Slow DEMA period
inpSignalPeriod = _input('inpSignalPeriod', 9)  # Signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
workEma = Arr(0, 0.0, dims=(1,))
workDema = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, signal, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Macd DEMA (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSignalPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = iDema(_price, inpFastPeriod, i, rates_total, 0) - iDema(_price, inpSlowPeriod, i, rates_total, 1)
        signal[i] = iEma(val[i], inpSignalPeriod, i, rates_total, 0)
        fillu[i] = val[i]
        filld[i] = signal[i]
        valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iDema(price, period, r, bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workDema, 0) != bars:
        ArrayResize(workDema, bars)
    instanceNo *= 2
    workDema[r][0 + instanceNo] = price
    workDema[r][1 + instanceNo] = price
    alpha = _fdiv(2.0, 1.0 + period)
    if r > 0:
        workDema[r][0 + instanceNo] = workDema[r - 1][0 + instanceNo] + (alpha * (price - workDema[r - 1][0 + instanceNo]))
        workDema[r][1 + instanceNo] = workDema[r - 1][1 + instanceNo] + (alpha * (workDema[r][0 + instanceNo] - workDema[r - 1][1 + instanceNo]))
    return (workDema[r][0 + instanceNo] * 2.0) - workDema[r][1 + instanceNo]

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


class MacdDEMA(_MQL5Indicator):
    name = 'Macd DEMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 19,  # Fast DEMA period
        'inpSlowPeriod': 39,  # Slow DEMA period
        'inpSignalPeriod': 9,  # Signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

