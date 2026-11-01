"""SHO — converted from MQL5: MQL5 Indicators/Simple harmonic oscillator/SHO.mq5

Simple Harmonic Oscillator
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Simple Harmonic Oscillator'], 'name': 'SHO', 'source': 'MQL5 Indicators/Simple harmonic oscillator/SHO.mq5', 'folder': 'Simple harmonic oscillator', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
work1 = Arr(0, 0.0)
work2 = Arr(0, 0.0)
work3 = Arr(0, 0.0)
prices = Arr(0, 0.0)
_alpha = 0.0

def OnInit():
    global _alpha
    SetIndexBuffer(0, val)
    SetIndexBuffer(1, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, work1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, work2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, work3, INDICATOR_CALCULATIONS)
    _alpha = _fdiv(2.0, 1.0 + (inpPeriod if (inpPeriod > 1) else 1))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Simple Harmonic Oscillator (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

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
        if i > 1:
            _vt = prices[i] - prices[i - 1]
            _vy = prices[i - 1] - prices[i - 2]
            _acceleration = _vt - _vy
            work1[i] = work1[i - 1] + (_alpha * (_acceleration - work1[i - 1]))
            _t = 2.0 * M_PI * MathSqrt(MathAbs(_fdiv(_vt, work1[i])))
            work2[i] = work2[i - 1] + (_alpha * ((_t if (prices[i] > prices[i - 1]) else (-_t)) - work2[i - 1]))
            work3[i] = work3[i - 1] + (_alpha * (_t - work3[i - 1]))
            val[i] = _fdiv(100 * work2[i], work3[i])
        else:
            work3[i] = 0.0
            work2[i] = work3[i]
            work1[i] = work2[i]
            val[i] = work1[i]
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SHO(_MQL5Indicator):
    name = 'SHO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

