"""wlxbwwiseman-2 — converted from MQL5: MQL5 Indicators/wlxBWWiseMan-2/wlxbwwiseman-2.mq5

Copyright: Copyright © 2005, wellx; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, wellx', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [3329330]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'wlxBWWiseMan-2 Sell', 2: 'wlxBWWiseMan-2 Buy'}, 'levels': [], 'description': [], 'name': 'wlxbwwiseman-2', 'source': 'MQL5 Indicators/wlxBWWiseMan-2/wlxbwwiseman-2.mq5', 'folder': 'wlxBWWiseMan-2', 'inputs': [{'mql': 'updown', 'py': 'updown', 'param': 'updown', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
updown = _input('updown', 10)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
AO_Handle = 0
min_rates_total = 0

def OnInit():
    global AO_Handle, ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, 33 + 5)
    ATR_Handle = iATR(Symbol(), PERIOD_CURRENT, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    AO_Handle = iAO(Symbol(), PERIOD_CURRENT)
    if AO_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора   Awesome oscillator')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 93)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 93)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'wlxBWWiseMan-2'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(AO_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    AO = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    to_copy += 4
    if CopyBuffer(AO_Handle, 0, 0, to_copy, AO) <= 0:
        return 0
    ArraySetAsSeries(AO, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if ((((AO[bar + 4] > 0.0 and AO[bar + 3] > 0.0) and AO[bar + 4] < AO[bar + 3]) and AO[bar + 3] > AO[bar + 2]) and AO[bar + 2] > AO[bar + 1]) and AO[bar + 1] > AO[bar]:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if ((((AO[bar + 4] < 0.0 and AO[bar + 3] < 0.0) and AO[bar + 4] > AO[bar + 3]) and AO[bar + 3] < AO[bar + 2]) and AO[bar + 2] < AO[bar + 1]) and AO[bar + 1] < AO[bar]:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wlxbwwiseman2(_MQL5Indicator):
    name = 'wlxbwwiseman-2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'updown': 10,
    }

