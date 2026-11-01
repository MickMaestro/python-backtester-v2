"""dailyrangeprojections — converted from MQL5: MQL5 Indicators/Daily Range Projections/dailyrangeprojections.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'dailyrangeprojections', 'source': 'MQL5 Indicators/Daily Range Projections/dailyrangeprojections.mq5', 'folder': 'Daily Range Projections', 'inputs': [{'mql': 'Color_MAX', 'py': 'Color_MAX', 'param': None, 'type': 'color', 'default': 0, 'label': "Tomorrow's high line color", 'sinput': False}, {'mql': 'Style_MAX', 'py': 'Style_MAX', 'param': 'Style_MAX', 'type': 'int', 'default': 0, 'label': "Tomorrow's high line style", 'sinput': False}, {'mql': 'Width_MAX', 'py': 'Width_MAX', 'param': 'Width_MAX', 'type': 'int', 'default': 4, 'label': "Tomorrow's high line width", 'sinput': False}, {'mql': 'Color_MID', 'py': 'Color_MID', 'param': None, 'type': 'color', 'default': 0, 'label': "Tomorrow's middle line color", 'sinput': False}, {'mql': 'Style_MID', 'py': 'Style_MID', 'param': 'Style_MID', 'type': 'int', 'default': 4, 'label': "Tomorrow's middle line style", 'sinput': False}, {'mql': 'Width_MID', 'py': 'Width_MID', 'param': 'Width_MID', 'type': 'int', 'default': 1, 'label': "Tomorrow's middle line width", 'sinput': False}, {'mql': 'Color_MIN', 'py': 'Color_MIN', 'param': None, 'type': 'color', 'default': 0, 'label': "Tomorrow's low line color", 'sinput': False}, {'mql': 'Style_MIN', 'py': 'Style_MIN', 'param': 'Style_MIN', 'type': 'int', 'default': 0, 'label': "Tomorrow's low line style", 'sinput': False}, {'mql': 'Width_MIN', 'py': 'Width_MIN', 'param': 'Width_MIN', 'type': 'int', 'default': 4, 'label': "Tomorrow's low line width", 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DarkOrchid = 0xCC3299  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# enum Width
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('Width', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
Style_MAX = _input('Style_MAX', SOLID_)  # Tomorrow's high line style
Width_MAX = _input('Width_MAX', Width_4)  # Tomorrow's high line width
Style_MID = _input('Style_MID', DASHDOTDOT_)  # Tomorrow's middle line style
Width_MID = _input('Width_MID', Width_1)  # Tomorrow's middle line width
Style_MIN = _input('Style_MIN', SOLID_)  # Tomorrow's low line style
Width_MIN = _input('Width_MIN', Width_4)  # Tomorrow's low line width
MAX = ""
MIN = ""
MID = ""

def CreateHline(chart_id, name, nwin, price, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_HLINE, 0, 0, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetHline(chart_id, name, nwin, price, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateHline(chart_id, name, nwin, price, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, 0, price)

def OnInit():
    global MAX, MID, MIN
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Daily Range Projections')
    MAX = 'Maximum Daily Range Projections'
    MIN = 'Minimum Daily Range Projections'
    MID = 'Middle Daily Range Projections'

def OnDeinit(reason):
    ObjectDelete(0, MAX)
    ObjectDelete(0, MID)
    ObjectDelete(0, MIN)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Period() >= PERIOD_D1:
        return 0
    Tomorrow_High = 0.0
    Tomorrow_Low = 0.0
    Tomorrow_Middle = 0.0
    rates = Arr(2, 0, dyn=False, factory=MqlRates)
    X = 0.0
    if CopyRates(Symbol(), PERIOD_D1, 0, 2, rates) <= 0:
        return 0
    if rates[1].close < rates[1].open:
        X = (rates[0].high + rates[0].low + rates[0].close + rates[0].low) / 2.0
    if rates[1].close > rates[1].open:
        X = (rates[0].high + rates[0].low + rates[0].close + rates[0].high) / 2.0
    if rates[1].close == rates[1].open:
        X = (rates[0].high + rates[0].low + rates[0].close + rates[0].close) / 2.0
    Tomorrow_High = NormalizeDouble(X - rates[0].low, Digits())
    Tomorrow_Low = NormalizeDouble(X - rates[0].high, Digits())
    Tomorrow_Middle = NormalizeDouble((Tomorrow_High + Tomorrow_Low) / 2.0, Digits())
    SetHline(0, MAX, 0, Tomorrow_High, Color_MAX, Style_MAX, Width_MAX, 'MAX ' + DoubleToString(Tomorrow_High, Digits()))
    SetHline(0, MID, 0, Tomorrow_Middle, Color_MID, Style_MID, Width_MID, 'MID ' + DoubleToString(Tomorrow_Middle, Digits()))
    SetHline(0, MIN, 0, Tomorrow_Low, Color_MIN, Style_MIN, Width_MIN, 'MIN ' + DoubleToString(Tomorrow_Low, Digits()))
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
Color_MAX = _input('Color_MAX', _uint(Lime))  # Tomorrow's high line color
Color_MID = _input('Color_MID', _uint(DarkOrchid))  # Tomorrow's middle line color
Color_MIN = _input('Color_MIN', _uint(Red))  # Tomorrow's low line color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dailyrangeprojections(_MQL5Indicator):
    name = 'dailyrangeprojections'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Style_MAX': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # Tomorrow's high line style
        'Width_MAX': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=4),  # Tomorrow's high line width
        'Style_MID': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # Tomorrow's middle line style
        'Width_MID': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Tomorrow's middle line width
        'Style_MIN': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # Tomorrow's low line style
        'Width_MIN': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=4),  # Tomorrow's low line width
    }

