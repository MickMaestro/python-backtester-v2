"""T3 Stochastic Momentum Index — converted from MQL5: MQL5 Indicators/T3 Stochastic Momentum Index/T3 Stochastic Momentum Index.mq5

T3 Stochastc Momentum Index
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [11119017, 16760576, 8036607], 2: [11119017]}, 'widths': {1: 2, 2: 1}, 'styles': {}, 'labels': {1: 'Smi', 2: 'Smi signal'}, 'levels': [40.0, -40.0], 'description': ['T3 Stochastc Momentum Index'], 'name': 'T3 Stochastic Momentum Index', 'source': 'MQL5 Indicators/T3 Stochastic Momentum Index/T3 Stochastic Momentum Index.mq5', 'folder': 'T3 Stochastic Momentum Index', 'inputs': [{'mql': 'inpLength', 'py': 'inpLength', 'param': 'inpLength', 'type': 'int', 'default': 13, 'label': 'Length', 'sinput': False}, {'mql': 'inpSmooth1', 'py': 'inpSmooth1', 'param': 'inpSmooth1', 'type': 'int', 'default': 25, 'label': 'Smooth period 1', 'sinput': False}, {'mql': 'inpSmooth2', 'py': 'inpSmooth2', 'param': 'inpSmooth2', 'type': 'int', 'default': 2, 'label': 'Smooth period 2', 'sinput': False}, {'mql': 'inpSignal', 'py': 'inpSignal', 'param': 'inpSignal', 'type': 'int', 'default': 5, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpT3Hot', 'py': 'inpT3Hot', 'param': 'inpT3Hot', 'type': 'double', 'default': 0.4, 'label': 'T3 hot', 'sinput': False}, {'mql': 'inpT3Original', 'py': 'inpT3Original', 'param': 'inpT3Original', 'type': 'bool', 'default': False, 'label': 'T3 original Tim Tillson calculation', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpLength = _input('inpLength', 13)  # Length
inpSmooth1 = _input('inpSmooth1', 25)  # Smooth period 1
inpSmooth2 = _input('inpSmooth2', 2)  # Smooth period 2
inpSignal = _input('inpSignal', 5)  # Signal period
inpT3Hot = _input('inpT3Hot', 0.4)  # T3 hot
inpT3Original = _input('inpT3Original', False)  # T3 original Tim Tillson calculation
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
workT3 = Arr(0, 0.0, dims=(30,))
workT3Coeffs = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, signal, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'T3 SMI (' + _str(inpLength) + ',' + _str(inpSmooth1) + ',' + _str(inpSmooth2) + ',' + _str(inpSignal) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _start = MathMax(i - inpLength + 1, 0)
        hh = high[ArrayMaximum(high, _start, inpLength)]
        ll = low[ArrayMinimum(low, _start, inpLength)]
        pr = getPrice(inpPrice, open, close, high, low, i, rates_total)
        ema10 = pr - (0.5 * (hh + ll))
        ema11 = iT3(ema10, inpSmooth1, inpT3Hot, inpT3Original, i, rates_total, 0)
        ema12 = iT3(ema11, inpSmooth2, inpT3Hot, inpT3Original, i, rates_total, 1)
        ema20 = hh - ll
        ema21 = iT3(ema20, inpSmooth1, inpT3Hot, inpT3Original, i, rates_total, 2)
        ema22 = iT3(ema21, inpSmooth2, inpT3Hot, inpT3Original, i, rates_total, 3)
        val[i] = (_fdiv(100.0 * ema12, 0.5 * ema22) if (ema22 != 0) else 0)
        signal[i] = iT3(val[i], inpSignal, inpT3Hot, inpT3Original, i, rates_total, 4)
        valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i

def iT3(price, period, hot, original, r, bars, instanceNo=0):
    if ArrayRange(workT3, 0) != bars:
        ArrayResize(workT3, bars)
    if ArrayRange(workT3Coeffs, 0) < (instanceNo + 1):
        ArrayResize(workT3Coeffs, instanceNo + 1)
    if workT3Coeffs[instanceNo][0] != period:
        workT3Coeffs[instanceNo][0] = period
        workT3Coeffs[instanceNo][1] = (-hot) * hot * hot
        workT3Coeffs[instanceNo][2] = (3 * hot * hot) + (3 * hot * hot * hot)
        workT3Coeffs[instanceNo][3] = (-6 * hot * hot) - (3 * hot) - (3 * hot * hot * hot)
        workT3Coeffs[instanceNo][4] = 1 + (3 * hot) + (hot * hot * hot) + (3 * hot * hot)
        if original:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 1.0 + period)
        else:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0))
    buffer = instanceNo * 6
    for k in range(0, 6):
        workT3[r][k + buffer] = (workT3[r - 1][k + buffer] if (r > 0) else price)
    if r > 0 and period > 1:
        workT3[r][0 + buffer] = workT3[r - 1][0 + buffer] + (workT3Coeffs[instanceNo][5] * (price - workT3[r - 1][0 + buffer]))
        workT3[r][1 + buffer] = workT3[r - 1][1 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][0 + buffer] - workT3[r - 1][1 + buffer]))
        workT3[r][2 + buffer] = workT3[r - 1][2 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][1 + buffer] - workT3[r - 1][2 + buffer]))
        workT3[r][3 + buffer] = workT3[r - 1][3 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][2 + buffer] - workT3[r - 1][3 + buffer]))
        workT3[r][4 + buffer] = workT3[r - 1][4 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][3 + buffer] - workT3[r - 1][4 + buffer]))
        workT3[r][5 + buffer] = workT3[r - 1][5 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][4 + buffer] - workT3[r - 1][5 + buffer]))
    return (workT3Coeffs[instanceNo][1] * workT3[r][5 + buffer]) + (workT3Coeffs[instanceNo][2] * workT3[r][4 + buffer]) + (workT3Coeffs[instanceNo][3] * workT3[r][3 + buffer]) + (workT3Coeffs[instanceNo][4] * workT3[r][2 + buffer])

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


class T3StochasticMomentumIndex(_MQL5Indicator):
    name = 'T3 Stochastic Momentum Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpLength': 13,  # Length
        'inpSmooth1': 25,  # Smooth period 1
        'inpSmooth2': 2,  # Smooth period 2
        'inpSignal': 5,  # Signal period
        'inpT3Hot': 0.4,  # T3 hot
        'inpT3Original': False,  # T3 original Tim Tillson calculation
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

