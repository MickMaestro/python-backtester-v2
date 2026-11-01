"""Corr_average — converted from MQL5: MQL5 Indicators/Corr average/Corr_average.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 8, 4: 8}, 'colors': {1: [14474460], 2: [8421504], 3: [11119017, 3329330, 36095], 4: [11119017, 3329330, 36095]}, 'widths': {4: 3}, 'styles': {2: 2}, 'labels': {1: 'Corrected average zone', 2: 'Corrected average middle', 3: 'Corrected average original', 4: 'Corrected average '}, 'levels': [], 'description': [], 'name': 'Corr_average', 'source': 'MQL5 Indicators/Corr average/Corr_average.mq5', 'folder': 'Corr average', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'AvgMethod', 'py': 'AvgMethod', 'param': 'AvgMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'AvgPeriod', 'py': 'AvgPeriod', 'param': 'AvgPeriod', 'type': 'int', 'default': 14, 'label': 'Average period', 'sinput': False}, {'mql': 'AvgPrice', 'py': 'AvgPrice', 'param': 'AvgPrice', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'CorrectionPeriod', 'py': 'CorrectionPeriod', 'param': 'CorrectionPeriod', 'type': 'int', 'default': 0, 'label': '"Correction" period (<0 no correction,0 to 1 same as average)', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 3, 'label': 'Color change on :', 'sinput': False}, {'mql': 'FlPeriod', 'py': 'FlPeriod', 'param': 'FlPeriod', 'type': 'int', 'default': 25, 'label': 'Period for finding floating levels', 'sinput': False}, {'mql': 'FlUp', 'py': 'FlUp', 'param': 'FlUp', 'type': 'double', 'default': 90.0, 'label': 'Upper level %', 'sinput': False}, {'mql': 'FlDown', 'py': 'FlDown', 'param': 'FlDown', 'type': 'double', 'default': 10.0, 'label': 'Lower level %', 'sinput': False}, {'mql': 'AlertsOn', 'py': 'AlertsOn', 'param': 'AlertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'AlertsOnCurrent', 'py': 'AlertsOnCurrent', 'param': 'AlertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'AlertsMessage', 'py': 'AlertsMessage', 'param': 'AlertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'AlertsSound', 'py': 'AlertsSound', 'param': 'AlertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'AlertsEmail', 'py': 'AlertsEmail', 'param': 'AlertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'AlertsNotify', 'py': 'AlertsNotify', 'param': 'AlertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate when in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum chgColor
chg_onSlope = 0
chg_onLevel = 1
chg_onMiddle = 2
chg_onOrig = 3
_enum('chgColor', {0: 'chg_onSlope', 1: 'chg_onLevel', 2: 'chg_onMiddle', 3: 'chg_onOrig'})

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
AvgMethod = _input('AvgMethod', ma_ema)  # Average method
AvgPeriod = _input('AvgPeriod', 14)  # Average period
AvgPrice = _input('AvgPrice', pr_close)  # Price
CorrectionPeriod = _input('CorrectionPeriod', 0)  # "Correction" period (<0 no correction,0 to 1 same as average)
ColorOn = _input('ColorOn', chg_onOrig)  # Color change on :
FlPeriod = _input('FlPeriod', 25)  # Period for finding floating levels
FlUp = _input('FlUp', 90.0)  # Upper level %
FlDown = _input('FlDown', 10.0)  # Lower level %
AlertsOn = _input('AlertsOn', False)  # Turn alerts on?
AlertsOnCurrent = _input('AlertsOnCurrent', True)  # Alert on current bar?
AlertsMessage = _input('AlertsMessage', True)  # Display messageas on alerts?
AlertsSound = _input('AlertsSound', False)  # Play sound on alerts?
AlertsEmail = _input('AlertsEmail', False)  # Send email on alerts?
AlertsNotify = _input('AlertsNotify', False)  # Send push notification on alerts?
Interpolate = _input('Interpolate', True)  # Interpolate when in multi time frame mode?
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
mid = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
count = Arr(0, 0.0)
orig = Arr(0, 0.0)
origc = Arr(0, 0.0)
_maNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
_mtfHandle = INVALID_HANDLE
timeFrame = 0
workSma = Arr(0, 0.0, dims=(4,))
workEma = Arr(0, 0.0, dims=(4,))
workSmma = Arr(0, 0.0, dims=(4,))
workLwma = Arr(0, 0.0, dims=(4,))
workDev = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(4,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global timeFrame
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, mid, INDICATOR_DATA)
    SetIndexBuffer(3, orig, INDICATOR_DATA)
    SetIndexBuffer(4, origc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, val, INDICATOR_DATA)
    SetIndexBuffer(6, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, count, INDICATOR_CALCULATIONS)
    timeFrame = MathMax(Period(), TimeFrame)
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' "Corrected" ' + _maNames[AvgMethod] + ' (' + _str(AvgPeriod) + ',' + _str(CorrectionPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
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
            _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, AvgMethod, AvgPeriod, AvgPrice, CorrectionPeriod, ColorOn, FlPeriod, FlUp, FlDown, AlertsOn, AlertsOnCurrent, AlertsMessage, AlertsSound, AlertsEmail, AlertsNotify)
        if _mtfHandle == INVALID_HANDLE:
            return 0
        if CopyBuffer(_mtfHandle, 7, 0, 1, result) == -1:
            return 0
        k = 0
        n = 0
        i = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _idiv(_int(result[0]) * PeriodSeconds(timeFrame), PeriodSeconds(Period())) - 1, 0))
        while i < rates_total:
            if CopyBuffer(_mtfHandle, 0, _DT(time[i]), 1, result) == -1:
                break
            fup[i] = result[0]
            if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) == -1:
                break
            fdn[i] = result[0]
            if CopyBuffer(_mtfHandle, 2, _DT(time[i]), 1, result) == -1:
                break
            mid[i] = result[0]
            if CopyBuffer(_mtfHandle, 3, _DT(time[i]), 1, result) == -1:
                break
            orig[i] = result[0]
            if CopyBuffer(_mtfHandle, 4, _DT(time[i]), 1, result) == -1:
                break
            origc[i] = result[0]
            if CopyBuffer(_mtfHandle, 5, _DT(time[i]), 1, result) == -1:
                break
            val[i] = result[0]
            if CopyBuffer(_mtfHandle, 6, _DT(time[i]), 1, result) == -1:
                break
            valc[i] = result[0]
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
                fup[i - k] = fup[i] + _fdiv((fup[i - n] - fup[i]) * k, n)
                fdn[i - k] = fdn[i] + _fdiv((fdn[i - n] - fdn[i]) * k, n)
                mid[i - k] = mid[i] + _fdiv((mid[i - n] - mid[i]) * k, n)
                orig[i - k] = orig[i] + _fdiv((orig[i - n] - orig[i]) * k, n)
                val[i - k] = val[i] + _fdiv((val[i - n] - val[i]) * k, n)
                k += 1
            i += 1
        return i
    deviationsPeriod = (CorrectionPeriod if (CorrectionPeriod > 0) else 0 if (CorrectionPeriod < 0) else AvgPeriod)
    colorOn = (ColorOn if (FlPeriod > 1 and deviationsPeriod > 1) else ColorOn if (ColorOn != chg_onOrig) else chg_onSlope)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(AvgPrice, open, close, high, low, i, rates_total)
        orig[i] = iCustomMa(AvgMethod, price, AvgPeriod, i, rates_total)
        v1 = MathPow(iDeviation(price, deviationsPeriod, False, i, rates_total), 2)
        v2 = (MathPow(val[i - 1] - orig[i], 2) if (i > 0) else 0)
        c = (0 if (v2 < v1 or v2 == 0) else (1 - _fdiv(v1, v2)))
        val[i] = ((val[i - 1] + (c * (orig[i] - val[i - 1]))) if (i > 0) else orig[i])
        start = MathMax(i - FlPeriod + 1, 0)
        min_ = val[ArrayMinimum(val, start, FlPeriod)]
        max_ = val[ArrayMaximum(val, start, FlPeriod)]
        range_ = max_ - min_
        fup[i] = min_ + ((FlUp * range_) / 100.0)
        fdn[i] = min_ + ((FlDown * range_) / 100.0)
        mid[i] = (fup[i] + fdn[i]) * 0.5
        _sw1 = colorOn
        if _sw1 == chg_onLevel:
            valc[i] = (1 if (val[i] > fup[i]) else 2 if (val[i] < fdn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        elif _sw1 == chg_onMiddle:
            valc[i] = (1 if (val[i] > mid[i]) else 2 if (val[i] < mid[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        elif _sw1 == chg_onOrig:
            valc[i] = (1 if (val[i] < orig[i]) else 2 if (val[i] > orig[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        else:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        origc[i] = (1 if (orig[i] > val[i]) else 2 if (orig[i] < val[i]) else origc[i - 1] if (i > 0) else 0)
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    manageAlerts(time, valc, rates_total)
    return rates_total

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw2 = mode
    if _sw2 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw2 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw2 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw2 == ma_lwma:
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

def iDeviation(value, length, isSample, i, bars):
    if ArraySize(workDev) != bars:
        ArrayResize(workDev, bars)
    workDev[i] = value
    oldMean = value
    newMean = value
    squares = 0.0
    k = 0
    k = 1
    while k < length and (i - k) >= 0:
        newMean = _fdiv(workDev[i - k] - oldMean, k + 1) + oldMean
        squares += (workDev[i - k] - oldMean) * (workDev[i - k] - newMean)
        oldMean = newMean
        k += 1
    return MathSqrt(_fdiv(squares, MathMax(k - isSample, 1)))

def manageAlerts(_time, _trend, bars):
    if AlertsOn:
        whichBar = bars - 1
        if not AlertsOnCurrent:
            whichBar = bars - 2
        time1 = _time[whichBar]
        if _trend[whichBar] != _trend[whichBar - 1]:
            add = 'slope changed to'
            _sw3 = ColorOn
            if _sw3 == chg_onLevel:
                add = 'outer level crossed'
            elif _sw3 == chg_onOrig:
                add = _maNames[AvgMethod] + ' value crossed'
            elif _sw3 == chg_onMiddle:
                add = 'middle level crossed'
            if _trend[whichBar] == 1:
                doAlert(time1, add + ' up')
            if _trend[whichBar] == 2:
                doAlert(time1, add + ' down')

def doAlert(forTime, doWhat):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        message = TimeToString(TimeLocal(), TIME_SECONDS) + ' ' + Symbol() + ' ' + _maNames[AvgMethod] + ' state changed to ' + doWhat
        if AlertsMessage:
            Alert(message)
        if AlertsEmail:
            SendMail(Symbol() + ' ' + _maNames[AvgMethod] + ' corrected', message)
        if AlertsNotify:
            SendNotification(message)
        if AlertsSound:
            PlaySound('alert2.wav')

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


class CorrAverage(_MQL5Indicator):
    name = 'Corr_average'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'AvgMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=1),  # Average method
        'AvgPeriod': 14,  # Average period
        'AvgPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'CorrectionPeriod': 0,  # "Correction" period (<0 no correction,0 to 1 same as average)
        'ColorOn': _Choice({0: 'change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross', 3: 'Change color on average value cross'}, default=3),  # Color change on :
        'FlPeriod': 25,  # Period for finding floating levels
        'FlUp': 90.0,  # Upper level %
        'FlDown': 10.0,  # Lower level %
        'AlertsOn': False,  # Turn alerts on?
        'AlertsOnCurrent': True,  # Alert on current bar?
        'AlertsMessage': True,  # Display messageas on alerts?
        'AlertsSound': False,  # Play sound on alerts?
        'AlertsEmail': False,  # Send email on alerts?
        'AlertsNotify': False,  # Send push notification on alerts?
        'Interpolate': True,  # Interpolate when in multi time frame mode?
    }

