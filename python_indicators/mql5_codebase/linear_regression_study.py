"""Linear regression study — converted from MQL5: MQL5 Indicators/Linear Regression Study/Linear regression study.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 8, 2: 1, 3: 1, 4: 1}, 'colors': {1: [12632256, 3329330, 42495], 2: [3329330], 3: [6908265], 4: [36095]}, 'widths': {1: 2}, 'styles': {2: 2, 3: 2, 4: 2}, 'labels': {1: 'Linear regression', 2: 'Linear regression channel up', 3: 'Linear regression line', 4: 'Linear regression channel down'}, 'levels': [], 'description': [], 'name': 'Linear regression study', 'source': 'MQL5 Indicators/Linear Regression Study/Linear regression study.mq5', 'folder': 'Linear Regression Study', 'inputs': [{'mql': 'inpLrPeriod', 'py': 'inpLrPeriod', 'param': 'inpLrPeriod', 'type': 'int', 'default': 30, 'label': 'Linear regression period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpProjectionLength', 'py': 'inpProjectionLength', 'param': 'inpProjectionLength', 'type': 'int', 'default': 50, 'label': 'Projection length', 'sinput': False}, {'mql': 'inpChannelMultiplier', 'py': 'inpChannelMultiplier', 'param': 'inpChannelMultiplier', 'type': 'double', 'default': 1.0, 'label': 'Stadard error channel width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpLrPeriod = _input('inpLrPeriod', 30)  # Linear regression period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpProjectionLength = _input('inpProjectionLength', 50)  # Projection length
inpChannelMultiplier = _input('inpChannelMultiplier', 1.0)  # Stadard error channel width
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
chanup = Arr(0, 0.0)
chanmi = Arr(0, 0.0)
chandn = Arr(0, 0.0)
workLr = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, chanup, INDICATOR_DATA)
    SetIndexBuffer(3, chanmi, INDICATOR_DATA)
    SetIndexBuffer(4, chandn, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, inpProjectionLength)
    PlotIndexSetInteger(3, PLOT_SHIFT, inpProjectionLength)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Linear regression (' + _str(inpLrPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    _lrslope = Box(0.0)
    _lrerror = Box(0.0)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iLrValue(getPrice(inpPrice, open, close, high, low, i, rates_total), inpLrPeriod, _lrslope, _lrerror, i, rates_total)
        valc[i] = (1 if (_lrslope.v > 0) else 2 if (_lrslope.v < 0) else valc[i - 1] if (i > 0) else 0)
        chandn[i] = EMPTY_VALUE
        chanmi[i] = EMPTY_VALUE
        chanup[i] = EMPTY_VALUE
        if i == (rates_total - 1):
            for k in range(0, inpLrPeriod):
                chanmi[rates_total - k - 1] = val[rates_total - 1] - (_lrslope.v * k)
            for k in range(inpLrPeriod + inpProjectionLength, 0 - 1, -1):
                chanup[rates_total - k - 1] = val[rates_total - 1] - (_lrslope.v * (k - inpProjectionLength)) + (inpChannelMultiplier * _lrerror.v)
                chandn[rates_total - k - 1] = val[rates_total - 1] - (_lrslope.v * (k - inpProjectionLength)) - (inpChannelMultiplier * _lrerror.v)
        i += 1
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, rates_total - inpProjectionLength - inpLrPeriod)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, rates_total - inpLrPeriod)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, rates_total - inpProjectionLength - inpLrPeriod)
    return i

def iLrValue(value, period, slope, error, r, bars):
    if ArraySize(workLr) != bars:
        ArrayResize(workLr, bars)
    workLr[r] = value
    if r < period or period < 2:
        return value
    sumx = 0.0
    sumxx = 0.0
    sumxy = 0.0
    sumy = 0.0
    sumyy = 0.0
    for k in range(0, period):
        price = workLr[r - k]
        sumx += k
        sumxx += k * k
        sumxy += k * price
        sumy += price
        sumyy += price * price
    slope.v = _fdiv((period * sumxy) - (sumx * sumy), (sumx * sumx) - (period * sumxx))
    error.v = MathSqrt(_fdiv((period * sumyy) - (sumy * sumy) - (slope.v * slope.v * ((period * sumxx) - (sumx * sumx))), period * (period - 2)))
    return _fdiv(sumy + (slope.v * sumx), period)

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


class LinearRegressionStudy(_MQL5Indicator):
    name = 'Linear regression study'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpLrPeriod': 30,  # Linear regression period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpProjectionLength': 50,  # Projection length
        'inpChannelMultiplier': 1.0,  # Stadard error channel width
    }

