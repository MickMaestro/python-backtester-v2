"""Gann_high-low_activator_2 — converted from MQL5: MQL5 Indicators/Gann High Low Activator/Gann_high-low_activator_2.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 8}, 'colors': {1: [14474460, 14474460], 2: [8421504], 3: [6908265, 3329330, 36095]}, 'widths': {3: 2}, 'styles': {2: 2}, 'labels': {1: 'Gann zone', 2: 'Gann middle', 3: 'Gann high/low'}, 'levels': [], 'description': [], 'name': 'Gann_high-low_activator_2', 'source': 'MQL5 Indicators/Gann High Low Activator/Gann_high-low_activator_2.mq5', 'folder': 'Gann High Low Activator', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'AvgPeriod', 'py': 'AvgPeriod', 'param': 'AvgPeriod', 'type': 'int', 'default': 10, 'label': 'Average period', 'sinput': False}, {'mql': 'AvgType', 'py': 'AvgType', 'param': 'AvgType', 'type': 'int', 'default': 0, 'label': 'Average method', 'sinput': False}, {'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'double', 'default': 0.0, 'label': 'Filter to use (<=0 for no filter)', 'sinput': False}, {'mql': 'FilterOn', 'py': 'FilterOn', 'param': 'FilterOn', 'type': 'int', 'default': 0, 'label': 'Filter :', 'sinput': False}, {'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'alertsOnCurrent', 'py': 'alertsOnCurrent', 'param': 'alertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'alertsMessage', 'py': 'alertsMessage', 'param': 'alertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'alertsNotify', 'py': 'alertsNotify', 'param': 'alertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data ?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# enum enFilterWhat
flt_prc = 0
flt_val = 1
flt_all = 2
_enum('enFilterWhat', {0: 'flt_prc', 1: 'flt_val', 2: 'flt_all'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
AvgPeriod = _input('AvgPeriod', 10)  # Average period
AvgType = _input('AvgType', ma_sma)  # Average method
Filter = _input('Filter', 0.0)  # Filter to use (<=0 for no filter)
FilterOn = _input('FilterOn', flt_prc)  # Filter :
alertsOn = _input('alertsOn', False)  # Turn alerts on?
alertsOnCurrent = _input('alertsOnCurrent', True)  # Alert on current bar?
alertsMessage = _input('alertsMessage', True)  # Display messageas on alerts?
alertsSound = _input('alertsSound', False)  # Play sound on alerts?
alertsEmail = _input('alertsEmail', False)  # Send email on alerts?
alertsNotify = _input('alertsNotify', False)  # Send push notification on alerts?
Interpolate = _input('Interpolate', True)  # Interpolate mtf data ?
sup = Arr(0, 0.0)
supc = Arr(0, 0.0)
mid = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
count = Arr(0, 0.0)
timeFrame = 0
indName = ""
workFil = Arr(0, 0.0, dims=(15,))
workSma = Arr(0, 0.0, dims=(4,))
workEma = Arr(0, 0.0, dims=(2,))
workSmma = Arr(0, 0.0, dims=(2,))
workLwma = Arr(0, 0.0, dims=(2,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global indName, timeFrame
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, mid, INDICATOR_DATA)
    SetIndexBuffer(3, sup, INDICATOR_DATA)
    SetIndexBuffer(4, supc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, count, INDICATOR_CALCULATIONS)
    timeFrame = MathMax(Period(), TimeFrame)
    indName = getIndicatorName()
    IndicatorSetString(INDICATOR_SHORTNAME, periodToString(timeFrame) + ' Gann high/low activator(' + _str(AvgPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_indHandle
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if timeFrame != Period():
        result = Arr(0, 0.0)
        currTime = Arr(0, 0)
        nextTime = Arr(0, 0)
        if _s_OnCalculate_indHandle == -1:
            _s_OnCalculate_indHandle = iCustom(Symbol(), timeFrame, indName, PERIOD_CURRENT, AvgPeriod, AvgType, Filter, FilterOn, alertsOn, alertsOnCurrent, alertsMessage, alertsSound, alertsEmail, alertsNotify)
        if _s_OnCalculate_indHandle == -1:
            return 0
        if CopyBuffer(_s_OnCalculate_indHandle, 5, 0, 1, result) == -1:
            return 0
        i = 0
        limit = rates_total - _int(MathMax(MathMin(_fdiv(result[0] * PeriodSeconds(timeFrame), PeriodSeconds(Period())), rates_total), 1))
        i = limit
        while limit > 0:
            if count[limit] == (EMPTY_VALUE - 1):
                break
            limit -= 1
        i = limit
        for i in range(i, rates_total):
            if CopyBuffer(_s_OnCalculate_indHandle, 0, _DT(time[i]), 1, result) == -1:
                break
            fup[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 1, _DT(time[i]), 1, result) == -1:
                break
            fdn[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 2, _DT(time[i]), 1, result) == -1:
                break
            mid[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 3, _DT(time[i]), 1, result) == -1:
                break
            sup[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 4, _DT(time[i]), 1, result) == -1:
                break
            supc[i] = result[0]
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
                fup[i - k] = fup[i] + _fdiv((fup[i - n] - fup[i]) * k, n)
                fdn[i - k] = fdn[i] + _fdiv((fdn[i - n] - fdn[i]) * k, n)
                mid[i - k] = mid[i] + _fdiv((mid[i - n] - mid[i]) * k, n)
                sup[i - k] = sup[i] + _fdiv((sup[i - n] - sup[i]) * k, n)
                k += 1
        else:
            i = _range_end(i, rates_total, 1)
        if i != rates_total:
            return 0
        return rates_total
    pfilter = Filter
    if FilterOn == flt_val:
        pfilter = 0.0
    vfilter = Filter
    if FilterOn == flt_prc:
        vfilter = 0.0
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        fup[i] = iFilter(iCustomMa(AvgType, iFilter(high[i - 1], pfilter, AvgPeriod, i, rates_total, 0), AvgPeriod, i, rates_total, 0), vfilter, AvgPeriod, i, rates_total, 1)
        fdn[i] = iFilter(iCustomMa(AvgType, iFilter(low[i - 1], pfilter, AvgPeriod, i, rates_total, 2), AvgPeriod, i, rates_total, 1), vfilter, AvgPeriod, i, rates_total, 3)
        mid[i] = (fup[i] + fdn[i]) / 2.0
        pclose = iFilter(close[i], pfilter, AvgPeriod, i, rates_total, 4)
        supc[i] = (1 if (pclose > fup[i]) else 2 if (pclose < fdn[i]) else supc[i - 1])
        sup[i] = (fdn[i] if (supc[i] == 1) else fup[i] if (supc[i] == 2) else pclose)
    manageAlerts(time, supc, rates_total)
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    return rates_total

def iFilter(value, filter_, period, i, bars, instanceNo=0):
    if filter_ <= 0 or period <= 0:
        return value
    if ArrayRange(workFil, 0) != bars:
        ArrayResize(workFil, bars)
    instanceNo *= 3
    workFil[i][instanceNo + 2] = value
    if i > 0:
        workFil[i][instanceNo + 0] = MathAbs(workFil[i][instanceNo + 2] - workFil[i - 1][instanceNo + 2])
        workFil[i][instanceNo + 1] = workFil[i][instanceNo + 0]
        fdev = 0.0
        fdif = 0.0
        k = 1
        while k < period and (i - k) >= 0:
            workFil[i][instanceNo + 1] += workFil[i - k][instanceNo + 0]
            k += 1
        workFil[i][instanceNo + 1] = _fdiv(workFil[i][instanceNo + 1], float(period))
        k = 0
        while k < period and (i - k) >= 0:
            fdev += MathPow(workFil[i - k][instanceNo + 0] - workFil[i - k][instanceNo + 1], 2)
            k += 1
        fdev = MathSqrt(_fdiv(fdev, float(period)))
        fdif = filter_ * fdev
        if MathAbs(workFil[i][instanceNo + 2] - workFil[i - 1][instanceNo + 2]) < fdif:
            workFil[i][instanceNo + 2] = workFil[i - 1][instanceNo + 2]
    return workFil[i][instanceNo + 2]

def manageAlerts(time, trend, bars):
    if not alertsOn:
        return
    whichBar = bars - 1
    if not alertsOnCurrent:
        whichBar = bars - 2
    time1 = time[whichBar]
    if trend[whichBar] != trend[whichBar - 1]:
        if trend[whichBar] == 1:
            doAlert(time1, 'up')
        if trend[whichBar] == 2:
            doAlert(time1, 'down')

def doAlert(forTime, doWhat):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    message = ""
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        message = periodToString(Period()) + ' ' + Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' Gann high/low activator state changed to ' + doWhat
        if alertsMessage:
            Alert(message)
        if alertsEmail:
            SendMail(Symbol() + ' Gann high/low activator', message)
        if alertsNotify:
            SendNotification(message)
        if alertsSound:
            PlaySound('alert2.wav')

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

def periodToString(period):
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

# ---- static local variables
_s_OnCalculate_indHandle = -1
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GannHighLowActivator2(_MQL5Indicator):
    name = 'Gann_high-low_activator_2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'AvgPeriod': 10,  # Average period
        'AvgType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Average method
        'Filter': 0.0,  # Filter to use (<=0 for no filter)
        'FilterOn': _Choice({0: 'Filter the prices', 1: 'Filter the averages value', 2: 'Filter all'}, default=0),  # Filter :
        'alertsOn': False,  # Turn alerts on?
        'alertsOnCurrent': True,  # Alert on current bar?
        'alertsMessage': True,  # Display messageas on alerts?
        'alertsSound': False,  # Play sound on alerts?
        'alertsEmail': False,  # Send email on alerts?
        'alertsNotify': False,  # Send push notification on alerts?
        'Interpolate': True,  # Interpolate mtf data ?
    }

