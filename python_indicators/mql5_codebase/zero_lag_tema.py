"""Zero lag TEMA — converted from MQL5: MQL5 Indicators/Zero lag TEMA/Zero lag TEMA.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Zero lag TEMA'}, 'levels': [], 'description': [], 'name': 'Zero lag TEMA', 'source': 'MQL5 Indicators/Zero lag TEMA/Zero lag TEMA.mq5', 'folder': 'Zero lag TEMA', 'inputs': [{'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}, {'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 27.0, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
inpPeriod = _input('inpPeriod', 27.0)  # Period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workZlTema = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Zero lag TEMA (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        val[i] = iZlTema(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, i, rates_total)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

def iZlTema(price, period, r, bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workZlTema, 0) != bars:
        ArrayResize(workZlTema, bars)
    instanceNo *= 6
    workZlTema[r][0 + instanceNo] = price
    workZlTema[r][1 + instanceNo] = price
    workZlTema[r][2 + instanceNo] = price
    workZlTema[r][3 + instanceNo] = price
    workZlTema[r][4 + instanceNo] = price
    workZlTema[r][5 + instanceNo] = price
    alpha = _fdiv(2.0, 1.0 + period)
    if r > 0:
        workZlTema[r][0 + instanceNo] = workZlTema[r - 1][0 + instanceNo] + (alpha * (price - workZlTema[r - 1][0 + instanceNo]))
        workZlTema[r][1 + instanceNo] = workZlTema[r - 1][1 + instanceNo] + (alpha * (workZlTema[r][0 + instanceNo] - workZlTema[r - 1][1 + instanceNo]))
        workZlTema[r][2 + instanceNo] = workZlTema[r - 1][2 + instanceNo] + (alpha * (workZlTema[r][1 + instanceNo] - workZlTema[r - 1][2 + instanceNo]))
        tema1 = workZlTema[r][2 + instanceNo] + (3.0 * (workZlTema[r][0 + instanceNo] - workZlTema[r][1 + instanceNo]))
        workZlTema[r][3 + instanceNo] = workZlTema[r - 1][3 + instanceNo] + (alpha * (tema1 - workZlTema[r - 1][3 + instanceNo]))
        workZlTema[r][4 + instanceNo] = workZlTema[r - 1][4 + instanceNo] + (alpha * (workZlTema[r][3 + instanceNo] - workZlTema[r - 1][4 + instanceNo]))
        workZlTema[r][5 + instanceNo] = workZlTema[r - 1][5 + instanceNo] + (alpha * (workZlTema[r][4 + instanceNo] - workZlTema[r - 1][5 + instanceNo]))
        tema2 = workZlTema[r][5 + instanceNo] + (3.0 * (workZlTema[r][3 + instanceNo] - workZlTema[r][4 + instanceNo]))
        return (2.0 * tema1) - tema2
    return price

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


class ZeroLagTEMA(_MQL5Indicator):
    name = 'Zero lag TEMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
        'inpPeriod': 27.0,  # Period
    }

