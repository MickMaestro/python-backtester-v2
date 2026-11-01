"""PVI_Smoothed — converted from MQL5: MQL5 Indicators/PVI_Smoothed/PVI_Smoothed.mq5

Smoothed Positive Volume Index
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'SPVI', 2: 'Signal'}, 'levels': [], 'description': ['Smoothed Positive Volume Index'], 'name': 'PVI_Smoothed', 'source': 'MQL5 Indicators/PVI_Smoothed/PVI_Smoothed.mq5', 'folder': 'PVI_Smoothed', 'inputs': [{'mql': 'InpPeriodSmooth', 'py': 'InpPeriodSmooth', 'param': 'InpPeriodSmooth', 'type': 'uint', 'default': 5, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpPeriodSignal', 'py': 'InpPeriodSignal', 'param': 'InpPeriodSignal', 'type': 'uint', 'default': 15, 'label': 'Signal line period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodSmooth = _input('InpPeriodSmooth', 5)  # Smoothing period
InpPeriodSignal = _input('InpPeriodSignal', 15)  # Signal line period
BufferPVI = Arr(0, 0.0)
BufferSig = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
period_pvi = 0
period_sig = 0

def OnInit():
    global period_pvi, period_sig
    period_pvi = (1 if (InpPeriodSmooth < 1) else InpPeriodSmooth)
    period_sig = (1 if (InpPeriodSignal < 1) else InpPeriodSignal)
    SetIndexBuffer(0, BufferPVI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSig, INDICATOR_DATA)
    SetIndexBuffer(2, BufferRAW, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SPVI(' + _str(period_pvi) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPVI, True)
    ArraySetAsSeries(BufferSig, True)
    ArraySetAsSeries(BufferRAW, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    max_ = fmax(period_sig, period_pvi)
    if limit > 1:
        limit = rates_total - max_ - 2
        ArrayInitialize(BufferPVI, 0)
        ArrayInitialize(BufferSig, 0)
        ArrayInitialize(BufferRAW, 0)
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - max_ - 2):
            BufferRAW[i] = 1.0
        else:
            if tick_volume[i] > tick_volume[i + 1]:
                BufferRAW[i] = BufferRAW[i + 1] * (1 + _fdiv(close[i] - close[i + 1], close[i + 1]))
            else:
                BufferRAW[i] = BufferRAW[i + 1]
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_pvi, BufferRAW, BufferPVI)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferPVI, BufferSig)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PVISmoothed(_MQL5Indicator):
    name = 'PVI_Smoothed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodSmooth': 5,  # Smoothing period
        'InpPeriodSignal': 15,  # Signal line period
    }

