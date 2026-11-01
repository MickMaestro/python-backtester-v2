"""Smoothed WPR — converted from MQL5: MQL5 Indicators/Smoothed WPR/Smoothed WPR.mq5

Smoothed WPR
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'WPR'}, 'levels': [], 'description': ['Smoothed WPR'], 'name': 'Smoothed WPR', 'source': 'MQL5 Indicators/Smoothed WPR/Smoothed WPR.mq5', 'folder': 'Smoothed WPR', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 0, 'label': 'Smoothing period (< 1 for same as WPR period)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpSmoothPeriod = _input('inpSmoothPeriod', 0)  # Smoothing period (< 1 for same as WPR period)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
smth = Arr(0, 0.0)
smtl = Arr(0, 0.0)
smtc = Arr(0, 0.0)
_alpha = 0.0

def OnInit():
    global _alpha
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, smth, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, smtl, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, smtc, INDICATOR_CALCULATIONS)
    _alpha = _fdiv(2.0, 1.0 + (inpSmoothPeriod if (inpSmoothPeriod > 0) else inpPeriod))
    IndicatorSetString(INDICATOR_SHORTNAME, 'WPR (' + _str(inpPeriod) + ',' + _str(inpSmoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if i > 0:
            smth[i] = smth[i - 1] + (_alpha * (high[i] - smth[i - 1]))
            smtl[i] = smtl[i - 1] + (_alpha * (low[i] - smtl[i - 1]))
            smtc[i] = smtc[i - 1] + (_alpha * (close[i] - smtc[i - 1]))
        else:
            smth[i] = high[i]
            smtl[i] = low[i]
            smtc[i] = close[i]
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = smth[ArrayMaximum(smth, start, inpPeriod - 1)]
            _s_OnCalculate_prev_min = smtl[ArrayMinimum(smtl, start, inpPeriod - 1)]
        max_ = (smth[i] if (smth[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (smtl[i] if (smtl[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        val[i] = (_fdiv((-(max_ - smtc[i])) * 100.0, max_ - min_) if (max_ != min_) else 0)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmoothedWPR(_MQL5Indicator):
    name = 'Smoothed WPR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpSmoothPeriod': 0,  # Smoothing period (< 1 for same as WPR period)
    }

