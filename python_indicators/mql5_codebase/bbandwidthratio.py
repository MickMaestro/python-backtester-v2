"""BBandWidthRatio — converted from MQL5: MQL5 Indicators/BBand Width Ratio/BBandWidthRatio.mq5

Copyright: Copyright 2017, sachjo; Link: https://; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2017, sachjo', 'link': 'https://', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [65535]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'BBandWidth'}, 'levels': [], 'description': [], 'name': 'BBandWidthRatio', 'source': 'MQL5 Indicators/BBand Width Ratio/BBandWidthRatio.mq5', 'folder': 'BBand Width Ratio', 'inputs': [{'mql': 'BB_Period', 'py': 'BB_Period', 'param': 'BB_Period', 'type': 'int', 'default': 25, 'label': 'BBands Period', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 2.0, 'label': 'Standard Deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buf = Arr(0, 0.0)
BufMA = Arr(0, 0.0)
BB_Period = _input('BB_Period', 25)  # BBands Period
Deviation = _input('Deviation', 2.0)  # Standard Deviation
hMA = 0

def OnInit():
    global hMA
    SetIndexBuffer(0, Buf, INDICATOR_DATA)
    hMA = iMA(None, 0, BB_Period, 0, MODE_SMA, PRICE_CLOSE)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    IndicatorRelease(hMA)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated
    if prev_calculated > 0:
        limit -= 1
    count = rates_total - limit
    if CopyBuffer(hMA, 0, 0, count, BufMA) < count:
        return 0
    for i in range(limit, rates_total):
        if i < BB_Period:
            Buf[i] = 0.0
        else:
            sum_ = 0.0
            for j in range(0, BB_Period):
                sum_ += close[i - j]
            ave = sum_ / BB_Period
            sum_ = 0.0
            for j in range(0, BB_Period):
                sum_ += (close[i - j] - ave) * (close[i - j] - ave)
            sko = MathSqrt(sum_ / BB_Period)
            Buf[i] = _fdiv(2 * (Deviation * sko), BufMA[i - limit])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBandWidthRatio(_MQL5Indicator):
    name = 'BBandWidthRatio'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BB_Period': 25,  # BBands Period
        'Deviation': 2.0,  # Standard Deviation
    }

