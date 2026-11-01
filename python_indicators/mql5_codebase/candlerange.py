"""CandleRange — converted from MQL5: MQL5 Indicators/Candle Range/CandleRange.mq5

Candle Range - displays candle's pip range on mouseover.
Modifiable font parameters, location, and normalization.
Copyright: www.Wolfforex.com, 2024; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.Wolfforex.com, 2024', 'version': '1.01', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ["Candle Range - displays candle's pip range on mouseover.", 'Modifiable font parameters, location, and normalization.'], 'name': 'CandleRange', 'source': 'MQL5 Indicators/Candle Range/CandleRange.mq5', 'folder': 'Candle Range', 'inputs': [{'mql': 'ShowBodySize', 'py': 'ShowBodySize', 'param': 'ShowBodySize', 'type': 'bool', 'default': False, 'label': 'ShowBodySize: if true, body size will be shown too.', 'sinput': False}, {'mql': 'HavePipettes', 'py': 'HavePipettes', 'param': 'HavePipettes', 'type': 'bool', 'default': False, 'label': 'HavePipettes: if true, ranges will be divided by 10.', 'sinput': False}, {'mql': 'TrueRange', 'py': 'TrueRange', 'param': 'TrueRange', 'type': 'bool', 'default': False, 'label': 'TrueRange: if true, use true range formula.', 'sinput': False}, {'mql': 'font_color', 'py': 'font_color', 'param': None, 'type': 'color', 'default': 13882323, 'label': '', 'sinput': False}, {'mql': 'font_size', 'py': 'font_size', 'param': 'font_size', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'font_face', 'py': 'font_face', 'param': None, 'type': 'string', 'default': 'Verdana', 'label': '', 'sinput': False}, {'mql': 'corner', 'py': 'corner', 'param': 'corner', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'distance_x', 'py': 'distance_x', 'param': 'distance_x', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'distance_y', 'py': 'distance_y', 'param': 'distance_y', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'DrawTextAsBackground', 'py': 'DrawTextAsBackground', 'param': 'DrawTextAsBackground', 'type': 'bool', 'default': False, 'label': 'DrawTextAsBackground: if true, the text will be drawn as background.', 'sinput': False}, {'mql': 'ObjectPrefix', 'py': 'ObjectPrefix', 'param': None, 'type': 'string', 'default': 'CR-', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ShowBodySize = _input('ShowBodySize', False)  # ShowBodySize: if true, body size will be shown too.
HavePipettes = _input('HavePipettes', False)  # HavePipettes: if true, ranges will be divided by 10.
TrueRange = _input('TrueRange', False)  # TrueRange: if true, use true range formula.
font_color = _input('font_color', clrLightGray)
font_size = _input('font_size', 10)
font_face = _input('font_face', 'Verdana')
corner = _input('corner', CORNER_LEFT_UPPER)
distance_x = _input('distance_x', 3)
distance_y = _input('distance_y', 12)
DrawTextAsBackground = _input('DrawTextAsBackground', False)  # DrawTextAsBackground: if true, the text will be drawn as background.
ObjectPrefix = _input('ObjectPrefix', 'CR-')
n_digits = 0
divider = 1.0

def OnInit():
    global divider, n_digits
    ObjectCreate(ChartID(), ObjectPrefix + 'Range', OBJ_LABEL, 0, 0, 0)
    ObjectSetString(ChartID(), ObjectPrefix + 'Range', OBJPROP_TEXT, '')
    ObjectSetInteger(ChartID(), ObjectPrefix + 'Range', OBJPROP_FONTSIZE, font_size)
    ObjectSetString(ChartID(), ObjectPrefix + 'Range', OBJPROP_FONT, font_face)
    ObjectSetInteger(ChartID(), ObjectPrefix + 'Range', OBJPROP_COLOR, font_color)
    ObjectSetInteger(ChartID(), ObjectPrefix + 'Range', OBJPROP_CORNER, corner)
    ObjectSetInteger(ChartID(), ObjectPrefix + 'Range', OBJPROP_XDISTANCE, distance_x)
    ObjectSetInteger(ChartID(), ObjectPrefix + 'Range', OBJPROP_YDISTANCE, distance_y)
    ObjectSetInteger(ChartID(), ObjectPrefix + 'Range', OBJPROP_BACK, DrawTextAsBackground)
    if HavePipettes:
        divider = 10.0
        n_digits = 1
    ChartSetInteger(ChartID(), CHART_EVENT_MOUSE_MOVE, True)

def OnDeinit(reason):
    ObjectDelete(ChartID(), ObjectPrefix + 'Range')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OutputRange(range_, body):
    text = 'Range: ' + DoubleToString(Normalize(range_), n_digits)
    if ShowBodySize:
        text += ' Body: ' + DoubleToString(Normalize(body), n_digits)
    ObjectSetString(ChartID(), ObjectPrefix + 'Range', OBJPROP_TEXT, text)
    ChartRedraw()

def Normalize(distance):
    return NormalizeDouble(_fdiv(_fdiv(distance, Point()), divider), n_digits)

def OnChartEvent(id_, lparam, dparam, sparam):
    global _s_OnChartEvent_prev_body, _s_OnChartEvent_prev_range
    if id_ == CHARTEVENT_MOUSE_MOVE:
        subwindow = Box(0)
        time = Box(0)
        price = Box(0.0)
        ChartXYToTimePrice(ChartID(), _int(lparam), _int(dparam), subwindow, time, price)
        i = iBarShift(Symbol(), Period(), time.v, True)
        if i < 0:
            return
        range_ = iHigh(Symbol(), Period(), i) - iLow(Symbol(), Period(), i)
        if TrueRange:
            range0 = 0.0
            if i < (iBars(Symbol(), Period()) - 1):
                range0 = MathMax(MathAbs(iClose(Symbol(), Period(), i + 1) - iHigh(Symbol(), Period(), i)), MathAbs(iClose(Symbol(), Period(), i + 1) - iLow(Symbol(), Period(), i)))
            range_ = MathMax(range_, range0)
        body = MathAbs(iOpen(Symbol(), Period(), i) - iClose(Symbol(), Period(), i))
        if range_ == _s_OnChartEvent_prev_range and body == _s_OnChartEvent_prev_body:
            return
        _s_OnChartEvent_prev_range = range_
        _s_OnChartEvent_prev_body = body
        OutputRange(range_, body)

# ---- static local variables
_s_OnChartEvent_prev_range = 0.0
_s_OnChartEvent_prev_body = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleRange(_MQL5Indicator):
    name = 'CandleRange'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ShowBodySize': False,  # ShowBodySize: if true, body size will be shown too.
        'HavePipettes': False,  # HavePipettes: if true, ranges will be divided by 10.
        'TrueRange': False,  # TrueRange: if true, use true range formula.
        'font_size': 10,
        'corner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=0),
        'distance_x': 3,
        'distance_y': 12,
        'DrawTextAsBackground': False,  # DrawTextAsBackground: if true, the text will be drawn as background.
    }

