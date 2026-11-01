"""Macd hl mtf — converted from MQL5: MQL5 Indicators/MACD High_Low MTF/Macd hl mtf.mq5

Macd high/low multi time frame version
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 8, 7: 8}, 'colors': {1: [16748574], 2: [16748574], 3: [11119017], 4: [3937500], 5: [3937500], 6: [11119017, 16748574, 16760576, 3937500, 255], 7: [11119017, 16748574, 16760576, 3937500, 255]}, 'widths': {6: 3, 7: 1}, 'styles': {2: 2, 3: 2, 4: 2}, 'labels': {1: 'Level up', 2: 'Early level up', 3: 'Zero level', 4: 'Early level down', 5: 'Level down', 6: 'Macd value', 7: 'Macd signal'}, 'levels': [], 'description': ['Macd high/low multi time frame version'], 'name': 'Macd hl mtf', 'source': 'MQL5 Indicators/MACD High_Low MTF/Macd hl mtf.mq5', 'folder': 'MACD High_Low MTF', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 19, 'label': 'Fast DEMA period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 39, 'label': 'Slow DEMA period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpLookBackPeriod', 'py': 'inpLookBackPeriod', 'param': 'inpLookBackPeriod', 'type': 'int', 'default': 50, 'label': 'Lookback period', 'sinput': False}, {'mql': 'inpEarlyLevel', 'py': 'inpEarlyLevel', 'param': 'inpEarlyLevel', 'type': 'double', 'default': 25.0, 'label': 'Early levels %', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpInterpolate', 'py': 'inpInterpolate', 'param': 'inpInterpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
inpFastPeriod = _input('inpFastPeriod', 19)  # Fast DEMA period
inpSlowPeriod = _input('inpSlowPeriod', 39)  # Slow DEMA period
inpSignalPeriod = _input('inpSignalPeriod', 9)  # Signal period
inpLookBackPeriod = _input('inpLookBackPeriod', 50)  # Lookback period
inpEarlyLevel = _input('inpEarlyLevel', 25.0)  # Early levels %
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpInterpolate = _input('inpInterpolate', True)  # Interpolate in multi time frame mode?
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
signalc = Arr(0, 0.0)
levelm = Arr(0, 0.0)
levelu1 = Arr(0, 0.0)
levelu2 = Arr(0, 0.0)
leveld1 = Arr(0, 0.0)
leveld2 = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
timeFrame = 0
workEma = Arr(0, 0.0, dims=(3,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _mtfHandle, timeFrame
    SetIndexBuffer(0, levelu2, INDICATOR_DATA)
    SetIndexBuffer(1, levelu1, INDICATOR_DATA)
    SetIndexBuffer(2, levelm, INDICATOR_DATA)
    SetIndexBuffer(3, leveld1, INDICATOR_DATA)
    SetIndexBuffer(4, leveld2, INDICATOR_DATA)
    SetIndexBuffer(5, val, INDICATOR_DATA)
    SetIndexBuffer(6, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, signal, INDICATOR_DATA)
    SetIndexBuffer(8, signalc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(9, count, INDICATOR_CALCULATIONS)
    for i in range(0, 5):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    timeFrame = MathMax(timeFrameGet(inpTimeFrame), Period())
    if timeFrame != Period():
        _mtfHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), 0, inpFastPeriod, inpSlowPeriod, inpSignalPeriod, inpLookBackPeriod, inpEarlyLevel, inpPrice)
        if _mtfHandle == INVALID_HANDLE:
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' Macd high/low (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSignalPeriod) + ',' + _str(inpLookBackPeriod) + ')')
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
        if CopyBuffer(_mtfHandle, 9, 0, 1, result) == -1:
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
                levelu2[i] = result[0]
                if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) == -1:
                    break
                levelu1[i] = result[0]
                if CopyBuffer(_mtfHandle, 2, _DT(time[i]), 1, result) == -1:
                    break
                levelm[i] = result[0]
                if CopyBuffer(_mtfHandle, 3, _DT(time[i]), 1, result) == -1:
                    break
                leveld1[i] = result[0]
                if CopyBuffer(_mtfHandle, 4, _DT(time[i]), 1, result) == -1:
                    break
                leveld2[i] = result[0]
                if CopyBuffer(_mtfHandle, 5, _DT(time[i]), 1, result) == -1:
                    break
                val[i] = result[0]
                if CopyBuffer(_mtfHandle, 6, _DT(time[i]), 1, result) == -1:
                    break
                valc[i] = result[0]
                if CopyBuffer(_mtfHandle, 7, _DT(time[i]), 1, result) == -1:
                    break
                signal[i] = result[0]
            else:
                levelu2[i] = levelu2[i - 1]
                levelu1[i] = levelu1[i - 1]
                levelm[i] = levelm[i - 1]
                leveld1[i] = leveld1[i - 1]
                leveld2[i] = leveld2[i - 1]
                val[i] = val[i - 1]
                valc[i] = valc[i - 1]
                signal[i] = signal[i - 1]
            signalc[i] = valc[i]
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
                levelu2[i - k] = levelu2[i] + _fdiv((levelu2[i - n] - levelu2[i]) * k, n)
                levelu1[i - k] = levelu1[i] + _fdiv((levelu1[i - n] - levelu1[i]) * k, n)
                levelm[i - k] = levelm[i] + _fdiv((levelm[i - n] - levelm[i]) * k, n)
                leveld1[i - k] = leveld1[i] + _fdiv((leveld1[i - n] - leveld1[i]) * k, n)
                leveld2[i - k] = leveld2[i] + _fdiv((leveld2[i - n] - leveld2[i]) * k, n)
                val[i - k] = val[i] + _fdiv((val[i - n] - val[i]) * k, n)
                signal[i - k] = signal[i] + _fdiv((signal[i - n] - signal[i]) * k, n)
                k += 1
            i += 1
        return i
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = iEma(_price, inpFastPeriod, i, rates_total, 0) - iEma(_price, inpSlowPeriod, i, rates_total, 1)
        signal[i] = iEma(val[i], inpSignalPeriod, i, rates_total, 2)
        _start = MathMax(i - inpLookBackPeriod, 0)
        _count = MathMin(_start + 1, inpLookBackPeriod)
        max_ = val[ArrayMaximum(val, _start, _count)]
        min_ = val[ArrayMinimum(val, _start, _count)]
        levelu2[i] = max_
        leveld2[i] = min_
        levelm[i] = (max_ + min_) / 2.0
        levelu1[i] = levelm[i] + (((levelu2[i] - levelm[i]) * inpEarlyLevel) / 100.0)
        leveld1[i] = levelm[i] - (((levelm[i] - leveld2[i]) * inpEarlyLevel) / 100.0)
        valc[i] = ((2 if (val[i] > levelu2[i]) else 1 if (val[i] > levelm[i]) else 0) if (val[i] > signal[i]) else (4 if (val[i] < leveld2[i]) else 3 if (val[i] < levelm[i]) else 0) if (val[i] < signal[i]) else valc[i - 1] if (i > 0) else 0)
        signalc[i] = valc[i]
        i += 1
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    return i

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def getPrice(tprice, open, close, high, low, i, _bars):
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

# ---- static local variables
_s_timeFrameCheck_warned = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MacdHlMtf(_MQL5Indicator):
    name = 'Macd hl mtf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=0),  # Time frame
        'inpFastPeriod': 19,  # Fast DEMA period
        'inpSlowPeriod': 39,  # Slow DEMA period
        'inpSignalPeriod': 9,  # Signal period
        'inpLookBackPeriod': 50,  # Lookback period
        'inpEarlyLevel': 25.0,  # Early levels %
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpInterpolate': True,  # Interpolate in multi time frame mode?
    }

