"""Linear regression sketcher — converted from MQL5: MQL5 Indicators/Linear Regression Sketcher/Linear regression sketcher.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 3329330, 42495]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Linear regression'}, 'levels': [], 'description': [], 'name': 'Linear regression sketcher', 'source': 'MQL5 Indicators/Linear Regression Sketcher/Linear regression sketcher.mq5', 'folder': 'Linear Regression Sketcher', 'inputs': [{'mql': 'inpLrPeriod', 'py': 'inpLrPeriod', 'param': 'inpLrPeriod', 'type': 'int', 'default': 50, 'label': 'Linear regression period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpLrcNo', 'py': 'inpLrcNo', 'param': 'inpLrcNo', 'type': 'int', 'default': 250, 'label': 'Number of linear regressions drawn', 'sinput': False}, {'mql': 'inpColorUp', 'py': 'inpColorUp', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Color when regression sloping up', 'sinput': False}, {'mql': 'inpColorDown', 'py': 'inpColorDown', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Color when regression sloping down', 'sinput': False}, {'mql': 'inpLinesWidthWhenTrendChange', 'py': 'inpLinesWidthWhenTrendChange', 'param': 'inpLinesWidthWhenTrendChange', 'type': 'int', 'default': 2, 'label': 'Lines width when trend change', 'sinput': False}, {'mql': 'inpChannelStyle', 'py': 'inpChannelStyle', 'param': 'inpChannelStyle', 'type': 'int', 'default': 2, 'label': 'Lines style', 'sinput': False}, {'mql': 'inpUniqueID', 'py': 'inpUniqueID', 'param': None, 'type': 'string', 'default': 'Lrs1', 'label': 'Indicator unique ID', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpLrPeriod = _input('inpLrPeriod', 50)  # Linear regression period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpLrcNo = _input('inpLrcNo', 250)  # Number of linear regressions drawn
inpColorUp = _input('inpColorUp', clrLimeGreen)  # Color when regression sloping up
inpColorDown = _input('inpColorDown', clrOrange)  # Color when regression sloping down
inpLinesWidthWhenTrendChange = _input('inpLinesWidthWhenTrendChange', 2)  # Lines width when trend change
inpChannelStyle = _input('inpChannelStyle', STYLE_DOT)  # Lines style
inpUniqueID = _input('inpUniqueID', 'Lrs1')  # Indicator unique ID
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workLr = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Linear regression sketcher (' + _str(inpLrPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, inpUniqueID + ':')
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    _lrslope = Box(0.0)
    _lrerror = Box(0.0)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iLrValue(getPrice(inpPrice, open, close, high, low, i, rates_total), inpLrPeriod, _lrslope, _lrerror, i, rates_total)
        valc[i] = (1 if (_lrslope.v > 0) else 2 if (_lrslope.v < 0) else valc[i - 1] if (i > 0) else 0)
        if i > (rates_total - inpLrcNo):
            if valc[i] != valc[i - 1]:
                createLine('', val[i], val[i] - (_lrslope.v * (inpLrPeriod - 1)), time, i, inpLinesWidthWhenTrendChange)
            else:
                createLine('', val[i], val[i] - (_lrslope.v * (inpLrPeriod - 1)), time, i)
        i += 1
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

def createLine(add, lrs, lre, time, i, lineWidth=0):
    name = inpUniqueID + ':' + add + _str(i)
    ObjectCreate(0, name, OBJ_TREND, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, time[i])
    ObjectSetInteger(0, name, OBJPROP_TIME, 1, time[i - inpLrPeriod + 1])
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, lrs)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, lre)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_RAY, False)
    ObjectSetInteger(0, name, OBJPROP_BACK, True)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, lineWidth)
    ObjectSetInteger(0, name, OBJPROP_STYLE, inpChannelStyle)
    theColor = (inpColorUp if (lrs > lre) else inpColorDown)
    ObjectSetInteger(0, name, OBJPROP_COLOR, theColor)

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


class LinearRegressionSketcher(_MQL5Indicator):
    name = 'Linear regression sketcher'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpLrPeriod': 50,  # Linear regression period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLrcNo': 250,  # Number of linear regressions drawn
        'inpLinesWidthWhenTrendChange': 2,  # Lines width when trend change
        'inpChannelStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Lines style
    }

