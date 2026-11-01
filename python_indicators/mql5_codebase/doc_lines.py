"""doc_lines — converted from MQL5: MQL5 Indicators/Grid Maker/doc_lines.mq5

Copyright: doc; Link: http://www.forex-tsd.com/; Version: 1.03

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'doc', 'link': 'http://www.forex-tsd.com/', 'version': '1.03', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'doc_lines', 'source': 'MQL5 Indicators/Grid Maker/doc_lines.mq5', 'folder': 'Grid Maker', 'inputs': [{'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'int', 'default': 1000, 'label': 'Step for horintal lines', 'sinput': False}, {'mql': 'max', 'py': 'max_', 'param': 'max_', 'type': 'double', 'default': 1.4, 'label': 'Max price value', 'sinput': False}, {'mql': 'min', 'py': 'min_', 'param': 'min_', 'type': 'double', 'default': 1.2, 'label': 'Min price value', 'sinput': False}, {'mql': 'Settings_H', 'py': 'Settings_H', 'param': None, 'type': 'string', 'default': 'Displacement for horizontal lines', 'label': '', 'sinput': False}, {'mql': 'Displacement1', 'py': 'Displacement1', 'param': 'Displacement1', 'type': 'int', 'default': 0, 'label': 'Level 0', 'sinput': False}, {'mql': 'Displacement2', 'py': 'Displacement2', 'param': 'Displacement2', 'type': 'int', 'default': 100, 'label': 'Displacement for long entry', 'sinput': False}, {'mql': 'Displacement3', 'py': 'Displacement3', 'param': 'Displacement3', 'type': 'int', 'default': 900, 'label': 'Displacement for short entry', 'sinput': False}, {'mql': 'Displacement4', 'py': 'Displacement4', 'param': 'Displacement4', 'type': 'int', 'default': 400, 'label': 'Displacement for TP long', 'sinput': False}, {'mql': 'Displacement5', 'py': 'Displacement5', 'param': 'Displacement5', 'type': 'int', 'default': 600, 'label': 'Displacement for TP short', 'sinput': False}, {'mql': 'Settings_V', 'py': 'Settings_V', 'param': None, 'type': 'string', 'default': 'Hours for vertical lines', 'label': '', 'sinput': False}, {'mql': 'StartLine0', 'py': 'StartLine0', 'param': None, 'type': 'string', 'default': '00:00', 'label': '', 'sinput': False}, {'mql': 'StartLine1', 'py': 'StartLine1', 'param': None, 'type': 'string', 'default': '05:00', 'label': '', 'sinput': False}, {'mql': 'StartLine2', 'py': 'StartLine2', 'param': None, 'type': 'string', 'default': '08:00', 'label': '', 'sinput': False}, {'mql': 'StartLine3', 'py': 'StartLine3', 'param': None, 'type': 'string', 'default': '15:30', 'label': '', 'sinput': False}, {'mql': 'StartLine4', 'py': 'StartLine4', 'param': None, 'type': 'string', 'default': '21:00', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Khaki = 0x8CE6F0  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name

# ---- inputs and global variables
Step = _input('Step', 1000)  # Step for horintal lines
max_ = _input('max_', 1.4)  # Max price value
min_ = _input('min_', 1.2)  # Min price value
Settings_H = _input('Settings_H', 'Displacement for horizontal lines')
Displacement1 = _input('Displacement1', 0)  # Level 0
Displacement2 = _input('Displacement2', 100)  # Displacement for long entry
Displacement3 = _input('Displacement3', 900)  # Displacement for short entry
Displacement4 = _input('Displacement4', 400)  # Displacement for TP long
Displacement5 = _input('Displacement5', 600)  # Displacement for TP short
Settings_V = _input('Settings_V', 'Hours for vertical lines')
StartLine0 = _input('StartLine0', '00:00')
StartLine1 = _input('StartLine1', '05:00')
StartLine2 = _input('StartLine2', '08:00')
StartLine3 = _input('StartLine3', '15:30')
StartLine4 = _input('StartLine4', '21:00')

def OnInit():
    return 0

def OnDeinit(reason):
    ObjectsDeleteAll(0, 0, OBJ_HLINE)
    ObjectsDeleteAll(0, 0, OBJ_VLINE)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Period() >= PERIOD_H4:
        return rates_total
    ObjectsDeleteAll(0, 0, OBJ_HLINE)
    Ris_H_Line()
    line_counter = 0
    str_ = MqlDateTime()
    stp = MqlDateTime()
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        TimeToStruct(time[i], str_)
        TimeToStruct(time[i] - 1, stp)
        startTime0 = StringToTime(TimeToString(time[i], TIME_DATE) + ' ' + StartLine0)
        startTime1 = StringToTime(TimeToString(time[i], TIME_DATE) + ' ' + StartLine1)
        startTime2 = StringToTime(TimeToString(time[i], TIME_DATE) + ' ' + StartLine2)
        startTime3 = StringToTime(TimeToString(time[i], TIME_DATE) + ' ' + StartLine3)
        startTime4 = StringToTime(TimeToString(time[i], TIME_DATE) + ' ' + StartLine4)
        if str_.day_of_year != stp.day_of_year:
            if str_.day_of_week > 0 and str_.day_of_week < 6:
                line_counter += 1
                SetVLine0('Vline_0_' + _str(line_counter), startTime0, zero)
                SetVLine1('Vline_1_' + _str(line_counter), startTime1, inter)
                SetVLine1('Vline_2_' + _str(line_counter), startTime2, inter)
                SetVLine1('Vline_3_' + _str(line_counter), startTime3, inter)
                SetVLine1('Vline_4_' + _str(line_counter), startTime4, inter)
    return rates_total

def SetVLine0(nm, t1, cl=_uint(Red)):
    if t1 <= 0:
        return
    if ObjectFind(0, nm) < 0:
        ObjectCreate(0, nm, OBJ_VLINE, 0, t1, 2)
    ObjectSetInteger(0, nm, OBJPROP_TIME, t1)
    ObjectSetInteger(0, nm, OBJPROP_COLOR, cl)
    ObjectSetInteger(0, nm, OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(0, nm, OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, nm, OBJPROP_BACK, True)
    ObjectSetInteger(0, nm, OBJPROP_SELECTABLE, False)

def SetVLine1(lm, t2, c2=_uint(Red)):
    if t2 <= 0:
        return
    if ObjectFind(0, lm) < 0:
        ObjectCreate(0, lm, OBJ_VLINE, 0, t2, 2)
    ObjectSetInteger(0, lm, OBJPROP_TIME, t2)
    ObjectSetInteger(0, lm, OBJPROP_COLOR, c2)
    ObjectSetInteger(0, lm, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, lm, OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, lm, OBJPROP_BACK, True)
    ObjectSetInteger(0, lm, OBJPROP_SELECTABLE, False)

def SetHLine1(nm, p1, cl=_uint(Red)):
    if ObjectFind(0, nm) < 0:
        ObjectCreate(0, nm, OBJ_HLINE, 0, 0, p1)
    ObjectSetInteger(0, nm, OBJPROP_COLOR, cl)
    ObjectSetInteger(0, nm, OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(0, nm, OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, nm, OBJPROP_SELECTABLE, False)

def SetHLine2(xc, p2, c2=_uint(Red)):
    if ObjectFind(0, xc) < 0:
        ObjectCreate(0, xc, OBJ_HLINE, 0, 0, p2)
    ObjectSetInteger(0, xc, OBJPROP_COLOR, c2)
    ObjectSetInteger(0, xc, OBJPROP_STYLE, STYLE_DASH)
    ObjectSetInteger(0, xc, OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, xc, OBJPROP_SELECTABLE, False)

def SetHLine3(xv, p3, c3=_uint(Red)):
    if ObjectFind(0, xv) < 0:
        ObjectCreate(0, xv, OBJ_HLINE, 0, 0, p3)
    ObjectSetInteger(0, xv, OBJPROP_COLOR, c3)
    ObjectSetInteger(0, xv, OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(0, xv, OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, xv, OBJPROP_SELECTABLE, False)

def Ris_H_Line():
    Uroven1 = 0.0
    Uroven2 = 0.0
    Uroven3 = 0.0
    Uroven4 = 0.0
    Uroven5 = 0.0
    line_counter = 0
    i = 0
    while Uroven1 <= max_:
        i += 1
        Uroven1 = ((i * Step) + Displacement1) * Point()
        Uroven2 = ((i * Step) + Displacement2) * Point()
        Uroven3 = ((i * Step) + Displacement3) * Point()
        Uroven4 = ((i * Step) + Displacement4) * Point()
        Uroven5 = ((i * Step) + Displacement5) * Point()
        if Uroven1 >= min_:
            line_counter += 1
            SetHLine1('Hline_0_' + _str(line_counter), Uroven1, H_zero)
            SetHLine2('Hline_1_' + _str(line_counter), Uroven2, H_entry)
            SetHLine2('Hline_2_' + _str(line_counter), Uroven3, H_entry)
            SetHLine3('Hline_3_' + _str(line_counter), Uroven4, H_tp)
            SetHLine3('Hline_4_' + _str(line_counter), Uroven5, H_tp)
    ChartRedraw()

# ---- global variables initialised from expressions
zero = _uint(Red)
inter = _uint(Khaki)
H_zero = _uint(Red)
H_entry = _uint(Yellow)
H_tp = _uint(Lime)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DocLines(_MQL5Indicator):
    name = 'doc_lines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Step': 1000,  # Step for horintal lines
        'max_': 1.4,  # Max price value
        'min_': 1.2,  # Min price value
        'Displacement1': 0,  # Level 0
        'Displacement2': 100,  # Displacement for long entry
        'Displacement3': 900,  # Displacement for short entry
        'Displacement4': 400,  # Displacement for TP long
        'Displacement5': 600,  # Displacement for TP short
    }

