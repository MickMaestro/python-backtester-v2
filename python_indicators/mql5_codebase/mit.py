"""MIT — converted from MQL5: MQL5 Indicators/MIT/MIT.mq5

Momentum In Time
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MIT', 2: 'Time begin'}, 'levels': [], 'description': ['Momentum In Time'], 'name': 'MIT', 'source': 'MQL5 Indicators/MIT/MIT.mq5', 'folder': 'MIT', 'inputs': [{'mql': 'InpHourBegin', 'py': 'InpHourBegin', 'param': 'InpHourBegin', 'type': 'uchar', 'default': 0, 'label': 'Hour begin', 'sinput': False}, {'mql': 'InpMinutesBegin', 'py': 'InpMinutesBegin', 'param': 'InpMinutesBegin', 'type': 'uchar', 'default': 0, 'label': 'Minutes begin', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpHourBegin = _input('InpHourBegin', 0)  # Hour begin
InpMinutesBegin = _input('InpMinutesBegin', 0)  # Minutes begin
BufferMIT = Arr(0, 0.0)
BufferBegin = Arr(0, 0.0)
hour = 0
minutes = 0

def OnInit():
    global hour, minutes
    hour = (23 if (InpHourBegin > 23) else InpHourBegin)
    minutes = (59 if (InpMinutesBegin > 59) else InpMinutesBegin)
    SetIndexBuffer(0, BufferMIT, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBegin, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MIT(' + IntegerToString(hour, 2, 48) + ':' + IntegerToString(minutes, 2, 48) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMIT, True)
    ArraySetAsSeries(BufferBegin, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 3
        ArrayInitialize(BufferMIT, 0)
        ArrayInitialize(BufferBegin, 0)
    for i in range(limit, 0 - 1, -1):
        if Period() < PERIOD_D1:
            day_index = BarShift("", PERIOD_D1, time[i])
            t = Time("", PERIOD_D1, day_index)
            if day_index == WRONG_VALUE or t == 0:
                continue
            t += (3600 * hour) + (60 * minutes)
            index = BarShift("", PERIOD_CURRENT, t, False)
            if index == WRONG_VALUE or index > (rates_total - 3):
                continue
            BufferMIT[i] = close[i] - open[index]
            BufferBegin[i] = (0 if (i == index) else EMPTY_VALUE)
        else:
            BufferMIT[i] = close[i] - open[i + 1]
    return rates_total

def Time(symbol_name, timeframe, shift):
    array = Arr(0, 0)
    return (array[0] if (CopyTime(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def BarShift(symbol_name, timeframe, time, exact=False):
    res = iBars_u_1(symbol_name, timeframe, time + 1, UINT_MAX)
    if exact:
        if (timeframe != PERIOD_MN1 or time > TimeCurrent()) and res == iBars_u_1(symbol_name, timeframe, time - PeriodSeconds(timeframe) + 1, UINT_MAX):
            return WRONG_VALUE
    return res

def iBars_u_1(symbol_name, timeframe, start_time, stop_time):
    global _s_iBars_LastBAR, _s_iBars_LastSymb, _s_iBars_LastTime, _s_iBars_LastTime0, _s_iBars_LastTimeCur, _s_iBars_LastTimeFrame, _s_iBars_PerSec, _s_iBars_PreBars, _s_iBars_PreBarsF, _s_iBars_PreBarsS, _s_iBars_flag, _s_iBars_max_bars
    if _s_iBars_max_bars is _UNSET:
        _s_iBars_max_bars = TerminalInfoInteger(TERMINAL_MAXBARS)
    TimeCur = 0
    if timeframe == 0:
        timeframe = Period()
    changeTF = _s_iBars_LastTimeFrame != timeframe
    changeSymb = _s_iBars_LastSymb != symbol_name
    change = (changeTF or changeSymb) or _s_iBars_flag
    _s_iBars_LastTimeFrame = timeframe
    _s_iBars_LastSymb = symbol_name
    if changeTF:
        _s_iBars_PerSec = PeriodSeconds(timeframe)
    if _s_iBars_PerSec == 0:
        _s_iBars_flag = True
        return 0
    if stop_time < start_time:
        TimeCur = stop_time
        stop_time = start_time
        start_time = TimeCur
    if changeSymb:
        if not SymbolInfoInteger(symbol_name, SYMBOL_SELECT):
            SymbolSelect(symbol_name, True)
            ChartRedraw()
    TimeCur = TimeCurrent()
    if timeframe == PERIOD_W1:
        TimeCur -= _imod(TimeCur + 345600, _s_iBars_PerSec)
    if timeframe < PERIOD_W1:
        TimeCur -= _imod(TimeCur, _s_iBars_PerSec)
    if start_time > TimeCur:
        _s_iBars_flag = True
        return 0
    if timeframe == PERIOD_MN1:
        dt = MqlDateTime()
        TimeToStruct(TimeCur, dt)
        TimeCur = (dt.year * 12) + dt.mon
    if (changeTF or changeSymb) or TimeCur != _s_iBars_LastTimeCur:
        _s_iBars_LastBAR = SeriesInfoInteger(symbol_name, timeframe, SERIES_LASTBAR_DATE)
    _s_iBars_LastTimeCur = TimeCur
    if start_time > _s_iBars_LastBAR:
        _s_iBars_flag = True
        return 0
    tS = 0
    tF = 0
    if timeframe == PERIOD_W1:
        tS = start_time - _imod(start_time + 345599, _s_iBars_PerSec) - 1
    elif timeframe < PERIOD_MN1:
        tS = start_time - _imod(start_time - 1, _s_iBars_PerSec) - 1
    else:
        dt = MqlDateTime()
        TimeToStruct(start_time - 1, dt)
        tS = (dt.year * 12) + dt.mon
    if change or tS != _s_iBars_LastTime:
        _s_iBars_PreBarsS = Bars(symbol_name, timeframe, start_time, UINT_MAX)
        _s_iBars_LastTime = tS
    if stop_time <= _s_iBars_LastBAR:
        if _s_iBars_PreBarsS >= _s_iBars_max_bars:
            _s_iBars_PreBars = Bars(symbol_name, timeframe, start_time, stop_time)
        else:
            if timeframe < PERIOD_W1:
                tF = stop_time - _imod(stop_time, _s_iBars_PerSec)
            elif timeframe == PERIOD_W1:
                tF = stop_time - _imod(stop_time + 345600, _s_iBars_PerSec)
            else:
                dt0 = MqlDateTime()
                TimeToStruct(stop_time - 1, dt0)
                tF = (dt0.year * 12) + dt0.mon
            if change or tF != _s_iBars_LastTime0:
                _s_iBars_PreBarsF = Bars(symbol_name, timeframe, stop_time + 1, UINT_MAX)
                _s_iBars_LastTime0 = tF
            _s_iBars_PreBars = _s_iBars_PreBarsS - _s_iBars_PreBarsF
    else:
        _s_iBars_PreBars = _s_iBars_PreBarsS
    _s_iBars_flag = False
    return _s_iBars_PreBars

def iBars_u_2(symbol_name, timeframe):
    return Bars(symbol_name, timeframe)

# ---- static local variables
_s_iBars_LastSymb = ""
_s_iBars_LastTimeFrame = 0
_s_iBars_LastTime = 0
_s_iBars_LastTime0 = 0
_s_iBars_PerSec = 0
_s_iBars_PreBars = 0
_s_iBars_PreBarsS = 0
_s_iBars_PreBarsF = 0
_s_iBars_LastBAR = 0
_s_iBars_LastTimeCur = 0
_s_iBars_flag = True
_s_iBars_max_bars = _UNSET


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MIT(_MQL5Indicator):
    name = 'MIT'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpHourBegin': 0,  # Hour begin
        'InpMinutesBegin': 0,  # Minutes begin
    }

