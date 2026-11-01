"""Spread — converted from MQL5: MQL5 Indicators/Spread indicator MT5/Spread.mq5

Spread - displays current spread in the chart window.
Modifiable font parameters, location, and normalization.
Copyright: https://t.me/ForexEaPremium; Link: https://t.me/ForexEaPremium; Version: 1.08

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://t.me/ForexEaPremium', 'link': 'https://t.me/ForexEaPremium', 'version': '1.08', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Spread - displays current spread in the chart window.', 'Modifiable font parameters, location, and normalization.'], 'name': 'Spread', 'source': 'MQL5 Indicators/Spread indicator MT5/Spread.mq5', 'folder': 'Spread indicator MT5', 'inputs': [{'mql': 'UseCustomPipSize', 'py': 'UseCustomPipSize', 'param': 'UseCustomPipSize', 'type': 'bool', 'default': False, 'label': 'UseCustomPipSize: if true, pip size will be based on DecimalPlaces input parameter.', 'sinput': False}, {'mql': 'DecimalPlaces', 'py': 'DecimalPlaces', 'param': 'DecimalPlaces', 'type': 'int', 'default': 0, 'label': 'DecimalPlaces: how many decimal places in a pip?', 'sinput': False}, {'mql': 'AlertIfSpreadAbove', 'py': 'AlertIfSpreadAbove', 'param': 'AlertIfSpreadAbove', 'type': 'double', 'default': 0.0, 'label': 'AlertIfSpreadAbove: if > 0 alert will sound when sprea above the value.', 'sinput': False}, {'mql': 'AlertNative', 'py': 'AlertNative', 'param': 'AlertNative', 'type': 'bool', 'default': True, 'label': 'AlertNative: Alert popup inside platform.', 'sinput': False}, {'mql': 'AlertSound', 'py': 'AlertSound', 'param': 'AlertSound', 'type': 'bool', 'default': False, 'label': 'AlertSound: Play a sound on alert.', 'sinput': False}, {'mql': 'AlertEmail', 'py': 'AlertEmail', 'param': 'AlertEmail', 'type': 'bool', 'default': False, 'label': 'AlertEmail: Send an email on alert.', 'sinput': False}, {'mql': 'AlertNotification', 'py': 'AlertNotification', 'param': 'AlertNotification', 'type': 'bool', 'default': False, 'label': 'AlertNotification: Send a push notification on alert.', 'sinput': False}, {'mql': 'DrawLabel', 'py': 'DrawLabel', 'param': 'DrawLabel', 'type': 'bool', 'default': False, 'label': 'DrawLabel: Draw spread as a line label.', 'sinput': False}, {'mql': 'font_color', 'py': 'font_color', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'font_size', 'py': 'font_size', 'param': 'font_size', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'font_face', 'py': 'font_face', 'param': None, 'type': 'string', 'default': 'Arial', 'label': '', 'sinput': False}, {'mql': 'corner', 'py': 'corner', 'param': 'corner', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'spread_distance_x', 'py': 'spread_distance_x', 'param': 'spread_distance_x', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'spread_distance_y', 'py': 'spread_distance_y', 'param': 'spread_distance_y', 'type': 'int', 'default': 130, 'label': '', 'sinput': False}, {'mql': 'DrawTextAsBackground', 'py': 'DrawTextAsBackground', 'param': 'DrawTextAsBackground', 'type': 'bool', 'default': False, 'label': 'DrawTextAsBackground: if true, the text will be drawn as background.', 'sinput': False}, {'mql': 'label_font_color', 'py': 'label_font_color', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'label_font_size', 'py': 'label_font_size', 'param': 'label_font_size', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'label_font_face', 'py': 'label_font_face', 'param': None, 'type': 'string', 'default': 'Courier', 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
UseCustomPipSize = _input('UseCustomPipSize', False)  # UseCustomPipSize: if true, pip size will be based on DecimalPlaces input parameter.
DecimalPlaces = _input('DecimalPlaces', 0)  # DecimalPlaces: how many decimal places in a pip?
AlertIfSpreadAbove = _input('AlertIfSpreadAbove', 0.0)  # AlertIfSpreadAbove: if > 0 alert will sound when sprea above the value.
AlertNative = _input('AlertNative', True)  # AlertNative: Alert popup inside platform.
AlertSound = _input('AlertSound', False)  # AlertSound: Play a sound on alert.
AlertEmail = _input('AlertEmail', False)  # AlertEmail: Send an email on alert.
AlertNotification = _input('AlertNotification', False)  # AlertNotification: Send a push notification on alert.
DrawLabel = _input('DrawLabel', False)  # DrawLabel: Draw spread as a line label.
font_color = _input('font_color', clrRed)
font_size = _input('font_size', 14)
font_face = _input('font_face', 'Arial')
corner = _input('corner', CORNER_LEFT_UPPER)
spread_distance_x = _input('spread_distance_x', 10)
spread_distance_y = _input('spread_distance_y', 130)
DrawTextAsBackground = _input('DrawTextAsBackground', False)  # DrawTextAsBackground: if true, the text will be drawn as background.
label_font_color = _input('label_font_color', clrRed)
label_font_size = _input('label_font_size', 13)
label_font_face = _input('label_font_face', 'Courier')
n_digits = 0
divider = 1.0
alert_done = False

def OnInit():
    global divider, n_digits
    IndicatorSetString(INDICATOR_SHORTNAME, 'Spread')
    ObjectCreate(0, 'Spread', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'Spread', OBJPROP_CORNER, corner)
    anchor = ANCHOR_LEFT_UPPER
    if corner == CORNER_LEFT_LOWER:
        anchor = ANCHOR_LEFT_LOWER
    elif corner == CORNER_RIGHT_LOWER:
        anchor = ANCHOR_RIGHT_LOWER
    elif corner == CORNER_RIGHT_UPPER:
        anchor = ANCHOR_RIGHT_UPPER
    ObjectSetInteger(0, 'Spread', OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(0, 'Spread', OBJPROP_XDISTANCE, spread_distance_x)
    ObjectSetInteger(0, 'Spread', OBJPROP_YDISTANCE, spread_distance_y)
    if DrawLabel:
        ObjectCreate(0, 'SpreadLabel', OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, 'SpreadLabel', OBJPROP_TIMEFRAMES, OBJ_ALL_PERIODS)
        ObjectSetInteger(0, 'SpreadLabel', OBJPROP_COLOR, label_font_color)
        ObjectSetInteger(0, 'SpreadLabel', OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, 'SpreadLabel', OBJPROP_HIDDEN, False)
        ObjectSetInteger(0, 'SpreadLabel', OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(0, 'SpreadLabel', OBJPROP_BACK, DrawTextAsBackground)
    if UseCustomPipSize:
        divider = _fdiv(MathPow(0.1, DecimalPlaces), Point())
        n_digits = _int(MathAbs(MathLog10(divider)))
    spread = float(SymbolInfoInteger(Symbol(), SYMBOL_SPREAD))
    OutputSpread(spread)
    ObjectSetString(0, 'Spread', OBJPROP_FONT, font_face)
    ObjectSetInteger(0, 'Spread', OBJPROP_FONTSIZE, font_size)
    ObjectSetInteger(0, 'Spread', OBJPROP_COLOR, font_color)

def OnDeinit(reason):
    ObjectDelete(0, 'Spread')
    ObjectDelete(0, 'SpreadLabel')

def OnCalculate(rates_total, prev_calculated, begin, price):
    global alert_done
    spread = _fdiv(SymbolInfoDouble(Symbol(), SYMBOL_ASK) - SymbolInfoDouble(Symbol(), SYMBOL_BID), Point())
    OutputSpread(spread)
    if DrawLabel:
        DrawPipsDifference('SpreadLabel', SymbolInfoDouble(Symbol(), SYMBOL_BID), SymbolInfoDouble(Symbol(), SYMBOL_ASK), label_font_color)
    if AlertIfSpreadAbove > 0:
        if NormalizeSpread(spread) < AlertIfSpreadAbove:
            alert_done = False
        elif not alert_done:
            if AlertNative:
                Alert('Spread = ', DoubleToString(NormalizeSpread(spread), n_digits))
            if AlertSound:
                PlaySound('alert.wav')
            if AlertEmail:
                SendMail(Symbol() + ' Spread = ' + DoubleToString(NormalizeSpread(spread), n_digits), Symbol() + ' Spread = ' + DoubleToString(NormalizeSpread(spread), n_digits))
            if AlertNotification:
                SendNotification(Symbol() + ' Spread = ' + DoubleToString(NormalizeSpread(spread), n_digits))
            alert_done = True
    return rates_total

def OutputSpread(spread):
    ObjectSetString(0, 'Spread', OBJPROP_TEXT, 'Spread: ' + DoubleToString(NormalizeSpread(spread), n_digits) + ' points.')

def NormalizeSpread(spread):
    return NormalizeDouble(_fdiv(spread, divider), n_digits)

def DrawPipsDifference(label, price1, price2, col):
    x = Box(0)
    y = Box(0)
    real_x = 0
    w = Box(0)
    h = Box(0)
    pips = DoubleToString(NormalizeSpread(_fdiv(MathAbs(price1 - price2), Point())), n_digits)
    ObjectSetString(0, label, OBJPROP_TEXT, pips)
    ObjectSetInteger(0, label, OBJPROP_FONTSIZE, label_font_size)
    ObjectSetString(0, label, OBJPROP_FONT, label_font_face)
    ObjectSetInteger(0, label, OBJPROP_COLOR, col)
    Time = Arr(1, 0, dyn=False)
    CopyTime(Symbol(), Period(), 0, 1, Time)
    real_x = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS) - 2
    ChartTimePriceToXY(0, 0, Time[0], price1, x, y)
    TextSetFont(label_font_face, (-label_font_size) * 10)
    TextGetSize(pips, w, h)
    ObjectSetInteger(0, label, OBJPROP_XDISTANCE, real_x - w.v)
    ObjectSetInteger(0, label, OBJPROP_YDISTANCE, y.v)

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ != CHARTEVENT_CHART_CHANGE:
        return
    if DrawLabel:
        DrawPipsDifference('SpreadLabel', SymbolInfoDouble(Symbol(), SYMBOL_BID), SymbolInfoDouble(Symbol(), SYMBOL_ASK), label_font_color)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Spread(_MQL5Indicator):
    name = 'Spread'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'UseCustomPipSize': False,  # UseCustomPipSize: if true, pip size will be based on DecimalPlaces input parameter.
        'DecimalPlaces': 0,  # DecimalPlaces: how many decimal places in a pip?
        'AlertIfSpreadAbove': 0.0,  # AlertIfSpreadAbove: if > 0 alert will sound when sprea above the value.
        'AlertNative': True,  # AlertNative: Alert popup inside platform.
        'AlertSound': False,  # AlertSound: Play a sound on alert.
        'AlertEmail': False,  # AlertEmail: Send an email on alert.
        'AlertNotification': False,  # AlertNotification: Send a push notification on alert.
        'DrawLabel': False,  # DrawLabel: Draw spread as a line label.
        'font_size': 14,
        'corner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=0),
        'spread_distance_x': 10,
        'spread_distance_y': 130,
        'DrawTextAsBackground': False,  # DrawTextAsBackground: if true, the text will be drawn as background.
        'label_font_size': 13,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

