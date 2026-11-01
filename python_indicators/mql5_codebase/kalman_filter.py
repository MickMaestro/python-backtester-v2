"""Kalman_Filter — converted from MQL5: MQL5 Indicators/Kalman_Filter/Kalman_Filter.mq5

Kalman Filter indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [8388736]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Kalman Filter'}, 'levels': [], 'description': ['Kalman Filter indicator'], 'name': 'Kalman_Filter', 'source': 'MQL5 Indicators/Kalman_Filter/Kalman_Filter.mq5', 'folder': 'Kalman_Filter', 'inputs': [{'mql': 'InpK', 'py': 'InpK', 'param': 'InpK', 'type': 'double', 'default': 1.0, 'label': 'K', 'sinput': False}, {'mql': 'InpSharpness', 'py': 'InpSharpness', 'param': 'InpSharpness', 'type': 'double', 'default': 1.0, 'label': 'Sharpness', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpK = _input('InpK', 1.0)  # K
InpSharpness = _input('InpSharpness', 1.0)  # Sharpness
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferKF = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferVelocity = Arr(0, 0.0)
k = 0.0
s = 0.0
shK = 0.0
handle_ma = 0

def OnInit():
    global handle_ma, k, s, shK
    k = (0.01 if (InpK < 0.01) else InpK)
    s = (0 if (InpSharpness < 0) else InpSharpness)
    shK = sqrt((s * k) / 100.0)
    SetIndexBuffer(0, BufferKF, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferVelocity, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Kalman Filter (' + DoubleToString(k, 2) + ',' + DoubleToString(s, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferKF, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferVelocity, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferKF, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferVelocity, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - 2):
            BufferVelocity[i] = 0.0
            BufferKF[i] = BufferMA[i]
        else:
            distance = BufferMA[i] - BufferKF[i + 1]
            error = BufferKF[i + 1] + (distance * shK)
            BufferVelocity[i] = BufferVelocity[i + 1] + ((distance * k) / 100.0)
            BufferKF[i] = error + BufferVelocity[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KalmanFilter(_MQL5Indicator):
    name = 'Kalman_Filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpK': 1.0,  # K
        'InpSharpness': 1.0,  # Sharpness
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

