"""Minions.Hikkake — converted from MQL5: MQL5 Indicators/Hikkake Pattern (Inside Day False Breakout)/Minions.Hikkake.mq5

Minions in the quest for the Hikakke patterns
 
(CC) Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
Copyright: www.MinionsLabs.com; Link: http://www.MinionsLabs.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.MinionsLabs.com', 'link': 'http://www.MinionsLabs.com', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [255], 2: [16748574], 3: [16711935], 4: [16711935]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Sell', 2: 'Buy', 3: 'Hikkake', 4: 'HikkakeEntry'}, 'levels': [], 'description': ['Minions in the quest for the Hikakke patterns', ' ', '(CC) Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'], 'name': 'Minions.Hikkake', 'source': 'MQL5 Indicators/Hikkake Pattern (Inside Day False Breakout)/Minions.Hikkake.mq5', 'folder': 'Hikkake Pattern (Inside Day False Breakout)', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
bufferSell_ID = 0  # put names on buffers!
bufferBuy_ID = 1
bufferHikkake_ID = 2
bufferHikkakeEntry_ID = 3
tickSize = 0.0  # minimum tick size for the symbol
bufferSell = Arr(0, 0.0)  # buffers for holding the data...
bufferBuy = Arr(0, 0.0)
bufferHikkake = Arr(0, 0.0)
bufferHikkakeEntry = Arr(0, 0.0)

def OnInit():
    global tickSize
    SetIndexBuffer(bufferBuy_ID, bufferBuy, INDICATOR_DATA)
    SetIndexBuffer(bufferSell_ID, bufferSell, INDICATOR_DATA)
    SetIndexBuffer(bufferHikkake_ID, bufferHikkake, INDICATOR_DATA)
    SetIndexBuffer(bufferHikkakeEntry_ID, bufferHikkakeEntry, INDICATOR_DATA)
    PlotIndexSetInteger(bufferSell_ID, PLOT_ARROW, 234)
    PlotIndexSetInteger(bufferBuy_ID, PLOT_ARROW, 233)
    PlotIndexSetInteger(bufferHikkake_ID, PLOT_ARROW, 108)
    PlotIndexSetInteger(bufferHikkakeEntry_ID, PLOT_ARROW, 158)
    PlotIndexSetInteger(bufferSell_ID, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetInteger(bufferBuy_ID, PLOT_ARROW_SHIFT, 10)
    tickSize = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_SIZE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    i = MathMax(3, prev_calculated - 1)
    for i in range(i, rates_total):
        if (high[i - 2] < high[i - 3] and low[i - 2] > low[i - 3]) and (high[i - 1] < high[i - 2] and low[i - 1] < low[i - 2]):
            bufferHikkake[i - 3] = high[i - 3]
            bufferHikkake[i - 2] = high[i - 2]
            bufferHikkake[i - 1] = high[i - 1]
            bufferHikkake[i] = EMPTY_VALUE
            bufferBuy[i] = EMPTY_VALUE
            bufferSell[i] = EMPTY_VALUE
            bufferHikkakeEntry[i] = high[i - 2] + tickSize
        else:
            if (high[i - 2] < high[i - 3] and low[i - 2] > low[i - 3]) and (high[i - 1] > high[i - 2] and low[i - 1] > low[i - 2]):
                bufferHikkake[i - 3] = low[i - 3]
                bufferHikkake[i - 2] = low[i - 2]
                bufferHikkake[i - 1] = low[i - 1]
                bufferHikkake[i] = EMPTY_VALUE
                bufferBuy[i] = EMPTY_VALUE
                bufferSell[i] = EMPTY_VALUE
                bufferHikkakeEntry[i] = low[i - 2] - tickSize
            else:
                bufferHikkake[i] = EMPTY_VALUE
                bufferHikkakeEntry[i] = EMPTY_VALUE
                bufferBuy[i] = EMPTY_VALUE
                bufferSell[i] = EMPTY_VALUE
        if (bufferHikkakeEntry[i - 2] == EMPTY_VALUE and bufferHikkakeEntry[i - 1] > 0) and bufferHikkakeEntry[i] == EMPTY_VALUE:
            bufferHikkakeEntry[i] = bufferHikkakeEntry[i - 1]
        if ((bufferHikkakeEntry[i - 3] == EMPTY_VALUE and bufferHikkakeEntry[i - 2] > 0) and bufferHikkakeEntry[i - 1] > 0) and bufferHikkakeEntry[i] == EMPTY_VALUE:
            bufferHikkakeEntry[i] = bufferHikkakeEntry[i - 1]
        if (((bufferHikkakeEntry[i] > 0 and bufferHikkake[i - 1] > 0) and bufferHikkake[i - 1] == high[i - 1]) or ((bufferHikkakeEntry[i] > 0 and bufferHikkake[i - 2] > 0) and bufferHikkake[i - 2] == high[i - 2])) or ((bufferHikkakeEntry[i] > 0 and bufferHikkake[i - 3] > 0) and bufferHikkake[i - 3] == high[i - 3]):
            if (high[i] >= bufferHikkakeEntry[i] and bufferBuy[i - 1] == EMPTY_VALUE) and bufferBuy[i - 2] == EMPTY_VALUE:
                bufferBuy[i] = bufferHikkakeEntry[i]
        if (((bufferHikkakeEntry[i] > 0 and bufferHikkake[i - 1] > 0) and bufferHikkake[i - 1] == low[i - 1]) or ((bufferHikkakeEntry[i] > 0 and bufferHikkake[i - 2] > 0) and bufferHikkake[i - 2] == low[i - 2])) or ((bufferHikkakeEntry[i] > 0 and bufferHikkake[i - 3] > 0) and bufferHikkake[i - 3] == low[i - 3]):
            if (low[i] <= bufferHikkakeEntry[i] and bufferSell[i - 1] == EMPTY_VALUE) and bufferSell[i - 2] == EMPTY_VALUE:
                bufferSell[i] = bufferHikkakeEntry[i]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MinionsHikkake(_MQL5Indicator):
    name = 'Minions.Hikkake'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

