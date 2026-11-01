"""spread — converted from MQL5: MQL5 Indicators/Spread/spread.mq5

Spread - displays current spread in the chart window.
Font, location and normalization can be defined in input parameters.
Copyright: Copyright © 2009, Andriy Moraru; Link: http://www.earnforex.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Andriy Moraru', 'link': 'http://www.earnforex.com', 'version': '1.01', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Spread - displays current spread in the chart window.', 'Font, location and normalization can be defined in input parameters.'], 'name': 'spread', 'source': 'MQL5 Indicators/Spread/spread.mq5', 'folder': 'Spread', 'inputs': [{'mql': 'font_color', 'py': 'font_color', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'font_size', 'py': 'font_size', 'param': 'font_size', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'font_face', 'py': 'font_face', 'param': None, 'type': 'string', 'default': 'Arial', 'label': '', 'sinput': False}, {'mql': 'corner', 'py': 'corner', 'param': 'corner', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'spread_distance_x', 'py': 'spread_distance_x', 'param': 'spread_distance_x', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'spread_distance_y', 'py': 'spread_distance_y', 'param': 'spread_distance_y', 'type': 'int', 'default': 130, 'label': '', 'sinput': False}, {'mql': 'normalize', 'py': 'normalize', 'param': 'normalize', 'type': 'bool', 'default': False, 'label': 'If true then the spread is normalized to traditional pips', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
font_size = _input('font_size', 14)
font_face = _input('font_face', 'Arial')
corner = _input('corner', ANCHOR_LEFT_UPPER)
spread_distance_x = _input('spread_distance_x', 10)
spread_distance_y = _input('spread_distance_y', 130)
normalize = _input('normalize', False)  # If true then the spread is normalized to traditional pips
Poin = 0.0
n_digits = 0
divider = 1.0

def OnInit():
    global Poin, divider, n_digits
    IndicatorSetString(INDICATOR_SHORTNAME, 'Spread')
    if Point() == 1e-05:
        Poin = 0.0001
    elif Point() == 0.001:
        Poin = 0.01
    else:
        Poin = Point()
    ObjectCreate(0, 'Spread', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'Spread', OBJPROP_ANCHOR, corner)
    ObjectSetInteger(0, 'Spread', OBJPROP_XDISTANCE, spread_distance_x)
    ObjectSetInteger(0, 'Spread', OBJPROP_YDISTANCE, spread_distance_y)
    spread = float(SymbolInfoInteger(Symbol(), SYMBOL_SPREAD))
    if Poin > Point() and normalize:
        divider = 10.0
        n_digits = 1
    ObjectSetString(0, 'Spread', OBJPROP_TEXT, 'Spread: ' + DoubleToString(NormalizeDouble(_fdiv(spread, divider), 1), n_digits) + ' points.')
    ObjectSetString(0, 'Spread', OBJPROP_FONT, font_face)
    ObjectSetInteger(0, 'Spread', OBJPROP_FONTSIZE, font_size)
    ObjectSetInteger(0, 'Spread', OBJPROP_COLOR, font_color)

def OnDeinit(reason):
    ObjectDelete(0, 'Spread')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    myspread = _fdiv(SymbolInfoDouble(Symbol(), SYMBOL_ASK) - SymbolInfoDouble(Symbol(), SYMBOL_BID), Point())
    ObjectSetString(0, 'Spread', OBJPROP_TEXT, 'Spread: ' + DoubleToString(NormalizeDouble(_fdiv(myspread, divider), 1), n_digits) + ' points.')
    ObjectSetString(0, 'Spread', OBJPROP_FONT, font_face)
    ObjectSetInteger(0, 'Spread', OBJPROP_FONTSIZE, font_size)
    ObjectSetInteger(0, 'Spread', OBJPROP_COLOR, font_color)
    return 0

# ---- global variables initialised from expressions
font_color = _input('font_color', _uint(Red))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Spread(_MQL5Indicator):
    name = 'spread'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'font_size': 14,
        'corner': _Choice({0: 'ANCHOR_LEFT_UPPER', 1: 'ANCHOR_LEFT', 2: 'ANCHOR_LEFT_LOWER', 3: 'ANCHOR_LOWER', 4: 'ANCHOR_RIGHT_LOWER', 5: 'ANCHOR_RIGHT', 6: 'ANCHOR_RIGHT_UPPER', 7: 'ANCHOR_UPPER', 8: 'ANCHOR_CENTER'}, default=0),
        'spread_distance_x': 10,
        'spread_distance_y': 130,
        'normalize': False,  # If true then the spread is normalized to traditional pips
    }

