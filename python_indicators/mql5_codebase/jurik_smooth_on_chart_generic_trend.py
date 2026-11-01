"""Jurik smooth on chart generic trend — converted from MQL5: MQL5 Indicators/Jurik smooth on chart generic trend/Jurik smooth on chart generic trend.mq5

Tripple Jurik on chart generic trend
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 8, 2: 8, 3: 8, 4: 8}, 'colors': {1: [11119017, 9639167, 32768], 2: [11119017, 9639167, 32768], 3: [11119017, 9639167, 32768], 4: [11119017, 9639167, 32768]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Smooth high', 2: 'Smooth close', 3: 'Smooth low', 4: 'Smooth generic'}, 'levels': [], 'description': ['Tripple Jurik on chart generic trend'], 'name': 'Jurik smooth on chart generic trend', 'source': 'MQL5 Indicators/Jurik smooth on chart generic trend/Jurik smooth on chart generic trend.mq5', 'folder': 'Jurik smooth on chart generic trend', 'inputs': [{'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'double', 'default': 27.0, 'label': 'Smooth period', 'sinput': False}, {'mql': 'inpSmoothPhase', 'py': 'inpSmoothPhase', 'param': 'inpSmoothPhase', 'type': 'double', 'default': 0.0, 'label': 'Smooth phase', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpSmoothPeriod = _input('inpSmoothPeriod', 27.0)  # Smooth period
inpSmoothPhase = _input('inpSmoothPhase', 0.0)  # Smooth phase
valu = Arr(0, 0.0)
valuc = Arr(0, 0.0)
valc = Arr(0, 0.0)
valcc = Arr(0, 0.0)
vald = Arr(0, 0.0)
valdc = Arr(0, 0.0)
valg = Arr(0, 0.0)
valgc = Arr(0, 0.0)
workSmooth = Arr(11, 0.0, dyn=False, dims=(40,))

def OnInit():
    SetIndexBuffer(0, valu, INDICATOR_DATA)
    SetIndexBuffer(1, valuc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, valc, INDICATOR_DATA)
    SetIndexBuffer(3, valcc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, vald, INDICATOR_DATA)
    SetIndexBuffer(5, valdc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, valg, INDICATOR_DATA)
    SetIndexBuffer(7, valgc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Triple Jurik OCGT (' + _str(inpSmoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        valu[i] = iSmooth(high[i], inpSmoothPeriod, inpSmoothPhase, i, 0)
        valc[i] = iSmooth(close[i], inpSmoothPeriod, inpSmoothPhase, i, 1)
        vald[i] = iSmooth(low[i], inpSmoothPeriod, inpSmoothPhase, i, 2)
        valg[i] = iSmooth((high[i] + low[i] + close[i]) / 3.0, inpSmoothPeriod, inpSmoothPhase, i, 3)
        valuc[i] = ((2 if (valu[i] > valu[i - 1]) else 1 if (valu[i] < valu[i - 1]) else valuc[i - 1]) if (i > 0) else 0)
        valcc[i] = ((2 if (valc[i] > valc[i - 1]) else 1 if (valc[i] < valc[i - 1]) else valcc[i - 1]) if (i > 0) else 0)
        valdc[i] = ((2 if (vald[i] > vald[i - 1]) else 1 if (vald[i] < vald[i - 1]) else valdc[i - 1]) if (i > 0) else 0)
        valgc[i] = (2 if ((valuc[i] == 2 and valcc[i] == 2) and valdc[i] == 2) else 1 if ((valuc[i] == 1 and valcc[i] == 1) and valdc[i] == 1) else 0)
        i += 1
    return i

def iSmooth(price, length, phase, i, instance=0):
    _indP = _int(MathMod(i - 1, 11))
    _indC = _int(MathMod(i, 11))
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
    del2 = price - workSmooth[_indP][_inst + 6]
    _indF = _int(MathMod(i - MathMin(i, 10), 11))
    workSmooth[_indC][_inst + 7] = (MathAbs(del1) if (MathAbs(del1) > MathAbs(del2)) else MathAbs(del2) if (MathAbs(del1) < MathAbs(del2)) else 0)
    workSmooth[_indC][_inst + 8] = workSmooth[_indP][_inst + 8] + ((workSmooth[_indC][_inst + 7] - workSmooth[_indF][_inst + 7]) * 0.1)
    workSmooth[_indC][_inst + 9] = workSmooth[_indP][_inst + 9] + (_fdiv(2.0, MathMax(4.0 * length, 30) + 1.0) * (workSmooth[_indC][_inst + 8] - workSmooth[_indP][_inst + 9]))
    dVolty = (_fdiv(workSmooth[_indC][_inst + 7], workSmooth[_indC][_inst + 9]) if (workSmooth[_indC][_inst + 9] > 0) else 0)
    if dVolty > MathPow(len1, _fdiv(1.0, pow1)):
        dVolty = MathPow(len1, _fdiv(1.0, pow1))
    if dVolty < 1.0:
        dVolty = 1.0
    pow2 = MathPow(dVolty, pow1)
    len2 = MathSqrt(0.5 * (length - 1)) * len1
    Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
    if del1 > 0:
        workSmooth[_indC][_inst + 5] = price
    else:
        workSmooth[_indC][_inst + 5] = price - (Kv * del1)
    if del2 < 0:
        workSmooth[_indC][_inst + 6] = price
    else:
        workSmooth[_indC][_inst + 6] = price - (Kv * del2)
    corr = (MathMax(MathMin(phase, 100), -100) / 100.0) + 1.5
    beta = _fdiv(0.45 * (length - 1), (0.45 * (length - 1)) + 2)
    alpha = MathPow(beta, pow2)
    workSmooth[_indC][_inst + 0] = price + (alpha * (workSmooth[_indP][_inst + 0] - price))
    workSmooth[_indC][_inst + 1] = ((price - workSmooth[_indC][_inst + 0]) * (1 - beta)) + (beta * workSmooth[_indP][_inst + 1])
    workSmooth[_indC][_inst + 2] = workSmooth[_indC][_inst + 0] + (corr * workSmooth[_indC][_inst + 1])
    workSmooth[_indC][_inst + 3] = ((workSmooth[_indC][_inst + 2] - workSmooth[_indP][_inst + 4]) * MathPow(1 - alpha, 2)) + (MathPow(alpha, 2) * workSmooth[_indP][_inst + 3])
    workSmooth[_indC][_inst + 4] = workSmooth[_indP][_inst + 4] + workSmooth[_indC][_inst + 3]
    return workSmooth[_indC][_inst + 4]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JurikSmoothOnChartGenericTrend(_MQL5Indicator):
    name = 'Jurik smooth on chart generic trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpSmoothPeriod': 27.0,  # Smooth period
        'inpSmoothPhase': 0.0,  # Smooth phase
    }

