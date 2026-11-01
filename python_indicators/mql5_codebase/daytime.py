"""DayTime — converted from MQL5: MQL5 Indicators/DayTime/DayTime.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 1}, 'colors': {1: [16711680], 2: [255], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'UP', 2: 'Down', 3: 'Open'}, 'levels': [], 'description': [], 'name': 'DayTime', 'source': 'MQL5 Indicators/DayTime/DayTime.mq5', 'folder': 'DayTime', 'inputs': [{'mql': 'InpDay', 'py': 'InpDay', 'param': 'InpDay', 'type': 'int', 'default': 1, 'label': 'Day of week', 'sinput': False}, {'mql': 'InpHour', 'py': 'InpHour', 'param': 'InpHour', 'type': 'uint', 'default': 12, 'label': 'Hour of day', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpDay = _input('InpDay', MONDAY)  # Day of week
InpHour = _input('InpHour', 12)  # Hour of day
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferOP = Arr(0, 0.0)
hour = 0

def OnInit():
    global hour
    hour = (23 if (InpHour > 23) else InpHour)
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferOP, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DayTime(' + EnumToString(InpDay, 'ENUM_DAY_OF_WEEK') + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferOP, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        day_of_week = TimeDayOfWeek_u(time[i])
        hour_of_day = TimeHour_u(time[i])
        prev_hour_of_day = TimeHour_u(time[i + 1])
        if (day_of_week == WRONG_VALUE or hour_of_day == WRONG_VALUE) or prev_hour_of_day == WRONG_VALUE:
            return 0
        if (day_of_week == InpDay and hour_of_day == hour) and prev_hour_of_day != InpHour:
            index = BarShift(PERIOD_D1, time[i])
            PrevDayOpen = Open(PERIOD_D1, index + 1)
            TimePrevDayOpen = Time(PERIOD_D1, index + 1)
            IndexPrevDayOpen = BarShift(PERIOD_CURRENT, TimePrevDayOpen)
            j = IndexPrevDayOpen
            while j >= close[i + 1]:
                BufferOP[j] = PrevDayOpen
                j -= 1
            if close[i + 1] < PrevDayOpen:
                BufferUP[i] = low[i]
            elif close[i + 1] > PrevDayOpen:
                BufferDN[i] = high[i]
        else:
            BufferOP[i] = EMPTY_VALUE
            BufferUP[i] = BufferOP[i]
            BufferDN[i] = BufferUP[i]
    return rates_total

def TimeDayOfWeek_u(time):
    tm = MqlDateTime()
    if not TimeToStruct(time, tm):
        return WRONG_VALUE
    return tm.day_of_week

def TimeHour_u(time):
    tm = MqlDateTime()
    if not TimeToStruct(time, tm):
        return WRONG_VALUE
    return tm.hour

def BarShift(timeframe, time):
    res = WRONG_VALUE
    last_bar = Box(0)
    if SeriesInfoInteger(Symbol(), timeframe, SERIES_LASTBAR_DATE, last_bar):
        if time > last_bar.v:
            res = 0
        else:
            shift = Bars(Symbol(), timeframe, time, last_bar.v)
            if shift > 0:
                res = shift - 1
    return res

def Open(timeframe, index):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyOpen(Symbol(), timeframe, index, 1, array) == 1:
        return array[0]
    return 0.0

def Time(timeframe, index):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    if CopyTime(Symbol(), timeframe, index, 1, array) == 1:
        return array[0]
    return 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DayTime(_MQL5Indicator):
    name = 'DayTime'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpDay': _Choice({0: 'SUNDAY', 1: 'MONDAY', 2: 'TUESDAY', 3: 'WEDNESDAY', 4: 'THURSDAY', 5: 'FRIDAY', 6: 'SATURDAY'}, default=1),  # Day of week
        'InpHour': 12,  # Hour of day
    }

