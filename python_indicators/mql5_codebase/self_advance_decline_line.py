"""Self Advance Decline line — converted from MQL5: MQL5 Indicators/Self advance decline line/Self Advance Decline line.mq5

Self Advance Decline line ...
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Self AD line '}, 'levels': [], 'description': ['Self Advance Decline line ...'], 'name': 'Self Advance Decline line', 'source': 'MQL5 Indicators/Self advance decline line/Self Advance Decline line.mq5', 'folder': 'Self advance decline line', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 25, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 25)  # Period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
sum_ = Arr(0, 0.0)
state = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, sum_, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, state, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Self Advance Decline line (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
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
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SelfAdvanceDeclineLine(_MQL5Indicator):
    name = 'Self Advance Decline line'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 25,  # Period
    }

