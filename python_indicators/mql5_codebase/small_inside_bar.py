"""Small_Inside_Bar — converted from MQL5: MQL5 Indicators/Small_Inside_Bar/Small_Inside_Bar.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bearish', 2: 'Bullish'}, 'levels': [], 'description': [], 'name': 'Small_Inside_Bar', 'source': 'MQL5 Indicators/Small_Inside_Bar/Small_Inside_Bar.mq5', 'folder': 'Small_Inside_Bar', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BufferBearish = Arr(0, 0.0)
BufferBullish = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferBearish, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBullish, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Small inside bar')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferBullish, True)
    ArraySetAsSeries(BufferBearish, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferBullish, EMPTY_VALUE)
        ArrayInitialize(BufferBearish, EMPTY_VALUE)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    for i in range(limit, 0 - 1, -1):
        bull_flag = False
        bear_flag = False
        ratio = 0.0
        if (high[i] - low[i]) == 0:
            ratio = 10.0
        else:
            ratio = _fdiv(high[i + 1] - low[i + 1], high[i] - low[i])
        if (high[i] < high[i + 1] and low[i] > low[i + 1]) and ratio > 2:
            if (close[i] > open[i] and high[i] < ((high[i + 1] + low[i + 1]) / 2)) and close[i + 1] < open[i + 1]:
                bull_flag = True
            if (close[i] < open[i] and low[i] < ((high[i + 1] + low[i + 1]) / 2)) and close[i + 1] > open[i + 1]:
                bear_flag = True
        if bull_flag:
            BufferBullish[i] = low[i]
        else:
            BufferBullish[i] = EMPTY_VALUE
        if bear_flag:
            BufferBearish[i] = high[i]
        else:
            BufferBearish[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmallInsideBar(_MQL5Indicator):
    name = 'Small_Inside_Bar'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

