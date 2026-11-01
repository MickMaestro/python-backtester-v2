"""Hurst exponent — converted from MQL5: MQL5 Indicators/Hurst Exponent/Hurst exponent.mq5

Hurst exponent
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16760576]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Hurst exponent'}, 'levels': [], 'description': ['Hurst exponent'], 'name': 'Hurst exponent', 'source': 'MQL5 Indicators/Hurst Exponent/Hurst exponent.mq5', 'folder': 'Hurst Exponent', 'inputs': [{'mql': 'inpHurstPeriod', 'py': 'inpHurstPeriod', 'param': 'inpHurstPeriod', 'type': 'int', 'default': 30, 'label': 'Hurst exponent period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpHurstPeriod = _input('inpHurstPeriod', 30)  # Hurst exponent period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
prices = Arr(0, 0.0)
x = Arr(0, 0.0)
y = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hurst exponent (' + _str(inpHurstPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArraySize(x) != inpHurstPeriod:
        ArrayResize(x, inpHurstPeriod)
        ArrayInitialize(x, 0)
        ArraySetAsSeries(x, True)
        ArrayResize(y, inpHurstPeriod)
        ArrayInitialize(y, 0)
        ArraySetAsSeries(y, True)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        mean = iSma(prices[i], inpHurstPeriod, i, rates_total)
        sums = 0.0
        k = 0
        while k < inpHurstPeriod and (i - k) >= 0:
            x[k] = prices[i - k] - mean
            sums += x[k] * x[k]
            k += 1
        maxY = x[0]
        minY = x[0]
        y[0] = x[0]
        for k in range(1, inpHurstPeriod):
            y[k] = y[k - 1] + x[k]
            maxY = MathMax(y[k], maxY)
            minY = MathMin(y[k], minY)
        iValue = 0.0
        if sums != 0:
            iValue = _fdiv(maxY - minY, 1.253314 * MathSqrt(sums / inpHurstPeriod))
        hurst = 0.0
        if iValue > 0:
            hurst = _fdiv(MathLog(iValue), MathLog(inpHurstPeriod))
        val[i] = hurst
        i += 1
    return i

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))

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


class HurstExponent(_MQL5Indicator):
    name = 'Hurst exponent'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpHurstPeriod': 30,  # Hurst exponent period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

