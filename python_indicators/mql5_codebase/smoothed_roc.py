"""Smoothed ROC — converted from MQL5: MQL5 Indicators/Smoothed Rate of Change/Smoothed ROC.mq5

Smoothed rate of Change
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Smoothed ROC'}, 'levels': [], 'description': ['Smoothed rate of Change'], 'name': 'Smoothed ROC', 'source': 'MQL5 Indicators/Smoothed Rate of Change/Smoothed ROC.mq5', 'folder': 'Smoothed Rate of Change', 'inputs': [{'mql': 'inpRocPeriod', 'py': 'inpRocPeriod', 'param': 'inpRocPeriod', 'type': 'int', 'default': 21, 'label': 'ROC period', 'sinput': False}, {'mql': 'inpEmaPeriod', 'py': 'inpEmaPeriod', 'param': 'inpEmaPeriod', 'type': 'int', 'default': 13, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRocPeriod = _input('inpRocPeriod', 21)  # ROC period
inpEmaPeriod = _input('inpEmaPeriod', 13)  # Smoothing period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workEma = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoothed ROC (' + _str(inpRocPeriod) + ',' + _str(inpEmaPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _pema = iEma(getPrice(inpPrice, open, close, high, low, i - inpRocPeriod, rates_total), inpEmaPeriod, i, rates_total, 0)
        _cema = iEma(getPrice(inpPrice, open, close, high, low, i, rates_total), inpEmaPeriod, i, rates_total, 1)
        val[i] = (_fdiv(100 * (_cema - _pema), _pema) if (_pema != 0) else 0)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def getPrice(tprice, open, close, high, low, i, _bars):
    if i > 0 and i < _bars:
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


class SmoothedROC(_MQL5Indicator):
    name = 'Smoothed ROC'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRocPeriod': 21,  # ROC period
        'inpEmaPeriod': 13,  # Smoothing period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

