"""BB_stops_-_rsi — converted from MQL5: MQL5 Indicators/BB Stops - RSI/BB_stops_-_rsi.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'separate', 'indicator_buffers': 11, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 12}, 'colors': {1: [8421504], 2: [8421504], 3: [12632256], 4: [16748574], 5: [6333684], 6: [12632256, 16748574, 6333684]}, 'widths': {4: 3, 5: 3, 6: 2}, 'styles': {1: 2, 2: 2, 3: 1}, 'labels': {}, 'levels': [], 'description': [], 'name': 'BB_stops_-_rsi', 'source': 'MQL5 Indicators/BB Stops - RSI/BB_stops_-_rsi.mq5', 'folder': 'BB Stops - RSI', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'int', 'default': 32, 'label': 'RSI period', 'sinput': False}, {'mql': 'RsiType', 'py': 'RsiType', 'param': 'RsiType', 'type': 'int', 'default': 4, 'label': 'RSI type', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'MaPeriod', 'py': 'MaPeriod', 'param': 'MaPeriod', 'type': 'int', 'default': 20, 'label': 'Bollinger bands period', 'sinput': False}, {'mql': 'MaMethod', 'py': 'MaMethod', 'param': 'MaMethod', 'type': 'int', 'default': 0, 'label': 'Moving average method', 'sinput': False}, {'mql': 'DeviationPeriod', 'py': 'DeviationPeriod', 'param': 'DeviationPeriod', 'type': 'int', 'default': 20, 'label': 'Deviations period', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 1.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'DeviationSample', 'py': 'DeviationSample', 'param': 'DeviationSample', 'type': 'bool', 'default': False, 'label': 'Deviation sample correction?', 'sinput': False}, {'mql': 'Risk', 'py': 'Risk', 'param': 'Risk', 'type': 'double', 'default': 1.0, 'label': 'Risk', 'sinput': False}, {'mql': 'AlertsOn', 'py': 'AlertsOn', 'param': 'AlertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'AlertsOnCurrent', 'py': 'AlertsOnCurrent', 'param': 'AlertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'AlertsMessage', 'py': 'AlertsMessage', 'param': 'AlertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messages on alerts?', 'sinput': False}, {'mql': 'AlertsSound', 'py': 'AlertsSound', 'param': 'AlertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'AlertsEmail', 'py': 'AlertsEmail', 'param': 'AlertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'AlertsNotify', 'py': 'AlertsNotify', 'param': 'AlertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data ?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

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
RsiPeriod = _input('RsiPeriod', 32)  # RSI period
RsiType = _input('RsiType', rsi_rsi)  # RSI type
Price = _input('Price', pr_close)  # Price
MaPeriod = _input('MaPeriod', 20)  # Bollinger bands period
MaMethod = _input('MaMethod', ma_sma)  # Moving average method
DeviationPeriod = _input('DeviationPeriod', 20)  # Deviations period
Deviation = _input('Deviation', 1.0)  # Deviation
DeviationSample = _input('DeviationSample', False)  # Deviation sample correction?
Risk = _input('Risk', 1.0)  # Risk
AlertsOn = _input('AlertsOn', False)  # Turn alerts on?
AlertsOnCurrent = _input('AlertsOnCurrent', True)  # Alert on current bar?
AlertsMessage = _input('AlertsMessage', True)  # Display messages on alerts?
AlertsSound = _input('AlertsSound', False)  # Play sound on alerts?
AlertsEmail = _input('AlertsEmail', False)  # Send email on alerts?
AlertsNotify = _input('AlertsNotify', False)  # Send push notification on alerts?
Interpolate = _input('Interpolate', True)  # Interpolate mtf data ?
rsi = Arr(0, 0.0)
bba = Arr(0, 0.0)
bbc = Arr(0, 0.0)
bblu = Arr(0, 0.0)
bbld = Arr(0, 0.0)
amax = Arr(0, 0.0)
amin = Arr(0, 0.0)
bmax = Arr(0, 0.0)
bmin = Arr(0, 0.0)
trend = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
timeFrame = 0
workRsi = Arr(0, 0.0, dims=(39,))
workDev = Arr(0, 0.0, dims=(1,))
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))
workHa = Arr(0, 0.0, dims=(4,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global timeFrame
    SetIndexBuffer(0, bmax, INDICATOR_DATA)
    SetIndexBuffer(1, bmin, INDICATOR_DATA)
    SetIndexBuffer(2, rsi, INDICATOR_DATA)
    SetIndexBuffer(3, bblu, INDICATOR_DATA)
    SetIndexBuffer(4, bbld, INDICATOR_DATA)
    SetIndexBuffer(5, bba, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_ARROW, 159)
    SetIndexBuffer(6, bbc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, amax, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, amin, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, count, INDICATOR_CALCULATIONS)
    timeFrame = MathMax(Period(), TimeFrame)
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' bb stops ' + getRsiName(RsiType) + ' (' + _str(RsiPeriod) + ',' + _str(MaPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tickVolume, volume, spread):
    global _mtfHandle
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if timeFrame != Period():
        result = Arr(0, 0.0)
        currTime = Arr(0, 0)
        nextTime = Arr(0, 0)
        if not timeFrameCheck(timeFrame, time):
            return 0
        if _mtfHandle == INVALID_HANDLE:
            _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, RsiPeriod, RsiType, Price, MaPeriod, MaMethod, DeviationPeriod, Deviation, DeviationSample, Risk, AlertsOn, AlertsOnCurrent, AlertsMessage, AlertsSound, AlertsEmail, AlertsNotify)
        if _mtfHandle == INVALID_HANDLE:
            return 0
        if CopyBuffer(_mtfHandle, 10, 0, 1, result) == -1:
            return 0
        k = 0
        n = 0
        i = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _idiv(_int(result[0]) * PeriodSeconds(timeFrame), PeriodSeconds(Period())) - 1, 0))
        while i < rates_total:
            if CopyBuffer(_mtfHandle, 0, _DT(time[i]), 1, result) == -1:
                break
            bmax[i] = result[0]
            if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) == -1:
                break
            bmin[i] = result[0]
            if CopyBuffer(_mtfHandle, 2, _DT(time[i]), 1, result) == -1:
                break
            rsi[i] = result[0]
            if CopyBuffer(_mtfHandle, 3, _DT(time[i]), 1, result) == -1:
                break
            bblu[i] = result[0]
            if CopyBuffer(_mtfHandle, 4, _DT(time[i]), 1, result) == -1:
                break
            bbld[i] = result[0]
            if CopyBuffer(_mtfHandle, 6, _DT(time[i]), 1, result) == -1:
                break
            bbc[i] = result[0]
            bba[i] = (((bblu[i] if (bbc[i] == 1) else bbld[i]) if (bbc[i] != bbc[i - 1]) else EMPTY_VALUE) if (i > 0) else EMPTY_VALUE)
            if not Interpolate:
                i += 1
                continue
            CopyTime(Symbol(), timeFrame, _DT(time[i]), 1, currTime)
            if i < (rates_total - 1):
                CopyTime(Symbol(), timeFrame, _DT(time[i + 1]), 1, nextTime)
                if currTime[0] == nextTime[0]:
                    i += 1
                    continue
            n = 1
            while (i - n) > 0 and time[i - n] >= currTime[0]:
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                rsi[i - k] = rsi[i] + _fdiv((rsi[i - n] - rsi[i]) * k, n)
                bmax[i - k] = bmax[i] + _fdiv((bmax[i - n] - bmax[i]) * k, n)
                bmin[i - k] = bmin[i] + _fdiv((bmin[i - n] - bmin[i]) * k, n)
                if bbc[i - k] == 1:
                    bblu[i - k] = bmin[i - k]
                if bbc[i - k] == 2:
                    bbld[i - k] = bmax[i - k]
                if bba[i - k] != EMPTY_VALUE:
                    bba[i - k] = (bblu[i - k] if (bbc[i - k] == 1) else bbld[i - k])
                k += 1
            i += 1
        return i
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        rsi[i] = iRsi(RsiType, getPrice(Price, open, close, high, low, i, rates_total, 0), RsiPeriod, i, rates_total)
        dev = iDeviation(rsi[i], DeviationPeriod, DeviationSample, i, rates_total)
        ma = iCustomMa(MaMethod, rsi[i], MaPeriod, i, rates_total, 0)
        amax[i] = ma + (dev * Deviation)
        amin[i] = ma - (dev * Deviation)
        bmax[i] = amax[i] + (0.5 * (Risk - 1) * (amax[i] - amin[i]))
        bmin[i] = amin[i] - (0.5 * (Risk - 1) * (amax[i] - amin[i]))
        trend[i] = ((1 if (rsi[i] > amax[i - 1]) else -1 if (rsi[i] < amin[i - 1]) else trend[i - 1]) if (i > 0) else 0)
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
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    manageAlerts(time, bbc, rates_total)
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
        return 50.0 * (_fdiv(workRsi[r][z + 1], MathMax(workRsi[r][z + 2], DBL_MIN)) + 1)
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
            workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (_fdiv(1, MathMax(period, 1)) * (_fdiv(100 * up, MathMax(up + dn, DBL_MIN)) - workRsi[r - 1][z + 1]))
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
        return _fdiv(100 * up, MathMax(up + dn, DBL_MIN))
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
        return _fdiv(50 * (up - dn), MathMax(up + dn, DBL_MIN)) + 50
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
        workRsi[r][instanceNo + 1] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(sump, MathMax(sumn, DBL_MIN)))
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
        workRsi[r][instanceNo + 1] = 100 - _fdiv(100, 1.0 + _fdiv(avgUp, MathMax(avgDn, DBL_MIN)))
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
        return MathMax(MathMin((_fdiv(mom, MathMax(moa, DBL_MIN)) + 1.0) * 50.0, 100.0), 0.0)
    return 0.0

def iDeviation(value, length, isSample, i, bars, instanceNo=0):
    if ArrayRange(workDev, 0) != bars:
        ArrayResize(workDev, bars)
    workDev[i][instanceNo] = value
    oldMean = value
    newMean = value
    squares = 0.0
    k = 0
    k = 1
    while k < length and (i - k) >= 0:
        newMean = _fdiv(workDev[i - k][instanceNo] - oldMean, k + 1) + oldMean
        squares += (workDev[i - k][instanceNo] - oldMean) * (workDev[i - k][instanceNo] - newMean)
        oldMean = newMean
        k += 1
    return MathSqrt(_fdiv(squares, MathMax(k - isSample, 1)))

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
    k = 1
    workSma[r][instanceNo + 0] = price
    avg = price
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo + 0]
        k += 1
    avg = _fdiv(avg, float(k))
    return avg

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
        _sw4 = tprice
        if _sw4 == pr_haclose:
            return haClose
        elif _sw4 == pr_haopen:
            return haOpen
        elif _sw4 == pr_hahigh:
            return haHigh
        elif _sw4 == pr_halow:
            return haLow
        elif _sw4 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw4 == pr_hamedianb:
            return (haOpen + haClose) / 2.0
        elif _sw4 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw4 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw4 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw4 == pr_hatbiased:
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
        elif _sw4 == pr_hatbiased2:
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw5 = tprice
    if _sw5 == pr_close:
        return close[i]
    elif _sw5 == pr_open:
        return open[i]
    elif _sw5 == pr_high:
        return high[i]
    elif _sw5 == pr_low:
        return low[i]
    elif _sw5 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw5 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw5 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw5 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw5 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw5 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
    elif _sw5 == pr_tbiased2:
        if close[i] > open[i]:
            return high[i]
        if close[i] < open[i]:
            return low[i]
        return close[i]
    return 0.0

def manageAlerts(_time, _trend, bars):
    if AlertsOn:
        whichBar = bars - 1
        if not AlertsOnCurrent:
            whichBar = bars - 2
        time1 = _time[whichBar]
        if _trend[whichBar] != _trend[whichBar - 1]:
            if _trend[whichBar] == 1:
                doAlert(time1, ' up')
            if _trend[whichBar] == 2:
                doAlert(time1, ' down')

def doAlert(forTime, doWhat):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        message = timeFrameToString(Period()) + ' ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' ' + Symbol() + ' bb stops ' + getRsiName(RsiType) + ' state changed to ' + doWhat
        if AlertsMessage:
            Alert(message)
        if AlertsEmail:
            SendMail(Symbol() + ' bb stops ' + getRsiName(RsiType), message)
        if AlertsNotify:
            SendNotification(message)
        if AlertsSound:
            PlaySound('alert2.wav')

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
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0
_s_timeFrameCheck_warned = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBStopsRsi(_MQL5Indicator):
    name = 'BB_stops_-_rsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'RsiPeriod': 32,  # RSI period
        'RsiType': _Choice({0: "Cuttler's RSI", 1: "Ehlers' smoothed RSI", 2: "Harris' RSI", 3: 'Rapid RSI', 4: 'RSI', 5: 'RSX', 6: 'Slow RSI'}, default=4),  # RSI type
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'MaPeriod': 20,  # Bollinger bands period
        'MaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Moving average method
        'DeviationPeriod': 20,  # Deviations period
        'Deviation': 1.0,  # Deviation
        'DeviationSample': False,  # Deviation sample correction?
        'Risk': 1.0,  # Risk
        'AlertsOn': False,  # Turn alerts on?
        'AlertsOnCurrent': True,  # Alert on current bar?
        'AlertsMessage': True,  # Display messages on alerts?
        'AlertsSound': False,  # Play sound on alerts?
        'AlertsEmail': False,  # Send email on alerts?
        'AlertsNotify': False,  # Send push notification on alerts?
        'Interpolate': True,  # Interpolate mtf data ?
    }

