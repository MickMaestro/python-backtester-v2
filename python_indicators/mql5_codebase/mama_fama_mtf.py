"""Mama + fama mtf — converted from MQL5: MQL5 Indicators/MAMA + FAMA Multi Timeframe/Mama + fama mtf.mq5

Mama - fama (multi time frame version)
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [11119017, 6333684, 16748574], 2: [11119017, 6333684, 16748574]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Fama', 2: 'Mama'}, 'levels': [], 'description': ['Mama - fama (multi time frame version)'], 'name': 'Mama + fama mtf', 'source': 'MQL5 Indicators/MAMA + FAMA Multi Timeframe/Mama + fama mtf.mq5', 'folder': 'MAMA + FAMA Multi Timeframe', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpFastLimit', 'py': 'inpFastLimit', 'param': 'inpFastLimit', 'type': 'double', 'default': 0.5, 'label': 'Fast limit', 'sinput': False}, {'mql': 'inpSlowLimit', 'py': 'inpSlowLimit', 'param': 'inpSlowLimit', 'type': 'double', 'default': 0.05, 'label': 'Slow limit', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}, {'mql': 'inpInterpolate', 'py': 'inpInterpolate', 'param': 'inpInterpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter
MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# enum enTimeFrames
tf_cu = 0
tf_m1 = 1
tf_m2 = 2
tf_m3 = 3
tf_m4 = 4
tf_m5 = 5
tf_m6 = 6
tf_m10 = 10
tf_m12 = 12
tf_m15 = 15
tf_m20 = 20
tf_m30 = 30
tf_h1 = 16385
tf_h2 = 16386
tf_h3 = 16387
tf_h4 = 16388
tf_h6 = 16390
tf_h8 = 16392
tf_h12 = 16396
tf_d1 = 16408
tf_w1 = 32769
tf_mn = 49153
tf_cp1 = -1
tf_cp2 = -2
tf_cp3 = -3
_enum('enTimeFrames', {0: 'tf_cu', 1: 'tf_m1', 2: 'tf_m2', 3: 'tf_m3', 4: 'tf_m4', 5: 'tf_m5', 6: 'tf_m6', 10: 'tf_m10', 12: 'tf_m12', 15: 'tf_m15', 20: 'tf_m20', 30: 'tf_m30', 16385: 'tf_h1', 16386: 'tf_h2', 16387: 'tf_h3', 16388: 'tf_h4', 16390: 'tf_h6', 16392: 'tf_h8', 16396: 'tf_h12', 16408: 'tf_d1', 32769: 'tf_w1', 49153: 'tf_mn', -1: 'tf_cp1', -2: 'tf_cp2', -3: 'tf_cp3'})

# ---- inputs and global variables
inpTimeFrame = _input('inpTimeFrame', tf_cu)  # Time frame
inpFastLimit = _input('inpFastLimit', 0.5)  # Fast limit
inpSlowLimit = _input('inpSlowLimit', 0.05)  # Slow limit
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
inpInterpolate = _input('inpInterpolate', True)  # Interpolate in multi time frame mode?
valf = Arr(0, 0.0)
valfc = Arr(0, 0.0)
valm = Arr(0, 0.0)
valmc = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
timeFrame = 0
workMama = Arr(0, 0.0, dims=(16,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _mtfHandle, timeFrame
    SetIndexBuffer(0, valf, INDICATOR_DATA)
    SetIndexBuffer(1, valfc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, valm, INDICATOR_DATA)
    SetIndexBuffer(3, valmc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, count, INDICATOR_CALCULATIONS)
    timeFrame = MathMax(timeFrameGet(inpTimeFrame), Period())
    if timeFrame != Period():
        _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), tf_cu, inpFastLimit, inpSlowLimit, inpPrice)
        if _mtfHandle == INVALID_HANDLE:
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' Mama - fama (' + _str(inpFastLimit) + ',' + _str(inpSlowLimit) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if timeFrame != Period():
        result = Arr(0, 0.0)
        if BarsCalculated(_mtfHandle) < 0:
            return prev_calculated
        if not timeFrameCheck(timeFrame, time):
            return prev_calculated
        if CopyBuffer(_mtfHandle, 4, 0, 1, result) == -1:
            return prev_calculated
        k = 0
        n = 0
        i = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _idiv(_int(result[0]) * PeriodSeconds(timeFrame), PeriodSeconds(Period())) - 1, 0))
        _prevMark = 0
        _seconds = PeriodSeconds(timeFrame)
        while i < rates_total:
            _currMark = _int(_idiv(time[i], _seconds))
            if _currMark != _prevMark:
                _prevMark = _currMark
                if CopyBuffer(_mtfHandle, 0, _DT(time[i]), 1, result) == -1:
                    break
                valf[i] = result[0]
                if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) == -1:
                    break
                valfc[i] = result[0]
                if CopyBuffer(_mtfHandle, 2, _DT(time[i]), 1, result) == -1:
                    break
                valm[i] = result[0]
                if CopyBuffer(_mtfHandle, 3, _DT(time[i]), 1, result) == -1:
                    break
                valmc[i] = result[0]
            else:
                valf[i] = valf[i - 1]
                valm[i] = valm[i - 1]
                valfc[i] = valfc[i - 1]
                valmc[i] = valmc[i - 1]
            if not inpInterpolate:
                i += 1
                continue
            _nextMark = (_int(_idiv(time[i + 1], _seconds)) if (i < (rates_total - 1)) else (_prevMark + 1))
            if _nextMark == _prevMark:
                i += 1
                continue
            n = 1
            while (i - n) > 0 and time[i - n] >= (_prevMark * _seconds):
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                valf[i - k] = valf[i] + _fdiv((valf[i - n] - valf[i]) * k, n)
                valm[i - k] = valm[i] + _fdiv((valm[i - n] - valm[i]) * k, n)
                k += 1
            i += 1
        return i
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _fama = Box(0.0)
        valm[i] = iMama(getPrice(inpPrice, open, close, high, low, i, rates_total), inpFastLimit, inpSlowLimit, _fama, i, rates_total)
        valf[i] = _fama.v
        valfc[i] = (1 if (valf[i] > valm[i]) else 2 if (valf[i] < valm[i]) else valfc[i - 1] if (i > 0) else 0)
        valmc[i] = valfc[i]
        i += 1
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    return i

def iMama(price, fastLimit, slowLimit, retFama, r, bars):
    if ArrayRange(workMama, 0) != bars:
        ArrayResize(workMama, bars)
    workMama[r][0] = price
    workMama[r][1] = ((((4.0 * workMama[r][0]) + (3.0 * workMama[r - 1][0]) + (2.0 * workMama[r - 2][0]) + workMama[r - 3][0]) / 10.0) if (r > 3) else price)
    workMama[r][2] = ((((0.0962 * workMama[r][1]) + (0.5769 * workMama[r - 2][1]) - (0.5769 * workMama[r - 4][1]) - (0.0962 * workMama[r - 6][1])) * ((0.075 * workMama[r - 1][3]) + 0.54)) if (r > 5) else workMama[r][1])
    workMama[r][5] = ((((0.0962 * workMama[r][2]) + (0.5769 * workMama[r - 2][2]) - (0.5769 * workMama[r - 4][2]) - (0.0962 * workMama[r - 6][2])) * ((0.075 * workMama[r - 1][3]) + 0.54)) if (r > 5) else workMama[r][2])
    workMama[r][6] = (workMama[r - 3][2] if (r > 2) else workMama[r][2])
    workMama[r][7] = ((((0.0962 * workMama[r][6]) + (0.5769 * workMama[r - 2][6]) - (0.5769 * workMama[r - 4][6]) - (0.0962 * workMama[r - 6][6])) * ((0.075 * workMama[r - 1][3]) + 0.54)) if (r > 5) else workMama[r][6])
    workMama[r][8] = ((((0.0962 * workMama[r][5]) + (0.5769 * workMama[r - 2][5]) - (0.5769 * workMama[r - 4][5]) - (0.0962 * workMama[r - 6][5])) * ((0.075 * workMama[r - 1][3]) + 0.54)) if (r > 5) else workMama[r][5])
    workMama[r][10] = (workMama[r][6] if (r == 0) else ((0.2 * (workMama[r][6] - workMama[r][8])) + (0.8 * workMama[r - 1][10])))
    workMama[r][9] = (workMama[r][5] if (r == 0) else ((0.2 * (workMama[r][5] + workMama[r][7])) + (0.8 * workMama[r - 1][9])))
    workMama[r][11] = (workMama[r][10] if (r == 0) else ((0.2 * ((workMama[r][10] * workMama[r - 1][10]) + (workMama[r][9] * workMama[r - 1][9]))) + (0.8 * workMama[r - 1][11])))
    workMama[r][12] = (workMama[r][10] if (r == 0) else ((0.2 * ((workMama[r][10] * workMama[r - 1][9]) - (workMama[r][9] * workMama[r - 1][10]))) + (0.8 * workMama[r - 1][12])))
    if workMama[r][11] != 0 and workMama[r][12] != 0:
        workMama[r][3] = _fdiv(360.0, MathArctan(_fdiv(workMama[r][12], workMama[r][11])) * (180.0 / M_PI))
    workMama[r][3] = (workMama[r][3] if (r == 0) else MathMin(workMama[r][3], 1.5 * workMama[r - 1][3]))
    workMama[r][3] = (workMama[r][3] if (r == 0) else MathMax(workMama[r][3], 0.67 * workMama[r - 1][3]))
    workMama[r][3] = MathMin(MathMax(workMama[r][3], 6), 50)
    workMama[r][3] = (workMama[r][3] if (r == 0) else ((0.2 * workMama[r][3]) + (0.8 * workMama[r - 1][3])))
    if workMama[r][6] != 0:
        workMama[r][4] = MathArctan(_fdiv(workMama[r][5], workMama[r][6])) * (180.0 / M_PI)
    DeltaPhase = (0 if (r == 0) else MathMax(workMama[r - 1][4] - workMama[r][4], 1))
    Alpha = (MathMax(MathMin(_fdiv(fastLimit, DeltaPhase), fastLimit), slowLimit) if (DeltaPhase != 0) else 1)
    workMama[r][13] = Alpha
    workMama[r][14] = (price if (r == 0) else ((workMama[r][13] * workMama[r][0]) + ((1.0 - workMama[r][13]) * workMama[r - 1][14])))
    workMama[r][15] = (price if (r == 0) else ((0.5 * workMama[r][13] * workMama[r][14]) + ((1.0 - (0.5 * workMama[r][13])) * workMama[r - 1][15])))
    retFama.v = workMama[r][15]
    return workMama[r][14]

def timeFrameToString(period):
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsStr[i]

def timeFrameGet(period):
    _shift = (MathAbs(period) if (period < 0) else 0)
    if _shift > 0 or period == tf_cu:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsPer[MathMin(i + _shift, ArraySize(_tfsPer) - 1)]

def getIndicatorName():
    _path = MQL5InfoString(MQL5_PROGRAM_PATH)
    _partsA = Arr(0, "")
    _partsS = StringGetCharacter('\\', 0)
    _partsN = StringSplit(_path, _partsS, _partsA)
    name = _partsA[_partsN - 1]
    n = _partsN - 2
    while n >= 0 and _toLower(_partsA[n]) != 'indicators':
        name = _partsA[n] + '\\' + name
        n -= 1
    return name

def _toLower(_toConvert):
    _toConvert = Box(_toConvert)
    StringToLower(_toConvert)
    return _toConvert.v

def timeFrameCheck(_timeFrame, time):
    global _s_timeFrameCheck_warned
    if time[0] < SeriesInfoInteger(Symbol(), _timeFrame, SERIES_FIRSTDATE):
        startTime = Box(0)
        testTime = Arr(0, 0)
        if SeriesInfoInteger(Symbol(), PERIOD_M1, SERIES_TERMINAL_FIRSTDATE, startTime):
            if startTime.v > 0:
                CopyTime(Symbol(), _timeFrame, _DT(time[0]), 1, testTime)
                SeriesInfoInteger(Symbol(), _timeFrame, SERIES_FIRSTDATE, startTime)
        if startTime.v <= 0 or startTime.v > time[0]:
            Comment(MQL5InfoString(MQL5_PROGRAM_NAME) + '\nMissing data for ' + timeFrameToString(_timeFrame) + ' time frame\nRe-trying on next tick')
            _s_timeFrameCheck_warned = True
            return False
    if _s_timeFrameCheck_warned:
        Comment('')
        _s_timeFrameCheck_warned = False
    return True

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
        _sw1 = tprice
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

# ---- static local variables
_s_timeFrameCheck_warned = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MamaFamaMtf(_MQL5Indicator):
    name = 'Mama + fama mtf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=0),  # Time frame
        'inpFastLimit': 0.5,  # Fast limit
        'inpSlowLimit': 0.05,  # Slow limit
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
        'inpInterpolate': True,  # Interpolate in multi time frame mode?
    }

