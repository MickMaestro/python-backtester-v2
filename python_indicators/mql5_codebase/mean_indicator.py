"""Mean_Indicator — converted from MQL5: MQL5 Indicators/Mean_Indicator/Mean_Indicator.mq5

Mean Indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 5}, 'colors': {1: [16711680], 2: [3329330], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Mean', 2: 'Up', 3: 'Down'}, 'levels': [], 'description': ['Mean Indicator'], 'name': 'Mean_Indicator', 'source': 'MQL5 Indicators/Mean_Indicator/Mean_Indicator.mq5', 'folder': 'Mean_Indicator', 'inputs': [{'mql': 'InpDayStart', 'py': 'InpDayStart', 'param': 'InpDayStart', 'type': 'uint', 'default': 0, 'label': 'Day hour begin', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpDayStart = _input('InpDayStart', 0)  # Day hour begin
BufferMean = Arr(0, 0.0)
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferTemp = Arr(0, 0.0)
begin = 0
bars_current = 0

def OnInit():
    global bars_current, begin
    begin = _int(InpDayStart)
    bars_current = BarsCurrentInTimeframe(PERIOD_D1)
    if Period() > PERIOD_H1:
        Alert('This indicator works only on H1 charts and lower')
        ChartSetSymbolPeriod(0, None, PERIOD_H1)
    SetIndexBuffer(0, BufferMean, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(3, BufferTemp, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Mean Indicator (' + _str(begin) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMean, True)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferTemp, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if rates_total < fmax(bars_current, 4) or (not IsTimeframeDataReady(PERIOD_D1)):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferMean, EMPTY_VALUE)
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferTemp, 0)
    daily_mean = 0.0
    prev_start = 0
    for i in range(limit, 0 - 1, -1):
        BufferMean[i] = EMPTY_VALUE
        BufferUP[i] = BufferMean[i]
        BufferDN[i] = BufferUP[i]
        if TimeHour_u(time[i]) == begin:
            day_bar = BarShift("", PERIOD_D1, time[i])
            if day_bar == WRONG_VALUE:
                continue
            day_time = Time("", PERIOD_D1, day_bar + 1)
            if day_time == 0:
                continue
            prev_start = BarShift("", PERIOD_CURRENT, day_time)
            if prev_start == WRONG_VALUE:
                continue
            n = 0
            daily_mean = 0.0
            for j in range(prev_start, i, -1):
                if j > (rates_total - 1):
                    continue
                daily_mean += close[j]
                n += 1
            daily_mean = _fdiv(daily_mean, n)
            prev_start = i
        BufferTemp[i] = daily_mean
        BufferMean[i] = BufferTemp[i]
        if i < prev_start:
            n = 0
            current_mean = 0.0
            for j in range(prev_start, i, -1):
                current_mean += close[j]
                n += 1
            BufferTemp[i] = _fdiv(current_mean, n)
        if BufferTemp[i] >= BufferTemp[i + 1]:
            BufferUP[i] = BufferTemp[i]
        else:
            BufferDN[i] = BufferTemp[i]
    return rates_total

def MinutesInPeriod(timeframe):
    if timeframe == PERIOD_CURRENT:
        timeframe = Period()
    return _idiv(PeriodSeconds(timeframe), 60)

def BarsCurrentInTimeframe(timeframe):
    return _idiv(MinutesInPeriod(timeframe), MinutesInPeriod(PERIOD_CURRENT))

def TimeHour_u(time):
    tm = MqlDateTime()
    if not TimeToStruct(time, tm):
        return WRONG_VALUE
    return tm.hour

def BarShift(symbol_name, timeframe, time, exact=False):
    res = Bars(symbol_name, timeframe, time + 1, UINT_MAX)
    if exact:
        if (timeframe != PERIOD_MN1 or time > TimeCurrent()) and res == Bars(symbol_name, timeframe, time - PeriodSeconds(timeframe) + 1, UINT_MAX):
            return WRONG_VALUE
    return res

def Time(symbol_name, timeframe, shift):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyTime(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def IsTimeframeDataReady(timeframe):
    ResetLastError()
    iTime(None, timeframe, 1)
    return GetLastError() == ERR_SUCCESS


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MeanIndicator(_MQL5Indicator):
    name = 'Mean_Indicator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpDayStart': 0,  # Day hour begin
    }

