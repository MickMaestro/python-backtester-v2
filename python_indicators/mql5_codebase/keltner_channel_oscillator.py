"""keltner_channel_oscillator — converted from MQL5: MQL5 Indicators/Keltner Channel Oscillator/keltner_channel_oscillator.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 1}, 'colors': {1: [14546909, 14804223], 2: [14546909], 3: [14804223], 4: [6908265]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {4: 0}, 'labels': {1: 'Break values', 2: 'Upper band', 3: 'Lower band', 4: 'Price'}, 'levels': [], 'description': [], 'name': 'keltner_channel_oscillator', 'source': 'MQL5 Indicators/Keltner Channel Oscillator/keltner_channel_oscillator.mq5', 'folder': 'Keltner Channel Oscillator', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 20, 'label': 'Moving average period', 'sinput': False}, {'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 0, 'label': 'Moving average type', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 5, 'label': 'Moving average price', 'sinput': False}, {'mql': 'AtrPeriod', 'py': 'AtrPeriod', 'param': 'AtrPeriod', 'type': 'int', 'default': 20, 'label': 'Range period', 'sinput': False}, {'mql': 'AtrMultiplier', 'py': 'AtrMultiplier', 'param': 'AtrMultiplier', 'type': 'double', 'default': 2.0, 'label': 'Range multiplier', 'sinput': False}, {'mql': 'AtrMode', 'py': 'AtrMode', 'param': 'AtrMode', 'type': 'int', 'default': 0, 'label': 'Range calculating mode', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enMaModes
ma_Simple = 0
ma_Expo = 1
_enum('enMaModes', {0: 'ma_Simple', 1: 'ma_Expo'})

# enum enAtrMode
atr_Rng = 0
atr_Atr = 1
_enum('enAtrMode', {0: 'atr_Rng', 1: 'atr_Atr'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
MAPeriod = _input('MAPeriod', 20)  # Moving average period
MAMethod = _input('MAMethod', ma_Simple)  # Moving average type
Price = _input('Price', pr_typical)  # Moving average price
AtrPeriod = _input('AtrPeriod', 20)  # Range period
AtrMultiplier = _input('AtrMultiplier', 2.0)  # Range multiplier
AtrMode = _input('AtrMode', atr_Rng)  # Range calculating mode
Interpolate = _input('Interpolate', True)  # Interpolate mtf data
oscu = Arr(0, 0.0)
oscd = Arr(0, 0.0)
channelUp = Arr(0, 0.0)
channelDn = Arr(0, 0.0)
price = Arr(0, 0.0)
countBuffer = Arr(0, 0.0)
timeFrame = 0
mtfHandle = 0
atrHandle = 0
calculating = False
workHa = Arr(0, 0.0, dims=(4,))
workSma = Arr(0, 0.0, dims=(2,))
workEma = Arr(0, 0.0, dims=(1,))

def OnInit():
    global calculating, mtfHandle, timeFrame
    SetIndexBuffer(0, oscu, INDICATOR_DATA)
    SetIndexBuffer(1, oscd, INDICATOR_DATA)
    SetIndexBuffer(2, channelUp, INDICATOR_DATA)
    SetIndexBuffer(3, channelDn, INDICATOR_DATA)
    SetIndexBuffer(4, price, INDICATOR_DATA)
    SetIndexBuffer(5, countBuffer, INDICATOR_CALCULATIONS)
    timeFrame = MathMax(Period(), TimeFrame)
    calculating = timeFrame == Period()
    if not calculating:
        mtfHandle = iCustom(None, timeFrame, getIndicatorName(), PERIOD_CURRENT, MAPeriod, MAMethod, Price, AtrPeriod, AtrMultiplier, AtrMode)
    IndicatorSetString(INDICATOR_SHORTNAME, getPeriodToString(timeFrame) + ' Keltner channel (' + _str(MAPeriod) + ',' + _str(AtrPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if calculating:
        for i in range(MathMax(prev_calculated - 1, 1), rates_total):
            atr = 0.0
            k = 0
            while k < AtrPeriod and (i - k - 1) >= 0:
                if AtrMode == atr_Atr:
                    atr += MathMax(high[i - k], close[i - k - 1]) - MathMin(low[i - k], close[i - k - 1])
                else:
                    atr += high[i - k] - low[i - k]
                k += 1
            atr = atr / AtrPeriod
            tprice = getPrice(Price, open, close, high, low, i, rates_total)
            ma = 0.0
            _sw1 = MAMethod
            if _sw1 == ma_Simple:
                ma = iSma(tprice, MAPeriod, i, rates_total)
            elif _sw1 == ma_Expo:
                ma = iEma(tprice, MAPeriod, i, rates_total)
            price[i] = tprice - ma
            channelUp[i] = atr * AtrMultiplier
            channelDn[i] = (-atr) * AtrMultiplier
            oscu[i] = 0.0
            oscd[i] = 0.0
            if price[i] > channelUp[i]:
                oscu[i] = channelUp[i]
            if price[i] < channelDn[i]:
                oscu[i] = channelDn[i]
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
    toscu = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 0, 0, bars, toscu)
    tchnu = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 2, 0, bars, tchnu)
    tchnd = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 3, 0, bars, tchnd)
    tpric = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 4, 0, bars, tpric)
    count = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 5, 0, bars, count)
    maxb = _int(MathMax(MathMin(_fdiv(count[bars - 1] * PeriodSeconds(timeFrame), PeriodSeconds(Period())), rates_total - 1), 1))
    for i in range(MathMax(prev_calculated - maxb, 0), rates_total):
        d = dateArrayBsearch(times, time[i], bars)
        if d > -1 and d < bars:
            oscd[i] = 0.0
            oscu[i] = toscu[d]
            price[i] = tpric[d]
            channelUp[i] = tchnu[d]
            channelDn[i] = tchnd[d]
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
                price[i - k] = price[i] + _fdiv((price[i - n] - price[i]) * float(k), n)
                channelUp[i - k] = channelUp[i] + _fdiv((channelUp[i - n] - channelUp[i]) * float(k), n)
                channelDn[i - k] = channelDn[i] + _fdiv((channelDn[i - n] - channelDn[i]) * float(k), n)
                if oscu[i - k] != 0:
                    if oscu[i - k] > 0:
                        oscu[i - k] = channelUp[i - k]
                    if oscu[i - k] < 0:
                        oscu[i - k] = channelDn[i - k]
                k += 1
    return rates_total

def getPrice(pricet, open, close, high, low, i, bars):
    if pricet >= pr_haclose and pricet <= pr_haaverage:
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
        _sw2 = pricet
        if _sw2 == pr_haclose:
            return haClose
        elif _sw2 == pr_haopen:
            return haOpen
        elif _sw2 == pr_hahigh:
            return haHigh
        elif _sw2 == pr_halow:
            return haLow
        elif _sw2 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw2 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw2 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw2 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
    _sw3 = pricet
    if _sw3 == pr_close:
        return close[i]
    elif _sw3 == pr_open:
        return open[i]
    elif _sw3 == pr_high:
        return high[i]
    elif _sw3 == pr_low:
        return low[i]
    elif _sw3 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw3 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw3 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

def iSma(tprice, period, r, bars, instanceNo=0):
    if ArrayRange(workSma, 0) != bars:
        ArrayResize(workSma, bars)
    instanceNo *= 2
    workSma[r][instanceNo] = tprice
    if r >= period:
        workSma[r][instanceNo + 1] = workSma[r - 1][instanceNo + 1] + _fdiv(workSma[r][instanceNo] - workSma[r - period][instanceNo], period)
    else:
        workSma[r][instanceNo + 1] = 0.0
        k = 0
        while k < period and (r - k) >= 0:
            workSma[r][instanceNo + 1] += workSma[r - k][instanceNo]
            k += 1
        workSma[r][instanceNo + 1] = _fdiv(workSma[r][instanceNo + 1], float(period))
    return workSma[r][instanceNo + 1]

def iEma(tprice, period, r, bars, instanceNo=0):
    if ArraySize(workEma) != bars:
        ArrayResize(workEma, bars)
    alpha = _fdiv(2.0, 1.0 + period)
    workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (tprice - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

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


class KeltnerChannelOscillator(_MQL5Indicator):
    name = 'keltner_channel_oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'MAPeriod': 20,  # Moving average period
        'MAMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average'}, default=0),  # Moving average type
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Heiken ashi close', 8: 'Heiken ashi open', 9: 'Heiken ashi high', 10: 'Heiken ashi low', 11: 'Heiken ashi median', 12: 'Heiken ashi typical', 13: 'Heiken ashi weighted', 14: 'Heiken ashi average'}, default=5),  # Moving average price
        'AtrPeriod': 20,  # Range period
        'AtrMultiplier': 2.0,  # Range multiplier
        'AtrMode': _Choice({0: 'Calculate using range', 1: 'Calculate using ATR'}, default=0),  # Range calculating mode
        'Interpolate': True,  # Interpolate mtf data
    }

