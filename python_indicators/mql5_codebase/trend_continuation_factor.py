"""Trend continuation factor — converted from MQL5: MQL5 Indicators/Trend Continuation Factor/Trend continuation factor.mq5

Trend continuation factor
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [15130800, 14150650], 2: [11119017, 6333684, 16760576]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Trend continuation factor zone', 2: 'Trend continuation factor'}, 'levels': [], 'description': ['Trend continuation factor'], 'name': 'Trend continuation factor', 'source': 'MQL5 Indicators/Trend Continuation Factor/Trend continuation factor.mq5', 'folder': 'Trend Continuation Factor', 'inputs': [{'mql': 'inpLength', 'py': 'inpLength', 'param': 'inpLength', 'type': 'int', 'default': 30, 'label': 'Trend continuation factor period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpLength = _input('inpLength', 30)  # Trend continuation factor period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levup = Arr(0, 0.0)
levdn = Arr(0, 0.0)
prices = Arr(0, 0.0)
values = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, levup, INDICATOR_DATA)
    SetIndexBuffer(1, levdn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend continuation factor (' + _str(inpLength) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(values, 0) != rates_total:
        ArrayResize(values, rates_total)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        roc = ((prices[i] - prices[i - 1]) if (i > 0) else 0)
        values[i][0] = 0.0
        values[i][1] = 0.0
        values[i][2] = 0.0
        values[i][3] = 0.0
        if roc > 0:
            values[i][0] = roc
            values[i][2] = ((values[i][0] + values[i - 1][2]) if (i > 0) else values[i][0])
        if roc < 0:
            values[i][1] = -roc
            values[i][3] = ((values[i][1] + values[i - 1][3]) if (i > 0) else values[i][1])
        levup[i] = 0.0
        levup[i] = 0.0
        l = 0
        while l < inpLength and (i - l) >= 0:
            levup[i] += values[i - l][0] - values[i - l][3]
            levdn[i] += values[i - l][1] - values[i - l][2]
            l += 1
        val[i] = levup[i]
        valc[i] = (2 if (levup[i] > levdn[i]) else 1 if (levup[i] < levdn[i]) else 0)
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


class TrendContinuationFactor(_MQL5Indicator):
    name = 'Trend continuation factor'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpLength': 30,  # Trend continuation factor period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

