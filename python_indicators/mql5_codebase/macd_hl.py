"""Macd hl — converted from MQL5: MQL5 Indicators/MACD High_Low/Macd hl.mq5

Macd high/low
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 8, 7: 8}, 'colors': {1: [16748574], 2: [16748574], 3: [11119017], 4: [3937500], 5: [3937500], 6: [11119017, 16748574, 16760576, 3937500, 255], 7: [11119017, 16748574, 16760576, 3937500, 255]}, 'widths': {6: 3, 7: 1}, 'styles': {2: 2, 3: 2, 4: 2}, 'labels': {1: 'Level up', 2: 'Early level up', 3: 'Zero level', 4: 'Early level down', 5: 'Level down', 6: 'Macd value', 7: 'Macd signal'}, 'levels': [], 'description': ['Macd high/low'], 'name': 'Macd hl', 'source': 'MQL5 Indicators/MACD High_Low/Macd hl.mq5', 'folder': 'MACD High_Low', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 19, 'label': 'Fast DEMA period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 39, 'label': 'Slow DEMA period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpLookBackPeriod', 'py': 'inpLookBackPeriod', 'param': 'inpLookBackPeriod', 'type': 'int', 'default': 50, 'label': 'Lookback period', 'sinput': False}, {'mql': 'inpEarlyLevel', 'py': 'inpEarlyLevel', 'param': 'inpEarlyLevel', 'type': 'double', 'default': 25.0, 'label': 'Early levels %', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 19)  # Fast DEMA period
inpSlowPeriod = _input('inpSlowPeriod', 39)  # Slow DEMA period
inpSignalPeriod = _input('inpSignalPeriod', 9)  # Signal period
inpLookBackPeriod = _input('inpLookBackPeriod', 50)  # Lookback period
inpEarlyLevel = _input('inpEarlyLevel', 25.0)  # Early levels %
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
    IndicatorSetString(INDICATOR_SHORTNAME, 'Macd high/low (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSignalPeriod) + ',' + _str(inpLookBackPeriod) + ')')
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
        _start = MathMax(i - inpLookBackPeriod, 0)
        _count = MathMin(_start + 1, inpLookBackPeriod)
        max_ = val[ArrayMaximum(val, _start, _count)]
        min_ = val[ArrayMinimum(val, _start, _count)]
        levelu2[i] = max_
        leveld2[i] = min_
        levelm[i] = (max_ + min_) / 2.0
        levelu1[i] = levelm[i] + (((levelu2[i] - levelm[i]) * inpEarlyLevel) / 100.0)
        leveld1[i] = levelm[i] - (((levelm[i] - leveld2[i]) * inpEarlyLevel) / 100.0)
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


class MacdHl(_MQL5Indicator):
    name = 'Macd hl'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpFastPeriod': 19,  # Fast DEMA period
        'inpSlowPeriod': 39,  # Slow DEMA period
        'inpSignalPeriod': 9,  # Signal period
        'inpLookBackPeriod': 50,  # Lookback period
        'inpEarlyLevel': 25.0,  # Early levels %
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

