"""Extremes with tick prices v2 — converted from MQL5: MQL5 Indicators/Extreme highs and lows with tick prices/Extremes with tick prices v2.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65407], 2: [65407]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Extreme highs', 2: 'Extreme lows'}, 'levels': [], 'description': [], 'name': 'Extremes with tick prices v2', 'source': 'MQL5 Indicators/Extreme highs and lows with tick prices/Extremes with tick prices v2.mq5', 'folder': 'Extreme highs and lows with tick prices', 'inputs': [{'mql': 'start', 'py': 'start', 'param': 'start', 'type': 'int', 'default': 5, 'label': 'Lookback bars', 'sinput': False}, {'mql': 'show_BoS', 'py': 'show_BoS', 'param': 'show_BoS', 'type': 'bool', 'default': True, 'label': 'Lines should keep drawing on BoS', 'sinput': False}, {'mql': 'using_optimization', 'py': 'using_optimization', 'param': 'using_optimization', 'type': 'bool', 'default': True, 'label': 'Use ticks from current bar only', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

COPY_TICKS_INFO = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
start = _input('start', 5)  # Lookback bars
show_BoS = _input('show_BoS', True)  # Lines should keep drawing on BoS
using_optimization = _input('using_optimization', True)  # Use ticks from current bar only
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
ticksReceived = 0

def OnInit():
    SetIndexBuffer(0, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LowBuffer, INDICATOR_DATA)
    ArraySetAsSeries(HighBuffer, True)
    ArraySetAsSeries(LowBuffer, True)
    ChartNavigate(0, CHART_END)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global ticksReceived
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    range_ = 0
    barStart = time[0]
    barEnd = time[0] + PeriodSeconds()
    if using_optimization:
        fromTime = iTime(Symbol(), Period(), 1)
        range_ = _int(CopyTicksRange(Symbol(), ticks, COPY_TICKS_INFO, fromTime * 1000, TimeCurrent() * 1000))
        ticksReceived = range_
    for i in range(start, 0 - 1, -1):
        if not using_optimization:
            fromTime = iTime(Symbol(), Period(), start - i)
            range_ = _int(CopyTicksRange(Symbol(), ticks, COPY_TICKS_INFO, fromTime * 1000, TimeCurrent() * 1000))
            ticksReceived = range_
        lowestBid = DBL_MAX
        highestAsk = -DBL_MAX
        if range_ > 0:
            for k in range(0, range_):
                if using_optimization:
                    if ticks[k].time >= barStart and ticks[k].time <= barEnd:
                        if ticks[k].bid != 0 and lowestBid > ticks[k].bid:
                            lowestBid = ticks[k].bid
                        if ticks[k].ask != 0 and highestAsk < ticks[k].ask:
                            highestAsk = ticks[k].ask
                elif not using_optimization:
                    if ticks[k].bid != 0 and lowestBid > ticks[k].bid:
                        lowestBid = ticks[k].bid
                    if ticks[k].ask != 0 and highestAsk < ticks[k].ask:
                        highestAsk = ticks[k].ask
        highestHigh = high[i]
        lowestLow = low[i]
        for j in range(1, start):
            if high[i + j] > highestHigh:
                highestHigh = high[i + j]
            if low[i + j] < lowestLow:
                lowestLow = low[i + j]
        HighBuffer[i] = MathMax(highestHigh, highestAsk)
        LowBuffer[i] = MathMin(lowestLow, lowestBid)
        if not show_BoS:
            if HighBuffer[i] != HighBuffer[i + 1]:
                HighBuffer[i + 1] = EMPTY_VALUE
            if LowBuffer[i] != LowBuffer[i + 1]:
                LowBuffer[i + 1] = EMPTY_VALUE
    for i in range(rates_total - 1, start - 1, -1):
        HighBuffer[i] = EMPTY_VALUE
        LowBuffer[i] = EMPTY_VALUE
    Comment('Ticks received: ', ticksReceived)
    return rates_total

# ---- global variables initialised from expressions
ticks = Arr(0, 0, factory=MqlTick)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ExtremesWithTickPricesV2(_MQL5Indicator):
    name = 'Extremes with tick prices v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'start': 5,  # Lookback bars
        'show_BoS': True,  # Lines should keep drawing on BoS
        'using_optimization': True,  # Use ticks from current bar only
    }

