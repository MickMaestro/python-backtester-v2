"""JMA z-score — converted from MQL5: MQL5 Indicators/JMA Z-score/JMA z-score.mq5

JMA z-score
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16748574, 9639167]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Z-score'}, 'levels': [], 'description': ['JMA z-score'], 'name': 'JMA z-score', 'source': 'MQL5 Indicators/JMA Z-score/JMA z-score.mq5', 'folder': 'JMA Z-score', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'JMA smooth period', 'sinput': False}, {'mql': 'inpPhase', 'py': 'inpPhase', 'param': 'inpPhase', 'type': 'double', 'default': 0.0, 'label': 'JMA phase', 'sinput': False}, {'mql': 'inpZsPeriod', 'py': 'inpZsPeriod', 'param': 'inpZsPeriod', 'type': 'int', 'default': 30, 'label': 'Z-score period (<=1 for same as JMA period)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # JMA smooth period
inpPhase = _input('inpPhase', 0.0)  # JMA phase
inpZsPeriod = _input('inpZsPeriod', 30)  # Z-score period (<=1 for same as JMA period)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
_zsPeriod = 0
workZs = Arr(0, 0.0)
workSmooth = Arr(11, 0.0, dyn=False, dims=(10,))

def OnInit():
    global _zsPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    _zsPeriod = (inpPeriod if (inpZsPeriod <= 1) else inpZsPeriod)
    if _zsPeriod <= 1:
        Alert('Z-score period can not be less than 2')
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'JMA z-score (' + _str(inpPeriod) + ',' + _str(_zsPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iZScore(iSmooth(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, inpPhase, i), _zsPeriod, i, rates_total)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iZScore(value, period, i, bars):
    if ArraySize(workZs) != bars:
        ArrayResize(workZs, bars)
    workZs[i] = value
    if period <= 1:
        return 0.0
    sumx = 0.0
    sumxx = 0.0
    mean = 0.0
    k = 0
    while k < period and (i - k) >= 0:
        pass
        mean += workZs[i - k]
        sumx += workZs[i - k]
        sumxx += workZs[i - k] * workZs[i - k]
        k += 1
    deviation = MathSqrt(_fdiv(sumxx - _fdiv(sumx * sumx, float(period)), float(period)))
    mean = _fdiv(mean, float(period))
    return (_fdiv(value - mean, deviation) if (deviation != 0) else 0)

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


class JMAZScore(_MQL5Indicator):
    name = 'JMA z-score'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # JMA smooth period
        'inpPhase': 0.0,  # JMA phase
        'inpZsPeriod': 30,  # Z-score period (<=1 for same as JMA period)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

