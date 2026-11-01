"""ATR adaptive Laguerre RSI — converted from MQL5: MQL5 Indicators/ATR adaptive Laguerre RSI/ATR adaptive Laguerre RSI.mq5

Copyright: © mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 16748574, 4678655]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ATR adaptive Laguerre RSI', 'source': 'MQL5 Indicators/ATR adaptive Laguerre RSI/ATR adaptive Laguerre RSI.mq5', 'folder': 'ATR adaptive Laguerre RSI', 'inputs': [{'mql': 'inpAtrPeriod', 'py': 'inpAtrPeriod', 'param': 'inpAtrPeriod', 'type': 'int', 'default': 32, 'label': 'ATR period', 'sinput': False}, {'mql': 'inpRsiPrice', 'py': 'inpRsiPrice', 'param': 'inpRsiPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpLevelUp', 'py': 'inpLevelUp', 'param': 'inpLevelUp', 'type': 'double', 'default': 0.85, 'label': 'Level up', 'sinput': False}, {'mql': 'inpLevelDown', 'py': 'inpLevelDown', 'param': 'inpLevelDown', 'type': 'double', 'default': 0.15, 'label': 'Level down', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpAtrPeriod = _input('inpAtrPeriod', 32)  # ATR period
inpRsiPrice = _input('inpRsiPrice', PRICE_CLOSE)  # Price
inpLevelUp = _input('inpLevelUp', 0.85)  # Level up
inpLevelDown = _input('inpLevelDown', 0.15)  # Level down
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
vals = Arr(0, 0.0)
atr = Arr(0, 0.0)
ª_atrHandle = 0
ª_atrPeriod = 0
workLagRsi = Arr(6, 0.0, dyn=False, dims=(4,))

def OnInit():
    global ª_atrHandle, ª_atrPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, atr, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpLevelUp)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inpLevelDown)
    ª_atrPeriod = (inpAtrPeriod if (inpAtrPeriod > 1) else 1)
    ª_atrHandle = iATR(Symbol(), 0, ª_atrPeriod)
    if not _checkHandle(ª_atrHandle, 'ATR'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR adaptive Laguerre RSI (' + _str(inpAtrPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_atrHandle, 0, 0, _copyCount, atr) != _copyCount:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        start = ((i - ª_atrPeriod + 1) if (i > ª_atrPeriod) else 0)
        max_ = atr[ArrayMaximum(atr, start, ª_atrPeriod)]
        min_ = atr[ArrayMinimum(atr, start, ª_atrPeriod)]
        coeff = ((1.0 - _fdiv(atr[i] - min_, max_ - min_)) if (min_ != max_) else 0.5)
        val[i] = iLaGuerreRsi(getPrice(inpRsiPrice, open, close, high, low, i), ª_atrPeriod * (coeff + 0.75), i)
        valc[i] = (1 if (val[i] > inpLevelUp) else 2 if (val[i] < inpLevelDown) else 0)
        i += 1
    return i

def iLaGuerreRsi(price, period, i, instance=0):
    _indC = _imod(i, 6)
    _inst = instance * 4
    CU = 0.0
    CD = 0.0
    if i > 0 and period > 1:
        _indP = _imod(i - 1, 6)
        _gamma = 1.0 - _fdiv(10.0, period + 9.0)
        workLagRsi[_indC][_inst] = price + (_gamma * (workLagRsi[_indP][_inst] - price))
        workLagRsi[_indC][_inst + 1] = workLagRsi[_indP][_inst] + (_gamma * (workLagRsi[_indP][_inst + 1] - workLagRsi[_indC][_inst]))
        workLagRsi[_indC][_inst + 2] = workLagRsi[_indP][_inst + 1] + (_gamma * (workLagRsi[_indP][_inst + 2] - workLagRsi[_indC][_inst + 1]))
        workLagRsi[_indC][_inst + 3] = workLagRsi[_indP][_inst + 2] + (_gamma * (workLagRsi[_indP][_inst + 3] - workLagRsi[_indC][_inst + 2]))
        if workLagRsi[_indC][_inst] >= workLagRsi[_indC][_inst + 1]:
            CU = workLagRsi[_indC][_inst] - workLagRsi[_indC][_inst + 1]
        else:
            CD = workLagRsi[_indC][_inst + 1] - workLagRsi[_indC][_inst]
        if workLagRsi[_indC][_inst + 1] >= workLagRsi[_indC][_inst + 2]:
            CU += workLagRsi[_indC][_inst + 1] - workLagRsi[_indC][_inst + 2]
        else:
            CD += workLagRsi[_indC][_inst + 2] - workLagRsi[_indC][_inst + 1]
        if workLagRsi[_indC][_inst + 2] >= workLagRsi[_indC][_inst + 3]:
            CU += workLagRsi[_indC][_inst + 2] - workLagRsi[_indC][_inst + 3]
        else:
            CD += workLagRsi[_indC][_inst + 3] - workLagRsi[_indC][_inst + 2]
    else:
        for k in range(0, 4):
            workLagRsi[_indC][_inst + k] = price
    return (_fdiv(CU, CU + CD) if ((CU + CD) != 0) else 0)

def getPrice(tprice, open, close, high, low, i):
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

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__handles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__handles, _size + 1)
        _s__checkHandle__handles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__handles[i])
        ArrayResize(_s__checkHandle__handles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- static local variables
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRAdaptiveLaguerreRSI(_MQL5Indicator):
    name = 'ATR adaptive Laguerre RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpAtrPeriod': 32,  # ATR period
        'inpRsiPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLevelUp': 0.85,  # Level up
        'inpLevelDown': 0.15,  # Level down
    }

