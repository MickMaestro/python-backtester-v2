"""Smoothed_repulse_2 — converted from MQL5: MQL5 Indicators/Smoothed repulse/Smoothed_repulse_2.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 8}, 'colors': {1: [14474460], 2: [8421504], 3: [12632256, 3329330, 17919]}, 'widths': {3: 3}, 'styles': {2: 2}, 'labels': {1: 'Smoothed repulse zone', 2: 'Smoothed repulse middle', 3: 'Smoothed repulse'}, 'levels': [], 'description': [], 'name': 'Smoothed_repulse_2', 'source': 'MQL5 Indicators/Smoothed repulse/Smoothed_repulse_2.mq5', 'folder': 'Smoothed repulse', 'inputs': [{'mql': 'RepulsePeriod', 'py': 'RepulsePeriod', 'param': 'RepulsePeriod', 'type': 'int', 'default': 14, 'label': 'Repulse period', 'sinput': False}, {'mql': 'RepulseAvgType', 'py': 'RepulseAvgType', 'param': 'RepulseAvgType', 'type': 'int', 'default': 1, 'label': 'Repulse average method', 'sinput': False}, {'mql': 'RepulseAvgMult', 'py': 'RepulseAvgMult', 'param': 'RepulseAvgMult', 'type': 'int', 'default': 5, 'label': 'Repulse average multiplier', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 1, 'label': 'Color change on', 'sinput': False}, {'mql': 'LevelPeriod', 'py': 'LevelPeriod', 'param': 'LevelPeriod', 'type': 'int', 'default': 50, 'label': 'Levels period', 'sinput': False}, {'mql': 'LevelUp', 'py': 'LevelUp', 'param': 'LevelUp', 'type': 'double', 'default': 90.0, 'label': 'Upper level', 'sinput': False}, {'mql': 'LevelDown', 'py': 'LevelDown', 'param': 'LevelDown', 'type': 'double', 'default': 10.0, 'label': 'Lower level', 'sinput': False}, {'mql': 'AlertsOn', 'py': 'AlertsOn', 'param': 'AlertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'AlertsOnCurrent', 'py': 'AlertsOnCurrent', 'param': 'AlertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'AlertsMessage', 'py': 'AlertsMessage', 'param': 'AlertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'AlertsSound', 'py': 'AlertsSound', 'param': 'AlertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'AlertsEmail', 'py': 'AlertsEmail', 'param': 'AlertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'AlertsNotify', 'py': 'AlertsNotify', 'param': 'AlertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter
MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# enum enColorOn
chg_onSlope = 0
chg_onLevel = 1
chg_onMiddle = 2
_enum('enColorOn', {0: 'chg_onSlope', 1: 'chg_onLevel', 2: 'chg_onMiddle'})

# ---- inputs and global variables
RepulsePeriod = _input('RepulsePeriod', 14)  # Repulse period
RepulseAvgType = _input('RepulseAvgType', ma_ema)  # Repulse average method
RepulseAvgMult = _input('RepulseAvgMult', 5)  # Repulse average multiplier
ColorOn = _input('ColorOn', chg_onLevel)  # Color change on
LevelPeriod = _input('LevelPeriod', 50)  # Levels period
LevelUp = _input('LevelUp', 90.0)  # Upper level
LevelDown = _input('LevelDown', 10.0)  # Lower level
AlertsOn = _input('AlertsOn', False)  # Turn alerts on?
AlertsOnCurrent = _input('AlertsOnCurrent', True)  # Alert on current bar?
AlertsMessage = _input('AlertsMessage', True)  # Display messageas on alerts?
AlertsSound = _input('AlertsSound', False)  # Play sound on alerts?
AlertsEmail = _input('AlertsEmail', False)  # Send email on alerts?
AlertsNotify = _input('AlertsNotify', False)  # Send push notification on alerts?
rep = Arr(0, 0.0)
repc = Arr(0, 0.0)
fup = Arr(0, 0.0)
fmi = Arr(0, 0.0)
fdn = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(2,))
workEma = Arr(0, 0.0, dims=(2,))
workSmma = Arr(0, 0.0, dims=(2,))
workLwma = Arr(0, 0.0, dims=(2,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, fmi, INDICATOR_DATA)
    SetIndexBuffer(3, rep, INDICATOR_DATA)
    SetIndexBuffer(4, repc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoothed repulse (' + _str(RepulsePeriod) + ',' + _str(RepulseAvgMult) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        length = MathMin(i, RepulsePeriod)
        start = MathMax(i - length + 1, 0)
        min_ = high[ArrayMinimum(high, start, length)]
        max_ = low[ArrayMaximum(low, start, length)]
        bull = iCustomMa(RepulseAvgType, _fdiv(100 * ((3.0 * close[i]) - (2.0 * min_) - open[i - length]), close[i]), length * RepulseAvgMult, i, rates_total, 0)
        bear = iCustomMa(RepulseAvgType, _fdiv(100 * (open[i - length] + (2.0 * max_) - (3.0 * close[i])), close[i]), length * RepulseAvgMult, i, rates_total, 1)
        rep[i] = bull - bear
        start = MathMax(i - LevelPeriod + 1, 0)
        min_ = rep[ArrayMinimum(rep, start, LevelPeriod)]
        max_ = rep[ArrayMaximum(rep, start, LevelPeriod)]
        rn = max_ - min_
        fup[i] = min_ + ((rn * LevelUp) / 100.0)
        fdn[i] = min_ + ((rn * LevelDown) / 100.0)
        fmi[i] = (fup[i] + fdn[i]) / 2.0
        _sw1 = ColorOn
        if _sw1 == chg_onLevel:
            repc[i] = (1 if (rep[i] > fup[i]) else 2 if (rep[i] < fdn[i]) else 0 if (rep[i] < fup[i] and rep[i] > fdn[i]) else repc[i - 1] if (i > 0) else 0)
        elif _sw1 == chg_onMiddle:
            repc[i] = (1 if (rep[i] > fmi[i]) else 2 if (rep[i] < fmi[i]) else repc[i - 1] if (i > 0) else 0)
        else:
            repc[i] = ((1 if (rep[i] > rep[i - 1]) else 2 if (rep[i] < rep[i - 1]) else repc[i - 1]) if (i > 0) else 0)
        i += 1
    manageAlerts(time, repc, rates_total)
    return i

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
        message = timeFrameToString(Period()) + ' ' + Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' smoothed repulse state changed to ' + doWhat
        if AlertsMessage:
            Alert(message)
        if AlertsEmail:
            SendMail(Symbol() + ' smoothed repulse', message)
        if AlertsNotify:
            SendNotification(message)
        if AlertsSound:
            PlaySound('alert2.wav')

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


class SmoothedRepulse2(_MQL5Indicator):
    name = 'Smoothed_repulse_2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RepulsePeriod': 14,  # Repulse period
        'RepulseAvgType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=1),  # Repulse average method
        'RepulseAvgMult': 5,  # Repulse average multiplier
        'ColorOn': _Choice({0: 'change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross'}, default=1),  # Color change on
        'LevelPeriod': 50,  # Levels period
        'LevelUp': 90.0,  # Upper level
        'LevelDown': 10.0,  # Lower level
        'AlertsOn': False,  # Turn alerts on?
        'AlertsOnCurrent': True,  # Alert on current bar?
        'AlertsMessage': True,  # Display messageas on alerts?
        'AlertsSound': False,  # Play sound on alerts?
        'AlertsEmail': False,  # Send email on alerts?
        'AlertsNotify': False,  # Send push notification on alerts?
    }

