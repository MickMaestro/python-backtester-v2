"""Normalized_Volume — converted from MQL5: MQL5 Indicators/Normalized_Volume/Normalized_Volume.mq5

Normalized Volume indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [32768, 255, 11119017], 2: [11119017]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Volume Norm', 2: 'Edge'}, 'levels': [], 'description': ['Normalized Volume indicator'], 'name': 'Normalized_Volume', 'source': 'MQL5 Indicators/Normalized_Volume/Normalized_Volume.mq5', 'folder': 'Normalized_Volume', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpLevel', 'py': 'InpLevel', 'param': 'InpLevel', 'type': 'double', 'default': 100.0, 'label': 'Threshold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpLevel = _input('InpLevel', 100.0)  # Threshold
BufferHist = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferEdge = Arr(0, 0.0)
BufferVolume = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
threshold = 0.0
period_ma = 0

def OnInit():
    global period_ma, threshold
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    threshold = (0 if (InpLevel < 0) else InpLevel)
    SetIndexBuffer(0, BufferHist, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferEdge, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferVolume, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Normalized Volume (' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, threshold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Threshold')
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferHist, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferEdge, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferVolume, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ma - 1
        ArrayInitialize(BufferHist, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferEdge, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferVolume, 0)
    for i in range(limit, 0 - 1, -1):
        BufferVolume[i] = float(tick_volume[i])
        BufferMA[i] = GetSMA(rates_total, i, period_ma, BufferVolume)
        if BufferMA[i] != 0:
            BufferHist[i] = _fdiv(BufferVolume[i], BufferMA[i]) * 100.0
            BufferEdge[i] = BufferHist[i]
            BufferColors[i] = (0 if (BufferHist[i] > threshold) else 1)
        else:
            BufferHist[i] = 0.0
            BufferEdge[i] = BufferHist[i]
            BufferColors[i] = 2.0
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NormalizedVolume(_MQL5Indicator):
    name = 'Normalized_Volume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpLevel': 100.0,  # Threshold
    }

