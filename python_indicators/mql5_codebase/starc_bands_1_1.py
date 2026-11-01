"""STARC_bands_1.1 — converted from MQL5: MQL5 Indicators/STARC bands/STARC_bands_1.1.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'chart', 'indicator_buffers': 13, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 7, 4: 1, 5: 17}, 'colors': {1: [15718560], 2: [15130800], 3: [15718560], 4: [11119017], 5: [11119017, 16760576, 6333684]}, 'widths': {}, 'styles': {4: 2}, 'labels': {1: 'upper filling', 2: 'middle filling', 3: 'lower filling', 4: 'Average', 5: 'STARC candles'}, 'levels': [], 'description': [], 'name': 'STARC_bands_1.1', 'source': 'MQL5 Indicators/STARC bands/STARC_bands_1.1.mq5', 'folder': 'STARC bands', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'StarcPeriod', 'py': 'StarcPeriod', 'param': 'StarcPeriod', 'type': 'int', 'default': 56, 'label': 'STARC main period', 'sinput': False}, {'mql': 'StarcFastPeriod', 'py': 'StarcFastPeriod', 'param': 'StarcFastPeriod', 'type': 'int', 'default': 3, 'label': 'Fast period (for candles color)', 'sinput': False}, {'mql': 'StarcMaType', 'py': 'StarcMaType', 'param': 'StarcMaType', 'type': 'int', 'default': 0, 'label': 'STARC average type', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'AtrPeriod', 'py': 'AtrPeriod', 'param': 'AtrPeriod', 'type': 'int', 'default': 100, 'label': 'ATR period', 'sinput': False}, {'mql': 'AtrMultiplier1', 'py': 'AtrMultiplier1', 'param': 'AtrMultiplier1', 'type': 'double', 'default': 2.0, 'label': 'ATR multiplier 1', 'sinput': False}, {'mql': 'AtrMultiplier2', 'py': 'AtrMultiplier2', 'param': 'AtrMultiplier2', 'type': 'double', 'default': 3.0, 'label': 'ATR multiplier 2', 'sinput': False}, {'mql': 'AtrMaType', 'py': 'AtrMaType', 'param': 'AtrMaType', 'type': 'int', 'default': 0, 'label': 'ATR averaging type', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data ?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

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
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
StarcPeriod = _input('StarcPeriod', 56)  # STARC main period
StarcFastPeriod = _input('StarcFastPeriod', 3)  # Fast period (for candles color)
StarcMaType = _input('StarcMaType', ma_sma)  # STARC average type
Price = _input('Price', pr_close)  # Price
AtrPeriod = _input('AtrPeriod', 100)  # ATR period
AtrMultiplier1 = _input('AtrMultiplier1', 2.0)  # ATR multiplier 1
AtrMultiplier2 = _input('AtrMultiplier2', 3.0)  # ATR multiplier 2
AtrMaType = _input('AtrMaType', ma_sma)  # ATR averaging type
Interpolate = _input('Interpolate', True)  # Interpolate mtf data ?
fill1u = Arr(0, 0.0)
fill1d = Arr(0, 0.0)
fill2u = Arr(0, 0.0)
fill2d = Arr(0, 0.0)
fillmu = Arr(0, 0.0)
fillmd = Arr(0, 0.0)
count = Arr(0, 0.0)
ma = Arr(0, 0.0)
cano = Arr(0, 0.0)
canh = Arr(0, 0.0)
canl = Arr(0, 0.0)
canc = Arr(0, 0.0)
cancl = Arr(0, 0.0)
timeFrame = 0
workHa = Arr(0, 0.0, dims=(4,))
workSma = Arr(0, 0.0, dims=(6,))
workEma = Arr(0, 0.0, dims=(3,))
workSmma = Arr(0, 0.0, dims=(3,))
workLwma = Arr(0, 0.0, dims=(3,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global timeFrame
    SetIndexBuffer(0, fill1u, INDICATOR_DATA)
    SetIndexBuffer(1, fill1d, INDICATOR_DATA)
    SetIndexBuffer(2, fillmu, INDICATOR_DATA)
    SetIndexBuffer(3, fillmd, INDICATOR_DATA)
    SetIndexBuffer(4, fill2u, INDICATOR_DATA)
    SetIndexBuffer(5, fill2d, INDICATOR_DATA)
    SetIndexBuffer(6, ma, INDICATOR_DATA)
    SetIndexBuffer(7, cano, INDICATOR_DATA)
    SetIndexBuffer(8, canh, INDICATOR_DATA)
    SetIndexBuffer(9, canl, INDICATOR_DATA)
    SetIndexBuffer(10, canc, INDICATOR_DATA)
    SetIndexBuffer(11, cancl, INDICATOR_DATA)
    SetIndexBuffer(12, count, INDICATOR_CALCULATIONS)
    timeFrame = MathMax(Period(), TimeFrame)
    PlotIndexSetString(0, PLOT_LABEL, timeFrameToString(timeFrame) + ' STARC upper area')
    PlotIndexSetString(1, PLOT_LABEL, timeFrameToString(timeFrame) + ' STARC middle area')
    PlotIndexSetString(2, PLOT_LABEL, timeFrameToString(timeFrame) + ' STARC lower area')
    return 0

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_indHandle
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if timeFrame != Period():
        result = Arr(0, 0.0)
        currTime = Arr(0, 0)
        nextTime = Arr(0, 0)
        if _s_OnCalculate_indHandle == -1:
            _s_OnCalculate_indHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, StarcPeriod, StarcFastPeriod, StarcMaType, Price, AtrPeriod, AtrMultiplier1, AtrMultiplier2, AtrMaType)
        if _s_OnCalculate_indHandle == -1:
            return 0
        if CopyBuffer(_s_OnCalculate_indHandle, 12, 0, 1, result) == -1:
            return 0
        i = 0
        limit = rates_total - _int(MathMin(_fdiv(result[0] * PeriodSeconds(timeFrame), PeriodSeconds(Period())), rates_total))
        limit = MathMax(limit, 0)
        for limit in range(limit, 0, -1):
            if count[limit] == (EMPTY_VALUE - 1):
                break
        else:
            limit = _range_end(limit, 0, -1)
        i = MathMin(limit, MathMax(prev_calculated - 1, 0))
        for i in range(i, rates_total):
            if CopyBuffer(_s_OnCalculate_indHandle, 0, _DT(time[i]), 1, result) == -1:
                break
            fill1u[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 1, _DT(time[i]), 1, result) == -1:
                break
            fill1d[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 2, _DT(time[i]), 1, result) == -1:
                break
            fillmu[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 3, _DT(time[i]), 1, result) == -1:
                break
            fillmd[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 4, _DT(time[i]), 1, result) == -1:
                break
            fill2u[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 5, _DT(time[i]), 1, result) == -1:
                break
            fill2d[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 6, _DT(time[i]), 1, result) == -1:
                break
            ma[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 11, _DT(time[i]), 1, result) == -1:
                break
            cancl[i] = result[0]
            cano[i] = open[i]
            canh[i] = high[i]
            canl[i] = low[i]
            canc[i] = close[i]
            count[i] = EMPTY_VALUE - 1
            if not Interpolate:
                continue
            CopyTime(Symbol(), TimeFrame, _DT(time[i]), 1, currTime)
            if i < (rates_total - 1):
                CopyTime(Symbol(), TimeFrame, _DT(time[i + 1]), 1, nextTime)
                if currTime[0] == nextTime[0]:
                    continue
            n = 0
            k = 0
            n = 1
            while (i - n) > 0 and time[i - n] >= currTime[0]:
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                fill1u[i - k] = fill1u[i] + _fdiv((fill1u[i - n] - fill1u[i]) * k, n)
                fill1d[i - k] = fill1d[i] + _fdiv((fill1d[i - n] - fill1d[i]) * k, n)
                fillmu[i - k] = fillmu[i] + _fdiv((fillmu[i - n] - fillmu[i]) * k, n)
                fillmd[i - k] = fillmd[i] + _fdiv((fillmd[i - n] - fillmd[i]) * k, n)
                fill2u[i - k] = fill2u[i] + _fdiv((fill2u[i - n] - fill2u[i]) * k, n)
                fill2d[i - k] = fill2d[i] + _fdiv((fill2d[i - n] - fill2d[i]) * k, n)
                ma[i - k] = ma[i] + _fdiv((ma[i - n] - ma[i]) * k, n)
                k += 1
        else:
            i = _range_end(i, rates_total, 1)
        if i != rates_total:
            return 0
        return rates_total
    atrPeriod = (AtrPeriod if (AtrPeriod > 0) else StarcPeriod)
    atrMultiplier1 = MathMin(AtrMultiplier1, AtrMultiplier2)
    atrMultiplier2 = MathMax(AtrMultiplier1, AtrMultiplier2)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(Price, open, close, high, low, i, rates_total, 0)
        tr = ((MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])) if (i > 0) else (high[i] - low[i]))
        atr = iCustomMa(AtrMaType, tr, atrPeriod, i, rates_total, 1)
        fma = iCustomMa(StarcMaType, price, StarcFastPeriod, i, rates_total, 2)
        ma[i] = iCustomMa(StarcMaType, price, StarcPeriod, i, rates_total, 0)
        fillmu[i] = ma[i] + (atrMultiplier1 * atr)
        fillmd[i] = ma[i] - (atrMultiplier1 * atr)
        fill1u[i] = ma[i] + (atrMultiplier2 * atr)
        fill1d[i] = fillmu[i]
        fill2d[i] = ma[i] - (atrMultiplier2 * atr)
        fill2u[i] = fillmd[i]
        canc[i] = close[i]
        cano[i] = open[i]
        canh[i] = high[i]
        canl[i] = low[i]
        cancl[i] = (1 if (fma > ma[i]) else 2 if (fma < ma[i]) else 0)
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    return rates_total

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
        _sw1 = tprice
        if _sw1 == pr_haclose:
            return haClose
        elif _sw1 == pr_haopen:
            return haOpen
        elif _sw1 == pr_hahigh:
            return haHigh
        elif _sw1 == pr_halow:
            return haLow
        elif _sw1 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw1 == pr_hamedianb:
            return (haOpen + haClose) / 2.0
        elif _sw1 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw1 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw1 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw1 == pr_hatbiased:
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
        elif _sw1 == pr_hatbiased2:
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw2 = tprice
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
    elif _sw2 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw2 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw2 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw2 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
    elif _sw2 == pr_tbiased2:
        if close[i] > open[i]:
            return high[i]
        if close[i] < open[i]:
            return low[i]
        return close[i]
    return 0.0

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw3 = mode
    if _sw3 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw3 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw3 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw3 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
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
    if period <= 1:
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

def getIndicatorName():
    progPath = MQL5InfoString(MQL5_PROGRAM_PATH)
    start = -1
    while True:
        foundAt = StringFind(progPath, '\\', start + 1)
        if foundAt >= 0:
            start = foundAt
        else:
            break
    indicatorName = StringSubstr(progPath, start + 1)
    indicatorName = StringSubstr(indicatorName, 0, StringLen(indicatorName) - 4)
    return indicatorName

def timeFrameToString(period):
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    i = ArraySize(_tfsPer) - 1
    for i in range(i, 0 - 1, -1):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, 0 - 1, -1)
    return _tfsStr[i]

# ---- static local variables
_s_OnCalculate_indHandle = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class STARCBands11(_MQL5Indicator):
    name = 'STARC_bands_1.1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'StarcPeriod': 56,  # STARC main period
        'StarcFastPeriod': 3,  # Fast period (for candles color)
        'StarcMaType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # STARC average type
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'AtrPeriod': 100,  # ATR period
        'AtrMultiplier1': 2.0,  # ATR multiplier 1
        'AtrMultiplier2': 3.0,  # ATR multiplier 2
        'AtrMaType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # ATR averaging type
        'Interpolate': True,  # Interpolate mtf data ?
    }

