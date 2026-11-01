"""dmi_stochastic_extreme_1.1 — converted from MQL5: MQL5 Indicators/DMI stochastic extreme/dmi_stochastic_extreme_1.1.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [13759441, 12052223], 2: [11119017, 3329330, 42495]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'DMI stochastic extreme', 2: 'DMI stochastic extreme'}, 'levels': [], 'description': [], 'name': 'dmi_stochastic_extreme_1.1', 'source': 'MQL5 Indicators/DMI stochastic extreme/dmi_stochastic_extreme_1.1.mq5', 'folder': 'DMI stochastic extreme', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'DmiPeriod', 'py': 'DmiPeriod', 'param': 'DmiPeriod', 'type': 'int', 'default': 32, 'label': 'DMI period', 'sinput': False}, {'mql': 'StochasticPeriod', 'py': 'StochasticPeriod', 'param': 'StochasticPeriod', 'type': 'int', 'default': 50, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'StochasticSlowing', 'py': 'StochasticSlowing', 'param': 'StochasticSlowing', 'type': 'int', 'default': 9, 'label': 'Stochastic slowing period', 'sinput': False}, {'mql': 'SmoothingMethod', 'py': 'SmoothingMethod', 'param': 'SmoothingMethod', 'type': 'int', 'default': 2, 'label': 'Smoothing method for atr and dmi calculation', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 2, 'label': 'Change color on :', 'sinput': False}, {'mql': 'LevelUp', 'py': 'LevelUp', 'param': 'LevelUp', 'type': 'double', 'default': 90.0, 'label': 'Level up', 'sinput': False}, {'mql': 'LevelDown', 'py': 'LevelDown', 'param': 'LevelDown', 'type': 'double', 'default': 10.0, 'label': 'Level down', 'sinput': False}, {'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'alertsOnCurrent', 'py': 'alertsOnCurrent', 'param': 'alertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'alertsMessage', 'py': 'alertsMessage', 'param': 'alertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'alertsNotify', 'py': 'alertsNotify', 'param': 'alertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data ?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# enum enColorOn
cc_onSlope = 0
cc_onMiddle = 1
cc_onLevels = 2
_enum('enColorOn', {0: 'cc_onSlope', 1: 'cc_onMiddle', 2: 'cc_onLevels'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
DmiPeriod = _input('DmiPeriod', 32)  # DMI period
StochasticPeriod = _input('StochasticPeriod', 50)  # Stochastic period
StochasticSlowing = _input('StochasticSlowing', 9)  # Stochastic slowing period
SmoothingMethod = _input('SmoothingMethod', ma_smma)  # Smoothing method for atr and dmi calculation
ColorOn = _input('ColorOn', cc_onLevels)  # Change color on :
LevelUp = _input('LevelUp', 90.0)  # Level up
LevelDown = _input('LevelDown', 10.0)  # Level down
alertsOn = _input('alertsOn', False)  # Turn alerts on?
alertsOnCurrent = _input('alertsOnCurrent', True)  # Alert on current bar?
alertsMessage = _input('alertsMessage', True)  # Display messageas on alerts?
alertsSound = _input('alertsSound', False)  # Play sound on alerts?
alertsEmail = _input('alertsEmail', False)  # Send email on alerts?
alertsNotify = _input('alertsNotify', False)  # Send push notification on alerts?
Interpolate = _input('Interpolate', True)  # Interpolate mtf data ?
sto = Arr(0, 0.0)
stoc = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
count = Arr(0, 0.0)
indHandle = INVALID_HANDLE
timeFrame = 0
workSto = Arr(0, 0.0, dims=(5,))
workSma = Arr(0, 0.0, dims=(6,))
workEma = Arr(0, 0.0, dims=(3,))
workSmma = Arr(0, 0.0, dims=(3,))
workLwma = Arr(0, 0.0, dims=(3,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global indHandle, timeFrame
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, sto, INDICATOR_DATA)
    SetIndexBuffer(3, stoc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, count, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, LevelUp)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, LevelDown)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, (LevelUp + LevelDown) / 2)
    timeFrame = MathMax(Period(), TimeFrame)
    if timeFrame != Period():
        indHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, DmiPeriod, StochasticPeriod, StochasticSlowing, SmoothingMethod, ColorOn, LevelUp, LevelDown, alertsOn, alertsOnCurrent, alertsMessage, alertsSound, alertsEmail, alertsNotify)
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' DMI stochastic extreme (' + _str(DmiPeriod) + ',' + _str(StochasticPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global indHandle
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if timeFrame != Period():
        result = Arr(0, 0.0)
        currTime = Arr(0, 0)
        nextTime = Arr(0, 0)
        if indHandle == INVALID_HANDLE:
            indHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, DmiPeriod, StochasticPeriod, StochasticSlowing, SmoothingMethod, ColorOn, LevelUp, LevelDown, alertsOn, alertsOnCurrent, alertsMessage, alertsSound, alertsEmail, alertsNotify)
        if indHandle == INVALID_HANDLE:
            return 0
        if CopyBuffer(indHandle, 4, 0, 1, result) == -1:
            return 0
        i = 0
        limit = rates_total - _int(MathMin(_fdiv(result[0] * PeriodSeconds(timeFrame), PeriodSeconds(Period())), rates_total))
        limit = MathMax(MathMin(limit, rates_total - 1), 0)
        for limit in range(limit, 0, -1):
            if count[limit] == (EMPTY_VALUE - 1):
                break
        else:
            limit = _range_end(limit, 0, -1)
        i = MathMin(limit, MathMax(prev_calculated - 1, 0))
        for i in range(i, rates_total):
            if CopyBuffer(indHandle, 0, _DT(time[i]), 1, result) == -1:
                break
            fillu[i] = result[0]
            if CopyBuffer(indHandle, 1, _DT(time[i]), 1, result) == -1:
                break
            filld[i] = result[0]
            if CopyBuffer(indHandle, 2, _DT(time[i]), 1, result) == -1:
                break
            sto[i] = result[0]
            if CopyBuffer(indHandle, 3, _DT(time[i]), 1, result) == -1:
                break
            stoc[i] = result[0]
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
                sto[i - k] = sto[i] + _fdiv((sto[i - n] - sto[i]) * k, n)
                k += 1
        else:
            i = _range_end(i, rates_total, 1)
        if i != rates_total:
            return 0
        i = MathMin(limit, MathMax(prev_calculated - 1, 0))
        for i in range(i, rates_total):
            fillu[i] = sto[i]
            filld[i] = MathMax(MathMin(sto[i], LevelUp), LevelDown)
        else:
            i = _range_end(i, rates_total, 1)
        return rates_total
    LevelMi = (LevelUp + LevelDown) / 2.0
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        dhh = ((high[i] - high[i - 1]) if (i > 0) else 0)
        dll = ((low[i - 1] - low[i]) if (i > 0) else 0)
        tr = ((MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])) if (i > 0) else (high[i] - low[i]))
        atr = iCustomMa(SmoothingMethod, tr, DmiPeriod, i, rates_total, 0)
        plusDM = (dhh if (dhh > dll and dhh > 0) else 0)
        minusDM = (dll if (dll > dhh and dll > 0) else 0)
        plusDI = _fdiv(100 * iCustomMa(SmoothingMethod, plusDM, DmiPeriod, i, rates_total, 1), atr)
        minusDI = _fdiv(100 * iCustomMa(SmoothingMethod, minusDM, DmiPeriod, i, rates_total, 2), atr)
        osc = plusDI - minusDI
        sto[i] = iStoch(osc, osc, osc, StochasticPeriod, StochasticSlowing, rates_total, i)
        _sw1 = ColorOn
        if _sw1 == cc_onLevels:
            stoc[i] = (1 if (sto[i] > LevelUp) else 2 if (sto[i] < LevelDown) else 0)
        elif _sw1 == cc_onMiddle:
            stoc[i] = (1 if (sto[i] > LevelMi) else 2 if (sto[i] < LevelMi) else 0)
        else:
            stoc[i] = ((1 if (sto[i] > sto[i - 1]) else 2 if (sto[i] < sto[i - 1]) else 0) if (i > 0) else 0)
        fillu[i] = sto[i]
        filld[i] = MathMax(MathMin(sto[i], LevelUp), LevelDown)
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    manageAlerts(time, stoc, rates_total)
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
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        message = timeFrameToString(Period()) + ' ' + Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' dmi stochastic extreme state changed to ' + doWhat
        if alertsMessage:
            Alert(message)
        if alertsEmail:
            SendMail(Symbol() + ' dmi stochastic extreme', message)
        if alertsNotify:
            SendNotification(message)
        if alertsSound:
            PlaySound('alert2.wav')

def iStoch(priceR, priceH, priceL, period, slowing, bars, i, instanceNo=0):
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
    while k < slowing and (i - k) >= 0:
        sumlow += workSto[i - k][2 + instanceNo] - workSto[i - k][4 + instanceNo]
        sumhigh += workSto[i - k][3 + instanceNo] - workSto[i - k][4 + instanceNo]
        k += 1
    if sumhigh != 0.0:
        return _fdiv(100.0 * sumlow, sumhigh)
    else:
        return 0.0

def getColor(stepNo, totalSteps, from_, to):
    stes = float(totalSteps) - 1.0
    step = _fdiv(from_ - to, stes)
    return _uint(round(from_ - (step * stepNo)))

def gradientColor(step, totalSteps, from_, to):
    newBlue = getColor(step, totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(step, totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(step, totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed

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
    if period <= 1:
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


class DmiStochasticExtreme11(_MQL5Indicator):
    name = 'dmi_stochastic_extreme_1.1'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'DmiPeriod': 32,  # DMI period
        'StochasticPeriod': 50,  # Stochastic period
        'StochasticSlowing': 9,  # Stochastic slowing period
        'SmoothingMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=2),  # Smoothing method for atr and dmi calculation
        'ColorOn': _Choice({0: 'Change color on slope change', 1: 'Change color on middle line cross', 2: 'Change color on outer levels cross'}, default=2),  # Change color on :
        'LevelUp': 90.0,  # Level up
        'LevelDown': 10.0,  # Level down
        'alertsOn': False,  # Turn alerts on?
        'alertsOnCurrent': True,  # Alert on current bar?
        'alertsMessage': True,  # Display messageas on alerts?
        'alertsSound': False,  # Play sound on alerts?
        'alertsEmail': False,  # Send email on alerts?
        'alertsNotify': False,  # Send push notification on alerts?
        'Interpolate': True,  # Interpolate mtf data ?
    }

