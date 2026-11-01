"""Bollinger_bands_1b — converted from MQL5: MQL5 Indicators/Bollinger Percent B/Bollinger_bands_1b.mq5

Copyright: Copyright 2014, mohsen khashei; Link: mkhashei@gmail.com; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014, mohsen khashei', 'link': 'mkhashei@gmail.com', 'version': '1.10', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [65535]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Bollinger bands %b'}, 'levels': [0.0, 0.5, 1.0], 'description': [], 'name': 'Bollinger_bands_1b', 'source': 'MQL5 Indicators/Bollinger Percent B/Bollinger_bands_1b.mq5', 'folder': 'Bollinger Percent B', 'inputs': [{'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'BBShift', 'py': 'BBShift', 'param': 'BBShift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'StdDeviation', 'py': 'StdDeviation', 'param': 'StdDeviation', 'type': 'double', 'default': 2.0, 'label': 'Standard Deviation', 'sinput': False}, {'mql': 'appliedprc', 'py': 'appliedprc', 'param': 'appliedprc', 'type': 'int', 'default': 1, 'label': 'Applied Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BBPeriod = _input('BBPeriod', 20)  # Period
BBShift = _input('BBShift', 0)  # Shift
StdDeviation = _input('StdDeviation', 2.0)  # Standard Deviation
appliedprc = _input('appliedprc', PRICE_CLOSE)  # Applied Price
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
BLGBuffer = Arr(0, 0.0)
bbhandle = 0

def OnInit():
    global bbhandle
    SetIndexBuffer(0, BLGBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MiddleBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, UpperBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, LowerBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(BLGBuffer, True)
    ArraySetAsSeries(MiddleBuffer, True)
    ArraySetAsSeries(UpperBuffer, True)
    ArraySetAsSeries(LowerBuffer, True)
    if Bars(Symbol(), Period()) < 60:
        Alert('We have less than 60 bars for Indicator exited now!!')
        return -1
    bbhandle = iBands(None, 0, BBPeriod, BBShift, StdDeviation, appliedprc)
    if bbhandle < 0:
        Alert('Can not create handle ', GetLastError(), '!!')
        return -1
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if BarsCalculated(bbhandle) < rates_total:
        return 0
    if CopyBuffer(bbhandle, 0, 0, rates_total, MiddleBuffer) <= 0:
        return 0
    if CopyBuffer(bbhandle, 1, 0, rates_total, UpperBuffer) <= 0:
        return 0
    if CopyBuffer(bbhandle, 2, 0, rates_total, LowerBuffer) <= 0:
        return 0
    pos = prev_calculated - 1
    if pos < 0:
        pos = 0
    for i in range(pos, rates_total - (BBPeriod + BBShift + 1)):
        BLGBuffer[i] = _fdiv(close[i] - LowerBuffer[i], UpperBuffer[i] - LowerBuffer[i])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BollingerBands1b(_MQL5Indicator):
    name = 'Bollinger_bands_1b'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BBPeriod': 20,  # Period
        'BBShift': 0,  # Shift
        'StdDeviation': 2.0,  # Standard Deviation
        'appliedprc': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied Price
    }

