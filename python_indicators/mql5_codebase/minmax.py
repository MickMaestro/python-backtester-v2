"""MinMax — converted from MQL5: MQL5 Indicators/MinMax indicator/MinMax.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 8, 2: 8, 3: 8}, 'colors': {1: [11119017, 7451452, 17919], 2: [11119017, 7451452, 17919], 3: [11119017, 7451452, 17919]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'MinMax', 2: 'MinMax', 3: 'Midle'}, 'levels': [], 'description': [], 'name': 'MinMax', 'source': 'MQL5 Indicators/MinMax indicator/MinMax.mq5', 'folder': 'MinMax indicator', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 25, 'label': 'MinMax period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 25)  # MinMax period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
valu = Arr(0, 0.0)
valuc = Arr(0, 0.0)
vald = Arr(0, 0.0)
valdc = Arr(0, 0.0)
valm = Arr(0, 0.0)
valmc = Arr(0, 0.0)
prices = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, valu, INDICATOR_DATA)
    SetIndexBuffer(1, valuc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, vald, INDICATOR_DATA)
    SetIndexBuffer(3, valdc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, valm, INDICATOR_DATA)
    SetIndexBuffer(5, valmc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, prices, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MinMax (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
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
        _start = i - inpPeriod + 1
        if _start < 0:
            _start = 0
        _max = prices[ArrayMaximum(prices, _start, inpPeriod)]
        _min = prices[ArrayMinimum(prices, _start, inpPeriod)]
        valu[i] = _max
        valuc[i] = ((1 if (valu[i] > valu[i - 1]) else 2 if (valu[i] < valu[i - 1]) else valuc[i - 1]) if (i > 0) else 0)
        vald[i] = _min
        valdc[i] = ((1 if (vald[i] > vald[i - 1]) else 2 if (vald[i] < vald[i - 1]) else valdc[i - 1]) if (i > 0) else 0)
        valm[i] = (_min + _max) / 2.0
        valmc[i] = ((1 if (valm[i] > valm[i - 1]) else 2 if (valm[i] < valm[i - 1]) else valmc[i - 1]) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MinMax(_MQL5Indicator):
    name = 'MinMax'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 25,  # MinMax period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

