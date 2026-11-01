"""Fractal dimension Jurik — converted from MQL5: MQL5 Indicators/Fractal Dimension - Jurik/Fractal dimension Jurik.mq5

Fractal dimension Jurik
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16760576, 8036607]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Fractal dimension index'}, 'levels': [], 'description': ['Fractal dimension Jurik'], 'name': 'Fractal dimension Jurik', 'source': 'MQL5 Indicators/Fractal Dimension - Jurik/Fractal dimension Jurik.mq5', 'folder': 'Fractal Dimension - Jurik', 'inputs': [{'mql': 'inpFdiPeriod', 'py': 'inpFdiPeriod', 'param': 'inpFdiPeriod', 'type': 'int', 'default': 30, 'label': 'Fractal dimension period', 'sinput': False}, {'mql': 'inpFdiCount', 'py': 'inpFdiCount', 'param': 'inpFdiCount', 'type': 'int', 'default': 5, 'label': 'Fractal dimension count', 'sinput': False}, {'mql': 'inpFdiSmooth', 'py': 'inpFdiSmooth', 'param': 'inpFdiSmooth', 'type': 'int', 'default': 5, 'label': 'Fractal dimension smoth', 'sinput': False}, {'mql': 'inpFdiThreshold', 'py': 'inpFdiThreshold', 'param': 'inpFdiThreshold', 'type': 'double', 'default': 1.5, 'label': 'Fractal dimension threshold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFdiPeriod = _input('inpFdiPeriod', 30)  # Fractal dimension period
inpFdiCount = _input('inpFdiCount', 5)  # Fractal dimension count
inpFdiSmooth = _input('inpFdiSmooth', 5)  # Fractal dimension smoth
inpFdiThreshold = _input('inpFdiThreshold', 1.5)  # Fractal dimension threshold
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)
smlRange = Arr(0, 0.0)
smlSumm = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, smlRange, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, smlSumm, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpFdiThreshold)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fractal dimension (Jurik) (' + _str(inpFdiPeriod) + ',' + _str(inpFdiCount) + ',' + _str(inpFdiSmooth) + ',' + _str(inpFdiThreshold) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        val[i] = iSma(iFD(close, high, low, inpFdiPeriod, inpFdiCount, i), inpFdiSmooth, i, rates_total)
        valc[i] = (1 if (val[i] > inpFdiThreshold) else 2)
        i += 1
    return i

def iFD(close, high, low, size, count, i):
    bigRange = 0.0
    window1 = size * (count - 1)
    window2 = size * count
    nLog = MathLog(count)
    smlRange[i] = ((MathMax(close[i - size], maxHigh(high, size, i)) - MathMin(close[i - size], minLow(low, size, i))) if (i >= size) else 0)
    smlSumm[i] = ((smlSumm[i - 1] + smlRange[i]) if (i > 0) else 0)
    if i > window1:
        bigRange = ((MathMax(close[i - window2], maxHigh(high, window2, i)) - MathMin(close[i - window2], minLow(low, window2, i))) if (i >= window2) else 0)
        smlSumm[i] -= smlRange[i - window1]
        return 2 - _fdiv(MathLog(_fdiv(bigRange, _fdiv(smlSumm[i], window1))), nLog)
    else:
        return 1.5

def minLow(low, period, shift):
    minValue = low[shift]
    i = 1
    while i < period and (shift - i) > -0:
        minValue = MathMin(minValue, low[shift - i])
        i += 1
    return minValue

def maxHigh(high, period, shift):
    maxValue = high[shift]
    i = 1
    while i < period and (shift - i) >= 0:
        maxValue = MathMax(maxValue, high[shift - i])
        i += 1
    return maxValue

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalDimensionJurik(_MQL5Indicator):
    name = 'Fractal dimension Jurik'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFdiPeriod': 30,  # Fractal dimension period
        'inpFdiCount': 5,  # Fractal dimension count
        'inpFdiSmooth': 5,  # Fractal dimension smoth
        'inpFdiThreshold': 1.5,  # Fractal dimension threshold
    }

