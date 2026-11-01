"""lemansignal — converted from MQL5: MQL5 Indicators/LeManSignal/lemansignal.mq5

Copyright: Copyright © 2009, LeMan.; Link: b-market@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, LeMan.', 'link': 'b-market@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'LeManSell', 2: 'LeManBuy'}, 'levels': [], 'description': [], 'name': 'lemansignal', 'source': 'MQL5 Indicators/LeManSignal/lemansignal.mq5', 'folder': 'LeManSignal', 'inputs': [{'mql': 'LPeriod', 'py': 'LPeriod', 'param': 'LPeriod', 'type': 'int', 'default': 12, 'label': 'Indicator period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LPeriod = _input('LPeriod', 12)  # Indicator period
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
StartBars = 0

def OnInit():
    global StartBars
    StartBars = LPeriod + LPeriod + 2 + 1
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'LeManSell')
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'LeManBuy')
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'LeManSignal'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    limit = 0
    bar = 0
    bar1 = 0
    bar2 = 0
    bar1p = 0
    bar2p = 0
    H1 = 0.0
    H2 = 0.0
    H3 = 0.0
    H4 = 0.0
    L1 = 0.0
    L2 = 0.0
    L3 = 0.0
    L4 = 0.0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - StartBars
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        bar1 = bar + 1
        bar2 = bar + 2
        bar1p = bar1 + LPeriod
        bar2p = bar2 + LPeriod
        H1 = high[ArrayMaximum(high, bar1, LPeriod)]
        H2 = high[ArrayMaximum(high, bar1p, LPeriod)]
        H3 = high[ArrayMaximum(high, bar2, LPeriod)]
        H4 = high[ArrayMaximum(high, bar2p, LPeriod)]
        L1 = low[ArrayMinimum(low, bar1, LPeriod)]
        L2 = low[ArrayMinimum(low, bar1p, LPeriod)]
        L3 = low[ArrayMinimum(low, bar2, LPeriod)]
        L4 = low[ArrayMinimum(low, bar2p, LPeriod)]
        BuyBuffer[bar] = EMPTY_VALUE
        SellBuffer[bar] = EMPTY_VALUE
        if H3 <= H4 and H1 > H2:
            BuyBuffer[bar] = high[bar + 1] + Point()
        if L3 >= L4 and L1 < L2:
            SellBuffer[bar] = low[bar + 1] - Point()
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Lemansignal(_MQL5Indicator):
    name = 'lemansignal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LPeriod': 12,  # Indicator period
    }

