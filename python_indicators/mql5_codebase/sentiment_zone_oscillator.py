"""Sentiment_zone_oscillator — converted from MQL5: MQL5 Indicators/Sentiment zone oscillator/Sentiment_zone_oscillator.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 8}, 'colors': {1: [3329330, 42495], 2: [3329330], 3: [12632256], 4: [42495], 5: [12632256, 3329330, 42495]}, 'widths': {5: 2}, 'styles': {2: 2, 3: 2, 4: 2}, 'labels': {1: 'Setiment zone oscillator levels', 2: 'Setiment zone oscillator up level', 3: 'Setiment zone oscillator middle level', 4: 'Setiment zone oscillator down level', 5: 'Setiment zone oscillator'}, 'levels': [], 'description': [], 'name': 'Sentiment_zone_oscillator', 'source': 'MQL5 Indicators/Sentiment zone oscillator/Sentiment_zone_oscillator.mq5', 'folder': 'Sentiment zone oscillator', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'SzoPeriod', 'py': 'SzoPeriod', 'param': 'SzoPeriod', 'type': 'int', 'default': 14, 'label': 'Sentiment zone period', 'sinput': False}, {'mql': 'SzoMethod', 'py': 'SzoMethod', 'param': 'SzoMethod', 'type': 'int', 'default': 4, 'label': 'Sentiment zone calculating method', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'PriceFiltering', 'py': 'PriceFiltering', 'param': 'PriceFiltering', 'type': 'int', 'default': 14, 'label': 'Price filtering period', 'sinput': False}, {'mql': 'PriceFilteringMethod', 'py': 'PriceFilteringMethod', 'param': 'PriceFilteringMethod', 'type': 'int', 'default': 0, 'label': 'Price filtering method', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 2, 'label': 'Color change', 'sinput': False}, {'mql': 'LevelType', 'py': 'LevelType', 'param': 'LevelType', 'type': 'int', 'default': 1, 'label': 'Level type', 'sinput': False}, {'mql': 'LevelPeriod', 'py': 'LevelPeriod', 'param': 'LevelPeriod', 'type': 'int', 'default': 25, 'label': 'Levels period', 'sinput': False}, {'mql': 'LevelUp', 'py': 'LevelUp', 'param': 'LevelUp', 'type': 'double', 'default': 90.0, 'label': 'Up level %', 'sinput': False}, {'mql': 'LevelDown', 'py': 'LevelDown', 'param': 'LevelDown', 'type': 'double', 'default': 10.0, 'label': 'Down level %', 'sinput': False}, {'mql': 'AlertsOn', 'py': 'AlertsOn', 'param': 'AlertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'AlertsOnCurrent', 'py': 'AlertsOnCurrent', 'param': 'AlertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'AlertsMessage', 'py': 'AlertsMessage', 'param': 'AlertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'AlertsSound', 'py': 'AlertsSound', 'param': 'AlertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'AlertsEmail', 'py': 'AlertsEmail', 'param': 'AlertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'AlertsNotify', 'py': 'AlertsNotify', 'param': 'AlertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate in multi time frame mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
ma_tema = 4
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma', 4: 'ma_tema'})

# enum enLevelType
lvl_floa = 0
lvl_quan = 1
_enum('enLevelType', {0: 'lvl_floa', 1: 'lvl_quan'})

# enum enColorOn
cc_onSlope = 0
cc_onMiddle = 1
cc_onLevels = 2
_enum('enColorOn', {0: 'cc_onSlope', 1: 'cc_onMiddle', 2: 'cc_onLevels'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
SzoPeriod = _input('SzoPeriod', 14)  # Sentiment zone period
SzoMethod = _input('SzoMethod', ma_tema)  # Sentiment zone calculating method
Price = _input('Price', pr_close)  # Price
PriceFiltering = _input('PriceFiltering', 14)  # Price filtering period
PriceFilteringMethod = _input('PriceFilteringMethod', ma_sma)  # Price filtering method
ColorOn = _input('ColorOn', cc_onLevels)  # Color change
LevelType = _input('LevelType', lvl_quan)  # Level type
LevelPeriod = _input('LevelPeriod', 25)  # Levels period
LevelUp = _input('LevelUp', 90.0)  # Up level %
LevelDown = _input('LevelDown', 10.0)  # Down level %
AlertsOn = _input('AlertsOn', False)  # Turn alerts on?
AlertsOnCurrent = _input('AlertsOnCurrent', True)  # Alert on current bar?
AlertsMessage = _input('AlertsMessage', True)  # Display messageas on alerts?
AlertsSound = _input('AlertsSound', False)  # Play sound on alerts?
AlertsEmail = _input('AlertsEmail', False)  # Send email on alerts?
AlertsNotify = _input('AlertsNotify', False)  # Send push notification on alerts?
Interpolate = _input('Interpolate', True)  # Interpolate in multi time frame mode
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelMi = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
count = Arr(0, 0.0)
state = Arr(0, 0.0)
prices = Arr(0, 0.0)
_maNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA', 'TEMA'], fill="")
_mtfHandle = INVALID_HANDLE
timeFrame = 0
_sortQuant = Arr(0, 0.0)
_workQuant = Arr(0, 0.0, dims=(1,))
workSma = Arr(0, 0.0, dims=(2,))
workEma = Arr(0, 0.0, dims=(2,))
workSmma = Arr(0, 0.0, dims=(2,))
workLwma = Arr(0, 0.0, dims=(2,))
workTema = Arr(0, 0.0, dims=(6,))
workHa = Arr(0, 0.0, dims=(4,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global timeFrame
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, levelUp, INDICATOR_DATA)
    SetIndexBuffer(3, levelMi, INDICATOR_DATA)
    SetIndexBuffer(4, levelDn, INDICATOR_DATA)
    SetIndexBuffer(5, val, INDICATOR_DATA)
    SetIndexBuffer(6, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, count, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, prices, INDICATOR_CALCULATIONS)
    for i in range(0, 4):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    timeFrame = MathMax(Period(), TimeFrame)
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' sentiment zone oscillator (' + _str(SzoPeriod) + ' ' + _maNames[SzoMethod] + ',' + _str(PriceFiltering) + ' ' + _maNames[PriceFilteringMethod] + ')')
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
            _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, SzoPeriod, SzoMethod, Price, PriceFiltering, PriceFilteringMethod, ColorOn, LevelType, LevelPeriod, LevelUp, LevelDown, AlertsOn, AlertsOnCurrent, AlertsMessage, AlertsSound, AlertsEmail, AlertsNotify)
        if _mtfHandle == INVALID_HANDLE:
            return 0
        if CopyBuffer(_mtfHandle, 7, 0, 1, result) == -1:
            return 0
        i = 0
        k = 0
        n = 0
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
            val[i] = result[0]
            if CopyBuffer(_mtfHandle, 6, _DT(time[i]), 1, result) == -1:
                break
            valc[i] = result[0]
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
                fill1[i - k] = fill1[i] + _fdiv((fill1[i - n] - fill1[i]) * k, n)
                fill2[i - k] = fill2[i] + _fdiv((fill2[i - n] - fill2[i]) * k, n)
                levelUp[i - k] = levelUp[i] + _fdiv((levelUp[i - n] - levelUp[i]) * k, n)
                levelMi[i - k] = levelMi[i] + _fdiv((levelMi[i - n] - levelMi[i]) * k, n)
                levelDn[i - k] = levelDn[i] + _fdiv((levelDn[i - n] - levelDn[i]) * k, n)
                val[i - k] = val[i] + _fdiv((val[i - n] - val[i]) * k, n)
                k += 1
        else:
            i = _range_end(i, rates_total, 1)
        return i
    levelPeriod = (LevelPeriod if (LevelPeriod > 1) else SzoPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        prices[i] = iCustomMa(PriceFilteringMethod, getPrice(Price, open, close, high, low, i, rates_total), PriceFiltering, i, rates_total, 1)
        useValue = ((1 if (prices[i] > prices[i - 1]) else -1 if (prices[i] < prices[i - 1]) else 0) if (i > 0) else 0)
        val[i] = iCustomMa(SzoMethod, useValue, SzoPeriod, i, rates_total, 0)
        _sw1 = LevelType
        if _sw1 == lvl_floa:
            start = MathMax(i - levelPeriod + 1, 0)
            min_ = val[ArrayMinimum(val, start, levelPeriod)]
            max_ = val[ArrayMaximum(val, start, levelPeriod)]
            range_ = max_ - min_
            levelUp[i] = min_ + ((LevelUp * range_) / 100.0)
            levelDn[i] = min_ + ((LevelDown * range_) / 100.0)
            levelMi[i] = (levelUp[i] + levelDn[i]) * 0.5
        else:
            levelUp[i] = iQuantile(val[i], levelPeriod, LevelUp, i, rates_total)
            levelDn[i] = iQuantile(val[i], levelPeriod, LevelDown, i, rates_total)
            levelMi[i] = iQuantile(val[i], levelPeriod, (LevelUp + LevelDown) * 0.5, i, rates_total)
        _sw2 = ColorOn
        if _sw2 == cc_onLevels:
            valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else 0 if (val[i] > levelDn[i] and val[i] < levelUp[i]) else valc[i - 1] if (i > 0) else 0)
        elif _sw2 == cc_onMiddle:
            valc[i] = (1 if (val[i] > levelMi[i]) else 2 if (val[i] < levelMi[i]) else 0)
        else:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        fill2[i] = (levelUp[i] if (val[i] > levelUp[i]) else levelDn[i] if (val[i] < levelDn[i]) else val[i])
        fill1[i] = val[i]
        i += 1
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    manageAlerts(time, valc, rates_total)
    return rates_total

def iQuantile(value, period, qp, i, bars, instanceNo=0):
    if ArrayRange(_workQuant, 0) != bars:
        ArrayResize(_workQuant, bars)
    _workQuant[i][instanceNo] = value
    if period < 1:
        return value
    if ArraySize(_sortQuant) != period:
        ArrayResize(_sortQuant, period)
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
    elif _sw3 == ma_tema:
        return iTema(price, _int(length), r, bars, instanceNo)
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

def iTema(price, period, r, bars, instanceNo=0):
    if ArrayRange(workTema, 0) != bars:
        ArrayResize(workTema, bars)
    instanceNo *= 3
    workTema[r][0 + instanceNo] = price
    workTema[r][1 + instanceNo] = price
    workTema[r][2 + instanceNo] = price
    if r > 0 and period > 1:
        alpha = _fdiv(2.0, 1.0 + period)
        workTema[r][0 + instanceNo] = workTema[r - 1][0 + instanceNo] + (alpha * (price - workTema[r - 1][0 + instanceNo]))
        workTema[r][1 + instanceNo] = workTema[r - 1][1 + instanceNo] + (alpha * (workTema[r][0 + instanceNo] - workTema[r - 1][1 + instanceNo]))
        workTema[r][2 + instanceNo] = workTema[r - 1][2 + instanceNo] + (alpha * (workTema[r][1 + instanceNo] - workTema[r - 1][2 + instanceNo]))
    return workTema[r][2 + instanceNo] + (3.0 * (workTema[r][0 + instanceNo] - workTema[r][1 + instanceNo]))

def manageAlerts(time, trend, bars):
    if not AlertsOn:
        return
    whichBar = bars - 1
    if not AlertsOnCurrent:
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
        message = timeFrameToString(Period()) + ' ' + Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' sentiment zone oscillator state changed to ' + doWhat
        if AlertsMessage:
            Alert(message)
        if AlertsEmail:
            SendMail(Symbol() + ' sentiment zone oscillator', message)
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


class SentimentZoneOscillator(_MQL5Indicator):
    name = 'Sentiment_zone_oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'SzoPeriod': 14,  # Sentiment zone period
        'SzoMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA', 4: 'Tripple exponential moving average'}, default=4),  # Sentiment zone calculating method
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'PriceFiltering': 14,  # Price filtering period
        'PriceFilteringMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA', 4: 'Tripple exponential moving average'}, default=0),  # Price filtering method
        'ColorOn': _Choice({0: 'Change color on slope change', 1: 'Change color on middle line cross', 2: 'Change color on outer levels cross'}, default=2),  # Color change
        'LevelType': _Choice({0: 'Floating levels', 1: 'Quantile levels'}, default=1),  # Level type
        'LevelPeriod': 25,  # Levels period
        'LevelUp': 90.0,  # Up level %
        'LevelDown': 10.0,  # Down level %
        'AlertsOn': False,  # Turn alerts on?
        'AlertsOnCurrent': True,  # Alert on current bar?
        'AlertsMessage': True,  # Display messageas on alerts?
        'AlertsSound': False,  # Play sound on alerts?
        'AlertsEmail': False,  # Send email on alerts?
        'AlertsNotify': False,  # Send push notification on alerts?
        'Interpolate': True,  # Interpolate in multi time frame mode
    }

