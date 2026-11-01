"""Step chart histogram — converted from MQL5: MQL5 Indicators/Step Chart Histogram/Step chart histogram.mq5

Step chart
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1, 'indicator_maximum': 1.0, 'indicator_minimum': 0.0}, 'types': {1: 10}, 'colors': {1: [11119017, 3329330, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Step chart'}, 'levels': [], 'description': ['Step chart'], 'name': 'Step chart histogram', 'source': 'MQL5 Indicators/Step Chart Histogram/Step chart histogram.mq5', 'folder': 'Step Chart Histogram', 'inputs': [{'mql': 'inpStepSize', 'py': 'inpStepSize', 'param': 'inpStepSize', 'type': 'double', 'default': 2.0, 'label': 'Step size (pips)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpStepSize = _input('inpStepSize', 2.0)  # Step size (pips)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
barh = Arr(0, 0.0)
barl = Arr(0, 0.0)
barc = Arr(0, 0.0)
steps = Arr(0, 0.0)
trend = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, barh, INDICATOR_DATA)
    SetIndexBuffer(1, barc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, steps, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, trend, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Step chart (' + _str(inpStepSize) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _stepSize = inpStepSize * Point() * MathPow(10, _imod(Digits(), 2))
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        if i == 0:
            steps[i] = MathRound(_fdiv(_price, _stepSize)) * _stepSize
            trend[i] = 0.0
            i += 1
            continue
        steps[i] = steps[i - 1]
        if MathAbs(_price - steps[i]) < _stepSize:
            steps[i] = steps[i - 1]
        else:
            while MathAbs(_price - steps[i]) > _stepSize:
                if _price > steps[i]:
                    steps[i] = steps[i] + _stepSize
                if _price < steps[i]:
                    steps[i] = steps[i] - _stepSize
        trend[i] = (1 if (steps[i] > steps[i - 1]) else -1 if (steps[i] < steps[i - 1]) else trend[i - 1])
        barh[i] = 1.0
        barc[i] = (1 if (trend[i] == 1) else 2)
        i += 1
    return i

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


class StepChartHistogram(_MQL5Indicator):
    name = 'Step chart histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpStepSize': 2.0,  # Step size (pips)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }
    y_range = (0.0, 1.0)

