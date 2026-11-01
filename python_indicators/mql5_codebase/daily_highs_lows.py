"""Daily_Highs_Lows — converted from MQL5: MQL5 Indicators/Dynamic Support and Resistance/Daily_Highs_Lows.mq5

Identify Daily Highs and Lows
with line acting as support and resistance
Copyright: Copyright 2023, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 3, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Prev Day High', 2: 'Prev Day Low'}, 'levels': [], 'description': ['Identify Daily Highs and Lows', 'with line acting as support and resistance'], 'name': 'Daily_Highs_Lows', 'source': 'MQL5 Indicators/Dynamic Support and Resistance/Daily_Highs_Lows.mq5', 'folder': 'Dynamic Support and Resistance', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
prevDayH = Arr(0, 0.0)
prevDayL = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, prevDayH, INDICATOR_DATA)
    SetIndexBuffer(1, prevDayL, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(prev_calculated, rates_total):
        shift = iBarShift(Symbol(), PERIOD_D1, time[i])
        highD1 = iHigh(Symbol(), PERIOD_D1, shift + 1)
        lowD1 = iLow(Symbol(), PERIOD_D1, shift + 1)
        prevDayH[i] = highD1
        prevDayL[i] = lowD1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailyHighsLows(_MQL5Indicator):
    name = 'Daily_Highs_Lows'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

