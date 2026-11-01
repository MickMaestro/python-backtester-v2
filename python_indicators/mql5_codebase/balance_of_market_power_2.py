"""Balance_of_market_power_2 — converted from MQL5: MQL5 Indicators/Balance of market power/Balance_of_market_power_2.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 8}, 'colors': {1: [14474460], 2: [8421504], 3: [12632256, 3329330, 17919]}, 'widths': {3: 3}, 'styles': {2: 2}, 'labels': {1: 'Balance of market power zone', 2: 'Balance of market power middle', 3: 'Balance of market power'}, 'levels': [], 'description': [], 'name': 'Balance_of_market_power_2', 'source': 'MQL5 Indicators/Balance of market power/Balance_of_market_power_2.mq5', 'folder': 'Balance of market power', 'inputs': [{'mql': 'BompSmoothPeriod', 'py': 'BompSmoothPeriod', 'param': 'BompSmoothPeriod', 'type': 'double', 'default': 90.0, 'label': 'Balance of market power smoothing period', 'sinput': False}, {'mql': 'BompSmoothPhase', 'py': 'BompSmoothPhase', 'param': 'BompSmoothPhase', 'type': 'double', 'default': 0.0, 'label': 'Balance of market power smoothing phase', 'sinput': False}, {'mql': 'BandsPeriod', 'py': 'BandsPeriod', 'param': 'BandsPeriod', 'type': 'int', 'default': 9, 'label': 'Bands period', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 0.5, 'label': 'Bands deviation', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 2, 'label': 'Color change on', 'sinput': False}, {'mql': 'AlertsOn', 'py': 'AlertsOn', 'param': 'AlertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'AlertsOnCurrent', 'py': 'AlertsOnCurrent', 'param': 'AlertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'AlertsMessage', 'py': 'AlertsMessage', 'param': 'AlertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts?', 'sinput': False}, {'mql': 'AlertsSound', 'py': 'AlertsSound', 'param': 'AlertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'AlertsEmail', 'py': 'AlertsEmail', 'param': 'AlertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'AlertsNotify', 'py': 'AlertsNotify', 'param': 'AlertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorOn
chg_onSlope = 0
chg_onLevel = 1
chg_onMiddle = 2
_enum('enColorOn', {0: 'chg_onSlope', 1: 'chg_onLevel', 2: 'chg_onMiddle'})

# ---- inputs and global variables
BompSmoothPeriod = _input('BompSmoothPeriod', 90.0)  # Balance of market power smoothing period
BompSmoothPhase = _input('BompSmoothPhase', 0.0)  # Balance of market power smoothing phase
BandsPeriod = _input('BandsPeriod', 9)  # Bands period
BandsDeviation = _input('BandsDeviation', 0.5)  # Bands deviation
ColorOn = _input('ColorOn', chg_onMiddle)  # Color change on
AlertsOn = _input('AlertsOn', False)  # Turn alerts on?
AlertsOnCurrent = _input('AlertsOnCurrent', True)  # Alert on current bar?
AlertsMessage = _input('AlertsMessage', True)  # Display messageas on alerts?
AlertsSound = _input('AlertsSound', False)  # Play sound on alerts?
AlertsEmail = _input('AlertsEmail', False)  # Send email on alerts?
AlertsNotify = _input('AlertsNotify', False)  # Send push notification on alerts?
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
fup = Arr(0, 0.0)
fmi = Arr(0, 0.0)
fdn = Arr(0, 0.0)
_smthWork = Arr(0, 0.0, dims=(20,))

def OnInit():
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, fmi, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    for i in range(0, 2):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Balance of market power (' + _str(BompSmoothPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    colorOn = (ColorOn if (BandsPeriod > 1) else chg_onSlope)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        range_ = MathMax(high[i] - low[i], DBL_MIN)
        buo = _fdiv(high[i] - open[i], range_)
        buc = _fdiv(close[i] - low[i], range_)
        buoc = _fdiv(MathMax(close[i] - open[i], 0), range_)
        beo = _fdiv(open[i] - low[i], range_)
        bec = _fdiv(high[i] - close[i], range_)
        beoc = _fdiv(MathMax(open[i] - close[i], 0), range_)
        val[i] = iSmooth(((buo + buc + buoc) / 3.0) - ((beo + bec + beoc) / 3.0), BompSmoothPeriod, BompSmoothPhase, i, rates_total, 0)
        if BandsPeriod > 1:
            avg = iSmooth(val[i], BandsPeriod, BompSmoothPhase, i, rates_total, 1)
            dev = 0.0
            k = 0
            while k < BandsPeriod and (i - k) >= 0:
                dev += MathPow(val[i - k] - avg, 2)
                k += 1
            dev = MathSqrt(dev / BandsPeriod)
            fup[i] = avg + dev
            fdn[i] = avg - dev
            fmi[i] = avg
        else:
            fmi[i] = val[i]
            fdn[i] = fmi[i]
            fup[i] = fdn[i]
        _sw1 = colorOn
        if _sw1 == chg_onLevel:
            valc[i] = (1 if (val[i] > fup[i]) else 2 if (val[i] < fdn[i]) else 0 if (val[i] < fup[i] and val[i] > fdn[i]) else valc[i - 1] if (i > 0) else 0)
        elif _sw1 == chg_onMiddle:
            valc[i] = (1 if (val[i] > fmi[i]) else 2 if (val[i] < fmi[i]) else valc[i - 1] if (i > 0) else 0)
        else:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    manageAlerts(time, valc, rates_total)
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
        message = Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' Balance of market power state changed to ' + doWhat
        if AlertsMessage:
            Alert(message)
        if AlertsEmail:
            SendMail(Symbol() + ' Balance of market power', message)
        if AlertsNotify:
            SendNotification(message)
        if AlertsSound:
            PlaySound('alert2.wav')

def iSmooth(price, length, phase, r, bars, instanceNo=0):
    if ArrayRange(_smthWork, 0) != bars:
        ArrayResize(_smthWork, bars)
    instanceNo *= 10
    if price == EMPTY_VALUE:
        price = 0.0
    k = 0
    if r == 0:
        while k < 7:
            _smthWork[0][instanceNo + k] = price
            k += 1
        while k < 10:
            _smthWork[0][instanceNo + k] = 0.0
            k += 1
        return price
    len1 = MathMax(_fdiv(MathLog(MathSqrt(0.5 * (length - 1))), MathLog(2.0)) + 2.0, 0)
    pow1 = MathMax(len1 - 2.0, 0.5)
    del1 = price - _smthWork[r - 1][instanceNo + 5]
    del2 = price - _smthWork[r - 1][instanceNo + 6]
    div = _fdiv(1.0, 10.0 + ((10.0 * MathMin(MathMax(length - 10, 0), 100)) / 100))
    forBar = MathMin(r, 10)
    _smthWork[r][instanceNo + 7] = (MathAbs(del1) if (MathAbs(del1) > MathAbs(del2)) else MathAbs(del2) if (MathAbs(del1) < MathAbs(del2)) else 0)
    _smthWork[r][instanceNo + 8] = _smthWork[r - 1][instanceNo + 8] + ((_smthWork[r][instanceNo + 7] - _smthWork[r - forBar][instanceNo + 7]) * div)
    _smthWork[r][instanceNo + 9] = _smthWork[r - 1][instanceNo + 9] + (_fdiv(2.0, MathMax(4.0 * length, 30) + 1.0) * (_smthWork[r][instanceNo + 8] - _smthWork[r - 1][instanceNo + 9]))
    dVolty = (_fdiv(_smthWork[r][instanceNo + 7], _smthWork[r][instanceNo + 9]) if (_smthWork[r][instanceNo + 9] > 0) else 0)
    if dVolty > MathPow(len1, _fdiv(1.0, pow1)):
        dVolty = MathPow(len1, _fdiv(1.0, pow1))
    if dVolty < 1:
        dVolty = 1.0
    pow2 = MathPow(dVolty, pow1)
    len2 = MathSqrt(0.5 * (length - 1)) * len1
    Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
    if del1 > 0:
        _smthWork[r][instanceNo + 5] = price
    else:
        _smthWork[r][instanceNo + 5] = price - (Kv * del1)
    if del2 < 0:
        _smthWork[r][instanceNo + 6] = price
    else:
        _smthWork[r][instanceNo + 6] = price - (Kv * del2)
    R = (MathMax(MathMin(phase, 100), -100) / 100.0) + 1.5
    beta = _fdiv(0.45 * (length - 1), (0.45 * (length - 1)) + 2)
    alpha = MathPow(beta, pow2)
    _smthWork[r][instanceNo + 0] = price + (alpha * (_smthWork[r - 1][instanceNo + 0] - price))
    _smthWork[r][instanceNo + 1] = ((price - _smthWork[r][instanceNo + 0]) * (1 - beta)) + (beta * _smthWork[r - 1][instanceNo + 1])
    _smthWork[r][instanceNo + 2] = _smthWork[r][instanceNo + 0] + (R * _smthWork[r][instanceNo + 1])
    _smthWork[r][instanceNo + 3] = ((_smthWork[r][instanceNo + 2] - _smthWork[r - 1][instanceNo + 4]) * MathPow(1 - alpha, 2)) + (MathPow(alpha, 2) * _smthWork[r - 1][instanceNo + 3])
    _smthWork[r][instanceNo + 4] = _smthWork[r - 1][instanceNo + 4] + _smthWork[r][instanceNo + 3]
    return _smthWork[r][instanceNo + 4]

# ---- static local variables
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BalanceOfMarketPower2(_MQL5Indicator):
    name = 'Balance_of_market_power_2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BompSmoothPeriod': 90.0,  # Balance of market power smoothing period
        'BompSmoothPhase': 0.0,  # Balance of market power smoothing phase
        'BandsPeriod': 9,  # Bands period
        'BandsDeviation': 0.5,  # Bands deviation
        'ColorOn': _Choice({0: 'change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross'}, default=2),  # Color change on
        'AlertsOn': False,  # Turn alerts on?
        'AlertsOnCurrent': True,  # Alert on current bar?
        'AlertsMessage': True,  # Display messageas on alerts?
        'AlertsSound': False,  # Play sound on alerts?
        'AlertsEmail': False,  # Send email on alerts?
        'AlertsNotify': False,  # Send push notification on alerts?
    }

