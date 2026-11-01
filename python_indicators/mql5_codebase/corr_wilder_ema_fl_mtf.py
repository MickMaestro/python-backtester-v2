"""Corr Wilder EMA (fl)(mtf) — converted from MQL5: MQL5 Indicators/Corrected Wilder's double smoothed ema - multi time frame version/Corr Wilder EMA (fl)(mtf).mq5

Corrected double smoothed Wilder's EMA
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 8, 4: 8}, 'colors': {1: [15132390], 2: [8421504], 3: [12632256, 7451452, 17919], 4: [12632256, 7451452, 17919]}, 'widths': {4: 3}, 'styles': {2: 2}, 'labels': {1: 'Corrected average zone', 2: 'Corrected average middle', 3: 'Corrected average original', 4: 'Corrected average '}, 'levels': [], 'description': ["Corrected double smoothed Wilder's EMA"], 'name': 'Corr Wilder EMA (fl)(mtf)', 'source': "MQL5 Indicators/Corrected Wilder's double smoothed ema - multi time frame version/Corr Wilder EMA (fl)(mtf).mq5", 'folder': "Corrected Wilder's double smoothed ema - multi time frame version", 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Average period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpCorrectionPeriod', 'py': 'inpCorrectionPeriod', 'param': 'inpCorrectionPeriod', 'type': 'int', 'default': 0, 'label': '"Correction" period (<0 no correction,0 to 1 same as average)', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 1, 'label': 'Color change on :', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Period for finding floating levels', 'sinput': False}, {'mql': 'inpFlUp', 'py': 'inpFlUp', 'param': 'inpFlUp', 'type': 'double', 'default': 90.0, 'label': 'Upper level %', 'sinput': False}, {'mql': 'inpFlDown', 'py': 'inpFlDown', 'param': 'inpFlDown', 'type': 'double', 'default': 10.0, 'label': 'Lower level %', 'sinput': False}, {'mql': 'inpInterpolate', 'py': 'inpInterpolate', 'param': 'inpInterpolate', 'type': 'int', 'default': 1, 'label': 'Interpolation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum chgColor
chg_onSlope = 0
chg_onLevel = 1
chg_onMiddle = 2
chg_onOrig = 3
_enum('chgColor', {0: 'chg_onSlope', 1: 'chg_onLevel', 2: 'chg_onMiddle', 3: 'chg_onOrig'})

# enum enIterpolate
interolate_yes = 1
interolate_no = 0
_enum('enIterpolate', {1: 'interolate_yes', 0: 'interolate_no'})

# ---- inputs and global variables
inpTimeFrame = _input('inpTimeFrame', tf_cu)  # Time frame
inpPeriod = _input('inpPeriod', 14)  # Average period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpCorrectionPeriod = _input('inpCorrectionPeriod', 0)  # "Correction" period (<0 no correction,0 to 1 same as average)
inpColorOn = _input('inpColorOn', chg_onLevel)  # Color change on :
inpFlPeriod = _input('inpFlPeriod', 25)  # Period for finding floating levels
inpFlUp = _input('inpFlUp', 90.0)  # Upper level %
inpFlDown = _input('inpFlDown', 10.0)  # Lower level %
inpInterpolate = _input('inpInterpolate', interolate_yes)  # Interpolation
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
mid = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
avg = Arr(0, 0.0)
avgw = Arr(0, 0.0)
avgc = Arr(0, 0.0)
count = Arr(0, 0.0)
_alpha = 0.0
ª_maPeriod = 0
ª_corrPeriod = 0
ª_colorOn = 0
ª_mtfHandle = 0
_indicatorTimeFrame = 0
_indicatorName = ""
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

class sCorrMaStruct(MqlObject):
    _q_fields = ('corrected', 'price', 'price2', 'summ', 'summ2')
    def __init__(self, *args):
        self.corrected = 0.0
        self.price = 0.0
        self.price2 = 0.0
        self.summ = 0.0
        self.summ2 = 0.0

def OnInit():
    global _alpha, _indicatorName, _indicatorTimeFrame, ª_colorOn, ª_corrPeriod, ª_maPeriod, ª_mtfHandle
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, mid, INDICATOR_DATA)
    SetIndexBuffer(3, avg, INDICATOR_DATA)
    SetIndexBuffer(4, avgc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, val, INDICATOR_DATA)
    SetIndexBuffer(6, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, avgw, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, count, INDICATOR_CALCULATIONS)
    _indicatorTimeFrame = MathMax(Period(), timeFrameGet(inpTimeFrame))
    if _indicatorTimeFrame != Period():
        _indicatorName = getIndicatorName()
        ª_mtfHandle = iCustom(Symbol(), _indicatorTimeFrame, _indicatorName, 0, inpPeriod, inpPrice, inpCorrectionPeriod, inpColorOn, inpFlPeriod, inpFlUp, inpFlDown)
        if not _checkHandle(ª_mtfHandle, 'Target time frame instance'):
            return INIT_FAILED
    ª_corrPeriod = (inpCorrectionPeriod if (inpCorrectionPeriod > 0) else 0 if (inpCorrectionPeriod < 0) else inpPeriod)
    ª_colorOn = (inpColorOn if (inpFlPeriod > 1 and ª_corrPeriod > 1) else inpColorOn if (inpColorOn != chg_onOrig) else chg_onSlope)
    ª_maPeriod = (inpPeriod if (inpPeriod > 1) else 1)
    _alpha = _fdiv(1.0, MathSqrt(ª_maPeriod))
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(_indicatorTimeFrame) + ' "Corrected" Wilder\'s EMA (' + _str(inpPeriod) + ',' + _str(inpCorrectionPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    if _indicatorTimeFrame != Period():
        result = Arr(1, 0.0, dyn=False)
        if CopyBuffer(ª_mtfHandle, 8, 0, 1, result) < 0:
            result[0] = rates_total
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
                if CopyBuffer(ª_mtfHandle, 0, _currMark, 1, result) < 1:
                    break
                fup[i] = result[0]
                if CopyBuffer(ª_mtfHandle, 1, _currMark, 1, result) < 1:
                    break
                fdn[i] = result[0]
                if CopyBuffer(ª_mtfHandle, 2, _currMark, 1, result) < 1:
                    break
                mid[i] = result[0]
                if CopyBuffer(ª_mtfHandle, 3, _currMark, 1, result) < 1:
                    break
                avg[i] = result[0]
                if CopyBuffer(ª_mtfHandle, 4, _currMark, 1, result) < 1:
                    break
                avgc[i] = result[0]
                if CopyBuffer(ª_mtfHandle, 5, _currMark, 1, result) < 1:
                    break
                val[i] = result[0]
                if CopyBuffer(ª_mtfHandle, 6, _currMark, 1, result) < 1:
                    break
                valc[i] = result[0]
            else:
                fup[i] = fup[i - 1]
                fdn[i] = fdn[i - 1]
                mid[i] = mid[i - 1]
                avg[i] = avg[i - 1]
                avgc[i] = avgc[i - 1]
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
                fup[i - k] = fup[i] + _fdiv((fup[i - n] - fup[i]) * k, n)
                fdn[i - k] = fdn[i] + _fdiv((fdn[i - n] - fdn[i]) * k, n)
                mid[i - k] = mid[i] + _fdiv((mid[i - n] - mid[i]) * k, n)
                avg[i - k] = avg[i] + _fdiv((avg[i - n] - avg[i]) * k, n)
                val[i - k] = val[i] + _fdiv((val[i - n] - val[i]) * k, n)
                k += 1
            i += 1
        return i
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        if i > 0:
            avgw[i] = avgw[i - 1] + (_alpha * (_price - avgw[i - 1]))
            avg[i] = avg[i - 1] + (_alpha * (avgw[i] - avg[i - 1]))
        else:
            avgw[i] = _price
            avg[i] = avgw[i]
        val[i] = iCorrMa(_price, avg[i], ª_corrPeriod, i, rates_total)
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpFlPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = val[ArrayMaximum(val, start, inpFlPeriod - 1)]
            _s_OnCalculate_prev_min = val[ArrayMinimum(val, start, inpFlPeriod - 1)]
        max_ = (val[i] if (val[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (val[i] if (val[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        range_ = (max_ - min_) / 100.0
        fup[i] = min_ + (inpFlUp * range_)
        fdn[i] = min_ + (inpFlDown * range_)
        mid[i] = min_ + (50.0 * range_)
        avgc[i] = (1 if (avg[i] > val[i]) else 2 if (avg[i] < val[i]) else 0)
        _sw2 = ª_colorOn
        if _sw2 == chg_onOrig:
            valc[i] = avgc[i]
        elif _sw2 == chg_onLevel:
            valc[i] = (1 if (val[i] > fup[i]) else 2 if (val[i] < fdn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        elif _sw2 == chg_onMiddle:
            valc[i] = (1 if (val[i] > mid[i]) else 2 if (val[i] < mid[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        else:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    count[rates_total - 1] = MathMax(i - prev_calculated + 1, 1)
    return i

def iCorrMa(price, average, period, i, bars, instance=0):
    global _s_iCorrMa_m_arraySize
    if _s_iCorrMa_m_arraySize < bars:
        _s_iCorrMa_m_arraySize = ArrayResize(_s_iCorrMa_m_array, bars + 500)
        if _s_iCorrMa_m_arraySize <= bars:
            return 0.0
    _s_iCorrMa_m_array[i][instance].price = price
    _s_iCorrMa_m_array[i][instance].price2 = price * price
    if i > period:
        _s_iCorrMa_m_array[i][instance].summ = _s_iCorrMa_m_array[i - 1][instance].summ + price - _s_iCorrMa_m_array[i - period][instance].price
        _s_iCorrMa_m_array[i][instance].summ2 = _s_iCorrMa_m_array[i - 1][instance].summ2 + _s_iCorrMa_m_array[i][instance].price2 - _s_iCorrMa_m_array[i - period][instance].price2
    else:
        _s_iCorrMa_m_array[i][instance].summ = _s_iCorrMa_m_array[i][instance].price
        _s_iCorrMa_m_array[i][instance].summ2 = _s_iCorrMa_m_array[i][instance].price2
        k = 1
        while k < period and i >= k:
            _s_iCorrMa_m_array[i][instance].summ += _s_iCorrMa_m_array[i - k][instance].price
            _s_iCorrMa_m_array[i][instance].summ2 += _s_iCorrMa_m_array[i - k][instance].price2
            k += 1
    if i > 0:
        v1 = _fdiv(_s_iCorrMa_m_array[i][instance].summ2 - _fdiv(_s_iCorrMa_m_array[i][instance].summ * _s_iCorrMa_m_array[i][instance].summ, float(period)), float(period))
        v2 = (_s_iCorrMa_m_array[i - 1][instance].corrected - average) * (_s_iCorrMa_m_array[i - 1][instance].corrected - average)
        c = (0 if (v2 < v1 or v2 == 0) else (1.0 - _fdiv(v1, v2)))
        _s_iCorrMa_m_array[i][instance].corrected = _s_iCorrMa_m_array[i - 1][instance].corrected + (c * (average - _s_iCorrMa_m_array[i - 1][instance].corrected))
    else:
        _s_iCorrMa_m_array[i][instance].corrected = average
    return _s_iCorrMa_m_array[i][instance].corrected

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
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0
_s_iCorrMa_m_array = Arr(0, 0, factory=sCorrMaStruct, dims=(1,))
_s_iCorrMa_m_arraySize = 0
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrWilderEMAFlMtf(_MQL5Indicator):
    name = 'Corr Wilder EMA (fl)(mtf)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=0),  # Time frame
        'inpPeriod': 14,  # Average period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpCorrectionPeriod': 0,  # "Correction" period (<0 no correction,0 to 1 same as average)
        'inpColorOn': _Choice({0: 'change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross', 3: 'Change color on average value cross'}, default=1),  # Color change on :
        'inpFlPeriod': 25,  # Period for finding floating levels
        'inpFlUp': 90.0,  # Upper level %
        'inpFlDown': 10.0,  # Lower level %
        'inpInterpolate': _Choice({1: 'Interpolate data when in multi time frame', 0: 'Do not interpolate data when in multi time frame'}, default=1),  # Interpolation
    }

