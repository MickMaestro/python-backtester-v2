"""NonLag ma trend — converted from MQL5: MQL5 Indicators/NonLag MA Trend/NonLag ma trend.mq5

nonlag trend
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [11119017, 16760576, 6333684]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'nonlag trend'}, 'levels': [], 'description': ['nonlag trend'], 'name': 'NonLag ma trend', 'source': 'MQL5 Indicators/NonLag MA Trend/NonLag ma trend.mq5', 'folder': 'NonLag MA Trend', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 10, 'label': 'Look back period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 10)  # Look back period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)
nlmvalues = Arr(0, 0.0, dims=(3,))
nlmprices = Arr(0, 0.0, dims=(1,))
nlmalphas = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, valu, INDICATOR_DATA)
    SetIndexBuffer(1, vald, INDICATOR_DATA)
    SetIndexBuffer(2, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'nonlag trend (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        prices[i] = iNonLagMa(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, i, rates_total)
        valu[i] = high[i]
        vald[i] = low[i]
        valc[i] = ((1 if (prices[i] > prices[i - 1]) else 2 if (prices[i] < prices[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iNonLagMa(price, length, r, bars, instanceNo=0):
    if ArrayRange(nlmprices, 0) != bars:
        ArrayResize(nlmprices, bars)
    if ArrayRange(nlmvalues, 0) < (instanceNo + 1):
        ArrayResize(nlmvalues, instanceNo + 1)
    nlmprices[r][instanceNo] = price
    if length < 5 or r < 3:
        return nlmprices[r][instanceNo]
    if nlmvalues[instanceNo][0] != length:
        Cycle = 4.0
        Coeff = 3.0 * M_PI
        Phase = _int(length - 1)
        nlmvalues[instanceNo][0] = length
        nlmvalues[instanceNo][1] = _int(length * 4) + Phase
        nlmvalues[instanceNo][2] = 0.0
        if ArrayRange(nlmalphas, 0) < _int(nlmvalues[instanceNo][1]):
            ArrayResize(nlmalphas, _int(nlmvalues[instanceNo][1]))
        k = 0
        while k < _int(nlmvalues[instanceNo][1]):
            t = 0.0
            if k <= (Phase - 1):
                t = _fdiv(1.0 * k, Phase - 1)
            else:
                t = 1.0 + _fdiv((k - Phase + 1) * ((2.0 * Cycle) - 1.0), (Cycle * length) - 1.0)
            beta = MathCos(M_PI * t)
            g = _fdiv(1.0, (Coeff * t) + 1)
            if t <= 0.5:
                g = 1.0
            nlmalphas[k][instanceNo] = g * beta
            nlmvalues[instanceNo][2] += nlmalphas[k][instanceNo]
            k += 1
    if nlmvalues[instanceNo][2] > 0:
        sum_ = 0.0
        k = 0
        while k < _int(nlmvalues[instanceNo][1]) and (r - k) >= 0:
            sum_ += nlmalphas[k][instanceNo] * nlmprices[r - k][instanceNo]
            k += 1
        return _fdiv(sum_, nlmvalues[instanceNo][2])
    else:
        return 0.0

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


class NonLagMaTrend(_MQL5Indicator):
    name = 'NonLag ma trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 10,  # Look back period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

