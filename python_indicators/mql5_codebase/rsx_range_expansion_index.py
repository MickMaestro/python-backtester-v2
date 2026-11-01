"""RSX range expansion index — converted from MQL5: MQL5 Indicators/RSX range expansion index/RSX range expansion index.mq5

RSX Range expansion index (REI)
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16760576, 8036607]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Range expansion index'}, 'levels': [], 'description': ['RSX Range expansion index (REI)'], 'name': 'RSX range expansion index', 'source': 'MQL5 Indicators/RSX range expansion index/RSX range expansion index.mq5', 'folder': 'RSX range expansion index', 'inputs': [{'mql': 'inpReiPeriod', 'py': 'inpReiPeriod', 'param': 'inpReiPeriod', 'type': 'int', 'default': 14, 'label': 'REI period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpReiPeriod = _input('inpReiPeriod', 14)  # REI period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workRsi = Arr(5, 0.0, dyn=False, dims=(26,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Range expansion index (REI) (' + _str(inpReiPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iRsx(high[i], inpReiPeriod, i, 0) + iRsx(low[i], inpReiPeriod, i, 1) - 100
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iRsx(price, period, i, instanceNo=0):
    _indP = _int(MathMod(i - 1, 5))
    _indC = _int(MathMod(i, 5))
    _inst = instanceNo * 13
    if i < period:
        for k in range(1, 13):
            workRsi[_indC][_inst + k] = 0.0
        return 50.0
    workRsi[_indC][_inst] = price
    Kg = _fdiv(3.0, 2.0 + period)
    Hg = 1.0 - Kg
    mom = workRsi[_indC][_inst] - workRsi[_indP][_inst]
    moa = MathAbs(mom)
    for k in range(0, 3):
        kk = _inst + (k * 2)
        workRsi[_indC][kk + 1] = (Kg * mom) + (Hg * workRsi[_indP][kk + 1])
        workRsi[_indC][kk + 2] = (Kg * workRsi[_indC][kk + 1]) + (Hg * workRsi[_indP][kk + 2])
        mom = (1.5 * workRsi[_indC][kk + 1]) - (0.5 * workRsi[_indC][kk + 2])
        workRsi[_indC][kk + 7] = (Kg * moa) + (Hg * workRsi[_indP][kk + 7])
        workRsi[_indC][kk + 8] = (Kg * workRsi[_indC][kk + 7]) + (Hg * workRsi[_indP][kk + 8])
        moa = (1.5 * workRsi[_indC][kk + 7]) - (0.5 * workRsi[_indC][kk + 8])
    return MathMax(MathMin((_fdiv(mom, MathMax(moa, DBL_MIN)) + 1.0) * 50.0, 100.0), 0.0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSXRangeExpansionIndex(_MQL5Indicator):
    name = 'RSX range expansion index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpReiPeriod': 14,  # REI period
    }

