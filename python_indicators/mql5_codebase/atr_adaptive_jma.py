"""ATR adaptive JMA — converted from MQL5: MQL5 Indicators/ATR adaptive JMA/ATR adaptive JMA.mq5

ATR adaptive JMA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 3937500, 32768]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'JMA'}, 'levels': [], 'description': ['ATR adaptive JMA'], 'name': 'ATR adaptive JMA', 'source': 'MQL5 Indicators/ATR adaptive JMA/ATR adaptive JMA.mq5', 'folder': 'ATR adaptive JMA', 'inputs': [{'mql': 'inpJmaPeriod', 'py': 'inpJmaPeriod', 'param': 'inpJmaPeriod', 'type': 'int', 'default': 14, 'label': 'JMA period', 'sinput': False}, {'mql': 'inpJmaPhase', 'py': 'inpJmaPhase', 'param': 'inpJmaPhase', 'type': 'double', 'default': 0.0, 'label': 'JMA phase', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpJmaPeriod = _input('inpJmaPeriod', 14)  # JMA period
inpJmaPhase = _input('inpJmaPhase', 0.0)  # JMA phase
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
atr = Arr(0, 0.0)
tr = Arr(0, 0.0)
workSmooth = Arr(11, 0.0, dyn=False, dims=(10,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, atr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, tr, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR adaptive JMA (' + _str(inpJmaPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        tr[i] = ((MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])) if (i > 0) else (high[i] - low[i]))
        atr[i] = 0.0
        k = 0
        while k < inpJmaPeriod and (i - k) >= 0:
            atr[i] += tr[i - k]
            k += 1
        atr[i] = atr[i] / inpJmaPeriod
        _start = MathMax(i - inpJmaPeriod + 1, 0)
        _max = atr[ArrayMaximum(atr, _start, inpJmaPeriod)]
        _min = atr[ArrayMinimum(atr, _start, inpJmaPeriod)]
        _coeff = ((1 - _fdiv(atr[i] - _min, _max - _min)) if (_min != _max) else 0.5)
        val[i] = iSmooth(getPrice(inpPrice, open, close, high, low, i, rates_total), (inpJmaPeriod * (_coeff + 1.0)) / 2.0, inpJmaPhase, i)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

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


class ATRAdaptiveJMA(_MQL5Indicator):
    name = 'ATR adaptive JMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpJmaPeriod': 14,  # JMA period
        'inpJmaPhase': 0.0,  # JMA phase
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

