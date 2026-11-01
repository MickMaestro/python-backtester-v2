"""bidaskchannel — converted from MQL5: MQL5 Indicators/BidAskChannel/bidaskchannel.mq5

High and Low level indicator taking spread into account
Copyright: Copyright © 2012,; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012,', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 4}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'BidAskChannel'}, 'levels': [], 'description': ['High and Low level indicator taking spread into account'], 'name': 'bidaskchannel', 'source': 'MQL5 Indicators/BidAskChannel/bidaskchannel.mq5', 'folder': 'BidAskChannel', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 1
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BidAskChannel')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        bar = rates_total - 1
        for bar in range(bar, limit, -1):
            ExtLineBuffer1[bar] = 0.0
            ExtLineBuffer2[bar] = 0.0
        else:
            bar = _range_end(bar, limit, -1)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(spread, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtLineBuffer2[bar] = high[bar] + (Point() * spread[bar])
        ExtLineBuffer1[bar] = low[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bidaskchannel(_MQL5Indicator):
    name = 'bidaskchannel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

