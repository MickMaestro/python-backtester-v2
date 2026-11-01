"""BIAS — converted from MQL5: MQL5 Indicators/Deviation Rate BIAS MT5/BIAS.mq5

BIAS
Copyright: Submarine; Link: https://www.mql5.com/en/users/carllin000; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Submarine', 'link': 'https://www.mql5.com/en/users/carllin000', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [65535], 3: [32768]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Long', 2: 'Mid', 3: 'Short'}, 'levels': [], 'description': ['BIAS'], 'name': 'BIAS', 'source': 'MQL5 Indicators/Deviation Rate BIAS MT5/BIAS.mq5', 'folder': 'Deviation Rate BIAS MT5', 'inputs': [{'mql': 'InPeriod', 'py': 'InPeriod', 'param': 'InPeriod', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'InLong', 'py': 'InLong', 'param': 'InLong', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'InMid', 'py': 'InMid', 'param': 'InMid', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'InShort', 'py': 'InShort', 'param': 'InShort', 'type': 'int', 'default': 24, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LongBuffer = Arr(0, 0.0)
MidBuffer = Arr(0, 0.0)
ShortBuffer = Arr(0, 0.0)
Long_h = 0
Mid_h = 0
Short_h = 0
Close_h = 0
InPeriod = _input('InPeriod', PERIOD_CURRENT)
InLong = _input('InLong', 6)
InMid = _input('InMid', 12)
InShort = _input('InShort', 24)

def OnInit():
    global Close_h, Long_h, Mid_h, Short_h
    SetIndexBuffer(0, LongBuffer)
    SetIndexBuffer(1, MidBuffer)
    SetIndexBuffer(2, ShortBuffer)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BIAS(' + _str(InLong) + ',' + _str(InMid) + ',' + _str(InShort) + ')')
    Long_h = iMA(None, InPeriod, InLong, 0, 0, 0)
    Mid_h = iMA(None, InPeriod, InMid, 0, 0, 0)
    Short_h = iMA(None, InPeriod, InShort, 0, 0, 0)
    Close_h = iMA(None, InPeriod, 1, 0, 0, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    Long = Arr(0, 0.0)
    if CopyBuffer(Long_h, 0, 0, rates_total, Long) <= 0:
        return 0
    Mid = Arr(0, 0.0)
    if CopyBuffer(Mid_h, 0, 0, rates_total, Mid) <= 0:
        return 0
    Short = Arr(0, 0.0)
    if CopyBuffer(Short_h, 0, 0, rates_total, Short) <= 0:
        return 0
    Close = Arr(0, 0.0)
    if CopyBuffer(Close_h, 0, 0, rates_total, Close) <= 0:
        return 0
    start = 100
    if prev_calculated > 0:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        LongBuffer[i] = _fdiv(Close[i] - Long[i], Long[i]) * 100
        MidBuffer[i] = _fdiv(Close[i] - Mid[i], Mid[i]) * 100
        ShortBuffer[i] = _fdiv(Close[i] - Short[i], Short[i]) * 100
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BIAS(_MQL5Indicator):
    name = 'BIAS'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InPeriod': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
        'InLong': 6,
        'InMid': 12,
        'InShort': 24,
    }

