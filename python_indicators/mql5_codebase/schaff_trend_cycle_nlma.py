"""Schaff trend cycle - nlma — converted from MQL5: MQL5 Indicators/Schaff Trend Cycle - NonLag MA/Schaff trend cycle - nlma.mq5

Schaff trend cycle - non lag MA
Copyright: Copyright 2018, mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 3329330, 42495]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Schaff trend cycle - NLMA'}, 'levels': [], 'description': ['Schaff trend cycle - non lag MA'], 'name': 'Schaff trend cycle - nlma', 'source': 'MQL5 Indicators/Schaff Trend Cycle - NonLag MA/Schaff trend cycle - nlma.mq5', 'folder': 'Schaff Trend Cycle - NonLag MA', 'inputs': [{'mql': 'SchaffPeriod', 'py': 'SchaffPeriod', 'param': 'SchaffPeriod', 'type': 'int', 'default': 32, 'label': 'Schaff period', 'sinput': False}, {'mql': 'FastNlma', 'py': 'FastNlma', 'param': 'FastNlma', 'type': 'int', 'default': 23, 'label': 'Fast nonlag ma period', 'sinput': False}, {'mql': 'SlowNlma', 'py': 'SlowNlma', 'param': 'SlowNlma', 'type': 'int', 'default': 50, 'label': 'Slow nonlag ma period', 'sinput': False}, {'mql': 'SmoothPeriod', 'py': 'SmoothPeriod', 'param': 'SmoothPeriod', 'type': 'double', 'default': 3.0, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SchaffPeriod = _input('SchaffPeriod', 32)  # Schaff period
FastNlma = _input('FastNlma', 23)  # Fast nonlag ma period
SlowNlma = _input('SlowNlma', 50)  # Slow nonlag ma period
SmoothPeriod = _input('SmoothPeriod', 3.0)  # Smoothing period
Price = _input('Price', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
macd = Arr(0, 0.0)
fastk1 = Arr(0, 0.0)
fastd1 = Arr(0, 0.0)
fastk2 = Arr(0, 0.0)
nlmvalues = Arr(0, 0.0, dims=(3,))
nlmprices = Arr(0, 0.0, dims=(2,))
nlmalphas = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, macd, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, fastk1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, fastk2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, fastd1, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Schaff trend cycle NLMA (' + _str(SchaffPeriod) + ',' + _str(FastNlma) + ',' + _str(SlowNlma) + ',' + _str(SmoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tickVolume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    alpha = _fdiv(2.0, 1.0 + SmoothPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(Price, open, close, high, low, i, rates_total)
        macd[i] = iNonLagMa(price, FastNlma, i, rates_total, 0) - iNonLagMa(price, SlowNlma, i, rates_total, 1)
        start = MathMax(i - SchaffPeriod + 1, 0)
        lowMacd = macd[ArrayMinimum(macd, start, SchaffPeriod)]
        highMacd = macd[ArrayMaximum(macd, start, SchaffPeriod)] - lowMacd
        fastk1[i] = ((100 * _fdiv(macd[i] - lowMacd, highMacd)) if (highMacd > 0) else fastk1[i - 1] if (i > 0) else 0)
        fastd1[i] = ((fastd1[i - 1] + (alpha * (fastk1[i] - fastd1[i - 1]))) if (i > 0) else fastk1[i])
        lowStoch = fastd1[ArrayMinimum(fastd1, start, SchaffPeriod)]
        highStoch = fastd1[ArrayMaximum(fastd1, start, SchaffPeriod)] - lowStoch
        fastk2[i] = ((100 * _fdiv(fastd1[i] - lowStoch, highStoch)) if (highStoch > 0) else fastk2[i - 1] if (i > 0) else 0)
        val[i] = ((val[i - 1] + (alpha * (fastk2[i] - val[i - 1]))) if (i > 0) else fastk2[i])
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else 0) if (i > 0) else 0)
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


class SchaffTrendCycleNlma(_MQL5Indicator):
    name = 'Schaff trend cycle - nlma'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SchaffPeriod': 32,  # Schaff period
        'FastNlma': 23,  # Fast nonlag ma period
        'SlowNlma': 50,  # Slow nonlag ma period
        'SmoothPeriod': 3.0,  # Smoothing period
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

