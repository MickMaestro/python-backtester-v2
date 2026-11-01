"""Delta_oscillator — converted from MQL5: MQL5 Indicators/Delta_Oscillator/Delta_oscillator.mq5

Delta oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Delta Osc'}, 'levels': [], 'description': ['Delta oscillator'], 'name': 'Delta_oscillator', 'source': 'MQL5 Indicators/Delta_Oscillator/Delta_oscillator.mq5', 'folder': 'Delta_Oscillator', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BufferOSC = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
BufferDelta = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferOSC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferPrice, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferDelta, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Delta Oscillator')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferOSC, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferPrice, True)
    ArraySetAsSeries(BufferDelta, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferOSC, EMPTY_VALUE)
        ArrayInitialize(BufferPrice, 0)
        ArrayInitialize(BufferDelta, 0)
    for i in range(limit, 0 - 1, -1):
        BufferPrice[i] = (open[i] + high[i] + low[i] + close[i]) / 4.0
        if BufferPrice[i] > 0 and BufferPrice[i + 1] > 0:
            BufferDelta[i] = BufferPrice[i] + log10(_fdiv(BufferPrice[i + 1], BufferPrice[i]))
        BufferOSC[i] = ((BufferPrice[i] - BufferDelta[i]) if (BufferDelta[i] != 0) else EMPTY_VALUE)
        BufferColors[i] = (0 if (BufferOSC[i] > BufferOSC[i + 1]) else 1 if (BufferOSC[i] < BufferOSC[i + 1]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DeltaOscillator(_MQL5Indicator):
    name = 'Delta_oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

