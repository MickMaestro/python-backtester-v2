"""Breakout — converted from MQL5: MQL5 Indicators/Breakout/Breakout.mq5

Breakout zones
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [255], 2: [255], 3: [16711935], 4: [16711935]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 2, 4: 2}, 'labels': {1: 'Upper period', 2: 'Lower period', 3: 'Upper area', 4: 'Lower area'}, 'levels': [], 'description': ['Breakout zones'], 'name': 'Breakout', 'source': 'MQL5 Indicators/Breakout/Breakout.mq5', 'folder': 'Breakout', 'inputs': [{'mql': 'InpHourBegin', 'py': 'InpHourBegin', 'param': 'InpHourBegin', 'type': 'uint', 'default': 0, 'label': '"Period" Hour begin', 'sinput': False}, {'mql': 'InpMinBegin', 'py': 'InpMinBegin', 'param': 'InpMinBegin', 'type': 'uint', 'default': 0, 'label': '"Period" Minutes begin', 'sinput': False}, {'mql': 'InpHourEnd', 'py': 'InpHourEnd', 'param': 'InpHourEnd', 'type': 'uint', 'default': 5, 'label': '"Period" Hour end', 'sinput': False}, {'mql': 'InpMinEnd', 'py': 'InpMinEnd', 'param': 'InpMinEnd', 'type': 'uint', 'default': 0, 'label': '"Period" Minutes end', 'sinput': False}, {'mql': 'InpHourEndArea', 'py': 'InpHourEndArea', 'param': 'InpHourEndArea', 'type': 'uint', 'default': 23, 'label': '"Area" Hour end', 'sinput': False}, {'mql': 'InpMinEndArea', 'py': 'InpMinEndArea', 'param': 'InpMinEndArea', 'type': 'uint', 'default': 0, 'label': '"Area" Minutes end', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpHourBegin = _input('InpHourBegin', 0)  # "Period" Hour begin
InpMinBegin = _input('InpMinBegin', 0)  # "Period" Minutes begin
InpHourEnd = _input('InpHourEnd', 5)  # "Period" Hour end
InpMinEnd = _input('InpMinEnd', 0)  # "Period" Minutes end
InpHourEndArea = _input('InpHourEndArea', 23)  # "Area" Hour end
InpMinEndArea = _input('InpMinEndArea', 0)  # "Area" Minutes end
BufferUpperPeriod = Arr(0, 0.0)
BufferLowerPeriod = Arr(0, 0.0)
BufferUpperArea = Arr(0, 0.0)
BufferLowerArea = Arr(0, 0.0)
hour_begin = 0
min_begin = 0
hour_end = 0
min_end = 0
hour_box_end = 0
min_box_end = 0
period_begin_min = 0
period_end_min = 0
box_end_mn = 0

def OnInit():
    global box_end_mn, hour_begin, hour_box_end, hour_end, min_begin, min_box_end, min_end, period_begin_min, period_end_min
    hour_begin = (23 if (InpHourBegin > 23) else InpHourBegin)
    min_begin = (59 if (InpMinBegin > 59) else InpMinBegin)
    hour_end = (23 if (InpHourEnd > 23) else InpHourEnd)
    min_end = (59 if (InpMinEnd > 59) else InpMinEnd)
    hour_box_end = (23 if (InpHourEndArea > 23) else hour_end if (InpHourEndArea < _uint(hour_end)) else InpHourEndArea)
    min_box_end = (59 if (InpMinEndArea > 59) else InpMinEndArea)
    period_begin_min = (60 * hour_begin) + min_begin
    period_end_min = (60 * hour_end) + min_end
    box_end_mn = (60 * hour_box_end) + min_box_end
    SetIndexBuffer(0, BufferUpperPeriod, INDICATOR_DATA)
    SetIndexBuffer(1, BufferLowerPeriod, INDICATOR_DATA)
    SetIndexBuffer(2, BufferUpperArea, INDICATOR_DATA)
    SetIndexBuffer(3, BufferLowerArea, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Breakout')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUpperPeriod, True)
    ArraySetAsSeries(BufferLowerPeriod, True)
    ArraySetAsSeries(BufferUpperArea, True)
    ArraySetAsSeries(BufferLowerArea, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferUpperPeriod, EMPTY_VALUE)
        ArrayInitialize(BufferLowerPeriod, EMPTY_VALUE)
        ArrayInitialize(BufferUpperArea, EMPTY_VALUE)
        ArrayInitialize(BufferLowerArea, EMPTY_VALUE)
    begin_bar = 0
    end_bar = 0
    min_price = 0.0
    max_price = 0.0
    for i in range(limit, 0 - 1, -1):
        cur_min = (TimeHour_u(time[i]) * 60) + TimeMinute_u(time[i])
        if ((period_end_min > period_begin_min and cur_min >= period_begin_min) and cur_min <= period_end_min) or (period_end_min < period_begin_min and (cur_min >= period_begin_min or cur_min <= period_end_min)):
            begin_bar = FindBar(InpHourBegin, InpMinBegin, time[i])
            if begin_bar == WRONG_VALUE:
                continue
            hb = Highest(begin_bar - i + 1, i)
            lb = Lowest(begin_bar - i + 1, i)
            if hb == WRONG_VALUE or lb == WRONG_VALUE:
                continue
            max_price = high[hb]
            min_price = low[lb]
            for j in range(begin_bar, i - 1, -1):
                BufferUpperPeriod[j] = max_price
                BufferLowerPeriod[j] = min_price
        else:
            BufferUpperPeriod[i] = EMPTY_VALUE
            BufferLowerPeriod[i] = EMPTY_VALUE
        if ((box_end_mn > period_end_min and cur_min >= period_end_min) and cur_min <= box_end_mn) or (box_end_mn < period_end_min and (cur_min >= period_end_min or cur_min <= box_end_mn)):
            begin_bar = FindBar(InpHourBegin, InpMinBegin, time[i])
            end_bar = FindBar(InpHourEnd, InpMinEnd, time[i])
            if begin_bar == WRONG_VALUE or end_bar == WRONG_VALUE:
                continue
            hb = Highest(begin_bar - end_bar + 1, end_bar)
            lb = Lowest(begin_bar - end_bar + 1, end_bar)
            if hb == WRONG_VALUE or lb == WRONG_VALUE:
                continue
            max_price = high[hb]
            min_price = low[lb]
            for j in range(end_bar, i - 1, -1):
                BufferUpperArea[j] = max_price
                BufferLowerArea[j] = min_price
        else:
            BufferUpperArea[i] = EMPTY_VALUE
            BufferLowerArea[i] = EMPTY_VALUE
    return rates_total

def TimeHour_u(time):
    tm = MqlDateTime()
    TimeToStruct(time, tm)
    return tm.hour

def TimeMinute_u(time):
    tm = MqlDateTime()
    TimeToStruct(time, tm)
    return tm.min

def FindBar(hour, minutes, time):
    tm = MqlDateTime()
    TimeToStruct(time, tm)
    tm.hour = hour
    tm.min = minutes
    t = StructToTime(tm)
    if t > time:
        t -= 86400
    return BarShift(Symbol(), PERIOD_CURRENT, t)

def BarShift(symbol_name, timeframe, time, exact=False):
    last_bar = Box(0)
    if not SeriesInfoInteger(symbol_name, timeframe, SERIES_LASTBAR_DATE, last_bar):
        array = Arr(1, 0, dyn=False)
        if CopyTime(symbol_name, timeframe, 0, 1, array) == 1:
            last_bar.v = array[0]
        else:
            return WRONG_VALUE
    if time > last_bar.v:
        return 0
    shift = Bars(symbol_name, timeframe, time, last_bar.v)
    array = Arr(1, 0, dyn=False)
    if CopyTime(symbol_name, timeframe, _DT(time), 1, array) == 1:
        return ((shift - 1) if (array[0] == time) else WRONG_VALUE if (exact and time > (array[0] + PeriodSeconds(timeframe))) else shift)
    return WRONG_VALUE

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMinimum(array) + start
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Breakout(_MQL5Indicator):
    name = 'Breakout'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpHourBegin': 0,  # "Period" Hour begin
        'InpMinBegin': 0,  # "Period" Minutes begin
        'InpHourEnd': 5,  # "Period" Hour end
        'InpMinEnd': 0,  # "Period" Minutes end
        'InpHourEndArea': 23,  # "Area" Hour end
        'InpMinEndArea': 0,  # "Area" Minutes end
    }

