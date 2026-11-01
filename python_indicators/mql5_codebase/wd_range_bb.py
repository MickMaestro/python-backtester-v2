"""wd.Range_BB — converted from MQL5: MQL5 Indicators/wd.Range_BB/wd.Range_BB.mq5

Provides Bollinger Bands, calculating the range bandwidth as the difference in pips between the upper and lower Bands.
Bollinger Bands appearance and behavior can be tailored by adjusting period, shift, deviation, and applied price, along with color and line style.
The 'range/bandwidth information' label can be placed in the specified Sub-Window, allowing customization of label positions.
Overall, this indicator helps traders visualize market flexibility and volatility based on Bollinger Bands' width.
Copyright: Copyright © 2024, Karya Prima Rajasa Mediavestama.; Link: https://www.mql5.com/en/code/48013; Version: 2.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2024, Karya Prima Rajasa Mediavestama.', 'link': 'https://www.mql5.com/en/code/48013', 'version': '2.24', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [7451452], 2: [7451452], 3: [7451452]}, 'widths': {1: 1, 2: 2, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'UpperBB', 2: 'MidBB', 3: 'LowerBB'}, 'levels': [], 'description': ['Provides Bollinger Bands, calculating the range bandwidth as the difference in pips between the upper and lower Bands.', 'Bollinger Bands appearance and behavior can be tailored by adjusting period, shift, deviation, and applied price, along with color and line style.', "The 'range/bandwidth information' label can be placed in the specified Sub-Window, allowing customization of label positions.", "Overall, this indicator helps traders visualize market flexibility and volatility based on Bollinger Bands' width."], 'name': 'wd.Range_BB', 'source': 'MQL5 Indicators/wd.Range_BB/wd.Range_BB.mq5', 'folder': 'wd.Range_BB', 'inputs': [{'mql': 'Comment1', 'py': 'Comment1', 'param': None, 'type': 'string', 'default': '===== Bollinger Bands Settings =======', 'label': '=======================', 'sinput': False}, {'mql': 'BB_period', 'py': 'BB_period', 'param': 'BB_period', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'BB_shift', 'py': 'BB_shift', 'param': 'BB_shift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 2.0, 'label': 'Deviations', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 1, 'label': 'Apply to', 'sinput': False}, {'mql': 'Comment2', 'py': 'Comment2', 'param': None, 'type': 'string', 'default': '===== Range/Bandwidth Settings ======', 'label': '========================', 'sinput': False}, {'mql': 'InfoColor', 'py': 'InfoColor', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Font color', 'sinput': False}, {'mql': 'InfoSize', 'py': 'InfoSize', 'param': 'InfoSize', 'type': 'int', 'default': 7, 'label': 'Font size', 'sinput': False}, {'mql': 'SubWindow', 'py': 'SubWindow', 'param': 'SubWindow', 'type': 'int', 'default': 0, 'label': 'Sub-Window placement', 'sinput': False}, {'mql': 'XDist', 'py': 'XDist', 'param': 'XDist', 'type': 'int', 'default': 4, 'label': 'X-Position label', 'sinput': False}, {'mql': 'YDist', 'py': 'YDist', 'param': 'YDist', 'type': 'int', 'default': 12, 'label': 'Y-Position label', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Comment1 = _input('Comment1', '===== Bollinger Bands Settings =======')  # =======================
BB_period = _input('BB_period', 20)  # Period
BB_shift = _input('BB_shift', 0)  # Shift
Deviation = _input('Deviation', 2.0)  # Deviations
Applied_price = _input('Applied_price', PRICE_CLOSE)  # Apply to
Comment2 = _input('Comment2', '===== Range/Bandwidth Settings ======')  # ========================
InfoColor = _input('InfoColor', clrOrange)  # Font color
InfoSize = _input('InfoSize', 7)  # Font size
SubWindow = _input('SubWindow', 0)  # Sub-Window placement
XDist = _input('XDist', 4)  # X-Position label
YDist = _input('YDist', 12)  # Y-Position label
UpperBB_Buffer = Arr(0, 0.0)
MidBB_Buffer = Arr(0, 0.0)
LowerBB_Buffer = Arr(0, 0.0)
labelRangeBB = 0  # Handle for the range bandwidth BB label
handleBB = 0
bars_calculated = 0

def CreateLabelInSubWindow(subWindowNumber):
    global labelRangeBB
    labelRangeBB = ObjectCreate(0, 'RangeBB', OBJ_LABEL, subWindowNumber, 0, 0)
    ObjectSetInteger(0, 'RangeBB', OBJPROP_COLOR, InfoColor)
    ObjectSetInteger(0, 'RangeBB', OBJPROP_FONTSIZE, InfoSize)
    ObjectSetInteger(0, 'RangeBB', OBJPROP_XDISTANCE, XDist)
    ObjectSetInteger(0, 'RangeBB', OBJPROP_YDISTANCE, YDist)
    ObjectSetString(0, 'RangeBB', OBJPROP_FONT, 'Arial Bold')
    ObjectSetString(0, 'RangeBB', OBJPROP_TEXT, 'wd.Range_BB: ')

def OnInit():
    global handleBB
    subWindowNumber = SubWindow
    CreateLabelInSubWindow(subWindowNumber)
    SetIndexBuffer(0, UpperBB_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, MidBB_Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowerBB_Buffer, INDICATOR_DATA)
    for i in range(0, 3):
        PlotIndexSetInteger(i, PLOT_SHIFT, BB_shift)
    handleBB = iBands(Symbol(), PERIOD_CURRENT, BB_period, BB_shift, Deviation, Applied_price)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    BBvalues = 0
    if (prev_calculated == 0 or BarsCalculated(handleBB) != bars_calculated) or rates_total > (prev_calculated + 1):
        BBvalues = MathMin(BarsCalculated(handleBB), rates_total)
    else:
        BBvalues = rates_total - prev_calculated + 1
    CopyBuffer(handleBB, 0, -BB_shift, BBvalues, MidBB_Buffer)
    CopyBuffer(handleBB, 1, -BB_shift, BBvalues, UpperBB_Buffer)
    CopyBuffer(handleBB, 2, -BB_shift, BBvalues, LowerBB_Buffer)
    BBandwidth = _int(MathRound(_fdiv(UpperBB_Buffer[rates_total - 1] - LowerBB_Buffer[rates_total - 1], Point())))
    labelBBandwidth = StringFormat('wd.Range_BB: %d', BBandwidth)
    ObjectSetString(0, 'RangeBB', OBJPROP_TEXT, labelBBandwidth)
    return rates_total

def OnDeinit(reason):
    IndicatorRelease(handleBB)
    ObjectDelete(0, 'RangeBB')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WdRangeBB(_MQL5Indicator):
    name = 'wd.Range_BB'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BB_period': 20,  # Period
        'BB_shift': 0,  # Shift
        'Deviation': 2.0,  # Deviations
        'Applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Apply to
        'InfoSize': 7,  # Font size
        'SubWindow': 0,  # Sub-Window placement
        'XDist': 4,  # X-Position label
        'YDist': 12,  # Y-Position label
    }

