"""Smoother momentum — converted from MQL5: MQL5 Indicators/Smoother momentum/Smoother momentum.mq5

Smoother momentum
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Smoother momentum'}, 'levels': [], 'description': ['Smoother momentum'], 'name': 'Smoother momentum', 'source': 'MQL5 Indicators/Smoother momentum/Smoother momentum.mq5', 'folder': 'Smoother momentum', 'inputs': [{'mql': 'inpMomPeriod', 'py': 'inpMomPeriod', 'param': 'inpMomPeriod', 'type': 'int', 'default': 20, 'label': 'Momentum period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpMomPeriod = _input('inpMomPeriod', 20)  # Momentum period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)
workSmom = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoother momentum (' + _str(inpMomPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iSmoothMomentum(getPrice(inpPrice, open, close, high, low, i, rates_total), inpMomPeriod, i, rates_total)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iSmoothMomentum(price, period, r, bars, instanceNo=0):
    global _s_iSmoothMomentum_m_arraySize
    if _s_iSmoothMomentum_m_arraySize < bars:
        _res = ArrayResize(workSmom, bars + 500)
        if _res <= bars:
            return 0.0
        _s_iSmoothMomentum_m_arraySize = _res
    instanceNo *= 3
    workSmom[r][0 + instanceNo] = price
    workSmom[r][1 + instanceNo] = price
    workSmom[r][2 + instanceNo] = price
    if r > 0:
        alphar = _fdiv(2.0, 1.0 + period)
        alphad = _fdiv(2.0, 1.0 + MathSqrt(period))
        workSmom[r][0 + instanceNo] = workSmom[r - 1][0 + instanceNo] + (alphar * (price - workSmom[r - 1][0 + instanceNo]))
        workSmom[r][1 + instanceNo] = workSmom[r - 1][1 + instanceNo] + (alphad * (price - workSmom[r - 1][1 + instanceNo]))
        workSmom[r][2 + instanceNo] = workSmom[r - 1][2 + instanceNo] + (alphad * (workSmom[r][1 + instanceNo] - workSmom[r - 1][2 + instanceNo]))
    return workSmom[r][2 + instanceNo] - workSmom[r][0 + instanceNo]

def getPrice(tprice, open, close, high, low, i, _bars):
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

# ---- static local variables
_s_iSmoothMomentum_m_arraySize = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmootherMomentum(_MQL5Indicator):
    name = 'Smoother momentum'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMomPeriod': 20,  # Momentum period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

