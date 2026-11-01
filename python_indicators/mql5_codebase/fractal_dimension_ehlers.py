"""Fractal dimension Ehlers — converted from MQL5: MQL5 Indicators/Fractal dimension - Ehlers/Fractal dimension Ehlers.mq5

Fractal dimension Ehlers
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16760576, 8036607]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Fractal dimension'}, 'levels': [], 'description': ['Fractal dimension Ehlers'], 'name': 'Fractal dimension Ehlers', 'source': 'MQL5 Indicators/Fractal dimension - Ehlers/Fractal dimension Ehlers.mq5', 'folder': 'Fractal dimension - Ehlers', 'inputs': [{'mql': 'inpFdiPeriod', 'py': 'inpFdiPeriod', 'param': 'inpFdiPeriod', 'type': 'int', 'default': 30, 'label': 'Fractal dimension period', 'sinput': False}, {'mql': 'inpFdiThreshold', 'py': 'inpFdiThreshold', 'param': 'inpFdiThreshold', 'type': 'double', 'default': 1.4, 'label': 'Fractal dimension threshold', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFdiPeriod = _input('inpFdiPeriod', 30)  # Fractal dimension period
inpFdiThreshold = _input('inpFdiThreshold', 1.4)  # Fractal dimension threshold
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
wrk = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpFdiThreshold)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fractal dimension (Ehlers) (' + _str(inpFdiPeriod) + ',' + _str(inpFdiThreshold) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(wrk, 0) != rates_total:
        ArrayResize(wrk, rates_total)
    log2 = MathLog(2.0)
    _fullSize = MathMax(inpFdiPeriod, 2)
    if MathMod(_fullSize, 2) > 0:
        _fullSize += 1
    _halfSize = _idiv(_fullSize, 2)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        wrk[i][0] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        wrk[i][1] = (((wrk[i][0] + (2.0 * wrk[i - 1][0]) + 2.0 + wrk[i - 2][0] + wrk[i - 3][0]) / 6.0) if (i > 2) else wrk[i][0])
        hh = wrk[i][1]
        ll = wrk[i][1]
        n = 1
        while n < _fullSize and (i - n) >= 0:
            hh = MathMax(hh, wrk[i - n][1])
            ll = MathMin(ll, wrk[i - n][1])
            n += 1
        n3 = _fdiv(hh - ll, _fullSize)
        hh = wrk[i][1]
        ll = wrk[i][1]
        n = 1
        while n < _halfSize and (i - n) >= 0:
            hh = MathMax(hh, wrk[i - n][1])
            ll = MathMin(ll, wrk[i - n][1])
            n += 1
        n1 = _fdiv(hh - ll, _halfSize)
        hh = (wrk[i - _halfSize][1] if (i >= _halfSize) else wrk[i][1])
        ll = (wrk[i - _halfSize][1] if (i >= _halfSize) else wrk[i][1])
        n = _halfSize + 1
        while n < _fullSize and (i - n) >= 0:
            hh = MathMax(hh, wrk[i - n][1])
            ll = MathMin(ll, wrk[i - n][1])
            n += 1
        n2 = _fdiv(hh - ll, _halfSize)
        if (n1 > 0 and n2 > 0) and n3 > 0:
            wrk[i][2] = ((0.5 * (_fdiv(MathLog(n1 + n2) - MathLog(n3), log2) + val[i - 1])) if (i > 0) else _fdiv(MathLog(n1 + n2) - MathLog(n3), log2))
        else:
            wrk[i][2] = (wrk[i - 1][2] if (i > 0) else 0)
        avg = wrk[i][2]
        n = 1
        while n < 20 and (i - n) >= 0:
            avg += wrk[i - n][2]
            n += 1
        avg = avg / 20
        val[i] = avg
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


class FractalDimensionEhlers(_MQL5Indicator):
    name = 'Fractal dimension Ehlers'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFdiPeriod': 30,  # Fractal dimension period
        'inpFdiThreshold': 1.4,  # Fractal dimension threshold
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

