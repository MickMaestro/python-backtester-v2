"""Decision_Candles_Colored — converted from MQL5: MQL5 Indicators/Decision Colored Candles - MT5/Decision_Candles_Colored.mq5

Copyright: Mohamed; Link: https://www.mql5.com/en/code/50992; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Mohamed', 'link': 'https://www.mql5.com/en/code/50992', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 2}, 'types': {1: 15, 2: 15}, 'colors': {1: [16711680, 16776960], 2: [255, 36095]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Decision_Candles_Colored', 'source': 'MQL5 Indicators/Decision Colored Candles - MT5/Decision_Candles_Colored.mq5', 'folder': 'Decision Colored Candles - MT5', 'inputs': [{'mql': 'dcpercent', 'py': 'dcpercent', 'param': 'dcpercent', 'type': 'double', 'default': 50.0, 'label': 'Decision Candle Body/range Percentage', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
dcpercent = _input('dcpercent', 50.0)  # Decision Candle Body/range Percentage
buff0 = Arr(0, 0.0)
buff1 = Arr(0, 0.0)
buff2 = Arr(0, 0.0)
buff3 = Arr(0, 0.0)
buff4 = Arr(0, 0.0)
buff5 = Arr(0, 0.0)
buff6 = Arr(0, 0.0)
buff7 = Arr(0, 0.0)

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'DCandles')
    SetIndexBuffer(0, buff0, INDICATOR_DATA)
    SetIndexBuffer(1, buff1, INDICATOR_DATA)
    SetIndexBuffer(2, buff2, INDICATOR_DATA)
    SetIndexBuffer(3, buff3, INDICATOR_DATA)
    SetIndexBuffer(4, buff4, INDICATOR_DATA)
    SetIndexBuffer(5, buff5, INDICATOR_DATA)
    SetIndexBuffer(6, buff6, INDICATOR_DATA)
    SetIndexBuffer(7, buff7, INDICATOR_DATA)
    for in_ in range(0, 8):
        PlotIndexSetInteger(in_, PLOT_SHOW_DATA, False)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = prev_calculated
    if start >= rates_total:
        start = rates_total - 1
    if start < 0:
        start = 0
    for i in range(start, rates_total):
        buff0[i] = EMPTY_VALUE
        buff1[i] = EMPTY_VALUE
        buff2[i] = EMPTY_VALUE
        buff3[i] = EMPTY_VALUE
        buff4[i] = EMPTY_VALUE
        buff5[i] = EMPTY_VALUE
        buff6[i] = EMPTY_VALUE
        buff7[i] = EMPTY_VALUE
        DC = (((high[i] - low[i]) * dcpercent) / 100) <= fabs(close[i] - open[i])
        up = DC and close[i] > open[i]
        dn = DC and close[i] < open[i]
        if up:
            buff0[i] = open[i]
            buff1[i] = high[i]
            buff2[i] = low[i]
            buff3[i] = close[i]
        if dn:
            buff4[i] = open[i]
            buff5[i] = high[i]
            buff6[i] = low[i]
            buff7[i] = close[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DecisionCandlesColored(_MQL5Indicator):
    name = 'Decision_Candles_Colored'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'dcpercent': 50.0,  # Decision Candle Body/range Percentage
    }

