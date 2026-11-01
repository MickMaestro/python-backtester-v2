"""ZigZag_Oscillator — converted from MQL5: MQL5 Indicators/ZigZag_Oscillator/ZigZag_Oscillator.mq5

ZigZag Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [3329330, 8894686, 17919, 11186720, 11119017]}, 'widths': {1: 6}, 'styles': {1: 0}, 'labels': {1: 'ZigZag Osc'}, 'levels': [], 'description': ['ZigZag Oscillator'], 'name': 'ZigZag_Oscillator', 'source': 'MQL5 Indicators/ZigZag_Oscillator/ZigZag_Oscillator.mq5', 'folder': 'ZigZag_Oscillator', 'inputs': [{'mql': 'InpDepth', 'py': 'InpDepth', 'param': 'InpDepth', 'type': 'uint', 'default': 12, 'label': 'ZigZag Depth', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'uint', 'default': 5, 'label': 'ZigZag Deviation', 'sinput': False}, {'mql': 'InpBackstep', 'py': 'InpBackstep', 'param': 'InpBackstep', 'type': 'uint', 'default': 3, 'label': 'ZigZag Backstep', 'sinput': False}, {'mql': 'InpPivotPoint', 'py': 'InpPivotPoint', 'param': 'InpPivotPoint', 'type': 'uchar', 'default': 1, 'label': 'ZigZag pivot point', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpDepth = _input('InpDepth', 12)  # ZigZag Depth
InpDeviation = _input('InpDeviation', 5)  # ZigZag Deviation
InpBackstep = _input('InpBackstep', 3)  # ZigZag Backstep
InpPivotPoint = _input('InpPivotPoint', 1)  # ZigZag pivot point
BufferZZOsc = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferZZ = Arr(0, 0.0)
BufferZZUP = Arr(0, 0.0)
BufferZZDN = Arr(0, 0.0)
BufferHigh = Arr(0, 0.0)
BufferLow = Arr(0, 0.0)
depth = 0
deviation = 0
backstep = 0
pivot = 0
handle_zz = 0

def OnInit():
    global backstep, depth, deviation, handle_zz, pivot
    backstep = (1 if (InpBackstep < 1) else InpBackstep)
    depth = (backstep if (_int(InpDepth) < backstep) else 1 if (InpDepth < 1) else InpDepth)
    deviation = (1 if (InpDeviation < 1) else InpDeviation)
    pivot = InpPivotPoint
    SetIndexBuffer(0, BufferZZOsc, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferZZ, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferZZUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferZZDN, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferHigh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferLow, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ZigZag Oscillator (' + _str(depth) + ',' + _str(deviation) + ',' + _str(backstep) + ', Pivot ' + _str(pivot) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, 'ZZOsc(' + _str(depth) + ',' + _str(deviation) + ',' + _str(backstep) + ',' + _str(pivot) + ')')
    ArraySetAsSeries(BufferZZOsc, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferZZ, True)
    ArraySetAsSeries(BufferZZUP, True)
    ArraySetAsSeries(BufferZZDN, True)
    ArraySetAsSeries(BufferHigh, True)
    ArraySetAsSeries(BufferLow, True)
    ResetLastError()
    handle_zz = iCustom(None, PERIOD_CURRENT, 'Examples\\ZigZag', depth, deviation, backstep)
    if handle_zz == INVALID_HANDLE:
        Print('The iCustom(MQL5/Indicators/Examples/ZigZag (', _str(depth), ',', _str(deviation), ',', _str(backstep), ')) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(depth, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 0:
        limit = rates_total - 2
        ArrayInitialize(BufferZZOsc, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 4)
        ArrayInitialize(BufferZZ, 0)
        ArrayInitialize(BufferZZUP, 0)
        ArrayInitialize(BufferZZDN, 0)
        ArrayInitialize(BufferHigh, 0)
        ArrayInitialize(BufferLow, 0)
    count = (rates_total if (limit > 0) else 1)
    copied = 0
    copied = CopyBuffer(handle_zz, 0, 0, count, BufferZZ)
    if copied != count:
        return 0
    last_zz = 0.0
    index = 0
    for i in range(limit, 0 - 1, -1):
        index = GetIndexExtremumZZ(rates_total, i, pivot, BufferZZ)
        if index == WRONG_VALUE:
            continue
        last_zz = BufferZZ[index]
        BufferZZOsc[i] = (_fdiv(100 * (close[i] - last_zz), last_zz) if (last_zz != 0) else 0)
        BufferColors[i] = ((0 if (BufferZZOsc[i] > BufferZZOsc[i + 1]) else 1 if (BufferZZOsc[i] < BufferZZOsc[i + 1]) else 4) if (BufferZZOsc[i] > 0) else (2 if (BufferZZOsc[i] < BufferZZOsc[i + 1]) else 3 if (BufferZZOsc[i] > BufferZZOsc[i + 1]) else 4) if (BufferZZOsc[i] < 0) else 4)
    return rates_total
    return rates_total

def GetIndexExtremumZZ(rates_total, shift, pivot_num, buffer_zz):
    k_ext = 0
    index = WRONG_VALUE
    for i in range(shift, rates_total):
        if buffer_zz[i] != 0:
            k_ext += 1
            if k_ext > pivot_num:
                index = i
                break
    return index


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigZagOscillator(_MQL5Indicator):
    name = 'ZigZag_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpDepth': 12,  # ZigZag Depth
        'InpDeviation': 5,  # ZigZag Deviation
        'InpBackstep': 3,  # ZigZag Backstep
        'InpPivotPoint': 1,  # ZigZag pivot point
    }

