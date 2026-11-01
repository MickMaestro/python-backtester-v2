"""Extremes with tick prices — converted from MQL5: MQL5 Indicators/Extreme highs and lows with tick prices/Extremes with tick prices.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65407], 2: [65407]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Extreme highs', 2: 'Extreme lows'}, 'levels': [], 'description': [], 'name': 'Extremes with tick prices', 'source': 'MQL5 Indicators/Extreme highs and lows with tick prices/Extremes with tick prices.mq5', 'folder': 'Extreme highs and lows with tick prices', 'inputs': [{'mql': 'length', 'py': 'length', 'param': 'length', 'type': 'int', 'default': 10, 'label': 'Length', 'sinput': False}, {'mql': 'show_BoS', 'py': 'show_BoS', 'param': 'show_BoS', 'type': 'bool', 'default': False, 'label': 'Lines should keep drawing on BoS', 'sinput': False}, {'mql': 'start', 'py': 'start', 'param': 'start', 'type': 'int', 'default': 200, 'label': 'Lookback bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

COPY_TICKS_INFO = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
length = _input('length', 10)  # Length
show_BoS = _input('show_BoS', False)  # Lines should keep drawing on BoS
start = _input('start', 200)  # Lookback bars
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
TickPriceAsk = Arr(0, 0.0)
TickPriceBid = Arr(0, 0.0)
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
    ArraySetAsSeries(TickPriceAsk, True)
    ArraySetAsSeries(TickPriceBid, True)
    i = start
    while i >= 0:
        highestAsk = -DBL_MAX
        lowestBid = DBL_MAX
        fromTime = iTime(Symbol(), Period(), MathMin(start - i, length))
        range_ = _int(CopyTicksRange(Symbol(), ticks, COPY_TICKS_INFO, fromTime * 1000, TimeCurrent() * 1000))
        ticksReceived = range_
        if range_ > 0:
            ArrayResize(TickPriceAsk, range_)
            ArrayResize(TickPriceBid, range_)
            for i_2 in range(0, range_):
                TickPriceAsk[i_2] = ticks[i_2].ask
                TickPriceBid[i_2] = ticks[i_2].bid
        highestHigh = high[i]
        lowestLow = low[i]
        for j in range(1, length):
            if high[i + j] > highestHigh:
                highestHigh = high[i + j]
            if low[i + j] < lowestLow:
                lowestLow = low[i + j]
        for i_2 in range(0, range_):
            if highestAsk < TickPriceAsk[i_2]:
                highestAsk = TickPriceAsk[i_2]
            if lowestBid > TickPriceBid[i_2]:
                lowestBid = TickPriceBid[i_2]
        HighBuffer[i] = MathMax(highestHigh, highestAsk)
        LowBuffer[i] = MathMin(lowestLow, lowestBid)
        if not show_BoS:
            if HighBuffer[i] != HighBuffer[i + 1]:
                HighBuffer[i + 1] = EMPTY_VALUE
            if LowBuffer[i] != LowBuffer[i + 1]:
                LowBuffer[i + 1] = EMPTY_VALUE
        ArrayRemove(TickPriceAsk, 0, WHOLE_ARRAY)
        ArrayRemove(TickPriceBid, 0, WHOLE_ARRAY)
        i -= 1
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


class ExtremesWithTickPrices(_MQL5Indicator):
    name = 'Extremes with tick prices'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'length': 10,  # Length
        'show_BoS': False,  # Lines should keep drawing on BoS
        'start': 200,  # Lookback bars
    }

