"""Precision_Trend — converted from MQL5: MQL5 Indicators/Precision Trend/Precision_Trend.mq5

Copyright: © mladen, 2017; Link: www.forex-station.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2017', 'link': 'www.forex-station.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [12632256, 3329330, 42495]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'value'}, 'levels': [], 'description': [], 'name': 'Precision_Trend', 'source': 'MQL5 Indicators/Precision Trend/Precision_Trend.mq5', 'folder': 'Precision Trend', 'inputs': [{'mql': 'PtrPeriod', 'py': 'PtrPeriod', 'param': 'PtrPeriod', 'type': 'int', 'default': 14, 'label': 'Precision trend period', 'sinput': False}, {'mql': 'PtrSensitivity', 'py': 'PtrSensitivity', 'param': 'PtrSensitivity', 'type': 'double', 'default': 3.0, 'label': 'Precision trend sensitivity', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PtrPeriod = _input('PtrPeriod', 14)  # Precision trend period
PtrSensitivity = _input('PtrSensitivity', 3.0)  # Precision trend sensitivity
valh = Arr(0, 0.0)
vall = Arr(0, 0.0)
valc = Arr(0, 0.0)
_ptWork = Arr(0, 0.0, dims=(7,))

def OnInit():
    SetIndexBuffer(0, valh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(1, vall, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Precision Trend (' + _str(PtrPeriod) + ',' + _str(PtrSensitivity) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        valc[i] = iPrecisionTrend(high, low, close, PtrPeriod, PtrSensitivity, i, rates_total)
        valh[i] = high[i]
        vall[i] = low[i]
        i += 1
    return i

def iPrecisionTrend(_high, _low, _close, _period, _sensitivity, i, bars, instanceNo=0):
    if ArrayRange(_ptWork, 0) != bars:
        ArrayResize(_ptWork, bars)
    instanceNo *= 7
    r = i
    _ptWork[r][instanceNo + 0] = _high[i] - _low[i]
    _ptWork[r][instanceNo + 2] = _ptWork[r][instanceNo + 0]
    k = 1
    while k < _period and (r - k) >= 0:
        _ptWork[r][instanceNo + 2] += _ptWork[r - k][instanceNo + 0]
        k += 1
    _ptWork[r][instanceNo + 2] = _fdiv(_ptWork[r][instanceNo + 2], k)
    _ptWork[r][instanceNo + 2] *= _sensitivity
    if r == 0:
        _ptWork[r][instanceNo + 1] = 0.0
        _ptWork[r][instanceNo + 3] = _close[i] - _ptWork[r][instanceNo + 2]
        _ptWork[r][instanceNo + 4] = _close[i] + _ptWork[r][instanceNo + 2]
        _ptWork[r][instanceNo + 5] = _close[i]
        _ptWork[r][instanceNo + 6] = _close[i]
    else:
        _ptWork[r][instanceNo + 1] = _ptWork[r - 1][instanceNo + 1]
        _ptWork[r][instanceNo + 3] = _ptWork[r - 1][instanceNo + 3]
        _ptWork[r][instanceNo + 4] = _ptWork[r - 1][instanceNo + 4]
        _ptWork[r][instanceNo + 5] = _ptWork[r - 1][instanceNo + 5]
        _ptWork[r][instanceNo + 6] = _ptWork[r - 1][instanceNo + 6]
        _sw1 = _int(_ptWork[r - 1][instanceNo + 1])
        if _sw1 == 0:
            if _close[i] > _ptWork[r - 1][instanceNo + 4]:
                _ptWork[r][instanceNo + 5] = _close[i]
                _ptWork[r][instanceNo + 3] = _close[i] - _ptWork[r][instanceNo + 2]
                _ptWork[r][instanceNo + 1] = 1.0
            if _close[i] < _ptWork[r - 1][instanceNo + 3]:
                _ptWork[r][instanceNo + 6] = _close[i]
                _ptWork[r][instanceNo + 4] = _close[i] + _ptWork[r][instanceNo + 2]
                _ptWork[r][instanceNo + 1] = 2.0
        elif _sw1 == 1:
            _ptWork[r][instanceNo + 3] = _ptWork[r - 1][instanceNo + 5] - _ptWork[r][instanceNo + 2]
            if _close[i] > _ptWork[r - 1][instanceNo + 5]:
                _ptWork[r][instanceNo + 5] = _close[i]
            if _close[i] < _ptWork[r - 1][instanceNo + 3]:
                _ptWork[r][instanceNo + 6] = _close[i]
                _ptWork[r][instanceNo + 4] = _close[i] + _ptWork[r][instanceNo + 2]
                _ptWork[r][instanceNo + 1] = 2.0
        elif _sw1 == 2:
            _ptWork[r][instanceNo + 4] = _ptWork[r - 1][instanceNo + 6] + _ptWork[r][instanceNo + 2]
            if _close[i] < _ptWork[r - 1][instanceNo + 6]:
                _ptWork[r][instanceNo + 6] = _close[i]
            if _close[i] > _ptWork[r - 1][instanceNo + 4]:
                _ptWork[r][instanceNo + 5] = _close[i]
                _ptWork[r][instanceNo + 3] = _close[i] - _ptWork[r][instanceNo + 2]
                _ptWork[r][instanceNo + 1] = 1.0
    return _ptWork[r][instanceNo + 1]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PrecisionTrend(_MQL5Indicator):
    name = 'Precision_Trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PtrPeriod': 14,  # Precision trend period
        'PtrSensitivity': 3.0,  # Precision trend sensitivity
    }

