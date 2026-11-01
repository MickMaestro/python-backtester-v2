"""Positive_Negative_Volume — converted from MQL5: MQL5 Indicators/Positive_Negative_Volume/Positive_Negative_Volume.mq5

Positive Negative Volume
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com/ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com/ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Volume'}, 'levels': [], 'description': ['Positive Negative Volume'], 'name': 'Positive_Negative_Volume', 'source': 'MQL5 Indicators/Positive_Negative_Volume/Positive_Negative_Volume.mq5', 'folder': 'Positive_Negative_Volume', 'inputs': [{'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Calculation method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_METHOD_CALC
METHOD_PR = 0
METHOD_HA = 1
_enum('ENUM_METHOD_CALC', {0: 'METHOD_PR', 1: 'METHOD_HA'})

# ---- inputs and global variables
InpMethod = _input('InpMethod', METHOD_PR)  # Calculation method
BufferHist = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferO = Arr(0, 0.0)
BufferC = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferHist, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferO, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferC, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PNVol')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, 'Volume(' + ('HAshi' if (InpMethod == METHOD_HA) else 'Price') + ')')
    ArraySetAsSeries(BufferHist, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferO, True)
    ArraySetAsSeries(BufferC, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferHist, EMPTY_VALUE)
        ArrayInitialize(BufferO, 0)
        ArrayInitialize(BufferC, 0)
    for i in range(limit, 0 - 1, -1):
        if InpMethod == METHOD_HA:
            if i == (rates_total - 2):
                BufferO[i] = (open[i + 1] + close[i + 1]) / 2
            else:
                BufferO[i] = (BufferO[i + 1] + BufferC[i + 1]) / 2
            BufferC[i] = (open[i] + high[i] + low[i] + close[i]) / 4
        else:
            BufferO[i] = open[i]
            BufferC[i] = close[i]
        if BufferC[i] > BufferO[i]:
            BufferHist[i] = float(tick_volume[i])
            BufferColors[i] = 0.0
        else:
            BufferHist[i] = float(-tick_volume[i])
            BufferColors[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PositiveNegativeVolume(_MQL5Indicator):
    name = 'Positive_Negative_Volume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMethod': _Choice({0: 'Price', 1: 'Heiken Ashi'}, default=0),  # Calculation method
    }

