"""Triple fast ema Hull — converted from MQL5: MQL5 Indicators/Triple fast ema Hull/Triple fast ema Hull.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 8, 2: 8, 3: 8}, 'colors': {1: [11119017, 9639167, 32768], 2: [11119017, 9639167, 32768], 3: [11119017, 9639167, 32768]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Fast ema Hull high', 2: 'Fast ema Hull close', 3: 'Fast ema Hull low'}, 'levels': [], 'description': [], 'name': 'Triple fast ema Hull', 'source': 'MQL5 Indicators/Triple fast ema Hull/Triple fast ema Hull.mq5', 'folder': 'Triple fast ema Hull', 'inputs': [{'mql': 'inpHullPeriod', 'py': 'inpHullPeriod', 'param': 'inpHullPeriod', 'type': 'double', 'default': 27.0, 'label': 'Fast ema Hull period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpHullPeriod = _input('inpHullPeriod', 27.0)  # Fast ema Hull period
hullu = Arr(0, 0.0)
hulluc = Arr(0, 0.0)
hullc = Arr(0, 0.0)
hullcc = Arr(0, 0.0)
hulld = Arr(0, 0.0)
hulldc = Arr(0, 0.0)
workHulle = Arr(5, 0.0, dyn=False, dims=(9,))

def OnInit():
    SetIndexBuffer(0, hullu, INDICATOR_DATA)
    SetIndexBuffer(1, hulluc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, hullc, INDICATOR_DATA)
    SetIndexBuffer(3, hullcc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, hulld, INDICATOR_DATA)
    SetIndexBuffer(5, hulldc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Triple fast ema Hull (' + _str(inpHullPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        hullu[i] = iHulle(high[i], inpHullPeriod, i, 0)
        hullc[i] = iHulle(close[i], inpHullPeriod, i, 1)
        hulld[i] = iHulle(low[i], inpHullPeriod, i, 2)
        hulluc[i] = ((2 if (hullu[i] > hullu[i - 1]) else 1 if (hullu[i] < hullu[i - 1]) else hulluc[i - 1]) if (i > 0) else 0)
        hullcc[i] = ((2 if (hullc[i] > hullc[i - 1]) else 1 if (hullc[i] < hullc[i - 1]) else hullcc[i - 1]) if (i > 0) else 0)
        hulldc[i] = ((2 if (hulld[i] > hulld[i - 1]) else 1 if (hulld[i] < hulld[i - 1]) else hulldc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iHulle(price, period, i, instance=0):
    _indP = _imod(i - 1, 5)
    _indC = _imod(i, 5)
    _inst = instance * 3
    if i > 0 and period > 1:
        workHulle[_indC][_inst] = ((workHulle[_indP][_inst] + (_fdiv(2.0, 2.0 + (((period / 2.0) - 1.0) / 2.0)) * (price - workHulle[_indP][_inst]))) if (i > 0) else price)
        workHulle[_indC][_inst + 1] = ((workHulle[_indP][_inst + 1] + (_fdiv(2.0, 2.0 + ((period - 1.0) / 2.0)) * (price - workHulle[_indP][_inst + 1]))) if (i > 0) else price)
        workHulle[_indC][_inst + 2] = ((workHulle[_indP][_inst + 2] + (_fdiv(2.0, 2.0 + ((MathSqrt(period) - 1.0) / 2.0)) * ((2 * workHulle[_indC][_inst]) - workHulle[_indC][_inst + 1] - workHulle[_indP][_inst + 2]))) if (i > 0) else price)
    else:
        for k in range(0, 3):
            workHulle[_indC][k + _inst] = (workHulle[_indP][k + _inst] if (i > 0) else price)
    return workHulle[_indC][_inst + 2]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TripleFastEmaHull(_MQL5Indicator):
    name = 'Triple fast ema Hull'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpHullPeriod': 27.0,  # Fast ema Hull period
    }

