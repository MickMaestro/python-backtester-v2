"""zerolag_tema_bars — converted from MQL5: MQL5 Indicators/Zerolag Tema Bars/zerolag_tema_bars.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 16}, 'colors': {1: [11119017], 2: [11119017], 3: [16760576, 9662683]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2, 3: 0}, 'labels': {1: 'ZlTema long', 2: 'ZlTema short', 3: 'ZlTemaTrend'}, 'levels': [], 'description': [], 'name': 'zerolag_tema_bars', 'source': 'MQL5 Indicators/Zerolag Tema Bars/zerolag_tema_bars.mq5', 'folder': 'Zerolag Tema Bars', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'LongPeriod', 'py': 'LongPeriod', 'param': 'LongPeriod', 'type': 'int', 'default': 55, 'label': 'Long period', 'sinput': False}, {'mql': 'LongPrice', 'py': 'LongPrice', 'param': 'LongPrice', 'type': 'int', 'default': 13, 'label': 'Long price', 'sinput': False}, {'mql': 'ShortPeriod', 'py': 'ShortPeriod', 'param': 'ShortPeriod', 'type': 'int', 'default': 55, 'label': 'Short period', 'sinput': False}, {'mql': 'ShortPrice', 'py': 'ShortPrice', 'param': 'ShortPrice', 'type': 'int', 'default': 5, 'label': 'Short price', 'sinput': False}, {'mql': 'LinesVisible', 'py': 'LinesVisible', 'param': 'LinesVisible', 'type': 'int', 'default': 0, 'label': 'Lines', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data', 'sinput': False}, {'mql': 'ViewAsCandles', 'py': 'ViewAsCandles', 'param': 'ViewAsCandles', 'type': 'bool', 'default': False, 'label': 'View as candles ?', 'sinput': False}, {'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': False, 'label': 'Alert on trend change', 'sinput': False}, {'mql': 'alertsOnCurrent', 'py': 'alertsOnCurrent', 'param': 'alertsOnCurrent', 'type': 'bool', 'default': True, 'label': 'Alert on current bar', 'sinput': False}, {'mql': 'alertsMessage', 'py': 'alertsMessage', 'param': 'alertsMessage', 'type': 'bool', 'default': True, 'label': 'Display messageas on alerts', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': 'Play sound on alerts', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': 'Send email on alerts', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_haclose = 7
pr_haopen = 8
pr_hahigh = 9
pr_halow = 10
pr_hamedian = 11
pr_hatypical = 12
pr_haweighted = 13
pr_haaverage = 14
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_haclose', 8: 'pr_haopen', 9: 'pr_hahigh', 10: 'pr_halow', 11: 'pr_hamedian', 12: 'pr_hatypical', 13: 'pr_haweighted', 14: 'pr_haaverage'})

# enum enLinesVisible
lv_visible = 0
lv_invisible = 1
_enum('enLinesVisible', {0: 'lv_visible', 1: 'lv_invisible'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
LongPeriod = _input('LongPeriod', 55)  # Long period
LongPrice = _input('LongPrice', pr_haweighted)  # Long price
ShortPeriod = _input('ShortPeriod', 55)  # Short period
ShortPrice = _input('ShortPrice', pr_typical)  # Short price
LinesVisible = _input('LinesVisible', lv_visible)  # Lines
Interpolate = _input('Interpolate', True)  # Interpolate mtf data
ViewAsCandles = _input('ViewAsCandles', False)  # View as candles ?
alertsOn = _input('alertsOn', False)  # Alert on trend change
alertsOnCurrent = _input('alertsOnCurrent', True)  # Alert on current bar
alertsMessage = _input('alertsMessage', True)  # Display messageas on alerts
alertsSound = _input('alertsSound', False)  # Play sound on alerts
alertsEmail = _input('alertsEmail', False)  # Send email on alerts
zlth = Arr(0, 0.0)
zltl = Arr(0, 0.0)
zlto = Arr(0, 0.0)
zltc = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
countBuffer = Arr(0, 0.0)
longb = Arr(0, 0.0)
shortb = Arr(0, 0.0)
timeFrame = 0
mtfHandle = 0
atrHandle = 0
calculating = False
workHa = Arr(0, 0.0, dims=(4,))
workTema = Arr(0, 0.0, dims=(12,))

def OnInit():
    global calculating, mtfHandle, timeFrame
    style = 0
    style = DRAW_NONE
    if LinesVisible == lv_visible:
        style = DRAW_LINE
    SetIndexBuffer(0, longb, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, style)
    SetIndexBuffer(1, shortb, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, style)
    style = DRAW_COLOR_BARS
    if ViewAsCandles:
        style = DRAW_COLOR_CANDLES
    SetIndexBuffer(2, zlto, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, style)
    SetIndexBuffer(3, zlth, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, style)
    SetIndexBuffer(4, zltl, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_TYPE, style)
    SetIndexBuffer(5, zltc, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_TYPE, style)
    SetIndexBuffer(6, colorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, countBuffer, INDICATOR_CALCULATIONS)
    timeFrame = MathMax(Period(), TimeFrame)
    calculating = timeFrame == Period()
    if not calculating:
        mtfHandle = iCustom(None, timeFrame, getIndicatorName(), PERIOD_CURRENT, LongPeriod, LongPrice, ShortPeriod, ShortPrice)
    IndicatorSetString(INDICATOR_SHORTNAME, getPeriodToString(timeFrame) + ' ZeroLag tema trend (' + _str(LongPeriod) + ',' + _str(ShortPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if calculating:
        for i in range(MathMax(prev_calculated - 1, 0), rates_total):
            if LongPeriod > 1:
                tema10 = iTema(getPrice(LongPrice, open, close, high, low, i, rates_total), LongPeriod, i, rates_total, 0)
                tema11 = iTema(tema10, LongPeriod, i, rates_total, 1)
                longb[i] = (2.0 * tema10) - tema11
            if ShortPeriod > 1:
                tema20 = iTema(getPrice(ShortPrice, open, close, high, low, i, rates_total), ShortPeriod, i, rates_total, 2)
                tema21 = iTema(tema20, ShortPeriod, i, rates_total, 3)
                shortb[i] = (2.0 * tema20) - tema21
            if LongPeriod > 1 and ShortPeriod > 1:
                if longb[i] > shortb[i]:
                    colorBuffer[i] = 1.0
                if longb[i] < shortb[i]:
                    colorBuffer[i] = 0.0
                zltc[i] = close[i]
                zlto[i] = open[i]
                zlth[i] = high[i]
                zltl[i] = low[i]
        countBuffer[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
        manageAlerts(time[rates_total - 1], time[rates_total - 2], colorBuffer, rates_total)
        return rates_total
    if BarsCalculated(mtfHandle) < LongPeriod:
        return 0
    times = Arr(0, 0)
    startTime = time[0] - PeriodSeconds(timeFrame)
    endTime = time[rates_total - 1]
    bars = CopyTime(None, timeFrame, _DT(startTime), _DT(endTime), times)
    if times[0] > time[0] or bars < 1:
        return rates_total
    tlong = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 0, 0, bars, tlong)
    tshor = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 1, 0, bars, tshor)
    tcolo = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 6, 0, bars, tcolo)
    count = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 7, 0, bars, count)
    maxb = _int(MathMax(MathMin(_fdiv(count[bars - 1] * PeriodSeconds(timeFrame), PeriodSeconds(Period())), rates_total - 1), 1))
    drawLines = LinesVisible == lv_visible and (LongPeriod > 1 or ShortPeriod > 1)
    for i in range(MathMax(prev_calculated - maxb, 0), rates_total):
        d = dateArrayBsearch(times, time[i], bars)
        if d > -1 and d < bars:
            zltc[i] = close[i]
            zlto[i] = open[i]
            zlth[i] = high[i]
            zltl[i] = low[i]
            colorBuffer[i] = tcolo[d]
            if drawLines:
                longb[i] = tlong[d]
                shortb[i] = tshor[d]
        if (not Interpolate) or (not drawLines):
            continue
        j = MathMin(i + 1, rates_total - 1)
        if d != dateArrayBsearch(times, time[j], bars) or i == j:
            n = 0
            k = 0
            n = 1
            while ((i - n) > 0 and time[i - n] >= times[d]) and n < _idiv(PeriodSeconds(timeFrame), PeriodSeconds(Period())):
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                if LongPeriod > 1:
                    longb[i - k] = longb[i] + _fdiv((longb[i - n] - longb[i]) * float(k), n)
                if ShortPeriod > 1:
                    shortb[i - k] = shortb[i] + _fdiv((shortb[i - n] - shortb[i]) * float(k), n)
                k += 1
    manageAlerts(times[bars - 1], times[bars - 2], tcolo, bars)
    return rates_total

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
        message = getPeriodToString(timeFrame) + ' ' + Symbol() + ' at : ' + TimeToString(TimeLocal(), TIME_SECONDS) + ' Zero Lag tema trend changed to ' + doWhat
        if alertsMessage:
            Alert(message)
        if alertsEmail:
            SendMail(Symbol() + ' Zero lag tema trend', message)
        if alertsSound:
            PlaySound('alert2.wav')

def getPrice(price, open, close, high, low, i, bars):
    if price >= pr_haclose and price <= pr_haaverage:
        if ArrayRange(workHa, 0) != bars:
            ArrayResize(workHa, bars)
        haOpen = 0.0
        if i > 0:
            haOpen = (workHa[i - 1][2] + workHa[i - 1][3]) / 2.0
        else:
            haOpen = open[i] + close[i]
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        if haOpen < haClose:
            workHa[i][0] = haLow
            workHa[i][1] = haHigh
        else:
            workHa[i][0] = haHigh
            workHa[i][1] = haLow
        workHa[i][2] = haOpen
        workHa[i][3] = haClose
        _sw1 = price
        if _sw1 == pr_haclose:
            return haClose
        elif _sw1 == pr_haopen:
            return haOpen
        elif _sw1 == pr_hahigh:
            return haHigh
        elif _sw1 == pr_halow:
            return haLow
        elif _sw1 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw1 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw1 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw1 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
    _sw2 = price
    if _sw2 == pr_close:
        return close[i]
    elif _sw2 == pr_open:
        return open[i]
    elif _sw2 == pr_high:
        return high[i]
    elif _sw2 == pr_low:
        return low[i]
    elif _sw2 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

def iTema(price, period, r, bars, instanceNo=0):
    if ArrayRange(workTema, 0) != bars:
        ArrayResize(workTema, bars)
    instanceNo *= 3
    if r == 0:
        workTema[r][0 + instanceNo] = price
        workTema[r][1 + instanceNo] = price
        workTema[r][2 + instanceNo] = price
        return price
    alpha = _fdiv(2.0, 1.0 + period)
    workTema[r][0 + instanceNo] = workTema[r - 1][0 + instanceNo] + (alpha * (price - workTema[r - 1][0 + instanceNo]))
    workTema[r][1 + instanceNo] = workTema[r - 1][1 + instanceNo] + (alpha * (workTema[r][0 + instanceNo] - workTema[r - 1][1 + instanceNo]))
    workTema[r][2 + instanceNo] = workTema[r - 1][2 + instanceNo] + (alpha * (workTema[r][1 + instanceNo] - workTema[r - 1][2 + instanceNo]))
    return workTema[r][2 + instanceNo] + (3.0 * (workTema[r][0 + instanceNo] - workTema[r][1 + instanceNo]))

def getIndicatorName():
    progPath = MQL5InfoString(MQL5_PROGRAM_PATH)
    toFind = 'MQL5\\Indicators\\'
    startLength = StringFind(progPath, toFind) + StringLen(toFind)
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


class ZerolagTemaBars(_MQL5Indicator):
    name = 'zerolag_tema_bars'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'LongPeriod': 55,  # Long period
        'LongPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Heiken ashi close', 8: 'Heiken ashi open', 9: 'Heiken ashi high', 10: 'Heiken ashi low', 11: 'Heiken ashi median', 12: 'Heiken ashi typical', 13: 'Heiken ashi weighted', 14: 'Heiken ashi average'}, default=13),  # Long price
        'ShortPeriod': 55,  # Short period
        'ShortPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Heiken ashi close', 8: 'Heiken ashi open', 9: 'Heiken ashi high', 10: 'Heiken ashi low', 11: 'Heiken ashi median', 12: 'Heiken ashi typical', 13: 'Heiken ashi weighted', 14: 'Heiken ashi average'}, default=5),  # Short price
        'LinesVisible': _Choice({0: 'ZeroLag lines visible', 1: 'ZeroLag lines not visible'}, default=0),  # Lines
        'Interpolate': True,  # Interpolate mtf data
        'ViewAsCandles': False,  # View as candles ?
        'alertsOn': False,  # Alert on trend change
        'alertsOnCurrent': True,  # Alert on current bar
        'alertsMessage': True,  # Display messageas on alerts
        'alertsSound': False,  # Play sound on alerts
        'alertsEmail': False,  # Send email on alerts
    }

