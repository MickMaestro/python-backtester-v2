"""Self Advance Decline line (fl) — converted from MQL5: MQL5 Indicators/Self Advance Decline line - with floating levels/Self Advance Decline line (fl).mq5

Self Advance Decline line ...
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [8421504], 2: [8421504], 3: [8421504], 4: [11119017, 7451452, 17919]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Upper level', 2: 'Middle level', 3: 'Lower level', 4: 'Self Advance Decline line'}, 'levels': [], 'description': ['Self Advance Decline line ...'], 'name': 'Self Advance Decline line (fl)', 'source': 'MQL5 Indicators/Self Advance Decline line - with floating levels/Self Advance Decline line (fl).mq5', 'folder': 'Self Advance Decline line - with floating levels', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 25, 'label': 'Period', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up %', 'sinput': False}, {'mql': 'inpFlLevelDn', 'py': 'inpFlLevelDn', 'param': 'inpFlLevelDn', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down %', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 1, 'label': 'Color changing mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorChangeOn
cchange_onSlope = 0
cchange_onLevels = 1
cchange_onZero = 2
_enum('enColorChangeOn', {0: 'cchange_onSlope', 1: 'cchange_onLevels', 2: 'cchange_onZero'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 25)  # Period
inpFlPeriod = _input('inpFlPeriod', 25)  # Floating levels period
inpFlLevelUp = _input('inpFlLevelUp', 90.0)  # Floating levels up %
inpFlLevelDn = _input('inpFlLevelDn', 10.0)  # Floating levels down %
inpColorChange = _input('inpColorChange', cchange_onLevels)  # Color changing mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
sum_ = Arr(0, 0.0)
state = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
levm = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, levu, INDICATOR_DATA)
    SetIndexBuffer(1, levm, INDICATOR_DATA)
    SetIndexBuffer(2, levd, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, sum_, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, state, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Self Advance Decline line (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        state[i] = (1 if (close[i] > open[i]) else -1 if (close[i] < open[i]) else 0)
        if i > inpPeriod:
            sum_[i] = sum_[i - 1] + state[i] - state[i - inpPeriod]
        else:
            sum_[i] = state[i]
            k = 1
            while k < inpPeriod and i >= k:
                sum_[i] += state[i - k]
                k += 1
        val[i] = ((val[i - 1] + sum_[i]) if (i > 0) else sum_[i])
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpFlPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = val[ArrayMaximum(val, start, inpFlPeriod - 1)]
            _s_OnCalculate_prev_min = val[ArrayMinimum(val, start, inpFlPeriod - 1)]
        max_ = (val[i] if (val[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (val[i] if (val[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        range_ = (max_ - min_) / 100.0
        levu[i] = min_ + (inpFlLevelUp * range_)
        levd[i] = min_ + (inpFlLevelDn * range_)
        levm[i] = (levu[i] + levd[i]) / 2
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SelfAdvanceDeclineLineFl(_MQL5Indicator):
    name = 'Self Advance Decline line (fl)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 25,  # Period
        'inpFlPeriod': 25,  # Floating levels period
        'inpFlLevelUp': 90.0,  # Floating levels up %
        'inpFlLevelDn': 10.0,  # Floating levels down %
        'inpColorChange': _Choice({0: 'Change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross'}, default=1),  # Color changing mode
    }

