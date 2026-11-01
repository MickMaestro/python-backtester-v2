"""RSI adaptive EMA ribbon — converted from MQL5: MQL5 Indicators/RSI adaptive EMA ribbon/RSI adaptive EMA ribbon.mq5

RSI adaptive EMA ribbon
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [11119017, 16760576, 8036607], 2: [11119017, 16760576, 8036607]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Fast RSI adaptive EMA', 2: 'Slow RSI adaptive EMA'}, 'levels': [], 'description': ['RSI adaptive EMA ribbon'], 'name': 'RSI adaptive EMA ribbon', 'source': 'MQL5 Indicators/RSI adaptive EMA ribbon/RSI adaptive EMA ribbon.mq5', 'folder': 'RSI adaptive EMA ribbon', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 12, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 26, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 12)  # Fast period
inpSlowPeriod = _input('inpSlowPeriod', 26)  # Slow period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
valf = Arr(0, 0.0)
valfc = Arr(0, 0.0)
vals = Arr(0, 0.0)
valsc = Arr(0, 0.0)
workRsi = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, valf, INDICATOR_DATA)
    SetIndexBuffer(1, valfc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, vals, INDICATOR_DATA)
    SetIndexBuffer(3, valsc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI adaptive EMA ribbon (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        _alphaf = MathAbs((iRsi(_price, inpFastPeriod, i, rates_total, 0) / 100.0) - 0.5) * 2.0
        _alphas = MathAbs((iRsi(_price, inpSlowPeriod, i, rates_total, 1) / 100.0) - 0.5) * 2.0
        valf[i] = ((valf[i - 1] + (_alphaf * (_price - valf[i - 1]))) if (i > 0) else _price)
        vals[i] = ((vals[i - 1] + (_alphas * (_price - vals[i - 1]))) if (i > 0) else _price)
        valfc[i] = (1 if (valf[i] > vals[i]) else 2 if (valf[i] < vals[i]) else valfc[i - 1] if (i > 0) else 0)
        valsc[i] = valfc[i]
        i += 1
    return i

def iRsi(price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 3
    workRsi[r][z + 0] = price
    alpha = _fdiv(1.0, MathMax(period, 1))
    if r < period:
        k = 0
        sum_ = 0.0
        k = 0
        while k < period and (r - k - 1) >= 0:
            sum_ += MathAbs(workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0])
            k += 1
        workRsi[r][z + 1] = _fdiv(workRsi[r][z + 0] - workRsi[0][z + 0], MathMax(k, 1))
        workRsi[r][z + 2] = _fdiv(sum_, MathMax(k, 1))
    else:
        change = workRsi[r][z + 0] - workRsi[r - 1][z + 0]
        workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (alpha * (change - workRsi[r - 1][z + 1]))
        workRsi[r][z + 2] = workRsi[r - 1][z + 2] + (alpha * (MathAbs(change) - workRsi[r - 1][z + 2]))
    return 50.0 * (_fdiv(workRsi[r][z + 1], MathMax(workRsi[r][z + 2], DBL_MIN)) + 1)

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


class RSIAdaptiveEMARibbon(_MQL5Indicator):
    name = 'RSI adaptive EMA ribbon'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpFastPeriod': 12,  # Fast period
        'inpSlowPeriod': 26,  # Slow period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

