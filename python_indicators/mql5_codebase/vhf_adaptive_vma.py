"""VHF adaptive VMA — converted from MQL5: MQL5 Indicators/VHF adaptive VMA/VHF adaptive VMA.mq5

VHF adaptive VMA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [8421504], 2: [11119017, 9639167, 3329330]}, 'widths': {1: 6, 2: 2}, 'styles': {}, 'labels': {1: 'Shadow', 2: 'VMA'}, 'levels': [], 'description': ['VHF adaptive VMA'], 'name': 'VHF adaptive VMA', 'source': 'MQL5 Indicators/VHF adaptive VMA/VHF adaptive VMA.mq5', 'folder': 'VHF adaptive VMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'VMA period', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 0, 'label': 'VHF period (<=1 for same as VMA period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # VMA period
inpPeriod2 = _input('inpPeriod2', 0)  # VHF period (<=1 for same as VMA period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
vals = Arr(0, 0.0)
vhf1 = Arr(0, 0.0)
vhf2 = Arr(0, 0.0)
_alpha = 0.0
_adpPeriod = 0

def OnInit():
    global _adpPeriod, _alpha
    SetIndexBuffer(0, vals, INDICATOR_DATA)
    SetIndexBuffer(1, val, INDICATOR_DATA)
    SetIndexBuffer(2, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, vhf1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, vhf2, INDICATOR_CALCULATIONS)
    _alpha = _fdiv(2.0, 1.0 + inpPeriod)
    _adpPeriod = (inpPeriod if (inpPeriod2 <= 1) else inpPeriod2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VMA (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _price = getPrice(inpPrice, open, close, high, low, i)
        _vhf = iVhf(_adpPeriod, close, vhf1, vhf2, i)
        val[i] = ((val[i - 1] + (_alpha * _vhf * 2.0 * (_price - val[i - 1]))) if (i > 0) else _price)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        vals[i] = val[i]
    return rates_total

def iVhf(period, price, diff, noise, i):
    diff[i] = (((price[i] - price[i - 1]) if (price[i] > price[i - 1]) else (price[i - 1] - price[i])) if (i > 0) else 0)
    if i >= period:
        noise[i] = noise[i - 1] - diff[i - period] + diff[i]
    else:
        noise[i] = 0.0
        k = 0
        while k < period and (i - k) >= 0:
            noise[i] += diff[i - k]
            k += 1
    start = ((i - period + 1) if (i >= period) else 0)
    HCP = price[ArrayMaximum(price, start, period)]
    LCP = price[ArrayMinimum(price, start, period)]
    return (_fdiv(HCP - LCP, noise[i]) if (noise[i] != 0) else 0)

def getPrice(tprice, open, close, high, low, i):
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


class VHFAdaptiveVMA(_MQL5Indicator):
    name = 'VHF adaptive VMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # VMA period
        'inpPeriod2': 0,  # VHF period (<=1 for same as VMA period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

