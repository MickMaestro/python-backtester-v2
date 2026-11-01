"""dm — converted from MQL5: MQL5 Indicators/DM/dm.mq5

Copyright: Copyright © 2007, AlexP; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, AlexP', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [4678655], 2: [13828244]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'DM Sell', 2: 'DM Buy'}, 'levels': [], 'description': [], 'name': 'dm', 'source': 'MQL5 Indicators/DM/dm.mq5', 'folder': 'DM', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
uptrend_ = False
old = False
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, 4)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'DM'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_oldtrend
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    trend = 0
    ATR = Arr(0, 0.0)
    c3 = 0.0
    c2 = 0.0
    c1 = 0.0
    c0 = 0.0
    l3 = 0.0
    l2 = 0.0
    l1 = 0.0
    l0 = 0.0
    h3 = 0.0
    h2 = 0.0
    h1 = 0.0
    h0 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_oldtrend = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        c3 = close[bar + 3]
        c2 = close[bar + 2]
        c1 = close[bar + 1]
        c0 = close[bar]
        l3 = low[bar + 3]
        l2 = low[bar + 2]
        l1 = low[bar + 1]
        l0 = low[bar]
        h3 = high[bar + 3]
        h2 = high[bar + 2]
        h1 = high[bar + 1]
        h0 = high[bar]
        if ((((l3 > l1 and l2 > l1) and l1 <= l0) and c3 > c2) and c2 > c1) and c1 < c0:
            trend = 1
        if ((((h3 < h1 and h2 < h1) and h1 >= h0) and c3 < c2) and c2 < c1) and c1 > c0:
            trend = -1
        if _s_OnCalculate_oldtrend <= 0 and trend > 0:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if _s_OnCalculate_oldtrend >= 0 and trend < 0:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_oldtrend = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_oldtrend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dm(_MQL5Indicator):
    name = 'dm'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

