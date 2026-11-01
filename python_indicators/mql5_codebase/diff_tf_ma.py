"""Diff_TF_MA — converted from MQL5: MQL5 Indicators/Diff_TF_MA - Moving Averages for two timeframes/Diff_TF_MA.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MA1', 2: 'MA2'}, 'levels': [], 'description': [], 'name': 'Diff_TF_MA', 'source': 'MQL5 Indicators/Diff_TF_MA - Moving Averages for two timeframes/Diff_TF_MA.mq5', 'folder': 'Diff_TF_MA - Moving Averages for two timeframes', 'inputs': [{'mql': 'InpMAPeriod', 'py': 'InpMAPeriod', 'param': 'InpMAPeriod', 'type': 'uint', 'default': 10, 'label': 'Period MA', 'sinput': False}, {'mql': 'InpMATimeframe', 'py': 'InpMATimeframe', 'param': 'InpMATimeframe', 'type': 'int', 'default': 16388, 'label': 'Timeframe MA', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMAPeriod = _input('InpMAPeriod', 10)  # Period MA
InpMATimeframe = _input('InpMATimeframe', PERIOD_H4)  # Timeframe MA
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
period_ma1 = 0
period_ma2 = 0
handle_ma1 = 0

def OnInit():
    global handle_ma1, period_ma1, period_ma2
    SetIndexBuffer(0, BufferMA1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    period_ma1 = (1 if (InpMAPeriod < 1) else InpMAPeriod)
    v1 = _idiv(PeriodSeconds(InpMATimeframe), 60)
    v2 = _idiv(PeriodSeconds(Period()), 60)
    v3 = _idiv(period_ma1 * v1, v2)
    period_ma2 = (v3 if (v3 > 0) else 1)
    PlotIndexSetString(0, PLOT_LABEL, 'MA(' + NameTimeframe(Period()) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'MA(' + NameTimeframe(InpMATimeframe) + ')')
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, period_ma2, 0, MODE_SMA, PRICE_CLOSE)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ma2:
        return 0
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferMA1, EMPTY_VALUE)
        ArrayInitialize(BufferMA2, EMPTY_VALUE)
    copied = (1 if (limit == 0) else rates_total)
    copied_ma1 = CopyBuffer(handle_ma1, 0, 0, copied, BufferMA1)
    if copied_ma1 != copied:
        return 0
    for i in range(limit, 0 - 1, -1):
        index = BarShift(InpMATimeframe, time[i])
        if index == WRONG_VALUE:
            return 0
        if time[i] == Time(InpMATimeframe, index):
            ma2 = GetMA(InpMATimeframe, period_ma1, MODE_SMA, PRICE_CLOSE, index)
            if ma2 == WRONG_VALUE:
                return 0
            BufferMA2[i] = ma2
    return rates_total

def GetMA(timeframe, period, method, price, shift):
    array = Arr(0, 0.0)
    ResetLastError()
    handle = iMA(Symbol(), timeframe, period, 0, method, price)
    if handle == INVALID_HANDLE:
        Print('Trading day average: Error creating MA handle ', GetLastError(), ', recalculate now')
        return WRONG_VALUE
    if CopyBuffer(handle, 0, shift, 1, array) == 1:
        return array[0]
    return WRONG_VALUE

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

def Time(timeframe, shift):
    array = Arr(0, 0)
    if CopyTime(Symbol(), timeframe, shift, 1, array) == 1:
        return array[0]
    return 0

def NameTimeframe(timeframe=PERIOD_CURRENT):
    if timeframe == PERIOD_CURRENT:
        timeframe = Period()
    _sw1 = timeframe
    if _sw1 == 1:
        return 'M1'
    elif _sw1 == 2:
        return 'M2'
    elif _sw1 == 3:
        return 'M3'
    elif _sw1 == 4:
        return 'M4'
    elif _sw1 == 5:
        return 'M5'
    elif _sw1 == 6:
        return 'M6'
    elif _sw1 == 10:
        return 'M10'
    elif _sw1 == 12:
        return 'M12'
    elif _sw1 == 15:
        return 'M15'
    elif _sw1 == 20:
        return 'M20'
    elif _sw1 == 30:
        return 'M30'
    elif _sw1 == 16385:
        return 'H1'
    elif _sw1 == 16386:
        return 'H2'
    elif _sw1 == 16387:
        return 'H3'
    elif _sw1 == 16388:
        return 'H4'
    elif _sw1 == 16390:
        return 'H6'
    elif _sw1 == 16392:
        return 'H8'
    elif _sw1 == 16396:
        return 'H12'
    elif _sw1 == 16408:
        return 'D1'
    elif _sw1 == 32769:
        return 'W1'
    elif _sw1 == 49153:
        return 'MN1'
    else:
        return _str(Period())


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DiffTFMA(_MQL5Indicator):
    name = 'Diff_TF_MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMAPeriod': 10,  # Period MA
        'InpMATimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Timeframe MA
    }

