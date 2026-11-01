"""Dsl - CMO — converted from MQL5: MQL5 Indicators/Dsl - CMO/Dsl - CMO.mq5

Discontinued signal lines version of Chandes momentum oscillator
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 8}, 'colors': {1: [14474460], 2: [11119017, 6333684, 16760576]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'CMO no trend zone', 2: 'CMO'}, 'levels': [], 'description': ['Discontinued signal lines version of Chandes momentum oscillator'], 'name': 'Dsl - CMO', 'source': 'MQL5 Indicators/Dsl - CMO/Dsl - CMO.mq5', 'folder': 'Dsl - CMO', 'inputs': [{'mql': 'inpCmoPeriod', 'py': 'inpCmoPeriod', 'param': 'inpCmoPeriod', 'type': 'int', 'default': 20, 'label': 'CMO period', 'sinput': False}, {'mql': 'inpCmoSignalPeriod', 'py': 'inpCmoSignalPeriod', 'param': 'inpCmoSignalPeriod', 'type': 'int', 'default': 9, 'label': 'CMO signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpCmoPeriod = _input('inpCmoPeriod', 20)  # CMO period
inpCmoSignalPeriod = _input('inpCmoSignalPeriod', 9)  # CMO signal period
cmo = Arr(0, 0.0)
cmoc = Arr(0, 0.0)
dslup = Arr(0, 0.0)
dsldn = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, dslup, INDICATOR_DATA)
    SetIndexBuffer(1, dsldn, INDICATOR_DATA)
    SetIndexBuffer(2, cmo, INDICATOR_DATA)
    SetIndexBuffer(3, cmoc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dsl Chandes momentum oscillator (' + _str(inpCmoPeriod) + ',' + _str(inpCmoSignalPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    _alpha = 2.0 / (1 + inpCmoSignalPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        SumUp = 0.0
        SumDn = 0.0
        k = 0
        while k < inpCmoPeriod and (i - k - 1) >= 0:
            diff = close[i - k] - close[i - k - 1]
            SumUp += (diff if (diff > 0) else 0)
            SumDn += ((-diff) if (diff < 0) else 0)
            k += 1
        cmo[i] = (_fdiv(100 * (SumUp - SumDn), SumUp + SumDn) if ((SumUp + SumDn) != 0) else 0)
        dslup[i] = (((dslup[i - 1] + (_alpha * (cmo[i] - dslup[i - 1]))) if (cmo[i] > 0) else dslup[i - 1]) if (i > 0) else 0)
        dsldn[i] = (((dsldn[i - 1] + (_alpha * (cmo[i] - dsldn[i - 1]))) if (cmo[i] < 0) else dsldn[i - 1]) if (i > 0) else 0)
        cmoc[i] = (2 if (cmo[i] > dslup[i]) else 1 if (cmo[i] < dsldn[i]) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DslCMO(_MQL5Indicator):
    name = 'Dsl - CMO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCmoPeriod': 20,  # CMO period
        'inpCmoSignalPeriod': 9,  # CMO signal period
    }

