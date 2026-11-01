"""Stochastic RVI lvl — converted from MQL5: MQL5 Indicators/Stochastic RVI - levels/Stochastic RVI lvl.mq5

Stochastic RVI - levels
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [11119017], 2: [11119017], 3: [8421504, 7451452, 17919]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'Level up', 2: 'Level down', 3: 'Stochastic RVI'}, 'levels': [], 'description': ['Stochastic RVI - levels'], 'name': 'Stochastic RVI lvl', 'source': 'MQL5 Indicators/Stochastic RVI - levels/Stochastic RVI lvl.mq5', 'folder': 'Stochastic RVI - levels', 'inputs': [{'mql': 'inpRviPeriod', 'py': 'inpRviPeriod', 'param': 'inpRviPeriod', 'type': 'int', 'default': 32, 'label': 'RVI period', 'sinput': False}, {'mql': 'inpLevelPeriod', 'py': 'inpLevelPeriod', 'param': 'inpLevelPeriod', 'type': 'double', 'default': 10.0, 'label': 'Levels period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRviPeriod = _input('inpRviPeriod', 32)  # RVI period
inpLevelPeriod = _input('inpLevelPeriod', 10.0)  # Levels period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
lup = Arr(0, 0.0)
ldn = Arr(0, 0.0)
rvi = Arr(0, 0.0)
work = Arr(0, 0.0)
rvi_num = Arr(0, 0.0)
rvi_denom = Arr(0, 0.0)
rvi_nums = Arr(0, 0.0)
rvi_denoms = Arr(0, 0.0)
ª_lvlPeriod = 0.0
ª_alphal = 0.0

def OnInit():
    global ª_alphal, ª_lvlPeriod
    SetIndexBuffer(0, lup, INDICATOR_DATA)
    SetIndexBuffer(1, ldn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, rvi, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, work, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, rvi_num, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, rvi_denom, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, rvi_nums, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, rvi_denoms, INDICATOR_CALCULATIONS)
    ª_lvlPeriod = (inpLevelPeriod if (inpLevelPeriod > 1) else 1)
    ª_alphal = _fdiv(2.0, 1.0 + ª_lvlPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic RVI (' + _str(inpRviPeriod) + ',' + _str(ª_lvlPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        rvi_num[i] = ((close[i] - open[i] + (2.0 * (close[i - 1] - open[i - 1])) + (2.0 * (close[i - 2] - open[i - 2])) + close[i - 3] - open[i - 3]) if (i > 2) else 0)
        rvi_denom[i] = ((high[i] - low[i] + (2.0 * (high[i - 1] - low[i - 1])) + (2.0 * (high[i - 2] - low[i - 2])) + high[i - 3] - low[i - 3]) if (i > 2) else 0)
        if i > (inpRviPeriod + 3):
            rvi_nums[i] = rvi_nums[i - 1] + rvi_num[i] - rvi_num[i - inpRviPeriod]
            rvi_denoms[i] = rvi_denoms[i - 1] + rvi_denom[i] - rvi_denom[i - inpRviPeriod]
        else:
            rvi_nums[i] = rvi_num[i]
            rvi_denoms[i] = rvi_denom[i]
            k = 1
            while k < inpRviPeriod and i >= k:
                rvi_nums[i] += rvi_num[i - k]
                rvi_denoms[i] += rvi_denom[i - k]
                k += 1
        rvi[i] = (_fdiv(rvi_nums[i], rvi_denoms[i]) if (rvi_denoms[i] != 0.0) else rvi_nums[i])
        _start = ((i - inpRviPeriod + 1) if (i > inpRviPeriod) else 0)
        _lo = rvi[ArrayMinimum(rvi, _start, inpRviPeriod)]
        _hi = rvi[ArrayMaximum(rvi, _start, inpRviPeriod)]
        work[i] = (_fdiv(rvi[i] - _lo, _hi - _lo) if (_hi != _lo) else 0)
        val[i] = ((((4.0 * work[i]) + (3.0 * work[i - 1]) + (2.0 * work[i - 2]) + work[i - 3]) / 10.0) if (i > 2) else 0)
        lup[i] = ((lup[i - 1] if (val[i] < ldn[i - 1]) else (lup[i - 1] + (ª_alphal * (val[i] - lup[i - 1])))) if (i > 0) else val[i])
        ldn[i] = ((ldn[i - 1] if (val[i] > lup[i - 1]) else (ldn[i - 1] + (ª_alphal * (val[i] - ldn[i - 1])))) if (i > 0) else val[i])
        valc[i] = (1 if (val[i] > lup[i]) else 2 if (val[i] < ldn[i]) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticRVILvl(_MQL5Indicator):
    name = 'Stochastic RVI lvl'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRviPeriod': 32,  # RVI period
        'inpLevelPeriod': 10.0,  # Levels period
    }

