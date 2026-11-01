"""WPO — converted from MQL5: MQL5 Indicators/Wave period oscillator/WPO.mq5

Wave period oscillator
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Wave period oscillator'], 'name': 'WPO', 'source': 'MQL5 Indicators/Wave period oscillator/WPO.mq5', 'folder': 'Wave period oscillator', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpHlPeriod', 'py': 'inpHlPeriod', 'param': 'inpHlPeriod', 'type': 'int', 'default': 3, 'label': 'Highest price period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpHlPeriod = _input('inpHlPeriod', 3)  # Highest price period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
prices = Arr(0, 0.0)
_alpha = 0.0

def OnInit():
    global _alpha
    SetIndexBuffer(0, val)
    SetIndexBuffer(1, prices)
    _alpha = _fdiv(2.0, 1.0 + (inpPeriod if (inpPeriod > 1) else 1))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Wave period oscillator (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max
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
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpHlPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = prices[ArrayMaximum(prices, start, inpHlPeriod - 1)]
        max_ = (prices[i] if (prices[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        _angle = MathArcsin(_fdiv(prices[i], max_))
        _wave = _fdiv(2.0 * M_PI, _angle)
        val[i] = ((val[i - 1] + (_alpha * ((_wave if (prices[i] > prices[i - 1]) else (-_wave)) - val[i - 1]))) if (i > 0) else 0)
        i += 1
    return i

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WPO(_MQL5Indicator):
    name = 'WPO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpHlPeriod': 3,  # Highest price period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

