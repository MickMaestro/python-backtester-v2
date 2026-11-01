"""4_ma_candles — converted from MQL5: MQL5 Indicators/4MA Candles/4_ma_candles.mq5

Copyright: mladen; Link: www.forex-tsd.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [8421504, 3329330, 6333684]}, 'widths': {}, 'styles': {}, 'labels': {1: '4 ma candles'}, 'levels': [], 'description': [], 'name': '4_ma_candles', 'source': 'MQL5 Indicators/4MA Candles/4_ma_candles.mq5', 'folder': '4MA Candles', 'inputs': [{'mql': 'AvgPeriod', 'py': 'AvgPeriod', 'param': 'AvgPeriod', 'type': 'int', 'default': 25, 'label': 'Averages period', 'sinput': False}, {'mql': 'AvgType', 'py': 'AvgType', 'param': 'AvgType', 'type': 'int', 'default': 1, 'label': 'Averages method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
avgSma = 0
avgEma = 1
avgSmma = 2
avgLwma = 3
_enum('enMaTypes', {0: 'avgSma', 1: 'avgEma', 2: 'avgSmma', 3: 'avgLwma'})

# ---- inputs and global variables
AvgPeriod = _input('AvgPeriod', 25)  # Averages period
AvgType = _input('AvgType', avgEma)  # Averages method
canc = Arr(0, 0.0)
cano = Arr(0, 0.0)
canh = Arr(0, 0.0)
canl = Arr(0, 0.0)
colors = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(8,))
workEma = Arr(0, 0.0, dims=(4,))
workSmma = Arr(0, 0.0, dims=(4,))
workLwma = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, cano, INDICATOR_DATA)
    SetIndexBuffer(1, canh, INDICATOR_DATA)
    SetIndexBuffer(2, canl, INDICATOR_DATA)
    SetIndexBuffer(3, canc, INDICATOR_DATA)
    SetIndexBuffer(4, colors, INDICATOR_COLOR_INDEX)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    bars = Bars(Symbol(), Period())
    if bars < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        mao = iCustomMa(AvgType, open[i], AvgPeriod, i, rates_total, 0)
        mac = iCustomMa(AvgType, close[i], AvgPeriod, i, rates_total, 1)
        mah = iCustomMa(AvgType, high[i], AvgPeriod, i, rates_total, 2)
        mal = iCustomMa(AvgType, low[i], AvgPeriod, i, rates_total, 3)
        canh[i] = MathMax(MathMax(MathMax(mao, mac), mal), mah)
        canl[i] = MathMin(MathMin(MathMin(mao, mac), mal), mah)
        cano[i] = mao
        canc[i] = mac
        colors[i] = (2 if (mao > mac) else 1 if (mao < mac) else 0)
    return rates_total

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == avgSma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == avgEma:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == avgSmma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == avgLwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    instanceNo *= 2
    k = 0
    workSma[r][instanceNo + 0] = price
    workSma[r][instanceNo + 1] = price
    k = 1
    while k < period and (r - k) >= 0:
        workSma[r][instanceNo + 1] += workSma[r - k][instanceNo + 0]
        k += 1
    workSma[r][instanceNo + 1] = _fdiv(workSma[r][instanceNo + 1], 1.0 * k)
    return workSma[r][instanceNo + 1]

def iEma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    alpha = _fdiv(2.0, 1.0 + period)
    if r > 0:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    if r < period:
        workSmma[r][instanceNo] = price
    else:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind4MaCandles(_MQL5Indicator):
    name = '4_ma_candles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AvgPeriod': 25,  # Averages period
        'AvgType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=1),  # Averages method
    }

