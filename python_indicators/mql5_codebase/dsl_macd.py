"""dsl_-_macd — converted from MQL5: MQL5 Indicators/Dsl - macd/dsl_-_macd.mq5

Copyright: © mladen, 2017; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2017', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [3329330], 2: [42495], 3: [12632256, 3329330, 42495]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'value'}, 'levels': [], 'description': [], 'name': 'dsl_-_macd', 'source': 'MQL5 Indicators/Dsl - macd/dsl_-_macd.mq5', 'folder': 'Dsl - macd', 'inputs': [{'mql': 'FastEma', 'py': 'FastEma', 'param': 'FastEma', 'type': 'int', 'default': 12, 'label': 'Fast ema period', 'sinput': False}, {'mql': 'SlowEma', 'py': 'SlowEma', 'param': 'SlowEma', 'type': 'int', 'default': 26, 'label': 'Slow ema period', 'sinput': False}, {'mql': 'SignalPeriod', 'py': 'SignalPeriod', 'param': 'SignalPeriod', 'type': 'double', 'default': 9.0, 'label': 'Signal period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter
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

# ---- inputs and global variables
FastEma = _input('FastEma', 12)  # Fast ema period
SlowEma = _input('SlowEma', 26)  # Slow ema period
SignalPeriod = _input('SignalPeriod', 9.0)  # Signal period
Price = _input('Price', pr_close)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
workEma = Arr(0, 0.0, dims=(2,))
nlmvalues = Arr(0, 0.0, dims=(3,))
nlmprices = Arr(0, 0.0, dims=(1,))
nlmalphas = Arr(0, 0.0, dims=(1,))
workHa = Arr(0, 0.0, dims=(4,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    for i in range(0, 2):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, ' (dsl) MACD (' + _str(FastEma) + ',' + _str(SlowEma) + ',' + _str(SignalPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    alpha = _fdiv(2.0, 1.0 + SignalPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(Price, open, close, high, low, i, rates_total)
        val[i] = iEma(price, FastEma, i, rates_total, 0) - iEma(price, SlowEma, i, rates_total, 1)
        levelUp[i] = (((levelUp[i - 1] + (alpha * (val[i] - levelUp[i - 1]))) if (val[i] > 0) else levelUp[i - 1]) if (i > 0) else 0)
        levelDn[i] = (((levelDn[i - 1] + (alpha * (val[i] - levelDn[i - 1]))) if (val[i] < 0) else levelDn[i - 1]) if (i > 0) else 0)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

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

def getIndicatorName():
    path = MQL5InfoString(MQL5_PROGRAM_PATH)
    data = TerminalInfoString(TERMINAL_DATA_PATH) + '\\MQL5\\Indicators\\'
    name = StringSubstr(path, StringLen(data))
    return name

def timeFrameToString(period):
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsStr[i]

def timeFrameCheck(_timeFrame, time):
    global _s_timeFrameCheck_warned
    if time[0] < SeriesInfoInteger(Symbol(), _timeFrame, SERIES_FIRSTDATE):
        startTime = Box(0)
        testTime = Arr(0, 0)
        if SeriesInfoInteger(Symbol(), PERIOD_M1, SERIES_TERMINAL_FIRSTDATE, startTime):
            if startTime.v > 0:
                CopyTime(Symbol(), _timeFrame, _DT(time[0]), 1, testTime)
                SeriesInfoInteger(Symbol(), _timeFrame, SERIES_FIRSTDATE, startTime)
        if startTime.v <= 0 or startTime.v > time[0]:
            Comment(MQL5InfoString(MQL5_PROGRAM_NAME) + '\nMissing data for ' + timeFrameToString(_timeFrame) + ' time frame\nRe-trying on next tick')
            _s_timeFrameCheck_warned = True
            return False
    if _s_timeFrameCheck_warned:
        Comment('')
        _s_timeFrameCheck_warned = False
    return True

# ---- static local variables
_s_timeFrameCheck_warned = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DslMacd(_MQL5Indicator):
    name = 'dsl_-_macd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastEma': 12,  # Fast ema period
        'SlowEma': 26,  # Slow ema period
        'SignalPeriod': 9.0,  # Signal period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
    }

