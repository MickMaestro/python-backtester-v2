"""Correlation trend indicator — converted from MQL5: MQL5 Indicators/Correlation trend indicator/Correlation trend indicator.mq5

Copyright: copyright© mladen 2020; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'copyright© mladen 2020', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [12632256], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Short', 2: 'Long'}, 'levels': [], 'description': [], 'name': 'Correlation trend indicator', 'source': 'MQL5 Indicators/Correlation trend indicator/Correlation trend indicator.mq5', 'folder': 'Correlation trend indicator', 'inputs': [{'mql': 'inpPeriodShort', 'py': 'inpPeriodShort', 'param': 'inpPeriodShort', 'type': 'int', 'default': 20, 'label': 'Short period', 'sinput': False}, {'mql': 'inpPeriodLong', 'py': 'inpPeriodLong', 'param': 'inpPeriodLong', 'type': 'int', 'default': 40, 'label': 'Long period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriodShort = _input('inpPeriodShort', 20)  # Short period
inpPeriodLong = _input('inpPeriodLong', 40)  # Long period
vals = Arr(0, 0.0)
vall = Arr(0, 0.0)
_longPeriod = 0
_shortPeriod = 0

def OnInit():
    global _longPeriod, _shortPeriod
    SetIndexBuffer(0, vals, INDICATOR_DATA)
    SetIndexBuffer(1, vall, INDICATOR_DATA)
    _longPeriod = MathMax(inpPeriodShort, inpPeriodLong)
    _shortPeriod = MathMin(inpPeriodShort, inpPeriodLong)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Correlation trend (%i,%i)', _shortPeriod, _longPeriod))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if limit < 0:
        limit = 0
    for i in range(limit, rates_total):
        SumSx = 0.0
        SumLx = 0.0
        SumSy = 0.0
        SumLy = 0.0
        SumSxx = 0.0
        SumLxx = 0.0
        SumSxy = 0.0
        SumLxy = 0.0
        SumSyy = 0.0
        SumLyy = 0.0
        k = 0
        while k < _longPeriod and i >= k:
            y = -k
            if k < _shortPeriod:
                SumSx += close[i - k]
                SumSxx += close[i - k] * close[i - k]
                SumSxy += close[i - k] * y
                SumSy += y
                SumSyy += y * y
            SumLx += close[i - k]
            SumLxx += close[i - k] * close[i - k]
            SumLxy += close[i - k] * y
            SumLy += y
            SumLyy += y * y
            k += 1
        _ts1 = (_shortPeriod * SumSxx) - (SumSx * SumSx)
        _ts2 = (_shortPeriod * SumSyy) - (SumSy * SumSy)
        _tl1 = (_longPeriod * SumLxx) - (SumLx * SumLx)
        _tl2 = (_longPeriod * SumLyy) - (SumLy * SumLy)
        vals[i] = (_fdiv((_shortPeriod * SumSxy) - (SumSx * SumSy), MathSqrt(_ts1 * _ts2)) if (_ts1 > 0 and _ts2 > 0) else 0)
        vall[i] = (_fdiv((_longPeriod * SumLxy) - (SumLx * SumLy), MathSqrt(_tl1 * _tl2)) if (_tl1 > 0 and _tl2 > 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrelationTrendIndicator(_MQL5Indicator):
    name = 'Correlation trend indicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriodShort': 20,  # Short period
        'inpPeriodLong': 40,  # Long period
    }

