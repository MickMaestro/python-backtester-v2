"""Congestion index — converted from MQL5: MQL5 Indicators/Congestion index/Congestion index.mq5

Congestion index
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3, 'indicator_minimum': -100.0, 'indicator_maximum': 100.0}, 'types': {1: 7, 2: 8, 3: 8}, 'colors': {1: [14870490, 14278143], 2: [11119017, 16748574, 3937500], 3: [11119017, 16748574, 3937500]}, 'widths': {2: 2, 3: 1}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Congestion idex', 3: 'Signal line'}, 'levels': [-85.0, -20.0, 0.0, 20.0, 85.0], 'description': ['Congestion index'], 'name': 'Congestion index', 'source': 'MQL5 Indicators/Congestion index/Congestion index.mq5', 'folder': 'Congestion index', 'inputs': [{'mql': 'inpLookBack', 'py': 'inpLookBack', 'param': 'inpLookBack', 'type': 'int', 'default': 28, 'label': 'Lookback period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 10, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 10, 'label': 'Signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpLookBack = _input('inpLookBack', 28)  # Lookback period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpSmoothPeriod = _input('inpSmoothPeriod', 10)  # Smoothing period
inpSignalPeriod = _input('inpSignalPeriod', 10)  # Signal period
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
signalc = Arr(0, 0.0)
prices = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, signal, INDICATOR_DATA)
    SetIndexBuffer(5, signalc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, prices, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Congestion index (' + _str(inpLookBack) + ',' + _str(inpSmoothPeriod) + ',' + _str(inpSignalPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    _alpha = _fdiv(2.0, 1.0 + inpSmoothPeriod)
    _alphas = _fdiv(2.0, 1.0 + inpSignalPeriod)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _start = MathMax(i - inpLookBack + 1, 0)
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        lowest = low[ArrayMinimum(low, _start, inpLookBack)]
        dividend = (_fdiv(100.0 * (prices[i] - prices[i - inpLookBack + 1]), prices[i - inpLookBack + 1]) if (i >= inpLookBack) else 0)
        divisor = (_fdiv(high[ArrayMaximum(high, _start, inpLookBack)] - lowest, lowest) if (lowest != 0) else 0)
        ci = (_fdiv(dividend, divisor) if (divisor != 0) else 0)
        val[i] = ((val[i - 1] + (_alpha * (ci - val[i - 1]))) if (i > 0) else ci)
        signal[i] = ((signal[i - 1] + (_alphas * (val[i] - signal[i - 1]))) if (i > 0) else val[i])
        fillu[i] = val[i]
        filld[i] = signal[i]
        valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        signalc[i] = valc[i]
        i += 1
    return i

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


class CongestionIndex(_MQL5Indicator):
    name = 'Congestion index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpLookBack': 28,  # Lookback period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpSmoothPeriod': 10,  # Smoothing period
        'inpSignalPeriod': 10,  # Signal period
    }
    y_range = (-100.0, 100.0)

