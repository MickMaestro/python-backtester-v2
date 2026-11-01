"""cci_simple_experiment — converted from MQL5: MQL5 Indicators/CCI Simple Experiment/cci_simple_experiment.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 8}, 'colors': {1: [16748574, 6333684], 2: [16748574], 3: [12632256], 4: [6333684], 5: [12632256, 16748574, 6333684]}, 'widths': {5: 2}, 'styles': {2: 2, 3: 2, 4: 2, 5: 0}, 'labels': {1: 'CCI fill', 2: 'CCI level up', 3: 'CCI middle level', 4: 'CCI level down', 5: 'CCI'}, 'levels': [], 'description': [], 'name': 'cci_simple_experiment', 'source': 'MQL5 Indicators/CCI Simple Experiment/cci_simple_experiment.mq5', 'folder': 'CCI Simple Experiment', 'inputs': [{'mql': 'pperiod', 'py': 'pperiod', 'param': 'pperiod', 'type': 'int', 'default': 50, 'label': 'CCI calculating period', 'sinput': False}, {'mql': 'pprice', 'py': 'pprice', 'param': 'pprice', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'psmooth', 'py': 'psmooth', 'param': 'psmooth', 'type': 'int', 'default': 32, 'label': 'Price smoothing', 'sinput': False}, {'mql': 'psmoothMethod', 'py': 'psmoothMethod', 'param': 'psmoothMethod', 'type': 'int', 'default': 1, 'label': 'Price smoothing method', 'sinput': False}, {'mql': 'flLookBack', 'py': 'flLookBack', 'param': 'flLookBack', 'type': 'int', 'default': 25, 'label': 'Floating levels look back period', 'sinput': False}, {'mql': 'flLevelUp', 'py': 'flLevelUp', 'param': 'flLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up level %', 'sinput': False}, {'mql': 'flLevelDown', 'py': 'flLevelDown', 'param': 'flLevelDown', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
pr_haclose = 10
pr_haopen = 11
pr_hahigh = 12
pr_halow = 13
pr_hamedian = 14
pr_hatypical = 15
pr_haweighted = 16
pr_haaverage = 17
pr_hamedianb = 18
pr_hatbiased = 19
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average', 8: 'pr_medianb', 9: 'pr_tbiased', 10: 'pr_haclose', 11: 'pr_haopen', 12: 'pr_hahigh', 13: 'pr_halow', 14: 'pr_hamedian', 15: 'pr_hatypical', 16: 'pr_haweighted', 17: 'pr_haaverage', 18: 'pr_hamedianb', 19: 'pr_hatbiased'})

# ---- inputs and global variables
pperiod = _input('pperiod', 50)  # CCI calculating period
pprice = _input('pprice', pr_close)  # Price
psmooth = _input('psmooth', 32)  # Price smoothing
psmoothMethod = _input('psmoothMethod', MODE_EMA)  # Price smoothing method
flLookBack = _input('flLookBack', 25)  # Floating levels look back period
flLevelUp = _input('flLevelUp', 90.0)  # Floating levels up level %
flLevelDown = _input('flLevelDown', 10.0)  # Floating levels down level %
buffer = Arr(0, 0.0)
levelup = Arr(0, 0.0)
levelmi = Arr(0, 0.0)
leveldn = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
prices = Arr(0, 0.0)
pricer = Arr(0, 0.0)
trend = Arr(0, 0.0)
_bars = 0
workSma = Arr(0, 0.0, dims=(2,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, levelup, INDICATOR_DATA)
    SetIndexBuffer(3, levelmi, INDICATOR_DATA)
    SetIndexBuffer(4, leveldn, INDICATOR_DATA)
    SetIndexBuffer(5, buffer, INDICATOR_DATA)
    SetIndexBuffer(6, trend, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, pricer, INDICATOR_CALCULATIONS)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _bars
    _bars = rates_total
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        pricer[i] = getPrice(pprice, open, close, high, low, i)
        _sw1 = psmoothMethod
        if _sw1 == MODE_SMA:
            prices[i] = iSma(pricer[i], psmooth, i, 0)
        elif _sw1 == MODE_EMA:
            prices[i] = iEma(pricer[i], psmooth, i, 0)
        elif _sw1 == MODE_SMMA:
            prices[i] = iSmma(pricer[i], psmooth, i, 0)
        elif _sw1 == MODE_LWMA:
            prices[i] = iLwma(pricer[i], psmooth, i, 0)
        noise = 0.0
        vhf = 0.0
        period = pperiod
        max_ = prices[i]
        min_ = prices[i]
        k = 0
        while k < pperiod and (i - k - 1) >= 0:
            noise += MathAbs(pricer[i - k] - pricer[i - k - 1])
            max_ = MathMax(pricer[i - k], max_)
            min_ = MathMin(pricer[i - k], min_)
            k += 1
        if noise > 0:
            vhf = _fdiv(max_ - min_, noise)
        if vhf != 0:
            period = MathCeil(pperiod * (-MathLog(vhf)))
        avg = 0.0
        k = 0
        while k < _int(period) and (i - k) >= 0:
            avg += prices[i - k]
            k += 1
        avg = _fdiv(avg, _int(period))
        dev = 0.0
        k = 0
        while k < _int(period) and (i - k) >= 0:
            dev += MathAbs(prices[i - k] - avg)
            k += 1
        dev = _fdiv(dev, _int(period))
        if dev != 0:
            buffer[i] = _fdiv(prices[i] - avg, 0.015 * dev)
        else:
            buffer[i] = 0.0
        min_ = buffer[i]
        max_ = buffer[i]
        k = 1
        while k < flLookBack and (i - k) >= 0:
            min_ = MathMin(buffer[i - k], min_)
            max_ = MathMax(buffer[i - k], max_)
            k += 1
        range_ = max_ - min_
        levelup[i] = min_ + ((flLevelUp * range_) / 100.0)
        leveldn[i] = min_ + ((flLevelDown * range_) / 100.0)
        levelmi[i] = min_ + (0.5 * range_)
        fill1[i] = buffer[i]
        fill2[i] = buffer[i]
        if buffer[i] > levelup[i]:
            fill2[i] = levelup[i]
        if buffer[i] < leveldn[i]:
            fill2[i] = leveldn[i]
        trend[i] = 0.0
        if buffer[i] > levelup[i]:
            trend[i] = 1.0
        if buffer[i] < leveldn[i]:
            trend[i] = 2.0
    return rates_total

def iSma(price, period, r, instanceNo=0):
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

def iEma(price, period, r, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    alpha = _fdiv(2.0, 1.0 + period)
    if r > 0:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    if r < period:
        workSmma[r][instanceNo] = price
    else:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, instanceNo=0):
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

def getPrice(tprice, open, close, high, low, i, instanceNo=0):
    if tprice >= pr_haclose:
        if ArrayRange(workHa, 0) != _bars:
            ArrayResize(workHa, _bars)
        r = i
        haOpen = 0.0
        if r > 0:
            haOpen = (workHa[r - 1][instanceNo + 2] + workHa[r - 1][instanceNo + 3]) / 2.0
        else:
            haOpen = (open[i] + close[i]) / 2
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        if haOpen < haClose:
            workHa[r][instanceNo + 0] = haLow
            workHa[r][instanceNo + 1] = haHigh
        else:
            workHa[r][instanceNo + 0] = haHigh
            workHa[r][instanceNo + 1] = haLow
        workHa[r][instanceNo + 2] = haOpen
        workHa[r][instanceNo + 3] = haClose
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
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CciSimpleExperiment(_MQL5Indicator):
    name = 'cci_simple_experiment'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'pperiod': 50,  # CCI calculating period
        'pprice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=0),  # Price
        'psmooth': 32,  # Price smoothing
        'psmoothMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Price smoothing method
        'flLookBack': 25,  # Floating levels look back period
        'flLevelUp': 90.0,  # Floating levels up level %
        'flLevelDown': 10.0,  # Floating levels down level %
    }

