"""CCI  squeeze mtf — converted from MQL5: MQL5 Indicators/CCI Squeeze Multi Timeframe/CCI  squeeze mtf.mq5

CCI squeeze multi time frame
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [3329330, 3329434, 42495, 17919], 2: [3329330, 3329434, 42495, 17919]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'CCI Histogram', 2: 'CCI'}, 'levels': [], 'description': ['CCI squeeze multi time frame'], 'name': 'CCI  squeeze mtf', 'source': 'MQL5 Indicators/CCI Squeeze Multi Timeframe/CCI  squeeze mtf.mq5', 'folder': 'CCI Squeeze Multi Timeframe', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpCciPeriod', 'py': 'inpCciPeriod', 'param': 'inpCciPeriod', 'type': 'int', 'default': 32, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpCciPrice', 'py': 'inpCciPrice', 'param': 'inpCciPrice', 'type': 'int', 'default': 6, 'label': 'CCI price', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 200, 'label': 'Average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpMaPrice', 'py': 'inpMaPrice', 'param': 'inpMaPrice', 'type': 'int', 'default': 6, 'label': 'Average price', 'sinput': False}, {'mql': 'inpInterpolate', 'py': 'inpInterpolate', 'param': 'inpInterpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
inpCciPeriod = _input('inpCciPeriod', 32)  # CCI period
inpCciPrice = _input('inpCciPrice', PRICE_TYPICAL)  # CCI price
inpMaPeriod = _input('inpMaPeriod', 200)  # Average period
inpMaMethod = _input('inpMaMethod', ma_ema)  # Average method
inpMaPrice = _input('inpMaPrice', PRICE_TYPICAL)  # Average price
inpInterpolate = _input('inpInterpolate', True)  # Interpolate in multi time frame mode?
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
valh = Arr(0, 0.0)
valhc = Arr(0, 0.0)
prices = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
_indicatorTimeFrame = 0
_indicatorName = ""
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _indicatorName, _indicatorTimeFrame, _mtfHandle
    SetIndexBuffer(0, valh, INDICATOR_DATA)
    SetIndexBuffer(1, valhc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, count, INDICATOR_CALCULATIONS)
    _indicatorTimeFrame = MathMax(timeFrameGet(inpTimeFrame), Period())
    _indicatorName = getIndicatorName()
    if _indicatorTimeFrame != Period():
        _mtfHandle = iCustom(Symbol(), _indicatorTimeFrame, _indicatorName, 0, inpCciPeriod, inpCciPrice, inpMaPeriod, inpMaMethod, inpMaPrice)
        if _mtfHandle == INVALID_HANDLE:
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(_indicatorTimeFrame) + ' CCI squeeze (' + _str(inpCciPeriod) + ',' + _str(inpMaPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if _indicatorTimeFrame != Period():
        result = Arr(1, 0.0, dyn=False)
        if BarsCalculated(_mtfHandle) < 0:
            return prev_calculated
        if CopyBuffer(_mtfHandle, 5, 0, 1, result) != 1:
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
                valh[i] = result[0]
                val[i] = valh[i]
                if CopyBuffer(_mtfHandle, 1, _DT(time[i]), 1, result) <= 0:
                    break
                valhc[i] = result[0]
                valc[i] = valhc[i]
            else:
                valh[i] = valh[i - 1]
                val[i] = valh[i]
                valhc[i] = valhc[i - 1]
                valc[i] = valhc[i]
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
                val[i - k] = val[i] + _fdiv((val[i - n] - val[i]) * k, n)
                valh[i - k] = valh[i] + _fdiv((valh[i - n] - valh[i]) * k, n)
                k += 1
            i += 1
        return i
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        prices[i] = getPrice(inpCciPrice, open, close, high, low, i, rates_total)
        avg = 0.0
        k = 0
        while k < inpCciPeriod and (i - k) >= 0:
            avg += prices[i - k]
            k += 1
        avg = avg / inpCciPeriod
        dev = 0.0
        k = 0
        while k < inpCciPeriod and (i - k) >= 0:
            dev += MathAbs(prices[i - k] - avg)
            k += 1
        dev = dev / inpCciPeriod
        prc = getPrice(inpMaPrice, open, close, high, low, i, rates_total)
        ma = iCustomMa(inpMaMethod, prc, inpMaPeriod, i, rates_total)
        val[i] = (_fdiv(prices[i] - avg, 0.015 * dev) if (dev != 0) else 0)
        if val[i] > 0:
            if prc > ma:
                valc[i] = 0.0
            if prc < ma:
                valc[i] = 1.0
        if val[i] < 0:
            if prc > ma:
                valc[i] = 2.0
            if prc < ma:
                valc[i] = 3.0
        valh[i] = val[i]
        valhc[i] = valc[i]
        i += 1
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    return i

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
    k = 0
    workSma[r][instanceNo + 0] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo + 0]
        k += 1
    return _fdiv(avg, k)

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
    if period <= 1:
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

def getPrice(tprice, open, close, high, low, i, _bars):
    _sw2 = tprice
    if _sw2 == PRICE_CLOSE:
        return close[i]
    elif _sw2 == PRICE_OPEN:
        return open[i]
    elif _sw2 == PRICE_HIGH:
        return high[i]
    elif _sw2 == PRICE_LOW:
        return low[i]
    elif _sw2 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCISqueezeMtf(_MQL5Indicator):
    name = 'CCI  squeeze mtf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=0),  # Time frame
        'inpCciPeriod': 32,  # CCI period
        'inpCciPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # CCI price
        'inpMaPeriod': 200,  # Average period
        'inpMaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=1),  # Average method
        'inpMaPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Average price
        'inpInterpolate': True,  # Interpolate in multi time frame mode?
    }

