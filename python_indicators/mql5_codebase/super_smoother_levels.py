"""Super smoother levels — converted from MQL5: MQL5 Indicators/Super smoother levels/Super smoother levels.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [8421504], 2: [3329330], 3: [42495], 4: [12632256, 3329330, 42495]}, 'widths': {1: 6, 4: 2}, 'styles': {2: 2, 3: 2}, 'labels': {1: 'shadow', 2: 'up level', 3: 'down level', 4: 'Super smoother'}, 'levels': [], 'description': [], 'name': 'Super smoother levels', 'source': 'MQL5 Indicators/Super smoother levels/Super smoother levels.mq5', 'folder': 'Super smoother levels', 'inputs': [{'mql': 'inpSsmPeriod', 'py': 'inpSsmPeriod', 'param': 'inpSsmPeriod', 'type': 'int', 'default': 14, 'label': 'Super smoother period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpSsmPeriod = _input('inpSsmPeriod', 14)  # Super smoother period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
vals = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
workSsm = Arr(10, 0.0, dyn=False, dims=(6,))
workSsmCoeffs = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, vals, INDICATOR_DATA)
    SetIndexBuffer(1, levelUp, INDICATOR_DATA)
    SetIndexBuffer(2, levelDn, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Super smoother levels (' + _str(inpSsmPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iSuperSmoother(close[i], inpSsmPeriod, i, False, 0)
        levelUp[i] = iSuperSmoother(val[i], inpSsmPeriod, i, ((not (val[i] > levelDn[i - 1])) if (i > 0) else False), 1)
        levelDn[i] = iSuperSmoother(val[i], inpSsmPeriod, i, ((not (val[i] < levelUp[i - 1])) if (i > 0) else False), 2)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        vals[i] = val[i]
        i += 1
    return i

def iSuperSmoother(price, period, i, copy=False, instance=0):
    _indP = _imod(i - 1, 10)
    _indC = _imod(i, 10)
    _inst = instance * 2
    if ((not copy) and i > 1) and period > 1:
        if ArrayRange(workSsmCoeffs, 0) < (instance + 1):
            ArrayResize(workSsmCoeffs, instance + 1)
            workSsmCoeffs[instance][0] = -99.0
        if workSsmCoeffs[instance][0] != period:
            a1 = MathExp(_fdiv(-1.414 * M_PI, period))
            b1 = 2.0 * a1 * MathCos(_fdiv(1.414 * M_PI, period))
            workSsmCoeffs[instance][2] = b1
            workSsmCoeffs[instance][3] = (-a1) * a1
            workSsmCoeffs[instance][1] = 1.0 - workSsmCoeffs[instance][2] - workSsmCoeffs[instance][3]
            workSsmCoeffs[instance][0] = period
        _indO = _imod(i - 2, 10)
        workSsm[_indC][_inst + 0] = price
        workSsm[_indC][_inst + 1] = ((workSsmCoeffs[instance][1] * (price + workSsm[_indP][_inst + 0])) / 2.0) + (workSsmCoeffs[instance][2] * workSsm[_indP][_inst + 1]) + (workSsmCoeffs[instance][3] * workSsm[_indO][_inst + 1])
    else:
        for k in range(0, 2):
            workSsm[_indC][_inst + k] = (workSsm[_indP][_inst + k] if (i > 0) else price)
    return workSsm[_indC][_inst + 1]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SuperSmootherLevels(_MQL5Indicator):
    name = 'Super smoother levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpSsmPeriod': 14,  # Super smoother period
    }

