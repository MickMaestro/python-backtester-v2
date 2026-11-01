"""Fractal dimension index — converted from MQL5: MQL5 Indicators/Fractal dimension index (Sevcik_Matulich)/Fractal dimension index.mq5

Fractal dimension index Sevcik/Matulich
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16760576, 8036607]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Fractal dimension index'}, 'levels': [], 'description': ['Fractal dimension index Sevcik/Matulich'], 'name': 'Fractal dimension index', 'source': 'MQL5 Indicators/Fractal dimension index (Sevcik_Matulich)/Fractal dimension index.mq5', 'folder': 'Fractal dimension index (Sevcik_Matulich)', 'inputs': [{'mql': 'inpFdiPeriod', 'py': 'inpFdiPeriod', 'param': 'inpFdiPeriod', 'type': 'int', 'default': 30, 'label': 'Fractal dimension period', 'sinput': False}, {'mql': 'inpFdiThreshold', 'py': 'inpFdiThreshold', 'param': 'inpFdiThreshold', 'type': 'double', 'default': 1.5, 'label': 'Fractal dimension threshold', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFdiPeriod = _input('inpFdiPeriod', 30)  # Fractal dimension period
inpFdiThreshold = _input('inpFdiThreshold', 1.5)  # Fractal dimension threshold
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpFdiThreshold)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fractal dimension index (Sevcik/Matulich) (' + _str(inpFdiPeriod) + ',' + _str(inpFdiThreshold) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    dx2 = MathPow(1.0 / inpFdiPeriod, 2)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        _start = MathMax(i - inpFdiPeriod + 1, 0)
        priceMax = prices[ArrayMaximum(prices, _start, inpFdiPeriod)]
        priceMin = prices[ArrayMinimum(prices, _start, inpFdiPeriod)]
        length = 0.0
        if priceMax == priceMin:
            length = 1.0
        else:
            pdi = priceMax - priceMin
            k = 1
            while k <= inpFdiPeriod and (i - k) >= 0:
                dy = _fdiv(prices[i - k] - prices[i - k + 1], pdi)
                length += MathSqrt(dx2 + (dy * dy))
                k += 1
        val[i] = 1 + _fdiv(MathLog(length) + MathLog(2), MathLog(2 * inpFdiPeriod))
        valc[i] = (1 if (val[i] > inpFdiThreshold) else 2)
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


class FractalDimensionIndex(_MQL5Indicator):
    name = 'Fractal dimension index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFdiPeriod': 30,  # Fractal dimension period
        'inpFdiThreshold': 1.5,  # Fractal dimension threshold
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

