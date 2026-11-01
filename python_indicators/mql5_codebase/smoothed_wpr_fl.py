"""Smoothed WPR (fl) — converted from MQL5: MQL5 Indicators/Smoothed WPR with floating levels/Smoothed WPR (fl).mq5

Smoothed WPR with floating levels
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [8421504], 2: [8421504], 3: [8421504], 4: [11119017, 7451452, 17919]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Upper level', 2: 'Middle level', 3: 'Lower level', 4: 'WPR'}, 'levels': [], 'description': ['Smoothed WPR with floating levels'], 'name': 'Smoothed WPR (fl)', 'source': 'MQL5 Indicators/Smoothed WPR with floating levels/Smoothed WPR (fl).mq5', 'folder': 'Smoothed WPR with floating levels', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 0, 'label': 'Smoothing period (< 1 for same as WPR period)', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up %', 'sinput': False}, {'mql': 'inpFlLevelDn', 'py': 'inpFlLevelDn', 'param': 'inpFlLevelDn', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down %', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 1, 'label': 'Color change type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorChangeOn
cchange_onSlope = 0
cchange_onLevels = 1
cchange_onZero = 2
_enum('enColorChangeOn', {0: 'cchange_onSlope', 1: 'cchange_onLevels', 2: 'cchange_onZero'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpSmoothPeriod = _input('inpSmoothPeriod', 0)  # Smoothing period (< 1 for same as WPR period)
inpFlPeriod = _input('inpFlPeriod', 25)  # Floating levels period
inpFlLevelUp = _input('inpFlLevelUp', 90.0)  # Floating levels up %
inpFlLevelDn = _input('inpFlLevelDn', 10.0)  # Floating levels down %
inpColorChange = _input('inpColorChange', cchange_onLevels)  # Color change type
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
levm = Arr(0, 0.0)
smth = Arr(0, 0.0)
smtl = Arr(0, 0.0)
smtc = Arr(0, 0.0)
_alpha = 0.0

def OnInit():
    global _alpha
    SetIndexBuffer(0, levu, INDICATOR_DATA)
    SetIndexBuffer(1, levm, INDICATOR_DATA)
    SetIndexBuffer(2, levd, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, smth, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, smtl, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, smtc, INDICATOR_CALCULATIONS)
    _alpha = _fdiv(2.0, 1.0 + (inpSmoothPeriod if (inpSmoothPeriod > 0) else inpPeriod))
    IndicatorSetString(INDICATOR_SHORTNAME, 'WPR (' + _str(inpPeriod) + ',' + _str(inpSmoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_maxv, _s_OnCalculate_prev_min, _s_OnCalculate_prev_minv
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
            start = i - inpPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = smth[ArrayMaximum(smth, start, inpPeriod - 1)]
            _s_OnCalculate_prev_min = smtl[ArrayMinimum(smtl, start, inpPeriod - 1)]
        max_ = (smth[i] if (smth[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (smtl[i] if (smtl[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        val[i] = (_fdiv((-(max_ - smtc[i])) * 100.0, max_ - min_) if (max_ != min_) else 0)
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_maxv = val[ArrayMaximum(val, start, inpPeriod - 1)]
            _s_OnCalculate_prev_minv = val[ArrayMinimum(val, start, inpPeriod - 1)]
        max_ = (val[i] if (val[i] > _s_OnCalculate_prev_maxv) else _s_OnCalculate_prev_maxv)
        min_ = (val[i] if (val[i] < _s_OnCalculate_prev_minv) else _s_OnCalculate_prev_minv)
        range_ = (max_ - min_) / 100.0
        levu[i] = min_ + (inpFlLevelUp * range_)
        levd[i] = min_ + (inpFlLevelDn * range_)
        levm[i] = min_ + (50.0 * range_)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        _sw1 = inpColorChange
        if _sw1 == cchange_onLevels:
            valc[i] = (1 if (val[i] > levu[i]) else 2 if (val[i] < levd[i]) else 0)
        elif _sw1 == cchange_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw1 == cchange_onZero:
            valc[i] = (1 if (val[i] > levm[i]) else 2 if (val[i] < levm[i]) else 0)
        i += 1
    return i

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0
_s_OnCalculate_prev_maxv = 0.0
_s_OnCalculate_prev_minv = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmoothedWPRFl(_MQL5Indicator):
    name = 'Smoothed WPR (fl)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 14,  # Period
        'inpSmoothPeriod': 0,  # Smoothing period (< 1 for same as WPR period)
        'inpFlPeriod': 25,  # Floating levels period
        'inpFlLevelUp': 90.0,  # Floating levels up %
        'inpFlLevelDn': 10.0,  # Floating levels down %
        'inpColorChange': _Choice({0: 'Change color on slope change', 1: 'Change color on levels crossing', 2: 'Change color on zero crossing'}, default=1),  # Color change type
    }

