"""ehlers_inverse_fisher_transform_2 — converted from MQL5: MQL5 Indicators/Ehlers Inverse Fisher Transform/ehlers_inverse_fisher_transform_2.mq5

Copyright: www.tradecode.com; Link: www.tradecode.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.tradecode.com', 'link': 'www.tradecode.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 9662683]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Inverse fishert transform'}, 'levels': [], 'description': [], 'name': 'ehlers_inverse_fisher_transform_2', 'source': 'MQL5 Indicators/Ehlers Inverse Fisher Transform/ehlers_inverse_fisher_transform_2.mq5', 'folder': 'Ehlers Inverse Fisher Transform', 'inputs': [{'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'int', 'default': 10, 'label': 'RSI period', 'sinput': False}, {'mql': 'RsiPrice', 'py': 'RsiPrice', 'param': 'RsiPrice', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'RsiMethod', 'py': 'RsiMethod', 'param': 'RsiMethod', 'type': 'int', 'default': 2, 'label': 'Rsi method', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'int', 'default': 9, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 3, 'label': 'Smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum rsiMethods
_rsi = 0
_wil = 1
_rsx = 2
_cut = 3
_enum('rsiMethods', {0: '_rsi', 1: '_wil', 2: '_rsx', 3: '_cut'})

# enum enumAveragesType
avgSma = 0
avgEma = 1
avgSmma = 2
avgLwma = 3
_enum('enumAveragesType', {0: 'avgSma', 1: 'avgEma', 2: 'avgSmma', 3: 'avgLwma'})

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_average = 7
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average'})

# ---- inputs and global variables
RsiPeriod = _input('RsiPeriod', 10)  # RSI period
RsiPrice = _input('RsiPrice', pr_close)  # Price
RsiMethod = _input('RsiMethod', _rsx)  # Rsi method
Smooth = _input('Smooth', 9)  # Smoothing period
SmoothMethod = _input('SmoothMethod', avgLwma)  # Smoothing method
ift = Arr(0, 0.0)
colorInd = Arr(0, 0.0)
totalBars = 0
workSma = Arr(0, 0.0, dims=(2,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))
workRsi = Arr(0, 0.0, dims=(13,))
workrSmma = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, ift, INDICATOR_DATA)
    SetIndexBuffer(1, colorInd, INDICATOR_COLOR_INDEX)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global totalBars
    totalBars = rates_total
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        rsi = 0.1 * (iRsi(getPrice(RsiPrice, open, close, high, low, rates_total, i), RsiPeriod, RsiMethod, rates_total, i) - 50.0)
        rss = iCustomMa(SmoothMethod, rsi, Smooth, i)
        ift[i] = _fdiv(MathExp(2.0 * rss) - 1.0, MathExp(2.0 * rss) + 1.0)
        colorInd[i] = 0.0
        if ift[i] > ift[i - 1]:
            colorInd[i] = 0.0
        if ift[i] < ift[i - 1]:
            colorInd[i] = 1.0
    return rates_total

def iCustomMa(mode, price, length, r, instanceNo=0):
    _sw1 = mode
    if _sw1 == avgSma:
        return iSma(price, _int(length), r, instanceNo)
    elif _sw1 == avgEma:
        return iEma(price, length, r, instanceNo)
    elif _sw1 == avgSmma:
        return iSmma(price, _int(length), r, instanceNo)
    elif _sw1 == avgLwma:
        return iLwma(price, _int(length), r, instanceNo)
    else:
        return price

def iSma(price, period, r, instanceNo=0):
    if ArrayRange(workSma, 0) != totalBars:
        ArrayResize(workSma, totalBars)
    instanceNo *= 2
    k = 0
    workSma[r][instanceNo] = price
    if r >= period:
        workSma[r][instanceNo + 1] = workSma[r - 1][instanceNo + 1] + _fdiv(workSma[r][instanceNo] - workSma[r - period][instanceNo], period)
    else:
        workSma[r][instanceNo + 1] = 0.0
        k = 0
        while k < period and (r - k) >= 0:
            workSma[r][instanceNo + 1] += workSma[r - k][instanceNo]
            k += 1
        workSma[r][instanceNo + 1] = _fdiv(workSma[r][instanceNo + 1], k)
    return workSma[r][instanceNo + 1]

def iEma(price, period, r, instanceNo=0):
    if ArrayRange(workEma, 0) != totalBars:
        ArrayResize(workEma, totalBars)
    alpha = _fdiv(2.0, 1.0 + period)
    workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, instanceNo=0):
    if ArrayRange(workSmma, 0) != totalBars:
        ArrayResize(workSmma, totalBars)
    if r < period:
        workSmma[r][instanceNo] = price
    else:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, instanceNo=0):
    if ArrayRange(workLwma, 0) != totalBars:
        ArrayResize(workLwma, totalBars)
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

def getPrice(price, open, close, high, low, bars, i):
    _sw2 = price
    if _sw2 == pr_close:
        return close[i]
    elif _sw2 == pr_open:
        return open[i]
    elif _sw2 == pr_high:
        return high[i]
    elif _sw2 == pr_low:
        return low[i]
    elif _sw2 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw2 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    return 0.0

def iRsi(price, period, rsiMode, bars, r, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 13
    workRsi[r][z + 0] = price
    _sw3 = rsiMode
    if _sw3 == _rsi:
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
            alpha = _fdiv(1.0, period)
            change = workRsi[r][z + 0] - workRsi[r - 1][z + 0]
            workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (alpha * (change - workRsi[r - 1][z + 1]))
            workRsi[r][z + 2] = workRsi[r - 1][z + 2] + (alpha * (MathAbs(change) - workRsi[r - 1][z + 2]))
        if workRsi[r][z + 2] != 0:
            return 50.0 * (_fdiv(workRsi[r][z + 1], workRsi[r][z + 2]) + 1)
        else:
            return 50.0
    elif _sw3 == _wil:
        if r > 0:
            workRsi[r][z + 1] = irSmma(0.5 * (MathAbs(workRsi[r][z + 0] - workRsi[r - 1][z + 0]) + (workRsi[r][z + 0] - workRsi[r - 1][z + 0])), 0.5 * (period - 1), r, bars, (instanceNo * 2) + 0)
            workRsi[r][z + 2] = irSmma(0.5 * (MathAbs(workRsi[r][z + 0] - workRsi[r - 1][z + 0]) - (workRsi[r][z + 0] - workRsi[r - 1][z + 0])), 0.5 * (period - 1), r, bars, (instanceNo * 2) + 1)
            if (workRsi[r][z + 1] + workRsi[r][z + 2]) != 0:
                return _fdiv(100.0 * workRsi[r][z + 1], workRsi[r][z + 1] + workRsi[r][z + 2])
            else:
                return 50.0
        else:
            return 50.0
    elif _sw3 == _rsx:
        if r < period:
            for k in range(1, 13):
                workRsi[r][k + z] = 0.0
            return 50.0
        Kg = _fdiv(3.0, 2.0 + period)
        Hg = 1.0 - Kg
        mom = workRsi[r][0 + z] - workRsi[r - 1][0 + z]
        moa = MathAbs(mom)
        for k in range(0, 3):
            kk = k * 2
            workRsi[r][z + kk + 1] = (Kg * mom) + (Hg * workRsi[r - 1][z + kk + 1])
            workRsi[r][z + kk + 2] = (Kg * workRsi[r][z + kk + 1]) + (Hg * workRsi[r - 1][z + kk + 2])
            mom = (1.5 * workRsi[r][z + kk + 1]) - (0.5 * workRsi[r][z + kk + 2])
            workRsi[r][z + kk + 7] = (Kg * moa) + (Hg * workRsi[r - 1][z + kk + 7])
            workRsi[r][z + kk + 8] = (Kg * workRsi[r][z + kk + 7]) + (Hg * workRsi[r - 1][z + kk + 8])
            moa = (1.5 * workRsi[r][z + kk + 7]) - (0.5 * workRsi[r][z + kk + 8])
        if moa != 0:
            return MathMax(MathMin((_fdiv(mom, moa) + 1.0) * 50.0, 100.0), 0.0)
        else:
            return 50.0
    elif _sw3 == _cut:
        sump = 0.0
        sumn = 0.0
        k = 0
        while k < period and (r - k - 1) >= 0:
            diff = workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0]
            if diff > 0:
                sump += diff
            if diff < 0:
                sumn -= diff
            k += 1
        if sumn > 0:
            return 100.0 - _fdiv(100.0, 1.0 + _fdiv(sump, sumn))
        else:
            return 50.0
    return price

def irSmma(price, period, r, bars, instanceNo=0):
    if ArrayRange(workrSmma, 0) != bars:
        ArrayResize(workrSmma, bars)
    if r < period:
        workrSmma[r][instanceNo] = price
    else:
        workrSmma[r][instanceNo] = workrSmma[r - 1][instanceNo] + _fdiv(price - workrSmma[r - 1][instanceNo], period)
    return workrSmma[r][instanceNo]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersInverseFisherTransform2(_MQL5Indicator):
    name = 'ehlers_inverse_fisher_transform_2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RsiPeriod': 10,  # RSI period
        'RsiPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4'}, default=0),  # Price
        'RsiMethod': _Choice({0: 'rsi', 1: "Wilder's rsi", 2: 'rsx', 3: "Cuttler's rsi"}, default=2),  # Rsi method
        'Smooth': 9,  # Smoothing period
        'SmoothMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=3),  # Smoothing method
    }

