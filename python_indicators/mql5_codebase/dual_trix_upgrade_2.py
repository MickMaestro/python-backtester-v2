"""dual_trix_upgrade_2 — converted from MQL5: MQL5 Indicators/Dual_Trix_Upgrade2/dual_trix_upgrade_2.mq5

Copyright: Q_IMPORT; Version: 4.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Q_IMPORT', 'version': '4.1', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [255], 2: [16711680], 3: [255], 4: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Plot1', 2: 'Plot2', 3: 'Plot3', 4: 'Plot4'}, 'levels': [], 'description': [], 'name': 'dual_trix_upgrade_2', 'source': 'MQL5 Indicators/Dual_Trix_Upgrade2/dual_trix_upgrade_2.mq5', 'folder': 'Dual_Trix_Upgrade2', 'inputs': [{'mql': 'seperator1', 'py': 'seperator1', 'param': None, 'type': 'string', 'default': '*--Indicator Settings--*', 'label': '', 'sinput': False}, {'mql': 'State1', 'py': 'State1', 'param': 'State1', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'seperator2', 'py': 'seperator2', 'param': None, 'type': 'string', 'default': '*--Periods--*', 'label': '', 'sinput': False}, {'mql': 'Plot1', 'py': 'Plot1', 'param': 'Plot1', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'Plot2', 'py': 'Plot2', 'param': 'Plot2', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'seperator3', 'py': 'seperator3', 'param': None, 'type': 'string', 'default': 'Indicator_Coordinates_Fast', 'label': '', 'sinput': False}, {'mql': 'XCord_Indicator_Value_Fast', 'py': 'XCord_Indicator_Value_Fast', 'param': 'XCord_Indicator_Value_Fast', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'YCord_Indicator_Value_Fast', 'py': 'YCord_Indicator_Value_Fast', 'param': 'YCord_Indicator_Value_Fast', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'seperator4', 'py': 'seperator4', 'param': None, 'type': 'string', 'default': 'Indicator_Coordinates_Slow', 'label': '', 'sinput': False}, {'mql': 'XCord_Indicator_Slow', 'py': 'XCord_Indicator_Slow', 'param': 'XCord_Indicator_Slow', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'YCord_Indicator_Slow', 'py': 'YCord_Indicator_Slow', 'param': 'YCord_Indicator_Slow', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'seperator5', 'py': 'seperator5', 'param': None, 'type': 'string', 'default': '*--Chart_Coordinates Fast--*', 'label': '', 'sinput': False}, {'mql': 'XCord_Chart_Value_Fast', 'py': 'XCord_Chart_Value_Fast', 'param': 'XCord_Chart_Value_Fast', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'YCord_Chart_Value_Fast', 'py': 'YCord_Chart_Value_Fast', 'param': 'YCord_Chart_Value_Fast', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'seperator6', 'py': 'seperator6', 'param': None, 'type': 'string', 'default': '*--Chart_Coordinates Slow--*', 'label': '', 'sinput': False}, {'mql': 'XCord_Chart_Slow', 'py': 'XCord_Chart_Slow', 'param': 'XCord_Chart_Slow', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'YCord_Chart_Slow', 'py': 'YCord_Chart_Slow', 'param': 'YCord_Chart_Slow', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'seperator7', 'py': 'seperator7', 'param': None, 'type': 'string', 'default': '*--Period_Coordinates Fast--*', 'label': '', 'sinput': False}, {'mql': 'XCord_Chart_Period_Fast', 'py': 'XCord_Chart_Period_Fast', 'param': 'XCord_Chart_Period_Fast', 'type': 'int', 'default': 60, 'label': '', 'sinput': False}, {'mql': 'YCord_Chart_Period_Fast', 'py': 'YCord_Chart_Period_Fast', 'param': 'YCord_Chart_Period_Fast', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'seperator8', 'py': 'seperator8', 'param': None, 'type': 'string', 'default': '*--Period_Coordinates_Slow--*', 'label': '', 'sinput': False}, {'mql': 'XCord_Chart_Period_Slow', 'py': 'XCord_Chart_Period_Slow', 'param': 'XCord_Chart_Period_Slow', 'type': 'int', 'default': 60, 'label': '', 'sinput': False}, {'mql': 'YCord_Chart_Period_Slow', 'py': 'YCord_Chart_Period_Slow', 'param': 'YCord_Chart_Period_Slow', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'ToClose', 'py': 'ToClose', 'param': 'ToClose', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
White = 0xFFFFFF  # MQL4 colour name

# ---- inputs and global variables
seperator1 = _input('seperator1', '*--Indicator Settings--*')
State1 = _input('State1', True)
seperator2 = _input('seperator2', '*--Periods--*')
Plot1 = _input('Plot1', 15)
Plot2 = _input('Plot2', 30)
seperator3 = _input('seperator3', 'Indicator_Coordinates_Fast')
XCord_Indicator_Value_Fast = _input('XCord_Indicator_Value_Fast', 0)
YCord_Indicator_Value_Fast = _input('YCord_Indicator_Value_Fast', 0)
seperator4 = _input('seperator4', 'Indicator_Coordinates_Slow')
XCord_Indicator_Slow = _input('XCord_Indicator_Slow', 0)
YCord_Indicator_Slow = _input('YCord_Indicator_Slow', 20)
seperator5 = _input('seperator5', '*--Chart_Coordinates Fast--*')
XCord_Chart_Value_Fast = _input('XCord_Chart_Value_Fast', 0)
YCord_Chart_Value_Fast = _input('YCord_Chart_Value_Fast', 0)
seperator6 = _input('seperator6', '*--Chart_Coordinates Slow--*')
XCord_Chart_Slow = _input('XCord_Chart_Slow', 0)
YCord_Chart_Slow = _input('YCord_Chart_Slow', 20)
seperator7 = _input('seperator7', '*--Period_Coordinates Fast--*')
XCord_Chart_Period_Fast = _input('XCord_Chart_Period_Fast', 60)
YCord_Chart_Period_Fast = _input('YCord_Chart_Period_Fast', 0)
seperator8 = _input('seperator8', '*--Period_Coordinates_Slow--*')
XCord_Chart_Period_Slow = _input('XCord_Chart_Period_Slow', 60)
YCord_Chart_Period_Slow = _input('YCord_Chart_Period_Slow', 20)
ToClose = _input('ToClose', PRICE_CLOSE)
TriX1 = Arr(0, 0.0)
TriX2 = Arr(0, 0.0)
TriX3 = Arr(0, 0.0)
TriX4 = Arr(0, 0.0)
TriXHandle1 = 0
TriXHandle2 = 0
TriXHandle3 = 0
TriXHandle4 = 0
window1 = 0
objectName = 'Guage1'
slowchart = 'Guage_slow_chart'
objectName1 = 'Guage2'
fastchart = 'Guage_fast_chart'
objectName2 = 'Guage3'
objectName3 = 'Guage4'
slowind = 'Guage_slow_ind'
fastind = 'Guage_slow_ind'

def OnInit():
    global TriXHandle1, TriXHandle2, TriXHandle3, TriXHandle4
    SetIndexBuffer(0, TriX1, INDICATOR_DATA)
    SetIndexBuffer(1, TriX2, INDICATOR_DATA)
    SetIndexBuffer(2, TriX3, INDICATOR_DATA)
    SetIndexBuffer(3, TriX4, INDICATOR_DATA)
    ArraySetAsSeries(TriX1, True)
    ArraySetAsSeries(TriX2, True)
    ArraySetAsSeries(TriX3, True)
    ArraySetAsSeries(TriX4, True)
    TriXHandle1 = iTriX(Symbol(), 0, Plot1, ToClose)
    TriXHandle2 = iTriX(Symbol(), 0, Plot2, ToClose)
    TriXHandle3 = iTriX(Symbol(), 0, Plot2, ToClose)
    TriXHandle4 = iTriX(Symbol(), 0, Plot1, ToClose)
    IndicatorSetInteger(INDICATOR_DIGITS, 6)
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    i = 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        to_copy += 1
    CopyBuffer(TriXHandle1, 0, 0, to_copy, TriX1)
    CopyBuffer(TriXHandle2, 0, 0, to_copy, TriX2)
    CopyBuffer(TriXHandle3, 0, 0, to_copy, TriX3)
    CopyBuffer(TriXHandle4, 0, 0, to_copy, TriX4)
    ObjectCreate(0, slowchart, OBJ_LABEL, 0, 0, 0)
    ObjectSetString(0, slowchart, OBJPROP_TEXT, '' + IntegerToString(Plot1))
    ObjectSetInteger(0, slowchart, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(0, slowchart, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
    ObjectSetInteger(0, slowchart, OBJPROP_XDISTANCE, XCord_Chart_Period_Fast)
    ObjectSetInteger(0, slowchart, OBJPROP_YDISTANCE, YCord_Chart_Period_Fast)
    ObjectSetInteger(0, slowchart, OBJPROP_COLOR, White)
    ObjectSetString(0, slowchart, OBJPROP_FONT, 'Impact')
    ObjectSetInteger(0, slowchart, OBJPROP_FONTSIZE, 10)
    ObjectCreate(0, fastchart, OBJ_LABEL, 0, 0, 0)
    ObjectSetString(0, fastchart, OBJPROP_TEXT, '' + IntegerToString(Plot2))
    ObjectSetInteger(0, fastchart, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(0, fastchart, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
    ObjectSetInteger(0, fastchart, OBJPROP_XDISTANCE, XCord_Chart_Period_Slow)
    ObjectSetInteger(0, fastchart, OBJPROP_YDISTANCE, YCord_Chart_Period_Slow)
    ObjectSetInteger(0, fastchart, OBJPROP_COLOR, White)
    ObjectSetString(0, fastchart, OBJPROP_FONT, 'Impact')
    ObjectSetInteger(0, fastchart, OBJPROP_FONTSIZE, 10)
    ObjectCreate(0, objectName3, OBJ_LABEL, 0, 0, 0)
    ObjectSetString(0, objectName3, OBJPROP_TEXT, DoubleToString(TriX4[to_copy - 1], 6))
    ObjectSetInteger(0, objectName3, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(0, objectName3, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
    ObjectSetInteger(0, objectName3, OBJPROP_XDISTANCE, XCord_Chart_Value_Fast)
    ObjectSetInteger(0, objectName3, OBJPROP_YDISTANCE, YCord_Chart_Value_Fast)
    ObjectSetInteger(0, objectName3, OBJPROP_COLOR, Red)
    ObjectSetString(0, objectName3, OBJPROP_FONT, 'Impact')
    ObjectSetInteger(0, objectName3, OBJPROP_FONTSIZE, 10)
    tm2 = Arr(1, 0, dyn=False)
    CopyTime(Symbol(), Period(), 0, 1, tm2)
    ObjectSetInteger(0, objectName3, OBJPROP_TIME, tm2[0])
    ObjectSetDouble(0, objectName3, OBJPROP_PRICE, TriX4[to_copy - 1])
    ObjectCreate(0, objectName, OBJ_LABEL, 0, 0, 0)
    ObjectSetString(0, objectName, OBJPROP_TEXT, DoubleToString(TriX3[to_copy - 1], 6))
    ObjectSetInteger(0, objectName, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(0, objectName, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
    ObjectSetInteger(0, objectName, OBJPROP_XDISTANCE, XCord_Chart_Slow)
    ObjectSetInteger(0, objectName, OBJPROP_YDISTANCE, YCord_Chart_Slow)
    ObjectSetInteger(0, objectName, OBJPROP_COLOR, Blue)
    ObjectSetString(0, objectName, OBJPROP_FONT, 'Impact')
    ObjectSetInteger(0, objectName, OBJPROP_FONTSIZE, 10)
    tm = Arr(1, 0, dyn=False)
    CopyTime(Symbol(), Period(), 0, 1, tm)
    ObjectSetInteger(0, objectName, OBJPROP_TIME, tm[0])
    ObjectSetDouble(0, objectName, OBJPROP_PRICE, TriX3[to_copy - 1])
    ObjectCreate(0, objectName2, OBJ_LABEL, 1, 0, 0)
    ObjectSetString(0, objectName2, OBJPROP_TEXT, DoubleToString(TriX2[to_copy - 1], 6))
    ObjectSetInteger(0, objectName2, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(0, objectName2, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
    ObjectSetInteger(0, objectName2, OBJPROP_XDISTANCE, XCord_Indicator_Slow)
    ObjectSetInteger(0, objectName2, OBJPROP_YDISTANCE, YCord_Indicator_Slow)
    ObjectSetInteger(0, objectName2, OBJPROP_COLOR, Blue)
    ObjectSetString(0, objectName2, OBJPROP_FONT, 'Impact')
    ObjectSetInteger(0, objectName2, OBJPROP_FONTSIZE, 10)
    tm1 = Arr(1, 0, dyn=False)
    CopyTime(Symbol(), Period(), 0, 1, tm1)
    ObjectSetInteger(0, objectName2, OBJPROP_TIME, tm1[0])
    ObjectSetDouble(0, objectName2, OBJPROP_PRICE, TriX2[to_copy - 1])
    ObjectCreate(0, objectName1, OBJ_LABEL, 1, 0, 0)
    ObjectSetString(0, objectName1, OBJPROP_TEXT, DoubleToString(TriX1[to_copy - 1], 6))
    ObjectSetInteger(0, objectName1, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(0, objectName1, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
    ObjectSetInteger(0, objectName1, OBJPROP_XDISTANCE, XCord_Indicator_Value_Fast)
    ObjectSetInteger(0, objectName1, OBJPROP_YDISTANCE, YCord_Indicator_Value_Fast)
    ObjectSetInteger(0, objectName1, OBJPROP_COLOR, Red)
    ObjectSetString(0, objectName1, OBJPROP_FONT, 'Impact')
    ObjectSetInteger(0, objectName1, OBJPROP_FONTSIZE, 10)
    tm3 = Arr(1, 0, dyn=False)
    CopyTime(Symbol(), Period(), 0, 1, tm3)
    ObjectSetInteger(0, objectName1, OBJPROP_TIME, tm3[0])
    ObjectSetDouble(0, objectName1, OBJPROP_PRICE, TriX1[to_copy - 1])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DualTrixUpgrade2(_MQL5Indicator):
    name = 'dual_trix_upgrade_2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'State1': True,
        'Plot1': 15,
        'Plot2': 30,
        'XCord_Indicator_Value_Fast': 0,
        'YCord_Indicator_Value_Fast': 0,
        'XCord_Indicator_Slow': 0,
        'YCord_Indicator_Slow': 20,
        'XCord_Chart_Value_Fast': 0,
        'YCord_Chart_Value_Fast': 0,
        'XCord_Chart_Slow': 0,
        'YCord_Chart_Slow': 20,
        'XCord_Chart_Period_Fast': 60,
        'YCord_Chart_Period_Fast': 0,
        'XCord_Chart_Period_Slow': 60,
        'YCord_Chart_Period_Slow': 20,
        'ToClose': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

