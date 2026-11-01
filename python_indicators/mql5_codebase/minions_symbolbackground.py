"""Minions.SymbolBackground — converted from MQL5: MQL5 Indicators/Symbol Name On Chart/Minions.SymbolBackground.mq5

Minions showing the Symbol at the Chart background in an unobtrusive way
 
(CC) Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
Copyright: www.MinionsLabs.com; Link: http://www.MinionsLabs.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.MinionsLabs.com', 'link': 'http://www.MinionsLabs.com', 'version': '1.0', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Minions showing the Symbol at the Chart background in an unobtrusive way', ' ', '(CC) Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'], 'name': 'Minions.SymbolBackground', 'source': 'MQL5 Indicators/Symbol Name On Chart/Minions.SymbolBackground.mq5', 'folder': 'Symbol Name On Chart', 'inputs': [{'mql': 'inpTextColor', 'py': 'inpTextColor', 'param': None, 'type': 'color', 'default': 2960685, 'label': 'Symbol Text color', 'sinput': False}, {'mql': 'inpFontType', 'py': 'inpFontType', 'param': 'inpFontType', 'type': 'int', 'default': 1, 'label': 'Font Type', 'sinput': False}, {'mql': 'inpFontSize', 'py': 'inpFontSize', 'param': 'inpFontSize', 'type': 'int', 'default': 24, 'label': 'Symbol Font size', 'sinput': False}, {'mql': 'inpWindowPosition', 'py': 'inpWindowPosition', 'param': 'inpWindowPosition', 'type': 'int', 'default': 1, 'label': 'Symbol position', 'sinput': False}, {'mql': 'inpXOffSet', 'py': 'inpXOffSet', 'param': 'inpXOffSet', 'type': 'int', 'default': 0, 'label': 'Reposition Symbol Offset on X axis (+/-)', 'sinput': False}, {'mql': 'inpYOffSet', 'py': 'inpYOffSet', 'param': 'inpYOffSet', 'type': 'int', 'default': 0, 'label': 'Reposition Symbol Offset on Y axis (+/-)', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ML_WINPOSITION
ML_WINPOSITION_UPPER_LEFT = 0
ML_WINPOSITION_UPPER_CENTER = 1
ML_WINPOSITION_UPPER_RIGHT = 2
ML_WINPOSITION_LOWER_LEFT = 3
ML_WINPOSITION_LOWER_CENTER = 4
ML_WINPOSITION_LOWER_RIGHT = 5
_enum('ML_WINPOSITION', {0: 'ML_WINPOSITION_UPPER_LEFT', 1: 'ML_WINPOSITION_UPPER_CENTER', 2: 'ML_WINPOSITION_UPPER_RIGHT', 3: 'ML_WINPOSITION_LOWER_LEFT', 4: 'ML_WINPOSITION_LOWER_CENTER', 5: 'ML_WINPOSITION_LOWER_RIGHT'})

# enum ML_FONTTYPE
ML_FONTTYPE_ARIAL = 0
ML_FONTTYPE_ARIALBLACK = 1
ML_FONTTYPE_VERDANA = 2
ML_FONTTYPE_TAHOMA = 3
ML_FONTTYPE_COURIERNEW = 4
ML_FONTTYPE_LUCIDACONSOLE = 5
_enum('ML_FONTTYPE', {0: 'ML_FONTTYPE_ARIAL', 1: 'ML_FONTTYPE_ARIALBLACK', 2: 'ML_FONTTYPE_VERDANA', 3: 'ML_FONTTYPE_TAHOMA', 4: 'ML_FONTTYPE_COURIERNEW', 5: 'ML_FONTTYPE_LUCIDACONSOLE'})

# ---- inputs and global variables
inpTextColor = _input('inpTextColor', 0x2D2D2D)  # Symbol Text color
inpFontType = _input('inpFontType', 1)  # Font Type
inpFontSize = _input('inpFontSize', 24)  # Symbol Font size
inpWindowPosition = _input('inpWindowPosition', ML_WINPOSITION_UPPER_CENTER)  # Symbol position
inpXOffSet = _input('inpXOffSet', 0)  # Reposition Symbol Offset on X axis (+/-)
inpYOffSet = _input('inpYOffSet', 0)  # Reposition Symbol Offset on Y axis (+/-)
_SymbolName = 'MLabs_SymbolBackground'  # Namespacing the Symbol Background...
_CurWindowWidth = 0  # holds the current Chart width

def OnInit():
    ObjectCreate(0, _SymbolName, OBJ_LABEL, 0, 0, 0)
    ObjectSetString(0, _SymbolName, OBJPROP_TEXT, Symbol())
    ObjectSetInteger(0, _SymbolName, OBJPROP_COLOR, inpTextColor)
    ObjectSetInteger(0, _SymbolName, OBJPROP_FONTSIZE, inpFontSize)
    ObjectSetInteger(0, _SymbolName, OBJPROP_BACK, True)
    if inpFontType == ML_FONTTYPE_ARIAL:
        ObjectSetString(0, _SymbolName, OBJPROP_FONT, 'Arial')
    if inpFontType == ML_FONTTYPE_ARIALBLACK:
        ObjectSetString(0, _SymbolName, OBJPROP_FONT, 'Arial Black')
    if inpFontType == ML_FONTTYPE_VERDANA:
        ObjectSetString(0, _SymbolName, OBJPROP_FONT, 'Verdana')
    if inpFontType == ML_FONTTYPE_TAHOMA:
        ObjectSetString(0, _SymbolName, OBJPROP_FONT, 'Tahoma')
    if inpFontType == ML_FONTTYPE_COURIERNEW:
        ObjectSetString(0, _SymbolName, OBJPROP_FONT, 'Courier New')
    if inpFontType == ML_FONTTYPE_LUCIDACONSOLE:
        ObjectSetString(0, _SymbolName, OBJPROP_FONT, 'Lucida Console')
    updateXY()
    ChartRedraw()

def OnDeinit(reason):
    ObjectDelete(0, _SymbolName)

def OnCalculate(rates_total, prev_calculated, begin, price):
    return 0

def OnChartEvent(id_, lparam, dparam, sparam):
    global _CurWindowWidth
    newWindowsWidth = 0
    if id_ == CHARTEVENT_CHART_CHANGE:
        newWindowsWidth = _int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, 0))
        if _CurWindowWidth != newWindowsWidth:
            updateXY()
            _CurWindowWidth = newWindowsWidth

def updateXY():
    if inpWindowPosition == ML_WINPOSITION_UPPER_LEFT:
        ObjectSetInteger(0, _SymbolName, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_XDISTANCE, inpXOffSet)
        ObjectSetInteger(0, _SymbolName, OBJPROP_YDISTANCE, inpYOffSet)
    elif inpWindowPosition == ML_WINPOSITION_UPPER_RIGHT:
        ObjectSetInteger(0, _SymbolName, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_XDISTANCE, inpXOffSet)
        ObjectSetInteger(0, _SymbolName, OBJPROP_YDISTANCE, inpYOffSet)
    elif inpWindowPosition == ML_WINPOSITION_UPPER_CENTER:
        ObjectSetInteger(0, _SymbolName, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_XDISTANCE, inpXOffSet + _idiv(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, 0), 2))
        ObjectSetInteger(0, _SymbolName, OBJPROP_YDISTANCE, inpYOffSet)
    elif inpWindowPosition == ML_WINPOSITION_LOWER_LEFT:
        ObjectSetInteger(0, _SymbolName, OBJPROP_CORNER, CORNER_LEFT_LOWER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_XDISTANCE, inpXOffSet)
        ObjectSetInteger(0, _SymbolName, OBJPROP_YDISTANCE, inpYOffSet)
    elif inpWindowPosition == ML_WINPOSITION_LOWER_RIGHT:
        ObjectSetInteger(0, _SymbolName, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_XDISTANCE, inpXOffSet)
        ObjectSetInteger(0, _SymbolName, OBJPROP_YDISTANCE, inpYOffSet)
    elif inpWindowPosition == ML_WINPOSITION_LOWER_CENTER:
        ObjectSetInteger(0, _SymbolName, OBJPROP_CORNER, CORNER_LEFT_LOWER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
        ObjectSetInteger(0, _SymbolName, OBJPROP_XDISTANCE, inpXOffSet + _idiv(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, 0), 2))
        ObjectSetInteger(0, _SymbolName, OBJPROP_YDISTANCE, inpYOffSet)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MinionsSymbolBackground(_MQL5Indicator):
    name = 'Minions.SymbolBackground'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Verdana', 3: 'Tahoma', 4: 'Courier New', 5: 'Lucida Console'}, default=1),  # Font Type
        'inpFontSize': 24,  # Symbol Font size
        'inpWindowPosition': _Choice({0: 'Upper Left of the chart', 1: 'Upper Center of the chart', 2: 'Upper Right of the chart', 3: 'Lower Left of the chart', 4: 'Lower Center of the chart', 5: 'Lower Right of the chart'}, default=1),  # Symbol position
        'inpXOffSet': 0,  # Reposition Symbol Offset on X axis (+/-)
        'inpYOffSet': 0,  # Reposition Symbol Offset on Y axis (+/-)
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

