"""Time Fractal Energy adaptive Laguerre RSI — converted from MQL5: MQL5 Indicators/Time Fractal Energy adaptive Laguerre RSI/Time Fractal Energy adaptive Laguerre RSI.mq5

Copyright: © mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16748574, 9662683]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Time Fractal Energy adaptive Laguerre RSI', 'source': 'MQL5 Indicators/Time Fractal Energy adaptive Laguerre RSI/Time Fractal Energy adaptive Laguerre RSI.mq5', 'folder': 'Time Fractal Energy adaptive Laguerre RSI', 'inputs': [{'mql': 'inpAtrPeriod', 'py': 'inpAtrPeriod', 'param': 'inpAtrPeriod', 'type': 'int', 'default': 14, 'label': 'ATR period', 'sinput': False}, {'mql': 'inpRsiPrice', 'py': 'inpRsiPrice', 'param': 'inpRsiPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'double', 'default': 5.0, 'label': 'Smoothing factor', 'sinput': False}, {'mql': 'inpLevelUp', 'py': 'inpLevelUp', 'param': 'inpLevelUp', 'type': 'double', 'default': 0.85, 'label': 'Level up', 'sinput': False}, {'mql': 'inpLevelDown', 'py': 'inpLevelDown', 'param': 'inpLevelDown', 'type': 'double', 'default': 0.15, 'label': 'Level down', 'sinput': False}, {'mql': 'inpColorDisplay', 'py': 'inpColorDisplay', 'param': 'inpColorDisplay', 'type': 'int', 'default': 0, 'label': 'Color change mode :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorDisplay
change_onLevel = 0
change_onSlope = 1
_enum('enColorDisplay', {0: 'change_onLevel', 1: 'change_onSlope'})

# ---- inputs and global variables
inpAtrPeriod = _input('inpAtrPeriod', 14)  # ATR period
inpRsiPrice = _input('inpRsiPrice', PRICE_CLOSE)  # Price
inpSmooth = _input('inpSmooth', 5.0)  # Smoothing factor
inpLevelUp = _input('inpLevelUp', 0.85)  # Level up
inpLevelDown = _input('inpLevelDown', 0.15)  # Level down
inpColorDisplay = _input('inpColorDisplay', change_onLevel)  # Color change mode :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
tr = Arr(0, 0.0)
_smoothFactor = 0.0
workLagRsi = Arr(5, 0.0, dyn=False, dims=(4,))
workLagFil = Arr(5, 0.0, dyn=False, dims=(4,))

def OnInit():
    global _smoothFactor
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, tr, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpLevelUp)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inpLevelDown)
    _smoothFactor = MathMax(1, inpSmooth)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Time Fractal Energy adaptive Laguerre RSI (' + _str(inpAtrPeriod) + ',' + _str(_smoothFactor) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        tr[i] = ((MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])) if (i > 0) else (high[i] - low[i]))
        _atr = tr[i]
        _min = low[i]
        _max = high[i]
        k = 1
        while k < inpAtrPeriod and (i - k) >= 0:
            _atr += tr[i - k]
            _max = MathMax(high[i - k], _max)
            _min = MathMin(low[i - k], _min)
            k += 1
        _gamma = (_fdiv(MathLog(_fdiv(_atr, _max - _min)), MathLog(inpAtrPeriod)) if (_min != _max) else 0)
        _rsi = iLaGuerreRsi(getPrice(inpRsiPrice, open, close, high, low, i, rates_total), _gamma, i)
        val[i] = iLaGuerreFil(_rsi, _fdiv(_gamma, _smoothFactor), i)
        _sw1 = inpColorDisplay
        if _sw1 == change_onLevel:
            valc[i] = (1 if (val[i] > inpLevelUp) else 2 if (val[i] < inpLevelDown) else 0)
        elif _sw1 == change_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iLaGuerreRsi(price, gamma, i, instance=0):
    _indP = _imod(i - 1, 5)
    _indC = _imod(i, 5)
    _inst = instance * 4
    workLagRsi[_indC][_inst] = ((((1.0 - gamma) * price) + (gamma * workLagRsi[_indP][_inst])) if (i > 0) else price)
    workLagRsi[_indC][_inst + 1] = ((((-gamma) * workLagRsi[_indC][_inst]) + workLagRsi[_indP][_inst] + (gamma * workLagRsi[_indP][_inst + 1])) if (i > 0) else price)
    workLagRsi[_indC][_inst + 2] = ((((-gamma) * workLagRsi[_indC][_inst + 1]) + workLagRsi[_indP][_inst + 1] + (gamma * workLagRsi[_indP][_inst + 2])) if (i > 0) else price)
    workLagRsi[_indC][_inst + 3] = ((((-gamma) * workLagRsi[_indC][_inst + 2]) + workLagRsi[_indP][_inst + 2] + (gamma * workLagRsi[_indP][_inst + 3])) if (i > 0) else price)
    CU = 0.0
    CD = 0.0
    if i > 0:
        if workLagRsi[_indC][_inst] >= workLagRsi[_indC][_inst + 1]:
            CU = workLagRsi[_indC][_inst] - workLagRsi[_indC][_inst + 1]
        else:
            CD = workLagRsi[_indC][_inst + 1] - workLagRsi[_indC][_inst]
        if workLagRsi[_indC][_inst + 1] >= workLagRsi[_indC][_inst + 2]:
            CU = CU + workLagRsi[_indC][_inst + 1] - workLagRsi[_indC][_inst + 2]
        else:
            CD = CD + workLagRsi[_indC][_inst + 2] - workLagRsi[_indC][_inst + 1]
        if workLagRsi[_indC][_inst + 2] >= workLagRsi[_indC][_inst + 3]:
            CU = CU + workLagRsi[_indC][_inst + 2] - workLagRsi[_indC][_inst + 3]
        else:
            CD = CD + workLagRsi[_indC][_inst + 3] - workLagRsi[_indC][_inst + 2]
    return (_fdiv(CU, CU + CD) if ((CU + CD) != 0) else 0)

def iLaGuerreFil(price, gamma, i, instance=0):
    if gamma <= 0:
        return price
    _indP = _imod(i - 1, 5)
    _indC = _imod(i, 5)
    _inst = instance * 4
    workLagFil[_indC][_inst] = ((((1.0 - gamma) * price) + (gamma * workLagFil[_indP][_inst])) if (i > 0) else price)
    workLagFil[_indC][_inst + 1] = ((((-gamma) * workLagFil[_indC][_inst]) + workLagFil[_indP][_inst] + (gamma * workLagFil[_indP][_inst + 1])) if (i > 0) else price)
    workLagFil[_indC][_inst + 2] = ((((-gamma) * workLagFil[_indC][_inst + 1]) + workLagFil[_indP][_inst + 1] + (gamma * workLagFil[_indP][_inst + 2])) if (i > 0) else price)
    workLagFil[_indC][_inst + 3] = ((((-gamma) * workLagFil[_indC][_inst + 2]) + workLagFil[_indP][_inst + 2] + (gamma * workLagFil[_indP][_inst + 3])) if (i > 0) else price)
    return (workLagFil[_indC][_inst + 0] + (2.0 * workLagFil[_indC][_inst + 1]) + (2.0 * workLagFil[_indC][_inst + 2]) + workLagFil[_indC][_inst + 3]) / 6.0

def getPrice(tprice, open, close, high, low, i, _bars):
    _sw2 = tprice
    if _sw2 == PRICE_CLOSE:
        return close[i]
    elif _sw2 == PRICE_OPEN:
        return open[i]
    elif _sw2 == PRICE_HIGH:
        return high[i]
    elif _sw2 == PRICE_LOW:
        return low[i]
    elif _sw2 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TimeFractalEnergyAdaptiveLaguerreRSI(_MQL5Indicator):
    name = 'Time Fractal Energy adaptive Laguerre RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpAtrPeriod': 14,  # ATR period
        'inpRsiPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpSmooth': 5.0,  # Smoothing factor
        'inpLevelUp': 0.85,  # Level up
        'inpLevelDown': 0.15,  # Level down
        'inpColorDisplay': _Choice({0: 'Change colors on levels crossing', 1: 'Change colors on Laguerre RSI slope'}, default=0),  # Color change mode :
    }

