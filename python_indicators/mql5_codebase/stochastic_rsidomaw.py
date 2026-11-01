"""Stochastic_Rsidomaw — converted from MQL5: MQL5 Indicators/Stochastic RSI (OMA)/Stochastic_Rsidomaw.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 8}, 'colors': {1: [13759441, 12052223], 2: [3329330], 3: [12632256], 4: [42495], 5: [12632256, 3329330, 42495]}, 'widths': {5: 2}, 'styles': {2: 2, 3: 2, 4: 2}, 'labels': {1: 'Stochastic rsi(oma) OB/OS zone', 2: 'Stochastic rsi(oma) up level', 3: 'Stochastic rsi(oma) middle level', 4: 'Stochastic rsi(oma) down level', 5: 'Stochastic rsi(oma)'}, 'levels': [], 'description': [], 'name': 'Stochastic_Rsidomaw', 'source': 'MQL5 Indicators/Stochastic RSI (OMA)/Stochastic_Rsidomaw.mq5', 'folder': 'Stochastic RSI (OMA)', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'StocPeriod', 'py': 'StocPeriod', 'param': 'StocPeriod', 'type': 'int', 'default': 32, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'StocSlowing', 'py': 'StocSlowing', 'param': 'StocSlowing', 'type': 'int', 'default': 8, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'int', 'default': 32, 'label': 'Rsi period', 'sinput': False}, {'mql': 'RsiPrice', 'py': 'RsiPrice', 'param': 'RsiPrice', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'RsiMethod', 'py': 'RsiMethod', 'param': 'RsiMethod', 'type': 'int', 'default': 4, 'label': 'Rsi method', 'sinput': False}, {'mql': 'PriceSmoothing', 'py': 'PriceSmoothing', 'param': 'PriceSmoothing', 'type': 'int', 'default': 8, 'label': 'Price smoothing (<= 1 for no smoothing)', 'sinput': False}, {'mql': 'PriceSmoothingM', 'py': 'PriceSmoothingM', 'param': 'PriceSmoothingM', 'type': 'int', 'default': 1, 'label': 'Price smoothing method', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 2, 'label': 'Color change :', 'sinput': False}, {'mql': 'LevelType', 'py': 'LevelType', 'param': 'LevelType', 'type': 'int', 'default': 0, 'label': 'Level type :', 'sinput': False}, {'mql': 'MinMaxPeriod', 'py': 'MinMaxPeriod', 'param': 'MinMaxPeriod', 'type': 'int', 'default': 25, 'label': 'Floating levels period (<= 1 for fixed levels)', 'sinput': False}, {'mql': 'LevelUp', 'py': 'LevelUp', 'param': 'LevelUp', 'type': 'double', 'default': 80.0, 'label': 'Up level %', 'sinput': False}, {'mql': 'LevelDown', 'py': 'LevelDown', 'param': 'LevelDown', 'type': 'double', 'default': 20.0, 'label': 'Down level %', 'sinput': False}, {'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'alertsOnCurrent', 'py': 'alertsOnCurrent', 'param': 'alertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'alertsMessage', 'py': 'alertsMessage', 'param': 'alertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'alertsNotify', 'py': 'alertsNotify', 'param': 'alertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data ?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enRsiTypes
rsi_cut = 0
rsi_ehl = 1
rsi_har = 2
rsi_rap = 3
rsi_rsi = 4
rsi_rsx = 5
rsi_slo = 6
_enum('enRsiTypes', {0: 'rsi_cut', 1: 'rsi_ehl', 2: 'rsi_har', 3: 'rsi_rap', 4: 'rsi_rsi', 5: 'rsi_rsx', 6: 'rsi_slo'})

# enum enColorOn
cc_onSlope = 0
cc_onMiddle = 1
cc_onLevels = 2
_enum('enColorOn', {0: 'cc_onSlope', 1: 'cc_onMiddle', 2: 'cc_onLevels'})

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# enum enLevelType
lvl_floa = 0
lvl_quan = 1
lvl_fixed = 2
_enum('enLevelType', {0: 'lvl_floa', 1: 'lvl_quan', 2: 'lvl_fixed'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
StocPeriod = _input('StocPeriod', 32)  # Stochastic period
StocSlowing = _input('StocSlowing', 8)  # Stochastic slowing
RsiPeriod = _input('RsiPeriod', 32)  # Rsi period
RsiPrice = _input('RsiPrice', pr_close)  # Price to use
RsiMethod = _input('RsiMethod', rsi_rsi)  # Rsi method
PriceSmoothing = _input('PriceSmoothing', 8)  # Price smoothing (<= 1 for no smoothing)
PriceSmoothingM = _input('PriceSmoothingM', ma_ema)  # Price smoothing method
ColorOn = _input('ColorOn', cc_onLevels)  # Color change :
LevelType = _input('LevelType', lvl_floa)  # Level type :
MinMaxPeriod = _input('MinMaxPeriod', 25)  # Floating levels period (<= 1 for fixed levels)
LevelUp = _input('LevelUp', 80.0)  # Up level %
LevelDown = _input('LevelDown', 20.0)  # Down level %
alertsOn = _input('alertsOn', False)  # Turn alerts on?
alertsOnCurrent = _input('alertsOnCurrent', True)  # Alert on current bar?
alertsMessage = _input('alertsMessage', True)  # Display messageas on alerts?
alertsSound = _input('alertsSound', False)  # Play sound on alerts?
alertsEmail = _input('alertsEmail', False)  # Send email on alerts?
alertsNotify = _input('alertsNotify', False)  # Send push notification on alerts?
Interpolate = _input('Interpolate', True)  # Interpolate mtf data ?
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelMi = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
timeFrame = 0
workSto = Arr(0, 0.0, dims=(6,))
_sortQuant = Arr(0, 0.0)
_workQuant = Arr(0, 0.0, dims=(1,))
workRsi = Arr(0, 0.0, dims=(39,))
workHa = Arr(0, 0.0, dims=(4,))
workSma = Arr(0, 0.0, dims=(3,))
workEma = Arr(0, 0.0, dims=(3,))
workSmma = Arr(0, 0.0, dims=(3,))
workLwma = Arr(0, 0.0, dims=(3,))
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
    for i in range(0, 4):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    timeFrame = MathMax(Period(), TimeFrame)
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' Stochastic ' + getRsiName(RsiMethod) + '(oma) (' + _str(StocPeriod) + ',' + _str(RsiPeriod) + ',' + _str(PriceSmoothing) + ',' + _str(MinMaxPeriod) + ')')
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
            _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, StocPeriod, StocSlowing, RsiPeriod, RsiPrice, RsiMethod, PriceSmoothing, PriceSmoothingM, ColorOn, LevelType, MinMaxPeriod, LevelUp, LevelDown, alertsOn, alertsOnCurrent, alertsMessage, alertsSound, alertsEmail, alertsNotify)
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
                levelUp[i - k] = levelUp[i] + _fdiv((levelUp[i - n] - levelUp[i]) * k, n)
                levelDn[i - k] = levelDn[i] + _fdiv((levelDn[i - n] - levelDn[i]) * k, n)
                val[i - k] = val[i] + _fdiv((val[i - n] - val[i]) * k, n)
                k += 1
        else:
            i = _range_end(i, rates_total, 1)
        return i
    levelType = (LevelType if (MinMaxPeriod > 1) else lvl_fixed)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        rsi = iRsi(RsiMethod, iCustomMa(PriceSmoothingM, getPrice(RsiPrice, open, close, high, low, i, rates_total), PriceSmoothing, i, rates_total), RsiPeriod, i, rates_total)
        val[i] = iStoch(rsi, rsi, rsi, StocPeriod, StocSlowing, i, rates_total)
        _sw1 = levelType
        if _sw1 == lvl_fixed:
            levelUp[i] = LevelUp
            levelDn[i] = LevelDown
            levelMi[i] = (levelUp[i] + levelDn[i]) / 2
        elif _sw1 == lvl_floa:
            start = MathMax(i - MinMaxPeriod + 1, 0)
            min_ = val[ArrayMinimum(val, start, MinMaxPeriod)]
            max_ = val[ArrayMaximum(val, start, MinMaxPeriod)]
            range_ = max_ - min_
            levelUp[i] = min_ + ((LevelUp * range_) / 100.0)
            levelDn[i] = min_ + ((LevelDown * range_) / 100.0)
            levelMi[i] = (levelUp[i] + levelDn[i]) * 0.5
        else:
            levelUp[i] = iQuantile(val[i], MinMaxPeriod, LevelUp, i, rates_total)
            levelDn[i] = iQuantile(val[i], MinMaxPeriod, LevelDown, i, rates_total)
            levelMi[i] = iQuantile(val[i], MinMaxPeriod, (LevelUp + LevelDown) * 0.5, i, rates_total)
        _sw2 = ColorOn
        if _sw2 == cc_onLevels:
            valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else 0 if (val[i] > levelDn[i] and val[i] < levelUp[i]) else valc[i - 1] if (i > 0) else 0)
        elif _sw2 == cc_onMiddle:
            valc[i] = (1 if (val[i] > levelMi[i]) else 2 if (val[i] < levelMi[i]) else 0)
        else:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else 0) if (i > 0) else 0)
        fill2[i] = (levelUp[i] if (val[i] > levelUp[i]) else levelDn[i] if (val[i] < levelDn[i]) else val[i])
        fill1[i] = val[i]
        i += 1
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    manageAlerts(time, valc, rates_total)
    return i

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
        message = timeFrameToString(Period()) + ' ' + Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + getRsiName(RsiMethod) + ' state changed to ' + doWhat
        if alertsMessage:
            Alert(message)
        if alertsEmail:
            SendMail(Symbol() + ' ' + getRsiName(RsiMethod), message)
        if alertsNotify:
            SendNotification(message)
        if alertsSound:
            PlaySound('alert2.wav')

def iStoch(priceR, priceH, priceL, period, slowing, i, bars, instanceNo=0):
    if ArrayRange(workSto, 0) != bars:
        ArrayResize(workSto, bars)
    instanceNo *= 5
    workSto[i][0 + instanceNo] = priceH
    workSto[i][1 + instanceNo] = priceL
    workSto[i][2 + instanceNo] = priceR
    workSto[i][3 + instanceNo] = priceH
    workSto[i][4 + instanceNo] = priceL
    k = 1
    while k < period and (i - k) >= 0:
        workSto[i][4 + instanceNo] = MathMin(workSto[i][4 + instanceNo], workSto[i - k][instanceNo + 1])
        workSto[i][3 + instanceNo] = MathMax(workSto[i][3 + instanceNo], workSto[i - k][instanceNo + 0])
        k += 1
    sumlow = 0.0
    sumhigh = 0.0
    k = 0
    while k < MathMax(slowing, 1) and (i - k) >= 0:
        sumlow += workSto[i - k][2 + instanceNo] - workSto[i - k][4 + instanceNo]
        sumhigh += workSto[i - k][3 + instanceNo] - workSto[i - k][4 + instanceNo]
        k += 1
    if sumhigh != 0.0:
        return _fdiv(100.0 * sumlow, sumhigh)
    else:
        return 0.0

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

def getRsiName(method):
    _sw3 = method
    if _sw3 == rsi_rsi:
        return 'RSI'
    elif _sw3 == rsi_rsx:
        return 'RSX'
    elif _sw3 == rsi_cut:
        return "Cuttler's RSI"
    elif _sw3 == rsi_har:
        return "Haris' RSI"
    elif _sw3 == rsi_rap:
        return 'Rapid RSI'
    elif _sw3 == rsi_slo:
        return 'Slow RSI'
    elif _sw3 == rsi_ehl:
        return "Ehlers' smoothed RSI"
    else:
        return ''

def iRsi(rsiMode, price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 13
    workRsi[r][z + 0] = price
    _sw4 = rsiMode
    if _sw4 == rsi_rsi:
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
    elif _sw4 == rsi_slo:
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
    elif _sw4 == rsi_rap:
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
    elif _sw4 == rsi_ehl:
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
    elif _sw4 == rsi_cut:
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
    elif _sw4 == rsi_har:
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
    elif _sw4 == rsi_rsx:
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
        _sw5 = tprice
        if _sw5 == pr_haclose:
            return haClose
        elif _sw5 == pr_haopen:
            return haOpen
        elif _sw5 == pr_hahigh:
            return haHigh
        elif _sw5 == pr_halow:
            return haLow
        elif _sw5 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw5 == pr_hamedianb:
            return (haOpen + haClose) / 2.0
        elif _sw5 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw5 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw5 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw5 == pr_hatbiased:
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
        elif _sw5 == pr_hatbiased2:
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw6 = tprice
    if _sw6 == pr_close:
        return close[i]
    elif _sw6 == pr_open:
        return open[i]
    elif _sw6 == pr_high:
        return high[i]
    elif _sw6 == pr_low:
        return low[i]
    elif _sw6 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw6 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw6 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw6 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw6 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw6 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
    elif _sw6 == pr_tbiased2:
        if close[i] > open[i]:
            return high[i]
        if close[i] < open[i]:
            return low[i]
        return close[i]
    return 0.0

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw7 = mode
    if _sw7 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw7 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw7 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw7 == ma_lwma:
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


class StochasticRsidomaw(_MQL5Indicator):
    name = 'Stochastic_Rsidomaw'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'StocPeriod': 32,  # Stochastic period
        'StocSlowing': 8,  # Stochastic slowing
        'RsiPeriod': 32,  # Rsi period
        'RsiPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price to use
        'RsiMethod': _Choice({0: "Cuttler's RSI", 1: "Ehlers' smoothed RSI", 2: "Harris' RSI", 3: 'Rapid RSI', 4: 'RSI', 5: 'RSX', 6: 'Slow RSI'}, default=4),  # Rsi method
        'PriceSmoothing': 8,  # Price smoothing (<= 1 for no smoothing)
        'PriceSmoothingM': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=1),  # Price smoothing method
        'ColorOn': _Choice({0: 'Change color on slope change', 1: 'Change color on middle line cross', 2: 'Change color on outer levels cross'}, default=2),  # Color change :
        'LevelType': _Choice({0: 'Floating levels', 1: 'Quantile levels', 2: 'Fixed levels'}, default=0),  # Level type :
        'MinMaxPeriod': 25,  # Floating levels period (<= 1 for fixed levels)
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

