"""Simple oscillator — converted from MQL5: MQL5 Indicators/Simple oscillator/Simple oscillator.mq5

Simple oscillator - invented by mladen
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [15135718, 15132403], 2: [11119017, 32768, 255]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Trend zone', 2: 'Oscillator'}, 'levels': [], 'description': ['Simple oscillator - invented by mladen'], 'name': 'Simple oscillator', 'source': 'MQL5 Indicators/Simple oscillator/Simple oscillator.mq5', 'folder': 'Simple oscillator', 'inputs': [{'mql': 'inpLength', 'py': 'inpLength', 'param': 'inpLength', 'type': 'int', 'default': 25, 'label': 'Oscillator period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpLength = _input('inpLength', 25)  # Oscillator period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levup = Arr(0, 0.0)
levdn = Arr(0, 0.0)
prices = Arr(0, 0.0)
ª_weight = 0.0

def OnInit():
    global ª_weight
    SetIndexBuffer(0, levup, INDICATOR_DATA)
    SetIndexBuffer(1, levdn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, prices, INDICATOR_CALCULATIONS)
    ª_weight = (inpLength - 1.0) / 2.0
    IndicatorSetString(INDICATOR_SHORTNAME, 'Simple oscillator (' + _str(inpLength) + ')')
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
        _weight = ª_weight
        val[i] = 0.0
        k = 0
        while k < inpLength and i >= k:
            val[i] += prices[i - k] * _weight
            k += 1
            _weight -= 1.0
        levdn[i] = 0.0
        levup[i] = val[i]
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SimpleOscillator(_MQL5Indicator):
    name = 'Simple oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpLength': 25,  # Oscillator period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

