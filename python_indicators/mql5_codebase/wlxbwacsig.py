"""wlxbwacsig — converted from MQL5: MQL5 Indicators/wlxBWACsig/wlxbwacsig.mq5

Copyright: Copyright © 2005, wellx; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, wellx', 'link': '', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [9639167], 2: [16776960]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'wlxBWACsig Sell', 2: 'wlxBWACsig Buy'}, 'levels': [], 'description': [], 'name': 'wlxbwacsig', 'source': 'MQL5 Indicators/wlxBWACsig/wlxbwacsig.mq5', 'folder': 'wlxBWACsig', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
uptrend_ = False
old = False
AC_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global AC_Handle, ATR_Handle, min_rates_total
    min_rates_total = 40
    AC_Handle = iAC(None, 0)
    if AC_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iAC indicator')
    ATR_Handle = iATR(None, 0, 15)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'wlxBWACsig Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'wlxBWACsig Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'wlxBWACsigSig'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(AC_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    bar1 = 0
    bar2 = 0
    bar3 = 0
    bar4 = 0
    AC = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    to_copy += 4
    if CopyBuffer(AC_Handle, 0, 0, to_copy, AC) <= 0:
        return 0
    ArraySetAsSeries(AC, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        bar1 = bar + 1
        bar2 = bar + 2
        bar3 = bar + 3
        bar4 = bar + 4
        if (((((AC[bar3] > 0 and AC[bar2] > 0) and AC[bar1] > 0) and AC[bar] > 0) and ((AC[bar3] > AC[bar2] and AC[bar1] > AC[bar2]) and AC[bar] > AC[bar1])) or ((((AC[bar3] < 0 and AC[bar2] < 0) and AC[bar1] < 0) and AC[bar] > 0) and ((AC[bar3] > AC[bar2] and AC[bar1] > AC[bar2]) and AC[bar] > AC[bar1]))) or (((((AC[bar4] < 0 and AC[bar3] < 0) and AC[bar2] < 0) and AC[bar1] < 0) and AC[bar] < 0) and (((AC[bar4] > AC[bar3] and AC[bar3] < AC[bar2]) and AC[bar2] < AC[bar1]) and AC[bar1] < AC[bar])):
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if (((((AC[bar3] < 0 and AC[bar2] < 0) and AC[bar1] < 0) and AC[bar] < 0) and ((AC[bar3] < AC[bar2] and AC[bar1] < AC[bar2]) and AC[bar] < AC[bar1])) or ((((AC[bar3] > 0 and AC[bar2] > 0) and AC[bar1] > 0) and AC[bar] < 0) and ((AC[bar3] < AC[bar2] and AC[bar1] < AC[bar2]) and AC[bar] < AC[bar1]))) or (((((AC[bar4] > 0 and AC[bar3] > 0) and AC[bar2] > 0) and AC[bar1] > 0) and AC[bar] > 0) and (((AC[bar4] < AC[bar3] and AC[bar3] > AC[bar2]) and AC[bar2] > AC[bar1]) and AC[bar1] > AC[bar])):
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wlxbwacsig(_MQL5Indicator):
    name = 'wlxbwacsig'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

