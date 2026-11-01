"""Period_Open_Line — converted from MQL5: MQL5 Indicators/Period_Open_Line/Period_Open_Line.mq5

Line of period opening
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Period Open'}, 'levels': [], 'description': ['Line of period opening'], 'name': 'Period_Open_Line', 'source': 'MQL5 Indicators/Period_Open_Line/Period_Open_Line.mq5', 'folder': 'Period_Open_Line', 'inputs': [{'mql': 'InpTimeframe', 'py': 'InpTimeframe', 'param': 'InpTimeframe', 'type': 'int', 'default': 16408, 'label': 'Timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpTimeframe = _input('InpTimeframe', PERIOD_D1)  # Timeframe
BufferOPN = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferOPN, INDICATOR_DATA)
    name = 'Period ' + StringSubstr(EnumToString(InpTimeframe, 'ENUM_TIMEFRAMES'), 7) + ' Open'
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, name)
    PlotIndexSetString(0, PLOT_LABEL, name)
    ArraySetAsSeries(BufferOPN, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferOPN, EMPTY_VALUE)
    index = WRONG_VALUE
    for i in range(limit, 0 - 1, -1):
        index = (BarShift(Symbol(), InpTimeframe, time[i]) if (InpTimeframe < PERIOD_MN1) else BarShift(Symbol(), InpTimeframe, BeginOfYear(time[i])))
        if index == WRONG_VALUE:
            return 0
        BufferOPN[i] = Open(InpTimeframe, index)
    return rates_total

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

def Open(timeframe, index):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyOpen(Symbol(), timeframe, index, 1, array) == 1:
        return array[0]
    return 0.0

def BeginOfYear(time):
    tm = MqlDateTime()
    if not TimeToStruct(time, tm):
        return WRONG_VALUE
    tm.mon = 1
    tm.day = 1
    return StructToTime(tm)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PeriodOpenLine(_MQL5Indicator):
    name = 'Period_Open_Line'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Timeframe
    }

