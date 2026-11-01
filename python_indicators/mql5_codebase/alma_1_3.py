"""Alma_1_3 — converted from MQL5: MQL5 Indicators/ALMA with addition filters/Alma_1_3.mq5

Copyright: mladen; Link: www.forex-tsd.com; Version: 1.3

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'version': '1.3', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [16748574], 2: [12632256], 3: [6333684], 4: [12632256, 16760576, 6333684]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2, 4: 0}, 'labels': {1: 'alma level up', 2: 'alma middle level', 3: 'alma level down', 4: 'alma'}, 'levels': [], 'description': [], 'name': 'Alma_1_3', 'source': 'MQL5 Indicators/ALMA with addition filters/Alma_1_3.mq5', 'folder': 'ALMA with addition filters', 'inputs': [{'mql': 'AlmaPeriod', 'py': 'AlmaPeriod', 'param': 'AlmaPeriod', 'type': 'int', 'default': 14, 'label': 'Calculation period', 'sinput': False}, {'mql': 'AlmaPrice', 'py': 'AlmaPrice', 'param': 'AlmaPrice', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'AlmaSigma', 'py': 'AlmaSigma', 'param': 'AlmaSigma', 'type': 'double', 'default': 6.0, 'label': 'Alma sigma', 'sinput': False}, {'mql': 'AlmaSample', 'py': 'AlmaSample', 'param': 'AlmaSample', 'type': 'double', 'default': 0.25, 'label': 'Alma sample', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 2, 'label': 'Color change on :', 'sinput': False}, {'mql': 'flLookBack', 'py': 'flLookBack', 'param': 'flLookBack', 'type': 'int', 'default': 25, 'label': 'Floating levels look back period', 'sinput': False}, {'mql': 'flLevelUp', 'py': 'flLevelUp', 'param': 'flLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up level %', 'sinput': False}, {'mql': 'flLevelDown', 'py': 'flLevelDown', 'param': 'flLevelDown', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down level %', 'sinput': False}, {'mql': 'fltPeriod', 'py': 'fltPeriod', 'param': 'fltPeriod', 'type': 'int', 'default': 0, 'label': 'Filter period (<= 0 to use alma period', 'sinput': False}, {'mql': 'fltFilter', 'py': 'fltFilter', 'param': 'fltFilter', 'type': 'double', 'default': 0.0, 'label': 'Filter value (<=0 for no filtering)', 'sinput': False}, {'mql': 'fltFilterOn', 'py': 'fltFilterOn', 'param': 'fltFilterOn', 'type': 'int', 'default': 0, 'label': 'Filter to be applied to :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enColorOn
cl_slope = 0
cl_mid = 1
cl_out = 2
_enum('enColorOn', {0: 'cl_slope', 1: 'cl_mid', 2: 'cl_out'})

# enum enFilter
flt_val = 0
flt_prc = 1
flt_all = 2
_enum('enFilter', {0: 'flt_val', 1: 'flt_prc', 2: 'flt_all'})

# ---- inputs and global variables
AlmaPeriod = _input('AlmaPeriod', 14)  # Calculation period
AlmaPrice = _input('AlmaPrice', pr_close)  # Price to use
AlmaSigma = _input('AlmaSigma', 6.0)  # Alma sigma
AlmaSample = _input('AlmaSample', 0.25)  # Alma sample
ColorOn = _input('ColorOn', cl_out)  # Color change on :
flLookBack = _input('flLookBack', 25)  # Floating levels look back period
flLevelUp = _input('flLevelUp', 90.0)  # Floating levels up level %
flLevelDown = _input('flLevelDown', 10.0)  # Floating levels down level %
fltPeriod = _input('fltPeriod', 0)  # Filter period (<= 0 to use alma period
fltFilter = _input('fltFilter', 0.0)  # Filter value (<=0 for no filtering)
fltFilterOn = _input('fltFilterOn', flt_val)  # Filter to be applied to :
MaBuffer = Arr(0, 0.0)
levup = Arr(0, 0.0)
levmi = Arr(0, 0.0)
levdn = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
totalBars = 0
workFil = Arr(0, 0.0, dims=(6,))
almaWork = Arr(0, 0.0, dims=(1,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, levup, INDICATOR_DATA)
    SetIndexBuffer(1, levmi, INDICATOR_DATA)
    SetIndexBuffer(2, levdn, INDICATOR_DATA)
    SetIndexBuffer(3, MaBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Alma (' + _str(AlmaPeriod) + ',' + _str(AlmaSigma) + _str(AlmaSample) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, TickVolume, Volume, Spread):
    global totalBars
    totalBars = rates_total
    fperiod = fltPeriod
    if fperiod <= 0:
        fperiod = AlmaPeriod
    pfilter = fltFilter
    if fltFilterOn == flt_val:
        pfilter = 0.0
    vfilter = fltFilter
    if fltFilterOn == flt_prc:
        vfilter = 0.0
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = iFilter(getPrice(AlmaPrice, open, close, high, low, rates_total, i), pfilter, fperiod, i, rates_total, 0)
        MaBuffer[i] = iFilter(iAlma(price, AlmaPeriod, AlmaSigma, AlmaSample, rates_total, i), vfilter, fperiod, i, rates_total, 1)
        min_ = MaBuffer[i]
        max_ = MaBuffer[i]
        k = 1
        while k < flLookBack and (i - k) >= 0:
            min_ = MathMin(MaBuffer[i - k], min_)
            max_ = MathMax(MaBuffer[i - k], max_)
            k += 1
        range_ = max_ - min_
        levup[i] = min_ + ((flLevelUp * range_) / 100.0)
        levdn[i] = min_ + ((flLevelDown * range_) / 100.0)
        levmi[i] = min_ + (0.5 * range_)
        ColorBuffer[i] = 0.0
        _sw1 = ColorOn
        if _sw1 == cl_slope:
            if i > 0:
                if MaBuffer[i] > MaBuffer[i - 1]:
                    ColorBuffer[i] = 1.0
                if MaBuffer[i] < MaBuffer[i - 1]:
                    ColorBuffer[i] = 2.0
        elif _sw1 == cl_mid:
            if MaBuffer[i] > levmi[i]:
                ColorBuffer[i] = 1.0
            if MaBuffer[i] < levmi[i]:
                ColorBuffer[i] = 2.0
        else:
            if MaBuffer[i] > levup[i]:
                ColorBuffer[i] = 1.0
            if MaBuffer[i] < levdn[i]:
                ColorBuffer[i] = 2.0
    return rates_total

def iFilter(tprice, filter_, period, i, bars, instanceNo=0):
    if filter_ <= 0:
        return tprice
    if ArrayRange(workFil, 0) != bars:
        ArrayResize(workFil, bars)
    instanceNo *= 3
    workFil[i][instanceNo + 2] = tprice
    if i < 1:
        return tprice
    workFil[i][instanceNo + 0] = MathAbs(workFil[i][instanceNo + 2] - workFil[i - 1][instanceNo + 2])
    workFil[i][instanceNo + 1] = workFil[i][instanceNo + 0]
    k = 1
    while k < period and (i - k) >= 0:
        workFil[i][instanceNo + 1] += workFil[i - k][instanceNo + 0]
        k += 1
    workFil[i][instanceNo + 1] = _fdiv(workFil[i][instanceNo + 1], period)
    stddev = 0.0
    k = 0
    while k < period and (i - k) >= 0:
        stddev += MathPow(workFil[i - k][instanceNo + 0] - workFil[i - k][instanceNo + 1], 2)
        k += 1
    stddev = MathSqrt(_fdiv(stddev, float(period)))
    filtev = filter_ * stddev
    if MathAbs(workFil[i][instanceNo + 2] - workFil[i - 1][instanceNo + 2]) < filtev:
        workFil[i][instanceNo + 2] = workFil[i - 1][instanceNo + 2]
    return workFil[i][instanceNo + 2]

def iAlma(price, period, sigma, sample, bars, r, instanceNo=0):
    if period <= 1:
        return price
    if ArrayRange(almaWork, 0) != bars:
        ArrayResize(almaWork, bars)
    almaWork[r][instanceNo] = price
    m = MathFloor(sample * (period - 1.0))
    s = _fdiv(period, sigma)
    sum_ = 0.0
    div = 0.0
    i = 0
    while i < period and (r - i) >= 0:
        coeff = MathExp(_fdiv(-((i - m) * (i - m)), 2.0 * s * s))
        sum_ += coeff * almaWork[r - i][instanceNo]
        div += coeff
        i += 1
    talma = price
    if div != 0:
        talma = _fdiv(sum_, div)
    return talma

def getPrice(price, open, close, high, low, bars, i, instanceNo=0):
    if price >= pr_haclose:
        if ArrayRange(workHa, 0) != bars:
            ArrayResize(workHa, bars)
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
        _sw2 = price
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
    _sw3 = price
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


class Alma13(_MQL5Indicator):
    name = 'Alma_1_3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AlmaPeriod': 14,  # Calculation period
        'AlmaPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=0),  # Price to use
        'AlmaSigma': 6.0,  # Alma sigma
        'AlmaSample': 0.25,  # Alma sample
        'ColorOn': _Choice({0: 'Change color on slope change', 1: 'Change color on middle level cross', 2: 'Change color on outer levels cross'}, default=2),  # Color change on :
        'flLookBack': 25,  # Floating levels look back period
        'flLevelUp': 90.0,  # Floating levels up level %
        'flLevelDown': 10.0,  # Floating levels down level %
        'fltPeriod': 0,  # Filter period (<= 0 to use alma period
        'fltFilter': 0.0,  # Filter value (<=0 for no filtering)
        'fltFilterOn': _Choice({0: 'Filter the value (alma)', 1: 'Filter the price', 2: 'Filter all'}, default=0),  # Filter to be applied to :
    }

