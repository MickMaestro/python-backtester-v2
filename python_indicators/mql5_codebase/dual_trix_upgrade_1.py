"""dual_trix_upgrade_1 — converted from MQL5: MQL5 Indicators/Dual Trix UpGrade_1/dual_trix_upgrade_1.mq5

Copyright: Q_IMPORT; Link: mql.shell@gmail.com; Version: 3.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Q_IMPORT', 'link': 'mql.shell@gmail.com', 'version': '3.1', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Plot1', 2: 'Plot2'}, 'levels': [], 'description': [], 'name': 'dual_trix_upgrade_1', 'source': 'MQL5 Indicators/Dual Trix UpGrade_1/dual_trix_upgrade_1.mq5', 'folder': 'Dual Trix UpGrade_1', 'inputs': [{'mql': 'State1', 'py': 'State1', 'param': 'State1', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Plot1', 'py': 'Plot1', 'param': 'Plot1', 'type': 'int', 'default': 15, 'label': 'Period Of The First Plot', 'sinput': False}, {'mql': 'Plot2', 'py': 'Plot2', 'param': 'Plot2', 'type': 'int', 'default': 30, 'label': 'Period Of The Second Plot', 'sinput': False}, {'mql': 'ToClose', 'py': 'ToClose', 'param': 'ToClose', 'type': 'int', 'default': 1, 'label': 'Price Applied To Both Plots', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
State1 = _input('State1', True)
Plot1 = _input('Plot1', 15)  # Period Of The First Plot
Plot2 = _input('Plot2', 30)  # Period Of The Second Plot
ToClose = _input('ToClose', PRICE_CLOSE)  # Price Applied To Both Plots
TriX1 = Arr(0, 0.0)  # Dynamic array to hold the values of Trix
EXT_TriX1 = Arr(0, 0.0)
TriX2 = Arr(0, 0.0)  # Dynamic array to hold the values of Trix
EXT_TriX2 = Arr(0, 0.0)
TriX3 = Arr(0, 0.0)  # Dynamic array to hold the values of Trix Calculations
EXT_TriX3 = Arr(0, 0.0)
TriX4 = Arr(0, 0.0)  # Dynamic array to hold the values of Trix Calculations
EXT_TriX4 = Arr(0, 0.0)
TriXHandle1 = 0  # Buffer to hold Trix 3 Array Access
TriXHandle2 = 0  # Buffer to hold Trix 4 Array Access
window1 = 0
window = 0
objectName = 'Guage1'
objectName1 = 'Guage2'

def OnInit():
    global TriXHandle1, TriXHandle2, window, window1
    SetIndexBuffer(0, TriX1, INDICATOR_DATA)
    SetIndexBuffer(1, TriX2, INDICATOR_DATA)
    SetIndexBuffer(2, TriX3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, TriX4, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(TriX1, True)
    ArraySetAsSeries(TriX2, True)
    ArraySetAsSeries(TriX3, True)
    ArraySetAsSeries(TriX4, True)
    ArrayInitialize(TriX3, EMPTY_VALUE)
    ArrayInitialize(TriX4, EMPTY_VALUE)
    TriXHandle1 = iTriX(Symbol(), 0, Plot1, ToClose)
    TriXHandle2 = iTriX(Symbol(), 0, Plot2, ToClose)
    IndicatorSetInteger(INDICATOR_DIGITS, 6)
    window = ChartWindowFind()
    window1 = ChartWindowFind()
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
    CopyBuffer(TriXHandle1, 0, 0, to_copy, TriX3)
    CopyBuffer(TriXHandle2, 0, 0, to_copy, TriX4)
    ObjectCreate(0, objectName, OBJ_TEXT, window, 0, 0)
    ObjectSetString(0, objectName, OBJPROP_TEXT, DoubleToString(TriX1[to_copy - 1], 6))
    ObjectSetInteger(0, objectName, OBJPROP_COLOR, Red)
    tm = Arr(1, 0, dyn=False)
    CopyTime(Symbol(), Period(), 0, 1, tm)
    ObjectSetInteger(0, objectName, OBJPROP_TIME, tm[0])
    ObjectSetDouble(0, objectName, OBJPROP_PRICE, TriX1[to_copy - 1])
    ObjectCreate(0, objectName1, OBJ_TEXT, window1, 0, 0)
    ObjectSetString(0, objectName1, OBJPROP_TEXT, DoubleToString(TriX2[to_copy - 1], 6))
    ObjectSetInteger(0, objectName1, OBJPROP_COLOR, Blue)
    tm1 = Arr(1, 0, dyn=False)
    CopyTime(Symbol(), Period(), 0, 1, tm1)
    ObjectSetInteger(0, objectName1, OBJPROP_TIME, tm1[0])
    ObjectSetDouble(0, objectName1, OBJPROP_PRICE, TriX2[to_copy - 1])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DualTrixUpgrade1(_MQL5Indicator):
    name = 'dual_trix_upgrade_1'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'State1': True,
        'Plot1': 15,  # Period Of The First Plot
        'Plot2': 30,  # Period Of The Second Plot
        'ToClose': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price Applied To Both Plots
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

