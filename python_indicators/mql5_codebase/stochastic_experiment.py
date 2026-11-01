"""Stochastic_experiment — converted from MQL5: MQL5 Indicators/Stochastic experiment/Stochastic_experiment.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [11119017, 16748574, 6333684], 2: [8421504]}, 'widths': {1: 3}, 'styles': {2: 2}, 'labels': {1: 'stochastic', 2: 'signal'}, 'levels': [], 'description': [], 'name': 'Stochastic_experiment', 'source': 'MQL5 Indicators/Stochastic experiment/Stochastic_experiment.mq5', 'folder': 'Stochastic experiment', 'inputs': [{'mql': 'StoPeriod', 'py': 'StoPeriod', 'param': 'StoPeriod', 'type': 'int', 'default': 32, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'StoSlowing', 'py': 'StoSlowing', 'param': 'StoSlowing', 'type': 'int', 'default': 9, 'label': 'Stochastic slowing period', 'sinput': False}, {'mql': 'StoMaType', 'py': 'StoMaType', 'param': 'StoMaType', 'type': 'int', 'default': 0, 'label': 'Stochastic average type', 'sinput': False}, {'mql': 'SigPeriod', 'py': 'SigPeriod', 'param': 'SigPeriod', 'type': 'int', 'default': 3, 'label': 'Stochastic signal period', 'sinput': False}, {'mql': 'SigMaType', 'py': 'SigMaType', 'param': 'SigMaType', 'type': 'int', 'default': 0, 'label': 'Signal average type', 'sinput': False}, {'mql': 'StoPrice', 'py': 'StoPrice', 'param': 'StoPrice', 'type': 'int', 'default': 0, 'label': 'Price :', 'sinput': False}, {'mql': 'AlertsOn', 'py': 'AlertsOn', 'param': 'AlertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'AlertsOnCurrent', 'py': 'AlertsOnCurrent', 'param': 'AlertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'AlertsMessage', 'py': 'AlertsMessage', 'param': 'AlertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'AlertsSound', 'py': 'AlertsSound', 'param': 'AlertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'AlertsEmail', 'py': 'AlertsEmail', 'param': 'AlertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'AlertsNotify', 'py': 'AlertsNotify', 'param': 'AlertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# enum enStochPrice
sto_hil = 0
sto_ctc = 1
_enum('enStochPrice', {0: 'sto_hil', 1: 'sto_ctc'})

# ---- inputs and global variables
StoPeriod = _input('StoPeriod', 32)  # Stochastic period
StoSlowing = _input('StoSlowing', 9)  # Stochastic slowing period
StoMaType = _input('StoMaType', ma_sma)  # Stochastic average type
SigPeriod = _input('SigPeriod', 3)  # Stochastic signal period
SigMaType = _input('SigMaType', ma_sma)  # Signal average type
StoPrice = _input('StoPrice', sto_hil)  # Price :
AlertsOn = _input('AlertsOn', False)  # Turn alerts on?
AlertsOnCurrent = _input('AlertsOnCurrent', True)  # Alert on current bar?
AlertsMessage = _input('AlertsMessage', True)  # Display messageas on alerts?
AlertsSound = _input('AlertsSound', False)  # Play sound on alerts?
AlertsEmail = _input('AlertsEmail', False)  # Send email on alerts?
AlertsNotify = _input('AlertsNotify', False)  # Send push notification on alerts?
sto = Arr(0, 0.0)
stoc = Arr(0, 0.0)
sig = Arr(0, 0.0)
_avgNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
workSma = Arr(0, 0.0, dims=(3,))
workEma = Arr(0, 0.0, dims=(3,))
workSmma = Arr(0, 0.0, dims=(3,))
workLwma = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, sto, INDICATOR_DATA)
    SetIndexBuffer(1, stoc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, sig, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, _avgNames[StoMaType] + ' stochastic (' + _str(StoPeriod) + ',' + _str(StoSlowing) + ', of ' + _str(SigPeriod) + ' ' + _avgNames[SigMaType] + ' signal)')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        start = MathMax(i - StoPeriod + 1, 0)
        blo = (low[ArrayMinimum(low, start, StoPeriod)] if (StoPrice == sto_hil) else close[ArrayMinimum(close, start, StoPeriod)])
        bhi = (high[ArrayMaximum(high, start, StoPeriod)] if (StoPrice == sto_hil) else close[ArrayMaximum(close, start, StoPeriod)])
        sumlow = iCustomMa(StoMaType, close[i] - blo, StoSlowing, i, rates_total, 0)
        sumhigh = iCustomMa(StoMaType, bhi - blo, StoSlowing, i, rates_total, 1)
        sto[i] = (_fdiv(100 * sumlow, sumhigh) if (sumhigh != sumlow) else 100)
        sig[i] = iCustomMa(SigMaType, sto[i], SigPeriod, i, rates_total, 2)
        stoc[i] = (1 if (sto[i] > sig[i]) else 2 if (sto[i] < sig[i]) else stoc[i - 1] if (i > 0) else 0)
        i += 1
    manageAlerts(time, stoc, rates_total)
    return i

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
        message = Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' stochastic state changed to ' + doWhat
        if AlertsMessage:
            Alert(message)
        if AlertsEmail:
            SendMail(Symbol() + ' stochastic', message)
        if AlertsNotify:
            SendNotification(message)
        if AlertsSound:
            PlaySound('alert2.wav')

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo + 0] = price
    avg = price
    k = 1
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

# ---- static local variables
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticExperiment(_MQL5Indicator):
    name = 'Stochastic_experiment'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StoPeriod': 32,  # Stochastic period
        'StoSlowing': 9,  # Stochastic slowing period
        'StoMaType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Stochastic average type
        'SigPeriod': 3,  # Stochastic signal period
        'SigMaType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Signal average type
        'StoPrice': _Choice({0: 'High/low', 1: 'Close/close'}, default=0),  # Price :
        'AlertsOn': False,  # Turn alerts on?
        'AlertsOnCurrent': True,  # Alert on current bar?
        'AlertsMessage': True,  # Display messageas on alerts?
        'AlertsSound': False,  # Play sound on alerts?
        'AlertsEmail': False,  # Send email on alerts?
        'AlertsNotify': False,  # Send push notification on alerts?
    }

