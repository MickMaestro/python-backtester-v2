"""spread_on_chart — converted from MQL5: MQL5 Indicators/spread_on_chart/spread_on_chart.mq5

Copyright: Copyright © 2010, Forexometer; Link: http://www.forexometer.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Forexometer', 'link': 'http://www.forexometer.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'spread_on_chart', 'source': 'MQL5 Indicators/spread_on_chart/spread_on_chart.mq5', 'folder': 'spread_on_chart', 'inputs': [{'mql': '_1', 'py': '_1', 'param': None, 'type': 'string', 'default': '// --- Place settings ---', 'label': '', 'sinput': False}, {'mql': 'Corner', 'py': 'Corner', 'param': 'Corner', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'XMargin', 'py': 'XMargin', 'param': 'XMargin', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'YMargin', 'py': 'YMargin', 'param': 'YMargin', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': '_2', 'py': '_2', 'param': None, 'type': 'string', 'default': '// --- Font settings ---', 'label': '', 'sinput': False}, {'mql': 'Font', 'py': 'Font', 'param': None, 'type': 'string', 'default': 'Arial', 'label': '', 'sinput': False}, {'mql': 'Color', 'py': 'Color', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Size', 'py': 'Size', 'param': 'Size', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DarkOrange = 0x008CFF  # MQL4 colour name

# enum enCorners
upper_left = 0
lower_left = 1
lower_right = 2
upper_right = 3
_enum('enCorners', {0: 'upper_left', 1: 'lower_left', 2: 'lower_right', 3: 'upper_right'})

# ---- inputs and global variables
_1 = _input('_1', '// --- Place settings ---')
Corner = _input('Corner', 0)
XMargin = _input('XMargin', 7)
YMargin = _input('YMargin', 12)
_2 = _input('_2', '// --- Font settings ---')
Font = _input('Font', 'Arial')
Size = _input('Size', 8)

def OnInit():
    iPlace_XMargin = 0
    if XMargin > 0:
        iPlace_XMargin = XMargin
    iPlace_YMargin = 0
    if YMargin > 0:
        iPlace_YMargin = YMargin
    iAnchor = 0
    _sw1 = Corner
    if _sw1 == 0:
        iAnchor = ANCHOR_LEFT_UPPER
    elif _sw1 == 1:
        iAnchor = ANCHOR_LEFT_LOWER
    elif _sw1 == 2:
        iAnchor = ANCHOR_RIGHT_LOWER
    elif _sw1 == 3:
        iAnchor = ANCHOR_RIGHT_UPPER
    ObjectCreate(0, 'spread', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'spread', OBJPROP_ANCHOR, iAnchor)
    ObjectSetInteger(0, 'spread', OBJPROP_CORNER, Corner)
    ObjectSetInteger(0, 'spread', OBJPROP_XDISTANCE, iPlace_XMargin)
    ObjectSetInteger(0, 'spread', OBJPROP_YDISTANCE, iPlace_YMargin)
    ObjectSetInteger(0, 'spread', OBJPROP_FONTSIZE, Size)
    ObjectSetString(0, 'spread', OBJPROP_FONT, Font)
    ObjectSetInteger(0, 'spread', OBJPROP_COLOR, Color)
    ObjectCreate(0, 'stoplevel', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'stoplevel', OBJPROP_ANCHOR, iAnchor)
    ObjectSetInteger(0, 'stoplevel', OBJPROP_CORNER, Corner)
    ObjectSetInteger(0, 'stoplevel', OBJPROP_XDISTANCE, iPlace_XMargin)
    ObjectSetInteger(0, 'stoplevel', OBJPROP_YDISTANCE, iPlace_YMargin + _int(1.5 * Size))
    ObjectSetInteger(0, 'stoplevel', OBJPROP_FONTSIZE, Size)
    ObjectSetString(0, 'stoplevel', OBJPROP_FONT, Font)
    ObjectSetInteger(0, 'stoplevel', OBJPROP_COLOR, Color)
    ObjectCreate(0, 'freezelevel', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'freezelevel', OBJPROP_ANCHOR, iAnchor)
    ObjectSetInteger(0, 'freezelevel', OBJPROP_CORNER, Corner)
    ObjectSetInteger(0, 'freezelevel', OBJPROP_XDISTANCE, iPlace_XMargin)
    ObjectSetInteger(0, 'freezelevel', OBJPROP_YDISTANCE, iPlace_YMargin + (3 * Size))
    ObjectSetInteger(0, 'freezelevel', OBJPROP_FONTSIZE, Size)
    ObjectSetString(0, 'freezelevel', OBJPROP_FONT, Font)
    ObjectSetInteger(0, 'freezelevel', OBJPROP_COLOR, Color)
    return 0

def OnDeinit(reason):
    ObjectDelete(0, 'spread')
    ObjectDelete(0, 'stoplevel')
    ObjectDelete(0, 'freezelevel')

def OnCalculate(rates_total, prev_calculated, begin, price):
    ObjectSetString(0, 'spread', OBJPROP_TEXT, 'spread = ' + DoubleToString(SymbolInfoInteger(Symbol(), SYMBOL_SPREAD), 1))
    ObjectSetString(0, 'stoplevel', OBJPROP_TEXT, 'stop level = ' + DoubleToString(SymbolInfoInteger(Symbol(), SYMBOL_TRADE_STOPS_LEVEL), 1))
    ObjectSetString(0, 'freezelevel', OBJPROP_TEXT, 'freeze level = ' + DoubleToString(SymbolInfoInteger(Symbol(), SYMBOL_TRADE_FREEZE_LEVEL), 1))
    return 0

# ---- global variables initialised from expressions
Color = _input('Color', _uint(DarkOrange))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SpreadOnChart(_MQL5Indicator):
    name = 'spread_on_chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Corner': _Choice({0: 'upper left', 1: 'lower left', 2: 'lower right', 3: 'upper right'}, default=0),
        'XMargin': 7,
        'YMargin': 12,
        'Size': 8,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

