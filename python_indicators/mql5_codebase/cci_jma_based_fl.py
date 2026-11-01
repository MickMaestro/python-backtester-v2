"""CCI - JMA based - fl — converted from MQL5: MQL5 Indicators/CCI JMA based with floating levels/CCI - JMA based - fl.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [3329330], 2: [42495], 3: [12632256], 4: [12632256, 3329330, 42495]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'middle level', 4: 'value'}, 'levels': [], 'description': [], 'name': 'CCI - JMA based - fl', 'source': 'MQL5 Indicators/CCI JMA based with floating levels/CCI - JMA based - fl.mq5', 'folder': 'CCI JMA based with floating levels', 'inputs': [{'mql': 'inpCciPeriod', 'py': 'inpCciPeriod', 'param': 'inpCciPeriod', 'type': 'int', 'default': 32, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpCciPrice', 'py': 'inpCciPrice', 'param': 'inpCciPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 32, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpSmoothPhase', 'py': 'inpSmoothPhase', 'param': 'inpSmoothPhase', 'type': 'double', 'default': 0.0, 'label': 'Smoothing phase', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 32, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 80.0, 'label': 'Up level %', 'sinput': False}, {'mql': 'inpFlLevelDown', 'py': 'inpFlLevelDown', 'param': 'inpFlLevelDown', 'type': 'double', 'default': 20.0, 'label': 'Down level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpCciPeriod = _input('inpCciPeriod', 32)  # CCI period
inpCciPrice = _input('inpCciPrice', PRICE_TYPICAL)  # Price
inpSmoothPeriod = _input('inpSmoothPeriod', 32)  # Smoothing period
inpSmoothPhase = _input('inpSmoothPhase', 0.0)  # Smoothing phase
inpFlPeriod = _input('inpFlPeriod', 32)  # Floating levels period
inpFlLevelUp = _input('inpFlLevelUp', 80.0)  # Up level %
inpFlLevelDown = _input('inpFlLevelDown', 20.0)  # Down level %
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
levelMi = Arr(0, 0.0)
workSmooth = Arr(11, 0.0, dyn=False, dims=(20,))
workEmaDeviation = Arr(5, 0.0, dyn=False, dims=(2,))

def OnInit():
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, levelMi, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI - T3 based - fl (' + _str(inpCciPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _price = iSmooth(getPrice(inpCciPrice, open, close, high, low, i, rates_total), inpSmoothPeriod, inpSmoothPhase, i, 1)
        avg = iSmooth(_price, inpCciPeriod, inpSmoothPhase, i, 0)
        dev = MathMax(iEmaDeviation(_price, inpCciPeriod, i), DBL_MIN)
        val[i] = _fdiv(_price - avg, 0.015 * dev)
        _start = MathMax(i - inpFlPeriod + 1, 0)
        min_ = val[ArrayMinimum(val, _start, inpFlPeriod)]
        max_ = val[ArrayMaximum(val, _start, inpFlPeriod)]
        range_ = max_ - min_
        levelUp[i] = min_ + ((inpFlLevelUp * range_) / 100.0)
        levelDn[i] = min_ + ((inpFlLevelDown * range_) / 100.0)
        levelMi[i] = min_ + ((50 * range_) / 100.0)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i

def iSmooth(price, length, phase, i, instance=0):
    _indP = _imod(i - 1, 11)
    _indC = _imod(i, 11)
    _inst = instance * 10
    if i == 0 or length <= 1:
        k = 0
        while k < 7:
            workSmooth[_indC][_inst + k] = price
            k += 1
        while k < 10:
            workSmooth[_indC][_inst + k] = 0.0
            k += 1
        return price
    len1 = MathMax(_fdiv(MathLog(MathSqrt(0.5 * (length - 1.0))), MathLog(2.0)) + 2.0, 0)
    pow1 = MathMax(len1 - 2.0, 0.5)
    del1 = price - workSmooth[_indP][_inst + 5]
    absDel1 = MathAbs(del1)
    del2 = price - workSmooth[_indP][_inst + 6]
    absDel2 = MathAbs(del2)
    _indF = _imod(i - MathMin(i, 10), 11)
    workSmooth[_indC][_inst + 7] = (absDel1 if (absDel1 > absDel2) else absDel2 if (absDel1 < absDel2) else 0)
    workSmooth[_indC][_inst + 8] = workSmooth[_indP][_inst + 8] + ((workSmooth[_indC][_inst + 7] - workSmooth[_indF][_inst + 7]) * 0.1)
    workSmooth[_indC][_inst + 9] = workSmooth[_indP][_inst + 9] + (_fdiv(2.0, MathMax(4.0 * length, 30) + 1.0) * (workSmooth[_indC][_inst + 8] - workSmooth[_indP][_inst + 9]))
    dVolty = (_fdiv(workSmooth[_indC][_inst + 7], workSmooth[_indC][_inst + 9]) if (workSmooth[_indC][_inst + 9] > 0) else 0)
    dVoltyTmp = MathPow(len1, _fdiv(1.0, pow1))
    if dVolty > dVoltyTmp:
        dVolty = dVoltyTmp
    if dVolty < 1.0:
        dVolty = 1.0
    pow2 = MathPow(dVolty, pow1)
    len2 = MathSqrt(0.5 * (length - 1)) * len1
    Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
    workSmooth[_indC][_inst + 5] = (price if (del1 > 0) else (price - (Kv * del1)))
    workSmooth[_indC][_inst + 6] = (price if (del2 < 0) else (price - (Kv * del2)))
    corr = (MathMax(MathMin(phase, 100), -100) / 100.0) + 1.5
    beta = _fdiv(0.45 * (length - 1), (0.45 * (length - 1)) + 2)
    alpha = MathPow(beta, pow2)
    workSmooth[_indC][_inst + 0] = price + (alpha * (workSmooth[_indP][_inst + 0] - price))
    workSmooth[_indC][_inst + 1] = ((price - workSmooth[_indC][_inst + 0]) * (1 - beta)) + (beta * workSmooth[_indP][_inst + 1])
    workSmooth[_indC][_inst + 2] = workSmooth[_indC][_inst + 0] + (corr * workSmooth[_indC][_inst + 1])
    workSmooth[_indC][_inst + 3] = ((workSmooth[_indC][_inst + 2] - workSmooth[_indP][_inst + 4]) * ((1 - alpha) * (1 - alpha))) + (alpha * alpha * workSmooth[_indP][_inst + 3])
    workSmooth[_indC][_inst + 4] = workSmooth[_indP][_inst + 4] + workSmooth[_indC][_inst + 3]
    return workSmooth[_indC][_inst + 4]

def iEmaDeviation(price, period, i, instance=0):
    _indP = _imod(i - 1, 5)
    _indC = _imod(i, 5)
    _inst = instance * 2
    if i > 0 and period > 1:
        alpha = _fdiv(2.0, 1.0 + period)
        workEmaDeviation[_indC][_inst + 0] = workEmaDeviation[_indP][_inst + 0] + (alpha * (price - workEmaDeviation[_indP][_inst + 0]))
        workEmaDeviation[_indC][_inst + 1] = workEmaDeviation[_indP][_inst + 1] + (alpha * ((price * price) - workEmaDeviation[_indP][_inst + 1]))
    else:
        for k in range(0, 2):
            workEmaDeviation[_indC][_inst + k] = price
    return MathSqrt(_fdiv(period * (workEmaDeviation[_indC][_inst + 1] - (workEmaDeviation[_indC][_inst + 0] * workEmaDeviation[_indC][_inst + 0])), MathMax(period - 1, 1)))

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIJMABasedFl(_MQL5Indicator):
    name = 'CCI - JMA based - fl'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCciPeriod': 32,  # CCI period
        'inpCciPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'inpSmoothPeriod': 32,  # Smoothing period
        'inpSmoothPhase': 0.0,  # Smoothing phase
        'inpFlPeriod': 32,  # Floating levels period
        'inpFlLevelUp': 80.0,  # Up level %
        'inpFlLevelDown': 20.0,  # Down level %
    }

