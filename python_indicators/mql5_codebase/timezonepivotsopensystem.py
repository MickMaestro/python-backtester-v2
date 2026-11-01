"""TimeZonePivotsOpenSystem — converted from MQL5: MQL5 Indicators/TimeZonePivotsOpenSystem/TimeZonePivotsOpenSystem.mq5

Copyright: Copyright © 2005, ; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, ', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 17}, 'colors': {1: [16443110], 2: [16711680], 3: [13850042], 4: [3329330, 8421376, 8421504, 8388736, 9639167]}, 'widths': {2: 3, 3: 3}, 'styles': {1: 0, 3: 0}, 'labels': {1: 'TimeZonePivots', 2: 'Upper Zone', 3: 'Lower Zone', 4: 'TimeZonePivotsOpenSystem Open;TimeZonePivotsOpenSystem High;TimeZonePivotsOpenSystem Low;TimeZonePivotsOpenSystem Close'}, 'levels': [], 'description': [''], 'name': 'TimeZonePivotsOpenSystem', 'source': 'MQL5 Indicators/TimeZonePivotsOpenSystem/TimeZonePivotsOpenSystem.mq5', 'folder': 'TimeZonePivotsOpenSystem', 'inputs': [{'mql': 'StartH', 'py': 'StartH', 'param': 'StartH', 'type': 'int', 'default': 0, 'label': 'Старт расчёта канала (Часы)', 'sinput': False}, {'mql': 'Offset', 'py': 'Offset', 'param': 'Offset', 'type': 'uint', 'default': 100, 'label': 'ширина канала в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# ---- inputs and global variables
StartH = _input('StartH', ENUM_HOUR_0)  # Старт расчёта канала (Часы)
Offset = _input('Offset', 100)  # ширина канала в пунктах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
Up0Buffer = Arr(0, 0.0)
Dn0Buffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 4
    SetIndexBuffer(0, Up0Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Up0Buffer, True)
    SetIndexBuffer(1, Dn0Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Dn0Buffer, True)
    SetIndexBuffer(2, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(3, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(4, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'TimeZonePivots(', EnumToString(StartH, 'HOURS'), ', ', Offset, ')')
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
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtCloseBuffer[bar] = 0.0
        ExtLowBuffer[bar] = ExtCloseBuffer[bar]
        ExtHighBuffer[bar] = ExtLowBuffer[bar]
        ExtOpenBuffer[bar] = ExtHighBuffer[bar]
        ExtColorBuffer[bar] = 2.0
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
            if close[bar] > UpBuffer[bar]:
                ExtOpenBuffer[bar] = open[bar]
                ExtHighBuffer[bar] = high[bar]
                ExtLowBuffer[bar] = low[bar]
                ExtCloseBuffer[bar] = close[bar]
                if close[bar] >= open[bar]:
                    ExtColorBuffer[bar] = 0.0
                else:
                    ExtColorBuffer[bar] = 1.0
            if close[bar] < DnBuffer[bar]:
                ExtOpenBuffer[bar] = open[bar]
                ExtHighBuffer[bar] = high[bar]
                ExtLowBuffer[bar] = low[bar]
                ExtCloseBuffer[bar] = close[bar]
                if close[bar] <= open[bar]:
                    ExtColorBuffer[bar] = 4.0
                else:
                    ExtColorBuffer[bar] = 3.0
        else:
            Up0Buffer[bar] = 0.0
            UpBuffer[bar] = Up0Buffer[bar]
            Dn0Buffer[bar] = 0.0
            DnBuffer[bar] = Dn0Buffer[bar]
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


class TimeZonePivotsOpenSystem(_MQL5Indicator):
    name = 'TimeZonePivotsOpenSystem'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartH': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=0),  # Старт расчёта канала (Часы)
        'Offset': 100,  # ширина канала в пунктах
    }

