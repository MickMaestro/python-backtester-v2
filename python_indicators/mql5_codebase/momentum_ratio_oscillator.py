"""Momentum ratio oscillator — converted from MQL5: MQL5 Indicators/Momentum ratio oscillator/Momentum ratio oscillator.mq5

Momentum ratio oscillator
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1, 'indicator_maximum': 1.1, 'indicator_minimum': -0.1}, 'types': {1: 8}, 'colors': {1: [12632256, 7451452, 36095]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Oscillator'}, 'levels': [1.0, 0.8, 0.2], 'description': ['Momentum ratio oscillator'], 'name': 'Momentum ratio oscillator', 'source': 'MQL5 Indicators/Momentum ratio oscillator/Momentum ratio oscillator.mq5', 'folder': 'Momentum ratio oscillator', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 50, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 50)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ema = Arr(0, 0.0)
emaa = Arr(0, 0.0)
emab = Arr(0, 0.0)
ª_alpha = 0.0

def OnInit():
    global ª_alpha
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ema, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, emaa, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, emab, INDICATOR_CALCULATIONS)
    ª_alpha = _fdiv(2.0, 1.0 * inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Momentum ratio oscillator (' + _str(inpPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        if i > 0:
            ema[i] = ema[i - 1] + (ª_alpha * (_price - ema[i - 1]))
            ratioa = _fdiv(ema[i], ema[i - 1])
            emaa[i] = emaa[i - 1] + (ª_alpha * ((ratioa if (ratioa < 1.0) else 0) - emaa[i - 1]))
            emab[i] = emab[i - 1] + (ª_alpha * ((ratioa if (ratioa > 1.0) else 0) - emab[i - 1]))
            ratiob = _fdiv(ratioa, ratioa + emab[i])
            val[i] = _fdiv(2.0 * ratioa, ratioa + (ratiob * emaa[i])) - 1.0
            valc[i] = (1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1])
        else:
            ema[i] = _price
            valc[i] = 0.0
            val[i] = valc[i]
            emab[i] = val[i]
            emaa[i] = emab[i]
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MomentumRatioOscillator(_MQL5Indicator):
    name = 'Momentum ratio oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 50,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }
    y_range = (-0.1, 1.1)

