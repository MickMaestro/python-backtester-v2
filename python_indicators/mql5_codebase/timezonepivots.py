"""TimeZonePivots — converted from MQL5: MQL5 Indicators/TimeZonePivots/TimeZonePivots.mq5

Copyright: Copyright © 2005, ; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, ', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [16443110], 2: [65280], 3: [42495]}, 'widths': {2: 3, 3: 3}, 'styles': {1: 0, 3: 0}, 'labels': {1: 'TimeZonePivots', 2: 'Upper Zone', 3: 'Lower Zone'}, 'levels': [], 'description': [''], 'name': 'TimeZonePivots', 'source': 'MQL5 Indicators/TimeZonePivots/TimeZonePivots.mq5', 'folder': 'TimeZonePivots', 'inputs': [{'mql': 'StartH', 'py': 'StartH', 'param': 'StartH', 'type': 'int', 'default': 0, 'label': 'Старт расчёта канала (Часы)', 'sinput': False}, {'mql': 'MiddleLine', 'py': 'MiddleLine', 'param': 'MiddleLine', 'type': 'int', 'default': 0, 'label': 'линия канала', 'sinput': False}, {'mql': 'Offset', 'py': 'Offset', 'param': 'Offset', 'type': 'uint', 'default': 100, 'label': 'ширина канала в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum HOURS
ENUM_HOUR_0 = 0
ENUM_HOUR_1 = 1
ENUM_HOUR_2 = 2
ENUM_HOUR_3 = 3
ENUM_HOUR_4 = 4
ENUM_HOUR_5 = 5
ENUM_HOUR_6 = 6
ENUM_HOUR_7 = 7
ENUM_HOUR_8 = 8
ENUM_HOUR_9 = 9
ENUM_HOUR_10 = 10
ENUM_HOUR_11 = 11
ENUM_HOUR_12 = 12
ENUM_HOUR_13 = 13
ENUM_HOUR_14 = 14
ENUM_HOUR_15 = 15
ENUM_HOUR_16 = 16
ENUM_HOUR_17 = 17
ENUM_HOUR_18 = 18
ENUM_HOUR_19 = 19
ENUM_HOUR_20 = 20
ENUM_HOUR_21 = 21
ENUM_HOUR_22 = 22
ENUM_HOUR_23 = 23
_enum('HOURS', {0: 'ENUM_HOUR_0', 1: 'ENUM_HOUR_1', 2: 'ENUM_HOUR_2', 3: 'ENUM_HOUR_3', 4: 'ENUM_HOUR_4', 5: 'ENUM_HOUR_5', 6: 'ENUM_HOUR_6', 7: 'ENUM_HOUR_7', 8: 'ENUM_HOUR_8', 9: 'ENUM_HOUR_9', 10: 'ENUM_HOUR_10', 11: 'ENUM_HOUR_11', 12: 'ENUM_HOUR_12', 13: 'ENUM_HOUR_13', 14: 'ENUM_HOUR_14', 15: 'ENUM_HOUR_15', 16: 'ENUM_HOUR_16', 17: 'ENUM_HOUR_17', 18: 'ENUM_HOUR_18', 19: 'ENUM_HOUR_19', 20: 'ENUM_HOUR_20', 21: 'ENUM_HOUR_21', 22: 'ENUM_HOUR_22', 23: 'ENUM_HOUR_23'})

# enum ENUM_MIDDLE_TYPE
MODE_PRICE_OPEN = 0
MODE_PRICE_CLOSE = 1
_enum('ENUM_MIDDLE_TYPE', {0: 'MODE_PRICE_OPEN', 1: 'MODE_PRICE_CLOSE'})

# ---- inputs and global variables
StartH = _input('StartH', ENUM_HOUR_0)  # Старт расчёта канала (Часы)
MiddleLine = _input('MiddleLine', MODE_PRICE_OPEN)  # линия канала
Offset = _input('Offset', 100)  # ширина канала в пунктах
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
Up0Buffer = Arr(0, 0.0)
Dn0Buffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 4
    SetIndexBuffer(0, Up0Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Up0Buffer, True)
    SetIndexBuffer(1, Dn0Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Dn0Buffer, True)
    SetIndexBuffer(2, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(3, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(DnBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'TimeZonePivots(', EnumToString(StartH, 'HOURS'), ', ', EnumToString(MiddleLine, 'ENUM_MIDDLE_TYPE'), ', ', Offset, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Last_bar, _s_OnCalculate_Last_day, _s_OnCalculate_Last_hour, _s_OnCalculate_Last_open
    if Period() > PERIOD_H1:
        Comment('Индикатору TimeZonePivots нужен ТФ младше H2!')
        return 0
    else:
        Comment('')
    if rates_total < min_rates_total:
        return 0
    bar = 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_Last_open = 0.0
        _s_OnCalculate_Last_day = -1
        _s_OnCalculate_Last_hour = -1
        _s_OnCalculate_Last_bar = 0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if MiddleLine == MODE_PRICE_OPEN:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            tm = MqlDateTime()
            TimeToStruct(time[bar], tm)
            if _s_OnCalculate_Last_day != tm.day and tm.hour == StartH:
                _s_OnCalculate_Last_day = tm.day
                _s_OnCalculate_Last_hour = tm.hour
                _s_OnCalculate_Last_open = open[bar]
                DnBuffer[bar + 2] = 0.0
                UpBuffer[bar + 2] = DnBuffer[bar + 2]
                DnBuffer[bar + 1] = UpBuffer[bar + 2]
                UpBuffer[bar + 1] = DnBuffer[bar + 1]
                Dn0Buffer[bar + 2] = 0.0
                Up0Buffer[bar + 2] = Dn0Buffer[bar + 2]
                Dn0Buffer[bar + 1] = Up0Buffer[bar + 2]
                Up0Buffer[bar + 1] = Dn0Buffer[bar + 1]
            if _s_OnCalculate_Last_day > 0:
                Up0Buffer[bar] = _s_OnCalculate_Last_open + (Offset * Point())
                UpBuffer[bar] = Up0Buffer[bar]
                Dn0Buffer[bar] = _s_OnCalculate_Last_open - (Offset * Point())
                DnBuffer[bar] = Dn0Buffer[bar]
            else:
                Up0Buffer[bar] = 0.0
                UpBuffer[bar] = Up0Buffer[bar]
                Dn0Buffer[bar] = 0.0
                DnBuffer[bar] = Dn0Buffer[bar]
        else:
            bar = _range_end(bar, 0 - 1, -1)
    if MiddleLine == MODE_PRICE_CLOSE:
        limit_ = limit + _s_OnCalculate_Last_bar
        _s_OnCalculate_Last_bar += limit
        bar = limit_
        for bar in range(bar, 0 - 1, -1):
            tm = MqlDateTime()
            TimeToStruct(time[bar], tm)
            if _s_OnCalculate_Last_day != tm.day and tm.hour == StartH:
                _s_OnCalculate_Last_bar = bar
                _s_OnCalculate_Last_day = tm.day
                _s_OnCalculate_Last_hour = tm.hour
                DnBuffer[bar + 2] = 0.0
                UpBuffer[bar + 2] = DnBuffer[bar + 2]
                DnBuffer[bar + 1] = UpBuffer[bar + 2]
                UpBuffer[bar + 1] = DnBuffer[bar + 1]
                Dn0Buffer[bar + 2] = 0.0
                Up0Buffer[bar + 2] = Dn0Buffer[bar + 2]
                Dn0Buffer[bar + 1] = Up0Buffer[bar + 2]
                Up0Buffer[bar + 1] = Dn0Buffer[bar + 1]
            for index in range(_s_OnCalculate_Last_bar, bar - 1, -1):
                if _s_OnCalculate_Last_day > 0:
                    Up0Buffer[index] = close[bar] + (Offset * Point())
                    UpBuffer[index] = Up0Buffer[index]
                    Dn0Buffer[index] = close[bar] - (Offset * Point())
                    DnBuffer[index] = Dn0Buffer[index]
                else:
                    Up0Buffer[index] = 0.0
                    UpBuffer[index] = Up0Buffer[index]
                    Dn0Buffer[index] = 0.0
                    DnBuffer[index] = Dn0Buffer[index]
        else:
            bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Last_open = 0.0
_s_OnCalculate_Last_day = 0
_s_OnCalculate_Last_hour = 0
_s_OnCalculate_Last_bar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TimeZonePivots(_MQL5Indicator):
    name = 'TimeZonePivots'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartH': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=0),  # Старт расчёта канала (Часы)
        'MiddleLine': _Choice({0: 'по цене открытия стартового часа', 1: 'по цене закрытия текущей свечи'}, default=0),  # линия канала
        'Offset': 100,  # ширина канала в пунктах
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

