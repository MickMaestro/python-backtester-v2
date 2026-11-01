"""Laguerre stripped of rsi — converted from MQL5: MQL5 Indicators/Laguerre stripped of RSI/Laguerre stripped of rsi.mq5

Copyright: © mladen, 2017; Link: www.forex-station.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2017', 'link': 'www.forex-station.com', 'window': 'separate', 'indicator_buffers': 11, 'indicator_plots': 8}, 'types': {1: 7, 2: 7, 3: 7, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [8310016, 8257691], 2: [8303616, 8257716], 3: [8297216, 8257741], 4: [8421504], 5: [8421504], 6: [8421504], 7: [8421504], 8: [12632256]}, 'widths': {8: 2}, 'styles': {}, 'labels': {1: 'Fill 1', 2: 'Fill 2', 3: 'Fill 3', 4: 'Laguerre 1', 5: 'Laguerre 2', 6: 'Laguerre 3', 7: 'Laguerre 4', 8: 'RSI'}, 'levels': [], 'description': [], 'name': 'Laguerre stripped of rsi', 'source': 'MQL5 Indicators/Laguerre stripped of RSI/Laguerre stripped of rsi.mq5', 'folder': 'Laguerre stripped of RSI', 'inputs': [{'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'RsiPrice', 'py': 'RsiPrice', 'param': 'RsiPrice', 'type': 'int', 'default': 0, 'label': 'RSI price', 'sinput': False}, {'mql': 'MaMethodToUse', 'py': 'MaMethodToUse', 'param': 'MaMethodToUse', 'type': 'int', 'default': -1, 'label': 'What ma method to use in rsi calculation', 'sinput': False}, {'mql': 'Gamma', 'py': 'Gamma', 'param': 'Gamma', 'type': 'double', 'default': 0.75, 'label': 'Laguerre gamma', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_average = 7
pr_medianb = 8
pr_tbiased = 9
pr_tbiased2 = 10
pr_haclose = 11
pr_haopen = 12
pr_hahigh = 13
pr_halow = 14
pr_hamedian = 15
pr_hatypical = 16
pr_haweighted = 17
pr_haaverage = 18
pr_hamedianb = 19
pr_hatbiased = 20
pr_hatbiased2 = 21
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average', 8: 'pr_medianb', 9: 'pr_tbiased', 10: 'pr_tbiased2', 11: 'pr_haclose', 12: 'pr_haopen', 13: 'pr_hahigh', 14: 'pr_halow', 15: 'pr_hamedian', 16: 'pr_hatypical', 17: 'pr_haweighted', 18: 'pr_haaverage', 19: 'pr_hamedianb', 20: 'pr_hatbiased', 21: 'pr_hatbiased2'})

# enum enRsiMaMethod
rsm_original = -1
rsm_sma = 0
rsm_ema = 1
rsm_smma = 2
rsm_lwma = 3
_enum('enRsiMaMethod', {-1: 'rsm_original', 0: 'rsm_sma', 1: 'rsm_ema', 2: 'rsm_smma', 3: 'rsm_lwma'})

# ---- inputs and global variables
RsiPeriod = _input('RsiPeriod', 14)  # RSI period
RsiPrice = _input('RsiPrice', pr_close)  # RSI price
MaMethodToUse = _input('MaMethodToUse', rsm_original)  # What ma method to use in rsi calculation
Gamma = _input('Gamma', 0.75)  # Laguerre gamma
lagg1u = Arr(0, 0.0)
lagg1d = Arr(0, 0.0)
lagg2u = Arr(0, 0.0)
lagg2d = Arr(0, 0.0)
lagg3u = Arr(0, 0.0)
lagg3d = Arr(0, 0.0)
lagg1 = Arr(0, 0.0)
lagg2 = Arr(0, 0.0)
lagg3 = Arr(0, 0.0)
lagg4 = Arr(0, 0.0)
rsi = Arr(0, 0.0)
workLag = Arr(0, 0.0, dims=(4,))
workRsi = Arr(0, 0.0, dims=(3,))
workSma = Arr(0, 0.0, dims=(6,))
workEma = Arr(0, 0.0, dims=(3,))
workSmma = Arr(0, 0.0, dims=(3,))
workLwma = Arr(0, 0.0, dims=(3,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, lagg1u, INDICATOR_DATA)
    SetIndexBuffer(1, lagg1d, INDICATOR_DATA)
    SetIndexBuffer(2, lagg2u, INDICATOR_DATA)
    SetIndexBuffer(3, lagg2d, INDICATOR_DATA)
    SetIndexBuffer(4, lagg3u, INDICATOR_DATA)
    SetIndexBuffer(5, lagg3d, INDICATOR_DATA)
    SetIndexBuffer(6, lagg1, INDICATOR_DATA)
    SetIndexBuffer(7, lagg2, INDICATOR_DATA)
    SetIndexBuffer(8, lagg3, INDICATOR_DATA)
    SetIndexBuffer(9, lagg4, INDICATOR_DATA)
    SetIndexBuffer(10, rsi, INDICATOR_DATA)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        laga = Box(0.0)
        lagb = Box(0.0)
        lagc = Box(0.0)
        lagd = Box(0.0)
        rsi[i] = iRsi(MaMethodToUse, getPrice(RsiPrice, open, close, high, low, i, rates_total), RsiPeriod, i, rates_total)
        iLaGuerre(rsi[i], Gamma, laga, lagb, lagc, lagd, i, rates_total, 0)
        lagg1[i] = laga.v
        lagg2[i] = lagb.v
        lagg3[i] = lagc.v
        lagg4[i] = lagd.v
        lagg1u[i] = laga.v
        lagg1d[i] = lagb.v
        lagg2u[i] = lagb.v
        lagg2d[i] = lagc.v
        lagg3u[i] = lagc.v
        lagg3d[i] = lagd.v
        i += 1
    return i

def iLaGuerre(price, gamma, val1, val2, val3, val4, i, bars, instanceNo=0):
    if ArrayRange(workLag, 0) != bars:
        ArrayResize(workLag, bars)
    instanceNo *= 4
    gamma = MathMax(MathMin(gamma, 0.99), 0.01)
    if i > 0:
        workLag[i][instanceNo + 0] = ((1.0 - gamma) * price) + (gamma * workLag[i - 1][instanceNo + 0])
        workLag[i][instanceNo + 1] = ((-gamma) * workLag[i][instanceNo + 0]) + workLag[i - 1][instanceNo + 0] + (gamma * workLag[i - 1][instanceNo + 1])
        workLag[i][instanceNo + 2] = ((-gamma) * workLag[i][instanceNo + 1]) + workLag[i - 1][instanceNo + 1] + (gamma * workLag[i - 1][instanceNo + 2])
        workLag[i][instanceNo + 3] = ((-gamma) * workLag[i][instanceNo + 2]) + workLag[i - 1][instanceNo + 2] + (gamma * workLag[i - 1][instanceNo + 3])
    else:
        for k in range(0, 4):
            workLag[i][instanceNo + k] = price
    val1.v = workLag[i][instanceNo + 0]
    val2.v = workLag[i][instanceNo + 1]
    val3.v = workLag[i][instanceNo + 2]
    val4.v = workLag[i][instanceNo + 3]

def iRsi(maMethod, price, period, i, _bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != _bars:
        ArrayResize(workRsi, _bars)
    r = i
    z = instanceNo * 3
    workRsi[r][z + 0] = price
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
        _sw1 = maMethod
        if _sw1 == rsm_original:
            alpha = _fdiv(1.0, period)
            workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (alpha * (change - workRsi[r - 1][z + 1]))
            workRsi[r][z + 2] = workRsi[r - 1][z + 2] + (alpha * (MathAbs(change) - workRsi[r - 1][z + 2]))
        elif _sw1 == rsm_sma:
            workRsi[r][z + 1] = iSma(change, _int(period), r, _bars, 0)
            workRsi[r][z + 2] = iSma(MathAbs(change), _int(period), r, _bars, 1)
        elif _sw1 == rsm_ema:
            workRsi[r][z + 1] = iEma(change, period, r, _bars, 0)
            workRsi[r][z + 2] = iEma(MathAbs(change), period, r, _bars, 1)
        elif _sw1 == rsm_smma:
            workRsi[r][z + 1] = iSmma(change, period, r, _bars, 0)
            workRsi[r][z + 2] = iSmma(MathAbs(change), period, r, _bars, 1)
        elif _sw1 == rsm_lwma:
            workRsi[r][z + 1] = iLwma(change, period, r, _bars, 0)
            workRsi[r][z + 2] = iLwma(MathAbs(change), period, r, _bars, 1)
    if workRsi[r][z + 2] != 0:
        return 50.0 * (_fdiv(workRsi[r][z + 1], workRsi[r][z + 2]) + 1)
    else:
        return 50.0

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

def getPrice(tprice, open, close, high, low, i, _bars, instanceNo=0):
    if tprice >= pr_haclose:
        if ArrayRange(workHa, 0) != _bars:
            ArrayResize(workHa, _bars)
        instanceNo *= 4
        haOpen = 0.0
        if i > 0:
            haOpen = (workHa[i - 1][instanceNo + 2] + workHa[i - 1][instanceNo + 3]) / 2.0
        else:
            haOpen = (open[i] + close[i]) / 2
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        if haOpen < haClose:
            workHa[i][instanceNo + 0] = haLow
            workHa[i][instanceNo + 1] = haHigh
        else:
            workHa[i][instanceNo + 0] = haHigh
            workHa[i][instanceNo + 1] = haLow
        workHa[i][instanceNo + 2] = haOpen
        workHa[i][instanceNo + 3] = haClose
        _sw2 = tprice
        if _sw2 == pr_haclose:
            return haClose
        elif _sw2 == pr_haopen:
            return haOpen
        elif _sw2 == pr_hahigh:
            return haHigh
        elif _sw2 == pr_halow:
            return haLow
        elif _sw2 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw2 == pr_hamedianb:
            return (haOpen + haClose) / 2.0
        elif _sw2 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw2 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw2 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw2 == pr_hatbiased:
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
        elif _sw2 == pr_hatbiased2:
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw3 = tprice
    if _sw3 == pr_close:
        return close[i]
    elif _sw3 == pr_open:
        return open[i]
    elif _sw3 == pr_high:
        return high[i]
    elif _sw3 == pr_low:
        return low[i]
    elif _sw3 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw3 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw3 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw3 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw3 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw3 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
    elif _sw3 == pr_tbiased2:
        if close[i] > open[i]:
            return high[i]
        if close[i] < open[i]:
            return low[i]
        return close[i]
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LaguerreStrippedOfRsi(_MQL5Indicator):
    name = 'Laguerre stripped of rsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RsiPeriod': 14,  # RSI period
        'RsiPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # RSI price
        'MaMethodToUse': _Choice({-1: 'Original RSI calculation', 0: 'Calculate RSI using SMA', 1: 'Calculate RSI using EMA', 2: 'Calculate RSI using SMMA', 3: 'Calculate RSI using LWMA'}, default=-1),  # What ma method to use in rsi calculation
        'Gamma': 0.75,  # Laguerre gamma
    }

