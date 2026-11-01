"""T3 deviation — converted from MQL5: MQL5 Indicators/T3 Deviation/T3 deviation.mq5

T3 deviation
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'T3 deviation'}, 'levels': [], 'description': ['T3 deviation'], 'name': 'T3 deviation', 'source': 'MQL5 Indicators/T3 Deviation/T3 deviation.mq5', 'folder': 'T3 Deviation', 'inputs': [{'mql': 'inpDevPeriod', 'py': 'inpDevPeriod', 'param': 'inpDevPeriod', 'type': 'int', 'default': 20, 'label': 'Deviation period', 'sinput': False}, {'mql': 'inpDevHot', 'py': 'inpDevHot', 'param': 'inpDevHot', 'type': 'double', 'default': 0.7, 'label': 'Deviation "hot"', 'sinput': False}, {'mql': 'inpDevType', 'py': 'inpDevType', 'param': 'inpDevType', 'type': 'int', 'default': 0, 'label': 'Deviation T3 type', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enT3Type
t3_tillson = 0
t3_fulksmat = 1
_enum('enT3Type', {0: 't3_tillson', 1: 't3_fulksmat'})

# ---- inputs and global variables
inpDevPeriod = _input('inpDevPeriod', 20)  # Deviation period
inpDevHot = _input('inpDevHot', 0.7)  # Deviation "hot"
inpDevType = _input('inpDevType', t3_tillson)  # Deviation T3 type
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)
t3Values = Arr(0, 0.0, dims=(36,))
_c1 = 0.0
_c2 = 0.0
_c3 = 0.0
_c4 = 0.0
t3Valued = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'T3 deviation (' + _str(inpDevPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iT3Deviation(getPrice(inpPrice, open, close, high, low, i, rates_total), inpDevPeriod, inpDevHot, inpDevType == t3_tillson, i, rates_total)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iT3(price, period, _original, i, bars, s):
    if ArrayRange(t3Values, 0) != bars:
        ArrayResize(t3Values, bars)
    r = i
    t3Values[r][s + 0] = price
    t3Values[r][s + 1] = price
    t3Values[r][s + 2] = price
    t3Values[r][s + 3] = price
    t3Values[r][s + 4] = price
    t3Values[r][s + 5] = price
    if r > 0:
        n = period
        if not _original:
            n = 1.0 + ((n - 1.0) / 2.0)
        alpha = _fdiv(2.0, 1.0 + n)
        t3Values[r][s + 0] = t3Values[r - 1][s + 0] + (alpha * (price - t3Values[r - 1][s + 0]))
        t3Values[r][s + 1] = t3Values[r - 1][s + 1] + (alpha * (t3Values[r][s + 0] - t3Values[r - 1][s + 1]))
        t3Values[r][s + 2] = t3Values[r - 1][s + 2] + (alpha * (t3Values[r][s + 1] - t3Values[r - 1][s + 2]))
        t3Values[r][s + 3] = t3Values[r - 1][s + 3] + (alpha * (t3Values[r][s + 2] - t3Values[r - 1][s + 3]))
        t3Values[r][s + 4] = t3Values[r - 1][s + 4] + (alpha * (t3Values[r][s + 3] - t3Values[r - 1][s + 4]))
        t3Values[r][s + 5] = t3Values[r - 1][s + 5] + (alpha * (t3Values[r][s + 4] - t3Values[r - 1][s + 5]))
    return (_c1 * t3Values[r][s + 5]) + (_c2 * t3Values[r][s + 4]) + (_c3 * t3Values[r][s + 3]) + (_c4 * t3Values[r][s + 2])

def iT3Deviation(price, period, _hot, _original, i, bars):
    global _c1, _c2, _c3, _c4
    if ArrayRange(t3Valued, 0) != bars:
        ArrayResize(t3Valued, bars)
    a = _hot
    _c1 = (-a) * a * a
    _c2 = 3 * ((a * a) + (a * a * a))
    _c3 = -3 * ((2 * a * a) + a + (a * a * a))
    _c4 = 1 + (3 * a) + (a * a * a) + (3 * a * a)
    n = period
    if not _original:
        n = 1.0 + ((n - 1) / 2.0)
    r = i
    alpha = _fdiv(2.0, 1.0 + n)
    temp = iT3(price, period, _original, i, bars, 0)
    t3Valued[r][0] = (MathSqrt((alpha * (price - temp) * (price - temp)) + ((1.0 - alpha) * t3Valued[r - 1][0] * t3Valued[r - 1][0])) if (r > 0) else 0)
    temp = iT3(t3Valued[r][0], period, _original, i, bars, 6)
    t3Valued[r][1] = (MathSqrt((alpha * (t3Valued[r][0] - temp) * (t3Valued[r][0] - temp)) + ((1.0 - alpha) * t3Valued[r - 1][1] * t3Valued[r - 1][1])) if (r > 0) else 0)
    temp = iT3(t3Valued[r][1], period, _original, i, bars, 12)
    t3Valued[r][2] = (MathSqrt((alpha * (t3Valued[r][1] - temp) * (t3Valued[r][1] - temp)) + ((1.0 - alpha) * t3Valued[r - 1][2] * t3Valued[r - 1][2])) if (r > 0) else 0)
    temp = iT3(t3Valued[r][2], period, _original, i, bars, 18)
    t3Valued[r][3] = (MathSqrt((alpha * (t3Valued[r][2] - temp) * (t3Valued[r][2] - temp)) + ((1.0 - alpha) * t3Valued[r - 1][3] * t3Valued[r - 1][3])) if (r > 0) else 0)
    temp = iT3(t3Valued[r][3], period, _original, i, bars, 24)
    t3Valued[r][4] = (MathSqrt((alpha * (t3Valued[r][3] - temp) * (t3Valued[r][3] - temp)) + ((1.0 - alpha) * t3Valued[r - 1][4] * t3Valued[r - 1][4])) if (r > 0) else 0)
    temp = iT3(t3Valued[r][4], period, _original, i, bars, 30)
    t3Valued[r][5] = (MathSqrt((alpha * (t3Valued[r][4] - temp) * (t3Valued[r][4] - temp)) + ((1.0 - alpha) * t3Valued[r - 1][5] * t3Valued[r - 1][5])) if (r > 0) else 0)
    return MathSqrt(n) * ((_c1 * t3Valued[r][5]) + (_c2 * t3Valued[r][4]) + (_c3 * t3Valued[r][3]) + (_c4 * t3Valued[r][2]))

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


class T3Deviation(_MQL5Indicator):
    name = 'T3 deviation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpDevPeriod': 20,  # Deviation period
        'inpDevHot': 0.7,  # Deviation "hot"
        'inpDevType': _Choice({0: 'Tim Tillson way of calculation', 1: 'Fulks/Matulich way of calculation'}, default=0),  # Deviation T3 type
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

