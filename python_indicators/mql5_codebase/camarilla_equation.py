"""camarilla_equation — converted from MQL5: MQL5 Indicators/Camarilla Equation/camarilla_equation.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'camarilla_equation', 'source': 'MQL5 Indicators/Camarilla Equation/camarilla_equation.mq5', 'folder': 'Camarilla Equation', 'inputs': [{'mql': 'CPeriod', 'py': 'CPeriod', 'param': 'CPeriod', 'type': 'int', 'default': 16408, 'label': '', 'sinput': False}, {'mql': 'color_H5', 'py': 'color_H5', 'param': None, 'type': 'color', 'default': 0, 'label': 'H5 level color', 'sinput': False}, {'mql': 'color_H4', 'py': 'color_H4', 'param': None, 'type': 'color', 'default': 0, 'label': 'H4 level color', 'sinput': False}, {'mql': 'color_H3', 'py': 'color_H3', 'param': None, 'type': 'color', 'default': 0, 'label': 'H3 level color', 'sinput': False}, {'mql': 'color_H2', 'py': 'color_H2', 'param': None, 'type': 'color', 'default': 0, 'label': 'H2 level color', 'sinput': False}, {'mql': 'color_H1', 'py': 'color_H1', 'param': None, 'type': 'color', 'default': 0, 'label': 'H1 level color', 'sinput': False}, {'mql': 'color_L1', 'py': 'color_L1', 'param': None, 'type': 'color', 'default': 0, 'label': 'L1 level color', 'sinput': False}, {'mql': 'color_L2', 'py': 'color_L2', 'param': None, 'type': 'color', 'default': 0, 'label': 'L2 level color', 'sinput': False}, {'mql': 'color_L3', 'py': 'color_L3', 'param': None, 'type': 'color', 'default': 0, 'label': 'L3 level color', 'sinput': False}, {'mql': 'color_L4', 'py': 'color_L4', 'param': None, 'type': 'color', 'default': 0, 'label': 'L4 level color', 'sinput': False}, {'mql': 'color_L5', 'py': 'color_L5', 'param': None, 'type': 'color', 'default': 0, 'label': 'L5 level color', 'sinput': False}, {'mql': 'style_H5', 'py': 'style_H5', 'param': 'style_H5', 'type': 'int', 'default': 3, 'label': 'H5 level line style', 'sinput': False}, {'mql': 'style_H4', 'py': 'style_H4', 'param': 'style_H4', 'type': 'int', 'default': 4, 'label': 'H4 level line style', 'sinput': False}, {'mql': 'style_H3', 'py': 'style_H3', 'param': 'style_H3', 'type': 'int', 'default': 0, 'label': 'H3 level line style', 'sinput': False}, {'mql': 'style_H2', 'py': 'style_H2', 'param': 'style_H2', 'type': 'int', 'default': 4, 'label': 'H2 level line style', 'sinput': False}, {'mql': 'style_H1', 'py': 'style_H1', 'param': 'style_H1', 'type': 'int', 'default': 4, 'label': 'H1 level line style', 'sinput': False}, {'mql': 'style_L1', 'py': 'style_L1', 'param': 'style_L1', 'type': 'int', 'default': 4, 'label': 'L1 level line style', 'sinput': False}, {'mql': 'style_L2', 'py': 'style_L2', 'param': 'style_L2', 'type': 'int', 'default': 4, 'label': 'L2 level line style', 'sinput': False}, {'mql': 'style_L3', 'py': 'style_L3', 'param': 'style_L3', 'type': 'int', 'default': 0, 'label': 'L3 level line style', 'sinput': False}, {'mql': 'style_L4', 'py': 'style_L4', 'param': 'style_L4', 'type': 'int', 'default': 4, 'label': 'L4 level line style', 'sinput': False}, {'mql': 'style_L5', 'py': 'style_L5', 'param': 'style_L5', 'type': 'int', 'default': 3, 'label': 'L5 level line style', 'sinput': False}, {'mql': 'width_H5', 'py': 'width_H5', 'param': 'width_H5', 'type': 'int', 'default': 1, 'label': 'H5 level width', 'sinput': False}, {'mql': 'width_H4', 'py': 'width_H4', 'param': 'width_H4', 'type': 'int', 'default': 1, 'label': 'H4 level width', 'sinput': False}, {'mql': 'width_H3', 'py': 'width_H3', 'param': 'width_H3', 'type': 'int', 'default': 2, 'label': 'H3 level width', 'sinput': False}, {'mql': 'width_H2', 'py': 'width_H2', 'param': 'width_H2', 'type': 'int', 'default': 1, 'label': 'H2 level width', 'sinput': False}, {'mql': 'width_H1', 'py': 'width_H1', 'param': 'width_H1', 'type': 'int', 'default': 1, 'label': 'H1 level width', 'sinput': False}, {'mql': 'width_L1', 'py': 'width_L1', 'param': 'width_L1', 'type': 'int', 'default': 1, 'label': 'L1 level width', 'sinput': False}, {'mql': 'width_L2', 'py': 'width_L2', 'param': 'width_L2', 'type': 'int', 'default': 1, 'label': 'L2 level width', 'sinput': False}, {'mql': 'width_L3', 'py': 'width_L3', 'param': 'width_L3', 'type': 'int', 'default': 2, 'label': 'L3 level width', 'sinput': False}, {'mql': 'width_L4', 'py': 'width_L4', 'param': 'width_L4', 'type': 'int', 'default': 1, 'label': 'L4 level width', 'sinput': False}, {'mql': 'width_L5', 'py': 'width_L5', 'param': 'width_L5', 'type': 'int', 'default': 1, 'label': 'L5 level width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Crimson = 0x3C14DC  # MQL4 colour name
DarkSlateGray = 0x4F4F2F  # MQL4 colour name
Green = 0x008000  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Purple = 0x800080  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# enum STYLE
STYLE_SOLID_ = 0
STYLE_DASH_ = 1
STYLE_DOT_ = 2
STYLE_DASHDOT_ = 3
STYLE_DASHDOTDOT_ = 4
_enum('STYLE', {0: 'STYLE_SOLID_', 1: 'STYLE_DASH_', 2: 'STYLE_DOT_', 3: 'STYLE_DASHDOT_', 4: 'STYLE_DASHDOTDOT_'})

# ---- inputs and global variables
CPeriod = _input('CPeriod', PERIOD_D1)
style_H5 = _input('style_H5', STYLE_DASHDOT)  # H5 level line style
style_H4 = _input('style_H4', STYLE_DASHDOTDOT)  # H4 level line style
style_H3 = _input('style_H3', STYLE_SOLID)  # H3 level line style
style_H2 = _input('style_H2', STYLE_DASHDOTDOT)  # H2 level line style
style_H1 = _input('style_H1', STYLE_DASHDOTDOT)  # H1 level line style
style_L1 = _input('style_L1', STYLE_DASHDOTDOT)  # L1 level line style
style_L2 = _input('style_L2', STYLE_DASHDOTDOT)  # L2 level line style
style_L3 = _input('style_L3', STYLE_SOLID)  # L3 level line style
style_L4 = _input('style_L4', STYLE_DASHDOTDOT)  # L4 level line style
style_L5 = _input('style_L5', STYLE_DASHDOT)  # L5 level line style
width_H5 = _input('width_H5', 1)  # H5 level width
width_H4 = _input('width_H4', 1)  # H4 level width
width_H3 = _input('width_H3', 2)  # H3 level width
width_H2 = _input('width_H2', 1)  # H2 level width
width_H1 = _input('width_H1', 1)  # H1 level width
width_L1 = _input('width_L1', 1)  # L1 level width
width_L2 = _input('width_L2', 1)  # L2 level width
width_L3 = _input('width_L3', 2)  # L3 level width
width_L4 = _input('width_L4', 1)  # L4 level width
width_L5 = _input('width_L5', 1)  # L5 level width

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
    pass

def OnDeinit(reason):
    ObjectDelete(0, 'Camarilla_Level_H5')
    ObjectDelete(0, 'Camarilla_Level_H4')
    ObjectDelete(0, 'Camarilla_Level_H3')
    ObjectDelete(0, 'Camarilla_Level_H2')
    ObjectDelete(0, 'Camarilla_Level_H1')
    ObjectDelete(0, 'Camarilla_Level_L1')
    ObjectDelete(0, 'Camarilla_Level_L2')
    ObjectDelete(0, 'Camarilla_Level_L3')
    ObjectDelete(0, 'Camarilla_Level_L4')
    ObjectDelete(0, 'Camarilla_Level_L5')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Period() >= CPeriod:
        Print('The period of the chart is more than necessary!!!')
        return 0
    if rates_total < 1:
        return 0
    iClose_ = Arr(0, 0.0)
    iHigh_ = Arr(0, 0.0)
    iLow_ = Arr(0, 0.0)
    Level_H1 = 0.0
    Level_H2 = 0.0
    Level_H3 = 0.0
    Level_H4 = 0.0
    Level_H5 = 0.0
    Level_L1 = 0.0
    Level_L2 = 0.0
    Level_L3 = 0.0
    Level_L4 = 0.0
    Level_L5 = 0.0
    if CopyClose(None, CPeriod, 1, 1, iClose_) < 1:
        return 0
    if CopyHigh(None, CPeriod, 1, 1, iHigh_) < 1:
        return 0
    if CopyLow(None, CPeriod, 1, 1, iLow_) < 1:
        return 0
    ArraySetAsSeries(iClose_, True)
    ArraySetAsSeries(iHigh_, True)
    ArraySetAsSeries(iLow_, True)
    Level_H1 = iClose_[0] + (((iHigh_[0] - iLow_[0]) * 1.1) / 12)
    Level_H2 = iClose_[0] + (((iHigh_[0] - iLow_[0]) * 1.1) / 6)
    Level_H3 = iClose_[0] + (((iHigh_[0] - iLow_[0]) * 1.1) / 4)
    Level_H4 = iClose_[0] + (((iHigh_[0] - iLow_[0]) * 1.1) / 2)
    Level_H5 = _fdiv(iHigh_[0], iLow_[0]) * iClose_[0]
    Level_L1 = iClose_[0] - (((iHigh_[0] - iLow_[0]) * 1.1) / 12)
    Level_L2 = iClose_[0] - (((iHigh_[0] - iLow_[0]) * 1.1) / 6)
    Level_L3 = iClose_[0] - (((iHigh_[0] - iLow_[0]) * 1.1) / 4)
    Level_L4 = iClose_[0] - (((iHigh_[0] - iLow_[0]) * 1.1) / 2)
    Level_L5 = iClose_[0] - (Level_H5 - iClose_[0])
    SetHline(0, 'Camarilla_Level_H5', 0, Level_H5, color_H5, style_H5, width_H5, 'Camarilla Level H5 ' + DoubleToString(Level_H5, Digits()))
    SetHline(0, 'Camarilla_Level_H4', 0, Level_H4, color_H4, style_H4, width_H4, 'Camarilla Level H4 ' + DoubleToString(Level_H4, Digits()))
    SetHline(0, 'Camarilla_Level_H3', 0, Level_H3, color_H3, style_H3, width_H3, 'Camarilla Level H3 ' + DoubleToString(Level_H3, Digits()))
    SetHline(0, 'Camarilla_Level_H2', 0, Level_H2, color_H2, style_H2, width_H2, 'Camarilla Level H2 ' + DoubleToString(Level_H2, Digits()))
    SetHline(0, 'Camarilla_Level_H1', 0, Level_H1, color_H1, style_H1, width_H1, 'Camarilla Level H1 ' + DoubleToString(Level_H1, Digits()))
    SetHline(0, 'Camarilla_Level_L1', 0, Level_L1, color_L1, style_L1, width_L1, 'Camarilla Level L1 ' + DoubleToString(Level_L1, Digits()))
    SetHline(0, 'Camarilla_Level_L2', 0, Level_L2, color_L2, style_L2, width_L2, 'Camarilla Level L2 ' + DoubleToString(Level_L2, Digits()))
    SetHline(0, 'Camarilla_Level_L3', 0, Level_L3, color_L3, style_L3, width_L3, 'Camarilla Level L3 ' + DoubleToString(Level_L3, Digits()))
    SetHline(0, 'Camarilla_Level_L4', 0, Level_L4, color_L4, style_L4, width_L4, 'Camarilla Level L4 ' + DoubleToString(Level_L4, Digits()))
    SetHline(0, 'Camarilla_Level_L5', 0, Level_L5, color_L5, style_L5, width_L5, 'Camarilla Level L5 ' + DoubleToString(Level_L5, Digits()))
    return rates_total

# ---- global variables initialised from expressions
color_H5 = _input('color_H5', _uint(Green))  # H5 level color
color_H4 = _input('color_H4', _uint(Lime))  # H4 level color
color_H3 = _input('color_H3', _uint(Lime))  # H3 level color
color_H2 = _input('color_H2', _uint(Green))  # H2 level color
color_H1 = _input('color_H1', _uint(DarkSlateGray))  # H1 level color
color_L1 = _input('color_L1', _uint(Purple))  # L1 level color
color_L2 = _input('color_L2', _uint(Crimson))  # L2 level color
color_L3 = _input('color_L3', _uint(Red))  # L3 level color
color_L4 = _input('color_L4', _uint(Red))  # L4 level color
color_L5 = _input('color_L5', _uint(Crimson))  # L5 level color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CamarillaEquation(_MQL5Indicator):
    name = 'camarilla_equation'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CPeriod': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),
        'style_H5': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=3),  # H5 level line style
        'style_H4': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # H4 level line style
        'style_H3': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # H3 level line style
        'style_H2': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # H2 level line style
        'style_H1': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # H1 level line style
        'style_L1': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # L1 level line style
        'style_L2': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # L2 level line style
        'style_L3': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # L3 level line style
        'style_L4': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # L4 level line style
        'style_L5': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=3),  # L5 level line style
        'width_H5': 1,  # H5 level width
        'width_H4': 1,  # H4 level width
        'width_H3': 2,  # H3 level width
        'width_H2': 1,  # H2 level width
        'width_H1': 1,  # H1 level width
        'width_L1': 1,  # L1 level width
        'width_L2': 1,  # L2 level width
        'width_L3': 2,  # L3 level width
        'width_L4': 1,  # L4 level width
        'width_L5': 1,  # L5 level width
    }

