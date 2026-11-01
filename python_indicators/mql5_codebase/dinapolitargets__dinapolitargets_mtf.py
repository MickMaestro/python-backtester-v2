"""dinapolitargets — converted from MQL5: MQL5 Indicators/DinapoliTargets_MTF/dinapolitargets.mq5

Copyright: Copyright © 2007, mishanya; Link: mishanya_fx@yahoo.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, mishanya', 'link': 'mishanya_fx@yahoo.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'dinapolitargets', 'source': 'MQL5 Indicators/DinapoliTargets_MTF/dinapolitargets.mq5', 'folder': 'DinapoliTargets_MTF', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 6, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'EndBar', 'py': 'EndBar', 'param': 'EndBar', 'type': 'uint', 'default': 1, 'label': 'End bar for calculation', 'sinput': False}, {'mql': 'Start_line_Color', 'py': 'Start_line_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Start level color', 'sinput': False}, {'mql': 'Start_line_Style', 'py': 'Start_line_Style', 'param': 'Start_line_Style', 'type': 'int', 'default': 0, 'label': 'Start level style', 'sinput': False}, {'mql': 'Start_line_Width', 'py': 'Start_line_Width', 'param': 'Start_line_Width', 'type': 'int', 'default': 2, 'label': 'Start line width', 'sinput': False}, {'mql': 'Target1_line_Color', 'py': 'Target1_line_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Target1 level color', 'sinput': False}, {'mql': 'Target1_line_Style', 'py': 'Target1_line_Style', 'param': 'Target1_line_Style', 'type': 'int', 'default': 1, 'label': 'Target1 level style', 'sinput': False}, {'mql': 'Target1_line_Width', 'py': 'Target1_line_Width', 'param': 'Target1_line_Width', 'type': 'int', 'default': 1, 'label': 'Target1 level width', 'sinput': False}, {'mql': 'Target2_line_Color', 'py': 'Target2_line_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Target2 level color', 'sinput': False}, {'mql': 'Target2_line_Style', 'py': 'Target2_line_Style', 'param': 'Target2_line_Style', 'type': 'int', 'default': 1, 'label': 'Target2 level style', 'sinput': False}, {'mql': 'Target2_line_Width', 'py': 'Target2_line_Width', 'param': 'Target2_line_Width', 'type': 'int', 'default': 1, 'label': 'Target2 level width', 'sinput': False}, {'mql': 'Target3_line_Color', 'py': 'Target3_line_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Target3 level color', 'sinput': False}, {'mql': 'Target3_line_Style', 'py': 'Target3_line_Style', 'param': 'Target3_line_Style', 'type': 'int', 'default': 1, 'label': 'Target3 level style', 'sinput': False}, {'mql': 'Target3_line_Width', 'py': 'Target3_line_Width', 'param': 'Target3_line_Width', 'type': 'int', 'default': 1, 'label': 'Target3 level width', 'sinput': False}, {'mql': 'Stop_line_Color', 'py': 'Stop_line_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Stop-loss level color', 'sinput': False}, {'mql': 'Stop_line_Style', 'py': 'Stop_line_Style', 'param': 'Stop_line_Style', 'type': 'int', 'default': 1, 'label': 'Stop-loss level style', 'sinput': False}, {'mql': 'Stop_line_Width', 'py': 'Stop_line_Width', 'param': 'Stop_line_Width', 'type': 'int', 'default': 1, 'label': 'End level width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
min_rates_total = 0

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
    global min_rates_total
    min_rates_total = _int(Length + 4)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dinapoli Targets')

def OnDeinit(reason):
    ObjectDelete(0, 'Start line')
    ObjectDelete(0, 'Stop line')
    ObjectDelete(0, 'Target1 line')
    ObjectDelete(0, 'Target2 line')
    ObjectDelete(0, 'Target3 line')
    Comment('')

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_volume, Volume, Spread):
    global _s_OnCalculate_BH, _s_OnCalculate_BL, _s_OnCalculate_Swing_n, _s_OnCalculate_Uzel0, _s_OnCalculate_Uzel1, _s_OnCalculate_Uzel2
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Spread, True)
    limit = 0
    bar = 0
    Swing = 0
    i = 0
    PointA = 0.0
    PointB = 0.0
    PointC = 0.0
    Target1 = 0.0
    Target2 = 0.0
    Target3 = 0.0
    Start = 0.0
    Stop = 0.0
    LL = 0.0
    HH = 0.0
    spread = 0.0
    dPointBA = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_Uzel0 = 0.0
        _s_OnCalculate_Uzel1 = 0.0
        _s_OnCalculate_Uzel2 = 0.0
        Swing = 0
        _s_OnCalculate_Swing_n = 0
        startbar = _int(rates_total - min_rates_total + EndBar)
        _s_OnCalculate_BH = High[startbar]
        _s_OnCalculate_BL = Low[startbar]
        Start = 0.0
        Stop = 0.0
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, _int(EndBar) - 1, -1):
        LL = 10000000.0
        HH = -100000000.0
        i = _int(Length)
        for i in range(i, 1 - 1, -1):
            barl = bar + i
            if Low[i] < LL:
                LL = Low[barl]
            if High[i] > HH:
                HH = High[barl]
        else:
            i = _range_end(i, 1 - 1, -1)
        if Low[bar] < LL and High[bar] > HH:
            Swing = 2
        else:
            if Low[bar] < LL:
                Swing = -1
            if High[bar] > HH:
                Swing = 1
        if Swing != _s_OnCalculate_Swing_n and _s_OnCalculate_Swing_n != 0:
            if Swing == 2:
                Swing = -_s_OnCalculate_Swing_n
                _s_OnCalculate_BH = High[bar]
                _s_OnCalculate_BL = Low[bar]
            _s_OnCalculate_Uzel2 = _s_OnCalculate_Uzel1
            _s_OnCalculate_Uzel1 = _s_OnCalculate_Uzel0
            if Swing == 1:
                _s_OnCalculate_Uzel0 = _s_OnCalculate_BL
            if Swing == -1:
                _s_OnCalculate_Uzel0 = _s_OnCalculate_BH
            _s_OnCalculate_BH = High[bar]
            _s_OnCalculate_BL = Low[bar]
        if Swing == 1 and High[bar] >= _s_OnCalculate_BH:
            _s_OnCalculate_BH = High[bar]
        if Swing == -1 and Low[bar] <= _s_OnCalculate_BL:
            _s_OnCalculate_BL = Low[bar]
        _s_OnCalculate_Swing_n = Swing
    else:
        bar = _range_end(bar, _int(EndBar) - 1, -1)
    PointA = _s_OnCalculate_Uzel2
    PointB = _s_OnCalculate_Uzel1
    PointC = _s_OnCalculate_Uzel0
    Comment(DoubleToString(NormalizeDouble(PointA, Digits()), Digits()), ' ', DoubleToString(NormalizeDouble(PointB, Digits()), Digits()), ' ', DoubleToString(NormalizeDouble(PointC, Digits()), Digits()))
    dPointBA = PointB - PointA
    Target1 = NormalizeDouble((dPointBA * 0.618) + PointC, Digits())
    Target2 = dPointBA + PointC
    Target3 = NormalizeDouble((dPointBA * 1.618) + PointC, Digits())
    spread = Spread[EndBar] * Point()
    if PointB <= PointC:
        Start = NormalizeDouble((dPointBA * 0.318) + PointC, Digits()) - spread
        Stop = PointC + (2 * spread)
    if PointB > PointC:
        Start = NormalizeDouble((dPointBA * 0.318) + PointC, Digits()) + spread
        Stop = PointC - (2 * spread)
    SetHline(0, 'Start line', 0, Start, Start_line_Color, Start_line_Style, Start_line_Width, 'Start line ' + DoubleToString(Start, Digits()))
    SetHline(0, 'Target1 line', 0, Target1, Target1_line_Color, Target1_line_Style, Target1_line_Width, 'Target1 line ' + DoubleToString(Target1, Digits()))
    SetHline(0, 'Target2 line', 0, Target2, Target2_line_Color, Target2_line_Style, Target2_line_Width, 'Target2 line ' + DoubleToString(Target2, Digits()))
    SetHline(0, 'Target3 line', 0, Target3, Target3_line_Color, Target3_line_Style, Target3_line_Width, 'Target3 line ' + DoubleToString(Target3, Digits()))
    SetHline(0, 'Stop line', 0, Stop, Stop_line_Color, Stop_line_Style, Stop_line_Width, 'Stop line ' + DoubleToString(Stop, Digits()))
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
Start_line_Color = _input('Start_line_Color', _uint(Magenta))  # Start level color
Target1_line_Color = _input('Target1_line_Color', _uint(Green))  # Target1 level color
Target2_line_Color = _input('Target2_line_Color', _uint(Orange))  # Target2 level color
Target3_line_Color = _input('Target3_line_Color', _uint(DarkOrchid))  # Target3 level color
Stop_line_Color = _input('Stop_line_Color', _uint(Red))  # Stop-loss level color

# ---- static local variables
_s_OnCalculate_Uzel0 = 0.0
_s_OnCalculate_Uzel1 = 0.0
_s_OnCalculate_Uzel2 = 0.0
_s_OnCalculate_BH = 0.0
_s_OnCalculate_BL = 0.0
_s_OnCalculate_Swing_n = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dinapolitargets(_MQL5Indicator):
    name = 'dinapolitargets'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
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

