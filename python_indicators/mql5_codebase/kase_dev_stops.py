"""Kase dev-stops — converted from MQL5: MQL5 Indicators/Kase DevStops/Kase dev-stops.mq5

Kase dev-stops
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 4}, 'types': {1: 8, 2: 8, 3: 8, 4: 8}, 'colors': {1: [11119017, 15453831, 6333684], 2: [11119017, 15453831, 6333684], 3: [11119017, 15453831, 6333684], 4: [11119017, 15453831, 6333684]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Dev-stop 1', 2: 'Dev-stop 2', 3: 'Dev-stop 3', 4: 'Main dev-stop'}, 'levels': [], 'description': ['Kase dev-stops'], 'name': 'Kase dev-stops', 'source': 'MQL5 Indicators/Kase DevStops/Kase dev-stops.mq5', 'folder': 'Kase DevStops', 'inputs': [{'mql': 'inpDesPeriod', 'py': 'inpDesPeriod', 'param': 'inpDesPeriod', 'type': 'int', 'default': 20, 'label': 'Dev-stop period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 21, 'label': 'Dev-stop slow period', 'sinput': False}, {'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 10, 'label': 'Dev-stop fast period', 'sinput': False}, {'mql': 'inpStdDev1', 'py': 'inpStdDev1', 'param': 'inpStdDev1', 'type': 'double', 'default': 0.0, 'label': 'Deviation 1', 'sinput': False}, {'mql': 'inpStdDev2', 'py': 'inpStdDev2', 'param': 'inpStdDev2', 'type': 'double', 'default': 1.0, 'label': 'Deviation 2', 'sinput': False}, {'mql': 'inpStdDev3', 'py': 'inpStdDev3', 'param': 'inpStdDev3', 'type': 'double', 'default': 2.2, 'label': 'Deviation 3', 'sinput': False}, {'mql': 'inpStdDev4', 'py': 'inpStdDev4', 'param': 'inpStdDev4', 'type': 'double', 'default': 3.6, 'label': 'Deviation 4', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpDesPeriod = _input('inpDesPeriod', 20)  # Dev-stop period
inpSlowPeriod = _input('inpSlowPeriod', 21)  # Dev-stop slow period
inpFastPeriod = _input('inpFastPeriod', 10)  # Dev-stop fast period
inpStdDev1 = _input('inpStdDev1', 0.0)  # Deviation 1
inpStdDev2 = _input('inpStdDev2', 1.0)  # Deviation 2
inpStdDev3 = _input('inpStdDev3', 2.2)  # Deviation 3
inpStdDev4 = _input('inpStdDev4', 3.6)  # Deviation 4
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
val1 = Arr(0, 0.0)
val1c = Arr(0, 0.0)
val2 = Arr(0, 0.0)
val2c = Arr(0, 0.0)
val3 = Arr(0, 0.0)
val3c = Arr(0, 0.0)
trend = Arr(0, 0.0)
price = Arr(0, 0.0)
pricc = Arr(0, 0.0)
range_ = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, val1, INDICATOR_DATA)
    SetIndexBuffer(3, val1c, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, val2, INDICATOR_DATA)
    SetIndexBuffer(5, val2c, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, val3, INDICATOR_DATA)
    SetIndexBuffer(7, val3c, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, price, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, pricc, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, range_, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Kase dev-stop (' + _str(inpDesPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpFastPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        pricc[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        average1 = iSma(pricc[i], inpFastPeriod, i, rates_total, 0)
        average2 = iSma(pricc[i], inpSlowPeriod, i, rates_total, 1)
        trend[i] = (1 if (average1 > average2) else -1 if (average1 < average2) else trend[i - 1] if (i > 0) else 0)
        price[i] = (price[i - 1] if (i > 0) else pricc[i])
        if i > 0 and trend[i] != trend[i - 1]:
            if trend[i] == 1:
                price[i] = high[i]
            else:
                price[i] = low[i]
        if trend[i] > 0:
            price[i] = MathMax(price[i], high[i])
        if trend[i] < 0:
            price[i] = MathMin(price[i], low[i])
        max_ = (MathMax(MathMax(high[i], high[i - 1]), pricc[i - 2]) if (i > 2) else 0)
        min_ = (MathMin(MathMin(low[i], low[i - 1]), pricc[i - 2]) if (i > 2) else 0)
        range_[i] = max_ - min_
        avg = range_[i]
        n = 1
        while n < inpDesPeriod and (i - n) >= 0:
            avg += range_[i - n]
            n += 1
        avg = _fdiv(avg, n)
        dev = MathPow(range_[i] - avg, 2)
        n = 1
        while n < inpDesPeriod and (i - n) >= 0:
            dev += (range_[i - n] - avg) * (range_[i - n] - avg)
            n += 1
        dev = MathSqrt(_fdiv(dev, n))
        val[i] = price[i] + (-1 * trend[i] * (avg + (inpStdDev1 * dev)))
        val1[i] = price[i] + (-1 * trend[i] * (avg + (inpStdDev2 * dev)))
        val2[i] = price[i] + (-1 * trend[i] * (avg + (inpStdDev3 * dev)))
        val3[i] = price[i] + (-1 * trend[i] * (avg + (inpStdDev4 * dev)))
        val3c[i] = (1 if (trend[i] == 1) else 2 if (trend[i] == -1) else 0)
        val2c[i] = val3c[i]
        val1c[i] = val2c[i]
        valc[i] = val1c[i]
        i += 1
    return i

def iSma(tprice, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = tprice
    avg = tprice
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))

def getPrice(tprice, open, close, high, low, i, _bars):
    if i > 0 and i < _bars:
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


class KaseDevStops(_MQL5Indicator):
    name = 'Kase dev-stops'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpDesPeriod': 20,  # Dev-stop period
        'inpSlowPeriod': 21,  # Dev-stop slow period
        'inpFastPeriod': 10,  # Dev-stop fast period
        'inpStdDev1': 0.0,  # Deviation 1
        'inpStdDev2': 1.0,  # Deviation 2
        'inpStdDev3': 2.2,  # Deviation 3
        'inpStdDev4': 3.6,  # Deviation 4
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

