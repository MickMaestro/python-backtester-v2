"""Candles Ask — converted from MQL5: MQL5 Indicators/Candles Ask/Candles Ask.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13850042]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Ask'}, 'levels': [], 'description': [], 'name': 'Candles Ask', 'source': 'MQL5 Indicators/Candles Ask/Candles Ask.mq5', 'folder': 'Candles Ask', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AskBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, AskBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        AskBuffer[i] = close[i] + (spread[i] * Point())
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandlesAsk(_MQL5Indicator):
    name = 'Candles Ask'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

