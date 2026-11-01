"""RSI_adaptive_T3_pre-filtered_1.2 — converted from MQL5: MQL5 Indicators/RSI - of adaptive T3/RSI_adaptive_T3_pre-filtered_1.2.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 11, 2: 8}, 'colors': {2: [3329330, 42495]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'RSi of adaptive T3', 2: 'RSi of adaptive T3'}, 'levels': [], 'description': [], 'name': 'RSI_adaptive_T3_pre-filtered_1.2', 'source': 'MQL5 Indicators/RSI - of adaptive T3/RSI_adaptive_T3_pre-filtered_1.2.mq5', 'folder': 'RSI - of adaptive T3', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'int', 'default': 25, 'label': 'Rsi period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'RsiType', 'py': 'RsiType', 'param': 'RsiType', 'type': 'int', 'default': 3, 'label': 'Rsi type', 'sinput': False}, {'mql': 'T3Period', 'py': 'T3Period', 'param': 'T3Period', 'type': 'double', 'default': 15.0, 'label': 'T3 Calculation period', 'sinput': False}, {'mql': 'T3Hot', 'py': 'T3Hot', 'param': 'T3Hot', 'type': 'double', 'default': 0.7, 'label': 'T3 hot value', 'sinput': False}, {'mql': 'T3Original', 'py': 'T3Original', 'param': 'T3Original', 'type': 'bool', 'default': True, 'label': 'Original Tillson T3 calculation?', 'sinput': False}, {'mql': 'LevelUp', 'py': 'LevelUp', 'param': 'LevelUp', 'type': 'double', 'default': 80.0, 'label': 'Level up', 'sinput': False}, {'mql': 'LevelDown', 'py': 'LevelDown', 'param': 'LevelDown', 'type': 'double', 'default': 20.0, 'label': 'Level down', 'sinput': False}, {'mql': 'AdaptivePeriod', 'py': 'AdaptivePeriod', 'param': 'AdaptivePeriod', 'type': 'int', 'default': 25, 'label': 'Period for adapting', 'sinput': False}, {'mql': 'ColorSteps', 'py': 'ColorSteps', 'param': 'ColorSteps', 'type': 'int', 'default': 20, 'label': 'Color steps for drawing', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 17919, 'label': 'Color down', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Color Up', 'sinput': False}, {'mql': 'ShowLine', 'py': 'ShowLine', 'param': 'ShowLine', 'type': 'bool', 'default': True, 'label': 'Show colored line', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enRsiTypes
rsi_cut = 0
rsi_ehl = 1
rsi_har = 2
rsi_rap = 3
rsi_rsi = 4
rsi_rsx = 5
rsi_slo = 6
_enum('enRsiTypes', {0: 'rsi_cut', 1: 'rsi_ehl', 2: 'rsi_har', 3: 'rsi_rap', 4: 'rsi_rsi', 5: 'rsi_rsx', 6: 'rsi_slo'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
RsiPeriod = _input('RsiPeriod', 25)  # Rsi period
Price = _input('Price', pr_close)  # Price to use
RsiType = _input('RsiType', rsi_rap)  # Rsi type
T3Period = _input('T3Period', 15.0)  # T3 Calculation period
T3Hot = _input('T3Hot', 0.7)  # T3 hot value
T3Original = _input('T3Original', True)  # Original Tillson T3 calculation?
LevelUp = _input('LevelUp', 80.0)  # Level up
LevelDown = _input('LevelDown', 20.0)  # Level down
AdaptivePeriod = _input('AdaptivePeriod', 25)  # Period for adapting
ColorSteps = _input('ColorSteps', 20)  # Color steps for drawing
ColorFrom = _input('ColorFrom', clrOrangeRed)  # Color down
ColorTo = _input('ColorTo', clrLimeGreen)  # Color Up
ShowLine = _input('ShowLine', True)  # Show colored line
Interpolate = _input('Interpolate', True)  # Interpolate in multi time frame mode?
rsi = Arr(0, 0.0)
rsic = Arr(0, 0.0)
rsiha = Arr(0, 0.0)
rsihb = Arr(0, 0.0)
rsihc = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
timeFrame = 0
cSteps = 0
workRsi = Arr(0, 0.0, dims=(13,))
workDev = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(2,))
workT3 = Arr(0, 0.0, dims=(6,))
workT3Coeffs = Arr(0, 0.0, dims=(6,))
workHa = Arr(0, 0.0, dims=(4,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _mtfHandle, cSteps, timeFrame
    SetIndexBuffer(0, rsiha, INDICATOR_DATA)
    SetIndexBuffer(1, rsihb, INDICATOR_DATA)
    SetIndexBuffer(2, rsihc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, rsi, INDICATOR_DATA)
    SetIndexBuffer(4, rsic, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, count, INDICATOR_CALCULATIONS)
    cSteps = (ColorSteps if (ColorSteps > 1) else 2)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, cSteps)
    PlotIndexSetInteger(1, PLOT_COLOR_INDEXES, cSteps)
    i = 0
    while i < cSteps:
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, gradientColor(i, cSteps, ColorFrom, ColorTo))
        i += 1
    if ShowLine:
        i = 0
        while i < cSteps:
            PlotIndexSetInteger(1, PLOT_LINE_COLOR, i, gradientColor(i, cSteps, ColorFrom, ColorTo))
            i += 1
    else:
        for i in range(0, cSteps):
            PlotIndexSetInteger(1, PLOT_LINE_COLOR, i, clrNONE)
    timeFrame = MathMax(Period(), TimeFrame)
    if timeFrame != Period():
        _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, RsiPeriod, Price, RsiType, T3Period, T3Hot, T3Original, LevelUp, LevelDown, AdaptivePeriod, ColorSteps)
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' ' + getRsiName(RsiType) + ' T3 adaptive filtered (' + _str(RsiPeriod) + ',' + _str(T3Period) + ',' + _str(AdaptivePeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _mtfHandle
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if timeFrame != Period():
        result = Arr(0, 0.0)
        currTime = Arr(0, 0)
        nextTime = Arr(0, 0)
        if _mtfHandle == INVALID_HANDLE:
            _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, RsiPeriod, Price, RsiType, T3Period, T3Hot, T3Original, LevelUp, LevelDown, AdaptivePeriod, ColorSteps)
        if _mtfHandle == INVALID_HANDLE:
            return 0
        if CopyBuffer(_mtfHandle, 5, 0, 1, result) == -1:
            return 0
        i = 0
        k = 0
        n = 0
        limit = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _idiv(_int(result[0]) * PeriodSeconds(timeFrame), PeriodSeconds(Period())) - 1, 0))
        i = limit
        for i in range(i, rates_total):
            if CopyBuffer(_mtfHandle, 0, _DT(time[i]), 1, result) == -1:
                break
            rsiha[i] = result[0]
            if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) == -1:
                break
            rsihb[i] = result[0]
            if CopyBuffer(_mtfHandle, 2, _DT(time[i]), 1, result) == -1:
                break
            rsihc[i] = result[0]
            if CopyBuffer(_mtfHandle, 3, _DT(time[i]), 1, result) == -1:
                break
            rsi[i] = result[0]
            if CopyBuffer(_mtfHandle, 4, _DT(time[i]), 1, result) == -1:
                break
            rsic[i] = result[0]
            if not Interpolate:
                continue
            CopyTime(Symbol(), TimeFrame, _DT(time[i]), 1, currTime)
            if i < (rates_total - 1):
                CopyTime(Symbol(), TimeFrame, _DT(time[i + 1]), 1, nextTime)
                if currTime[0] == nextTime[0]:
                    continue
            n = 1
            while (i - n) > 0 and time[i - n] >= currTime[0]:
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                rsiha[i - k] = rsiha[i] + _fdiv((rsiha[i - n] - rsiha[i]) * k, n)
                rsihb[i - k] = rsihb[i] + _fdiv((rsihb[i - n] - rsihb[i]) * k, n)
                rsi[i - k] = rsi[i] + _fdiv((rsi[i - n] - rsi[i]) * k, n)
                k += 1
        else:
            i = _range_end(i, rates_total, 1)
        return i
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(Price, open, close, high, low, i, rates_total)
        dev = iDeviation(price, iSma(price, AdaptivePeriod, rates_total, i, 0), AdaptivePeriod, rates_total, i)
        avg = iSma(dev, AdaptivePeriod, rates_total, i, 1)
        period = (_fdiv(T3Period * avg, dev) if (dev != 0) else T3Period)
        rsi[i] = iRsi(RsiType, iT3(price, period, T3Hot, T3Original, i, rates_total, 0), RsiPeriod, i, rates_total)
        rsiha[i] = rsi[i]
        rsihb[i] = (LevelUp if (rsi[i] > LevelUp) else LevelDown if (rsi[i] < LevelDown) else rsi[i])
        rsic[i] = MathFloor((MathMin(rsi[i], 99.9999) * cSteps) / 100.0)
        rsihc[i] = rsic[i]
        i += 1
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    return i

def getRsiName(method):
    _sw1 = method
    if _sw1 == rsi_rsi:
        return 'RSI'
    elif _sw1 == rsi_rsx:
        return 'RSX'
    elif _sw1 == rsi_cut:
        return "Cuttler's RSI"
    elif _sw1 == rsi_har:
        return "Haris' RSI"
    elif _sw1 == rsi_rap:
        return 'Rapid RSI'
    elif _sw1 == rsi_slo:
        return 'Slow RSI'
    elif _sw1 == rsi_ehl:
        return "Ehlers' smoothed RSI"
    else:
        return ''

def iRsi(rsiMode, price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 13
    workRsi[r][z + 0] = price
    _sw2 = rsiMode
    if _sw2 == rsi_rsi:
        alpha = _fdiv(1.0, MathMax(period, 1))
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
            workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (alpha * (change - workRsi[r - 1][z + 1]))
            workRsi[r][z + 2] = workRsi[r - 1][z + 2] + (alpha * (MathAbs(change) - workRsi[r - 1][z + 2]))
        return 50.0 * (_fdiv(workRsi[r][z + 1], MathMax(workRsi[r][z + 2], 1e-16)) + 1)
    elif _sw2 == rsi_slo:
        up = 0.0
        dn = 0.0
        k = 0
        while k < _int(period) and (r - k - 1) >= 0:
            diff = workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0]
            if diff > 0:
                up += diff
            else:
                dn -= diff
            k += 1
        if r < 1:
            workRsi[r][z + 1] = 50.0
        else:
            workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (_fdiv(1, MathMax(period, 1)) * (_fdiv(100 * up, MathMax(up + dn, 1e-16)) - workRsi[r - 1][z + 1]))
        return workRsi[r][z + 1]
    elif _sw2 == rsi_rap:
        up = 0.0
        dn = 0.0
        k = 0
        while k < _int(period) and (r - k - 1) >= 0:
            diff = workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0]
            if diff > 0:
                up += diff
            else:
                dn -= diff
            k += 1
        return _fdiv(100 * up, MathMax(up + dn, 1e-16))
    elif _sw2 == rsi_ehl:
        up = 0.0
        dn = 0.0
        workRsi[r][z + 3] = (((workRsi[r][z + 0] + (2.0 * workRsi[r - 1][z + 0]) + workRsi[r - 2][z + 0]) / 4.0) if (r > 2) else price)
        k = 0
        while k < _int(period) and (r - k - 1) >= 0:
            diff = workRsi[r - k][z + 3] - workRsi[r - k - 1][z + 3]
            if diff > 0:
                up += diff
            else:
                dn -= diff
            k += 1
        return _fdiv(50 * (up - dn), MathMax(up + dn, 1e-16)) + 50
    elif _sw2 == rsi_cut:
        sump = 0.0
        sumn = 0.0
        k = 0
        while k < _int(period) and (r - k - 1) >= 0:
            diff = workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0]
            if diff > 0:
                sump += diff
            else:
                sumn -= diff
            k += 1
        workRsi[r][instanceNo + 1] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(sump, MathMax(sumn, 1e-16)))
        return workRsi[r][instanceNo + 1]
    elif _sw2 == rsi_har:
        avgUp = 0.0
        avgDn = 0.0
        up = 0.0
        dn = 0.0
        k = 0
        while k < _int(period) and (r - k - 1) >= 0:
            diff = workRsi[r - k][instanceNo + 0] - workRsi[r - k - 1][instanceNo + 0]
            if diff > 0:
                avgUp += diff
                up += 1
            else:
                avgDn -= diff
                dn += 1
            k += 1
        if up != 0:
            avgUp = _fdiv(avgUp, up)
        if dn != 0:
            avgDn = _fdiv(avgDn, dn)
        workRsi[r][instanceNo + 1] = 100 - _fdiv(100, 1.0 + _fdiv(avgUp, MathMax(avgDn, 1e-16)))
        return workRsi[r][instanceNo + 1]
    elif _sw2 == rsi_rsx:
        Kg = _fdiv(3.0, 2.0 + period)
        Hg = 1.0 - Kg
        if r < period:
            for k in range(1, 13):
                workRsi[r][k + z] = 0.0
            return 50.0
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
        return MathMax(MathMin((_fdiv(mom, MathMax(moa, 1e-16)) + 1.0) * 50.0, 100.0), 0.0)
    return 0.0

def iDeviation(price, dMA, period, totalBars, i):
    if ArrayRange(workDev, 0) != totalBars:
        ArrayResize(workDev, totalBars)
    workDev[i] = price
    dSum = 0.0
    k = 0
    while (i - k) >= 0 and k < period:
        dSum += (workDev[i - k] - dMA) * (workDev[i - k] - dMA)
        k += 1
    return MathSqrt(_fdiv(dSum, period))

def iSma(price, period, totalBars, r, instanceNo=0):
    if ArrayRange(workSma, 0) != totalBars:
        ArrayResize(workSma, totalBars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))

def iT3(price, period, hot, original, r, bars, instanceNo=0):
    if ArrayRange(workT3, 0) != bars:
        ArrayResize(workT3, bars)
    if ArrayRange(workT3Coeffs, 0) < (instanceNo + 1):
        ArrayResize(workT3Coeffs, instanceNo + 1)
    if workT3Coeffs[instanceNo][0] != period:
        workT3Coeffs[instanceNo][0] = period
        a = hot
        workT3Coeffs[instanceNo][1] = (-a) * a * a
        workT3Coeffs[instanceNo][2] = (3 * a * a) + (3 * a * a * a)
        workT3Coeffs[instanceNo][3] = (-6 * a * a) - (3 * a) - (3 * a * a * a)
        workT3Coeffs[instanceNo][4] = 1 + (3 * a) + (a * a * a) + (3 * a * a)
        if original:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 1.0 + period)
        else:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0))
    buffer = instanceNo * 6
    for k in range(0, 6):
        workT3[r][k + buffer] = price
    if r > 1 and period > 1:
        workT3[r][0 + buffer] = workT3[r - 1][0 + buffer] + (workT3Coeffs[instanceNo][5] * (price - workT3[r - 1][0 + buffer]))
        workT3[r][1 + buffer] = workT3[r - 1][1 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][0 + buffer] - workT3[r - 1][1 + buffer]))
        workT3[r][2 + buffer] = workT3[r - 1][2 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][1 + buffer] - workT3[r - 1][2 + buffer]))
        workT3[r][3 + buffer] = workT3[r - 1][3 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][2 + buffer] - workT3[r - 1][3 + buffer]))
        workT3[r][4 + buffer] = workT3[r - 1][4 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][3 + buffer] - workT3[r - 1][4 + buffer]))
        workT3[r][5 + buffer] = workT3[r - 1][5 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][4 + buffer] - workT3[r - 1][5 + buffer]))
    return (workT3Coeffs[instanceNo][1] * workT3[r][5 + buffer]) + (workT3Coeffs[instanceNo][2] * workT3[r][4 + buffer]) + (workT3Coeffs[instanceNo][3] * workT3[r][3 + buffer]) + (workT3Coeffs[instanceNo][4] * workT3[r][2 + buffer])

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
        _sw3 = tprice
        if _sw3 == pr_haclose:
            return haClose
        elif _sw3 == pr_haopen:
            return haOpen
        elif _sw3 == pr_hahigh:
            return haHigh
        elif _sw3 == pr_halow:
            return haLow
        elif _sw3 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw3 == pr_hamedianb:
            return (haOpen + haClose) / 2.0
        elif _sw3 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw3 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw3 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw3 == pr_hatbiased:
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
        elif _sw3 == pr_hatbiased2:
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw4 = tprice
    if _sw4 == pr_close:
        return close[i]
    elif _sw4 == pr_open:
        return open[i]
    elif _sw4 == pr_high:
        return high[i]
    elif _sw4 == pr_low:
        return low[i]
    elif _sw4 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw4 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw4 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw4 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw4 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw4 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
    elif _sw4 == pr_tbiased2:
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

def getColor(stepNo, totalSteps, from_, to):
    stes = float(totalSteps) - 1.0
    step = _fdiv(from_ - to, stes)
    return _uint(round(from_ - (step * stepNo)))

def gradientColor(step, totalSteps, from_, to):
    newBlue = getColor(step, totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(step, totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(step, totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIAdaptiveT3PreFiltered12(_MQL5Indicator):
    name = 'RSI_adaptive_T3_pre-filtered_1.2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'RsiPeriod': 25,  # Rsi period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price to use
        'RsiType': _Choice({0: "Cuttler's RSI", 1: "Ehlers' smoothed RSI", 2: "Harris' RSI", 3: 'Rapid RSI', 4: 'RSI', 5: 'RSX', 6: 'Slow RSI'}, default=3),  # Rsi type
        'T3Period': 15.0,  # T3 Calculation period
        'T3Hot': 0.7,  # T3 hot value
        'T3Original': True,  # Original Tillson T3 calculation?
        'LevelUp': 80.0,  # Level up
        'LevelDown': 20.0,  # Level down
        'AdaptivePeriod': 25,  # Period for adapting
        'ColorSteps': 20,  # Color steps for drawing
        'ShowLine': True,  # Show colored line
        'Interpolate': True,  # Interpolate in multi time frame mode?
    }

