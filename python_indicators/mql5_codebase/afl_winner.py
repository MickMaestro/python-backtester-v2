"""afl_winner — converted from MQL5: MQL5 Indicators/AFL Winner/afl_winner.mq5

Copyright: avoitenko; Link: https://login.mql5.com/en/users/avoitenko; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'avoitenko', 'link': 'https://login.mql5.com/en/users/avoitenko', 'version': '2.00', 'window': 'separate', 'indicator_minimum': -10.0, 'indicator_maximum': 110.0, 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [16748574, 17919]}, 'widths': {1: 5}, 'styles': {}, 'labels': {1: 'High;Low'}, 'levels': [0.0, 100.0], 'description': [], 'name': 'afl_winner', 'source': 'MQL5 Indicators/AFL Winner/afl_winner.mq5', 'folder': 'AFL Winner', 'inputs': [{'mql': 'InpPeriods', 'py': 'InpPeriods', 'param': 'InpPeriods', 'type': 'ushort', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpAverage', 'py': 'InpAverage', 'param': 'InpAverage', 'type': 'ushort', 'default': 5, 'label': 'Average', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriods = _input('InpPeriods', 10)  # Period
InpAverage = _input('InpAverage', 5)  # Average
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
cost = Arr(0, 0.0)
pa5 = Arr(0, 0.0)
rsv = Arr(0, 0.0)
pak = Arr(0, 0.0)
pad = Arr(0, 0.0)
pa = 0.0
scost5 = 0.0
svolume5 = 0
w1 = 0
w2 = 0
offset = 0
min_ = 0.0
max_ = 0.0
periods = 0
average = 0

def OnInit():
    global average, offset, periods
    periods = _ushort(fmax(2, InpPeriods))
    average = _ushort(fmax(2, InpAverage))
    offset = periods + (average * average) + 1
    SetIndexBuffer(0, ExtHighBuffer)
    SetIndexBuffer(1, ExtLowBuffer)
    SetIndexBuffer(2, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, cost, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, pa5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, rsv, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, pak, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, pad, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    ArraySetAsSeries(cost, True)
    ArraySetAsSeries(pa5, True)
    ArraySetAsSeries(rsv, True)
    ArraySetAsSeries(pak, True)
    ArraySetAsSeries(pad, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, offset)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('AFL Winner (%u, %u)', periods, average))
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global max_, min_, pa, scost5, svolume5
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total <= offset:
        return 0
    limit = 0
    if rates_total < prev_calculated or prev_calculated <= 0:
        limit = rates_total - offset
        ArrayInitialize(ExtHighBuffer, EMPTY_VALUE)
        ArrayInitialize(ExtLowBuffer, EMPTY_VALUE)
        ArrayInitialize(ExtColorBuffer, 0)
    else:
        limit = rates_total - prev_calculated
    for i in range(limit, 0 - 1, -1):
        pa = ((2 * close[i]) + high[i] + low[i]) / 4
        cost[i] = pa * tick_volume[i]
        scost5 = Sum(cost, i, average)
        svolume5 = _long(Sum(tick_volume, i, average))
        if svolume5 == 0:
            continue
        pa5[i] = _fdiv(scost5, svolume5)
        max_ = pa5[ArrayMaximum(pa5, i, periods)]
        min_ = pa5[ArrayMinimum(pa5, i, periods)]
        rsv[i] = _fdiv(pa5[i] - min_, fmax(max_ - min_, Point())) * 100
    LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, average, rsv, pak, _GlobRef(globals(), 'w1'))
    LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, average, pak, pad, _GlobRef(globals(), 'w2'))
    for i in range(limit, 0 - 1, -1):
        ExtHighBuffer[i] = pak[i]
        ExtLowBuffer[i] = pad[i]
        ExtColorBuffer[i] = 0.0
        if pak[i] < pad[i]:
            ExtColorBuffer[i] = 1.0
    return rates_total

def Sum(buffer, index, count):
    sum_ = 0
    total = ArraySize(buffer)
    for i in range(index, fmin(total, index + count)):
        sum_ += buffer[i]
    return sum_


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AflWinner(_MQL5Indicator):
    name = 'afl_winner'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriods': 10,  # Period
        'InpAverage': 5,  # Average
    }
    y_range = (-10.0, 110.0)

