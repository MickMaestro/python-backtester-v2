"""ATR adaptive Laguerre filter — converted from MQL5: MQL5 Indicators/ATR adaptive Laguerre filter/ATR adaptive Laguerre filter.mq5

ATR adaptive Laguerre filter
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 3937500]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Laguerre filter'}, 'levels': [], 'description': ['ATR adaptive Laguerre filter'], 'name': 'ATR adaptive Laguerre filter', 'source': 'MQL5 Indicators/ATR adaptive Laguerre filter/ATR adaptive Laguerre filter.mq5', 'folder': 'ATR adaptive Laguerre filter', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 14.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14.0)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
atr = Arr(0, 0.0)
_atrHandle = 0
_atrPeriod = 0
workLagFil = Arr(6, 0.0, dyn=False, dims=(4,))

def OnInit():
    global _atrHandle, _atrPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, atr, INDICATOR_CALCULATIONS)
    _atrPeriod = MathMax(_int(inpPeriod), 1)
    _atrHandle = iATR(Symbol(), 0, _atrPeriod)
    if not _checkHandle(_atrHandle):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR adaptive Laguerre filter (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(_atrHandle) < rates_total:
        return prev_calculated
    _copyCount = MathMin(rates_total - prev_calculated + 1, rates_total)
    if CopyBuffer(_atrHandle, 0, 0, _copyCount, atr) != _copyCount:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _start = MathMax(i - _atrPeriod + 1, 0)
        _max = atr[ArrayMaximum(atr, _start, _atrPeriod)]
        _min = atr[ArrayMinimum(atr, _start, _atrPeriod)]
        _coeff = ((1 - _fdiv(atr[i] - _min, _max - _min)) if (_min != _max) else 0.5)
        val[i] = iLaGuerreFil(getPrice(inpPrice, open, close, high, low, i), (inpPeriod * (_coeff + 1.0)) / 2.0, i)
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

def _checkHandle(_handle):
    _size = ArraySize(_s__checkHandle__handles)
    if _handle != INVALID_HANDLE:
        ArrayResize(_s__checkHandle__handles, _size + 1)
        _s__checkHandle__handles[_size] = _handle
        return True
    for i in range(_size - 1, 0, -1):
        IndicatorRelease(_s__checkHandle__handles[i])
    ArrayResize(_s__checkHandle__handles, 0)
    return False

# ---- static local variables
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRAdaptiveLaguerreFilter(_MQL5Indicator):
    name = 'ATR adaptive Laguerre filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14.0,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

