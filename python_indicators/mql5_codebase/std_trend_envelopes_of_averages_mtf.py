"""STD Trend envelopes of averages - mtf — converted from MQL5: MQL5 Indicators/STD Trend Envelopes of Averages - multi time frame/STD Trend envelopes of averages - mtf.mq5

STD Trend envelopes of averages - mtf
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [16748574], 2: [3937500], 3: [16748574], 4: [3937500]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {}, 'labels': {1: 'Trend envelope up trend line', 2: 'Trend envelope down trend line', 3: 'Trend envelope up trend start', 4: 'Trend envelope down trend start'}, 'levels': [], 'description': ['STD Trend envelopes of averages - mtf'], 'name': 'STD Trend envelopes of averages - mtf', 'source': 'MQL5 Indicators/STD Trend Envelopes of Averages - multi time frame/STD Trend envelopes of averages - mtf.mq5', 'folder': 'STD Trend Envelopes of Averages - multi time frame', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpDevPeriod', 'py': 'inpDevPeriod', 'param': 'inpDevPeriod', 'type': 'int', 'default': 14, 'label': 'Deviations period', 'sinput': False}, {'mql': 'inpDeviation', 'py': 'inpDeviation', 'param': 'inpDeviation', 'type': 'double', 'default': 1.5, 'label': 'Deviations multilication factor', 'sinput': False}, {'mql': 'inpSmtPeriod', 'py': 'inpSmtPeriod', 'param': 'inpSmtPeriod', 'type': 'int', 'default': 14, 'label': 'Smoothing period (<=1 for no smoothing)', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'inpInterpolate', 'py': 'inpInterpolate', 'param': 'inpInterpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter
MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

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
inpDevPeriod = _input('inpDevPeriod', 14)  # Deviations period
inpDeviation = _input('inpDeviation', 1.5)  # Deviations multilication factor
inpSmtPeriod = _input('inpSmtPeriod', 14)  # Smoothing period (<=1 for no smoothing)
inpMaMethod = _input('inpMaMethod', ma_sma)  # Smoothing method
inpInterpolate = _input('inpInterpolate', True)  # Interpolate in multi time frame mode?
lineup = Arr(0, 0.0)
linedn = Arr(0, 0.0)
arrowup = Arr(0, 0.0)
arrowdn = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
_indicatorTimeFrame = 0
_indicatorName = ""
workDev = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(2,))
workEma = Arr(0, 0.0, dims=(2,))
workSmma = Arr(0, 0.0, dims=(2,))
workLwma = Arr(0, 0.0, dims=(2,))
workTrendEnvelopes = Arr(0, 0.0, dims=(3,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

class sTrendEnvelope(MqlObject):
    _q_fields = ('upline', 'downline', 'trend', 'trendChange')
    def __init__(self, *args):
        self.upline = 0.0
        self.downline = 0.0
        self.trend = 0
        self.trendChange = False

def OnInit():
    global _indicatorName, _indicatorTimeFrame, _mtfHandle
    SetIndexBuffer(0, lineup, INDICATOR_DATA)
    SetIndexBuffer(1, linedn, INDICATOR_DATA)
    SetIndexBuffer(2, arrowup, INDICATOR_DATA)
    PlotIndexGetInteger(2, PLOT_ARROW, 159)
    SetIndexBuffer(3, arrowdn, INDICATOR_DATA)
    PlotIndexGetInteger(3, PLOT_ARROW, 159)
    SetIndexBuffer(4, count, INDICATOR_CALCULATIONS)
    _indicatorTimeFrame = MathMax(timeFrameGet(inpTimeFrame), Period())
    _indicatorName = getIndicatorName()
    if _indicatorTimeFrame != Period():
        _mtfHandle = iCustom(Symbol(), _indicatorTimeFrame, _indicatorName, 0, inpDevPeriod, inpDeviation, inpSmtPeriod, inpMaMethod)
        if _mtfHandle == INVALID_HANDLE:
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(_indicatorTimeFrame) + ' STD trend envelopes (' + _str(inpDevPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if _indicatorTimeFrame != Period():
        result = Arr(0, 0.0)
        if BarsCalculated(_mtfHandle) < 0:
            return prev_calculated
        if not timeFrameCheck(_indicatorTimeFrame, time):
            return prev_calculated
        if CopyBuffer(_mtfHandle, 4, 0, 1, result) == -1:
            return prev_calculated
        k = 0
        n = 0
        i = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _int(_fdiv(result[0] * float(PeriodSeconds(_indicatorTimeFrame)), PeriodSeconds(Period()))) - 1, 0))
        _prevMark = 0
        _seconds = PeriodSeconds(_indicatorTimeFrame)
        while i < rates_total:
            _currMark = _int(_idiv(time[i], _seconds))
            if _currMark != _prevMark:
                _prevMark = _currMark
                if CopyBuffer(_mtfHandle, 0, _DT(time[i]), 1, result) <= 0:
                    break
                lineup[i] = result[0]
                if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) <= 0:
                    break
                linedn[i] = result[0]
                if CopyBuffer(_mtfHandle, 2, _DT(time[i]), 1, result) <= 0:
                    break
                arrowup[i] = result[0]
                if CopyBuffer(_mtfHandle, 3, _DT(time[i]), 1, result) <= 0:
                    break
                arrowdn[i] = result[0]
            else:
                lineup[i] = lineup[i - 1]
                linedn[i] = linedn[i - 1]
                arrowdn[i] = EMPTY_VALUE
                arrowup[i] = EMPTY_VALUE
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
                if lineup[i] != EMPTY_VALUE and lineup[i - n] != EMPTY_VALUE:
                    lineup[i - k] = lineup[i] + _fdiv((lineup[i - n] - lineup[i]) * k, n)
                if linedn[i] != EMPTY_VALUE and linedn[i - n] != EMPTY_VALUE:
                    linedn[i - k] = linedn[i] + _fdiv((linedn[i - n] - linedn[i]) * k, n)
                k += 1
            i += 1
        return i
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _dev = iDeviation(close[i], inpDevPeriod, i, rates_total)
        _high = iCustomMa(inpMaMethod, high[i], inpSmtPeriod, i, rates_total, 0)
        _low = iCustomMa(inpMaMethod, low[i], inpSmtPeriod, i, rates_total, 1)
        _result = iTrendEnvelope(_high, _low, close[i], _dev * inpDeviation, i, rates_total)
        lineup[i] = _result.upline
        linedn[i] = _result.downline
        arrowup[i] = (lineup[i] if (_result.trendChange and _result.trend == 1) else EMPTY_VALUE)
        arrowdn[i] = (linedn[i] if (_result.trendChange and _result.trend == -1) else EMPTY_VALUE)
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    return rates_total

def iDeviation(value, length, i, bars, isSample=False):
    if ArraySize(workDev) != bars:
        ArrayResize(workDev, bars)
    workDev[i] = value
    sumx = 0.0
    sumxx = 0.0
    k = 0
    while k < length and (i - k) >= 0:
        pass
        sumx += workDev[i - k]
        sumxx += workDev[i - k] * workDev[i - k]
        k += 1
    return MathSqrt(_fdiv(sumxx - _fdiv(sumx * sumx, length), MathMax(length - isSample, 1)))

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    workSmma[r][instanceNo] = price
    if r > 1 and period > 1:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    if period < 1:
        return price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

def iTrendEnvelope(valueh, valuel, value, deviation, i, bars, instanceNo=0):
    if ArrayRange(workTrendEnvelopes, 0) != bars:
        ArrayResize(workTrendEnvelopes, bars)
    instanceNo *= 3
    workTrendEnvelopes[i][instanceNo + 1] = valueh + deviation
    workTrendEnvelopes[i][instanceNo + 0] = valuel - deviation
    workTrendEnvelopes[i][instanceNo + 2] = ((1 if (value > workTrendEnvelopes[i - 1][instanceNo + 1]) else -1 if (value < workTrendEnvelopes[i - 1][instanceNo + 0]) else workTrendEnvelopes[i - 1][instanceNo + 2]) if (i > 0) else 0)
    if (i > 0 and workTrendEnvelopes[i][instanceNo + 2] > 0) and workTrendEnvelopes[i][instanceNo + 0] < workTrendEnvelopes[i - 1][instanceNo + 0]:
        workTrendEnvelopes[i][instanceNo + 0] = workTrendEnvelopes[i - 1][instanceNo + 0]
    if (i > 0 and workTrendEnvelopes[i][instanceNo + 2] < 0) and workTrendEnvelopes[i][instanceNo + 1] > workTrendEnvelopes[i - 1][instanceNo + 1]:
        workTrendEnvelopes[i][instanceNo + 1] = workTrendEnvelopes[i - 1][instanceNo + 1]
    _result = sTrendEnvelope()
    _result.trend = _int(workTrendEnvelopes[i][instanceNo + 2])
    _result.trendChange = ((workTrendEnvelopes[i][instanceNo + 2] != workTrendEnvelopes[i - 1][instanceNo + 2]) if (i > 0) else False)
    _result.upline = (workTrendEnvelopes[i][instanceNo + 0] if (workTrendEnvelopes[i][instanceNo + 2] == 1) else EMPTY_VALUE)
    _result.downline = (workTrendEnvelopes[i][instanceNo + 1] if (workTrendEnvelopes[i][instanceNo + 2] == -1) else EMPTY_VALUE)
    return _copy(_result)

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
    _path = Box(MQL5InfoString(MQL5_PROGRAM_PATH))
    StringToLower(_path)
    _partsA = Arr(0, "")
    _partsS = StringGetCharacter('\\', 0)
    _partsN = StringSplit(_path.v, _partsS, _partsA)
    name = _partsA[_partsN - 1]
    n = _partsN - 2
    while n >= 0 and _partsA[n] != 'indicators':
        name = _partsA[n] + '\\' + name
        n -= 1
    return name

def timeFrameCheck(_timeFrame, time):
    if time[0] < SeriesInfoInteger(Symbol(), _timeFrame, SERIES_FIRSTDATE):
        startTime = Box(0)
        testTime = Arr(0, 0)
        if SeriesInfoInteger(Symbol(), PERIOD_M1, SERIES_TERMINAL_FIRSTDATE, startTime):
            if startTime.v > 0:
                CopyTime(Symbol(), _timeFrame, _DT(time[0]), 1, testTime)
                SeriesInfoInteger(Symbol(), _timeFrame, SERIES_FIRSTDATE, startTime)
        if startTime.v <= 0 or startTime.v > time[0]:
            Comment(MQL5InfoString(MQL5_PROGRAM_NAME) + '\nMissing data for ' + timeFrameToString(_timeFrame) + ' time frame\nRe-trying on next tick')
            return False
    _comment = ChartGetString(0, CHART_COMMENT)
    _shortName = MQL5InfoString(MQL5_PROGRAM_NAME)
    if StringFind(_comment, _shortName, 0) >= 0:
        Comment('')
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class STDTrendEnvelopesOfAveragesMtf(_MQL5Indicator):
    name = 'STD Trend envelopes of averages - mtf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=0),  # Time frame
        'inpDevPeriod': 14,  # Deviations period
        'inpDeviation': 1.5,  # Deviations multilication factor
        'inpSmtPeriod': 14,  # Smoothing period (<=1 for no smoothing)
        'inpMaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Smoothing method
        'inpInterpolate': True,  # Interpolate in multi time frame mode?
    }

