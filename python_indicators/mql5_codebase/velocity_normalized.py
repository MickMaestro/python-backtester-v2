"""Velocity_-_normalized — converted from MQL5: MQL5 Indicators/Velocity - normalized/Velocity_-_normalized.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 8}, 'colors': {1: [13759441, 12052223], 2: [3329330], 3: [12632256], 4: [42495], 5: [12632256, 3329330, 42495]}, 'widths': {5: 2}, 'styles': {2: 2, 3: 2, 4: 2}, 'labels': {1: 'velocity OB/OS zone', 2: 'velocity up level', 3: 'velocity middle level', 4: 'velocity down level', 5: 'velocity'}, 'levels': [], 'description': [], 'name': 'Velocity_-_normalized', 'source': 'MQL5 Indicators/Velocity - normalized/Velocity_-_normalized.mq5', 'folder': 'Velocity - normalized', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'VelPeriod', 'py': 'VelPeriod', 'param': 'VelPeriod', 'type': 'int', 'default': 32, 'label': 'Velocity period', 'sinput': False}, {'mql': 'VelPrice', 'py': 'VelPrice', 'param': 'VelPrice', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'NormMethod', 'py': 'NormMethod', 'param': 'NormMethod', 'type': 'int', 'default': 0, 'label': 'Normalization method', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 2, 'label': 'Color change :', 'sinput': False}, {'mql': 'MinMaxPeriod', 'py': 'MinMaxPeriod', 'param': 'MinMaxPeriod', 'type': 'int', 'default': 50, 'label': 'Floating levels period (<= 1 to use velocity period)', 'sinput': False}, {'mql': 'LevelUp', 'py': 'LevelUp', 'param': 'LevelUp', 'type': 'double', 'default': 80.0, 'label': 'Up level %', 'sinput': False}, {'mql': 'LevelDown', 'py': 'LevelDown', 'param': 'LevelDown', 'type': 'double', 'default': 20.0, 'label': 'Down level %', 'sinput': False}, {'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'alertsOnCurrent', 'py': 'alertsOnCurrent', 'param': 'alertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'alertsMessage', 'py': 'alertsMessage', 'param': 'alertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'alertsNotify', 'py': 'alertsNotify', 'param': 'alertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data ?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enNormMethod
nm_atr = 0
nm_std = 1
nm_stc = 2
nm_non = 3
_enum('enNormMethod', {0: 'nm_atr', 1: 'nm_std', 2: 'nm_stc', 3: 'nm_non'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
VelPeriod = _input('VelPeriod', 32)  # Velocity period
VelPrice = _input('VelPrice', pr_close)  # Price to use
NormMethod = _input('NormMethod', nm_atr)  # Normalization method
ColorOn = _input('ColorOn', cc_onLevels)  # Color change :
MinMaxPeriod = _input('MinMaxPeriod', 50)  # Floating levels period (<= 1 to use velocity period)
LevelUp = _input('LevelUp', 80.0)  # Up level %
LevelDown = _input('LevelDown', 20.0)  # Down level %
alertsOn = _input('alertsOn', False)  # Turn alerts on?
alertsOnCurrent = _input('alertsOnCurrent', True)  # Alert on current bar?
alertsMessage = _input('alertsMessage', True)  # Display messageas on alerts?
alertsSound = _input('alertsSound', False)  # Play sound on alerts?
alertsEmail = _input('alertsEmail', False)  # Send email on alerts?
alertsNotify = _input('alertsNotify', False)  # Send push notification on alerts?
Interpolate = _input('Interpolate', True)  # Interpolate mtf data ?
vel = Arr(0, 0.0)
velc = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelMi = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
timeFrame = 0
workDev = Arr(0, 0.0)
workMom = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(4,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _mtfHandle, timeFrame
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, levelUp, INDICATOR_DATA)
    SetIndexBuffer(3, levelMi, INDICATOR_DATA)
    SetIndexBuffer(4, levelDn, INDICATOR_DATA)
    SetIndexBuffer(5, vel, INDICATOR_DATA)
    SetIndexBuffer(6, velc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, count, INDICATOR_CALCULATIONS)
    for i in range(0, 4):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    timeFrame = MathMax(Period(), TimeFrame)
    if timeFrame != Period():
        _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, VelPeriod, VelPrice, NormMethod, ColorOn, MinMaxPeriod, LevelUp, LevelDown, alertsOn, alertsOnCurrent, alertsMessage, alertsSound, alertsEmail, alertsNotify)
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' ATR normalzed velocity (' + _str(VelPeriod) + ',' + _str(MinMaxPeriod) + ')')
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
            _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, VelPeriod, VelPrice, NormMethod, ColorOn, MinMaxPeriod, LevelUp, LevelDown, alertsOn, alertsOnCurrent, alertsMessage, alertsSound, alertsEmail, alertsNotify)
        if _mtfHandle == INVALID_HANDLE:
            return 0
        if CopyBuffer(_mtfHandle, 7, 0, 1, result) == -1:
            return 0
        i = 0
        limit = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _idiv(_int(result[0]) * PeriodSeconds(timeFrame), PeriodSeconds(Period())) - 1, 0))
        i = limit
        for i in range(i, rates_total):
            if CopyBuffer(_mtfHandle, 0, _DT(time[i]), 1, result) == -1:
                break
            fill1[i] = result[0]
            if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) == -1:
                break
            fill2[i] = result[0]
            if CopyBuffer(_mtfHandle, 2, _DT(time[i]), 1, result) == -1:
                break
            levelUp[i] = result[0]
            if CopyBuffer(_mtfHandle, 3, _DT(time[i]), 1, result) == -1:
                break
            levelMi[i] = result[0]
            if CopyBuffer(_mtfHandle, 4, _DT(time[i]), 1, result) == -1:
                break
            levelDn[i] = result[0]
            if CopyBuffer(_mtfHandle, 5, _DT(time[i]), 1, result) == -1:
                break
            vel[i] = result[0]
            if CopyBuffer(_mtfHandle, 6, _DT(time[i]), 1, result) == -1:
                break
            velc[i] = result[0]
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
                levelUp[i - k] = levelUp[i] + _fdiv((levelUp[i - n] - levelUp[i]) * k, n)
                levelDn[i - k] = levelDn[i] + _fdiv((levelDn[i - n] - levelDn[i]) * k, n)
                levelMi[i - k] = levelMi[i] + _fdiv((levelMi[i - n] - levelMi[i]) * k, n)
                vel[i - k] = vel[i] + _fdiv((vel[i - n] - vel[i]) * k, n)
                k += 1
        else:
            i = _range_end(i, rates_total, 1)
        if i != rates_total:
            return 0
        return rates_total
    minMaxPeriod = (MinMaxPeriod if (MinMaxPeriod > 0) else VelPeriod)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(VelPrice, open, close, high, low, i, rates_total)
        div = 0.0
        _sw1 = NormMethod
        if _sw1 == nm_atr:
            div = iAtr(VelPeriod, high, low, close, i)
        elif _sw1 == nm_non:
            div = 1.0
        else:
            div = iDeviation(price, VelPeriod, NormMethod == nm_stc, i, rates_total)
        vel[i] = (_fdiv(iMomentumS(price, VelPeriod, 1.0, 2.0, i, rates_total), div) if (div != 0) else iMomentumS(price, VelPeriod, 1.0, 2.0, i, rates_total))
        min_ = vel[i]
        max_ = vel[i]
        k = 1
        while k < minMaxPeriod and (i - k) >= 0:
            min_ = MathMin(vel[i - k], min_)
            max_ = MathMax(vel[i - k], max_)
            k += 1
        range_ = max_ - min_
        levelUp[i] = min_ + ((LevelUp * range_) / 100.0)
        levelDn[i] = min_ + ((LevelDown * range_) / 100.0)
        levelMi[i] = min_ + (0.5 * range_)
        _sw2 = ColorOn
        if _sw2 == cc_onLevels:
            velc[i] = (1 if (vel[i] > levelUp[i]) else 2 if (vel[i] < levelDn[i]) else 0)
        elif _sw2 == cc_onMiddle:
            velc[i] = (1 if (vel[i] > levelMi[i]) else 2 if (vel[i] < levelMi[i]) else 0)
        else:
            velc[i] = ((1 if (vel[i] > vel[i - 1]) else 2 if (vel[i] < vel[i - 1]) else 0) if (i > 0) else 0)
        fill1[i] = vel[i]
        fill2[i] = (levelUp[i] if (vel[i] > levelUp[i]) else levelDn[i] if (vel[i] < levelDn[i]) else vel[i])
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    manageAlerts(time, velc, rates_total)
    return rates_total

def iAtr(atrPeriod, high, low, close, i):
    atr = 0.0
    k = 0
    while k < atrPeriod and (i - k) >= 0:
        if (i - k) == 0:
            atr += high[i - k] + low[i - k]
        else:
            atr += MathMax(high[i - k], close[i - k - 1]) - MathMin(low[i - k], close[i - k - 1])
        k += 1
    return _fdiv(atr, atrPeriod)

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
        message = timeFrameToString(Period()) + ' ' + Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' velocity state changed to ' + doWhat
        if alertsMessage:
            Alert(message)
        if alertsEmail:
            SendMail(Symbol() + ' velocity', message)
        if alertsNotify:
            SendNotification(message)
        if alertsSound:
            PlaySound('alert2.wav')

def iMomentumS(price, length, powSlow, powFast, i, bars):
    if ArraySize(workMom) != bars:
        ArrayResize(workMom, bars)
    workMom[i] = price
    suma = 0.0
    sumwa = 0.0
    sumb = 0.0
    sumwb = 0.0
    k = 0
    while k < length and (i - k) >= 0:
        weight = length - k
        suma += workMom[i - k] * MathPow(weight, powSlow)
        sumb += workMom[i - k] * MathPow(weight, powFast)
        sumwa += MathPow(weight, powSlow)
        sumwb += MathPow(weight, powFast)
        k += 1
    return _fdiv(sumb, sumwb) - _fdiv(suma, sumwa)

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


class VelocityNormalized(_MQL5Indicator):
    name = 'Velocity_-_normalized'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'VelPeriod': 32,  # Velocity period
        'VelPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price to use
        'NormMethod': _Choice({0: 'Use ATR for normalization', 1: 'Use standard deviation without sample correction', 2: 'Use standard deviation with sample correction', 3: 'No normalization'}, default=0),  # Normalization method
        'ColorOn': _Choice({0: 'Change color on slope change', 1: 'Change color on middle line cross', 2: 'Change color on outer levels cross'}, default=2),  # Color change :
        'MinMaxPeriod': 50,  # Floating levels period (<= 1 to use velocity period)
        'LevelUp': 80.0,  # Up level %
        'LevelDown': 20.0,  # Down level %
        'alertsOn': False,  # Turn alerts on?
        'alertsOnCurrent': True,  # Alert on current bar?
        'alertsMessage': True,  # Display messageas on alerts?
        'alertsSound': False,  # Play sound on alerts?
        'alertsEmail': False,  # Send email on alerts?
        'alertsNotify': False,  # Send push notification on alerts?
        'Interpolate': True,  # Interpolate mtf data ?
    }

