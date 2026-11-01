"""leader_of_the_macd — converted from MQL5: MQL5 Indicators/Leader of the MACD/leader_of_the_macd.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 1}, 'colors': {1: [15986136, 14804223], 2: [16760576, 9662683], 3: [11119017]}, 'widths': {2: 2}, 'styles': {2: 0, 3: 4}, 'labels': {1: 'Leader of the MACD', 2: 'MACD', 3: 'MACD signal line'}, 'levels': [], 'description': [], 'name': 'leader_of_the_macd', 'source': 'MQL5 Indicators/Leader of the MACD/leader_of_the_macd.mq5', 'folder': 'Leader of the MACD', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'FastEMAPeriod', 'py': 'FastEMAPeriod', 'param': 'FastEMAPeriod', 'type': 'int', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'SlowEMAPeriod', 'py': 'SlowEMAPeriod', 'param': 'SlowEMAPeriod', 'type': 'int', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'SignalEMAPeriod', 'py': 'SignalEMAPeriod', 'param': 'SignalEMAPeriod', 'type': 'int', 'default': 9, 'label': 'Signal EMA period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price to use', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
FastEMAPeriod = _input('FastEMAPeriod', 12)  # Fast EMA period
SlowEMAPeriod = _input('SlowEMAPeriod', 26)  # Slow EMA period
SignalEMAPeriod = _input('SignalEMAPeriod', 9)  # Signal EMA period
Price = _input('Price', PRICE_CLOSE)  # Price to use
Interpolate = _input('Interpolate', True)  # Interpolate mtf data
leader = Arr(0, 0.0)
leaderz = Arr(0, 0.0)
macd = Arr(0, 0.0)
signal = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
countBuffer = Arr(0, 0.0)
timeFrame = 0
mtfHandle = 0
atrHandle = 0
calculating = False
work = Arr(0, 0.0, dims=(4,))

def OnInit():
    global calculating, mtfHandle, timeFrame
    SetIndexBuffer(0, leader, INDICATOR_DATA)
    SetIndexBuffer(1, leaderz, INDICATOR_DATA)
    SetIndexBuffer(2, macd, INDICATOR_DATA)
    SetIndexBuffer(3, colorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, signal, INDICATOR_DATA)
    SetIndexBuffer(5, countBuffer, INDICATOR_CALCULATIONS)
    timeFrame = MathMax(Period(), TimeFrame)
    calculating = timeFrame == Period()
    if not calculating:
        mtfHandle = iCustom(None, timeFrame, getIndicatorName(), PERIOD_CURRENT, FastEMAPeriod, SlowEMAPeriod, Price)
    IndicatorSetString(INDICATOR_SHORTNAME, getPeriodToString(timeFrame) + ' Leader of the MACD (' + _str(FastEMAPeriod) + ',' + _str(SlowEMAPeriod) + ',' + _str(SignalEMAPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if calculating:
        if ArrayRange(work, 0) < rates_total:
            ArrayResize(work, rates_total)
        fastAlpha = _fdiv(2.0, 1.0 + FastEMAPeriod)
        slowAlpha = _fdiv(2.0, 1.0 + SlowEMAPeriod)
        signalAlpha = _fdiv(2.0, 1.0 + SignalEMAPeriod)
        for i in range(MathMax(prev_calculated - 1, 0), rates_total):
            price = getPrice(Price, open, close, high, low, i)
            if i == 0:
                work[i][0] = price
                work[i][1] = price
                work[i][2] = price
                work[i][3] = price
                macd[i] = 0.0
                signal[i] = 0.0
                continue
            work[i][0] = work[i - 1][0] + (fastAlpha * (price - work[i - 1][0]))
            work[i][1] = work[i - 1][1] + (fastAlpha * (price - work[i][0] - work[i - 1][1]))
            work[i][2] = work[i - 1][2] + (slowAlpha * (price - work[i - 1][2]))
            work[i][3] = work[i - 1][3] + (slowAlpha * (price - work[i][2] - work[i - 1][3]))
            macd[i] = work[i][0] - work[i][2]
            leader[i] = work[i][1] - work[i][3] + macd[i]
            signal[i] = signal[i - 1] + (signalAlpha * (macd[i] - signal[i - 1]))
            leaderz[i] = 0.0
            colorBuffer[i] = colorBuffer[i - 1]
            if macd[i] > macd[i - 1]:
                colorBuffer[i] = 0.0
            if macd[i] < macd[i - 1]:
                colorBuffer[i] = 1.0
        countBuffer[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
        return rates_total
    if BarsCalculated(mtfHandle) <= 0:
        return 0
    times = Arr(0, 0)
    startTime = time[0] - PeriodSeconds(timeFrame)
    endTime = time[rates_total - 1]
    bars = CopyTime(None, timeFrame, _DT(startTime), _DT(endTime), times)
    if (times[0] > time[0] or bars < 1) or bars > rates_total:
        return rates_total
    tlead = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 0, 0, bars, tlead)
    tmacd = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 2, 0, bars, tmacd)
    tcolo = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 3, 0, bars, tcolo)
    tsign = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 4, 0, bars, tsign)
    count = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 5, 0, bars, count)
    maxb = _int(MathMax(MathMin(_fdiv(count[bars - 1] * PeriodSeconds(timeFrame), PeriodSeconds(Period())), rates_total - 1), 1))
    for i in range(MathMax(prev_calculated - maxb, 0), rates_total):
        d = dateArrayBsearch(times, time[i], bars)
        if d > -1 and d < bars:
            macd[i] = tmacd[d]
            signal[i] = tsign[d]
            leader[i] = tlead[d]
            colorBuffer[i] = tcolo[d]
        if not Interpolate:
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
                macd[i - k] = macd[i] + _fdiv((macd[i - n] - macd[i]) * float(k), n)
                signal[i - k] = signal[i] + _fdiv((signal[i - n] - signal[i]) * float(k), n)
                leader[i - k] = leader[i] + _fdiv((leader[i - n] - leader[i]) * float(k), n)
                k += 1
    return rates_total

def minValue(array, useValue, period, shift):
    minValue_ = array[shift][useValue]
    i = 1
    while i < period and (shift - i) >= 0:
        minValue_ = MathMin(minValue_, array[shift - i][useValue])
        i += 1
    return minValue_

def maxValue(array, useValue, period, shift):
    maxValue_ = array[shift][useValue]
    i = 1
    while i < period and (shift - i) >= 0:
        maxValue_ = MathMax(maxValue_, array[shift - i][useValue])
        i += 1
    return maxValue_

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
_s_getPeriodToString__per = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 0x4001, 0x4002, 0x4003, 0x4004, 0x4006, 0x4008, 0x400c, 0x4018, 0x8001, 0xc001], fill=0)
_s_getPeriodToString__tfs = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LeaderOfTheMacd(_MQL5Indicator):
    name = 'leader_of_the_macd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'FastEMAPeriod': 12,  # Fast EMA period
        'SlowEMAPeriod': 26,  # Slow EMA period
        'SignalEMAPeriod': 9,  # Signal EMA period
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price to use
        'Interpolate': True,  # Interpolate mtf data
    }

