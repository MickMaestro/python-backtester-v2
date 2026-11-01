"""Swing_line_1.1 — converted from MQL5: MQL5 Indicators/Swing line - extended version/Swing_line_1.1.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 3329330, 9662683]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'Swing line'}, 'levels': [], 'description': [], 'name': 'Swing_line_1.1', 'source': 'MQL5 Indicators/Swing line - extended version/Swing_line_1.1.mq5', 'folder': 'Swing line - extended version', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'AlertsOn', 'py': 'AlertsOn', 'param': 'AlertsOn', 'type': 'bool', 'default': False, 'label': 'Turn alerts on?', 'sinput': False}, {'mql': 'AlertsOnCurrent', 'py': 'AlertsOnCurrent', 'param': 'AlertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar?', 'sinput': False}, {'mql': 'AlertsMessage', 'py': 'AlertsMessage', 'param': 'AlertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messages on alerts?', 'sinput': False}, {'mql': 'AlertsSound', 'py': 'AlertsSound', 'param': 'AlertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts?', 'sinput': False}, {'mql': 'AlertsEmail', 'py': 'AlertsEmail', 'param': 'AlertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts?', 'sinput': False}, {'mql': 'AlertsNotify', 'py': 'AlertsNotify', 'param': 'AlertsNotify', 'type': 'bool', 'default': False, 'label': 'Send push notification on alerts?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
AlertsOn = _input('AlertsOn', False)  # Turn alerts on?
AlertsOnCurrent = _input('AlertsOnCurrent', True)  # Alert on current bar?
AlertsMessage = _input('AlertsMessage', True)  # Display messages on alerts?
AlertsSound = _input('AlertsSound', False)  # Play sound on alerts?
AlertsEmail = _input('AlertsEmail', False)  # Send email on alerts?
AlertsNotify = _input('AlertsNotify', False)  # Send push notification on alerts?
Interpolate = _input('Interpolate', True)  # Interpolate in multi time frame mode?
swli = Arr(0, 0.0)
swlic = Arr(0, 0.0)
count = Arr(0, 0.0)
_indicatorTimeFrame = 0
_mtfHandle = INVALID_HANDLE
work = Arr(0, 0.0, dims=(5,))

def OnInit():
    global _indicatorTimeFrame, _mtfHandle
    SetIndexBuffer(0, swli, INDICATOR_DATA)
    SetIndexBuffer(1, swlic, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, count, INDICATOR_CALCULATIONS)
    _indicatorTimeFrame = MathMax(Period(), TimeFrame)
    if _indicatorTimeFrame != Period():
        _mtfHandle = iCustom(Symbol(), _indicatorTimeFrame, getName(), PERIOD_CURRENT, AlertsOn, AlertsOnCurrent, AlertsMessage, AlertsSound, AlertsEmail, AlertsNotify)
        if _mtfHandle == INVALID_HANDLE:
            return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if _indicatorTimeFrame != Period():
        result = Arr(1, 0.0, dyn=False)
        if CopyBuffer(_mtfHandle, 2, 0, 1, result) < 1:
            for i in range(prev_calculated, rates_total):
                Comment(StringSubstr(EnumToString(_indicatorTimeFrame, 'ENUM_TIMEFRAMES'), 7) + ' data not ready\nnext attempt will be made on new tick')
            return prev_calculated
        elif StringFind(ChartGetString(0, CHART_COMMENT), 'data not ready') >= 0:
            Comment('')
        n = 0
        k = 0
        i = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _int(_fdiv(result[0] * float(PeriodSeconds(_indicatorTimeFrame)), PeriodSeconds(Period()))) - 1, 0))
        _prevMark = -99
        _prevTime = 0
        while i < rates_total:
            _currMark = iBarShift(Symbol(), _indicatorTimeFrame, time[i])
            if _currMark < 0:
                i += 1
                continue
            if _currMark != _prevMark:
                _prevMark = _currMark
                _prevTime = time[i]
                if CopyBuffer(_mtfHandle, 0, _currMark, 1, result) < 1:
                    break
                swli[i] = result[0]
                if CopyBuffer(_mtfHandle, 1, _currMark, 1, result) < 1:
                    break
                swlic[i] = result[0]
            else:
                swli[i] = swli[i - 1]
                swlic[i] = swlic[i - 1]
            if not Interpolate:
                i += 1
                continue
            _nextMark = (iBarShift(Symbol(), _indicatorTimeFrame, time[i + 1]) if (i < (rates_total - 1)) else (_prevMark + 1))
            if _nextMark == _prevMark:
                i += 1
                continue
            n = 1
            while (i - n) > 0 and time[i - n] >= _prevTime:
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                swli[i - k] = swli[i] + _fdiv((swli[i - n] - swli[i]) * k, n)
                k += 1
            i += 1
        return rates_total
    if ArrayRange(work, 0) != rates_total:
        ArrayResize(work, rates_total)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        work[i][4] = (work[i - 1][4] if (i > 0) else -1)
        work[i][0] = (work[i - 1][0] if (i > 0) else high[i])
        work[i][1] = (work[i - 1][1] if (i > 0) else low[i])
        work[i][2] = (work[i - 1][2] if (i > 0) else high[i])
        work[i][3] = (work[i - 1][3] if (i > 0) else low[i])
        if i > 0 and work[i - 1][4] == 1:
            work[i][0] = MathMax(work[i - 1][0], high[i])
            work[i][1] = MathMax(work[i - 1][1], low[i])
            if high[i] < work[i][1]:
                work[i][4] = -1.0
                work[i][2] = high[i]
                work[i][3] = low[i]
        if i > 0 and work[i - 1][4] == -1:
            work[i][2] = MathMin(work[i - 1][2], high[i])
            work[i][3] = MathMin(work[i - 1][3], low[i])
            if low[i] > work[i][2]:
                work[i][4] = 1.0
                work[i][0] = high[i]
                work[i][1] = low[i]
        swli[i] = (work[i][1] if (work[i][4] == 1) else work[i][2] if (work[i][4] == -1) else close[i])
        swlic[i] = (1 if (work[i][4] == 1) else 2 if (work[i][4] == -1) else 0)
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    manageAlerts(time, swlic, rates_total)
    return rates_total

def manageAlerts(time, ttrend, bars):
    if not AlertsOn:
        return
    whichBar = bars - 1
    if not AlertsOnCurrent:
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
        message = StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' ' + Symbol() + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' swing line state changed to ' + doWhat
        if AlertsMessage:
            Alert(message)
        if AlertsEmail:
            SendMail(Symbol() + ' swing line', message)
        if AlertsNotify:
            SendNotification(message)
        if AlertsSound:
            PlaySound('alert2.wav')

def getName():
    _path = Box(MQL5InfoString(MQL5_PROGRAM_PATH))
    StringToLower(_path)
    _partsA = Arr(0, "")
    _partsN = StringSplit(_path.v, StringGetCharacter('\\', 0), _partsA)
    name = _partsA[_partsN - 1]
    n = _partsN - 2
    while n >= 0 and _partsA[n] != 'indicators':
        name = _partsA[n] + '\\' + name
        n -= 1
    return name

# ---- static local variables
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SwingLine11(_MQL5Indicator):
    name = 'Swing_line_1.1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'AlertsOn': False,  # Turn alerts on?
        'AlertsOnCurrent': True,  # Alert on current bar?
        'AlertsMessage': True,  # Display messages on alerts?
        'AlertsSound': False,  # Play sound on alerts?
        'AlertsEmail': False,  # Send email on alerts?
        'AlertsNotify': False,  # Send push notification on alerts?
        'Interpolate': True,  # Interpolate in multi time frame mode?
    }

