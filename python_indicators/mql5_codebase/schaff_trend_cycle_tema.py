"""Schaff trend cycle - tema — converted from MQL5: MQL5 Indicators/Schaff Trend Cycle - TEMA/Schaff trend cycle - tema.mq5

Schaff trend cycle - tema
Copyright: Copyright 2017, mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2017, mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 3329330, 42495]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Schaff trend cycle - tema value'}, 'levels': [], 'description': ['Schaff trend cycle - tema'], 'name': 'Schaff trend cycle - tema', 'source': 'MQL5 Indicators/Schaff Trend Cycle - TEMA/Schaff trend cycle - tema.mq5', 'folder': 'Schaff Trend Cycle - TEMA', 'inputs': [{'mql': 'SchaffPeriod', 'py': 'SchaffPeriod', 'param': 'SchaffPeriod', 'type': 'int', 'default': 32, 'label': 'Schaff period', 'sinput': False}, {'mql': 'FastTema', 'py': 'FastTema', 'param': 'FastTema', 'type': 'int', 'default': 23, 'label': 'Fast tema period', 'sinput': False}, {'mql': 'SlowTema', 'py': 'SlowTema', 'param': 'SlowTema', 'type': 'int', 'default': 50, 'label': 'Slow tema period', 'sinput': False}, {'mql': 'SmoothPeriod', 'py': 'SmoothPeriod', 'param': 'SmoothPeriod', 'type': 'double', 'default': 3.0, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
SchaffPeriod = _input('SchaffPeriod', 32)  # Schaff period
FastTema = _input('FastTema', 23)  # Fast tema period
SlowTema = _input('SlowTema', 50)  # Slow tema period
SmoothPeriod = _input('SmoothPeriod', 3.0)  # Smoothing period
Price = _input('Price', pr_close)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
macd = Arr(0, 0.0)
fastk1 = Arr(0, 0.0)
fastd1 = Arr(0, 0.0)
fastk2 = Arr(0, 0.0)
workTema = Arr(0, 0.0, dims=(6,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, macd, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, fastk1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, fastk2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, fastd1, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Schaff trend cycle TEMA (' + _str(SchaffPeriod) + ',' + _str(FastTema) + ',' + _str(SlowTema) + ',' + _str(SmoothPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    alpha = _fdiv(2.0, 1.0 + SmoothPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(Price, open, close, high, low, i, rates_total)
        macd[i] = iTema(price, FastTema, i, rates_total, 0) - iTema(price, SlowTema, i, rates_total, 1)
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

def iTema(price, period, r, bars, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(workTema, 0) != bars:
        ArrayResize(workTema, bars)
    instanceNo *= 3
    workTema[r][0 + instanceNo] = price
    workTema[r][1 + instanceNo] = price
    workTema[r][2 + instanceNo] = price
    alpha = _fdiv(2.0, 1.0 + period)
    if r > 0:
        workTema[r][0 + instanceNo] = workTema[r - 1][0 + instanceNo] + (alpha * (price - workTema[r - 1][0 + instanceNo]))
        workTema[r][1 + instanceNo] = workTema[r - 1][1 + instanceNo] + (alpha * (workTema[r][0 + instanceNo] - workTema[r - 1][1 + instanceNo]))
        workTema[r][2 + instanceNo] = workTema[r - 1][2 + instanceNo] + (alpha * (workTema[r][1 + instanceNo] - workTema[r - 1][2 + instanceNo]))
    return workTema[r][2 + instanceNo] + (3.0 * (workTema[r][0 + instanceNo] - workTema[r][1 + instanceNo]))

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SchaffTrendCycleTema(_MQL5Indicator):
    name = 'Schaff trend cycle - tema'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SchaffPeriod': 32,  # Schaff period
        'FastTema': 23,  # Fast tema period
        'SlowTema': 50,  # Slow tema period
        'SmoothPeriod': 3.0,  # Smoothing period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
    }

