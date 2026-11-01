"""Candles_parbitrary_seconds8_1.1 — converted from MQL5: MQL5 Indicators/Candles, arbitrary seconds/Candles_parbitrary_seconds8_1.1.mq5

Copyright: mladen; Link: www.forex-tsd.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [8421504, 3329330, 6333684]}, 'widths': {}, 'styles': {}, 'labels': {1: 'open;high;low;close'}, 'levels': [], 'description': [], 'name': 'Candles_parbitrary_seconds8_1.1', 'source': 'MQL5 Indicators/Candles, arbitrary seconds/Candles_parbitrary_seconds8_1.1.mq5', 'folder': 'Candles, arbitrary seconds', 'inputs': [{'mql': 'Seconds', 'py': 'Seconds', 'param': 'Seconds', 'type': 'int', 'default': 3, 'label': 'Seconds for candles interval', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Seconds = _input('Seconds', 3)  # Seconds for candles interval
canc = Arr(0, 0.0)
cano = Arr(0, 0.0)
canh = Arr(0, 0.0)
canl = Arr(0, 0.0)
colors = Arr(0, 0.0)
seconds = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, cano, INDICATOR_DATA)
    SetIndexBuffer(1, canh, INDICATOR_DATA)
    SetIndexBuffer(2, canl, INDICATOR_DATA)
    SetIndexBuffer(3, canc, INDICATOR_DATA)
    SetIndexBuffer(4, colors, INDICATOR_COLOR_INDEX)
    EventSetTimer(Seconds)
    IndicatorSetString(INDICATOR_SHORTNAME, _str(Seconds) + ' seconds chart')
    return 0

def OnDeinit(reason):
    EventKillTimer()

def OnTimer():
    close = Arr(0, 0.0)
    CopyClose(Symbol(), Period(), 0, 1, close)
    size = ArrayRange(seconds, 0)
    ArrayResize(seconds, size + 1)
    seconds[size][0] = close[0]
    seconds[size][1] = close[0]
    seconds[size][2] = close[0]
    seconds[size][3] = close[0]
    updateData()

def updateData():
    rates_total = ArraySize(canh)
    size = ArrayRange(seconds, 0)
    if size <= 0:
        for i in range(rates_total - 1, 0 - 1, -1):
            canh[i] = EMPTY_VALUE
            canl[i] = EMPTY_VALUE
            cano[i] = EMPTY_VALUE
            canc[i] = EMPTY_VALUE
        return
    close = Arr(0, 0.0)
    CopyClose(Symbol(), Period(), 0, 1, close)
    seconds[size - 1][2] = MathMax(seconds[size - 1][2], close[0])
    seconds[size - 1][3] = MathMin(seconds[size - 1][3], close[0])
    seconds[size - 1][1] = close[0]
    for i in range(MathMin(rates_total - 1, size - 1), 0 - 1, -1):
        y = rates_total - i - 1
        canh[y] = seconds[size - i - 1][2]
        canl[y] = seconds[size - i - 1][3]
        cano[y] = seconds[size - i - 1][0]
        canc[y] = seconds[size - i - 1][1]
        colors[y] = (2 if (cano[y] > canc[y]) else 1 if (cano[y] < canc[y]) else 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    bars = Bars(Symbol(), Period())
    if bars < rates_total:
        return -1
    updateData()
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandlesParbitrarySeconds811(_MQL5Indicator):
    name = 'Candles_parbitrary_seconds8_1.1'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Seconds': 3,  # Seconds for candles interval
    }

