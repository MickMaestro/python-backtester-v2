"""Price_Line — converted from MQL5: MQL5 Indicators/Price Line/Price_Line.mq5

Copyright: Copyright 2021, Dark Ryd3r; Link: https://twitter.com/DarkrRyd3r; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, Dark Ryd3r', 'link': 'https://twitter.com/DarkrRyd3r', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Price_Line', 'source': 'MQL5 Indicators/Price Line/Price_Line.mq5', 'folder': 'Price Line', 'inputs': [{'mql': 'CurrentTime', 'py': 'CurrentTime', 'param': 'CurrentTime', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'inpTextColorPositive', 'py': 'inpTextColorPositive', 'param': None, 'type': 'color', 'default': 10408790, 'label': 'Positive Color', 'sinput': False}, {'mql': 'inpTextColorNegative', 'py': 'inpTextColorNegative', 'param': None, 'type': 'color', 'default': 9639167, 'label': 'Negative Color', 'sinput': False}, {'mql': 'inpFontType', 'py': 'inpFontType', 'param': 'inpFontType', 'type': 'int', 'default': 1, 'label': 'Font Type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ML_FONTTYPE
ML_FONTTYPE_ARIAL = 0
ML_FONTTYPE_ARIALBLACK = 1
ML_FONTTYPE_VERDANA = 2
ML_FONTTYPE_TAHOMA = 3
ML_FONTTYPE_COURIERNEW = 4
ML_FONTTYPE_LUCIDACONSOLE = 5
_enum('ML_FONTTYPE', {0: 'ML_FONTTYPE_ARIAL', 1: 'ML_FONTTYPE_ARIALBLACK', 2: 'ML_FONTTYPE_VERDANA', 3: 'ML_FONTTYPE_TAHOMA', 4: 'ML_FONTTYPE_COURIERNEW', 5: 'ML_FONTTYPE_LUCIDACONSOLE'})

# enum TimeSelect
Current = 0
GMT = 1
Local = 2
_enum('TimeSelect', {0: 'Current', 1: 'GMT', 2: 'Local'})

# ---- inputs and global variables
CurrentTime = _input('CurrentTime', GMT)
_SymbolName = 'SymbolPriceLine'  # Namespacing the Symbol Background...
inpTextColorPositive = _input('inpTextColorPositive', 0x9ED356)  # Positive Color
inpTextColorNegative = _input('inpTextColorNegative', clrDeepPink)  # Negative Color
inpFontType = _input('inpFontType', 1)  # Font Type
inpFontSize = 12  # Symbol Font size
inpXOffSet = -35  # Reposition Symbol Offset on X axis (+/-)
inpYOffSet = 10  # Reposition Symbol Offset on Y axis (+/-)
gmt = ""
_CurWindowWidth = 0  # holds the current Chart width

def OnInit():
    ChartRedraw()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, _SymbolName)
    ObjectDelete(0, 'PriceTime')
    ObjectDelete(0, 'ltp')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prevCl, gmt
    if CurrentTime == Current:
        tm = TimeCurrent()
        gmt = TimeToString(tm, TIME_SECONDS)
    if CurrentTime == GMT:
        tm = TimeGMT()
        gmt = TimeToString(tm, TIME_SECONDS)
    if CurrentTime == Local:
        tm = TimeLocal()
        gmt = TimeToString(tm, TIME_SECONDS)
    last = iClose(None, PERIOD_M1, 0)
    if _s_OnCalculate_prevCl is _UNSET:
        _s_OnCalculate_prevCl = iClose(None, PERIOD_D1, 1)
    Calc2 = _fdiv(-(_s_OnCalculate_prevCl - last), last) * 100
    Value = DoubleToString(Calc2, 2)
    if _s_OnCalculate_prevCl < last:
        ObjectCreate(0, _SymbolName, OBJ_LABEL, 0, 0, 0)
        ObjectSetString(0, _SymbolName, OBJPROP_TEXT, Symbol() + '\r\r\r\r')
        ObjectSetInteger(0, _SymbolName, OBJPROP_COLOR, inpTextColorPositive)
        ObjectSetInteger(0, _SymbolName, OBJPROP_FONTSIZE, inpFontSize)
        ObjectSetInteger(0, _SymbolName, OBJPROP_BACK, False)
    else:
        ObjectCreate(0, _SymbolName, OBJ_LABEL, 0, 0, 0)
        ObjectSetString(0, _SymbolName, OBJPROP_TEXT, Symbol() + '\r\r\r\r')
        ObjectSetInteger(0, _SymbolName, OBJPROP_COLOR, inpTextColorNegative)
        ObjectSetInteger(0, _SymbolName, OBJPROP_FONTSIZE, inpFontSize)
        ObjectSetInteger(0, _SymbolName, OBJPROP_BACK, False)
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
    ObjectSetInteger(0, _SymbolName, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(0, _SymbolName, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
    ObjectSetInteger(0, _SymbolName, OBJPROP_XDISTANCE, inpXOffSet)
    ObjectSetInteger(0, _SymbolName, OBJPROP_YDISTANCE, inpYOffSet)
    if not HLineCreate(0, 'ltp', 0, last, clrSnow, STYLE_SOLID, 1, True, False, True, 0):
        return 0
    text = DoubleToString(last, Digits()) + '\r ' + '\r (' + Value + '%)\r  ' + gmt + '\r'
    if _s_OnCalculate_prevCl < last:
        if not TextCreate(0, 'PriceTime', 0, TimeGMT(), last, '        ' + text, 'Arial Black', inpFontSize, inpTextColorPositive, 0.0, ANCHOR_LEFT_LOWER, True, False, True, 0):
            return 0
    else:
        if not TextCreate(0, 'PriceTime', 0, TimeGMT(), last, '        ' + text, 'Arial Black', inpFontSize, inpTextColorNegative, 0.0, ANCHOR_LEFT_LOWER, True, False, True, 0):
            return 0
    return rates_total

def HLineCreate(chart_ID=0, name='HLine', sub_window=0, price=0.0, clr=clrRed, style=STYLE_SOLID, width=1, back=False, selection=True, hidden=True, z_order=0):
    if not price:
        price = iClose(None, PERIOD_M1, 0)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_HLINE, sub_window, 0, price):
        Print('HLineCreate', ': failed to create a horizontal line! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def TextCreate(chart_ID=0, name='Text', sub_window=0, time=0, price=0.0, text='Text', font='Arial', font_size=10, clr=clrRed, angle=0.0, anchor=ANCHOR_LEFT_UPPER, back=False, selection=False, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_TEXT, sub_window, time, price):
        Print('TextCreate', ': failed to create "Text" object! Error code = ', GetLastError())
        return False
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
    ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
    ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
    ObjectSetDouble(chart_ID, name, OBJPROP_ANGLE, angle)
    ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

# ---- static local variables
_s_OnCalculate_prevCl = _UNSET


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceLine(_MQL5Indicator):
    name = 'Price_Line'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CurrentTime': _Choice({0: 'Current', 1: 'GMT', 2: 'Local'}, default=1),
        'inpFontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Verdana', 3: 'Tahoma', 4: 'Courier New', 5: 'Lucida Console'}, default=1),  # Font Type
    }

