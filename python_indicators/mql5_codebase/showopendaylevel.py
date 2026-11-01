"""showopendaylevel — converted from MQL5: MQL5 Indicators/ShowOpenDayLevel/showopendaylevel.mq5

Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711935]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'ShowOpenDayLevel'}, 'levels': [], 'description': [], 'name': 'showopendaylevel', 'source': 'MQL5 Indicators/ShowOpenDayLevel/showopendaylevel.mq5', 'folder': 'ShowOpenDayLevel', 'inputs': [{'mql': 'HourShift', 'py': 'HourShift', 'param': 'HourShift', 'type': 'int', 'default': 0, 'label': 'shift of determine time of the day start', 'sinput': False}, {'mql': 'SundayTab', 'py': 'SundayTab', 'param': 'SundayTab', 'type': 'int', 'default': 1, 'label': 'sundays tab', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum HOUR_SHIFT
H0 = 0
H1 = 1
H2 = 2
H3 = 3
H4 = 4
H5 = 5
H6 = 6
H7 = 7
H8 = 8
H9 = 9
H10 = 10
H11 = 11
H12 = 12
H13 = 13
H14 = 14
H15 = 15
H16 = 16
H17 = 17
H18 = 18
H19 = 19
H20 = 20
H21 = 21
H22 = 22
H23 = 23
_enum('HOUR_SHIFT', {0: 'H0', 1: 'H1', 2: 'H2', 3: 'H3', 4: 'H4', 5: 'H5', 6: 'H6', 7: 'H7', 8: 'H8', 9: 'H9', 10: 'H10', 11: 'H11', 12: 'H12', 13: 'H13', 14: 'H14', 15: 'H15', 16: 'H16', 17: 'H17', 18: 'H18', 19: 'H19', 20: 'H20', 21: 'H21', 22: 'H22', 23: 'H23'})

# enum DAY_MODE
Friday = 0
Sunday = 1
Monday = 2
_enum('DAY_MODE', {0: 'Friday', 1: 'Sunday', 2: 'Monday'})

# ---- inputs and global variables
HourShift = _input('HourShift', H0)  # shift of determine time of the day start
SundayTab = _input('SundayTab', Sunday)  # sundays tab
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 3
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 2)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'ShowOpenDayLevel( Shift = ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def GetLastOpen(Buffer, hshift, stab, Time, index):
    tm = MqlDateTime()
    TimeToStruct(Time[index + 0], tm)
    Hour0 = tm.hour
    DW0 = tm.day_of_week
    TimeToStruct(Time[index + 1], tm)
    Hour1 = tm.hour
    if DW0 == SUNDAY:
        _sw1 = SundayTab
        if _sw1 == Friday:
            Buffer[index] = Buffer[index + 1]
            return True
        elif _sw1 == Monday:
            if Hour1 != Hour0 and Hour0 == HourShift:
                iOpen_ = Arr(1, 0.0, dyn=False)
                if CopyOpen(Symbol(), PERIOD_H1, _DT(Time[index]), 1, iOpen_) <= 0:
                    return False
                Buffer[index] = iOpen_[0]
            else:
                Buffer[index] = Buffer[index + 1]
            return True
    if DW0 == MONDAY and SundayTab == Monday:
        Buffer[index] = Buffer[index + 1]
        return True
    if Hour1 != Hour0 and Hour0 == HourShift:
        iOpen_ = Arr(1, 0.0, dyn=False)
        if CopyOpen(Symbol(), PERIOD_H1, _DT(Time[index]), 1, iOpen_) <= 0:
            return False
        Buffer[index] = iOpen_[0]
    else:
        Buffer[index] = Buffer[index + 1]
    return True

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or Period() > PERIOD_H1:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if not GetLastOpen(IndBuffer, HourShift, (SundayTab != 0), time, bar):
            return 0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Showopendaylevel(_MQL5Indicator):
    name = 'showopendaylevel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HourShift': _Choice({0: '0', 1: '+1', 2: '+2', 3: '+3', 4: '+3', 5: '+5', 6: '+6', 7: '+7', 8: '+8', 9: '+9', 10: '+10', 11: '+11', 12: '+12', 13: '+13', 14: '+13', 15: '+15', 16: '+16', 17: '+17', 18: '+18', 19: '+19', 20: '+20', 21: '+21', 22: '+22', 23: '+23'}, default=0),  # shift of determine time of the day start
        'SundayTab': _Choice({0: 'how the end of fridays', 1: 'how the end of sundays', 2: 'how the start of mondays'}, default=1),  # sundays tab
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

