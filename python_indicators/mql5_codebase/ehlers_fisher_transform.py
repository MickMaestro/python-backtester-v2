"""Ehlers fisher transform — converted from MQL5: MQL5 Indicators/Ehlers Fisher transform/Ehlers fisher transform.mq5

.
Ehlers fisher transform
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 32768, 3937500]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'ft'}, 'levels': [], 'description': ['.', 'Ehlers fisher transform'], 'name': 'Ehlers fisher transform', 'source': 'MQL5 Indicators/Ehlers Fisher transform/Ehlers fisher transform.mq5', 'folder': 'Ehlers Fisher transform', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)
work = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, work, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ehlers fisher transform (' + _str(inpPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            prices[i] = close[i]
        elif _sw1 == PRICE_OPEN:
            prices[i] = open[i]
        elif _sw1 == PRICE_HIGH:
            prices[i] = high[i]
        elif _sw1 == PRICE_LOW:
            prices[i] = low[i]
        elif _sw1 == PRICE_MEDIAN:
            prices[i] = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            prices[i] = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            prices[i] = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            prices[i] = 0.0
        _start = ((i - inpPeriod + 1) if (i > inpPeriod) else 0)
        _max = prices[ArrayMaximum(prices, _start, inpPeriod)]
        _min = prices[ArrayMinimum(prices, _start, inpPeriod)]
        work[i] = ((((0.333 * 2.0 * (_fdiv(prices[i] - _min, _max - _min) - 0.5)) + (0.667 * work[i - 1])) if (_max != _min) else 0) if (i > 0) else 0)
        work[i] = (0.999 if (work[i] > 0.999) else -0.999 if (work[i] < -0.999) else work[i])
        val[i] = (((0.5 * MathLog(_fdiv(1.0 + work[i], 1.0 - work[i]))) + (0.5 * val[i - 1])) if (i > 0) else 0)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersFisherTransform(_MQL5Indicator):
    name = 'Ehlers fisher transform'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

