"""Fast Ema Hull — converted from MQL5: MQL5 Indicators/Fast ema Hull average/Fast Ema Hull.mq5

Fast EMA Hull
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 32768]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Fast Ema hull'}, 'levels': [], 'description': ['Fast EMA Hull'], 'name': 'Fast Ema Hull', 'source': 'MQL5 Indicators/Fast ema Hull average/Fast Ema Hull.mq5', 'folder': 'Fast ema Hull average', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 27.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 27.0)  # Period
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workHulle = Arr(5, 0.0, dyn=False, dims=(3,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fast Ema Hull (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        val[i] = iHulle(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, i)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

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

def getPrice(tprice, open, close, high, low, i, _bars):
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


class FastEmaHull(_MQL5Indicator):
    name = 'Fast Ema Hull'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 27.0,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

