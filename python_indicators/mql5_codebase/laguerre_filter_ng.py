"""Laguerre filter - ng — converted from MQL5: MQL5 Indicators/Laguerre filter - no gamma/Laguerre filter - ng.mq5

Laguerre filter - no gamma
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 3937500]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Laguerre filter'}, 'levels': [], 'description': ['Laguerre filter - no gamma'], 'name': 'Laguerre filter - ng', 'source': 'MQL5 Indicators/Laguerre filter - no gamma/Laguerre filter - ng.mq5', 'folder': 'Laguerre filter - no gamma', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 14.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14.0)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workLagFil = Arr(6, 0.0, dyn=False, dims=(4,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Laguerre filter -ng (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iLaGuerreFil(getPrice(inpPrice, open, close, high, low, i), inpPeriod, i)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iLaGuerreFil(price, period, i, instance=0):
    _indC = _imod(i, 6)
    _inst = instance * 4
    if i > 0 and period > 1:
        _indP = _imod(i - 1, 6)
        _gamma = 1.0 - _fdiv(10.0, period + 9.0)
        workLagFil[_indC][_inst] = price + (_gamma * (workLagFil[_indP][_inst] - price))
        workLagFil[_indC][_inst + 1] = workLagFil[_indP][_inst] + (_gamma * (workLagFil[_indP][_inst + 1] - workLagFil[_indC][_inst]))
        workLagFil[_indC][_inst + 2] = workLagFil[_indP][_inst + 1] + (_gamma * (workLagFil[_indP][_inst + 2] - workLagFil[_indC][_inst + 1]))
        workLagFil[_indC][_inst + 3] = workLagFil[_indP][_inst + 2] + (_gamma * (workLagFil[_indP][_inst + 3] - workLagFil[_indC][_inst + 2]))
    else:
        for k in range(0, 4):
            workLagFil[_indC][_inst + k] = price
    return (workLagFil[_indC][_inst] + (2.0 * workLagFil[_indC][_inst + 1]) + (2.0 * workLagFil[_indC][_inst + 2]) + workLagFil[_indC][_inst + 3]) / 6.0

def getPrice(tprice, open, close, high, low, i):
    if i >= 0:
        _sw1 = tprice
        if _sw1 == PRICE_CLOSE:
            return close[i]
        elif _sw1 == PRICE_OPEN:
            return open[i]
        elif _sw1 == PRICE_HIGH:
            return high[i]
        elif _sw1 == PRICE_LOW:
            return low[i]
        elif _sw1 == PRICE_MEDIAN:
            return (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            return (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LaguerreFilterNg(_MQL5Indicator):
    name = 'Laguerre filter - ng'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14.0,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

