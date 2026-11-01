"""Point of Balance — converted from MQL5: MQL5 Indicators/Point of Balance/Point of Balance.mq5

Point of balance
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 2, 2: 2}, 'colors': {1: [16760576], 2: [17919]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Point of balance down'}, 'levels': [], 'description': ['Point of balance'], 'name': 'Point of Balance', 'source': 'MQL5 Indicators/Point of Balance/Point of Balance.mq5', 'folder': 'Point of Balance', 'inputs': [{'mql': 'inpPobPeriod', 'py': 'inpPobPeriod', 'param': 'inpPobPeriod', 'type': 'int', 'default': 12, 'label': 'Point of balance period', 'sinput': False}, {'mql': 'inpPobLevel', 'py': 'inpPobLevel', 'param': 'inpPobLevel', 'type': 'int', 'default': 10, 'label': 'Point of balance level (>=1 and <=10)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPobPeriod = _input('inpPobPeriod', 12)  # Point of balance period
inpPobLevel = _input('inpPobLevel', 10)  # Point of balance level (>=1 and <=10)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
prices = Arr(0, 0.0)
mpavg = Arr(0, 0.0, dims=(11,))
_pobLevel = 0

def OnInit():
    global _pobLevel
    SetIndexBuffer(0, valu, INDICATOR_DATA)
    SetIndexBuffer(1, vald, INDICATOR_DATA)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    _pobLevel = MathMax(MathMin(inpPobPeriod, 10), 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Point of Balance (' + _str(_pobLevel) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(mpavg, 0) != rates_total:
        ArrayResize(mpavg, rates_total)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        mpavg[i][0] = MidPoint(0, i)
        mpavg[i][1] = MidPoint(1, i)
        mpavg[i][2] = MidPoint(2, i)
        mpavg[i][3] = MidPoint(3, i)
        mpavg[i][4] = MidPoint(4, i)
        mpavg[i][5] = MidPoint(5, i)
        mpavg[i][6] = MidPoint(6, i)
        mpavg[i][7] = MidPoint(7, i)
        mpavg[i][8] = MidPoint(8, i)
        mpavg[i][9] = MidPoint(9, i)
        mpavg[i][10] = MidPoint(10, i)
        _start = MathMax(i - _pobLevel, 0)
        hiPrice = prices[ArrayMaximum(prices, _start, _pobLevel)]
        loPrice = prices[ArrayMinimum(prices, _start, _pobLevel)]
        _avg = mpavg[i][0]
        k = 1
        while k <= _pobLevel:
            _avg += mpavg[i][k]
            k += 1
        _avg = _fdiv(_avg, k)
        value = (_fdiv(100 * (prices[i] - _avg), hiPrice - loPrice) if (hiPrice != loPrice) else 0)
        valu[i] = (value if (value > 0) else EMPTY_VALUE)
        vald[i] = (value if (value < 0) else EMPTY_VALUE)
        i += 1
    return i

def MidPoint(_forDim, shift):
    maxValue = (prices[shift] if (_forDim == 0) else mpavg[shift][_forDim - 1])
    minValue = (prices[shift] if (_forDim == 0) else mpavg[shift][_forDim - 1])
    i = 1
    while i < inpPobPeriod and (shift - i) >= 0:
        minValue = MathMin(minValue, (prices[shift - i] if (_forDim == 0) else mpavg[shift - i][_forDim - 1]))
        maxValue = MathMax(minValue, (prices[shift - i] if (_forDim == 0) else mpavg[shift - i][_forDim - 1]))
        i += 1
    return (maxValue + minValue) / 2

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


class PointOfBalance(_MQL5Indicator):
    name = 'Point of Balance'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPobPeriod': 12,  # Point of balance period
        'inpPobLevel': 10,  # Point of balance level (>=1 and <=10)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

