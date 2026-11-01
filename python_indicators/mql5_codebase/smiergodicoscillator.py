"""SMIErgodicOscillator — converted from MQL5: MQL5 Indicators/SMI Ergodic Oscillator/SMIErgodicOscillator.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [255]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'SMIO'}, 'levels': [], 'description': [], 'name': 'SMIErgodicOscillator', 'source': 'MQL5 Indicators/SMI Ergodic Oscillator/SMIErgodicOscillator.mq5', 'folder': 'SMI Ergodic Oscillator', 'inputs': [{'mql': 'InpPeriodLong', 'py': 'InpPeriodLong', 'param': 'InpPeriodLong', 'type': 'uint', 'default': 20, 'label': 'Long Length', 'sinput': False}, {'mql': 'InpPeriodShort', 'py': 'InpPeriodShort', 'param': 'InpPeriodShort', 'type': 'uint', 'default': 5, 'label': 'Short Length', 'sinput': False}, {'mql': 'InpPeriodSignal', 'py': 'InpPeriodSignal', 'param': 'InpPeriodSignal', 'type': 'uint', 'default': 5, 'label': 'Signal Line Length', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodLong = _input('InpPeriodLong', 20)  # Long Length
InpPeriodShort = _input('InpPeriodShort', 5)  # Short Length
InpPeriodSignal = _input('InpPeriodSignal', 5)  # Signal Line Length
ExtBufferSMIO = Arr(0, 0.0)
ExtBufferSig = Arr(0, 0.0)
ExtBufferTSI = Arr(0, 0.0)
ExtBufferUDM = Arr(0, 0.0)
ExtBufferADM = Arr(0, 0.0)
ExtBufferUDM1 = Arr(0, 0.0)
ExtBufferUDM2 = Arr(0, 0.0)
ExtBufferADM1 = Arr(0, 0.0)
ExtBufferADM2 = Arr(0, 0.0)
ExtPeriodLong = 0
ExtPeriodShort = 0
ExtPeriodSignal = 0

def OnInit():
    global ExtPeriodLong, ExtPeriodShort, ExtPeriodSignal
    SetIndexBuffer(0, ExtBufferSMIO, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBufferSig, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtBufferTSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtBufferUDM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtBufferADM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtBufferUDM1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ExtBufferUDM2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, ExtBufferADM1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, ExtBufferADM2, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtBufferSMIO, True)
    ArraySetAsSeries(ExtBufferSig, True)
    ArraySetAsSeries(ExtBufferTSI, True)
    ArraySetAsSeries(ExtBufferUDM, True)
    ArraySetAsSeries(ExtBufferADM, True)
    ArraySetAsSeries(ExtBufferUDM1, True)
    ArraySetAsSeries(ExtBufferUDM2, True)
    ArraySetAsSeries(ExtBufferADM1, True)
    ArraySetAsSeries(ExtBufferADM2, True)
    ExtPeriodLong = (2 if (InpPeriodLong < 2) else InpPeriodLong)
    ExtPeriodShort = (2 if (InpPeriodShort < 2) else InpPeriodShort)
    ExtPeriodSignal = (2 if (InpPeriodSignal < 2) else InpPeriodSignal)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('SMIO (%lu, %lu, %lu)', ExtPeriodLong, ExtPeriodShort, ExtPeriodSignal))
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = fmax(ExtPeriodLong, fmax(ExtPeriodShort, ExtPeriodSignal))
    if rates_total < max_:
        return 0
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(ExtBufferSMIO, EMPTY_VALUE)
        ArrayInitialize(ExtBufferSig, 0)
        ArrayInitialize(ExtBufferTSI, 0)
        ArrayInitialize(ExtBufferUDM, 0)
        ArrayInitialize(ExtBufferUDM1, 0)
        ArrayInitialize(ExtBufferUDM2, 0)
        ArrayInitialize(ExtBufferADM, 0)
        ArrayInitialize(ExtBufferADM1, 0)
        ArrayInitialize(ExtBufferADM2, 0)
    for i in range(limit, 0 - 1, -1):
        ExtBufferUDM[i] = close[i] - close[i + 1]
        ExtBufferADM[i] = fabs(ExtBufferUDM[i])
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, ExtPeriodShort, ExtBufferUDM, ExtBufferUDM1) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, ExtPeriodShort, ExtBufferADM, ExtBufferADM1) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, ExtPeriodShort, ExtPeriodLong, ExtBufferUDM1, ExtBufferUDM2) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, ExtPeriodShort, ExtPeriodLong, ExtBufferADM1, ExtBufferADM2) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        ExtBufferTSI[i] = (_fdiv(100.0 * ExtBufferUDM2[i], ExtBufferADM2[i]) if (ExtBufferADM2[i] != 0) else 0)
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, ExtPeriodSignal, ExtBufferTSI, ExtBufferSig) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        ExtBufferSMIO[i] = ExtBufferTSI[i] - ExtBufferSig[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SMIErgodicOscillator(_MQL5Indicator):
    name = 'SMIErgodicOscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodLong': 20,  # Long Length
        'InpPeriodShort': 5,  # Short Length
        'InpPeriodSignal': 5,  # Signal Line Length
    }

