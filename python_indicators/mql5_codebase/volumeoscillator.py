"""VolumeOscillator — converted from MQL5: MQL5 Indicators/Volume Oscillator/VolumeOscillator.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Volume OSC'}, 'levels': [], 'description': [], 'name': 'VolumeOscillator', 'source': 'MQL5 Indicators/Volume Oscillator/VolumeOscillator.mq5', 'folder': 'Volume Oscillator', 'inputs': [{'mql': 'InpPeriodShort', 'py': 'InpPeriodShort', 'param': 'InpPeriodShort', 'type': 'uint', 'default': 5, 'label': 'Short Length', 'sinput': False}, {'mql': 'InpPeriodLong', 'py': 'InpPeriodLong', 'param': 'InpPeriodLong', 'type': 'uint', 'default': 10, 'label': 'Long Length', 'sinput': False}, {'mql': 'InpVolume', 'py': 'InpVolume', 'param': 'InpVolume', 'type': 'int', 'default': 0, 'label': 'Volume', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodShort = _input('InpPeriodShort', 5)  # Short Length
InpPeriodLong = _input('InpPeriodLong', 10)  # Long Length
InpVolume = _input('InpVolume', VOLUME_TICK)  # Volume
ExtBufferOSC = Arr(0, 0.0)
ExtBufferVolume = Arr(0, 0.0)
ExtBufferEMALong = Arr(0, 0.0)
ExtBufferEMAShort = Arr(0, 0.0)
ExtPeriodLong = 0
ExtPeriodShort = 0

def OnInit():
    global ExtPeriodLong, ExtPeriodShort
    SetIndexBuffer(0, ExtBufferOSC, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBufferVolume, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtBufferEMALong, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtBufferEMAShort, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtBufferOSC, True)
    ArraySetAsSeries(ExtBufferVolume, True)
    ArraySetAsSeries(ExtBufferEMALong, True)
    ArraySetAsSeries(ExtBufferEMAShort, True)
    ExtPeriodLong = (1 if (InpPeriodLong < 1) else InpPeriodLong)
    ExtPeriodShort = (1 if (InpPeriodShort < 1) else InpPeriodShort)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Volume Osc (%lu, %lu)', ExtPeriodShort, ExtPeriodLong))
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = fmax(ExtPeriodLong, ExtPeriodShort)
    if rates_total < fmax(max_, 2):
        return 0
    ArraySetAsSeries(volume, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1 - max_
        ArrayInitialize(ExtBufferOSC, EMPTY_VALUE)
        ArrayInitialize(ExtBufferVolume, 0)
        ArrayInitialize(ExtBufferEMALong, 0)
        ArrayInitialize(ExtBufferEMAShort, 0)
    for i in range(limit, 0 - 1, -1):
        ExtBufferVolume[i] = float((tick_volume[i] if (InpVolume == VOLUME_TICK) else volume[i]))
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, ExtPeriodLong, ExtBufferVolume, ExtBufferEMALong) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, ExtPeriodShort, ExtBufferVolume, ExtBufferEMAShort) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        ExtBufferOSC[i] = (_fdiv(100 * (ExtBufferEMAShort[i] - ExtBufferEMALong[i]), ExtBufferEMALong[i]) if (ExtBufferEMALong[i] != 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeOscillator(_MQL5Indicator):
    name = 'VolumeOscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodShort': 5,  # Short Length
        'InpPeriodLong': 10,  # Long Length
        'InpVolume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume
    }

