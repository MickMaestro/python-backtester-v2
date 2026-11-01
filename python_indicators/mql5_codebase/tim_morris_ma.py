"""Tim Morris MA — converted from MQL5: MQL5 Indicators/Tim Morris MA/Tim Morris MA.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Tim Morris MA'}, 'levels': [], 'description': [], 'name': 'Tim Morris MA', 'source': 'MQL5 Indicators/Tim Morris MA/Tim Morris MA.mq5', 'folder': 'Tim Morris MA', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': 'Inverse of driving coefficient (length)', 'sinput': False}, {'mql': 'Damping', 'py': 'Damping', 'param': 'Damping', 'type': 'double', 'default': 5.0, 'label': 'Smoothing percent', 'sinput': False}, {'mql': 'Noise', 'py': 'Noise', 'param': 'Noise', 'type': 'double', 'default': 30.0, 'label': 'Noise (in pips)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 10)  # Inverse of driving coefficient (length)
Damping = _input('Damping', 5.0)  # Smoothing percent
Noise = _input('Noise', 30.0)  # Noise (in pips)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
wrkTm = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Tim Morris MA (' + _str(Length) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    _noise = Noise * Point() * MathPow(10, _imod(Digits(), 2))
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        val[i] = iTmSmooth(getPrice(inpPrice, open, close, high, low, i, rates_total), Damping, _noise, Length, i, rates_total)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

def iTmSmooth(price, damping, noise, length, i, bars):
    if ArrayRange(wrkTm, 0) != bars:
        ArrayResize(wrkTm, bars)
    if length <= 1:
        return price
    wrkTm[i][0] = price
    y1 = (wrkTm[i - 1][1] if (i > 0) else 0)
    y2 = (wrkTm[i - 1][2] if (i > 0) else 0)
    err = _fdiv(wrkTm[i][0] - (2.0 * y1) + y2, noise)
    drv = MathMax(MathMin((_fdiv(1.0, length) * err * err) + (_fdiv(1.0, length) * MathAbs(err)), 0.5), 0.0)
    dmp = MathMax(MathMin(_fdiv(_fdiv(1.0, length) * MathAbs(y1 - y2), noise) + (damping / 100.0), 1.0), 0.0)
    tmAvg = y1 + (noise * err * drv) + ((y1 - y2) * (1.0 - dmp))
    wrkTm[i][1] = tmAvg
    wrkTm[i][2] = y1
    return tmAvg

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


class TimMorrisMA(_MQL5Indicator):
    name = 'Tim Morris MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # Inverse of driving coefficient (length)
        'Damping': 5.0,  # Smoothing percent
        'Noise': 30.0,  # Noise (in pips)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

