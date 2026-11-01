"""Volume_Accumulation_Percentage — converted from MQL5: MQL5 Indicators/Volume_Accumulation_Percentage/Volume_Accumulation_Percentage.mq5

Volume Accumulation Percentage indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'VACC'}, 'levels': [], 'description': ['Volume Accumulation Percentage indicator'], 'name': 'Volume_Accumulation_Percentage', 'source': 'MQL5 Indicators/Volume_Accumulation_Percentage/Volume_Accumulation_Percentage.mq5', 'folder': 'Volume_Accumulation_Percentage', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
BufferVACC = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferVA = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
BufferVAA = Arr(0, 0.0)
BufferVolA = Arr(0, 0.0)
period_ind = 0

def OnInit():
    global period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferVACC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferVA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferVAA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferVolA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volume Accumulation Percentage')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferVACC, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferVA, True)
    ArraySetAsSeries(BufferVol, True)
    ArraySetAsSeries(BufferVAA, True)
    ArraySetAsSeries(BufferVolA, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4 or Point() == 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferVACC, 0)
        ArrayInitialize(BufferVA, 0)
        ArrayInitialize(BufferVol, 0)
        ArrayInitialize(BufferVAA, 0)
        ArrayInitialize(BufferVolA, 0)
    for i in range(limit, 0 - 1, -1):
        BufferVA[i] = (_fdiv(Point() * tick_volume[i] * ((2 * close[i]) - high[i] - low[i]), high[i] - low[i]) if ((high[i] - low[i]) != 0) else 0)
        BufferVol[i] = tick_volume[i] * Point()
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVA, BufferVAA)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVol, BufferVolA)
    for i in range(limit, 0 - 1, -1):
        BufferVACC[i] = (_fdiv(100.0 * BufferVAA[i], BufferVolA[i]) if (BufferVolA[i] != 0) else 0)
        BufferColors[i] = (1 if (BufferVACC[i] < BufferVACC[i + 1]) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeAccumulationPercentage(_MQL5Indicator):
    name = 'Volume_Accumulation_Percentage'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
    }

