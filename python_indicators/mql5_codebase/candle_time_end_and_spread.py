"""candle_time_end_and_spread — converted from MQL5: MQL5 Indicators/Candle Time End and Spread/candle_time_end_and_spread.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'candle_time_end_and_spread', 'source': 'MQL5 Indicators/Candle Time End and Spread/candle_time_end_and_spread.mq5', 'folder': 'Candle Time End and Spread', 'inputs': [{'mql': 'Clock_Color', 'py': 'Clock_Color', 'param': None, 'type': 'color', 'default': 6908265, 'label': '', 'sinput': False}, {'mql': 'Corner', 'py': 'Corner', 'param': 'Corner', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Clock_Color = _input('Clock_Color', clrDimGray)
Corner = _input('Corner', CORNER_RIGHT_UPPER)
objname = 'Spread&Bar'
s1 = Arr(0, 0.0)

def OnInit():
    ObjectCreate(0, objname, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, objname, OBJPROP_CORNER, Corner)
    ObjectSetInteger(0, objname, OBJPROP_XDISTANCE, 10)
    ObjectSetInteger(0, objname, OBJPROP_YDISTANCE, 2)
    Anchor = ANCHOR_LEFT_UPPER
    _sw1 = Corner
    if _sw1 == CORNER_LEFT_UPPER:
        Anchor = ANCHOR_LEFT_UPPER
    elif _sw1 == CORNER_RIGHT_UPPER:
        Anchor = ANCHOR_RIGHT_UPPER
    elif _sw1 == CORNER_LEFT_LOWER:
        Anchor = ANCHOR_LEFT_LOWER
    elif _sw1 == CORNER_RIGHT_LOWER:
        Anchor = ANCHOR_RIGHT_LOWER
    ObjectSetInteger(0, objname, OBJPROP_ANCHOR, Anchor)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, objname)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spreads):
    ArraySetAsSeries(time, True)
    m = _int(time[0] + PeriodSeconds() - TimeCurrent())
    s = _imod(m, 60)
    m = _idiv(m - s, 60)
    spread = SymbolInfoInteger(Symbol(), SYMBOL_SPREAD)
    _sp = ''
    _m = ''
    _s = ''
    if spread < 10:
        _sp = '..'
    elif spread < 100:
        _sp = '.'
    if m < 10:
        _m = '0'
    if s < 10:
        _s = '0'
    ObjectSetString(0, objname, OBJPROP_TEXT, 'Spread: ' + IntegerToString(spread) + _sp + ' Next Bar in ' + _m + IntegerToString(m) + ':' + _s + IntegerToString(s))
    ObjectSetInteger(0, objname, OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(0, objname, OBJPROP_COLOR, Clock_Color)
    ObjectSetString(0, objname, OBJPROP_FONT, 'Courier')
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleTimeEndAndSpread(_MQL5Indicator):
    name = 'candle_time_end_and_spread'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Corner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),
    }

