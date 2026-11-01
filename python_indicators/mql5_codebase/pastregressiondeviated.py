"""pastregressiondeviated — converted from MQL5: MQL5 Indicators/Past Regression Deviated/pastregressiondeviated.mq5

past regression deviated
Copyright: Copyright © 2006, tageiger, aka fxid10t@yahoo.com; Link: fxid10t@yahoo.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, tageiger, aka fxid10t@yahoo.com', 'link': 'fxid10t@yahoo.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {4: 1, 1: 1, 2: 1, 3: 1, 5: 1, 6: 1, 7: 1}, 'colors': {4: [8721863], 1: [13828244], 2: [42495], 3: [8421376], 5: [8421376], 6: [42495], 7: [13828244]}, 'widths': {4: 1, 1: 1, 2: 1, 3: 1, 5: 1, 6: 1, 7: 1}, 'styles': {4: 4, 1: 4, 2: 4, 3: 4, 5: 4, 6: 4, 7: 4}, 'labels': {4: 'past regression deviated', 1: '3st Std up', 2: '2st Std up', 3: '1st Std up', 5: '1st Std down', 6: '2st Std down', 7: '3st Std down'}, 'levels': [], 'description': ['past regression deviated'], 'name': 'pastregressiondeviated', 'source': 'MQL5 Indicators/Past Regression Deviated/pastregressiondeviated.mq5', 'folder': 'Past Regression Deviated', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 55, 'label': 'Amount of bars for regression', 'sinput': False}, {'mql': 'StdChannel1', 'py': 'StdChannel1', 'param': 'StdChannel1', 'type': 'double', 'default': 1.0, 'label': '1st channel', 'sinput': False}, {'mql': 'StdChannel2', 'py': 'StdChannel2', 'param': 'StdChannel2', 'type': 'double', 'default': 2.0, 'label': '2nd channel', 'sinput': False}, {'mql': 'StdChannel3', 'py': 'StdChannel3', 'param': 'StdChannel3', 'type': 'double', 'default': 3.0, 'label': '3rd channel', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'Line_color', 'py': 'Line_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Trend line color', 'sinput': False}, {'mql': 'Line_style', 'py': 'Line_style', 'param': 'Line_style', 'type': 'int', 'default': 0, 'label': 'Trend line style', 'sinput': False}, {'mql': 'Line_width', 'py': 'Line_width', 'param': 'Line_width', 'type': 'int', 'default': 3, 'label': 'Trend line width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Red = 0x0000FF  # MQL4 colour name

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# ---- inputs and global variables
period = 0
Length = _input('Length', 55)  # Amount of bars for regression
StdChannel1 = _input('StdChannel1', 1.0)  # 1st channel
StdChannel2 = _input('StdChannel2', 2.0)  # 2nd channel
StdChannel3 = _input('StdChannel3', 3.0)  # 3rd channel
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Line_style = _input('Line_style', STYLE_SOLID)  # Trend line style
Line_width = _input('Line_width', w_3)  # Trend line width
MeanBuffer = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
min_rates_total = 0

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def OnInit():
    global min_rates_total
    min_rates_total = Length + 1
    SetIndexBuffer(3, MeanBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MeanBuffer, True)
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer5, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer6, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(ExtLineBuffer3, True)
    ArraySetAsSeries(ExtLineBuffer4, True)
    ArraySetAsSeries(ExtLineBuffer5, True)
    ArraySetAsSeries(ExtLineBuffer6, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Past regression deviated(', Length, ', ', StdChannel1, ', ', StdChannel2, ', ', StdChannel3, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    ObjectDelete(0, _str(period) + 'm ' + _str(Length) + ' TL')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    StartBar = 0
    EndBar = 0
    n = 0
    value = 0.0
    a = 0.0
    b = 0.0
    c = 0.0
    sumy = 0.0
    sumx = 0.0
    sumx2 = 0.0
    sumxy = 0.0
    X = 0.0
    StdDev = 0.0
    SumSquared = 0.0
    Price1 = 0.0
    Price2 = 0.0
    name = ""
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        StartBar = bar + Length
        EndBar = bar
        n = StartBar - EndBar + 1
        value = close[EndBar]
        sumy = value
        sumx = 0.0
        sumxy = 0.0
        sumx2 = 0.0
        for ii in range(1, n):
            value = close[EndBar + ii]
            sumy += value
            sumxy += value * ii
            sumx += ii
            sumx2 += ii * ii
        c = (sumx2 * n) - (sumx * sumx)
        if c == 0.0:
            return 0
        b = _fdiv((sumxy * n) - (sumx * sumy), c)
        a = _fdiv(sumy - (sumx * b), n)
        Price2 = a
        Price1 = a + (b * n)
        MeanBuffer[bar] = NormalizeDouble(Price2, Digits())
        name = _str(period) + 'm ' + _str(Length) + ' TL'
        SetTline(0, name, 0, time[StartBar], Price1, time[EndBar], Price2, Line_color, Line_style, Line_width, name)
        X = 0.0
        StdDev = 0.0
        SumSquared = 0.0
        for iii in range(bar, StartBar):
            X = MathAbs(close[iii] - ObjectGetValueByTime(0, name, time[iii], 0))
            SumSquared += X * X
        StdDev = MathSqrt(_fdiv(SumSquared, StartBar - EndBar - 1))
        ExtLineBuffer1[bar] = MeanBuffer[bar] + (StdChannel1 * StdDev)
        ExtLineBuffer2[bar] = MeanBuffer[bar] + (StdChannel2 * StdDev)
        ExtLineBuffer3[bar] = MeanBuffer[bar] + (StdChannel3 * StdDev)
        ExtLineBuffer4[bar] = MeanBuffer[bar] - (StdChannel1 * StdDev)
        ExtLineBuffer5[bar] = MeanBuffer[bar] - (StdChannel2 * StdDev)
        ExtLineBuffer6[bar] = MeanBuffer[bar] - (StdChannel3 * StdDev)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
Line_color = _input('Line_color', _uint(Red))  # Trend line color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pastregressiondeviated(_MQL5Indicator):
    name = 'pastregressiondeviated'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 55,  # Amount of bars for regression
        'StdChannel1': 1.0,  # 1st channel
        'StdChannel2': 2.0,  # 2nd channel
        'StdChannel3': 3.0,  # 3rd channel
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'Line_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Trend line style
        'Line_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Trend line width
    }

