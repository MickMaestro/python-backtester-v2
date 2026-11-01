"""doji_arrows — converted from MQL5: MQL5 Indicators/Doji_Arrows/doji_arrows.mq5

The indicator finds Doji candlesticks and highlights them on a chart using colored arrows
Copyright: Copyright © 2007, NNN; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, NNN', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [9639167], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'DojiArrows Sell', 2: 'DojiArrows Buy'}, 'levels': [], 'description': ['The indicator finds Doji candlesticks and highlights them on a chart using colored arrows'], 'name': 'doji_arrows', 'source': 'MQL5 Indicators/Doji_Arrows/doji_arrows.mq5', 'folder': 'Doji_Arrows', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, 3)
    ATR_Handle = iATR(Symbol(), PERIOD_CURRENT, ATR_Period)
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
    short_name = 'DojiArrows'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_downtrend, _s_OnCalculate_prev_uptrend
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    bar1 = 0
    bar2 = 0
    ATR = Arr(0, 0.0)
    uptrend = False
    downtrend = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_prev_uptrend = False
        _s_OnCalculate_prev_downtrend = False
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        bar1 = bar + 1
        bar2 = bar + 2
        if close[bar2] == open[bar2] and close[bar1] > high[bar2]:
            uptrend = True
        if close[bar2] != open[bar2] and close[bar1] <= high[bar2]:
            uptrend = False
        if uptrend != _s_OnCalculate_prev_uptrend and uptrend:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if close[bar2] == open[bar2] and close[bar1] < low[bar2]:
            downtrend = True
        if close[bar2] != open[bar2] and close[bar1] >= low[bar2]:
            downtrend = False
        if downtrend != _s_OnCalculate_prev_downtrend and downtrend:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_prev_uptrend = uptrend
            _s_OnCalculate_prev_downtrend = downtrend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_prev_uptrend = False
_s_OnCalculate_prev_downtrend = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DojiArrows(_MQL5Indicator):
    name = 'doji_arrows'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

