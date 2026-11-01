"""Dsl - CMO bars — converted from MQL5: MQL5 Indicators/Dsl - CMO bars/Dsl - CMO bars.mq5

Discontinued signal lines version of Chandes momentum oscillator
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 16}, 'colors': {1: [11119017, 6333684, 16760576]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Dsl CMO trend bars'}, 'levels': [], 'description': ['Discontinued signal lines version of Chandes momentum oscillator'], 'name': 'Dsl - CMO bars', 'source': 'MQL5 Indicators/Dsl - CMO bars/Dsl - CMO bars.mq5', 'folder': 'Dsl - CMO bars', 'inputs': [{'mql': 'inpCmoPeriod', 'py': 'inpCmoPeriod', 'param': 'inpCmoPeriod', 'type': 'int', 'default': 20, 'label': 'CMO period', 'sinput': False}, {'mql': 'inpCmoSignalPeriod', 'py': 'inpCmoSignalPeriod', 'param': 'inpCmoSignalPeriod', 'type': 'int', 'default': 9, 'label': 'CMO signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpCmoPeriod = _input('inpCmoPeriod', 20)  # CMO period
inpCmoSignalPeriod = _input('inpCmoSignalPeriod', 9)  # CMO signal period
cmo = Arr(0, 0.0)
cmoc = Arr(0, 0.0)
dslup = Arr(0, 0.0)
dsldn = Arr(0, 0.0)
baro = Arr(0, 0.0)
barh = Arr(0, 0.0)
barl = Arr(0, 0.0)
barc = Arr(0, 0.0)
barcl = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, baro, INDICATOR_DATA)
    SetIndexBuffer(1, barh, INDICATOR_DATA)
    SetIndexBuffer(2, barl, INDICATOR_DATA)
    SetIndexBuffer(3, barc, INDICATOR_DATA)
    SetIndexBuffer(4, barcl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, dslup, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, dsldn, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, cmo, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, cmoc, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dsl Chandes momentum oscillator (' + _str(inpCmoPeriod) + ',' + _str(inpCmoSignalPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prevDisplayType
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    currDisplayType = _int(ChartGetInteger(0, CHART_MODE))
    if currDisplayType != _s_OnCalculate_prevDisplayType:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, (DRAW_COLOR_CANDLES if (currDisplayType == CHART_CANDLES) else DRAW_COLOR_BARS))
        _s_OnCalculate_prevDisplayType = currDisplayType
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
        barh[i] = high[i]
        barl[i] = low[i]
        barc[i] = close[i]
        baro[i] = open[i]
        barcl[i] = cmoc[i]
        i += 1
    return i

# ---- static local variables
_s_OnCalculate_prevDisplayType = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DslCMOBars(_MQL5Indicator):
    name = 'Dsl - CMO bars'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCmoPeriod': 20,  # CMO period
        'inpCmoSignalPeriod': 9,  # CMO signal period
    }

