"""one_more_average — converted from MQL5: MQL5 Indicators/One More Average/one_more_average.mq5

Copyright: Mladen; Link: http://www.forex-tsd.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Mladen', 'link': 'http://www.forex-tsd.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 36095, 3145645, 55295]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'One more average'}, 'levels': [], 'description': [], 'name': 'one_more_average', 'source': 'MQL5 Indicators/One More Average/one_more_average.mq5', 'folder': 'One More Average', 'inputs': [{'mql': 'inpLength', 'py': 'inpLength', 'param': 'inpLength', 'type': 'int', 'default': 26, 'label': 'Averaging period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'inpSpeed', 'py': 'inpSpeed', 'param': 'inpSpeed', 'type': 'float', 'default': 1.0, 'label': 'Speed', 'sinput': False}, {'mql': 'inpAdaptive', 'py': 'inpAdaptive', 'param': 'inpAdaptive', 'type': 'bool', 'default': True, 'label': 'Should it be adaptive?', 'sinput': False}, {'mql': '_1', 'py': '_1', 'param': None, 'type': 'string', 'default': '', 'label': 'Multi time frame settings', 'sinput': False}, {'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpInterpolated', 'py': 'inpInterpolated', 'param': 'inpInterpolated', 'type': 'bool', 'default': True, 'label': 'Interpolated multi time frame?', 'sinput': False}, {'mql': '_2', 'py': '_2', 'param': None, 'type': 'string', 'default': '', 'label': '.', 'sinput': False}, {'mql': 'inpCalculating', 'py': 'inpCalculating', 'param': 'inpCalculating', 'type': 'int', 'default': 0, 'label': 'Reserved for internal use', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
inpLength = _input('inpLength', 26)  # Averaging period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Applied price
inpSpeed = _input('inpSpeed', 1.0)  # Speed
inpAdaptive = _input('inpAdaptive', True)  # Should it be adaptive?
_1 = _input('_1', '')  # Multi time frame settings
inpTimeFrame = _input('inpTimeFrame', PERIOD_CURRENT)  # Time frame
inpInterpolated = _input('inpInterpolated', True)  # Interpolated multi time frame?
_2 = _input('_2', '')  # .
inpCalculating = _input('inpCalculating', 0)  # Reserved for internal use
OMABuffer = Arr(0, 0.0)
OMACalculated = Arr(0, 0.0)
clrBuffer = Arr(0, 0.0)
prcBuffer = Arr(0, 0.0)
stored = Arr(0, 0.0, dims=(7,))
iTimeFrame = 0
calculating = False
priceHandle = 0
omaHandle = 0
Length = 0
Speed = 0.0

def OnInit():
    global Length, Speed, calculating, iTimeFrame, omaHandle, priceHandle
    SetIndexBuffer(0, OMABuffer, INDICATOR_DATA)
    ArraySetAsSeries(OMABuffer, True)
    SetIndexBuffer(1, clrBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(clrBuffer, True)
    SetIndexBuffer(2, prcBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(prcBuffer, True)
    Length = (inpLength if (inpLength > 0) else 1)
    Speed = (inpSpeed if (inpSpeed > -1.5) else -1.5)
    if not (calculating := inpCalculating == 155522):
        iTimeFrame = ((inpTimeFrame if (inpTimeFrame > Period()) else Period()) if (inpTimeFrame != PERIOD_CURRENT) else Period())
        omaHandle = iCustom(None, iTimeFrame, getIndicatorName(), Length, inpPrice, Speed, inpAdaptive, '', iTimeFrame, inpInterpolated, '', 155522)
    else:
        priceHandle = iMA(None, inpTimeFrame, 1, 0, MODE_SMA, inpPrice)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not ArrayGetAsSeries(time):
        ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if prev_calculated > 0:
        limit += 1
    if prev_calculated == 0:
        last = 0
        if inpAdaptive:
            last = _int(round(Length * 2.5)) + 1
        else:
            last = Length
        limit -= last + 1
        for i in range(0, last + 1):
            clrBuffer[rates_total - i - 1] = 0.0
            OMABuffer[rates_total - i - 1] = 0.0
    if not calculating:
        timeArray = Arr(0, 0)
        ArraySetAsSeries(timeArray, True)
        copiedDates = 0
        for i in range(0, 5):
            if (copiedDates := CopyTime(Symbol(), iTimeFrame, _DT(time[rates_total - 1]), _DT(time[0]), timeArray)) > 0:
                break
        if copiedDates <= 0:
            Print('not all times copied. Will try on next tick')
            return rates_total
        if not checkCalculated(omaHandle, copiedDates, 'averages'):
            return rates_total
        if not doCopy(omaHandle, prcBuffer, 0, copiedDates, 'averages'):
            return rates_total
        minBars = _int(round(_idiv(periodToMinutes(iTimeFrame), periodToMinutes(Period())))) + 1
        limit = (limit if (limit > minBars) else minBars)
        for i in range(limit, 0 - 1, -1):
            d = dateArrayBsearch(timeArray, time[i], copiedDates)
            t = timeArray[d]
            OMABuffer[i] = prcBuffer[d]
            clrBuffer[i] = clrBuffer[i + 1]
            if OMABuffer[i] > OMABuffer[i + 1]:
                clrBuffer[i] = 0.0
            if OMABuffer[i] < OMABuffer[i + 1]:
                clrBuffer[i] = 1.0
            if iTimeFrame > Period() and d == 0:
                if OMABuffer[i] > OMABuffer[i + 1]:
                    clrBuffer[i] = 2.0
                if OMABuffer[i] < OMABuffer[i + 1]:
                    clrBuffer[i] = 3.0
            if inpInterpolated:
                if iTimeFrame <= Period() or (i > 0 and d == dateArrayBsearch(timeArray, time[i - 1], copiedDates)):
                    continue
                n = 1
                while (i + n) < Bars(Symbol(), 0) and time[i + n] >= t:
                    n += 1
                    continue
                    n += 1
                factor = _fdiv(1.0, n)
                for k in range(1, n):
                    OMABuffer[i + k] = (k * factor * OMABuffer[i + n]) + ((1.0 - (k * factor)) * OMABuffer[i])
        return rates_total
    if ArrayRange(stored, 0) != rates_total:
        ArrayResize(stored, rates_total)
    if not checkCalculated(priceHandle, rates_total, 'prices'):
        return prev_calculated
    if not doCopy(priceHandle, prcBuffer, 0, limit, 'prices'):
        return prev_calculated
    if prev_calculated == 0:
        ArrayInitialize(stored, 0)
    i = limit
    r = rates_total - limit - 1
    while i >= 0:
        OMABuffer[i] = iAverage(prcBuffer[i], Length, Speed, inpAdaptive, r)
        i -= 1
        r += 1
    return rates_total

def iAverage(price, averagePeriod, speed, adaptive, r):
    e1 = stored[r - 1][0]
    e2 = stored[r - 1][1]
    e3 = stored[r - 1][2]
    e4 = stored[r - 1][3]
    e5 = stored[r - 1][4]
    e6 = stored[r - 1][5]
    if adaptive and averagePeriod > 1:
        minPeriod = averagePeriod / 2.0
        maxPeriod = minPeriod * 5.0
        endPeriod = _int(MathCeil(maxPeriod))
        signal = MathAbs(price - stored[r - endPeriod][6])
        noise = 1e-11
        for k in range(1, endPeriod):
            noise = noise + MathAbs(price - stored[r - k][6])
        if noise != 0:
            averagePeriod = (_fdiv(signal, noise) * (maxPeriod - minPeriod)) + minPeriod
    alpha = _fdiv(2.0 + speed, 1.0 + speed + averagePeriod)
    e1 = e1 + (alpha * (price - e1))
    e2 = e2 + (alpha * (e1 - e2))
    v1 = (1.5 * e1) - (0.5 * e2)
    e3 = e3 + (alpha * (v1 - e3))
    e4 = e4 + (alpha * (e3 - e4))
    v2 = (1.5 * e3) - (0.5 * e4)
    e5 = e5 + (alpha * (v2 - e5))
    e6 = e6 + (alpha * (e5 - e6))
    v3 = (1.5 * e5) - (0.5 * e6)
    stored[r][0] = e1
    stored[r][1] = e2
    stored[r][2] = e3
    stored[r][3] = e4
    stored[r][4] = e5
    stored[r][5] = e6
    stored[r][6] = price
    return v3

def dateArrayBsearch(dates, toFind, total):
    mid = 0
    first = 0
    last = total - 1
    while last >= first:
        mid = (first + last) >> 1
        if toFind == dates[mid] or ((mid > 0 and toFind > dates[mid]) and toFind < dates[mid - 1]):
            break
        if toFind > dates[mid]:
            last = mid - 1
        else:
            first = mid + 1
    return mid

def periodToMinutes(period):
    i = 0
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    for i in range(i, 20):
        if period == _s_periodToMinutes__per[i]:
            break
    else:
        i = _range_end(i, 20, 1)
    return _s_periodToMinutes__min[i]

def checkCalculated(bufferHandle, total, checkDescription):
    calculated = BarsCalculated(bufferHandle)
    if calculated < total:
        Print('Not all data of ' + checkDescription + ' calculated (', _str(total - calculated), ' un-calculated bars )')
        return False
    return True

def doCopy(bufferHandle, buffer, buffNum, copyCount, copyDescription):
    if CopyBuffer(bufferHandle, buffNum, 0, copyCount, buffer) <= 0:
        Print('Getting ' + copyDescription + ' failed! Error', GetLastError())
        return False
    return True

def getIndicatorName():
    progPath = MQL5InfoString(MQL5_PROGRAM_PATH)
    toFind = 'MQL5\\Indicators\\'
    startLength = StringFind(progPath, toFind) + StringLen(toFind)
    indicatorName = StringSubstr(progPath, startLength)
    indicatorName = StringSubstr(indicatorName, 0, StringLen(indicatorName) - 4)
    return indicatorName

# ---- static local variables
_s_periodToMinutes__per = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 0x4001, 0x4002, 0x4003, 0x4004, 0x4006, 0x4008, 0x400c, 0x4018, 0x8001, 0xc001], fill=0)
_s_periodToMinutes__min = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60, 120, 180, 240, 360, 480, 720, 1440, 10080, 43200], fill=0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OneMoreAverage(_MQL5Indicator):
    name = 'one_more_average'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpLength': 26,  # Averaging period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'inpSpeed': 1.0,  # Speed
        'inpAdaptive': True,  # Should it be adaptive?
        'inpTimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'inpInterpolated': True,  # Interpolated multi time frame?
        'inpCalculating': 0,  # Reserved for internal use
    }

