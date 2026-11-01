"""dailyrange — converted from MQL5: MQL5 Indicators/DailyRange/dailyrange.mq5

Copyright: Copyright © 2005, mishanya; Link: http://www.fxtradercenter.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, mishanya', 'link': 'http://www.fxtradercenter.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'dailyrange', 'source': 'MQL5 Indicators/DailyRange/dailyrange.mq5', 'folder': 'DailyRange', 'inputs': [{'mql': 'StepBack', 'py': 'StepBack', 'param': 'StepBack', 'type': 'uint', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Color_Res', 'py': 'Color_Res', 'param': None, 'type': 'color', 'default': 0, 'label': 'Color of Resistance level', 'sinput': False}, {'mql': 'Color_Sup', 'py': 'Color_Sup', 'param': None, 'type': 'color', 'default': 0, 'label': 'Color of Support level', 'sinput': False}, {'mql': 'Style_Res', 'py': 'Style_Res', 'param': 'Style_Res', 'type': 'int', 'default': 0, 'label': 'Style of Resistance level', 'sinput': False}, {'mql': 'Style_Sup', 'py': 'Style_Sup', 'param': 'Style_Sup', 'type': 'int', 'default': 0, 'label': 'Style of Support level', 'sinput': False}, {'mql': 'Width_Res', 'py': 'Width_Res', 'param': 'Width_Res', 'type': 'int', 'default': 2, 'label': 'Width of Resistance level', 'sinput': False}, {'mql': 'Width_Sup', 'py': 'Width_Sup', 'param': 'Width_Sup', 'type': 'int', 'default': 2, 'label': 'Width of Support level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Lime = 0x00FF00  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# enum Number
Number_0 = 0
Number_1 = 1
Number_2 = 2
Number_3 = 3
_enum('Number', {0: 'Number_0', 1: 'Number_1', 2: 'Number_2', 3: 'Number_3'})

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
StepBack = _input('StepBack', 0)
Style_Res = _input('Style_Res', SOLID_)  # Style of Resistance level
Style_Sup = _input('Style_Sup', SOLID_)  # Style of Support level
Width_Res = _input('Width_Res', Width_2)  # Width of Resistance level
Width_Sup = _input('Width_Sup', Width_2)  # Width of Support level
d = 0

def CreateHline(chart_id, name, nwin, price, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_HLINE, 0, 0, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)

def SetHline(chart_id, name, nwin, price, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateHline(chart_id, name, nwin, price, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, 0, price)

def OnInit():
    global d
    d = _int(1 + StepBack)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'DailyRange')

def OnDeinit(reason):
    ObjectDelete(0, 'DSup line')
    ObjectDelete(0, 'DRes line')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_res, _s_OnCalculate_sup
    if Period() >= PERIOD_D1:
        return 0
    if prev_calculated != rates_total:
        dOpen = Arr(0, 0.0)
        dClose = Arr(0, 0.0)
        dLow = Arr(0, 0.0)
        dHigh = Arr(0, 0.0)
        X = 0.0
        to_copy = d + 1
        if CopyOpen(Symbol(), PERIOD_D1, 0, to_copy, dOpen) <= 0:
            return 0
        if CopyClose(Symbol(), PERIOD_D1, 0, to_copy, dClose) <= 0:
            return 0
        if CopyLow(Symbol(), PERIOD_D1, 0, to_copy, dLow) <= 0:
            return 0
        if CopyHigh(Symbol(), PERIOD_D1, 0, to_copy, dHigh) <= 0:
            return 0
        ArraySetAsSeries(dOpen, True)
        ArraySetAsSeries(dClose, True)
        ArraySetAsSeries(dLow, True)
        ArraySetAsSeries(dHigh, True)
        X = dHigh[d] + dLow[d] + dClose[d]
        if dClose[d] < dOpen[d]:
            X += dLow[d]
        if dClose[d] > dOpen[d]:
            X += dHigh[d]
        if dClose[d] == dOpen[d]:
            X += dClose[d]
        X = X / 2
        _s_OnCalculate_res = X - dLow[d]
        _s_OnCalculate_sup = X - dHigh[d]
    SetHline(0, 'DSup line', 0, _s_OnCalculate_sup, Color_Sup, Style_Sup, Width_Sup, 'DSup line' + DoubleToString(_s_OnCalculate_sup, Digits()))
    SetHline(0, 'DRes line', 0, _s_OnCalculate_res, Color_Res, Style_Res, Width_Res, 'DRes line' + DoubleToString(_s_OnCalculate_res, Digits()))
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
Color_Res = _input('Color_Res', _uint(Lime))  # Color of Resistance level
Color_Sup = _input('Color_Sup', _uint(Red))  # Color of Support level

# ---- static local variables
_s_OnCalculate_sup = 0.0
_s_OnCalculate_res = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dailyrange(_MQL5Indicator):
    name = 'dailyrange'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StepBack': 0,
        'Style_Res': _Choice({0: 'solid', 1: 'dash', 2: 'dot', 3: 'dash-dot', 4: 'dash-dot-dot'}, default=0),  # Style of Resistance level
        'Style_Sup': _Choice({0: 'solid', 1: 'dash', 2: 'dot', 3: 'dash-dot', 4: 'dash-dot-dot'}, default=0),  # Style of Support level
        'Width_Res': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # Width of Resistance level
        'Width_Sup': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # Width of Support level
    }

