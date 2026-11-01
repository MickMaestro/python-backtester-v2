"""absolute_strength_-_averages — converted from MQL5: MQL5 Indicators/Absolute Strength Averages/absolute_strength_-_averages.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [3329330], 2: [42495], 3: [3329330], 4: [42495]}, 'widths': {1: 2, 2: 2}, 'styles': {3: 2, 4: 2}, 'labels': {1: 'Smooth bulls', 2: 'Smooth bears', 3: 'Signal bulls', 4: 'Signal bears'}, 'levels': [], 'description': [], 'name': 'absolute_strength_-_averages', 'source': 'MQL5 Indicators/Absolute Strength Averages/absolute_strength_-_averages.mq5', 'folder': 'Absolute Strength Averages', 'inputs': [{'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 0, 'label': 'Calculation method', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 14, 'label': 'Calculation length', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'int', 'default': 5, 'label': 'Smoothing length', 'sinput': False}, {'mql': 'Signal', 'py': 'Signal', 'param': 'Signal', 'type': 'int', 'default': 5, 'label': 'Signal smoothing length', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'AvgMethod', 'py': 'AvgMethod', 'param': 'AvgMethod', 'type': 'int', 'default': 5, 'label': 'Averaging method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_AS_MODE
RSI_method = 0
Stochastic_method = 1
_enum('ENUM_AS_MODE', {0: 'RSI_method', 1: 'Stochastic_method'})

# enum enAverages
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
_enum('enAverages', {0: 'avgSma', 1: 'avgEma', 2: 'avgDsema', 3: 'avgDema', 4: 'avgTema', 5: 'avgSmma', 6: 'avgLwma', 7: 'avgPwma', 8: 'avgAlex', 9: 'avgVwma', 10: 'avgHull', 11: 'avgTma', 12: 'avgSine', 13: 'avgLsma', 14: 'avgIe2', 15: 'avgNlma', 16: 'avgZlma', 17: 'avgLead'})

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_average = 7
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average'})

# ---- inputs and global variables
Mode = _input('Mode', RSI_method)  # Calculation method
Length = _input('Length', 14)  # Calculation length
Smooth = _input('Smooth', 5)  # Smoothing length
Signal = _input('Signal', 5)  # Signal smoothing length
Price = _input('Price', pr_close)  # Price
AvgMethod = _input('AvgMethod', avgSmma)  # Averaging method
SmthBulls = Arr(0, 0.0)
SmthBears = Arr(0, 0.0)
SigBulls = Arr(0, 0.0)
SigBears = Arr(0, 0.0)
totalBars = 0
methodNames = Arr.of(['SMA', 'EMA', 'Double smoothed EMA', 'Double EMA', 'Tripple EMA', 'Smoothed MA', 'Linear weighted MA', 'Parabolic weighted MA', 'Alexander MA', 'Volume weghted MA', 'Hull MA', 'Triangular MA', 'Sine weighted MA', 'Linear regression', 'IE/2', 'NonLag MA', 'Zero lag EMA', 'Leader EMA'], fill="")
workSma = Arr(0, 0.0, dims=(12,))
workEma = Arr(0, 0.0, dims=(6,))
workDsema = Arr(0, 0.0, dims=(12,))
workDema = Arr(0, 0.0, dims=(12,))
workTema = Arr(0, 0.0, dims=(18,))
workSmma = Arr(0, 0.0, dims=(6,))
workLwma = Arr(0, 0.0, dims=(6,))
workLwmp = Arr(0, 0.0, dims=(6,))
workAlex = Arr(0, 0.0, dims=(6,))
workTma = Arr(0, 0.0, dims=(6,))
workSineWMA = Arr(0, 0.0, dims=(6,))
workWwma = Arr(0, 0.0, dims=(6,))
workHull = Arr(0, 0.0, dims=(12,))
workLinr = Arr(0, 0.0, dims=(6,))
workIe2 = Arr(0, 0.0, dims=(6,))
workLeader = Arr(0, 0.0, dims=(12,))
workZl = Arr(0, 0.0, dims=(12,))
nlm_values = Arr(3, 0.0, dyn=False, dims=(6,))
nlm_prices = Arr(0, 0.0, dims=(6,))
nlm_alphas = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, SmthBulls, INDICATOR_DATA)
    SetIndexBuffer(1, SmthBears, INDICATOR_DATA)
    SetIndexBuffer(2, SigBulls, INDICATOR_DATA)
    SetIndexBuffer(3, SigBears, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, getAverageName(AvgMethod) + ' Absolute strength (' + _str(Mode) + ',' + _str(Length) + ',' + _str(Smooth) + ',' + _str(Signal) + ',' + _str(Price) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global totalBars
    totalBars = rates_total
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        Price1 = getPrice(Price, open, close, high, low, rates_total, i)
        Price2 = getPrice(Price, open, close, high, low, rates_total, i - 1)
        Bulls = 0.0
        Bears = 0.0
        if Mode == RSI_method:
            Bulls = 0.5 * (MathAbs(Price1 - Price2) + (Price1 - Price2))
            Bears = 0.5 * (MathAbs(Price1 - Price2) - (Price1 - Price2))
        else:
            smax = high[i]
            k = 1
            while k < Length and (i - k) >= 0:
                smax = MathMax(smax, high[i - k])
                k += 1
            smin = low[i]
            k = 1
            while k < Length and (i - k) >= 0:
                smin = MathMin(smin, low[i - k])
                k += 1
            Bulls = Price1 - smin
            Bears = smax - Price1
        AvgBulls = iCustomMa(Bulls, Length, AvgMethod, tick_volume, i, 0)
        AvgBears = iCustomMa(Bears, Length, AvgMethod, tick_volume, i, 1)
        SmthBulls[i] = iCustomMa(AvgBulls, Smooth, AvgMethod, tick_volume, i, 2)
        SmthBears[i] = iCustomMa(AvgBears, Smooth, AvgMethod, tick_volume, i, 3)
        SigBulls[i] = iCustomMa(SmthBulls[i], Signal, AvgMethod, tick_volume, i, 4)
        SigBears[i] = iCustomMa(SmthBears[i], Signal, AvgMethod, tick_volume, i, 5)
    return rates_total

def getPrice(price, open, close, high, low, bars, i):
    _sw1 = price
    if _sw1 == pr_close:
        return close[i]
    elif _sw1 == pr_open:
        return open[i]
    elif _sw1 == pr_high:
        return high[i]
    elif _sw1 == pr_low:
        return low[i]
    elif _sw1 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw1 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    return 0.0

def getAverageName(method):
    max_ = ArraySize(methodNames) - 1
    method = MathMax(MathMin(method, max_), 0)
    return methodNames[method]

def iCustomMa(price, length, mode, Volume, r, instanceNo=0):
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


class AbsoluteStrengthAverages(_MQL5Indicator):
    name = 'absolute_strength_-_averages'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Mode': _Choice({0: 'Calculate absolute strength using RSI method', 1: 'Calculate absolute strength using Stochastic method'}, default=0),  # Calculation method
        'Length': 14,  # Calculation length
        'Smooth': 5,  # Smoothing length
        'Signal': 5,  # Signal smoothing length
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4'}, default=0),  # Price
        'AvgMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Double smoothed EMA', 3: 'Double EMA', 4: 'Tripple EMA', 5: 'Smoothed MA', 6: 'Linear weighted MA', 7: 'Parabolic weighted MA', 8: 'Alexander MA', 9: 'Volume weighted MA', 10: 'Hull MA', 11: 'Triangular MA', 12: 'Sine weighted MA', 13: 'Linear regression value', 14: 'IE/2', 15: 'Non lag MA', 16: 'Zeo lag EMA', 17: 'Leader EMA'}, default=5),  # Averaging method
    }

