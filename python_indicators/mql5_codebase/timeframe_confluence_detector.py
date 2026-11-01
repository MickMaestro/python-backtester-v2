"""Timeframe Confluence Detector — converted from MQL5: MQL5 Indicators/Confluence Detector/Timeframe Confluence Detector.mq5

Copyright: phade; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Functions not available here: CopySeries
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'phade', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [8894686], 2: [8421504], 3: [11119017]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Timeframe Confluence Detector', 'source': 'MQL5 Indicators/Confluence Detector/Timeframe Confluence Detector.mq5', 'folder': 'Confluence Detector', 'inputs': [{'mql': 'timeframe_a', 'py': 'timeframe_a', 'param': 'timeframe_a', 'type': 'int', 'default': 0, 'label': 'Current period', 'sinput': False}, {'mql': 'timeframe_b', 'py': 'timeframe_b', 'param': 'timeframe_b', 'type': 'int', 'default': 16386, 'label': '1st timeframe deviation to current period', 'sinput': False}, {'mql': 'timeframe_c', 'py': 'timeframe_c', 'param': 'timeframe_c', 'type': 'int', 'default': 16385, 'label': '2nd timeframe deviation to current period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

COPY_RATES_CLOSE = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
timeframe_a = _input('timeframe_a', PERIOD_CURRENT)  # Current period
timeframe_b = _input('timeframe_b', PERIOD_H2)  # 1st timeframe deviation to current period
timeframe_c = _input('timeframe_c', PERIOD_H1)  # 2nd timeframe deviation to current period
bars = 0
buf_a = Arr(0, 0.0)
buf_b = Arr(0, 0.0)
buf_c = Arr(0, 0.0)
deviator_a = Arr(0, 0.0)
deviator_b = Arr(0, 0.0)

def OnInit():
    IndicatorRelease(0)
    SetIndexBuffer(0, buf_a, INDICATOR_DATA)
    SetIndexBuffer(1, deviator_a, INDICATOR_DATA)
    SetIndexBuffer(2, deviator_b, INDICATOR_DATA)
    SetIndexBuffer(3, buf_b, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, buf_c, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(buf_a, True)
    ArraySetAsSeries(buf_b, True)
    ArraySetAsSeries(buf_c, True)
    ArraySetAsSeries(deviator_a, True)
    ArraySetAsSeries(deviator_b, True)
    PlotIndexSetString(0, PLOT_LABEL, TimeframeToString(timeframe_a))
    PlotIndexSetString(1, PLOT_LABEL, 'Deviation from ' + TimeframeToString(timeframe_b) + ' to ' + TimeframeToString(timeframe_a))
    PlotIndexSetString(2, PLOT_LABEL, 'Deviation from ' + TimeframeToString(timeframe_c) + ' to ' + TimeframeToString(timeframe_a))
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _missing('CopySeries')(Symbol(), timeframe_a, 0, rates_total, COPY_RATES_CLOSE, buf_a)
    _missing('CopySeries')(Symbol(), timeframe_b, 0, rates_total, COPY_RATES_CLOSE, buf_b)
    _missing('CopySeries')(Symbol(), timeframe_c, 0, rates_total, COPY_RATES_CLOSE, buf_c)
    for i in range(rates_total - 1, 0 - 1, -1):
        deviator_a[i] = MathAbs(buf_b[i] - buf_a[i]) + buf_b[i] - (60 * Point())
        deviator_b[i] = MathAbs(buf_c[i] - buf_a[i]) + buf_c[i] - (60 * 2 * Point())
    return rates_total

def TimeframeToString(timeframe):
    result = ""
    _sw1 = timeframe
    if _sw1 == PERIOD_M1:
        result = 'M1'
    elif _sw1 == PERIOD_M5:
        result = 'M5'
    elif _sw1 == PERIOD_M15:
        result = 'M15'
    elif _sw1 == PERIOD_M30:
        result = 'M30'
    elif _sw1 == PERIOD_H1:
        result = 'H1'
    elif _sw1 == PERIOD_H2:
        result = 'H2'
    elif _sw1 == PERIOD_H4:
        result = 'H4'
    elif _sw1 == PERIOD_D1:
        result = 'D1'
    elif _sw1 == PERIOD_W1:
        result = 'W1'
    elif _sw1 == PERIOD_MN1:
        result = 'MN1'
    else:
        result = ''
    return result


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TimeframeConfluenceDetector(_MQL5Indicator):
    name = 'Timeframe Confluence Detector'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'timeframe_a': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Current period
        'timeframe_b': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16386),  # 1st timeframe deviation to current period
        'timeframe_c': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # 2nd timeframe deviation to current period
    }

