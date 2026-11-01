"""Vertical Horizontal Filter VHF — converted from MQL5: MQL5 Indicators/Vertical Horizontal Filter/Vertical Horizontal Filter VHF.mq5

Vertical Horizontal Filter (VHF)
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Vertical Horizontal Filter (VHF)'], 'name': 'Vertical Horizontal Filter VHF', 'source': 'MQL5 Indicators/Vertical Horizontal Filter/Vertical Horizontal Filter VHF.mq5', 'folder': 'Vertical Horizontal Filter', 'inputs': [{'mql': 'inpVhfPeriod', 'py': 'inpVhfPeriod', 'param': 'inpVhfPeriod', 'type': 'int', 'default': 28, 'label': 'VHF period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpVhfPeriod = _input('inpVhfPeriod', 28)  # VHF period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Vertical Horizontal Filter (' + _str(inpVhfPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        start = MathMax(i - inpVhfPeriod + 1, 0)
        noise = 0.0
        k = 0
        while k < inpVhfPeriod and (i - k - 1) >= 0:
            noise += MathAbs(prices[i - k] - prices[i - k - 1])
            k += 1
        HCP = prices[ArrayMaximum(prices, start, inpVhfPeriod)]
        LCP = prices[ArrayMinimum(prices, start, inpVhfPeriod)]
        val[i] = (_fdiv(HCP - LCP, noise) if (noise != 0) else 0)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
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


class VerticalHorizontalFilterVHF(_MQL5Indicator):
    name = 'Vertical Horizontal Filter VHF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpVhfPeriod': 28,  # VHF period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

