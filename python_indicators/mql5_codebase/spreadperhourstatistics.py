"""spreadperhourstatistics — converted from MQL5: MQL5 Indicators/Spread per hour statistics/spreadperhourstatistics.mq5

Copyright: Copyright 2016, Alexander Sinitsyn; Link: https://www.mql5.com/en/users/wongv; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, Alexander Sinitsyn', 'link': 'https://www.mql5.com/en/users/wongv', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'spreadperhourstatistics', 'source': 'MQL5 Indicators/Spread per hour statistics/spreadperhourstatistics.mq5', 'folder': 'Spread per hour statistics', 'inputs': [{'mql': 'InpColor', 'py': 'InpColor', 'param': None, 'type': 'color', 'default': 11119017, 'label': 'Color', 'sinput': False}, {'mql': 'InpDayOfWeek', 'py': 'InpDayOfWeek', 'param': 'InpDayOfWeek', 'type': 'int', 'default': -1, 'label': 'Day of week', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DAY_OF_WEEK__
ANY_ = -1
MONDAY_ = 1
TUESDAY_ = 2
WEDNESDAY_ = 3
THURSDAY_ = 4
FRIDAY_ = 5
SATURDAY_ = 6
SUNDAY_ = 0
_enum('ENUM_DAY_OF_WEEK__', {-1: 'ANY_', 1: 'MONDAY_', 2: 'TUESDAY_', 3: 'WEDNESDAY_', 4: 'THURSDAY_', 5: 'FRIDAY_', 6: 'SATURDAY_', 0: 'SUNDAY_'})

# ---- inputs and global variables
InpColor = _input('InpColor', clrDarkGray)  # Color
InpDayOfWeek = _input('InpDayOfWeek', ANY_)  # Day of week
spread_c = Arr(24, 0.0, dyn=False)
spread_a = Arr(24, 0.0, dyn=False)

def OnInit():
    DebugAddLine(0)
    DebugAddLine(1)
    DebugAddLine(2)
    DebugAddLine(3)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    DebugRemoveLines()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    FillSpread()
    ShowSpread()
    return rates_total

def DebugAddLine(num):
    if num > 15 or num < -1:
        return
    line_height = 14
    lname = StringFormat('__lbl_w_%d', num)
    if ObjectFind(0, lname) != -1:
        ObjectDelete(0, lname)
    ObjectCreate(0, lname, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, lname, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(0, lname, OBJPROP_XDISTANCE, 288)
    ObjectSetInteger(0, lname, OBJPROP_YDISTANCE, 20 + (line_height * num))
    ObjectSetInteger(0, lname, OBJPROP_COLOR, (clrRed if (num == -1) else InpColor))
    ObjectSetString(0, lname, OBJPROP_FONT, 'Tahoma')
    ObjectSetString(0, lname, OBJPROP_TEXT, ' ')

def DebugPrint_1(line, msg):
    lname = StringFormat('__lbl_w_%d', line)
    ObjectSetString(0, lname, OBJPROP_TEXT, (msg if (msg != '') else ' '))

def DebugPrint_2(msg):
    DebugPrint_1(0, msg)

def DebugRemoveLines():
    for num in range(-1, 16):
        lname = StringFormat('__lbl_w_%d', num)
        if ObjectFind(0, lname) != -1:
            ObjectDelete(0, lname)

def StringJoin(in_array, precision=2, idx_from=0, idx_to=-1, separator=' '):
    result = Box('')
    __size = ArraySize(in_array) - 1
    __idx_to = (__size if (idx_to == -1) else MathMin(__size, idx_to))
    if __idx_to < idx_from:
        return 'error'
    for i in range(idx_from, __idx_to + 1):
        StringAdd(result, DoubleToString(in_array[i], precision))
        StringAdd(result, separator)
    StringTrimRight(result)
    return result.v

def FillSpread():
    tick = MqlTick()
    SymbolInfoTick(Symbol(), tick)
    __points = SymbolInfoDouble(Symbol(), SYMBOL_POINT)
    __spread = _int(MathRound(_fdiv(tick.ask - tick.bid, __points)))
    __mdt = MqlDateTime()
    TimeToStruct(TimeCurrent(), __mdt)
    if InpDayOfWeek == ANY_ or __mdt.day_of_week == InpDayOfWeek:
        spread_c[__mdt.hour] += 1
        spread_a[__mdt.hour] += __spread

def ShowSpread():
    avg_sp = Arr(24, 0.0, dyn=False)
    for i in range(0, 24):
        if spread_c[i] > 0:
            avg_sp[i] = _fdiv(spread_a[i], spread_c[i])
        else:
            avg_sp[i] = 0.0
    DebugPrint_1(0, 'spreads for ' + (EnumToString(InpDayOfWeek, 'ENUM_DAY_OF_WEEK__') if (InpDayOfWeek != ANY_) else 'all days'))
    DebugPrint_1(1, '0-7    ' + StringJoin(avg_sp, 1, 0, 7, '  '))
    DebugPrint_1(2, '8-15  ' + StringJoin(avg_sp, 1, 8, 15, '  '))
    DebugPrint_1(3, '16-23 ' + StringJoin(avg_sp, 1, 16, 23, '  '))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Spreadperhourstatistics(_MQL5Indicator):
    name = 'spreadperhourstatistics'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpDayOfWeek': _Choice({-1: 'Any', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 0: 'Sunday'}, default=-1),  # Day of week
    }

