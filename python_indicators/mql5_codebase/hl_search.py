"""HL_Search — converted from MQL5: MQL5 Indicators/Wick or Body High Low/HL_Search.mq5

Copyright: Copyright 2024, Rajesh Kumar Nait; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Rajesh Kumar Nait', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'HL_Search', 'source': 'MQL5 Indicators/Wick or Body High Low/HL_Search.mq5', 'folder': 'Wick or Body High Low', 'inputs': [{'mql': 'TextColor', 'py': 'TextColor', 'param': None, 'type': 'color', 'default': 16448255, 'label': '', 'sinput': False}, {'mql': 'TextFont', 'py': 'TextFont', 'param': None, 'type': 'string', 'default': 'Arial', 'label': '', 'sinput': False}, {'mql': 'TextSize', 'py': 'TextSize', 'param': 'TextSize', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Text_Adjustment', 'py': 'Text_Adjustment', 'param': 'Text_Adjustment', 'type': 'int', 'default': 2, 'label': 'Adjust High Low Text in points', 'sinput': False}, {'mql': 'SelectMode', 'py': 'SelectMode', 'param': 'SelectMode', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Mode
Wick_HL = 0
Body_HL = 1
_enum('Mode', {0: 'Wick_HL', 1: 'Body_HL'})

# ---- inputs and global variables
ind_h = 0
ind_l = 0
ind_db = 0
ind_dt = 0
lvb = 0
_fvb = 0
_clb = 0
fvb = -1
clb = -1
ind_l_cl = 0
ind_l_op = 0
l_lb = 0
ind_h_cl = 0
ind_h_op = 0
h_ub = 0
prefix = 'd_'
TextColor = _input('TextColor', clrSnow)
TextFont = _input('TextFont', 'Arial')
TextSize = _input('TextSize', 10)
Text_Adjustment = _input('Text_Adjustment', 2)  # Adjust High Low Text in points
showh2l = False
showl2h = False
SelectMode = _input('SelectMode', Body_HL)

def OnInit():
    global showh2l, showl2h
    ChartSetInteger(0, CHART_EVENT_OBJECT_CREATE, True)
    ChartSetInteger(0, CHART_EVENT_OBJECT_DELETE, True)
    showl2h = False
    showh2l = False
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)

def OnCalculate(rates_total, prev_calculated, time_, open_, high_, low_, close_, tick_volume, volume, spread):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        FindChartBars()

def FindChartBars():
    global _clb, _fvb, clb, fvb, h_ub, ind_h, ind_h_cl, ind_h_op, ind_l, ind_l_cl, ind_l_op, l_lb, lvb
    _fvb = _int(ChartGetInteger(ChartID(), CHART_FIRST_VISIBLE_BAR, 0))
    _clb = _int(ChartGetInteger(ChartID(), CHART_WIDTH_IN_BARS, 0))
    if _fvb > 0 and (_fvb != fvb or _clb != clb):
        lvb = _fvb - (_clb - 1)
        if lvb < 0:
            lvb = 0
        ind_h = iHighest(Symbol(), Period(), MODE_HIGH, _fvb - lvb, lvb)
        ind_l = iLowest(Symbol(), Period(), MODE_LOW, _fvb - lvb, lvb)
        ind_h_cl = iHighest(Symbol(), Period(), MODE_CLOSE, _fvb - lvb, lvb)
        ind_h_op = iHighest(Symbol(), Period(), MODE_OPEN, _fvb - lvb, lvb)
        if upperBody(ind_h_cl) > upperBody(ind_h_op):
            h_ub = ind_h_cl
        else:
            h_ub = ind_h_op
        if upperBody(ind_h_cl) == upperBody(ind_h_op):
            if ind_h_cl > ind_h_op:
                h_ub = ind_h_op
            else:
                h_ub = ind_h_cl
        if upperBody(h_ub) == upperBody(h_ub - 1):
            h_ub = h_ub - 1
        ind_l_cl = iLowest(Symbol(), Period(), MODE_CLOSE, _fvb - lvb, lvb)
        ind_l_op = iLowest(Symbol(), Period(), MODE_OPEN, _fvb - lvb, lvb)
        if lowerBody(ind_l_cl) > lowerBody(ind_l_op):
            l_lb = ind_l_op
        else:
            l_lb = ind_l_cl
        if lowerBody(ind_l_cl) == lowerBody(ind_l_op):
            if ind_l_cl > ind_l_op:
                l_lb = ind_l_op
            else:
                l_lb = ind_l_cl
        if lowerBody(l_lb) == lowerBody(l_lb - 1):
            l_lb = l_lb - 1
        if SelectMode == Wick_HL:
            TextCreate(0, prefix + 'High', 0, time(ind_h), high(ind_h) + (Text_Adjustment * Point()), DoubleToString(high(ind_h), Digits()), TextFont, TextSize, TextColor, 0.0, ANCHOR_CENTER, True, False, True, 0)
            TextCreate(0, prefix + 'Low', 0, time(ind_l), low(ind_l) - (Text_Adjustment * Point()), DoubleToString(low(ind_l), Digits()), TextFont, TextSize, TextColor, 0.0, ANCHOR_CENTER, True, False, True, 0)
        if SelectMode == Body_HL:
            TextCreate(0, prefix + 'High_UB', 0, time(h_ub), high(h_ub) + (Text_Adjustment * Point()), '' + DoubleToString(high(h_ub), Digits()), TextFont, TextSize, TextColor, 0.0, ANCHOR_CENTER, True, False, True, 0)
            TextCreate(0, prefix + 'Low_LB', 0, time(l_lb), low(l_lb) - (Text_Adjustment * Point()), '' + DoubleToString(low(l_lb), Digits()), TextFont, TextSize, TextColor, 0.0, ANCHOR_CENTER, True, False, True, 0)
        ChartRedraw()
        fvb = _fvb
        clb = _clb

def time(index):
    return iTime(None, 0, index)

def high(index):
    return iHigh(None, 0, index)

def low(index):
    return iLow(None, 0, index)

def open(index):
    return iOpen(None, 0, index)

def close(index):
    return iClose(None, 0, index)

def upperBody(index):
    return MathMax(open(index), close(index))

def lowerBody(index):
    return MathMin(open(index), close(index))

def TextCreate(chart_ID, name, sub_window, time_, price, text, font, font_size_, clr, angle, anchor, back, selection, hidden, z_order):
    ObjectCreate(chart_ID, name, OBJ_TEXT, sub_window, time_, price)
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
    ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
    ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size_)
    ObjectSetDouble(chart_ID, name, OBJPROP_ANGLE, angle)
    ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HLSearch(_MQL5Indicator):
    name = 'HL_Search'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TextSize': 10,
        'Text_Adjustment': 2,  # Adjust High Low Text in points
        'SelectMode': _Choice({0: 'Wick_HL', 1: 'Body_HL'}, default=1),
    }

