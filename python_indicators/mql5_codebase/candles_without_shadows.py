"""Candles without shadows — converted from MQL5: MQL5 Indicators/Candles without shadows/Candles without shadows.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16443110, 3329330, 8421504]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ColorCandles'}, 'levels': [], 'description': [], 'name': 'Candles without shadows', 'source': 'MQL5 Indicators/Candles without shadows/Candles without shadows.mq5', 'folder': 'Candles without shadows', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BufferOpen = Arr(0, 0.0)
BufferHigh = Arr(0, 0.0)
BufferLow = Arr(0, 0.0)
BufferClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferOpen, INDICATOR_DATA)
    SetIndexBuffer(1, BufferHigh, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLow, INDICATOR_DATA)
    SetIndexBuffer(3, BufferClose, INDICATOR_DATA)
    SetIndexBuffer(4, BufferColors, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    symbol = Symbol()
    PlotIndexSetString(0, PLOT_LABEL, symbol + ' Open;' + symbol + ' High;' + symbol + ' Low;' + symbol + ' Close')
    IndicatorSetString(INDICATOR_SHORTNAME, 'DRAW_COLOR_CANDLES(' + symbol + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        BufferOpen[i] = open[i]
        BufferClose[i] = close[i]
        if open[i] < close[i]:
            BufferHigh[i] = close[i]
            BufferLow[i] = open[i]
            BufferColors[i] = 0.0
        else:
            BufferHigh[i] = open[i]
            BufferLow[i] = close[i]
            if open[i] > close[i]:
                BufferColors[i] = 1.0
            else:
                BufferColors[i] = 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandlesWithoutShadows(_MQL5Indicator):
    name = 'Candles without shadows'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

