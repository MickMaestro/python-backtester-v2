"""sidus — converted from MQL5: MQL5 Indicators/Sidus/sidus.mq5

Copyright: Copyright © 2006, GwadaTradeBoy; Link: racooni_1975@yahoo.fr; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, GwadaTradeBoy', 'link': 'racooni_1975@yahoo.fr', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 7, 4: 7}, 'colors': {1: [8421376], 2: [8721863], 3: [14822282, 16711935], 4: [65280, 255]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Sidus Buy', 2: 'Sidus Sell', 3: 'Sidus Fast EMA', 4: 'Sidus Fast LWMA'}, 'levels': [], 'description': [], 'name': 'sidus', 'source': 'MQL5 Indicators/Sidus/sidus.mq5', 'folder': 'Sidus', 'inputs': [{'mql': 'FastEMA', 'py': 'FastEMA', 'param': 'FastEMA', 'type': 'int', 'default': 18, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'SlowEMA', 'py': 'SlowEMA', 'param': 'SlowEMA', 'type': 'int', 'default': 28, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'FastLWMA', 'py': 'FastLWMA', 'param': 'FastLWMA', 'type': 'int', 'default': 5, 'label': 'Fast LWMA period', 'sinput': False}, {'mql': 'SlowLWMA', 'py': 'SlowLWMA', 'param': 'SlowLWMA', 'type': 'int', 'default': 8, 'label': 'Slow LWMA period', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastEMA = _input('FastEMA', 18)  # Fast EMA period
SlowEMA = _input('SlowEMA', 28)  # Slow EMA period
FastLWMA = _input('FastLWMA', 5)  # Fast LWMA period
SlowLWMA = _input('SlowLWMA', 8)  # Slow LWMA period
IPC = _input('IPC', PRICE_CLOSE)  # Applied price
digit = 0.0  # Range in points
FstEmaBuffer = Arr(0, 0.0)
SlwEmaBuffer = Arr(0, 0.0)
FstLwmaBuffer = Arr(0, 0.0)
SlwLwmaBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
DIGIT = 0.0
min_rates_total = 0
FstEma_Handle = 0
SlwEma_Handle = 0
FstLwma_Handle = 0
SlwLwma_Handle = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, DIGIT, FstEma_Handle, FstLwma_Handle, SlwEma_Handle, SlwLwma_Handle, min_rates_total
    min_rates_total = MathMax(FastLWMA, SlowLWMA) + 3
    DIGIT = digit * Point()
    ATR_Handle = iATR(None, 0, 15)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    FstEma_Handle = iMA(None, 0, FastEMA, 0, MODE_EMA, IPC)
    if FstEma_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the FastEMA indicator')
    SlwEma_Handle = iMA(None, 0, SlowEMA, 0, MODE_EMA, IPC)
    if SlwEma_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the SlowEma indicator')
    FstLwma_Handle = iMA(None, 0, FastLWMA, 0, MODE_LWMA, IPC)
    if FstLwma_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the FastLWMA indicator')
    SlwLwma_Handle = iMA(None, 0, SlowLWMA, 0, MODE_LWMA, IPC)
    if SlwLwma_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the SlowLWMA indicator')
    SetIndexBuffer(0, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    SetIndexBuffer(1, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(2, FstEmaBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(FstEmaBuffer, True)
    SetIndexBuffer(3, SlwEmaBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(SlwEmaBuffer, True)
    SetIndexBuffer(4, FstLwmaBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(FstLwmaBuffer, True)
    SetIndexBuffer(5, SlwLwmaBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(SlwLwmaBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Sidus(', FastEMA, ', ', SlowEMA, ', ', FastLWMA, ', ', SlowLWMA, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(FstEma_Handle) < rates_total) or BarsCalculated(SlwEma_Handle) < rates_total) or BarsCalculated(FstLwma_Handle) < rates_total) or BarsCalculated(SlwLwma_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    range_ = 0.0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        to_copy = rates_total
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    if CopyBuffer(FstEma_Handle, 0, 0, to_copy, FstEmaBuffer) <= 0:
        return 0
    if CopyBuffer(SlwEma_Handle, 0, 0, to_copy, SlwEmaBuffer) <= 0:
        return 0
    if CopyBuffer(FstLwma_Handle, 0, 0, to_copy, FstLwmaBuffer) <= 0:
        return 0
    if CopyBuffer(SlwLwma_Handle, 0, 0, to_copy, SlwLwmaBuffer) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        range_ = (ATR[bar] * 3) / 8
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if FstLwmaBuffer[bar] > (SlwLwmaBuffer[bar] + DIGIT) and FstLwmaBuffer[bar + 1] <= SlwLwmaBuffer[bar + 1]:
            BuyBuffer[bar] = low[bar] - range_
        if SlwLwmaBuffer[bar] > (SlwEmaBuffer[bar] + DIGIT) and SlwLwmaBuffer[bar + 1] <= SlwEmaBuffer[bar]:
            BuyBuffer[bar] = low[bar] - range_
        if FstLwmaBuffer[bar] < (SlwLwmaBuffer[bar] - DIGIT) and FstLwmaBuffer[bar + 1] >= SlwLwmaBuffer[bar + 1]:
            SellBuffer[bar] = high[bar] + range_
        if SlwLwmaBuffer[bar] < (SlwEmaBuffer[bar] - DIGIT) and SlwLwmaBuffer[bar + 1] >= SlwEmaBuffer[bar]:
            SellBuffer[bar] = high[bar] + range_
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Sidus(_MQL5Indicator):
    name = 'sidus'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastEMA': 18,  # Fast EMA period
        'SlowEMA': 28,  # Slow EMA period
        'FastLWMA': 5,  # Fast LWMA period
        'SlowLWMA': 8,  # Slow LWMA period
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

