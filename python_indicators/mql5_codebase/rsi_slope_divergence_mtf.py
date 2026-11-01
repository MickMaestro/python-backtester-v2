"""Rsi slope divergence (mtf) — converted from MQL5: MQL5 Indicators/RSI slope divergence - multi time frame version/Rsi slope divergence (mtf).mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11119017]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Rsi'}, 'levels': [], 'description': [], 'name': 'Rsi slope divergence (mtf)', 'source': 'MQL5 Indicators/RSI slope divergence - multi time frame version/Rsi slope divergence (mtf).mq5', 'folder': 'RSI slope divergence - multi time frame version', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpLrPeriod', 'py': 'inpLrPeriod', 'param': 'inpLrPeriod', 'type': 'int', 'default': 50, 'label': 'Linear regression period', 'sinput': False}, {'mql': 'inpLrWidth', 'py': 'inpLrWidth', 'param': 'inpLrWidth', 'type': 'double', 'default': 2.0, 'label': 'Linear regression channel width', 'sinput': False}, {'mql': 'inpClrDiverging', 'py': 'inpClrDiverging', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color of middle liones when there is divergence', 'sinput': False}, {'mql': 'inpChartLineColor', 'py': 'inpChartLineColor', 'param': None, 'type': 'color', 'default': 11119017, 'label': 'On chart channel color', 'sinput': False}, {'mql': 'inpChartBackColor', 'py': 'inpChartBackColor', 'param': None, 'type': 'color', 'default': 14474460, 'label': 'On chart channel back color', 'sinput': False}, {'mql': 'inpChartLineMiddleStyle', 'py': 'inpChartLineMiddleStyle', 'param': 'inpChartLineMiddleStyle', 'type': 'int', 'default': 2, 'label': 'On chart channel middle line style', 'sinput': False}, {'mql': 'inpChartLineStyle', 'py': 'inpChartLineStyle', 'param': 'inpChartLineStyle', 'type': 'int', 'default': 0, 'label': 'On chart channel outer lines style', 'sinput': False}, {'mql': 'inpRsiLineColor', 'py': 'inpRsiLineColor', 'param': None, 'type': 'color', 'default': 11119017, 'label': 'On rsi channel color', 'sinput': False}, {'mql': 'inpRsiBackColor', 'py': 'inpRsiBackColor', 'param': None, 'type': 'color', 'default': 14474460, 'label': 'On rsi channel back color', 'sinput': False}, {'mql': 'inpRsiLineMiddleStyle', 'py': 'inpRsiLineMiddleStyle', 'param': 'inpRsiLineMiddleStyle', 'type': 'int', 'default': 2, 'label': 'On rsi channel middle line style', 'sinput': False}, {'mql': 'inpRsiLineStyle', 'py': 'inpRsiLineStyle', 'param': 'inpRsiLineStyle', 'type': 'int', 'default': 0, 'label': 'On rsi channel outer lines style', 'sinput': False}, {'mql': 'inpUniqueID', 'py': 'inpUniqueID', 'param': None, 'type': 'string', 'default': 'RsiSlopeDiv1', 'label': 'Unique ID for objects', 'sinput': False}, {'mql': 'inpInterpolate', 'py': 'inpInterpolate', 'param': 'inpInterpolate', 'type': 'int', 'default': 1, 'label': 'Interpolation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
inpPeriod = _input('inpPeriod', 14)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpLrPeriod = _input('inpLrPeriod', 50)  # Linear regression period
inpLrWidth = _input('inpLrWidth', 2.0)  # Linear regression channel width
inpClrDiverging = _input('inpClrDiverging', clrRed)  # Color of middle liones when there is divergence
inpChartLineColor = _input('inpChartLineColor', clrDarkGray)  # On chart channel color
inpChartBackColor = _input('inpChartBackColor', clrGainsboro)  # On chart channel back color
inpChartLineMiddleStyle = _input('inpChartLineMiddleStyle', STYLE_DOT)  # On chart channel middle line style
inpChartLineStyle = _input('inpChartLineStyle', STYLE_SOLID)  # On chart channel outer lines style
inpRsiLineColor = _input('inpRsiLineColor', clrDarkGray)  # On rsi channel color
inpRsiBackColor = _input('inpRsiBackColor', clrGainsboro)  # On rsi channel back color
inpRsiLineMiddleStyle = _input('inpRsiLineMiddleStyle', STYLE_DOT)  # On rsi channel middle line style
inpRsiLineStyle = _input('inpRsiLineStyle', STYLE_SOLID)  # On rsi channel outer lines style
inpUniqueID = _input('inpUniqueID', 'RsiSlopeDiv1')  # Unique ID for objects
inpInterpolate = _input('inpInterpolate', interolate_yes)  # Interpolation
val = Arr(0, 0.0)
prices = Arr(0, 0.0)
count = Arr(0, 0.0)
ª_rsiHandle = 0
ª_rsiPeriod = 0
ª_mtfHandle = 0
_indicatorTimeFrame = 0
_indicatorName = ""
_indicatorShortName = ""
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _indicatorName, _indicatorShortName, _indicatorTimeFrame, ª_mtfHandle, ª_rsiHandle, ª_rsiPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, count, INDICATOR_CALCULATIONS)
    _indicatorTimeFrame = MathMax(Period(), timeFrameGet(inpTimeFrame))
    if _indicatorTimeFrame != Period():
        _indicatorName = getIndicatorName()
        ª_mtfHandle = iCustom(Symbol(), _indicatorTimeFrame, _indicatorName, 0, inpPeriod, inpPrice, inpLrPeriod, inpLrWidth, inpClrDiverging, inpChartLineColor, inpChartBackColor, inpChartLineMiddleStyle, inpChartLineStyle, inpRsiLineColor, inpRsiBackColor, inpRsiLineMiddleStyle, inpRsiLineStyle, inpUniqueID)
        if not _checkHandle(ª_mtfHandle, 'Target ' + timeFrameToString(_indicatorTimeFrame) + ' time frame instance'):
            return INIT_FAILED
    ª_rsiPeriod = (inpPeriod if (inpPeriod > 1) else 1)
    ª_rsiHandle = iRSI(Symbol(), 0, ª_rsiPeriod, inpPrice)
    if not _checkHandle(ª_rsiHandle, 'RSI'):
        return INIT_FAILED
    _indicatorShortName = '(' + inpUniqueID + ') ' + timeFrameToString(_indicatorTimeFrame) + ' Rsi slope divergence (' + _str(ª_rsiPeriod) + ',' + _str(inpLrPeriod) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, _indicatorShortName)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, inpUniqueID + ':')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if _indicatorTimeFrame != Period():
        result = Arr(1, 0.0, dyn=False)
        if CopyBuffer(ª_mtfHandle, 2, 0, 1, result) < 0:
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
                val[i] = result[0]
            else:
                val[i] = val[i - 1]
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
    if CopyBuffer(ª_rsiHandle, 0, 0, _copyCount, val) != _copyCount:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            prices[i] = close[i]
        elif _sw1 == PRICE_OPEN:
            prices[i] = open[i]
        elif _sw1 == PRICE_HIGH:
            prices[i] = high[i]
        elif _sw1 == PRICE_LOW:
            prices[i] = low[i]
        elif _sw1 == PRICE_MEDIAN:
            prices[i] = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            prices[i] = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            prices[i] = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            prices[i] = 0.0
        i += 1
    rsiError = Box(0.0)
    rsiSlope = Box(0.0)
    lrRsi = iLrValue(val, inpLrPeriod, rsiSlope, rsiError, rates_total - 1)
    prcError = Box(0.0)
    prcSlope = Box(0.0)
    lrPrc = iLrValue(prices, inpLrPeriod, prcSlope, prcError, rates_total - 1)
    _isThereDivergence = (rsiSlope.v * prcSlope.v) < 0
    window = ChartWindowFind(0, _indicatorShortName)
    createChannel(window, lrRsi, lrRsi - ((inpLrPeriod - 1.0) * rsiSlope.v), 'rsiLine', inpRsiLineColor, (inpClrDiverging if _isThereDivergence else inpRsiLineColor), inpRsiLineStyle, inpRsiLineMiddleStyle, inpRsiBackColor, rsiError.v * inpLrWidth)
    createChannel(0, lrPrc, lrPrc - ((inpLrPeriod - 1.0) * prcSlope.v), 'prcLine', inpChartLineColor, (inpClrDiverging if _isThereDivergence else inpRsiLineColor), inpChartLineStyle, inpChartLineMiddleStyle, inpChartBackColor, prcError.v * inpLrWidth)
    count[rates_total - 1] = MathMax(i - prev_calculated + 1, 1)
    return rates_total

def createChannel(window, price1, price2, addName, theColor, middleColor, theStyle, theMiddleStyle, backColor, error):
    name = inpUniqueID + ':' + addName
    if ObjectFind(0, name) == -1:
        ObjectCreate(0, name, OBJ_TREND, window, 0, 0, 0, 0)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price1)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price2)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, iTime(None, Period(), 0) + PeriodSeconds(Period()) - 1)
    ObjectSetInteger(0, name, OBJPROP_TIME, 1, iTime(None, Period(), inpLrPeriod - 1))
    ObjectSetInteger(0, name, OBJPROP_RAY, False)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_COLOR, middleColor)
    ObjectSetInteger(0, name, OBJPROP_STYLE, theMiddleStyle)
    if error <= 0:
        return
    name = inpUniqueID + ':' + addName + 'up'
    if ObjectFind(0, name) == -1:
        ObjectCreate(0, name, OBJ_TREND, window, 0, 0, 0, 0)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price1 + error)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price2 + error)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, iTime(None, Period(), 0) + PeriodSeconds(Period()) - 1)
    ObjectSetInteger(0, name, OBJPROP_TIME, 1, iTime(None, Period(), inpLrPeriod - 1))
    ObjectSetInteger(0, name, OBJPROP_RAY, False)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_COLOR, theColor)
    ObjectSetInteger(0, name, OBJPROP_STYLE, theStyle)
    name = inpUniqueID + ':' + addName + 'down'
    if ObjectFind(0, name) == -1:
        ObjectCreate(0, name, OBJ_TREND, window, 0, 0, 0, 0)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price1 - error)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price2 - error)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, iTime(None, Period(), 0) + PeriodSeconds(Period()) - 1)
    ObjectSetInteger(0, name, OBJPROP_TIME, 1, iTime(None, Period(), inpLrPeriod - 1))
    ObjectSetInteger(0, name, OBJPROP_RAY, False)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_COLOR, theColor)
    ObjectSetInteger(0, name, OBJPROP_STYLE, theStyle)
    if backColor != clrNONE:
        name = inpUniqueID + ':' + addName + 'tup'
        if ObjectFind(0, name) == -1:
            ObjectCreate(0, name, OBJ_TRIANGLE, window, 0, 0, 0, 0)
        ObjectSetInteger(0, name, OBJPROP_TIME, 0, iTime(None, Period(), 0) + PeriodSeconds(Period()) - 1)
        ObjectSetInteger(0, name, OBJPROP_TIME, 1, iTime(None, Period(), 0) + PeriodSeconds(Period()) - 1)
        ObjectSetInteger(0, name, OBJPROP_TIME, 2, iTime(None, Period(), inpLrPeriod - 1))
        ObjectSetInteger(0, name, OBJPROP_COLOR, backColor)
        ObjectSetInteger(0, name, OBJPROP_BACK, True)
        ObjectSetInteger(0, name, OBJPROP_FILL, True)
        ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
        ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
        ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price1 + error)
        ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price1 - error)
        ObjectSetDouble(0, name, OBJPROP_PRICE, 2, price2 - error)
        name = inpUniqueID + ':' + addName + 'tdn'
        if ObjectFind(0, name) == -1:
            ObjectCreate(0, name, OBJ_TRIANGLE, window, 0, 0, 0, 0)
        ObjectSetInteger(0, name, OBJPROP_TIME, 0, iTime(None, Period(), 0) + PeriodSeconds(Period()) - 1)
        ObjectSetInteger(0, name, OBJPROP_TIME, 1, iTime(None, Period(), inpLrPeriod - 1))
        ObjectSetInteger(0, name, OBJPROP_TIME, 2, iTime(None, Period(), inpLrPeriod - 1))
        ObjectSetInteger(0, name, OBJPROP_COLOR, backColor)
        ObjectSetInteger(0, name, OBJPROP_BACK, True)
        ObjectSetInteger(0, name, OBJPROP_FILL, True)
        ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
        ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
        ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price1 + error)
        ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price2 - error)
        ObjectSetDouble(0, name, OBJPROP_PRICE, 2, price2 + error)

def iLrValue(values, period, slope, error, i):
    sumx = 0.0
    sumxx = 0.0
    sumxy = 0.0
    sumy = 0.0
    sumyy = 0.0
    k = 0
    while k < period and i >= k:
        price = values[i - k]
        sumx += k
        sumxx += k * k
        sumxy += k * price
        sumy += price
        sumyy += price * price
        k += 1
    slope.v = _fdiv((period * sumxy) - (sumx * sumy), (sumx * sumx) - (period * sumxx))
    error.v = MathSqrt(_fdiv((period * sumyy) - (sumy * sumy) - (slope.v * slope.v * ((period * sumxx) - (sumx * sumx))), period * (period - 2)))
    return _fdiv(sumy + (slope.v * sumx), period)

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


class RsiSlopeDivergenceMtf(_MQL5Indicator):
    name = 'Rsi slope divergence (mtf)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=0),  # Time frame
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLrPeriod': 50,  # Linear regression period
        'inpLrWidth': 2.0,  # Linear regression channel width
        'inpChartLineMiddleStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # On chart channel middle line style
        'inpChartLineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # On chart channel outer lines style
        'inpRsiLineMiddleStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # On rsi channel middle line style
        'inpRsiLineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # On rsi channel outer lines style
        'inpInterpolate': _Choice({1: 'Interpolate data when in multi time frame', 0: 'Do not interpolate data when in multi time frame'}, default=1),  # Interpolation
    }

