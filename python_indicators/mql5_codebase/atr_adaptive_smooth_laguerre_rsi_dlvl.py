"""ATR adaptive smooth Laguerre RSI (dlvl) — converted from MQL5: MQL5 Indicators/ATR adaptive smooth Laguerre RSI (dlvl)/ATR adaptive smooth Laguerre RSI (dlvl).mq5

Copyright: © mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [11119017], 2: [11119017], 3: [8421504, 16748574, 4678655]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'Level up', 2: 'Level down'}, 'levels': [], 'description': [], 'name': 'ATR adaptive smooth Laguerre RSI (dlvl)', 'source': 'MQL5 Indicators/ATR adaptive smooth Laguerre RSI (dlvl)/ATR adaptive smooth Laguerre RSI (dlvl).mq5', 'folder': 'ATR adaptive smooth Laguerre RSI (dlvl)', 'inputs': [{'mql': 'inpAtrPeriod', 'py': 'inpAtrPeriod', 'param': 'inpAtrPeriod', 'type': 'int', 'default': 32, 'label': 'Laguerre/ATR period', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'double', 'default': 5.0, 'label': 'Smooth period', 'sinput': False}, {'mql': 'inpRsiPrice', 'py': 'inpRsiPrice', 'param': 'inpRsiPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpLevelPeriod', 'py': 'inpLevelPeriod', 'param': 'inpLevelPeriod', 'type': 'double', 'default': 10.0, 'label': 'Levels period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpAtrPeriod = _input('inpAtrPeriod', 32)  # Laguerre/ATR period
inpSmoothPeriod = _input('inpSmoothPeriod', 5.0)  # Smooth period
inpRsiPrice = _input('inpRsiPrice', PRICE_CLOSE)  # Price
inpLevelPeriod = _input('inpLevelPeriod', 10.0)  # Levels period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
atr = Arr(0, 0.0)
lup = Arr(0, 0.0)
ldn = Arr(0, 0.0)
ª_atrHandle = 0
ª_atrPeriod = 0
ª_smoothPeriod = 0.0
ª_alphal = 0.0
ª_lvlPeriod = 0.0
workLagRsi = Arr(6, 0.0, dyn=False, dims=(5,))

def OnInit():
    global ª_alphal, ª_atrHandle, ª_atrPeriod, ª_lvlPeriod, ª_smoothPeriod
    SetIndexBuffer(0, lup, INDICATOR_DATA)
    SetIndexBuffer(1, ldn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, atr, INDICATOR_CALCULATIONS)
    ª_atrPeriod = (inpAtrPeriod if (inpAtrPeriod > 1) else 1)
    ª_smoothPeriod = MathMax(inpSmoothPeriod, 1)
    ª_lvlPeriod = MathMax(inpLevelPeriod, 1)
    ª_alphal = _fdiv(2.0, 1.0 + ª_lvlPeriod)
    ª_atrHandle = iATR(Symbol(), 0, ª_atrPeriod)
    if not _checkHandle(ª_atrHandle, 'ATR'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR adaptive Laguerre RSI (' + _str(inpAtrPeriod) + ',' + _str(ª_atrPeriod) + ',' + _str(ª_lvlPeriod) + ')')
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
        coeff = ((1.75 - _fdiv(atr[i] - min_, max_ - min_)) if (min_ != max_) else 0.5)
        val[i] = iLaGuerreRsi(getPrice(inpRsiPrice, open, close, high, low, i), ª_atrPeriod * coeff, ª_smoothPeriod, i)
        lup[i] = ((lup[i - 1] if (val[i] < ldn[i - 1]) else (lup[i - 1] + (ª_alphal * (val[i] - lup[i - 1])))) if (i > 0) else val[i])
        ldn[i] = ((ldn[i - 1] if (val[i] > lup[i - 1]) else (ldn[i - 1] + (ª_alphal * (val[i] - ldn[i - 1])))) if (i > 0) else val[i])
        valc[i] = (1 if (val[i] > lup[i]) else 2 if (val[i] < ldn[i]) else 0)
        i += 1
    return i

def iLaGuerreRsi(price, period, smooth, i, instance=0):
    _indC = _imod(i, 6)
    _inst = instance * 5
    CU = 0.0
    CD = 0.0
    if i > 0 and period > 1:
        _indP = _imod(i - 1, 6)
        _gamma = 1.0 - _fdiv(10.0, period + 9.0)
        workLagRsi[_indC][_inst + 4] = workLagRsi[_indP][_inst + 4] + (_fdiv(2.0, 1.0 + smooth) * (price - workLagRsi[_indP][_inst + 4]))
        workLagRsi[_indC][_inst] = workLagRsi[_indC][_inst + 4] + (_gamma * (workLagRsi[_indP][_inst] - workLagRsi[_indC][_inst + 4]))
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
        for k in range(0, 5):
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


class ATRAdaptiveSmoothLaguerreRSIDlvl(_MQL5Indicator):
    name = 'ATR adaptive smooth Laguerre RSI (dlvl)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpAtrPeriod': 32,  # Laguerre/ATR period
        'inpSmoothPeriod': 5.0,  # Smooth period
        'inpRsiPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLevelPeriod': 10.0,  # Levels period
    }

