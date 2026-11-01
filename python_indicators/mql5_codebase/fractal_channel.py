"""Fractal_Channel — converted from MQL5: MQL5 Indicators/Fractal_Channel/Fractal_Channel.mq5

Fractal Channel indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper', 2: 'Lower'}, 'levels': [], 'description': ['Fractal Channel indicator'], 'name': 'Fractal_Channel', 'source': 'MQL5 Indicators/Fractal_Channel/Fractal_Channel.mq5', 'folder': 'Fractal_Channel', 'inputs': [{'mql': 'InpFrames', 'py': 'InpFrames', 'param': 'InpFrames', 'type': 'uint', 'default': 5, 'label': 'Frame', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFrames = _input('InpFrames', 5)  # Frame
BufferUpper = Arr(0, 0.0)
BufferLower = Arr(0, 0.0)
frames = 0
shift = 0

def OnInit():
    global frames, shift
    frames = (3 if (InpFrames < 3) else InpFrames)
    shift = _idiv(frames - 1, 2)
    SetIndexBuffer(0, BufferUpper, INDICATOR_DATA)
    SetIndexBuffer(1, BufferLower, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fractal channel (' + _str(frames) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUpper, True)
    ArraySetAsSeries(BufferLower, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - shift - 3
        ArrayInitialize(BufferUpper, EMPTY_VALUE)
        ArrayInitialize(BufferLower, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        UpFr = True
        DnFr = True
        for j in range(1, shift + 1):
            if high[i + shift] <= high[i + shift - j] or high[i + shift] <= high[i + shift + j]:
                UpFr = False
            if low[i + shift] >= low[i + shift - j] or low[i + shift] >= low[i + shift + j]:
                DnFr = False
        if UpFr:
            for j in range(0, shift + 1):
                BufferUpper[i + shift - j] = high[i + shift]
        else:
            for j in range(0, shift + 1):
                BufferUpper[i + shift - j] = BufferUpper[i + shift + 1 - j]
        if DnFr:
            for j in range(0, shift + 1):
                BufferLower[i + shift - j] = low[i + shift]
        else:
            for j in range(0, shift + 1):
                BufferLower[i + shift - j] = BufferLower[i + shift + 1 - j]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalChannel(_MQL5Indicator):
    name = 'Fractal_Channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFrames': 5,  # Frame
    }

