"""VWAP_Custom_Position — converted from MQL5: MQL5 Indicators/VWAP Custom Position/VWAP_Custom_Position.mq5

The indicator VWAP_Custom_Position calculates standard VWAP line, with user defined start point.
The start point is defined by the (movable) ARROW created on chart.
 
VWAP means Volume Weighted Average Price.
Copyright: José Ricardo Magalhães; Link: joserrrm@yahoo.com.br; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'José Ricardo Magalhães', 'link': 'joserrrm@yahoo.com.br', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'VWAP Custom'}, 'levels': [], 'description': ['The indicator VWAP_Custom_Position calculates standard VWAP line, with user defined start point.', 'The start point is defined by the (movable) ARROW created on chart.', ' ', 'VWAP means Volume Weighted Average Price.'], 'name': 'VWAP_Custom_Position', 'source': 'MQL5 Indicators/VWAP Custom Position/VWAP_Custom_Position.mq5', 'folder': 'VWAP Custom Position', 'inputs': [{'mql': 'vwapID', 'py': 'vwapID', 'param': None, 'type': 'string', 'default': '01', 'label': 'VWAP ID  (must be unique)', 'sinput': False}, {'mql': 'Method', 'py': 'Method', 'param': 'Method', 'type': 'int', 'default': 5, 'label': 'Price Calculation Method', 'sinput': False}, {'mql': 'vwapColor', 'py': 'vwapColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'VWAP Color', 'sinput': False}, {'mql': 'arrowSize', 'py': 'arrowSize', 'param': 'arrowSize', 'type': 'int', 'default': 3, 'label': 'Arrow Size', 'sinput': False}, {'mql': 'Anchor', 'py': 'Anchor', 'param': 'Anchor', 'type': 'int', 'default': 0, 'label': 'Arrow Anchor Point', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Fuchsia = 0xFF00FF  # MQL4 colour name

# enum PRICE_METHOD
Close = 0
Open = 1
High = 2
Low = 3
Median = 4
Typical = 5
Weighted = 6
_enum('PRICE_METHOD', {0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted'})

# ---- inputs and global variables
vwapID = _input('vwapID', '01')  # VWAP ID  (must be unique)
Method = _input('Method', Typical)  # Price Calculation Method
arrowSize = _input('arrowSize', 3)  # Arrow Size
Anchor = _input('Anchor', ANCHOR_TOP)  # Arrow Anchor Point
vwapBuffer = Arr(0, 0.0)
startVWAP = 0
Prefix = ""
iRatesTotal = 0
iTime_v = Arr(0, 0)
iOpen_v = Arr(0, 0.0)
iHigh_v = Arr(0, 0.0)
iLow_v = Arr(0, 0.0)
iClose_v = Arr(0, 0.0)
iVolume_v = Arr(0, 0.0)
obj_time = 0
first = True
counter = 0

def OnInit():
    global Prefix
    SetIndexBuffer(0, vwapBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, vwapColor)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    Prefix = 'Obj_' + vwapID
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ArrayInitialize(vwapBuffer, 0.0)
    if reason != REASON_PARAMETERS and reason != REASON_CHARTCHANGE:
        ObjectsDeleteAll(0, Prefix)
        ChartRedraw(0)

def OnChartEvent(id_, lparam, dparam, sparam):
    if sparam == Prefix:
        EventSetMillisecondTimer(100)
    else:
        EventKillTimer()

def OnTimer():
    global obj_time, startVWAP
    obj_time = ObjectGetInteger(0, Prefix, OBJPROP_TIME)
    for i in range(iRatesTotal - 1, 0, -1):
        if obj_time >= iTime_v[i]:
            startVWAP = i
            break
    ArrayInitialize(vwapBuffer, 0.0)
    CalculateVWAP()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global counter, first, iRatesTotal, obj_time, startVWAP
    if first:
        ArrayInitialize(vwapBuffer, 0.0)
        ArrayResize(iTime_v, rates_total, _idiv(rates_total, 2))
        ArrayResize(iOpen_v, rates_total, _idiv(rates_total, 2))
        ArrayResize(iHigh_v, rates_total, _idiv(rates_total, 2))
        ArrayResize(iLow_v, rates_total, _idiv(rates_total, 2))
        ArrayResize(iClose_v, rates_total, _idiv(rates_total, 2))
        ArrayResize(iVolume_v, rates_total, _idiv(rates_total, 2))
    counter = (0 if first else MathMax(prev_calculated - 1, 0))
    for i in range(counter, rates_total):
        iRatesTotal = rates_total
        iTime_v[i] = time[i]
        iOpen_v[i] = open[i]
        iHigh_v[i] = high[i]
        iLow_v[i] = low[i]
        iClose_v[i] = close[i]
        iVolume_v[i] = float(volume[i])
    if ObjectFind(0, Prefix) != 0:
        CreateObject()
    if first:
        CustomizeObject()
        first = False
    obj_time = ObjectGetInteger(0, Prefix, OBJPROP_TIME)
    for i in range(iRatesTotal - 1, 0, -1):
        if obj_time >= iTime_v[i]:
            startVWAP = i
            break
    if vwapBuffer[startVWAP - 1] != 0:
        ArrayInitialize(vwapBuffer, 0.0)
    CalculateVWAP()
    return rates_total

def CalculateVWAP():
    sumPrice = 0.0
    sumVol = 0.0
    i = startVWAP
    while i < iRatesTotal:
        sumPrice += Price(iOpen_v, iHigh_v, iLow_v, iClose_v, i) * iVolume_v[i]
        sumVol += iVolume_v[i]
        vwapBuffer[i] = _fdiv(sumPrice, sumVol)
        i += 1

def Price(open, high, low, close, index):
    output = 0.0
    if Method == Open:
        output = open[index]
    elif Method == High:
        output = high[index]
    elif Method == Low:
        output = low[index]
    elif Method == Median:
        output = (high[index] + low[index]) / 2
    elif Method == Typical:
        output = (high[index] + low[index] + close[index]) / 3
    elif Method == Weighted:
        output = (high[index] + low[index] + close[index] + close[index]) / 4
    else:
        output = close[index]
    return output

def CreateObject():
    offset = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR)) - _idiv(_int(ChartGetInteger(0, CHART_WIDTH_IN_BARS)), 2)
    Hposition = iTime_v[iRatesTotal - offset]
    Vposition = 0.0
    if Anchor == ANCHOR_TOP:
        Vposition = iLow_v[iRatesTotal - offset]
    else:
        Vposition = iHigh_v[iRatesTotal - offset]
    ObjectCreate(0, Prefix, OBJ_ARROW, 0, Hposition, Vposition)
    ObjectSetInteger(0, Prefix, OBJPROP_ARROWCODE, 233)
    ObjectSetInteger(0, Prefix, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, Prefix, OBJPROP_FILL, False)
    ObjectSetInteger(0, Prefix, OBJPROP_BACK, False)
    ObjectSetInteger(0, Prefix, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, Prefix, OBJPROP_SELECTED, True)
    ObjectSetInteger(0, Prefix, OBJPROP_HIDDEN, False)
    ObjectSetInteger(0, Prefix, OBJPROP_ZORDER, 100)
    ObjectSetInteger(0, Prefix, OBJPROP_FILL, True)

def CustomizeObject():
    ObjectSetInteger(0, Prefix, OBJPROP_WIDTH, arrowSize)
    ObjectSetInteger(0, Prefix, OBJPROP_COLOR, vwapColor)
    if Anchor == ANCHOR_TOP:
        ObjectSetInteger(0, Prefix, OBJPROP_ARROWCODE, 233)
    if Anchor == ANCHOR_BOTTOM:
        ObjectSetInteger(0, Prefix, OBJPROP_ARROWCODE, 234)
    ObjectSetInteger(0, Prefix, OBJPROP_ANCHOR, Anchor)

# ---- global variables initialised from expressions
vwapColor = _input('vwapColor', _uint(Fuchsia))  # VWAP Color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VWAPCustomPosition(_MQL5Indicator):
    name = 'VWAP_Custom_Position'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Method': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median Price (HL/2)', 5: 'Typical Price (HLC/3)', 6: 'Weighted Close (HLCC/4)'}, default=5),  # Price Calculation Method
        'arrowSize': 3,  # Arrow Size
        'Anchor': _Choice({0: 'ANCHOR_TOP', 1: 'ANCHOR_BOTTOM'}, default=0),  # Arrow Anchor Point
    }

