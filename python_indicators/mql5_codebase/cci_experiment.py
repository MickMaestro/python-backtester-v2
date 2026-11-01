"""CCI_experiment — converted from MQL5: MQL5 Indicators/CCI - experiment extended/CCI_experiment.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 8}, 'colors': {1: [3329330, 9639167], 2: [3329434], 3: [12632256], 4: [11823615], 5: [12632256, 3329330, 11823615]}, 'widths': {5: 2}, 'styles': {2: 2, 3: 2, 4: 2, 5: 0}, 'labels': {1: 'CCI Ob/Os zone', 2: 'CCI level up', 3: 'CCI middle level', 4: 'CCI level down', 5: 'CCI'}, 'levels': [], 'description': [], 'name': 'CCI_experiment', 'source': 'MQL5 Indicators/CCI - experiment extended/CCI_experiment.mq5', 'folder': 'CCI - experiment extended', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'CciPeriod', 'py': 'CciPeriod', 'param': 'CciPeriod', 'type': 'int', 'default': 50, 'label': 'CCI calculating period', 'sinput': False}, {'mql': 'CciPrice', 'py': 'CciPrice', 'param': 'CciPrice', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'CciAdapting', 'py': 'CciAdapting', 'param': 'CciAdapting', 'type': 'int', 'default': 0, 'label': 'Adapting type', 'sinput': False}, {'mql': 'PriceSmooth', 'py': 'PriceSmooth', 'param': 'PriceSmooth', 'type': 'int', 'default': 32, 'label': 'Price smoothing', 'sinput': False}, {'mql': 'PriceSmoothMethod', 'py': 'PriceSmoothMethod', 'param': 'PriceSmoothMethod', 'type': 'int', 'default': 1, 'label': 'Price smoothing method', 'sinput': False}, {'mql': 'LevelsPeriod', 'py': 'LevelsPeriod', 'param': 'LevelsPeriod', 'type': 'int', 'default': 25, 'label': 'Levels period (<0 no levels, 0 same as CCI period)', 'sinput': False}, {'mql': 'LevelsUp', 'py': 'LevelsUp', 'param': 'LevelsUp', 'type': 'double', 'default': 90.0, 'label': 'Levels up level %', 'sinput': False}, {'mql': 'LevelsDown', 'py': 'LevelsDown', 'param': 'LevelsDown', 'type': 'double', 'default': 10.0, 'label': 'Levels down level %', 'sinput': False}, {'mql': 'LevelType', 'py': 'LevelType', 'param': 'LevelType', 'type': 'int', 'default': 0, 'label': 'Levels type', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 1, 'label': 'Color change on :', 'sinput': False}, {'mql': 'AlertsOn', 'py': 'AlertsOn', 'param': 'AlertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'AlertsOnCurrent', 'py': 'AlertsOnCurrent', 'param': 'AlertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'AlertsMessage', 'py': 'AlertsMessage', 'param': 'AlertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'AlertsSound', 'py': 'AlertsSound', 'param': 'AlertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'AlertsEmail', 'py': 'AlertsEmail', 'param': 'AlertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'AlertsNotify', 'py': 'AlertsNotify', 'param': 'AlertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum chgColor
chg_onSlope = 0
chg_onLevel = 1
chg_onMiddle = 2
_enum('chgColor', {0: 'chg_onSlope', 1: 'chg_onLevel', 2: 'chg_onMiddle'})

# enum enLevelType
lvl_floa = 0
lvl_quan = 1
_enum('enLevelType', {0: 'lvl_floa', 1: 'lvl_quan'})

# enum enAdapting
ada_vhf = 0
ada_noa = 1
_enum('enAdapting', {0: 'ada_vhf', 1: 'ada_noa'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
CciPeriod = _input('CciPeriod', 50)  # CCI calculating period
CciPrice = _input('CciPrice', pr_close)  # Price
CciAdapting = _input('CciAdapting', ada_vhf)  # Adapting type
PriceSmooth = _input('PriceSmooth', 32)  # Price smoothing
PriceSmoothMethod = _input('PriceSmoothMethod', ma_ema)  # Price smoothing method
LevelsPeriod = _input('LevelsPeriod', 25)  # Levels period (<0 no levels, 0 same as CCI period)
LevelsUp = _input('LevelsUp', 90.0)  # Levels up level %
LevelsDown = _input('LevelsDown', 10.0)  # Levels down level %
LevelType = _input('LevelType', lvl_floa)  # Levels type
ColorOn = _input('ColorOn', chg_onLevel)  # Color change on :
AlertsOn = _input('AlertsOn', False)  # Turn alerts on?
AlertsOnCurrent = _input('AlertsOnCurrent', True)  # Alert on current bar?
AlertsMessage = _input('AlertsMessage', True)  # Display messageas on alerts?
AlertsSound = _input('AlertsSound', False)  # Play sound on alerts?
AlertsEmail = _input('AlertsEmail', False)  # Send email on alerts?
AlertsNotify = _input('AlertsNotify', False)  # Send push notification on alerts?
Interpolate = _input('Interpolate', True)  # Interpolate in multi time frame mode?
val = Arr(0, 0.0)
fillup = Arr(0, 0.0)
filldn = Arr(0, 0.0)
levelup = Arr(0, 0.0)
levelmi = Arr(0, 0.0)
leveldn = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
count = Arr(0, 0.0)
prices = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
timeFrame = 0
_workVhf = Arr(0, 0.0, dims=(1,))
_sortQuant = Arr(0, 0.0)
_workQuant = Arr(0, 0.0, dims=(1,))
workSma = Arr(0, 0.0, dims=(3,))
workEma = Arr(0, 0.0, dims=(3,))
workSmma = Arr(0, 0.0, dims=(3,))
workLwma = Arr(0, 0.0, dims=(3,))
workHa = Arr(0, 0.0, dims=(12,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _mtfHandle, timeFrame
    SetIndexBuffer(0, fillup, INDICATOR_DATA)
    SetIndexBuffer(1, filldn, INDICATOR_DATA)
    SetIndexBuffer(2, levelup, INDICATOR_DATA)
    SetIndexBuffer(3, levelmi, INDICATOR_DATA)
    SetIndexBuffer(4, leveldn, INDICATOR_DATA)
    SetIndexBuffer(5, val, INDICATOR_DATA)
    SetIndexBuffer(6, colorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, count, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, prices, INDICATOR_CALCULATIONS)
    for i in range(0, 4):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    timeFrame = MathMax(Period(), TimeFrame)
    if timeFrame != Period():
        _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, CciPeriod, CciPrice, CciAdapting, PriceSmooth, PriceSmoothMethod, LevelsPeriod, LevelsUp, LevelsDown, LevelType, ColorOn, AlertsOn, AlertsOnCurrent, AlertsMessage, AlertsSound, AlertsEmail, AlertsNotify)
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' CCI (' + _str(CciPeriod) + ',' + _str(PriceSmooth) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _mtfHandle
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if timeFrame != Period():
        result = Arr(0, 0.0)
        currTime = Arr(0, 0)
        nextTime = Arr(0, 0)
        if _mtfHandle == INVALID_HANDLE:
            _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, CciPeriod, CciPrice, CciAdapting, PriceSmooth, PriceSmoothMethod, LevelsPeriod, LevelsUp, LevelsDown, LevelType, ColorOn, AlertsOn, AlertsOnCurrent, AlertsMessage, AlertsSound, AlertsEmail, AlertsNotify)
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
            fillup[i] = result[0]
            if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) == -1:
                break
            filldn[i] = result[0]
            if CopyBuffer(_mtfHandle, 2, _DT(time[i]), 1, result) == -1:
                break
            levelup[i] = result[0]
            if CopyBuffer(_mtfHandle, 3, _DT(time[i]), 1, result) == -1:
                break
            levelmi[i] = result[0]
            if CopyBuffer(_mtfHandle, 4, _DT(time[i]), 1, result) == -1:
                break
            leveldn[i] = result[0]
            if CopyBuffer(_mtfHandle, 5, _DT(time[i]), 1, result) == -1:
                break
            val[i] = result[0]
            if CopyBuffer(_mtfHandle, 6, _DT(time[i]), 1, result) == -1:
                break
            colorBuffer[i] = result[0]
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
                fillup[i - k] = fillup[i] + _fdiv((fillup[i - n] - fillup[i]) * k, n)
                filldn[i - k] = filldn[i] + _fdiv((filldn[i - n] - filldn[i]) * k, n)
                levelup[i - k] = levelup[i] + _fdiv((levelup[i - n] - levelup[i]) * k, n)
                leveldn[i - k] = leveldn[i] + _fdiv((leveldn[i - n] - leveldn[i]) * k, n)
                levelmi[i - k] = levelmi[i] + _fdiv((levelmi[i - n] - levelmi[i]) * k, n)
                val[i - k] = val[i] + _fdiv((val[i - n] - val[i]) * k, n)
                k += 1
        else:
            i = _range_end(i, rates_total, 1)
        return i
    levelsPeriod = (1 if (LevelsPeriod < 0) else CciPeriod if (LevelsPeriod == 0) else LevelsPeriod)
    colorOn = (ColorOn if (levelsPeriod > 1) else chg_onSlope)
    i = 0
    i = MathMax(prev_calculated - 1, 0)
    for i in range(i, rates_total):
        price = getPrice(CciPrice, open, close, high, low, i, rates_total)
        vhf = (iVhf(price, CciPeriod, i, rates_total) if (CciAdapting == ada_vhf) else 0)
        period = (MathCeil(CciPeriod * (-MathLog(vhf))) if (vhf != 0) else CciPeriod)
        prices[i] = iCustomMa(PriceSmoothMethod, price, PriceSmooth, i, rates_total)
        avg = 0.0
        k = 0
        while k < _int(period) and (i - k) >= 0:
            avg += prices[i - k]
            k += 1
        avg = _fdiv(avg, _int(period))
        dev = 0.0
        k = 0
        while k < _int(period) and (i - k) >= 0:
            dev += MathAbs(prices[i - k] - avg)
            k += 1
        dev = _fdiv(dev, _int(period))
        if dev != 0:
            val[i] = _fdiv(prices[i] - avg, 0.015 * dev)
        else:
            val[i] = 0.0
        if LevelType == lvl_floa:
            start = MathMax(i - levelsPeriod + 1, 0)
            min_ = val[ArrayMinimum(val, start, levelsPeriod)]
            max_ = val[ArrayMaximum(val, start, levelsPeriod)]
            range_ = max_ - min_
            levelup[i] = min_ + ((LevelsUp * range_) / 100.0)
            leveldn[i] = min_ + ((LevelsDown * range_) / 100.0)
            levelmi[i] = min_ + (0.5 * range_)
        else:
            levelup[i] = iQuantile(val[i], levelsPeriod, LevelsUp, i, rates_total)
            leveldn[i] = iQuantile(val[i], levelsPeriod, LevelsDown, i, rates_total)
            levelmi[i] = iQuantile(val[i], levelsPeriod, (LevelsUp + LevelsDown) / 2.0, i, rates_total)
        _sw1 = colorOn
        if _sw1 == chg_onLevel:
            colorBuffer[i] = (1 if (val[i] > levelup[i]) else 2 if (val[i] < leveldn[i]) else 0 if (val[i] < levelup[i] and val[i] > leveldn[i]) else colorBuffer[i - 1] if (i > 0) else 0)
        elif _sw1 == chg_onMiddle:
            colorBuffer[i] = (1 if (val[i] > levelmi[i]) else 2 if (val[i] < levelmi[i]) else colorBuffer[i - 1] if (i > 0) else 0)
        else:
            colorBuffer[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else colorBuffer[i - 1]) if (i > 0) else 0)
        fillup[i] = val[i]
        filldn[i] = MathMin(MathMax(val[i], leveldn[i]), levelup[i])
    else:
        i = _range_end(i, rates_total, 1)
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    manageAlerts(time, colorBuffer, rates_total)
    return i

def iVhf(value, period, i, bars, instanceNo=0):
    if ArrayRange(_workVhf, 0) != bars:
        ArrayResize(_workVhf, bars)
    _workVhf[i][instanceNo] = value
    noise = 0.0
    vhf = 0.0
    max_ = value
    min_ = value
    k = 0
    while k < period and (i - k - 1) >= 0:
        noise += MathAbs(_workVhf[i - k][instanceNo] - _workVhf[i - k - 1][instanceNo])
        max_ = MathMax(_workVhf[i - k][instanceNo], max_)
        min_ = MathMin(_workVhf[i - k][instanceNo], min_)
        k += 1
    if noise > 0:
        vhf = _fdiv(max_ - min_, noise)
    return vhf

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
        message = timeFrameToString(Period()) + ' ' + Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' CCI state changed to ' + doWhat
        if AlertsMessage:
            Alert(message)
        if AlertsEmail:
            SendMail(Symbol() + ' CCI', message)
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

# ---- static local variables
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIExperiment(_MQL5Indicator):
    name = 'CCI_experiment'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'CciPeriod': 50,  # CCI calculating period
        'CciPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price
        'CciAdapting': _Choice({0: 'VHF adaptive', 1: 'Regular (no adapting)'}, default=0),  # Adapting type
        'PriceSmooth': 32,  # Price smoothing
        'PriceSmoothMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=1),  # Price smoothing method
        'LevelsPeriod': 25,  # Levels period (<0 no levels, 0 same as CCI period)
        'LevelsUp': 90.0,  # Levels up level %
        'LevelsDown': 10.0,  # Levels down level %
        'LevelType': _Choice({0: 'Floating levels', 1: 'Quantile levels'}, default=0),  # Levels type
        'ColorOn': _Choice({0: 'change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross'}, default=1),  # Color change on :
        'AlertsOn': False,  # Turn alerts on?
        'AlertsOnCurrent': True,  # Alert on current bar?
        'AlertsMessage': True,  # Display messageas on alerts?
        'AlertsSound': False,  # Play sound on alerts?
        'AlertsEmail': False,  # Send email on alerts?
        'AlertsNotify': False,  # Send push notification on alerts?
        'Interpolate': True,  # Interpolate in multi time frame mode?
    }

