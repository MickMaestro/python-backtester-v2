"""the20sv0i20 — converted from MQL5: MQL5 Indicators/The20sv0.20/the20sv0i20.mq5

Copyright: Copyright © 2005, TraderSeven; Link: TraderSeven@gmx.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TraderSeven', 'link': 'TraderSeven@gmx.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'The20sv0.20 Sell', 2: 'The20sv0.20 Buy'}, 'levels': [], 'description': [], 'name': 'the20sv0i20', 'source': 'MQL5 Indicators/The20sv0.20/the20sv0i20.mq5', 'folder': 'The20sv0.20', 'inputs': [{'mql': 'Variation', 'py': 'Variation', 'param': 'Variation', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'StopLevel', 'py': 'StopLevel', 'param': 'StopLevel', 'type': 'double', 'default': 0.2, 'label': 'level of triggering', 'sinput': False}, {'mql': 'Range', 'py': 'Range', 'param': 'Range', 'type': 'uint', 'default': 10, 'label': 'distance in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Variation = _input('Variation', False)
StopLevel = _input('StopLevel', 0.2)  # level of triggering
Range = _input('Range', 10)  # distance in points
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
PRange = 0.0
min_rates_total = 0

def OnInit():
    global PRange, min_rates_total
    min_rates_total = 5
    PRange = Range * Point()
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 181)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 181)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'The20sv0.20'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    for bar in range(limit, 0 - 1, -1):
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        LastBarsRange = high[bar + 1] - low[bar + 1]
        Top20 = high[bar + 1] - (LastBarsRange * StopLevel)
        Bottom20 = low[bar + 1] + (LastBarsRange * StopLevel)
        if not Variation:
            if (open[bar + 1] >= Top20 and close[bar + 1] <= Bottom20) and low[bar] <= (low[bar + 1] + PRange):
                BuyBuffer[bar] = low[bar]
            if (open[bar + 1] <= Bottom20 and close[bar + 1] >= Top20) and high[bar] >= (high[bar + 1] + PRange):
                SellBuffer[bar] = high[bar]
        else:
            if ((((high[bar + 4] - low[bar + 4]) > LastBarsRange and (high[bar + 3] - low[bar + 3]) > LastBarsRange) and (high[bar + 2] - low[bar + 2]) > LastBarsRange) and high[bar + 2] > high[bar + 1]) and low[bar + 2] < low[bar + 1]:
                if open[bar] <= Bottom20:
                    BuyBuffer[bar] = low[bar]
                if open[bar] >= Top20:
                    SellBuffer[bar] = high[bar]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class The20sv0i20(_MQL5Indicator):
    name = 'the20sv0i20'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Variation': False,
        'StopLevel': 0.2,  # level of triggering
        'Range': 10,  # distance in points
    }

