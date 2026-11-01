"""Gann_high-low_activator — converted from MQL5: MQL5 Indicators/Gann High Low Activator/Gann_high-low_activator.mq5

Copyright: mladen; Link: www.forex-tsd.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 8}, 'colors': {1: [14474460], 2: [8421504], 3: [11119017, 3329330, 17919]}, 'widths': {3: 2}, 'styles': {2: 2}, 'labels': {1: 'Gann zone', 2: 'Gann middle', 3: 'Gann high/low'}, 'levels': [], 'description': [], 'name': 'Gann_high-low_activator', 'source': 'MQL5 Indicators/Gann High Low Activator/Gann_high-low_activator.mq5', 'folder': 'Gann High Low Activator', 'inputs': [{'mql': 'AvgPeriod', 'py': 'AvgPeriod', 'param': 'AvgPeriod', 'type': 'int', 'default': 10, 'label': 'Average period', 'sinput': False}, {'mql': 'AvgType', 'py': 'AvgType', 'param': 'AvgType', 'type': 'int', 'default': 0, 'label': 'Average method', 'sinput': False}, {'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'alertsOnCurrent', 'py': 'alertsOnCurrent', 'param': 'alertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'alertsMessage', 'py': 'alertsMessage', 'param': 'alertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'alertsNotify', 'py': 'alertsNotify', 'param': 'alertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_Sma = 0
ma_Ema = 1
ma_Smma = 2
ma_Lwma = 3
_enum('enMaTypes', {0: 'ma_Sma', 1: 'ma_Ema', 2: 'ma_Smma', 3: 'ma_Lwma'})

# ---- inputs and global variables
AvgPeriod = _input('AvgPeriod', 10)  # Average period
AvgType = _input('AvgType', ma_Sma)  # Average method
alertsOn = _input('alertsOn', False)  # Turn alerts on?
alertsOnCurrent = _input('alertsOnCurrent', True)  # Alert on current bar?
alertsMessage = _input('alertsMessage', True)  # Display messageas on alerts?
alertsSound = _input('alertsSound', False)  # Play sound on alerts?
alertsEmail = _input('alertsEmail', False)  # Send email on alerts?
alertsNotify = _input('alertsNotify', False)  # Send push notification on alerts?
avg = Arr(0, 0.0)
avgc = Arr(0, 0.0)
mid = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(12,))
workEma = Arr(0, 0.0, dims=(6,))
workSmma = Arr(0, 0.0, dims=(6,))
workLwma = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, mid, INDICATOR_DATA)
    SetIndexBuffer(3, avg, INDICATOR_DATA)
    SetIndexBuffer(4, avgc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Gann high/low activator (' + _str(AvgPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        fup[i] = iCustomMa(AvgType, high[i - 1], AvgPeriod, i, rates_total, 0)
        fdn[i] = iCustomMa(AvgType, low[i - 1], AvgPeriod, i, rates_total, 1)
        mid[i] = (fup[i] + fdn[i]) / 2.0
        avgc[i] = (1 if (close[i] > fup[i]) else 2 if (close[i] < fdn[i]) else avgc[i - 1])
        avg[i] = (fdn[i] if (avgc[i] == 1) else fup[i] if (avgc[i] == 2) else close[i])
    manageAlerts(time, avgc, rates_total)
    return rates_total

def manageAlerts(time, trend, bars):
    if alertsOn:
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
        message = TimeToString(TimeLocal(), TIME_SECONDS) + ' ' + Symbol() + ' Gann high/low activator state changed to ' + doWhat
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
    if _sw1 == ma_Sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_Ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == ma_Smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_Lwma:
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

# ---- static local variables
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GannHighLowActivator(_MQL5Indicator):
    name = 'Gann_high-low_activator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AvgPeriod': 10,  # Average period
        'AvgType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Average method
        'alertsOn': False,  # Turn alerts on?
        'alertsOnCurrent': True,  # Alert on current bar?
        'alertsMessage': True,  # Display messageas on alerts?
        'alertsSound': False,  # Play sound on alerts?
        'alertsEmail': False,  # Send email on alerts?
        'alertsNotify': False,  # Send push notification on alerts?
    }

