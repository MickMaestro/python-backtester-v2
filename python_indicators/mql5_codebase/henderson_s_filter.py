"""Henderson's filter — converted from MQL5: MQL5 Indicators/Henderson's Filter/Henderson's filter.mq5

Henderson's filter
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: "Henderson's filter"}, 'levels': [], 'description': ["Henderson's filter"], 'name': "Henderson's filter", 'source': "MQL5 Indicators/Henderson's Filter/Henderson's filter.mq5", 'folder': "Henderson's Filter", 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
prices = Arr(0, 0.0)
weights = Arr(0, 0.0)
_filterSize = 0
_half = 0
_size = 0

def OnInit():
    global _filterSize, _half, _size
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, prices, INDICATOR_CALCULATIONS)
    _filterSize = MathMax(inpPeriod, 3)
    if MathMod(_filterSize, 2) == 0:
        _filterSize += 1
    ArrayResize(weights, _filterSize)
    m = MathFloor(_filterSize / 2.0)
    _half = _int(m)
    divisor = 8.0 * (m + 2.0) * (((m + 2.0) * (m + 2.0)) - 1.0) * ((4.0 * (m + 2.0) * (m + 2)) - 1.0) * ((4.0 * (m + 2.0) * (m + 2.0)) - 9.0) * ((4.0 * (m + 2.0) * (m + 2.0)) - 25.0)
    for j in range(-_half, _half + 1):
        weights[j + _half] = _fdiv(315.0 * (((m + 1.0) * (m + 1.0)) - (j * j)) * (((m + 2.0) * (m + 2.0)) - (j * j)) * (((m + 3.0) * (m + 3.0)) - (j * j)) * ((3.0 * (m + 2.0) * (m + 2.0)) - (11.0 * (j * j)) - 16.0), divisor)
    _size = ArraySize(weights)
    IndicatorSetString(INDICATOR_SHORTNAME, "Henderson's filter (" + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - _half, 0), rates_total):
        mod = 1.0
        if (rates_total - i - 1) < _half:
            weightTotal = 0.0
            for k in range(_half - (rates_total - i - 1), _size):
                weightTotal += weights[k]
            mod = _fdiv(1.0, weightTotal)
        sum_ = mod * weights[_half] * getPrice(inpPrice, open, close, high, low, i, rates_total)
        j = 1
        while j <= _half:
            if (i - j) >= 0:
                sum_ += mod * weights[_half + j] * getPrice(inpPrice, open, close, high, low, i - j, rates_total)
            if (i + j) < rates_total:
                sum_ += mod * weights[_half - j] * getPrice(inpPrice, open, close, high, low, i + j, rates_total)
            j += 1
        val[i] = sum_
    return rates_total

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


class HendersonSFilter(_MQL5Indicator):
    name = "Henderson's filter"
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 32,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

