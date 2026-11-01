"""interpolation — converted from MQL5: MQL5 Indicators/Interpolation/interpolation.mq5

Copyright: Copyright © 2008, Gryb Alexander; Link: ICQ: 478-923-832 E-mail: alexandergrib@rambler.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, Gryb Alexander', 'link': 'ICQ: 478-923-832 E-mail: alexandergrib@rambler.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Interpolation'}, 'levels': [], 'description': [], 'name': 'interpolation', 'source': 'MQL5 Indicators/Interpolation/interpolation.mq5', 'folder': 'Interpolation', 'inputs': [{'mql': 'inumPrognoz', 'py': 'inumPrognoz', 'param': 'inumPrognoz', 'type': 'uint', 'default': 2, 'label': 'Number of predicted bars', 'sinput': False}, {'mql': 'ibegin', 'py': 'ibegin', 'param': 'ibegin', 'type': 'uint', 'default': 0, 'label': 'Starting bar for the analysis', 'sinput': False}, {'mql': 'iend', 'py': 'iend', 'param': 'iend', 'type': 'uint', 'default': 5, 'label': 'Last bar for the analysis', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inumPrognoz = _input('inumPrognoz', 2)  # Number of predicted bars
ibegin = _input('ibegin', 0)  # Starting bar for the analysis
iend = _input('iend', 5)  # Last bar for the analysis
b = Arr(0, 0.0)
min_rates_total = 0
Shift = 0
begin = 0
end = 0
numPrognoz = 0
IndBuffer = Arr(0, 0.0)

def OnInit():
    global Shift, begin, end, min_rates_total, numPrognoz
    numPrognoz = _int(inumPrognoz)
    begin = _int(ibegin)
    end = _int(iend)
    Shift = MathMax(numPrognoz - begin, 0)
    min_rates_total = end + numPrognoz
    if end < begin:
        Print('Incorrect values of the input parameters for the analyzed bars!')
    size = end + 1 + numPrognoz
    if ArrayResize(b, size) < size:
        Print('Failed to distribute the memory for b[] array')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Interpolation')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    ObjectDelete(0, 'Interpolation begin')
    ObjectDelete(0, 'Interpolation end')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or end < begin:
        return 0
    if prev_calculated <= 0:
        for bar in range(rates_total - 1, 0 - 1, -1):
            IndBuffer[bar] = 0.0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(close, True)
    for k in range(end, begin - 1, -1):
        b[k] = k
    start = begin - numPrognoz
    finish = end + numPrognoz + 1
    for bar in range(0, finish):
        IndBuffer[bar] = 0.0
    for bar in range(start, finish):
        a = 0.0
        for k in range(begin, end + 1):
            b1 = 1.0
            d = 1.0
            for z in range(begin, k):
                b1 *= bar - b[z]
                d *= b[k] - b[z]
            for z in range(k + 1, end + 1):
                b1 *= bar - b[z]
                d *= b[k] - b[z]
            a += _fdiv(close[k] * b1, d)
        IndBuffer[bar + Shift] = a
    SetVline(0, 'Interpolation end', 0, time[end], clrBlue, 0, 2, True, 'Interpolation end')
    SetVline(0, 'Interpolation begin', 0, time[begin], clrRed, 0, 2, True, 'Interpolation begin')
    ChartRedraw(0)
    return rates_total

def CreateVline(chart_id, name, nwin, time1, Color, style, width, background, text):
    ObjectCreate(chart_id, name, OBJ_VLINE, nwin, time1, 999999999)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, background)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetString(chart_id, name, OBJPROP_TOOLTIP, '\n')
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetVline(chart_id, name, nwin, time1, Color, style, width, background, text):
    if ObjectFind(chart_id, name) == -1:
        CreateVline(chart_id, name, nwin, time1, Color, style, width, background, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, 999999999)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Interpolation(_MQL5Indicator):
    name = 'interpolation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inumPrognoz': 2,  # Number of predicted bars
        'ibegin': 0,  # Starting bar for the analysis
        'iend': 5,  # Last bar for the analysis
    }

