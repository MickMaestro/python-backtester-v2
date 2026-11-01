"""BB stops - EMA deviation — converted from MQL5: MQL5 Indicators/BB Stops - EMA Deviation/BB stops - EMA deviation.mq5

Bollinger bands  stops - EMA deviation version
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 12}, 'colors': {1: [8421504], 2: [8421504], 3: [16748574], 4: [6333684], 5: [12632256, 16748574, 6333684]}, 'widths': {3: 3, 4: 3, 5: 2}, 'styles': {1: 2, 2: 2}, 'labels': {}, 'levels': [], 'description': ['Bollinger bands  stops - EMA deviation version'], 'name': 'BB stops - EMA deviation', 'source': 'MQL5 Indicators/BB Stops - EMA Deviation/BB stops - EMA deviation.mq5', 'folder': 'BB Stops - EMA Deviation', 'inputs': [{'mql': 'MaPeriod', 'py': 'MaPeriod', 'param': 'MaPeriod', 'type': 'int', 'default': 20, 'label': 'Bollinger bands period', 'sinput': False}, {'mql': 'MaMethod', 'py': 'MaMethod', 'param': 'MaMethod', 'type': 'int', 'default': 0, 'label': 'Moving average method', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'DeviationPeriod', 'py': 'DeviationPeriod', 'param': 'DeviationPeriod', 'type': 'int', 'default': 20, 'label': 'Deviations period', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 1.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'Risk', 'py': 'Risk', 'param': 'Risk', 'type': 'double', 'default': 1.0, 'label': 'Risk', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
MaPeriod = _input('MaPeriod', 20)  # Bollinger bands period
MaMethod = _input('MaMethod', ma_sma)  # Moving average method
Price = _input('Price', pr_close)  # Price
DeviationPeriod = _input('DeviationPeriod', 20)  # Deviations period
Deviation = _input('Deviation', 1.0)  # Deviation
Risk = _input('Risk', 1.0)  # Risk
bba = Arr(0, 0.0)
bbc = Arr(0, 0.0)
bblu = Arr(0, 0.0)
bbld = Arr(0, 0.0)
amax = Arr(0, 0.0)
amin = Arr(0, 0.0)
bmax = Arr(0, 0.0)
bmin = Arr(0, 0.0)
trend = Arr(0, 0.0)
workEmaDeviation = Arr(0, 0.0, dims=(2,))
workSma = Arr(0, 0.0, dims=(2,))
workEma = Arr(0, 0.0, dims=(2,))
workSmma = Arr(0, 0.0, dims=(2,))
workLwma = Arr(0, 0.0, dims=(2,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, bmax, INDICATOR_DATA)
    SetIndexBuffer(1, bmin, INDICATOR_DATA)
    SetIndexBuffer(2, bblu, INDICATOR_DATA)
    SetIndexBuffer(3, bbld, INDICATOR_DATA)
    SetIndexBuffer(4, bba, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    SetIndexBuffer(5, bbc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, amax, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, amin, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, trend, INDICATOR_CALCULATIONS)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tickVolume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(Price, open, close, high, low, i, rates_total, 0)
        dev = iEmaDeviation(price, DeviationPeriod, i, rates_total)
        ma = iCustomMa(MaMethod, price, MaPeriod, i, rates_total, 0)
        amax[i] = ma + (dev * Deviation)
        amin[i] = ma - (dev * Deviation)
        bmax[i] = amax[i] + (0.5 * (Risk - 1) * (amax[i] - amin[i]))
        bmin[i] = amin[i] - (0.5 * (Risk - 1) * (amax[i] - amin[i]))
        trend[i] = ((1 if (price > amax[i - 1]) else -1 if (price < amin[i - 1]) else trend[i - 1]) if (i > 0) else 0)
        if i > 0:
            if trend[i] == -1 and amax[i] > amax[i - 1]:
                amax[i] = amax[i - 1]
            if trend[i] == 1 and amin[i] < amin[i - 1]:
                amin[i] = amin[i - 1]
            if trend[i] == -1 and bmax[i] > bmax[i - 1]:
                bmax[i] = bmax[i - 1]
            if trend[i] == 1 and bmin[i] < bmin[i - 1]:
                bmin[i] = bmin[i - 1]
        bblu[i] = EMPTY_VALUE
        bbld[i] = EMPTY_VALUE
        if trend[i] == 1:
            bblu[i] = bmin[i]
            bbc[i] = 1.0
        if trend[i] == -1:
            bbld[i] = bmax[i]
            bbc[i] = 2.0
        bba[i] = (((bblu[i] if (trend[i] == 1) else bbld[i]) if (trend[i] != trend[i - 1]) else EMPTY_VALUE) if (i > 0) else EMPTY_VALUE)
        i += 1
    return i

def iEmaDeviation(price, period, i, bars, instanceNo=0):
    if ArrayRange(workEmaDeviation, 0) != bars:
        ArrayResize(workEmaDeviation, bars)
    instanceNo *= 2
    workEmaDeviation[i][instanceNo + 0] = price
    workEmaDeviation[i][instanceNo + 1] = price
    if i > 0 and period > 1:
        alpha = _fdiv(2.0, 1.0 + period)
        workEmaDeviation[i][instanceNo + 0] = workEmaDeviation[i - 1][instanceNo + 0] + (alpha * (price - workEmaDeviation[i - 1][instanceNo + 0]))
        workEmaDeviation[i][instanceNo + 1] = workEmaDeviation[i - 1][instanceNo + 1] + (alpha * ((price * price) - workEmaDeviation[i - 1][instanceNo + 1]))
    return MathSqrt(_fdiv(period * (workEmaDeviation[i][instanceNo + 1] - (workEmaDeviation[i][instanceNo + 0] * workEmaDeviation[i][instanceNo + 0])), MathMax(period - 1, 1)))

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    workSmma[r][instanceNo] = price
    if r > 1 and period > 1:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    if period < 1:
        return price
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


class BBStopsEMADeviation(_MQL5Indicator):
    name = 'BB stops - EMA deviation'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MaPeriod': 20,  # Bollinger bands period
        'MaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Moving average method
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'DeviationPeriod': 20,  # Deviations period
        'Deviation': 1.0,  # Deviation
        'Risk': 1.0,  # Risk
    }

