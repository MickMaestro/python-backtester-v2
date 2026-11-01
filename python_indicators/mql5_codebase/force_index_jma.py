"""Force index - JMA — converted from MQL5: MQL5 Indicators/Force index - JMA/Force index - JMA.mq5

Force index - JMA
Copyright: © mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [16760576, 13353215], 2: [11119017, 16748574, 9662683]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'filling', 2: 'Force index'}, 'levels': [], 'description': ['Force index - JMA'], 'name': 'Force index - JMA', 'source': 'MQL5 Indicators/Force index - JMA/Force index - JMA.mq5', 'folder': 'Force index - JMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpPhase', 'py': 'inpPhase', 'param': 'inpPhase', 'type': 'double', 'default': 0.0, 'label': 'Smoothing phase', 'sinput': False}, {'mql': 'inpVolume', 'py': 'inpVolume', 'param': 'inpVolume', 'type': 'int', 'default': 0, 'label': 'Volume to use', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Smoothing period
inpPhase = _input('inpPhase', 0.0)  # Smoothing phase
inpVolume = _input('inpVolume', VOLUME_TICK)  # Volume to use
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
workSmooth = Arr(11, 0.0, dyn=False, dims=(10,))

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Force index (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _diff = (((tick_volume[i] if (inpVolume == VOLUME_TICK) else volume[i]) * (close[i] - close[i - 1])) if (i > 0) else 0)
        val[i] = iSmooth(_diff, inpPeriod, inpPhase, i)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        fillu[i] = val[i]
        filld[i] = 0.0
        i += 1
    return i

def iSmooth(price, length, phase, i, instance=0):
    _indP = _imod(i - 1, 11)
    _indC = _imod(i, 11)
    _inst = instance * 10
    if i == 0 or length <= 1:
        k = 0
        while k < 7:
            workSmooth[_indC][_inst + k] = price
            k += 1
        while k < 10:
            workSmooth[_indC][_inst + k] = 0.0
            k += 1
        return price
    len1 = MathMax(_fdiv(MathLog(MathSqrt(0.5 * (length - 1.0))), MathLog(2.0)) + 2.0, 0)
    pow1 = MathMax(len1 - 2.0, 0.5)
    del1 = price - workSmooth[_indP][_inst + 5]
    absDel1 = MathAbs(del1)
    del2 = price - workSmooth[_indP][_inst + 6]
    absDel2 = MathAbs(del2)
    _indF = _imod(i - MathMin(i, 10), 11)
    workSmooth[_indC][_inst + 7] = (absDel1 if (absDel1 > absDel2) else absDel2 if (absDel1 < absDel2) else 0)
    workSmooth[_indC][_inst + 8] = workSmooth[_indP][_inst + 8] + ((workSmooth[_indC][_inst + 7] - workSmooth[_indF][_inst + 7]) * 0.1)
    workSmooth[_indC][_inst + 9] = workSmooth[_indP][_inst + 9] + (_fdiv(2.0, MathMax(4.0 * length, 30) + 1.0) * (workSmooth[_indC][_inst + 8] - workSmooth[_indP][_inst + 9]))
    dVolty = (_fdiv(workSmooth[_indC][_inst + 7], workSmooth[_indC][_inst + 9]) if (workSmooth[_indC][_inst + 9] > 0) else 0)
    dVoltyTmp = MathPow(len1, _fdiv(1.0, pow1))
    if dVolty > dVoltyTmp:
        dVolty = dVoltyTmp
    if dVolty < 1.0:
        dVolty = 1.0
    pow2 = MathPow(dVolty, pow1)
    len2 = MathSqrt(0.5 * (length - 1)) * len1
    Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
    workSmooth[_indC][_inst + 5] = (price if (del1 > 0) else (price - (Kv * del1)))
    workSmooth[_indC][_inst + 6] = (price if (del2 < 0) else (price - (Kv * del2)))
    corr = (MathMax(MathMin(phase, 100), -100) / 100.0) + 1.5
    beta = _fdiv(0.45 * (length - 1), (0.45 * (length - 1)) + 2)
    alpha = MathPow(beta, pow2)
    workSmooth[_indC][_inst + 0] = price + (alpha * (workSmooth[_indP][_inst + 0] - price))
    workSmooth[_indC][_inst + 1] = ((price - workSmooth[_indC][_inst + 0]) * (1 - beta)) + (beta * workSmooth[_indP][_inst + 1])
    workSmooth[_indC][_inst + 2] = workSmooth[_indC][_inst + 0] + (corr * workSmooth[_indC][_inst + 1])
    workSmooth[_indC][_inst + 3] = ((workSmooth[_indC][_inst + 2] - workSmooth[_indP][_inst + 4]) * ((1 - alpha) * (1 - alpha))) + (alpha * alpha * workSmooth[_indP][_inst + 3])
    workSmooth[_indC][_inst + 4] = workSmooth[_indP][_inst + 4] + workSmooth[_indC][_inst + 3]
    return workSmooth[_indC][_inst + 4]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ForceIndexJMA(_MQL5Indicator):
    name = 'Force index - JMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Smoothing period
        'inpPhase': 0.0,  # Smoothing phase
        'inpVolume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume to use
    }

