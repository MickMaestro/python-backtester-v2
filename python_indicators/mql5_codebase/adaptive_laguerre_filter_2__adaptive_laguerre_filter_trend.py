"""Adaptive_Laguerre_filter_2 — converted from MQL5: MQL5 Indicators/Adaptive Laguerre filter trend/Adaptive_Laguerre_filter_2.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 16760576, 6333684]}, 'widths': {1: 3}, 'styles': {}, 'labels': {1: 'Laguerre'}, 'levels': [], 'description': [], 'name': 'Adaptive_Laguerre_filter_2', 'source': 'MQL5 Indicators/Adaptive Laguerre filter trend/Adaptive_Laguerre_filter_2.mq5', 'folder': 'Adaptive Laguerre filter trend', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'LaggPeriod', 'py': 'LaggPeriod', 'param': 'LaggPeriod', 'type': 'double', 'default': 10.0, 'label': 'Laguerre period', 'sinput': False}, {'mql': 'LaggSmooth', 'py': 'LaggSmooth', 'param': 'LaggSmooth', 'type': 'double', 'default': 0.5, 'label': 'Laguerre "smooth"', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 4, 'label': 'Price', 'sinput': False}, {'mql': 'AlertsOn', 'py': 'AlertsOn', 'param': 'AlertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'AlertsOnCurrent', 'py': 'AlertsOnCurrent', 'param': 'AlertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'AlertsMessage', 'py': 'AlertsMessage', 'param': 'AlertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'AlertsSound', 'py': 'AlertsSound', 'param': 'AlertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'AlertsEmail', 'py': 'AlertsEmail', 'param': 'AlertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'AlertsNotify', 'py': 'AlertsNotify', 'param': 'AlertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data ?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
LaggPeriod = _input('LaggPeriod', 10.0)  # Laguerre period
LaggSmooth = _input('LaggSmooth', 0.5)  # Laguerre "smooth"
Price = _input('Price', pr_median)  # Price
AlertsOn = _input('AlertsOn', False)  # Turn alerts on?
AlertsOnCurrent = _input('AlertsOnCurrent', True)  # Alert on current bar?
AlertsMessage = _input('AlertsMessage', True)  # Display messageas on alerts?
AlertsSound = _input('AlertsSound', False)  # Play sound on alerts?
AlertsEmail = _input('AlertsEmail', False)  # Send email on alerts?
AlertsNotify = _input('AlertsNotify', False)  # Send push notification on alerts?
Interpolate = _input('Interpolate', True)  # Interpolate mtf data ?
lagg1 = Arr(0, 0.0)
lagg1c = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
timeFrame = 0
_sortLagf = Arr(0, 0.0)
_workLagFila = Arr(0, 0.0, dims=(6,))
workHa = Arr(0, 0.0, dims=(4,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global timeFrame
    SetIndexBuffer(0, lagg1, INDICATOR_DATA)
    SetIndexBuffer(1, lagg1c, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, count, INDICATOR_CALCULATIONS)
    timeFrame = MathMax(Period(), TimeFrame)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Adaptive Laguerre (' + _str(LaggPeriod) + ')')
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
            _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, LaggPeriod, LaggSmooth, Price, AlertsOn, AlertsOnCurrent, AlertsMessage, AlertsSound, AlertsEmail, AlertsNotify)
        if _mtfHandle == INVALID_HANDLE:
            return 0
        if CopyBuffer(_mtfHandle, 2, 0, 1, result) == -1:
            return 0
        i = 0
        k = 0
        n = 0
        limit = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _idiv(_int(result[0]) * PeriodSeconds(timeFrame), PeriodSeconds(Period())) - 1, 0))
        i = limit
        for i in range(i, rates_total):
            if CopyBuffer(_mtfHandle, 0, _DT(time[i]), 1, result) == -1:
                break
            lagg1[i] = result[0]
            if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) == -1:
                break
            lagg1c[i] = result[0]
            if not Interpolate:
                continue
            CopyTime(Symbol(), timeFrame, _DT(time[i]), 1, currTime)
            if i < (rates_total - 1):
                CopyTime(Symbol(), timeFrame, _DT(time[i + 1]), 1, nextTime)
                if currTime[0] == nextTime[0]:
                    continue
            n = 1
            while (i - n) > 0 and time[i - n] >= currTime[0]:
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                lagg1[i - k] = lagg1[i] + _fdiv((lagg1[i - n] - lagg1[i]) * k, n)
                k += 1
        else:
            i = _range_end(i, rates_total, 1)
        return i
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        lagg1[i] = iLaGuerreFilterAdaptive(getPrice(Price, open, close, high, low, i, rates_total), LaggPeriod, LaggSmooth, rates_total, i, 0)
        lagg1c[i] = ((1 if (lagg1[i] > lagg1[i - 1]) else 2 if (lagg1[i] < lagg1[i - 1]) else lagg1c[i - 1]) if (i > 0) else 0)
        i += 1
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    manageAlerts(time, lagg1c, rates_total)
    return i

def iLaGuerreFilterAdaptive(price, period, smooth, bars, i, instanceNo=0):
    median = _int(MathMax(period * smooth, 2))
    if ArrayRange(_workLagFila, 0) != bars:
        ArrayResize(_workLagFila, bars)
    instanceNo *= 6
    if ArraySize(_sortLagf) != median:
        ArrayResize(_sortLagf, median)
    _workLagFila[i][instanceNo + 4] = price
    _workLagFila[i][instanceNo + 5] = (MathAbs(price - _workLagFila[i - 1][instanceNo + 4]) if (i > 0) else 0)
    alpha = 0.0
    hi = _workLagFila[i][instanceNo + 5]
    lo = _workLagFila[i][instanceNo + 5]
    k = 1
    while k < period and (i - k) >= 0:
        hi = MathMax(hi, _workLagFila[i - k][instanceNo + 5])
        lo = MathMin(lo, _workLagFila[i - k][instanceNo + 5])
        k += 1
    if hi != lo:
        k = 0
        while k < median and (i - k) >= 0:
            _sortLagf[k] = _fdiv(_workLagFila[i - k][instanceNo + 5] - lo, hi - lo)
            k += 1
        while k < median:
            _sortLagf[k] = 0.0
            k += 1
        ArraySort(_sortLagf)
        if MathMod(median, 2.0) != 0:
            alpha = _sortLagf[_idiv(median, 2)]
        else:
            alpha = (_sortLagf[_idiv(median, 2)] + _sortLagf[_idiv(median, 2) - 1]) / 2.0
    gamma = MathMax(MathMin(1.0 - alpha, 1 - DBL_MIN), DBL_MIN)
    if i > 0 and period > 1:
        _workLagFila[i][instanceNo + 0] = ((1.0 - gamma) * price) + (gamma * _workLagFila[i - 1][instanceNo + 0])
        _workLagFila[i][instanceNo + 1] = ((-gamma) * _workLagFila[i][instanceNo + 0]) + _workLagFila[i - 1][instanceNo + 0] + (gamma * _workLagFila[i - 1][instanceNo + 1])
        _workLagFila[i][instanceNo + 2] = ((-gamma) * _workLagFila[i][instanceNo + 1]) + _workLagFila[i - 1][instanceNo + 1] + (gamma * _workLagFila[i - 1][instanceNo + 2])
        _workLagFila[i][instanceNo + 3] = ((-gamma) * _workLagFila[i][instanceNo + 2]) + _workLagFila[i - 1][instanceNo + 2] + (gamma * _workLagFila[i - 1][instanceNo + 3])
        _workLagFila[i][instanceNo + 4] = (_workLagFila[i][instanceNo + 0] + (2.0 * _workLagFila[i][instanceNo + 1]) + (2.0 * _workLagFila[i][instanceNo + 2]) + _workLagFila[i][instanceNo + 3]) / 6.0
    else:
        for k in range(0, 4 + 1):
            _workLagFila[i][instanceNo + k] = price
    return _workLagFila[i][instanceNo + 4]

def manageAlerts(atime, atrend, bars):
    if not AlertsOn:
        return
    whichBar = bars - 1
    if not AlertsOnCurrent:
        whichBar = bars - 2
    time1 = atime[whichBar]
    if atrend[whichBar] != atrend[whichBar - 1]:
        if atrend[whichBar] == 1:
            doAlert(time1, 'up')
        if atrend[whichBar] == 2:
            doAlert(time1, 'down')

def doAlert(forTime, doWhat):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    message = ""
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        message = timeFrameToString(Period()) + ' ' + Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' adaptive Laguerre filter state changed to ' + doWhat
        if AlertsMessage:
            Alert(message)
        if AlertsEmail:
            SendMail(Symbol() + ' adaptive Laguerre filter', message)
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
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0
_s_timeFrameCheck_warned = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdaptiveLaguerreFilter2(_MQL5Indicator):
    name = 'Adaptive_Laguerre_filter_2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'LaggPeriod': 10.0,  # Laguerre period
        'LaggSmooth': 0.5,  # Laguerre "smooth"
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=4),  # Price
        'AlertsOn': False,  # Turn alerts on?
        'AlertsOnCurrent': True,  # Alert on current bar?
        'AlertsMessage': True,  # Display messageas on alerts?
        'AlertsSound': False,  # Play sound on alerts?
        'AlertsEmail': False,  # Send email on alerts?
        'AlertsNotify': False,  # Send push notification on alerts?
        'Interpolate': True,  # Interpolate mtf data ?
    }

