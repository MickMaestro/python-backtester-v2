"""RSI bands — converted from MQL5: MQL5 Indicators/RSI bands/RSI bands.mq5

RSI bands
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [3329330], 2: [17919], 3: [3329330], 4: [17919]}, 'widths': {}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'Dampening overbought', 2: 'Dampening oversold', 3: 'Overbought', 4: 'Oversold'}, 'levels': [], 'description': ['RSI bands'], 'name': 'RSI bands', 'source': 'MQL5 Indicators/RSI bands/RSI bands.mq5', 'folder': 'RSI bands', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpDampening', 'py': 'inpDampening', 'param': 'inpDampening', 'type': 'double', 'default': 0.5, 'label': 'Dampening', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpOverbought', 'py': 'inpOverbought', 'param': 'inpOverbought', 'type': 'double', 'default': 70.0, 'label': 'Overbought level', 'sinput': False}, {'mql': 'inpOversold', 'py': 'inpOversold', 'param': 'inpOversold', 'type': 'double', 'default': 30.0, 'label': 'Oversold level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpDampening = _input('inpDampening', 0.5)  # Dampening
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpOverbought = _input('inpOverbought', 70.0)  # Overbought level
inpOversold = _input('inpOversold', 30.0)  # Oversold level
valud = Arr(0, 0.0)
valdd = Arr(0, 0.0)
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
rsiBandWork = Arr(0, 0.0, dims=(16,))

def OnInit():
    SetIndexBuffer(0, valud, INDICATOR_DATA)
    SetIndexBuffer(1, valdd, INDICATOR_DATA)
    SetIndexBuffer(2, valu, INDICATOR_DATA)
    SetIndexBuffer(3, vald, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI bands(' + _str(inpRsiPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        valu[i] = rsiBand(price, inpRsiPeriod, inpOverbought, i, 0.0, rates_total, 0)
        vald[i] = rsiBand(price, inpRsiPeriod, inpOversold, i, 0.0, rates_total, 1)
        valud[i] = (rsiBand(price, inpRsiPeriod, inpOverbought, i, inpDampening, rates_total, 2) if (inpDampening != 0) else EMPTY_VALUE)
        valdd[i] = (rsiBand(price, inpRsiPeriod, inpOversold, i, inpDampening, rates_total, 3) if (inpDampening != 0) else EMPTY_VALUE)
        i += 1
    return i

def rsiBand(price, rsiPeriod, targetLevel, i, dampening, bars, instance=0):
    if ArrayRange(rsiBandWork, 0) != bars:
        ArrayResize(rsiBandWork, bars)
    instance *= 4
    rsiBandWork[i][instance + 0] = price
    pprice = (rsiBandWork[i - 1][instance + 0] if (i > 0) else price)
    cprice = rsiBandWork[i][instance + 0]
    diff = cprice - pprice
    w = (diff if (diff > 0) else 0)
    s = ((-diff) if (diff < 0) else 0)
    p = (rsiBandWork[i - 1][instance + 1] if (i > 0) else 0)
    n = (rsiBandWork[i - 1][instance + 2] if (i > 0) else 0)
    prev = (rsiBandWork[i - 1][instance + 3] if (i > 0) else 0)
    match = 0.0
    if prev > pprice:
        match = pprice + p - (p * rsiPeriod) - _fdiv(((n * rsiPeriod) - n) * targetLevel, targetLevel - 100.0)
    else:
        match = pprice - n - p + (n * rsiPeriod) + (p * rsiPeriod) + _fdiv(100.0 * p, targetLevel) - _fdiv(100.0 * p * rsiPeriod, targetLevel)
    if dampening != 0:
        if (match - cprice) > ((dampening / 100) * cprice):
            match = cprice * (1 + (dampening / 100))
        elif (match - cprice) < (((-dampening) / 100) * cprice):
            match = cprice * (1 - (dampening / 100))
    rsiBandWork[i][instance + 1] = _fdiv(((rsiPeriod - 1) * p) + w, rsiPeriod)
    rsiBandWork[i][instance + 2] = _fdiv(((rsiPeriod - 1) * n) + s, rsiPeriod)
    rsiBandWork[i][instance + 3] = match
    return match

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


class RSIBands(_MQL5Indicator):
    name = 'RSI bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
        'inpDampening': 0.5,  # Dampening
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpOverbought': 70.0,  # Overbought level
        'inpOversold': 30.0,  # Oversold level
    }

