"""Trading_Day_Average — converted from MQL5: MQL5 Indicators/Dynamic channel of one trading day/Trading_Day_Average.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 4, 2: 1, 3: 1}, 'colors': {1: [65535], 2: [255], 3: [32768]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Cloud', 2: 'High', 3: 'Low'}, 'levels': [], 'description': [], 'name': 'Trading_Day_Average', 'source': 'MQL5 Indicators/Dynamic channel of one trading day/Trading_Day_Average.mq5', 'folder': 'Dynamic channel of one trading day', 'inputs': [{'mql': 'InpHourBegin', 'py': 'InpHourBegin', 'param': 'InpHourBegin', 'type': 'uchar', 'default': 3, 'label': 'Hour of the beginning of the day', 'sinput': False}, {'mql': 'InpMinutesBegin', 'py': 'InpMinutesBegin', 'param': 'InpMinutesBegin', 'type': 'uchar', 'default': 0, 'label': 'Minute of the beginning of the day', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpHourBegin = _input('InpHourBegin', 3)  # Hour of the beginning of the day
InpMinutesBegin = _input('InpMinutesBegin', 0)  # Minute of the beginning of the day
BufferCloud1 = Arr(0, 0.0)
BufferCloud2 = Arr(0, 0.0)
BufferLow = Arr(0, 0.0)
BufferHigh = Arr(0, 0.0)
hour_begin = 0
minutes_begin = 0
time_begin = 0

def OnInit():
    global hour_begin, minutes_begin
    hour_begin = (23 if (InpHourBegin > 23) else InpHourBegin)
    minutes_begin = (59 if (InpMinutesBegin > 59) else InpMinutesBegin)
    SetIndexBuffer(0, BufferCloud1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCloud2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHigh, INDICATOR_DATA)
    SetIndexBuffer(3, BufferLow, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trading day average')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    ArraySetAsSeries(BufferCloud1, True)
    ArraySetAsSeries(BufferCloud2, True)
    ArraySetAsSeries(BufferHigh, True)
    ArraySetAsSeries(BufferLow, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferCloud1, EMPTY_VALUE)
        ArrayInitialize(BufferCloud2, EMPTY_VALUE)
        ArrayInitialize(BufferHigh, EMPTY_VALUE)
        ArrayInitialize(BufferLow, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        last_begin = LastBegin(time[i], hour_begin, minutes_begin)
        if last_begin == 0:
            return 0
        if last_begin > time[i]:
            last_begin -= PeriodSeconds(PERIOD_D1)
        last_begin_bar = BarShift(Symbol(), PERIOD_CURRENT, last_begin)
        if last_begin_bar == WRONG_VALUE:
            return 0
        period = last_begin_bar - i + 1
        ma_high = GetMA(period, MODE_SMA, PRICE_HIGH, i)
        ma_low = GetMA(period, MODE_SMA, PRICE_LOW, i)
        if ma_high == WRONG_VALUE or ma_low == WRONG_VALUE:
            return 0
        BufferCloud1[i] = ma_high
        BufferHigh[i] = BufferCloud1[i]
        BufferCloud2[i] = ma_low
        BufferLow[i] = BufferCloud2[i]
    return rates_total

def LastBegin(time, hour, minutes):
    stm = MqlDateTime()
    tm = time
    if tm == 0:
        return 0
    TimeToStruct(tm, stm)
    stm.hour = hour
    stm.min = minutes
    return StructToTime(stm)

def BarShift(symbol_name, timeframe, time):
    res = WRONG_VALUE
    last_bar = 0
    if SeriesInfoInteger(symbol_name, timeframe, SERIES_LASTBAR_DATE, _ValRef(last_bar)):
        if time > last_bar:
            res = 0
        else:
            shift = Bars(symbol_name, timeframe, time, last_bar)
            if shift > 0:
                res = shift - 1
    return res

def GetMA(period, method, price, shift):
    array = Arr(0, 0.0)
    ResetLastError()
    handle = iMA(None, PERIOD_CURRENT, period, 0, method, price)
    if handle == INVALID_HANDLE:
        Print('Trading day average: Error creating MA handle ', GetLastError(), ', recalculate now')
        return WRONG_VALUE
    if CopyBuffer(handle, 0, shift, 1, array) == 1:
        return array[0]
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TradingDayAverage(_MQL5Indicator):
    name = 'Trading_Day_Average'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpHourBegin': 3,  # Hour of the beginning of the day
        'InpMinutesBegin': 0,  # Minute of the beginning of the day
    }

