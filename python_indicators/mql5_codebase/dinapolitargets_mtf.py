"""dinapolitargets_mtf — converted from MQL5: MQL5 Indicators/DinapoliTargets_MTF/dinapolitargets_mtf.mq5

Copyright: Copyright © 2007, mishanya; Link: mishanya_fx@yahoo.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, mishanya', 'link': 'mishanya_fx@yahoo.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'dinapolitargets_mtf', 'source': 'MQL5 Indicators/DinapoliTargets_MTF/dinapolitargets_mtf.mq5', 'folder': 'DinapoliTargets_MTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 6, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'EndBar', 'py': 'EndBar', 'param': 'EndBar', 'type': 'uint', 'default': 1, 'label': 'End bar for calculation', 'sinput': False}, {'mql': 'Start_line_Color', 'py': 'Start_line_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Start level color', 'sinput': False}, {'mql': 'Start_line_Style', 'py': 'Start_line_Style', 'param': 'Start_line_Style', 'type': 'int', 'default': 0, 'label': 'Start level style', 'sinput': False}, {'mql': 'Start_line_Width', 'py': 'Start_line_Width', 'param': 'Start_line_Width', 'type': 'int', 'default': 2, 'label': 'Start line width', 'sinput': False}, {'mql': 'Target1_line_Color', 'py': 'Target1_line_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Target1 level color', 'sinput': False}, {'mql': 'Target1_line_Style', 'py': 'Target1_line_Style', 'param': 'Target1_line_Style', 'type': 'int', 'default': 1, 'label': 'Target1 level style', 'sinput': False}, {'mql': 'Target1_line_Width', 'py': 'Target1_line_Width', 'param': 'Target1_line_Width', 'type': 'int', 'default': 1, 'label': 'Target1 level width', 'sinput': False}, {'mql': 'Target2_line_Color', 'py': 'Target2_line_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Target2 level color', 'sinput': False}, {'mql': 'Target2_line_Style', 'py': 'Target2_line_Style', 'param': 'Target2_line_Style', 'type': 'int', 'default': 1, 'label': 'Target2 level style', 'sinput': False}, {'mql': 'Target2_line_Width', 'py': 'Target2_line_Width', 'param': 'Target2_line_Width', 'type': 'int', 'default': 1, 'label': 'Target2 level width', 'sinput': False}, {'mql': 'Target3_line_Color', 'py': 'Target3_line_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Target3 level color', 'sinput': False}, {'mql': 'Target3_line_Style', 'py': 'Target3_line_Style', 'param': 'Target3_line_Style', 'type': 'int', 'default': 1, 'label': 'Target3 level style', 'sinput': False}, {'mql': 'Target3_line_Width', 'py': 'Target3_line_Width', 'param': 'Target3_line_Width', 'type': 'int', 'default': 1, 'label': 'Target3 level width', 'sinput': False}, {'mql': 'Stop_line_Color', 'py': 'Stop_line_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Stop-loss level color', 'sinput': False}, {'mql': 'Stop_line_Style', 'py': 'Stop_line_Style', 'param': 'Stop_line_Style', 'type': 'int', 'default': 1, 'label': 'Stop-loss level style', 'sinput': False}, {'mql': 'Stop_line_Width', 'py': 'Stop_line_Width', 'param': 'Stop_line_Width', 'type': 'int', 'default': 1, 'label': 'End level width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DarkOrchid = 0xCC3299  # MQL4 colour name
Green = 0x008000  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name
Orange = 0x00A5FF  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# enum WIDTH
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('WIDTH', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
Length = _input('Length', 6)  # Smoothing period
EndBar = _input('EndBar', 1)  # End bar for calculation
Start_line_Style = _input('Start_line_Style', SOLID_)  # Start level style
Start_line_Width = _input('Start_line_Width', Width_2)  # Start line width
Target1_line_Style = _input('Target1_line_Style', DASH_)  # Target1 level style
Target1_line_Width = _input('Target1_line_Width', Width_1)  # Target1 level width
Target2_line_Style = _input('Target2_line_Style', DASH_)  # Target2 level style
Target2_line_Width = _input('Target2_line_Width', Width_1)  # Target2 level width
Target3_line_Style = _input('Target3_line_Style', DASH_)  # Target3 level style
Target3_line_Width = _input('Target3_line_Width', Width_1)  # Target3 level width
Stop_line_Style = _input('Stop_line_Style', DASH_)  # Stop-loss level style
Stop_line_Width = _input('Stop_line_Width', Width_1)  # End level width
Init = False
Dinapolis = Arr(0, 0.0)
min_rates_total = 0
Dinapoli_Handle = 0

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
    global Dinapoli_Handle, Init, min_rates_total
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('DinapoliTargets indicator chart period cannot be less than the current chart period')
        Init = False
        return 1
    Dinapoli_Handle = iCustom(None, TimeFrame, 'DinapoliTargets', Length, EndBar, Start_line_Color, Start_line_Style, Start_line_Width, Target1_line_Color, Target1_line_Style, Target1_line_Width, Target2_line_Color, Target2_line_Style, Target2_line_Width, Target3_line_Color, Target3_line_Style, Target3_line_Width, Stop_line_Color, Stop_line_Style, Stop_line_Width)
    if Dinapoli_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the DinapoliTargets indicator')
        return 1
    min_rates_total = _int(_idiv((Length + 4) * PeriodSeconds(TimeFrame), PeriodSeconds()))
    SetIndexBuffer(0, Dinapolis, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(Dinapolis, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dinapoli Targets')
    return 0

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, Time, Open, high, low, Close, Tick_volume, Volume, Spread):
    if BarsCalculated(Dinapoli_Handle) < min_rates_total or (not Init):
        return 0
    if BarsCalculated(Dinapoli_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    return rates_total

# ---- global variables initialised from expressions
Start_line_Color = _input('Start_line_Color', _uint(Magenta))  # Start level color
Target1_line_Color = _input('Target1_line_Color', _uint(Green))  # Target1 level color
Target2_line_Color = _input('Target2_line_Color', _uint(Orange))  # Target2 level color
Target3_line_Color = _input('Target3_line_Color', _uint(DarkOrchid))  # Target3 level color
Stop_line_Color = _input('Stop_line_Color', _uint(Red))  # Stop-loss level color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DinapolitargetsMtf(_MQL5Indicator):
    name = 'dinapolitargets_mtf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'Length': 6,  # Smoothing period
        'EndBar': 1,  # End bar for calculation
        'Start_line_Style': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # Start level style
        'Start_line_Width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # Start line width
        'Target1_line_Style': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=1),  # Target1 level style
        'Target1_line_Width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Target1 level width
        'Target2_line_Style': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=1),  # Target2 level style
        'Target2_line_Width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Target2 level width
        'Target3_line_Style': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=1),  # Target3 level style
        'Target3_line_Width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Target3 level width
        'Stop_line_Style': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=1),  # Stop-loss level style
        'Stop_line_Width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # End level width
    }

