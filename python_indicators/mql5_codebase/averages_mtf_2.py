"""averages_-_mtf_2 — converted from MQL5: MQL5 Indicators/Averages MTF V2/averages_-_mtf_2.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16760576, 9662683]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'averages_-_mtf_2', 'source': 'MQL5 Indicators/Averages MTF V2/averages_-_mtf_2.mq5', 'folder': 'Averages MTF V2', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Apply to', 'sinput': False}, {'mql': 'AveragePeriod', 'py': 'AveragePeriod', 'param': 'AveragePeriod', 'type': 'int', 'default': 14, 'label': 'Calculation period', 'sinput': False}, {'mql': 'AverageType', 'py': 'AverageType', 'param': 'AverageType', 'type': 'int', 'default': 0, 'label': 'Calculation type', 'sinput': False}, {'mql': 'Multicolor', 'py': 'Multicolor', 'param': 'Multicolor', 'type': 'bool', 'default': True, 'label': 'Multi color mode?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data ?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# enum enumAveragesType
avgSma = 0
avgEma = 1
avgDsema = 2
avgDema = 3
avgTema = 4
avgSmma = 5
avgLwma = 6
avgPwma = 7
avgAlex = 8
avgVwma = 9
avgHull = 10
avgTma = 11
avgSine = 12
avgLsma = 13
avgIe2 = 14
avgNlma = 15
avgZlma = 16
avgLead = 17
_enum('enumAveragesType', {0: 'avgSma', 1: 'avgEma', 2: 'avgDsema', 3: 'avgDema', 4: 'avgTema', 5: 'avgSmma', 6: 'avgLwma', 7: 'avgPwma', 8: 'avgAlex', 9: 'avgVwma', 10: 'avgHull', 11: 'avgTma', 12: 'avgSine', 13: 'avgLsma', 14: 'avgIe2', 15: 'avgNlma', 16: 'avgZlma', 17: 'avgLead'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
Price = _input('Price', PRICE_CLOSE)  # Apply to
AveragePeriod = _input('AveragePeriod', 14)  # Calculation period
AverageType = _input('AverageType', 0)  # Calculation type
Multicolor = _input('Multicolor', True)  # Multi color mode?
Interpolate = _input('Interpolate', True)  # Interpolate mtf data ?
MaBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
CountBuffer = Arr(0, 0.0)
gAverageType = 0
timeFrame = 0
mtfHandle = 0
calculating = False
totalBars = 0
methodNames = Arr.of(['SMA', 'EMA', 'Double smoothed EMA', 'Double EMA', 'Tripple EMA', 'Smoothed MA', 'Linear weighted MA', 'Parabolic weighted MA', 'Alexander MA', 'Volume weghted MA', 'Hull MA', 'Triangular MA', 'Sine weighted MA', 'Linear regression', 'IE/2', 'NonLag MA', 'Zero lag EMA', 'Leader EMA'], fill="")
workSma = Arr(0, 0.0, dims=(2,))
workEma = Arr(0, 0.0, dims=(1,))
workDsema = Arr(0, 0.0, dims=(2,))
workDema = Arr(0, 0.0, dims=(2,))
workTema = Arr(0, 0.0, dims=(3,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))
workLwmp = Arr(0, 0.0, dims=(1,))
workAlex = Arr(0, 0.0, dims=(1,))
workTma = Arr(0, 0.0, dims=(1,))
workSineWMA = Arr(0, 0.0, dims=(1,))
workWwma = Arr(0, 0.0, dims=(1,))
workHull = Arr(0, 0.0, dims=(2,))
workLinr = Arr(0, 0.0, dims=(1,))
workIe2 = Arr(0, 0.0, dims=(1,))
workLeader = Arr(0, 0.0, dims=(2,))
workZl = Arr(0, 0.0, dims=(2,))
nlm_values = Arr(3, 0.0, dyn=False, dims=(1,))
nlm_prices = Arr(0, 0.0, dims=(1,))
nlm_alphas = Arr(0, 0.0, dims=(1,))

def OnInit():
    global calculating, gAverageType, mtfHandle, timeFrame
    SetIndexBuffer(0, MaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, CountBuffer, INDICATOR_CALCULATIONS)
    gAverageType = AverageType
    timeFrame = MathMax(Period(), TimeFrame)
    calculating = timeFrame == Period()
    if not calculating:
        name = getIndicatorName()
        mtfHandle = iCustom(None, timeFrame, name, PERIOD_CURRENT, Price, AveragePeriod, AverageType, Multicolor)
    PlotIndexSetString(0, PLOT_LABEL, getAverageName(AverageType) + ' (' + _str(AveragePeriod) + ')')
    IndicatorSetString(INDICATOR_SHORTNAME, getAverageName(gAverageType) + ' (' + _str(AveragePeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global totalBars
    if calculating:
        totalBars = rates_total
        for i in range(MathMax(prev_calculated - 1, 1), rates_total):
            price = getPrice(Price, rates_total - i - 1)
            MaBuffer[i] = iCustomMa(AverageType, price, AveragePeriod, TickVolume, i)
            if Multicolor and i > 0:
                ColorBuffer[i] = ColorBuffer[i - 1]
                if MaBuffer[i] > MaBuffer[i - 1]:
                    ColorBuffer[i] = 0.0
                if MaBuffer[i] < MaBuffer[i - 1]:
                    ColorBuffer[i] = 1.0
            else:
                ColorBuffer[i] = 0.0
        CountBuffer[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
        return rates_total
    times = Arr(0, 0)
    startTime = Time[0] - PeriodSeconds(timeFrame)
    endTime = Time[rates_total - 1]
    bars = CopyTime(None, timeFrame, _DT(startTime), _DT(endTime), times)
    if times[0] > Time[0] or bars < 1:
        return prev_calculated
    values = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 0, 0, bars, values)
    colors = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 1, 0, bars, colors)
    counts = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 2, 0, bars, counts)
    maxb = _int(MathMax(MathMin(_fdiv(counts[bars - 1] * PeriodSeconds(timeFrame), PeriodSeconds(Period())), rates_total - 1), 1))
    for i in range(MathMax(prev_calculated - maxb, 0), rates_total):
        d = dateArrayBsearch(times, Time[i], bars)
        if d > -1 and d < bars:
            MaBuffer[i] = values[d]
            ColorBuffer[i] = colors[d]
        if not Interpolate:
            continue
        l = MathMin(i + 1, rates_total - 1)
        if d != dateArrayBsearch(times, Time[l], bars) or i == l:
            n = 0
            k = 0
            n = 1
            while (i - n) > 0 and Time[i - n] >= times[d]:
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                MaBuffer[i - k] = MaBuffer[i] + _fdiv((MaBuffer[i - n] - MaBuffer[i]) * k, n)
                k += 1
    return rates_total

def getPrice(price, position):
    _rates = Arr(0, 0, factory=MqlRates)
    copyCount = CopyRates(Symbol(), Period(), position, 1, _rates)
    if copyCount == 1:
        _sw1 = price
        if _sw1 == PRICE_CLOSE:
            return _rates[0].close
        elif _sw1 == PRICE_HIGH:
            return _rates[0].high
        elif _sw1 == PRICE_LOW:
            return _rates[0].low
        elif _sw1 == PRICE_OPEN:
            return _rates[0].open
        elif _sw1 == PRICE_MEDIAN:
            return (_rates[0].high + _rates[0].low) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            return (_rates[0].high + _rates[0].low + _rates[0].close) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            return (_rates[0].high + _rates[0].low + _rates[0].close + _rates[0].close) / 4.0
        else:
            return 0.0
    return 0.0

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

def getIndicatorName():
    progPath = MQL5InfoString(MQL5_PROGRAM_PATH)
    terminalPath = TerminalInfoString(TERMINAL_PATH)
    startLength = StringLen(terminalPath) + 17
    progLength = StringLen(progPath)
    indicatorName = StringSubstr(progPath, startLength)
    indicatorName = StringSubstr(indicatorName, 0, StringLen(indicatorName) - 4)
    return indicatorName

def getAverageName(method):
    max_ = ArraySize(methodNames) - 1
    method = MathMax(MathMin(method, max_), 0)
    return methodNames[method]

def iCustomMa(mode, price, length, Volume, r, instanceNo=0):
    _sw2 = mode
    if _sw2 == avgSma:
        return iSma(price, _int(length), r, instanceNo)
    elif _sw2 == avgEma:
        return iEma(price, length, r, instanceNo)
    elif _sw2 == avgDsema:
        return iDsema(price, length, r, instanceNo)
    elif _sw2 == avgDema:
        return iDema(price, length, r, instanceNo)
    elif _sw2 == avgTema:
        return iTema(price, length, r, instanceNo)
    elif _sw2 == avgSmma:
        return iSmma(price, length, r, instanceNo)
    elif _sw2 == avgLwma:
        return iLwma(price, length, r, instanceNo)
    elif _sw2 == avgPwma:
        return iLwmp(price, length, r, instanceNo)
    elif _sw2 == avgAlex:
        return iAlex(price, length, r, instanceNo)
    elif _sw2 == avgVwma:
        return iWwma(price, length, Volume, r, instanceNo)
    elif _sw2 == avgHull:
        return iHull(price, length, r, instanceNo)
    elif _sw2 == avgTma:
        return iTma(price, length, r, instanceNo)
    elif _sw2 == avgSine:
        return iSineWMA(price, _int(length), r, instanceNo)
    elif _sw2 == avgLsma:
        return iLinr(price, length, r, instanceNo)
    elif _sw2 == avgIe2:
        return iIe2(price, length, r, instanceNo)
    elif _sw2 == avgNlma:
        return iNonLagMa(price, length, r, instanceNo)
    elif _sw2 == avgZlma:
        return iZeroLag(price, length, r, instanceNo)
    elif _sw2 == avgLead:
        return iLeader(price, length, r, instanceNo)
    else:
        return price

def iSma(price, period, r, instanceNo=0):
    if ArrayRange(workSma, 0) != totalBars:
        ArrayResize(workSma, totalBars)
    instanceNo *= 2
    k = 0
    workSma[r][instanceNo] = price
    if r >= period:
        workSma[r][instanceNo + 1] = workSma[r - 1][instanceNo + 1] + _fdiv(workSma[r][instanceNo] - workSma[r - period][instanceNo], period)
    else:
        workSma[r][instanceNo + 1] = 0.0
        k = 0
        while k < period and (r - k) >= 0:
            workSma[r][instanceNo + 1] += workSma[r - k][instanceNo]
            k += 1
        workSma[r][instanceNo + 1] = _fdiv(workSma[r][instanceNo + 1], k)
    return workSma[r][instanceNo + 1]

def iEma(price, period, r, instanceNo=0):
    if ArrayRange(workEma, 0) != totalBars:
        ArrayResize(workEma, totalBars)
    alpha = _fdiv(2.0, 1.0 + period)
    workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iDsema(price, period, r, instanceNo=0):
    if ArrayRange(workDsema, 0) != totalBars:
        ArrayResize(workDsema, totalBars)
    instanceNo *= 2
    alpha = _fdiv(2.0, 1.0 + MathSqrt(period))
    workDsema[r][0 + instanceNo] = workDsema[r - 1][0 + instanceNo] + (alpha * (price - workDsema[r - 1][0 + instanceNo]))
    workDsema[r][1 + instanceNo] = workDsema[r - 1][1 + instanceNo] + (alpha * (workDsema[r][0 + instanceNo] - workDsema[r - 1][1 + instanceNo]))
    return workDsema[r][1 + instanceNo]

def iDema(price, period, r, instanceNo=0):
    if ArrayRange(workDema, 0) != totalBars:
        ArrayResize(workDema, totalBars)
    instanceNo *= 2
    alpha = _fdiv(2.0, 1.0 + period)
    workDema[r][0 + instanceNo] = workDema[r - 1][0 + instanceNo] + (alpha * (price - workDema[r - 1][0 + instanceNo]))
    workDema[r][1 + instanceNo] = workDema[r - 1][1 + instanceNo] + (alpha * (workDema[r][0 + instanceNo] - workDema[r - 1][1 + instanceNo]))
    return (workDema[r][0 + instanceNo] * 2.0) - workDema[r][1 + instanceNo]

def iTema(price, period, r, instanceNo=0):
    if ArrayRange(workTema, 0) != totalBars:
        ArrayResize(workTema, totalBars)
    instanceNo *= 3
    alpha = _fdiv(2.0, 1.0 + period)
    workTema[r][0 + instanceNo] = workTema[r - 1][0 + instanceNo] + (alpha * (price - workTema[r - 1][0 + instanceNo]))
    workTema[r][1 + instanceNo] = workTema[r - 1][1 + instanceNo] + (alpha * (workTema[r][0 + instanceNo] - workTema[r - 1][1 + instanceNo]))
    workTema[r][2 + instanceNo] = workTema[r - 1][2 + instanceNo] + (alpha * (workTema[r][1 + instanceNo] - workTema[r - 1][2 + instanceNo]))
    return workTema[r][2 + instanceNo] + (3.0 * (workTema[r][0 + instanceNo] - workTema[r][1 + instanceNo]))

def iSmma(price, period, r, instanceNo=0):
    if ArrayRange(workSmma, 0) != totalBars:
        ArrayResize(workSmma, totalBars)
    if r < period:
        workSmma[r][instanceNo] = price
    else:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, instanceNo=0):
    if ArrayRange(workLwma, 0) != totalBars:
        ArrayResize(workLwma, totalBars)
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

def iLwmp(price, period, r, instanceNo=0):
    if ArrayRange(workLwmp, 0) != totalBars:
        ArrayResize(workLwmp, totalBars)
    workLwmp[r][instanceNo] = price
    sumw = period * period
    sum_ = sumw * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = (period - k) * (period - k)
        sumw += weight
        sum_ += weight * workLwmp[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

def iAlex(price, period, r, instanceNo=0):
    if ArrayRange(workAlex, 0) != totalBars:
        ArrayResize(workAlex, totalBars)
    if period < 4:
        return price
    workAlex[r][instanceNo] = price
    sumw = period - 2
    sum_ = sumw * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k - 2
        sumw += weight
        sum_ += weight * workAlex[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

def iTma(price, period, r, instanceNo=0):
    if ArrayRange(workTma, 0) != totalBars:
        ArrayResize(workTma, totalBars)
    workTma[r][instanceNo] = price
    half = (period + 1.0) / 2.0
    sum_ = price
    sumw = 1.0
    k = 1
    while k < period and (r - k) >= 0:
        weight = k + 1
        if weight > half:
            weight = period - k
        sumw += weight
        sum_ += weight * workTma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

def iSineWMA(price, period, r, instanceNo=0):
    if period < 1:
        return price
    if ArrayRange(workSineWMA, 0) != totalBars:
        ArrayResize(workSineWMA, totalBars)
    workSineWMA[r][instanceNo] = price
    sum_ = 0.0
    sumw = 0.0
    k = 0
    while k < period and (r - k) >= 0:
        weight = MathSin(_fdiv(3.141592653589793 * (k + 1.0), period + 1.0))
        sumw += weight
        sum_ += weight * workSineWMA[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

def iWwma(price, period, Volume, r, instanceNo=0):
    if ArrayRange(workWwma, 0) != totalBars:
        ArrayResize(workWwma, totalBars)
    workWwma[r][instanceNo] = price
    sumw = float(Volume[r])
    sum_ = sumw * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = float(Volume[r - k])
        sumw += weight
        sum_ += weight * workWwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

def iHull(price, period, r, instanceNo=0):
    if ArrayRange(workHull, 0) != totalBars:
        ArrayResize(workHull, totalBars)
    k = 0
    HmaPeriod = _int(MathMax(period, 2))
    HalfPeriod = _int(MathFloor(_idiv(HmaPeriod, 2)))
    HullPeriod = _int(MathFloor(MathSqrt(HmaPeriod)))
    hma = 0.0
    hmw = 0.0
    weight = 0.0
    instanceNo *= 2
    workHull[r][instanceNo] = price
    hmw = HalfPeriod
    hma = hmw * price
    k = 1
    while k < HalfPeriod and (r - k) >= 0:
        weight = HalfPeriod - k
        hmw += weight
        hma += weight * workHull[r - k][instanceNo]
        k += 1
    workHull[r][instanceNo + 1] = _fdiv(2.0 * hma, hmw)
    hmw = HmaPeriod
    hma = hmw * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = HmaPeriod - k
        hmw += weight
        hma += weight * workHull[r - k][instanceNo]
        k += 1
    workHull[r][instanceNo + 1] -= _fdiv(hma, hmw)
    hmw = HullPeriod
    hma = hmw * workHull[r][instanceNo + 1]
    k = 1
    while k < HullPeriod and (r - k) >= 0:
        weight = HullPeriod - k
        hmw += weight
        hma += weight * workHull[r - k][1 + instanceNo]
        k += 1
    return _fdiv(hma, hmw)

def iLinr(price, period, r, instanceNo=0):
    if ArrayRange(workLinr, 0) != totalBars:
        ArrayResize(workLinr, totalBars)
    period = MathMax(period, 1)
    workLinr[r][instanceNo] = price
    lwmw = period
    lwma = lwmw * price
    sma = price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        lwmw += weight
        lwma += weight * workLinr[r - k][instanceNo]
        sma += workLinr[r - k][instanceNo]
        k += 1
    return _fdiv(3.0 * lwma, lwmw) - _fdiv(2.0 * sma, period)

def iIe2(price, period, r, instanceNo=0):
    if ArrayRange(workIe2, 0) != totalBars:
        ArrayResize(workIe2, totalBars)
    period = MathMax(period, 1)
    workIe2[r][instanceNo] = price
    sumx = 0.0
    sumxx = 0.0
    sumxy = 0.0
    sumy = 0.0
    k = 0
    while k < period and (r - k) >= 0:
        price = workIe2[r - k][instanceNo]
        sumx += k
        sumxx += k * k
        sumxy += k * price
        sumy += price
        k += 1
    slope = _fdiv((period * sumxy) - (sumx * sumy), (sumx * sumx) - (period * sumxx))
    average = _fdiv(sumy, period)
    return (average + slope + _fdiv(sumy + (slope * sumx), period)) / 2.0

def iLeader(price, period, r, instanceNo=0):
    if ArrayRange(workLeader, 0) != totalBars:
        ArrayResize(workLeader, totalBars)
    instanceNo *= 2
    period = MathMax(period, 1)
    alpha = _fdiv(2.0, period + 1.0)
    workLeader[r][instanceNo] = workLeader[r - 1][instanceNo] + (alpha * (price - workLeader[r - 1][instanceNo]))
    workLeader[r][instanceNo + 1] = workLeader[r - 1][instanceNo + 1] + (alpha * (price - workLeader[r][instanceNo] - workLeader[r - 1][instanceNo + 1]))
    return workLeader[r][instanceNo] + workLeader[r][instanceNo + 1]

def iZeroLag(price, length, r, instanceNo=0):
    if ArrayRange(workZl, 0) != totalBars:
        ArrayResize(workZl, totalBars)
    instanceNo *= 2
    alpha = _fdiv(2.0, 1.0 + length)
    per = _int((length - 1.0) / 2.0)
    workZl[r][0 + instanceNo] = price
    if r < per:
        workZl[r][1 + instanceNo] = price
    else:
        workZl[r][1 + instanceNo] = workZl[r - 1][1 + instanceNo] + (alpha * ((2.0 * price) - workZl[r - per][0 + instanceNo] - workZl[r - 1][1 + instanceNo]))
    return workZl[r][1 + instanceNo]

def iNonLagMa(price, length, r, instanceNo=0):
    if ArrayRange(nlm_prices, 0) != totalBars:
        ArrayResize(nlm_prices, totalBars)
    nlm_prices[r][instanceNo] = price
    if length < 3 or r < 3:
        return nlm_prices[r][instanceNo]
    k = 0
    if nlm_values[0][instanceNo] != length:
        Cycle = 4.0
        Coeff = 3.0 * 3.141592653589793
        Phase = _int(length - 1)
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AveragesMtf2(_MQL5Indicator):
    name = 'averages_-_mtf_2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Apply to
        'AveragePeriod': 14,  # Calculation period
        'AverageType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Double smoothed EMA', 3: 'Double EMA', 4: 'Tripple EMA', 5: 'Smoothed MA', 6: 'Linear weighted MA', 7: 'Parabolic weighted MA', 8: 'Alexander MA', 9: 'Volume weighted MA', 10: 'Hull MA', 11: 'Triangular MA', 12: 'Sine weighted MA', 13: 'Linear regression value', 14: 'IE/2', 15: 'Non lag MA', 16: 'Zeo lag EMA', 17: 'Leader EMA'}, default=0),  # Calculation type
        'Multicolor': True,  # Multi color mode?
        'Interpolate': True,  # Interpolate mtf data ?
    }

