"""Average trend (mtf) — converted from MQL5: MQL5 Indicators/Average trend - multi time frame/Average trend (mtf).mq5

average trend
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16748574, 6333684]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Average trend'}, 'levels': [], 'description': ['average trend'], 'name': 'Average trend (mtf)', 'source': 'MQL5 Indicators/Average trend - multi time frame/Average trend (mtf).mq5', 'folder': 'Average trend - multi time frame', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 35, 'label': 'Average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpAcceleration', 'py': 'inpAcceleration', 'param': 'inpAcceleration', 'type': 'double', 'default': 1.05, 'label': 'Acceleration factor', 'sinput': False}, {'mql': 'inpInterpolate', 'py': 'inpInterpolate', 'param': 'inpInterpolate', 'type': 'int', 'default': 1, 'label': 'Interpolation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum enIterpolate
interolate_yes = 1
interolate_no = 0
_enum('enIterpolate', {1: 'interolate_yes', 0: 'interolate_no'})

# ---- inputs and global variables
inpTimeFrame = _input('inpTimeFrame', tf_cu)  # Time frame
inpMaPeriod = _input('inpMaPeriod', 35)  # Average period
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpAcceleration = _input('inpAcceleration', 1.05)  # Acceleration factor
inpInterpolate = _input('inpInterpolate', interolate_yes)  # Interpolation
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
avg = Arr(0, 0.0)
trend = Arr(0, 0.0)
step = Arr(0, 0.0)
count = Arr(0, 0.0)
_maHandle = 0
_mtfHandle = 0
_indicatorTimeFrame = 0
_indicatorName = ""
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _indicatorName, _indicatorTimeFrame, _maHandle, _mtfHandle
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, avg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, step, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, count, INDICATOR_CALCULATIONS)
    _indicatorTimeFrame = MathMax(Period(), timeFrameGet(inpTimeFrame))
    if _indicatorTimeFrame != Period():
        _indicatorName = getIndicatorName()
        _mtfHandle = iCustom(Symbol(), _indicatorTimeFrame, _indicatorName, 0, inpMaPeriod, inpMaMethod, inpPrice, inpAcceleration)
        if not _checkHandle(_mtfHandle, 'Target time frame instance'):
            return INIT_FAILED
    else:
        _maHandle = iMA(Symbol(), 0, inpMaPeriod, 0, inpMaMethod, inpPrice)
        if not _checkHandle(_maHandle, 'average'):
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(_indicatorTimeFrame) + ' average (' + StringSubstr(EnumToString(inpMaMethod, 'ENUM_MA_METHOD'), 5) + ') trend (' + _str(inpMaPeriod) + ',' + _str(inpAcceleration) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if _indicatorTimeFrame != Period():
        result = Arr(1, 0.0, dyn=False)
        if CopyBuffer(_mtfHandle, 5, 0, 1, result) < 1:
            ChartSetSymbolPeriod(0, Symbol(), Period())
            return prev_calculated
        n = 0
        k = 0
        i = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _int(_fdiv(result[0] * float(PeriodSeconds(_indicatorTimeFrame)), PeriodSeconds(Period()))) - 1, 0))
        _prevMark = -99
        _prevTime = 0
        while i < rates_total:
            _currMark = iBarShift(Symbol(), _indicatorTimeFrame, time[i])
            if _currMark < 0:
                i += 1
                continue
            if _currMark != _prevMark:
                _prevMark = _currMark
                _prevTime = time[i]
                if CopyBuffer(_mtfHandle, 0, _currMark, 1, result) < 1:
                    break
                val[i] = result[0]
                if CopyBuffer(_mtfHandle, 1, _currMark, 1, result) < 1:
                    break
                valc[i] = result[0]
            else:
                val[i] = val[i - 1]
                valc[i] = valc[i - 1]
            if not inpInterpolate:
                i += 1
                continue
            _nextMark = (iBarShift(Symbol(), _indicatorTimeFrame, time[i + 1]) if (i < (rates_total - 1)) else (_prevMark + 1))
            if _nextMark == _prevMark:
                i += 1
                continue
            n = 1
            while (i - n) > 0 and time[i - n] >= _prevTime:
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                val[i - k] = val[i] + _fdiv((val[i - n] - val[i]) * k, n)
                k += 1
            i += 1
        return i
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(_maHandle, 0, 0, _copyCount, avg) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if i > 0:
            trend[i] = (1 if (avg[i] > avg[i - 1]) else -1 if (avg[i] < avg[i - 1]) else trend[i - 1])
            step[i] = (0.01 if (trend[i] != trend[i - 1]) else (step[i - 1] * inpAcceleration))
            val[i] = val[i - 1] + (trend[i] * step[i])
        else:
            trend[i] = 0.0
            step[i] = 0.01
            val[i] = 0.0
        valc[i] = (1 if (trend[i] == 1) else 2 if (trend[i] == -1) else 0)
        i += 1
    count[rates_total - 1] = MathMax(i - prev_calculated + 1, 1)
    return i

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
    if period <= 0:
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
    _partsN = StringSplit(_path.v, StringGetCharacter('\\', 0), _partsA)
    name = _partsA[_partsN - 1]
    n = _partsN - 2
    while n >= 0 and _partsA[n] != 'indicators':
        name = _partsA[n] + '\\' + name
        n -= 1
    return name

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__chandles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__chandles, _size + 1)
        _s__checkHandle__chandles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__chandles[i])
        ArrayResize(_s__checkHandle__chandles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- static local variables
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AverageTrendMtf(_MQL5Indicator):
    name = 'Average trend (mtf)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=0),  # Time frame
        'inpMaPeriod': 35,  # Average period
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpAcceleration': 1.05,  # Acceleration factor
        'inpInterpolate': _Choice({1: 'Interpolate data when in multi time frame', 0: 'Do not interpolate data when in multi time frame'}, default=1),  # Interpolation
    }

