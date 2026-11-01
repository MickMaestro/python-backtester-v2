"""Multi JMA slopes 2 — converted from MQL5: MQL5 Indicators/Multi JMA Slopes/Multi JMA slopes 2.mq5

Multi JMA slopes
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 3, 2: 3}, 'colors': {1: [3329330], 2: [3937500]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Multi JMA slopes up', 2: 'Multi JMA slopes down'}, 'levels': [], 'description': ['Multi JMA slopes'], 'name': 'Multi JMA slopes 2', 'source': 'MQL5 Indicators/Multi JMA Slopes/Multi JMA slopes 2.mq5', 'folder': 'Multi JMA Slopes', 'inputs': [{'mql': 'inpPeriod1', 'py': 'inpPeriod1', 'param': 'inpPeriod1', 'type': 'int', 'default': 8, 'label': 'Period 1', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 11, 'label': 'Period 2', 'sinput': False}, {'mql': 'inpPeriod3', 'py': 'inpPeriod3', 'param': 'inpPeriod3', 'type': 'int', 'default': 14, 'label': 'Period 3', 'sinput': False}, {'mql': 'inpPeriod4', 'py': 'inpPeriod4', 'param': 'inpPeriod4', 'type': 'int', 'default': 17, 'label': 'Period 4', 'sinput': False}, {'mql': 'inpPeriod5', 'py': 'inpPeriod5', 'param': 'inpPeriod5', 'type': 'int', 'default': 20, 'label': 'Period 5', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod1 = _input('inpPeriod1', 8)  # Period 1
inpPeriod2 = _input('inpPeriod2', 11)  # Period 2
inpPeriod3 = _input('inpPeriod3', 14)  # Period 3
inpPeriod4 = _input('inpPeriod4', 17)  # Period 4
inpPeriod5 = _input('inpPeriod5', 20)  # Period 5
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
histou = Arr(0, 0.0)
histod = Arr(0, 0.0)
avg1 = Arr(0, 0.0)
avg2 = Arr(0, 0.0)
avg3 = Arr(0, 0.0)
avg4 = Arr(0, 0.0)
avg5 = Arr(0, 0.0)
workSmooth = Arr(11, 0.0, dyn=False, dims=(50,))

def OnInit():
    SetIndexBuffer(0, histou, INDICATOR_DATA)
    SetIndexBuffer(1, histod, INDICATOR_DATA)
    SetIndexBuffer(2, avg1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, avg2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, avg3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, avg4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, avg5, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Multi JMA slopes (' + _str(inpPeriod1) + ',' + _str(inpPeriod2) + ',' + _str(inpPeriod3) + ',' + _str(inpPeriod4) + ',' + _str(inpPeriod5) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        avg1[i] = iSmooth(_price, inpPeriod1, 0.0, i, 0)
        avg2[i] = iSmooth(_price, inpPeriod2, 0.0, i, 1)
        avg3[i] = iSmooth(_price, inpPeriod3, 0.0, i, 2)
        avg4[i] = iSmooth(_price, inpPeriod4, 0.0, i, 3)
        avg5[i] = iSmooth(_price, inpPeriod5, 0.0, i, 4)
        histod[i] = 0.0
        histou[i] = histod[i]
        if i > 0:
            if avg1[i] > avg1[i - 1]:
                histou[i] += 1
            if avg1[i] < avg1[i - 1]:
                histod[i] -= 1
            if avg2[i] > avg2[i - 1]:
                histou[i] += 1
            if avg2[i] < avg2[i - 1]:
                histod[i] -= 1
            if avg3[i] > avg3[i - 1]:
                histou[i] += 1
            if avg3[i] < avg3[i - 1]:
                histod[i] -= 1
            if avg4[i] > avg4[i - 1]:
                histou[i] += 1
            if avg4[i] < avg4[i - 1]:
                histod[i] -= 1
            if avg5[i] > avg5[i - 1]:
                histou[i] += 1
            if avg5[i] < avg5[i - 1]:
                histod[i] -= 1
    return rates_total

def iSmooth(price, length, phase, i, instance=0):
    _indP = _int(MathMod(i - 1, 11))
    _indC = _int(MathMod(i, 11))
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
    _indF = _int(MathMod(i - MathMin(i, 10), 11))
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
    if del1 > 0:
        workSmooth[_indC][_inst + 5] = price
    else:
        workSmooth[_indC][_inst + 5] = price - (Kv * del1)
    if del2 < 0:
        workSmooth[_indC][_inst + 6] = price
    else:
        workSmooth[_indC][_inst + 6] = price - (Kv * del2)
    corr = (MathMax(MathMin(phase, 100), -100) / 100.0) + 1.5
    beta = _fdiv(0.45 * (length - 1), (0.45 * (length - 1)) + 2)
    alpha = MathPow(beta, pow2)
    workSmooth[_indC][_inst + 0] = price + (alpha * (workSmooth[_indP][_inst + 0] - price))
    workSmooth[_indC][_inst + 1] = ((price - workSmooth[_indC][_inst + 0]) * (1 - beta)) + (beta * workSmooth[_indP][_inst + 1])
    workSmooth[_indC][_inst + 2] = workSmooth[_indC][_inst + 0] + (corr * workSmooth[_indC][_inst + 1])
    workSmooth[_indC][_inst + 3] = ((workSmooth[_indC][_inst + 2] - workSmooth[_indP][_inst + 4]) * MathPow(1 - alpha, 2)) + (MathPow(alpha, 2) * workSmooth[_indP][_inst + 3])
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


class MultiJMASlopes2(_MQL5Indicator):
    name = 'Multi JMA slopes 2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod1': 8,  # Period 1
        'inpPeriod2': 11,  # Period 2
        'inpPeriod3': 14,  # Period 3
        'inpPeriod4': 17,  # Period 4
        'inpPeriod5': 20,  # Period 5
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

