"""Didi_Index — converted from MQL5: MQL5 Indicators/Didi_Index_HTF/Didi_Index.mq5

Copyright: Rudinei Felipetto; Link: http://www.conttinua.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rudinei Felipetto', 'link': 'http://www.conttinua.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [65280], 2: [16777215], 3: [65535]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Curta', 2: 'Media', 3: 'Longa'}, 'levels': [], 'description': [], 'name': 'Didi_Index', 'source': 'MQL5 Indicators/Didi_Index_HTF/Didi_Index.mq5', 'folder': 'Didi_Index_HTF', 'inputs': [{'mql': 'Curta', 'py': 'Curta', 'param': 'Curta', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Media', 'py': 'Media', 'param': 'Media', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Longa', 'py': 'Longa', 'param': 'Longa', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Curta = _input('Curta', 3)
Media = _input('Media', 8)
Longa = _input('Longa', 20)
CurtaBuffer = Arr(0, 0.0)
MediaBuffer = Arr(0, 0.0)
LongaBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, CurtaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MediaBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LongaBuffer, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (Longa - 1 + begin):
        return 0
    if prev_calculated == 0:
        ArrayInitialize(CurtaBuffer, 0)
        ArrayInitialize(MediaBuffer, 0)
        ArrayInitialize(LongaBuffer, 0)
    CalculateDidiIndex()
    return rates_total

def OnTradeTransaction(trans, request, result):
    pass

def CalculateDidiIndex():
    short_handle = 0
    average_handle = 0
    long_handle = 0
    short_bars = 0
    average_bars = 0
    long_bars = 0
    short_handle = iMA(Symbol(), PERIOD_CURRENT, Curta, 0, MODE_SMA, PRICE_CLOSE)
    average_handle = iMA(Symbol(), PERIOD_CURRENT, Media, 0, MODE_SMA, PRICE_CLOSE)
    long_handle = iMA(Symbol(), PERIOD_CURRENT, Longa, 0, MODE_SMA, PRICE_CLOSE)
    short_bars = BarsCalculated(short_handle)
    average_bars = BarsCalculated(average_handle)
    long_bars = BarsCalculated(long_handle)
    CopyBuffer(short_handle, 0, 0, short_bars, CurtaBuffer)
    CopyBuffer(average_handle, 0, 0, average_bars, MediaBuffer)
    CopyBuffer(long_handle, 0, 0, long_bars, LongaBuffer)
    for i in range(0, short_bars):
        if not MediaBuffer[i]:
            MediaBuffer[i] = EMPTY_VALUE
        if i >= Media:
            CurtaBuffer[i] = _fdiv(CurtaBuffer[i], MediaBuffer[i])
            if i >= Longa:
                LongaBuffer[i] = _fdiv(LongaBuffer[i], MediaBuffer[i])
            else:
                LongaBuffer[i] = 1.0
        else:
            CurtaBuffer[i] = 1.0
        MediaBuffer[i] = 1.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DidiIndex(_MQL5Indicator):
    name = 'Didi_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Curta': 3,
        'Media': 8,
        'Longa': 20,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

