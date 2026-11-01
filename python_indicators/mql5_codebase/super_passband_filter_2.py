"""Super_Passband_Filter_2 — converted from MQL5: MQL5 Indicators/Super Passband Filter 2.0/Super_Passband_Filter_2.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 8}, 'colors': {1: [13759441, 12052223], 2: [3329330], 3: [12632256], 4: [42495], 5: [12632256, 3329330, 42495]}, 'widths': {5: 2}, 'styles': {2: 2, 3: 2, 4: 2, 5: 0}, 'labels': {1: 'super passband fill', 2: 'super passband level up', 3: 'super passband middle level', 4: 'super passband level down', 5: 'supper passband'}, 'levels': [], 'description': [], 'name': 'Super_Passband_Filter_2', 'source': 'MQL5 Indicators/Super Passband Filter 2.0/Super_Passband_Filter_2.mq5', 'folder': 'Super Passband Filter 2.0', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'Period1', 'py': 'Period1', 'param': 'Period1', 'type': 'double', 'default': 40.0, 'label': 'Period 1', 'sinput': False}, {'mql': 'Period2', 'py': 'Period2', 'param': 'Period2', 'type': 'double', 'default': 60.0, 'label': 'Period 2', 'sinput': False}, {'mql': 'RmsCount', 'py': 'RmsCount', 'param': 'RmsCount', 'type': 'int', 'default': 50, 'label': 'Calculation count', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 2, 'label': 'Color change :', 'sinput': False}, {'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'alertsOnCurrent', 'py': 'alertsOnCurrent', 'param': 'alertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'alertsMessage', 'py': 'alertsMessage', 'param': 'alertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'alertsNotify', 'py': 'alertsNotify', 'param': 'alertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data ?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enColorOn
cc_onSlope = 0
cc_onMiddle = 1
cc_onLevels = 2
_enum('enColorOn', {0: 'cc_onSlope', 1: 'cc_onMiddle', 2: 'cc_onLevels'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
Period1 = _input('Period1', 40.0)  # Period 1
Period2 = _input('Period2', 60.0)  # Period 2
RmsCount = _input('RmsCount', 50)  # Calculation count
Price = _input('Price', pr_close)  # Price to use
ColorOn = _input('ColorOn', cc_onLevels)  # Color change :
alertsOn = _input('alertsOn', False)  # Turn alerts on?
alertsOnCurrent = _input('alertsOnCurrent', True)  # Alert on current bar?
alertsMessage = _input('alertsMessage', True)  # Display messageas on alerts?
alertsSound = _input('alertsSound', False)  # Play sound on alerts?
alertsEmail = _input('alertsEmail', False)  # Send email on alerts?
alertsNotify = _input('alertsNotify', False)  # Send push notification on alerts?
Interpolate = _input('Interpolate', True)  # Interpolate mtf data ?
buffer = Arr(0, 0.0)
levelup = Arr(0, 0.0)
levelmi = Arr(0, 0.0)
leveldn = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
trend = Arr(0, 0.0)
prices = Arr(0, 0.0)
count = Arr(0, 0.0)
timeFrame = 0
workHa = Arr(0, 0.0, dims=(4,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global timeFrame
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, levelup, INDICATOR_DATA)
    SetIndexBuffer(3, levelmi, INDICATOR_DATA)
    SetIndexBuffer(4, leveldn, INDICATOR_DATA)
    SetIndexBuffer(5, buffer, INDICATOR_DATA)
    SetIndexBuffer(6, trend, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, count, INDICATOR_CALCULATIONS)
    for i in range(0, 4):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    timeFrame = MathMax(Period(), TimeFrame)
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' Supper passband filter (' + _str(Period1) + ',' + _str(Period2) + ',' + _str(RmsCount) + ')')
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
            _s_OnCalculate_indHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, Period1, Period2, RmsCount, Price, ColorOn, alertsOn, alertsOnCurrent, alertsMessage, alertsSound, alertsEmail, alertsNotify)
        if _s_OnCalculate_indHandle == -1:
            return 0
        if CopyBuffer(_s_OnCalculate_indHandle, 8, 0, 1, result) == -1:
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
            fill1[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 1, _DT(time[i]), 1, result) == -1:
                break
            fill2[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 2, _DT(time[i]), 1, result) == -1:
                break
            levelup[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 3, _DT(time[i]), 1, result) == -1:
                break
            levelmi[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 4, _DT(time[i]), 1, result) == -1:
                break
            leveldn[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 5, _DT(time[i]), 1, result) == -1:
                break
            buffer[i] = result[0]
            if CopyBuffer(_s_OnCalculate_indHandle, 6, _DT(time[i]), 1, result) == -1:
                break
            trend[i] = result[0]
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
                fill1[i - k] = fill1[i] + _fdiv((fill1[i - n] - fill1[i]) * k, n)
                fill2[i - k] = fill2[i] + _fdiv((fill2[i - n] - fill2[i]) * k, n)
                levelup[i - k] = levelup[i] + _fdiv((levelup[i - n] - levelup[i]) * k, n)
                leveldn[i - k] = leveldn[i] + _fdiv((leveldn[i - n] - leveldn[i]) * k, n)
                levelmi[i - k] = levelmi[i] + _fdiv((levelmi[i - n] - levelmi[i]) * k, n)
                buffer[i - k] = buffer[i] + _fdiv((buffer[i - n] - buffer[i]) * k, n)
                k += 1
        else:
            i = _range_end(i, rates_total, 1)
        if i != rates_total:
            return 0
        return rates_total
    a1 = 5.0 / Period1
    a2 = 5.0 / Period2
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        prices[i] = getPrice(Price, open, close, high, low, i, rates_total)
        if i < 2:
            buffer[i] = prices[i]
            continue
        buffer[i] = ((a1 - a2) * prices[i]) + (((a2 * (1 - a1)) - (a1 * (1 - a2))) * prices[i - 1]) + ((1 - a1 + (1 - a2)) * buffer[i - 1]) - ((1 - a1) * (1 - a2) * buffer[i - 2])
        rms = 0.0
        k = 0
        while k < RmsCount and (i - k) >= 0:
            rms += buffer[i - k] * buffer[i - k]
            k += 1
        rms = MathSqrt(rms / RmsCount)
        levelup[i] = rms
        levelmi[i] = 0.0
        leveldn[i] = -rms
        _sw1 = ColorOn
        if _sw1 == cc_onLevels:
            trend[i] = (1 if (buffer[i] > levelup[i]) else 2 if (buffer[i] < leveldn[i]) else 0)
        elif _sw1 == cc_onMiddle:
            trend[i] = (1 if (buffer[i] > levelmi[i]) else 2 if (buffer[i] < levelmi[i]) else 0)
        else:
            trend[i] = ((1 if (buffer[i] > buffer[i - 1]) else 2 if (buffer[i] < buffer[i - 1]) else 0) if (i > 0) else 0)
        fill1[i] = buffer[i]
        fill2[i] = (levelup[i] if (buffer[i] > levelup[i]) else leveldn[i] if (buffer[i] < leveldn[i]) else buffer[i])
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    manageAlerts(time, trend, rates_total)
    return rates_total

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
    message = ""
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        message = timeFrameToString(Period()) + ' ' + Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' super passband filter state changed to ' + doWhat
        if alertsMessage:
            Alert(message)
        if alertsEmail:
            SendMail(Symbol() + ' super passband filter', message)
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
        _sw2 = tprice
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
        elif _sw2 == pr_hatbiased2:
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw3 = tprice
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
    elif _sw3 == pr_tbiased2:
        if close[i] > open[i]:
            return high[i]
        if close[i] < open[i]:
            return low[i]
        return close[i]
    return 0.0

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
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SuperPassbandFilter2(_MQL5Indicator):
    name = 'Super_Passband_Filter_2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'Period1': 40.0,  # Period 1
        'Period2': 60.0,  # Period 2
        'RmsCount': 50,  # Calculation count
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price to use
        'ColorOn': _Choice({0: 'Change color on slope change', 1: 'Change color on middle line cross', 2: 'Change color on outer levels cross'}, default=2),  # Color change :
        'alertsOn': False,  # Turn alerts on?
        'alertsOnCurrent': True,  # Alert on current bar?
        'alertsMessage': True,  # Display messageas on alerts?
        'alertsSound': False,  # Play sound on alerts?
        'alertsEmail': False,  # Send email on alerts?
        'alertsNotify': False,  # Send push notification on alerts?
        'Interpolate': True,  # Interpolate mtf data ?
    }

