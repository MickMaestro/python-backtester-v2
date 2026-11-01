"""Cronex DeMarker — converted from MQL5: MQL5 Indicators/Cronex DeMarker/Cronex DeMarker.mq5

Copyright: Copyright © 2007, Cronex; Link: http://www.metaquotes.net/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Cronex', 'link': 'http://www.metaquotes.net/', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [11186720], 2: [64636], 3: [15631086]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'iDeMarker', 2: 'Fast MA', 3: 'Slow MA'}, 'levels': [0.3, 0.7], 'description': [], 'name': 'Cronex DeMarker', 'source': 'MQL5 Indicators/Cronex DeMarker/Cronex DeMarker.mq5', 'folder': 'Cronex DeMarker', 'inputs': [{'mql': 'Inp_DeMarker_ma_period', 'py': 'Inp_DeMarker_ma_period', 'param': 'Inp_DeMarker_ma_period', 'type': 'int', 'default': 14, 'label': 'DeMarker: period of moving average', 'sinput': False}, {'mql': 'Inp_FastMA', 'py': 'Inp_FastMA', 'param': 'Inp_FastMA', 'type': 'int', 'default': 14, 'label': 'Fast MA', 'sinput': False}, {'mql': 'Inp_SlowMA', 'py': 'Inp_SlowMA', 'param': 'Inp_SlowMA', 'type': 'int', 'default': 25, 'label': 'Slow MA', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
Inp_DeMarker_ma_period = _input('Inp_DeMarker_ma_period', 14)  # DeMarker: period of moving average
Inp_FastMA = _input('Inp_FastMA', 14)  # Fast MA
Inp_SlowMA = _input('Inp_SlowMA', 25)  # Slow MA
iDeMarkerBuffer = Arr(0, 0.0)
iDeMarkerBufferMA1 = Arr(0, 0.0)
iDeMarkerBufferMA2 = Arr(0, 0.0)
handle = 0
bars_calculated = 0
weightfast = 0
weightslow = 0

def OnInit():
    global handle
    SetIndexBuffer(0, iDeMarkerBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, iDeMarkerBufferMA1, INDICATOR_DATA)
    SetIndexBuffer(2, iDeMarkerBufferMA2, INDICATOR_DATA)
    handle = iDeMarker(Symbol(), Period(), Inp_DeMarker_ma_period)
    if handle == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iDeMarker indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'DeM(' + IntegerToString(Inp_DeMarker_ma_period) + ',' + IntegerToString(Inp_FastMA) + ',' + IntegerToString(Inp_SlowMA) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    values_to_copy = 0
    calculated = BarsCalculated(handle)
    if calculated <= 0:
        PrintFormat('BarsCalculated() returned %d, error code %d', calculated, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(iDeMarkerBuffer, handle, values_to_copy):
        return 0
    bars_calculated = calculated
    LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, Inp_FastMA, iDeMarkerBuffer, iDeMarkerBufferMA1, _GlobRef(globals(), 'weightfast'))
    LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, Inp_SlowMA, iDeMarkerBuffer, iDeMarkerBufferMA2, _GlobRef(globals(), 'weightslow'))
    return rates_total

def FillArrayFromBuffer(values, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, values) < 0:
        PrintFormat('Failed to copy data from the iDeMarker indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    Comment('')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CronexDeMarker(_MQL5Indicator):
    name = 'Cronex DeMarker'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_DeMarker_ma_period': 14,  # DeMarker: period of moving average
        'Inp_FastMA': 14,  # Fast MA
        'Inp_SlowMA': 25,  # Slow MA
    }

