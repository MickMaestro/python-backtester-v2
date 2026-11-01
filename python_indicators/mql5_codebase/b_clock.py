"""b-clock — converted from MQL5: MQL5 Indicators/b-clock/b-clock.mq5

Copyright: Copyright 2013, Totom Sukopratomo; Link: https://login.mql5.com/en/users/tomsuk001; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, Totom Sukopratomo', 'link': 'https://login.mql5.com/en/users/tomsuk001', 'version': '2.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'b-clock', 'source': 'MQL5 Indicators/b-clock/b-clock.mq5', 'folder': 'b-clock', 'inputs': [{'mql': 'ShowComment', 'py': 'ShowComment', 'param': 'ShowComment', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'FontColor', 'py': 'FontColor', 'param': None, 'type': 'color', 'default': 11119017, 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'FontName', 'py': 'FontName', 'param': None, 'type': 'string', 'default': 'Tahoma', 'label': '', 'sinput': False}, {'mql': 'Offset', 'py': 'Offset', 'param': 'Offset', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ShowComment = _input('ShowComment', True)
FontColor = _input('FontColor', clrDarkGray)
FontSize = _input('FontSize', 10)
FontName = _input('FontName', 'Tahoma')
Offset = _input('Offset', 5)

def OnInit():
    return 0

def OnDeinit(reason):
    Comment('')
    ObjectDelete(0, 'time')

def OnCalculate(rates_total, prev_calculated, begin, price):
    rates = Arr(0, 0, factory=MqlRates)
    tick = MqlTick()
    SymbolInfoTick(Symbol(), tick)
    if CopyRates(Symbol(), PERIOD_CURRENT, 0, 1, rates) < 1:
        return 0
    i = 0.0
    m = 0
    s = 0
    m = rates[0].time + (GetMinute() * 60) - tick.time
    i = m / 60.0
    s = _imod(m, 60)
    m = _idiv(m - _imod(m, 60), 60)
    if ShowComment:
        Comment(IntegerToString(m, 0, 32) + ' minutes ' + IntegerToString(s, 0, 32) + ' seconds left to bar end')
    text = '  <' + IntegerToString(m, 0, 32) + ':' + IntegerToString(s, 0, 32)
    if ObjectFind(0, 'time') < 1:
        ObjectCreate(0, 'time', OBJ_TEXT, 0, rates[0].time, tick.bid + (Point() * Offset))
        ObjectSetString(0, 'time', OBJPROP_TEXT, text)
        ObjectSetInteger(0, 'time', OBJPROP_COLOR, FontColor)
        ObjectSetInteger(0, 'time', OBJPROP_FONTSIZE, FontSize)
        ObjectSetString(0, 'time', OBJPROP_FONT, FontName)
    else:
        ObjectSetString(0, 'time', OBJPROP_TEXT, text)
        ObjectMove(0, 'time', 0, rates[0].time, tick.bid + (Point() * Offset))
    return rates_total

def GetMinute():
    _sw1 = Period()
    if _sw1 == PERIOD_M1:
        return 1
    elif _sw1 == PERIOD_M2:
        return 2
    elif _sw1 == PERIOD_M3:
        return 3
    elif _sw1 == PERIOD_M4:
        return 4
    elif _sw1 == PERIOD_M5:
        return 5
    elif _sw1 == PERIOD_M6:
        return 6
    elif _sw1 == PERIOD_M10:
        return 10
    elif _sw1 == PERIOD_M12:
        return 12
    elif _sw1 == PERIOD_M15:
        return 15
    elif _sw1 == PERIOD_M20:
        return 20
    elif _sw1 == PERIOD_M30:
        return 30
    elif _sw1 == PERIOD_H1:
        return 60
    elif _sw1 == PERIOD_H2:
        return 120
    elif _sw1 == PERIOD_H3:
        return 180
    elif _sw1 == PERIOD_H4:
        return 240
    elif _sw1 == PERIOD_H6:
        return 360
    elif _sw1 == PERIOD_H8:
        return 480
    elif _sw1 == PERIOD_H12:
        return 720
    elif _sw1 == PERIOD_D1:
        return 1440
    elif _sw1 == PERIOD_W1:
        return 10080
    elif _sw1 == PERIOD_MN1:
        return 43200
    return 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BClock(_MQL5Indicator):
    name = 'b-clock'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ShowComment': True,
        'FontSize': 10,
        'Offset': 5,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

