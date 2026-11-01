"""Rsi slope divergence — converted from MQL5: MQL5 Indicators/Rsi slope divergence/Rsi slope divergence.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11119017]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Rsi'}, 'levels': [], 'description': [], 'name': 'Rsi slope divergence', 'source': 'MQL5 Indicators/Rsi slope divergence/Rsi slope divergence.mq5', 'folder': 'Rsi slope divergence', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpLrPeriod', 'py': 'inpLrPeriod', 'param': 'inpLrPeriod', 'type': 'int', 'default': 50, 'label': 'Linear regression period', 'sinput': False}, {'mql': 'inpLrWidth', 'py': 'inpLrWidth', 'param': 'inpLrWidth', 'type': 'double', 'default': 2.0, 'label': 'Linear regression channel width', 'sinput': False}, {'mql': 'inpClrDiverging', 'py': 'inpClrDiverging', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color of middle liones when there is divergence', 'sinput': False}, {'mql': 'inpChartLineColor', 'py': 'inpChartLineColor', 'param': None, 'type': 'color', 'default': 11119017, 'label': 'On chart channel color', 'sinput': False}, {'mql': 'inpChartLineMiddleStyle', 'py': 'inpChartLineMiddleStyle', 'param': 'inpChartLineMiddleStyle', 'type': 'int', 'default': 2, 'label': 'On chart channel middle line style', 'sinput': False}, {'mql': 'inpChartLineStyle', 'py': 'inpChartLineStyle', 'param': 'inpChartLineStyle', 'type': 'int', 'default': 0, 'label': 'On chart channel outer lines style', 'sinput': False}, {'mql': 'inpRsiLineColor', 'py': 'inpRsiLineColor', 'param': None, 'type': 'color', 'default': 11119017, 'label': 'On rsi channel color', 'sinput': False}, {'mql': 'inpRsiLineMiddleStyle', 'py': 'inpRsiLineMiddleStyle', 'param': 'inpRsiLineMiddleStyle', 'type': 'int', 'default': 2, 'label': 'On rsi channel middle line style', 'sinput': False}, {'mql': 'inpRsiLineStyle', 'py': 'inpRsiLineStyle', 'param': 'inpRsiLineStyle', 'type': 'int', 'default': 0, 'label': 'On rsi channel outer lines style', 'sinput': False}, {'mql': 'inpUniqueID', 'py': 'inpUniqueID', 'param': None, 'type': 'string', 'default': 'RsiSlopeDiv1', 'label': 'Unique ID for objects', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpLrPeriod = _input('inpLrPeriod', 50)  # Linear regression period
inpLrWidth = _input('inpLrWidth', 2.0)  # Linear regression channel width
inpClrDiverging = _input('inpClrDiverging', clrRed)  # Color of middle liones when there is divergence
inpChartLineColor = _input('inpChartLineColor', clrDarkGray)  # On chart channel color
inpChartLineMiddleStyle = _input('inpChartLineMiddleStyle', STYLE_DOT)  # On chart channel middle line style
inpChartLineStyle = _input('inpChartLineStyle', STYLE_SOLID)  # On chart channel outer lines style
inpRsiLineColor = _input('inpRsiLineColor', clrDarkGray)  # On rsi channel color
inpRsiLineMiddleStyle = _input('inpRsiLineMiddleStyle', STYLE_DOT)  # On rsi channel middle line style
inpRsiLineStyle = _input('inpRsiLineStyle', STYLE_SOLID)  # On rsi channel outer lines style
inpUniqueID = _input('inpUniqueID', 'RsiSlopeDiv1')  # Unique ID for objects
val = Arr(0, 0.0)
prices = Arr(0, 0.0)
ª_rsiHandle = 0
ª_rsiPeriod = 0

def OnInit():
    global ª_rsiHandle, ª_rsiPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, prices, INDICATOR_CALCULATIONS)
    ª_rsiPeriod = (inpPeriod if (inpPeriod > 1) else 1)
    ª_rsiHandle = iRSI(Symbol(), 0, ª_rsiPeriod, inpPrice)
    if not _checkHandle(ª_rsiHandle, 'RSI'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rsi slope divergence (' + _str(ª_rsiPeriod) + ',' + _str(inpLrPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, inpUniqueID + ':')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
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
    window = ChartWindowFind()
    createChannel(window, lrRsi, lrRsi - ((inpLrPeriod - 1.0) * rsiSlope.v), 'rsiLine', inpRsiLineColor, (inpClrDiverging if _isThereDivergence else inpRsiLineColor), inpRsiLineStyle, inpRsiLineMiddleStyle, rsiError.v * inpLrWidth)
    createChannel(0, lrPrc, lrPrc - ((inpLrPeriod - 1.0) * prcSlope.v), 'prcLine', inpChartLineColor, (inpClrDiverging if _isThereDivergence else inpRsiLineColor), inpChartLineStyle, inpChartLineMiddleStyle, prcError.v * inpLrWidth)
    return rates_total

def createChannel(window, price1, price2, addName, theColor, middleColor, theStyle, theMiddleStyle, error):
    name = inpUniqueID + ':' + addName
    if ObjectFind(0, name) == -1:
        ObjectCreate(0, name, OBJ_TREND, window, 0, 0, 0, 0)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price1)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price2)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, iTime(None, Period(), 0))
    ObjectSetInteger(0, name, OBJPROP_TIME, 1, iTime(None, Period(), inpLrPeriod - 1))
    ObjectSetInteger(0, name, OBJPROP_RAY, False)
    ObjectSetInteger(0, name, OBJPROP_COLOR, middleColor)
    ObjectSetInteger(0, name, OBJPROP_STYLE, theMiddleStyle)
    if error <= 0:
        return
    name = inpUniqueID + ':' + addName + 'up'
    if ObjectFind(0, name) == -1:
        ObjectCreate(0, name, OBJ_TREND, window, 0, 0, 0, 0)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price1 + error)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price2 + error)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, iTime(None, Period(), 0))
    ObjectSetInteger(0, name, OBJPROP_TIME, 1, iTime(None, Period(), inpLrPeriod - 1))
    ObjectSetInteger(0, name, OBJPROP_RAY, False)
    ObjectSetInteger(0, name, OBJPROP_COLOR, theColor)
    ObjectSetInteger(0, name, OBJPROP_STYLE, theStyle)
    name = inpUniqueID + ':' + addName + 'down'
    if ObjectFind(0, name) == -1:
        ObjectCreate(0, name, OBJ_TREND, window, 0, 0, 0, 0)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price1 - error)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price2 - error)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, iTime(None, Period(), 0))
    ObjectSetInteger(0, name, OBJPROP_TIME, 1, iTime(None, Period(), inpLrPeriod - 1))
    ObjectSetInteger(0, name, OBJPROP_RAY, False)
    ObjectSetInteger(0, name, OBJPROP_COLOR, theColor)
    ObjectSetInteger(0, name, OBJPROP_STYLE, theStyle)

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


class RsiSlopeDivergence(_MQL5Indicator):
    name = 'Rsi slope divergence'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLrPeriod': 50,  # Linear regression period
        'inpLrWidth': 2.0,  # Linear regression channel width
        'inpChartLineMiddleStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # On chart channel middle line style
        'inpChartLineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # On chart channel outer lines style
        'inpRsiLineMiddleStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # On rsi channel middle line style
        'inpRsiLineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # On rsi channel outer lines style
    }

