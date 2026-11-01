"""Step chart - cci — converted from MQL5: MQL5 Indicators/Step chart of CCI/Step chart - cci.mq5

Step chart of CCI
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 11}, 'colors': {1: [11119017], 2: [11119017, 16748574, 6333684]}, 'widths': {2: 2}, 'styles': {1: 2}, 'labels': {1: 'Step chart of CCI', 2: 'Step chart'}, 'levels': [], 'description': ['Step chart of CCI'], 'name': 'Step chart - cci', 'source': 'MQL5 Indicators/Step chart of CCI/Step chart - cci.mq5', 'folder': 'Step chart of CCI', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'inpStepSize', 'py': 'inpStepSize', 'param': 'inpStepSize', 'type': 'double', 'default': 5.0, 'label': 'Step size (in CCI units)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # CCI period
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # Price
inpStepSize = _input('inpStepSize', 5.0)  # Step size (in CCI units)
barh = Arr(0, 0.0)
barl = Arr(0, 0.0)
barc = Arr(0, 0.0)
val = Arr(0, 0.0)
workCci = Arr(0, 0.0, dims=(1,))
_stepChartWork = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, barh, INDICATOR_DATA)
    SetIndexBuffer(2, barl, INDICATOR_DATA)
    SetIndexBuffer(3, barc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Step chart of (' + _str(inpPeriod) + ' CCI)')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iCci(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, i, rates_total)
        rbarh = Box(0.0)
        rbarl = Box(0.0)
        rtrend = Box(0.0)
        iStepChart(val[i], inpStepSize, rbarh, rbarl, rtrend, i, rates_total)
        barh[i] = rbarh.v
        barl[i] = ((rbarh.v - 1) if (rbarh.v == rbarl.v) else rbarl.v)
        barc[i] = (1 if (rtrend.v == 1) else 2)
        i += 1
    return i

def iCci(price, period, i, bars, instanceNo=0):
    if ArrayRange(workCci, 0) != bars:
        ArrayResize(workCci, bars)
    workCci[i][instanceNo + 0] = price
    avg = 0.0
    k = 0
    while k < period and (i - k) >= 0:
        avg += workCci[i - k][instanceNo]
        k += 1
    avg = _fdiv(avg, period)
    dev = 0.0
    k = 0
    while k < period and (i - k) >= 0:
        dev += MathAbs(workCci[i - k][instanceNo] - avg)
        k += 1
    dev = _fdiv(dev, period)
    cci = (_fdiv(price - avg, 0.015 * dev) if (dev != 0) else 0)
    return cci

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


class StepChartCci(_MQL5Indicator):
    name = 'Step chart - cci'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # CCI period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'inpStepSize': 5.0,  # Step size (in CCI units)
    }

