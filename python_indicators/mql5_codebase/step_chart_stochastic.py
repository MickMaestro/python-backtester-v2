"""Step chart - stochastic — converted from MQL5: MQL5 Indicators/Step chart of stochastic/Step chart - stochastic.mq5

Step chart of stochastic
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 11}, 'colors': {1: [11119017], 2: [11119017, 16748574, 6333684]}, 'widths': {2: 2}, 'styles': {1: 2}, 'labels': {1: 'Step chart of stochastic', 2: 'Step chart'}, 'levels': [], 'description': ['Step chart of stochastic'], 'name': 'Step chart - stochastic', 'source': 'MQL5 Indicators/Step chart of stochastic/Step chart - stochastic.mq5', 'folder': 'Step chart of stochastic', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpSlowing', 'py': 'inpSlowing', 'param': 'inpSlowing', 'type': 'int', 'default': 3, 'label': 'Stochastic slowing (smoothing) period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpStepSize', 'py': 'inpStepSize', 'param': 'inpStepSize', 'type': 'double', 'default': 5.0, 'label': 'Step size (in stochastic %)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # Stochastic period
inpSlowing = _input('inpSlowing', 3)  # Stochastic slowing (smoothing) period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpStepSize = _input('inpStepSize', 5.0)  # Step size (in stochastic %)
barh = Arr(0, 0.0)
barl = Arr(0, 0.0)
barc = Arr(0, 0.0)
val = Arr(0, 0.0)
workSto = Arr(0, 0.0, dims=(5,))
_stepChartWork = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, barh, INDICATOR_DATA)
    SetIndexBuffer(2, barl, INDICATOR_DATA)
    SetIndexBuffer(3, barc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Step chart of (' + _str(inpPeriod) + ',' + _str(inpSlowing) + ' Stochastic)')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = iStoch(_price, _price, _price, inpPeriod, inpSlowing, i, rates_total)
        rbarh = Box(0.0)
        rbarl = Box(0.0)
        rtrend = Box(0.0)
        iStepChart(val[i], inpStepSize, rbarh, rbarl, rtrend, i, rates_total)
        barh[i] = rbarh.v
        barl[i] = ((rbarh.v - 1) if (rbarh.v == rbarl.v) else rbarl.v)
        barc[i] = (1 if (rtrend.v == 1) else 2)
        i += 1
    return i

def iStoch(priceR, priceH, priceL, period, slowing, i, bars, instanceNo=0):
    if ArrayRange(workSto, 0) != bars:
        ArrayResize(workSto, bars)
    instanceNo *= 5
    workSto[i][0 + instanceNo] = priceH
    workSto[i][1 + instanceNo] = priceL
    workSto[i][2 + instanceNo] = priceR
    workSto[i][3 + instanceNo] = priceH
    workSto[i][4 + instanceNo] = priceL
    k = 1
    while k < period and (i - k) >= 0:
        workSto[i][4 + instanceNo] = MathMin(workSto[i][4 + instanceNo], workSto[i - k][instanceNo + 1])
        workSto[i][3 + instanceNo] = MathMax(workSto[i][3 + instanceNo], workSto[i - k][instanceNo + 0])
        k += 1
    sumlow = 0.0
    sumhigh = 0.0
    k = 0
    while k < slowing and (i - k) >= 0:
        sumlow += workSto[i - k][2 + instanceNo] - workSto[i - k][4 + instanceNo]
        sumhigh += workSto[i - k][3 + instanceNo] - workSto[i - k][4 + instanceNo]
        k += 1
    if sumhigh != 0.0:
        return _fdiv(100.0 * sumlow, sumhigh)
    else:
        return 0.0

def iStepChart(value, stepSize, rbarh, rbarl, rtrend, i, bars, instanceNo=0):
    if ArrayRange(_stepChartWork, 0) != bars:
        ArrayResize(_stepChartWork, bars)
    instanceNo *= 2
    if i == 0:
        rbarl.v = ((MathRound(_fdiv(value, stepSize)) * stepSize) if (stepSize > 0) else value)
        rbarh.v = rbarl.v
        _stepChartWork[i][instanceNo + 0] = rbarh.v
        rtrend.v = 0.0
        _stepChartWork[i][instanceNo + 1] = rtrend.v
    else:
        if MathAbs(value - _stepChartWork[i - 1][instanceNo + 0]) < stepSize:
            _stepChartWork[i][instanceNo + 0] = _stepChartWork[i - 1][instanceNo + 0]
        else:
            _stepChartWork[i][instanceNo + 0] = _stepChartWork[i - 1][instanceNo + 0]
            while MathAbs(value - _stepChartWork[i][instanceNo + 0]) > stepSize:
                if value > _stepChartWork[i][instanceNo + 0]:
                    _stepChartWork[i][instanceNo + 0] += stepSize
                if value < _stepChartWork[i][instanceNo + 0]:
                    _stepChartWork[i][instanceNo + 0] -= stepSize
        _stepChartWork[i][instanceNo + 1] = (1 if (_stepChartWork[i][instanceNo + 0] > _stepChartWork[i - 1][instanceNo + 0]) else -1 if (_stepChartWork[i][instanceNo + 0] < _stepChartWork[i - 1][instanceNo + 0]) else _stepChartWork[i - 1][instanceNo + 1])
        rbarh.v = _stepChartWork[i][instanceNo + 0]
        rbarl.v = _stepChartWork[i - 1][instanceNo + 0]
        rtrend.v = _stepChartWork[i][instanceNo + 1]

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


class StepChartStochastic(_MQL5Indicator):
    name = 'Step chart - stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # Stochastic period
        'inpSlowing': 3,  # Stochastic slowing (smoothing) period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpStepSize': 5.0,  # Step size (in stochastic %)
    }

