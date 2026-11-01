"""Aroon_oscillator_1.7 — converted from MQL5: MQL5 Indicators/Aroon oscillator - dynamic zones (levels)/Aroon_oscillator_1.7.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 4, 'indicator_minimum': -101.0, 'indicator_maximum': 101.0}, 'types': {1: 7, 2: 1, 3: 1, 4: 8}, 'colors': {1: [13759441, 12052223], 2: [13759441], 3: [12052223], 4: [11119017, 3329330, 42495]}, 'widths': {4: 2}, 'styles': {4: 0}, 'labels': {1: 'Aroon', 2: 'Aroon levels up', 3: 'Aroon levels down', 4: 'Aroon oscillator'}, 'levels': [], 'description': [], 'name': 'Aroon_oscillator_1.7', 'source': 'MQL5 Indicators/Aroon oscillator - dynamic zones (levels)/Aroon_oscillator_1.7.mq5', 'folder': 'Aroon oscillator - dynamic zones (levels)', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'AroonPeriod', 'py': 'AroonPeriod', 'param': 'AroonPeriod', 'type': 'int', 'default': 25, 'label': 'Aroon oscillator period', 'sinput': False}, {'mql': 'PriceHigh', 'py': 'PriceHigh', 'param': 'PriceHigh', 'type': 'int', 'default': 2, 'label': 'Price to use for high', 'sinput': False}, {'mql': 'PriceLow', 'py': 'PriceLow', 'param': 'PriceLow', 'type': 'int', 'default': 3, 'label': 'Price to use for low', 'sinput': False}, {'mql': 'LevelsPeriod', 'py': 'LevelsPeriod', 'param': 'LevelsPeriod', 'type': 'int', 'default': 0, 'label': 'Levels period (0 to use the same as Arron period)', 'sinput': False}, {'mql': 'LevelsUp', 'py': 'LevelsUp', 'param': 'LevelsUp', 'type': 'double', 'default': 80.0, 'label': 'Levels up', 'sinput': False}, {'mql': 'LevelsDown', 'py': 'LevelsDown', 'param': 'LevelsDown', 'type': 'double', 'default': 20.0, 'label': 'Levels down', 'sinput': False}, {'mql': 'FilterValue', 'py': 'FilterValue', 'param': 'FilterValue', 'type': 'double', 'default': 0.0, 'label': 'Filter (<=0, for no filter)', 'sinput': False}, {'mql': 'FilterPeriod', 'py': 'FilterPeriod', 'param': 'FilterPeriod', 'type': 'int', 'default': 0, 'label': 'Filter period (<=0 for using Aroon period)', 'sinput': False}, {'mql': 'FilterWhat', 'py': 'FilterWhat', 'param': 'FilterWhat', 'type': 'int', 'default': 16, 'label': 'Filter what?', 'sinput': False}, {'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'alertsOnCurrent', 'py': 'alertsOnCurrent', 'param': 'alertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'alertsMessage', 'py': 'alertsMessage', 'param': 'alertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'alertsNotify', 'py': 'alertsNotify', 'param': 'alertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data ?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enFilterWhat
flt_01 = 1
flt_02 = 16
flt_03 = 17
_enum('enFilterWhat', {1: 'flt_01', 16: 'flt_02', 17: 'flt_03'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
AroonPeriod = _input('AroonPeriod', 25)  # Aroon oscillator period
PriceHigh = _input('PriceHigh', pr_high)  # Price to use for high
PriceLow = _input('PriceLow', pr_low)  # Price to use for low
LevelsPeriod = _input('LevelsPeriod', 0)  # Levels period (0 to use the same as Arron period)
LevelsUp = _input('LevelsUp', 80.0)  # Levels up
LevelsDown = _input('LevelsDown', 20.0)  # Levels down
FilterValue = _input('FilterValue', 0.0)  # Filter (<=0, for no filter)
FilterPeriod = _input('FilterPeriod', 0)  # Filter period (<=0 for using Aroon period)
FilterWhat = _input('FilterWhat', 0x10)  # Filter what?
alertsOn = _input('alertsOn', False)  # Turn alerts on?
alertsOnCurrent = _input('alertsOnCurrent', True)  # Alert on current bar?
alertsMessage = _input('alertsMessage', True)  # Display messageas on alerts?
alertsSound = _input('alertsSound', False)  # Play sound on alerts?
alertsEmail = _input('alertsEmail', False)  # Send email on alerts?
alertsNotify = _input('alertsNotify', False)  # Send push notification on alerts?
Interpolate = _input('Interpolate', True)  # Interpolate mtf data ?
osc = Arr(0, 0.0)
oscc = Arr(0, 0.0)
oscu = Arr(0, 0.0)
oscd = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
prh = Arr(0, 0.0)
prl = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
timeFrame = 0
_sortQuant = Arr(0, 0.0)
_workQuant = Arr(0, 0.0, dims=(1,))
workFil = Arr(0, 0.0, dims=(9,))
workHa = Arr(0, 0.0, dims=(8,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _mtfHandle, timeFrame
    SetIndexBuffer(0, oscu, INDICATOR_DATA)
    SetIndexBuffer(1, oscd, INDICATOR_DATA)
    SetIndexBuffer(2, levu, INDICATOR_DATA)
    SetIndexBuffer(3, levd, INDICATOR_DATA)
    SetIndexBuffer(4, osc, INDICATOR_DATA)
    SetIndexBuffer(5, oscc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, prh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, prl, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, count, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    timeFrame = MathMax(Period(), TimeFrame)
    if timeFrame != Period():
        _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, AroonPeriod, PriceHigh, PriceLow, LevelsPeriod, LevelsUp, LevelsDown, FilterValue, FilterPeriod, FilterWhat, alertsOn, alertsOnCurrent, alertsMessage, alertsSound, alertsEmail, alertsNotify)
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' Arron oscillator(' + DoubleToString(AroonPeriod, 0) + ',' + _str(LevelsPeriod) + ')')
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
            _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, AroonPeriod, PriceHigh, PriceLow, LevelsPeriod, LevelsUp, LevelsDown, FilterValue, FilterPeriod, FilterWhat, alertsOn, alertsOnCurrent, alertsMessage, alertsSound, alertsEmail, alertsNotify)
        if _mtfHandle == INVALID_HANDLE:
            return 0
        if CopyBuffer(_mtfHandle, 8, 0, 1, result) == -1:
            return 0
        i = 0
        limit = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _idiv(_int(result[0]) * PeriodSeconds(timeFrame), PeriodSeconds(Period())) - 1, 0))
        i = limit
        for i in range(i, rates_total):
            if CopyBuffer(_mtfHandle, 0, _DT(time[i]), 1, result) == -1:
                break
            oscu[i] = result[0]
            if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) == -1:
                break
            oscd[i] = result[0]
            if CopyBuffer(_mtfHandle, 2, _DT(time[i]), 1, result) == -1:
                break
            levu[i] = result[0]
            if CopyBuffer(_mtfHandle, 3, _DT(time[i]), 1, result) == -1:
                break
            levd[i] = result[0]
            if CopyBuffer(_mtfHandle, 4, _DT(time[i]), 1, result) == -1:
                break
            osc[i] = result[0]
            if CopyBuffer(_mtfHandle, 5, _DT(time[i]), 1, result) == -1:
                break
            oscc[i] = result[0]
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
                oscu[i - k] = oscu[i] + _fdiv((oscu[i - n] - oscu[i]) * k, n)
                oscd[i - k] = oscd[i] + _fdiv((oscd[i - n] - oscd[i]) * k, n)
                osc[i - k] = osc[i] + _fdiv((osc[i - n] - osc[i]) * k, n)
                k += 1
        else:
            i = _range_end(i, rates_total, 1)
        if i != rates_total:
            return 0
        return rates_total
    lperiod = (LevelsPeriod if (LevelsPeriod > 0) else AroonPeriod)
    tperiod = (FilterPeriod if (FilterPeriod > 0) else AroonPeriod)
    pfilter = (FilterValue if ((FilterWhat & 0x01) != 0) else 0)
    vfilter = (FilterValue if ((FilterWhat & 0x10) != 0) else 0)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        prh[i] = iFilter(getPrice(PriceHigh, open, close, high, low, i, rates_total, 0), pfilter, tperiod, i, rates_total, 0)
        prl[i] = iFilter(getPrice(PriceLow, open, close, high, low, i, rates_total, 1), pfilter, tperiod, i, rates_total, 1)
        if prl[i] > prh[i]:
            temp = prh[i]
            prh[i] = prl[i]
            prl[i] = temp
        max_ = prh[i]
        maxi = 0.0
        min_ = prl[i]
        mini = 0.0
        k = 1
        while k <= AroonPeriod and (i - k) >= 0:
            if max_ < prh[i - k]:
                maxi = k
                max_ = prh[i - k]
            if min_ > prl[i - k]:
                mini = k
                min_ = prl[i - k]
            k += 1
        osc[i] = iFilter((100.0 * (mini - maxi)) / float(AroonPeriod), vfilter, tperiod, i, rates_total, 2)
        oscu[i] = osc[i]
        levu[i] = iQuantile(osc[i], lperiod, LevelsUp, i, rates_total)
        levd[i] = iQuantile(osc[i], lperiod, LevelsDown, i, rates_total)
        oscd[i] = MathMax(MathMin(osc[i], levu[i]), levd[i])
        oscc[i] = ((1 if (osc[i] > levu[i]) else 2 if (osc[i] < levd[i]) else 0) if (i > 0) else 0)
    manageAlerts(time, oscc, rates_total)
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    return rates_total

def iQuantile(value, period, qp, i, bars, instanceNo=0):
    if period < 1:
        return value
    if ArrayRange(_workQuant, 0) != bars:
        ArrayResize(_workQuant, bars)
    if ArraySize(_sortQuant) != period:
        ArrayResize(_sortQuant, period)
    _workQuant[i][instanceNo] = value
    k = 0
    while k < period and (i - k) >= 0:
        _sortQuant[k] = _workQuant[i - k][instanceNo]
        k += 1
    while k < period:
        _sortQuant[k] = 0.0
        k += 1
    ArraySort(_sortQuant)
    index = ((period - 1.0) * qp) / 100.0
    ind = _int(index)
    delta = index - ind
    if ind == NormalizeDouble(index, 5):
        return _sortQuant[ind]
    else:
        return ((1.0 - delta) * _sortQuant[ind]) + (delta * _sortQuant[ind + 1])

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

def manageAlerts(time, ttrend, bars):
    if not alertsOn:
        return
    whichBar = bars - 1
    if not alertsOnCurrent:
        whichBar = bars - 2
    time1 = time[whichBar]
    if ttrend[whichBar] != ttrend[whichBar - 1]:
        if ttrend[whichBar] == 1:
            doAlert(time1, 'up')
        if ttrend[whichBar] == 2:
            doAlert(time1, 'down')

def doAlert(forTime, doWhat):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        message = timeFrameToString(Period()) + ' ' + Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' Aroon oscillator state changed to ' + doWhat
        if alertsMessage:
            Alert(message)
        if alertsEmail:
            SendMail(Symbol() + ' Aroon oscillator', message)
        if alertsNotify:
            SendNotification(message)
        if alertsSound:
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
    i = ArraySize(_tfsPer) - 1
    for i in range(i, 0 - 1, -1):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, 0 - 1, -1)
    return _tfsStr[i]

# ---- static local variables
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AroonOscillator17(_MQL5Indicator):
    name = 'Aroon_oscillator_1.7'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'AroonPeriod': 25,  # Aroon oscillator period
        'PriceHigh': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=2),  # Price to use for high
        'PriceLow': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=3),  # Price to use for low
        'LevelsPeriod': 0,  # Levels period (0 to use the same as Arron period)
        'LevelsUp': 80.0,  # Levels up
        'LevelsDown': 20.0,  # Levels down
        'FilterValue': 0.0,  # Filter (<=0, for no filter)
        'FilterPeriod': 0,  # Filter period (<=0 for using Aroon period)
        'FilterWhat': _Choice({1: 'Filter the prices', 16: 'Filter the Aroon oscillator value', 17: 'Filter prices and the Aroon oscillator value'}, default=16),  # Filter what?
        'alertsOn': False,  # Turn alerts on?
        'alertsOnCurrent': True,  # Alert on current bar?
        'alertsMessage': True,  # Display messageas on alerts?
        'alertsSound': False,  # Play sound on alerts?
        'alertsEmail': False,  # Send email on alerts?
        'alertsNotify': False,  # Send push notification on alerts?
        'Interpolate': True,  # Interpolate mtf data ?
    }
    y_range = (-101.0, 101.0)

