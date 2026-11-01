"""chandes_dmi — converted from MQL5: MQL5 Indicators/Tushar Chande's DMI/chandes_dmi.mq5

Copyright: mladen; Link: www.tradcode.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.tradcode.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 8}, 'colors': {1: [3329330, 42495, 8421504]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Chande DMI'}, 'levels': [], 'description': [], 'name': 'chandes_dmi', 'source': "MQL5 Indicators/Tushar Chande's DMI/chandes_dmi.mq5", 'folder': "Tushar Chande's DMI", 'inputs': [{'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'StdDevPeriod', 'py': 'StdDevPeriod', 'param': 'StdDevPeriod', 'type': 'int', 'default': 5, 'label': 'Period of Standard Deviation', 'sinput': False}, {'mql': 'MAStdDevPeriod', 'py': 'MAStdDevPeriod', 'param': 'MAStdDevPeriod', 'type': 'int', 'default': 10, 'label': 'Period of smoothing', 'sinput': False}, {'mql': 'MAStdDevMode', 'py': 'MAStdDevMode', 'param': 'MAStdDevMode', 'type': 'int', 'default': 0, 'label': 'Mode of smoothing MA', 'sinput': False}, {'mql': 'DMIPeriod', 'py': 'DMIPeriod', 'param': 'DMIPeriod', 'type': 'int', 'default': 15, 'label': 'Dynamic Momentum Index Period', 'sinput': False}, {'mql': 'DmiLowerLimit', 'py': 'DmiLowerLimit', 'param': 'DmiLowerLimit', 'type': 'int', 'default': 10, 'label': 'Dynamic Periods Lower Bound', 'sinput': False}, {'mql': 'DmiUpperLimit', 'py': 'DmiUpperLimit', 'param': 'DmiUpperLimit', 'type': 'int', 'default': 50, 'label': 'Dynamic Periods Upper Bound', 'sinput': False}, {'mql': 'LevelUp', 'py': 'LevelUp', 'param': 'LevelUp', 'type': 'double', 'default': 70.0, 'label': 'Lower level', 'sinput': False}, {'mql': 'LevelDown', 'py': 'LevelDown', 'param': 'LevelDown', 'type': 'double', 'default': 30.0, 'label': 'Upper level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enAvgType
avgSma = 0
avgEma = 1
avgSmma = 2
avgLwma = 3
_enum('enAvgType', {0: 'avgSma', 1: 'avgEma', 2: 'avgSmma', 3: 'avgLwma'})

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
Price = _input('Price', pr_close)  # Price to use
StdDevPeriod = _input('StdDevPeriod', 5)  # Period of Standard Deviation
MAStdDevPeriod = _input('MAStdDevPeriod', 10)  # Period of smoothing
MAStdDevMode = _input('MAStdDevMode', 0)  # Mode of smoothing MA
DMIPeriod = _input('DMIPeriod', 15)  # Dynamic Momentum Index Period
DmiLowerLimit = _input('DmiLowerLimit', 10)  # Dynamic Periods Lower Bound
DmiUpperLimit = _input('DmiUpperLimit', 50)  # Dynamic Periods Upper Bound
LevelUp = _input('LevelUp', 70.0)  # Lower level
LevelDown = _input('LevelDown', 30.0)  # Upper level
dmi = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
totalBars = 0
trend = Arr(0, 0.0)
avgma = Arr(0, 0.0)
prics = Arr(0, 0.0)
wrkBuffer = Arr(0, 0.0, dims=(13,))
workRsi = Arr(0, 0.0, dims=(3,))
workSma = Arr(0, 0.0, dims=(4,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, dmi, INDICATOR_DATA)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, LevelUp)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, LevelDown)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Chandes DMI (' + DoubleToString(DMIPeriod, 1) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global totalBars
    totalBars = rates_total
    if ArraySize(trend) != rates_total:
        ArrayResize(trend, rates_total)
        ArrayResize(avgma, rates_total)
        ArrayResize(prics, rates_total)
        ArrayResize(wrkBuffer, rates_total)
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        prics[i] = getPrice(Price, open, close, high, low, i, rates_total)
        avgma[i] = iSma(prics[i], MAStdDevPeriod, i, 1)
        deviation = iDeviationPlus(prics, avgma, MAStdDevPeriod, i)
        deviatioa = iCustomMa(MAStdDevMode, deviation, MAStdDevPeriod, i, 0)
        vi = 0.0
        td = 1
        if deviatioa != 0:
            vi = _fdiv(deviation, deviatioa)
        if vi != 0:
            td = _int(MathRound(_fdiv(DMIPeriod, vi)))
        td = MathMax(MathMin(td, DmiUpperLimit), DmiLowerLimit)
        Kg = _fdiv(3.0, 2.0 + td)
        Hg = 1.0 - Kg
        wrkBuffer[i][12] = prics[i]
        if i == 0:
            for c in range(0, 12):
                wrkBuffer[i][c] = 0.0
            continue
        roc = wrkBuffer[i][12] - wrkBuffer[i - 1][12]
        roa = MathAbs(roc)
        for k in range(0, 3):
            kk = k * 2
            wrkBuffer[i][kk + 0] = (Kg * roc) + (Hg * wrkBuffer[i - 1][kk + 0])
            wrkBuffer[i][kk + 1] = (Kg * wrkBuffer[i][kk + 0]) + (Hg * wrkBuffer[i - 1][kk + 1])
            roc = (1.5 * wrkBuffer[i][kk + 0]) - (0.5 * wrkBuffer[i][kk + 1])
            wrkBuffer[i][kk + 6] = (Kg * roa) + (Hg * wrkBuffer[i - 1][kk + 6])
            wrkBuffer[i][kk + 7] = (Kg * wrkBuffer[i][kk + 6]) + (Hg * wrkBuffer[i - 1][kk + 7])
            roa = (1.5 * wrkBuffer[i][kk + 6]) - (0.5 * wrkBuffer[i][kk + 7])
        if roa != 0:
            dmi[i] = MathMax(MathMin((_fdiv(roc, roa) + 1.0) * 50.0, 100.0), 0.0)
        else:
            dmi[i] = 50.0
        trend[i] = 0.0
        if dmi[i] > LevelUp:
            trend[i] = 1.0
        if dmi[i] < LevelDown:
            trend[i] = -1.0
        if trend[i] == 1:
            colorBuffer[i] = 0.0
        if trend[i] == -1:
            colorBuffer[i] = 1.0
        if trend[i] == 0:
            colorBuffer[i] = 2.0
    return rates_total

def getPrice(price, open, close, high, low, i, bars):
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

def iDeviationPlus(array, ma, period, i):
    sum_ = 0.0
    k = 0
    while k < period and (i - k) >= 0:
        sum_ += (array[i - k] - ma[i]) * (array[i - k] - ma[i])
        k += 1
    return MathSqrt(_fdiv(sum_, period))

def iRsi(price, period, bars, i, forInstance=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = forInstance * 3
    alpha = _fdiv(1.0, period)
    workRsi[i][0 + z] = price
    if i < period:
        k = 0
        sum_ = 0.0
        k = 0
        while k < period and (i - k - 1) >= 0:
            sum_ += MathAbs(workRsi[i - k][0 + z] - workRsi[i - k - 1][0 + z])
            k += 1
        workRsi[i][1 + z] = _fdiv(workRsi[i][0 + z] - workRsi[0][0 + z], MathMax(k, 1))
        workRsi[i][2 + z] = _fdiv(sum_, MathMax(k, 1))
    else:
        change = workRsi[i][0 + z] - workRsi[i - 1][0 + z]
        workRsi[i][1 + z] = workRsi[i - 1][1 + z] + (alpha * (change - workRsi[i - 1][1 + z]))
        workRsi[i][2 + z] = workRsi[i - 1][2 + z] + (alpha * (MathAbs(change) - workRsi[i - 1][2 + z]))
    if workRsi[i][2 + z] != 0:
        return 50.0 * (_fdiv(workRsi[i][1 + z], workRsi[i][2 + z]) + 1)
    else:
        return 0.0

def iCustomMa(mode, price, length, r, instanceNo=0):
    _sw2 = mode
    if _sw2 == avgSma:
        return iSma(price, _int(length), r, instanceNo)
    elif _sw2 == avgEma:
        return iEma(price, length, r, instanceNo)
    elif _sw2 == avgSmma:
        return iSmma(price, _int(length), r, instanceNo)
    elif _sw2 == avgLwma:
        return iLwma(price, _int(length), r, instanceNo)
    else:
        return price

def iSma(price, period, r, instanceNo=0):
    if ArrayRange(workSma, 0) != totalBars:
        ArrayResize(workSma, totalBars)
    instanceNo *= 2
    k = 0
    workSma[r][instanceNo] = price
    workSma[r][instanceNo + 1] = 0.0
    k = 0
    while k < period and (r - k) >= 0:
        workSma[r][instanceNo + 1] += workSma[r - k][instanceNo]
        k += 1
    workSma[r][instanceNo + 1] = _fdiv(workSma[r][instanceNo + 1], float(k))
    return workSma[r][instanceNo + 1]

def iEma(price, period, r, instanceNo=0):
    if ArrayRange(workEma, 0) != totalBars:
        ArrayResize(workEma, totalBars)
    alpha = _fdiv(2.0, 1.0 + period)
    workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (alpha * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChandesDmi(_MQL5Indicator):
    name = 'chandes_dmi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average'}, default=0),  # Price to use
        'StdDevPeriod': 5,  # Period of Standard Deviation
        'MAStdDevPeriod': 10,  # Period of smoothing
        'MAStdDevMode': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Mode of smoothing MA
        'DMIPeriod': 15,  # Dynamic Momentum Index Period
        'DmiLowerLimit': 10,  # Dynamic Periods Lower Bound
        'DmiUpperLimit': 50,  # Dynamic Periods Upper Bound
        'LevelUp': 70.0,  # Lower level
        'LevelDown': 30.0,  # Upper level
    }
    y_range = (0.0, 100.0)

