"""nonlag_ma_macd_-_mtf_amp_alerts — converted from MQL5: MQL5 Indicators/Nonlag_MA_MACD/nonlag_ma_macd_-_mtf_amp_alerts.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 10, 2: 1, 3: 1}, 'colors': {1: [16760576, 9662683], 2: [16760576], 3: [6908265]}, 'widths': {1: 2, 2: 2, 3: 1}, 'styles': {1: 0, 2: 0, 3: 2}, 'labels': {2: 'NonLag ma MACD'}, 'levels': [], 'description': [], 'name': 'nonlag_ma_macd_-_mtf_amp_alerts', 'source': 'MQL5 Indicators/Nonlag_MA_MACD/nonlag_ma_macd_-_mtf_amp_alerts.mq5', 'folder': 'Nonlag_MA_MACD', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'FastLength', 'py': 'FastLength', 'param': 'FastLength', 'type': 'int', 'default': 12, 'label': 'Fast MACD length', 'sinput': False}, {'mql': 'SlowLength', 'py': 'SlowLength', 'param': 'SlowLength', 'type': 'int', 'default': 26, 'label': 'Slow MACD length', 'sinput': False}, {'mql': 'SignalLength', 'py': 'SignalLength', 'param': 'SignalLength', 'type': 'int', 'default': 9, 'label': 'Signal length', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price to use', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data', 'sinput': False}, {'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': False, 'label': 'Alert on trend change', 'sinput': False}, {'mql': 'alertsOnCurrent', 'py': 'alertsOnCurrent', 'param': 'alertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar', 'sinput': False}, {'mql': 'alertsMessage', 'py': 'alertsMessage', 'param': 'alertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
FastLength = _input('FastLength', 12)  # Fast MACD length
SlowLength = _input('SlowLength', 26)  # Slow MACD length
SignalLength = _input('SignalLength', 9)  # Signal length
Price = _input('Price', PRICE_CLOSE)  # Price to use
Interpolate = _input('Interpolate', True)  # Interpolate mtf data
alertsOn = _input('alertsOn', False)  # Alert on trend change
alertsOnCurrent = _input('alertsOnCurrent', True)  # Alert on current bar
alertsMessage = _input('alertsMessage', True)  # Display messageas on alerts
alertsSound = _input('alertsSound', False)  # Play sound on alerts
alertsEmail = _input('alertsEmail', False)  # Send email on alerts
macd = Arr(0, 0.0)
signal = Arr(0, 0.0)
osma = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
countBuffer = Arr(0, 0.0)
timeFrame = 0
mtfHandle = 0
calculating = False
nlm_values = Arr(3, 0.0, dyn=False, dims=(3,))
nlm_prices = Arr(0, 0.0, dims=(3,))
nlm_alphas = Arr(0, 0.0, dims=(3,))

def OnInit():
    global calculating, mtfHandle, timeFrame
    SetIndexBuffer(0, osma, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 2)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, macd, INDICATOR_DATA)
    SetIndexBuffer(3, signal, INDICATOR_DATA)
    SetIndexBuffer(4, countBuffer, INDICATOR_CALCULATIONS)
    timeFrame = MathMax(Period(), TimeFrame)
    calculating = timeFrame == Period()
    if not calculating:
        name = getIndicatorName()
        mtfHandle = iCustom(None, timeFrame, name, PERIOD_CURRENT, FastLength, SlowLength, SignalLength, Price)
    IndicatorSetString(INDICATOR_SHORTNAME, getPeriodToString(timeFrame) + ' NonLag ma MACD (' + _str(FastLength) + ',' + _str(SlowLength) + ',' + _str(SignalLength) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if calculating:
        for i in range(MathMax(prev_calculated - 1, 0), rates_total):
            price = getPrice(Price, open, close, high, low, i)
            macd[i] = iNoLagMa(price, FastLength, i, 0) - iNoLagMa(price, SlowLength, i, 1)
            signal[i] = iNoLagMa(macd[i], SignalLength, i, 2)
            osma[i] = macd[i] - signal[i]
            if i > 0:
                colorBuffer[i] = colorBuffer[i - 1]
                if osma[i] > 0:
                    colorBuffer[i] = 0.0
                if osma[i] < 0:
                    colorBuffer[i] = 1.0
        countBuffer[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
        manageAlerts(time[rates_total - 1], time[rates_total - 2], colorBuffer, rates_total)
        return rates_total
    times = Arr(0, 0)
    startTime = time[0] - PeriodSeconds(timeFrame)
    endTime = time[rates_total - 1]
    bars = CopyTime(None, timeFrame, _DT(startTime), _DT(endTime), times)
    if times[0] > time[0] or bars < 1:
        return prev_calculated
    tosma = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 0, 0, bars, tosma)
    tcolo = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 1, 0, bars, tcolo)
    tmacd = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 2, 0, bars, tmacd)
    tsign = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 3, 0, bars, tsign)
    count = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 4, 0, bars, count)
    maxb = _int(MathMax(MathMin(_fdiv(count[bars - 1] * PeriodSeconds(timeFrame), PeriodSeconds(Period())), rates_total - 1), 1))
    for i in range(MathMax(prev_calculated - maxb, 0), rates_total):
        d = dateArrayBsearch(times, time[i], bars)
        if d > -1 and d < bars:
            osma[i] = tosma[d]
            macd[i] = tmacd[d]
            signal[i] = tsign[d]
            colorBuffer[i] = tcolo[d]
        if not Interpolate:
            continue
        j = MathMin(i + 1, rates_total - 1)
        if d != dateArrayBsearch(times, time[j], bars) or i == j:
            n = 0
            k = 0
            n = 1
            while (i - n) > 0 and time[i - n] >= times[d]:
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                macd[i - k] = macd[i] + _fdiv((macd[i - n] - macd[i]) * k, n)
                osma[i - k] = osma[i] + _fdiv((osma[i - n] - osma[i]) * k, n)
                signal[i - k] = signal[i] + _fdiv((signal[i - n] - signal[i]) * k, n)
                k += 1
    manageAlerts(times[bars - 1], times[bars - 2], tcolo, bars)
    return rates_total

def iNoLagMa(price, length, r, instanceNo=0):
    if ArrayRange(nlm_prices, 0) != Bars(Symbol(), 0):
        ArrayResize(nlm_prices, Bars(Symbol(), 0))
    nlm_prices[r][instanceNo] = price
    if length < 3 or r < 3:
        return nlm_prices[r][instanceNo]
    if nlm_values[0][instanceNo] != length:
        Cycle = 4.0
        Coeff = 3.0 * 3.141592653589793
        Phase = length - 1
        nlm_values[0][instanceNo] = length
        nlm_values[1][instanceNo] = (length * 4) + Phase
        nlm_values[2][instanceNo] = 0.0
        if ArrayRange(nlm_alphas, 0) < nlm_values[1][instanceNo]:
            ArrayResize(nlm_alphas, _int(nlm_values[1][instanceNo]))
        k = 0
        while k < nlm_values[1][instanceNo]:
            t = 0.0
            if k <= (Phase - 1):
                t = _fdiv(1.0 * k, Phase - 1)
            else:
                t = 1.0 + _fdiv((k - Phase + 1) * ((2.0 * Cycle) - 1.0), (Cycle * length) - 1.0)
            beta = MathCos(3.141592653589793 * t)
            g = _fdiv(1.0, (Coeff * t) + 1)
            if t <= 0.5:
                g = 1.0
            nlm_alphas[k][instanceNo] = g * beta
            nlm_values[2][instanceNo] += nlm_alphas[k][instanceNo]
            k += 1
    if nlm_values[2][instanceNo] > 0:
        sum_ = 0.0
        k = 0
        while k < nlm_values[1][instanceNo] and (r - k) >= 0:
            sum_ += nlm_alphas[k][instanceNo] * nlm_prices[r - k][instanceNo]
            k += 1
        return _fdiv(sum_, nlm_values[2][instanceNo])
    else:
        return 0.0

def manageAlerts(currTime, prevTime, trend, bars):
    if alertsOn:
        time = currTime
        whichBar = bars - 1
        if not alertsOnCurrent:
            whichBar = bars - 2
            time = prevTime
        if trend[whichBar] != trend[whichBar - 1]:
            if trend[whichBar] == 0:
                doAlert(time, 'up')
            if trend[whichBar] == 1:
                doAlert(time, 'down')

def doAlert(forTime, doWhat):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    message = ""
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != forTime:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = forTime
        message = Symbol() + ' ' + getPeriodToString(timeFrame) + ' at ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' NonLag ma MACD trend changed to ' + doWhat
        if alertsMessage:
            Alert(message)
        if alertsEmail:
            SendMail(Symbol() + ' NonLag ma MACD', message)
        if alertsSound:
            PlaySound('alert2.wav')

def getPrice(price, open, close, high, low, i):
    _sw1 = price
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

def getIndicatorName():
    progPath = MQL5InfoString(MQL5_PROGRAM_PATH)
    terminalPath = TerminalInfoString(TERMINAL_PATH)
    startLength = StringLen(terminalPath) + 17
    progLength = StringLen(progPath)
    indicatorName = StringSubstr(progPath, startLength)
    indicatorName = StringSubstr(indicatorName, 0, StringLen(indicatorName) - 4)
    return indicatorName

def getPeriodToString(period):
    i = 0
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    for i in range(i, 20):
        if period == _s_getPeriodToString__per[i]:
            break
    else:
        i = _range_end(i, 20, 1)
    return _s_getPeriodToString__tfs[i]

def dateArrayBsearch(times, toFind, total):
    mid = 0
    first = 0
    last = total - 1
    while last >= first:
        mid = (first + last) >> 1
        if toFind == times[mid] or ((mid < (total - 1) and toFind > times[mid]) and toFind < times[mid + 1]):
            break
        if toFind < times[mid]:
            last = mid - 1
        else:
            first = mid + 1
    return mid

# ---- static local variables
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0
_s_getPeriodToString__per = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 0x4001, 0x4002, 0x4003, 0x4004, 0x4006, 0x4008, 0x400c, 0x4018, 0x8001, 0xc001], fill=0)
_s_getPeriodToString__tfs = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NonlagMaMacdMtfAmpAlerts(_MQL5Indicator):
    name = 'nonlag_ma_macd_-_mtf_amp_alerts'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'FastLength': 12,  # Fast MACD length
        'SlowLength': 26,  # Slow MACD length
        'SignalLength': 9,  # Signal length
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price to use
        'Interpolate': True,  # Interpolate mtf data
        'alertsOn': False,  # Alert on trend change
        'alertsOnCurrent': True,  # Alert on current bar
        'alertsMessage': True,  # Display messageas on alerts
        'alertsSound': False,  # Play sound on alerts
        'alertsEmail': False,  # Send email on alerts
    }

