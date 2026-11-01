"""PriceLine_renko — converted from MQL5: MQL5 Indicators/Price Line 3/PriceLine_renko.mq5

Copyright: Rajesh Nait, Copyright 2023; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rajesh Nait, Copyright 2023', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'PriceLine_renko', 'source': 'MQL5 Indicators/Price Line 3/PriceLine_renko.mq5', 'folder': 'Price Line 3', 'inputs': [{'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'int', 'default': 10, 'label': 'Font size', 'sinput': False}, {'mql': 'InpAngle', 'py': 'InpAngle', 'param': 'InpAngle', 'type': 'double', 'default': 0.0, 'label': 'Slope angle in degrees', 'sinput': False}, {'mql': 'InpAnchor', 'py': 'InpAnchor', 'param': 'InpAnchor', 'type': 'int', 'default': 8, 'label': 'Anchor type', 'sinput': False}, {'mql': 'InpBack', 'py': 'InpBack', 'param': 'InpBack', 'type': 'bool', 'default': False, 'label': 'Background object', 'sinput': False}, {'mql': 'InpSelection', 'py': 'InpSelection', 'param': 'InpSelection', 'type': 'bool', 'default': False, 'label': 'Highlight to move', 'sinput': False}, {'mql': 'InpHidden', 'py': 'InpHidden', 'param': 'InpHidden', 'type': 'bool', 'default': True, 'label': 'Hidden in the object list', 'sinput': False}, {'mql': 'InpZOrder', 'py': 'InpZOrder', 'param': 'InpZOrder', 'type': 'long', 'default': 0, 'label': 'Priority for mouse click', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
tf = PERIOD_M30  # 2nd chart PERIOD for sync
myfont = 'Orbitron'
AllowZoom = True
_SymbolName = 'SymbolPriceLine'  # Namespacing the Symbol Background...
StringSymbolList = Arr(0, "")  # Namespacing the Symbol Background...
Value = ""  # Namespacing the Symbol Background...
text = ""  # Namespacing the Symbol Background...
left = ""  # Namespacing the Symbol Background...
gmt = ""  # Namespacing the Symbol Background...
inpTextColorPositive = 0x9ED356  # Positive Color
inpTextColorNegative = 0x4536F2  # Negative Color
inpFontSize = 12  # Symbol Font size
inpXOffSet = 32  # Reposition Symbol Offset on X axis (+/-)
inpYOffSet = 20  # Reposition Symbol Offset on Y axis (+/-)
m_prev_bars = 0
tm = 0
time_0 = 0
symID = 0.0
symTotal = 0.0
Calc2 = 0.0
last = 0.0
copen = 0.0
prevCl = 0.0
_CurWindowWidth = 0
NumSymbols = 0
scale = 0
prefix = 'p_'
InpFontSize = _input('InpFontSize', 10)  # Font size
InpAngle = _input('InpAngle', 0.0)  # Slope angle in degrees
InpAnchor = _input('InpAnchor', ANCHOR_CENTER)  # Anchor type
InpBack = _input('InpBack', False)  # Background object
InpSelection = _input('InpSelection', False)  # Highlight to move
InpHidden = _input('InpHidden', True)  # Hidden in the object list
InpZOrder = _input('InpZOrder', 0)  # Priority for mouse click

def OnInit():
    global symID, symTotal
    ChartSetInteger(ChartID(), CHART_EVENT_MOUSE_WHEEL, True)
    symID = GlobalVariableGet('SymbolID')
    symTotal = GlobalVariableGet('SymbolTotal')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Calc2, Value, copen, gmt, last, m_prev_bars, prevCl, time_0, tm
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    time_0 = time[rates_total - 1]
    m_prev_bars = time_0
    tm = TimeGMT()
    gmt = TimeToString(tm, TIME_SECONDS)
    last = close[0]
    copen = open[0]
    prevCl = iClose(None, PERIOD_M1, 1440)
    if last > 0 and prevCl > 0:
        Calc2 = _fdiv(-(prevCl - last), prevCl) * 100
        Value = DoubleToString(Calc2, 2)
        if not LabelCreate(0, prefix + 'last', 0, inpXOffSet, inpYOffSet, CORNER_RIGHT_LOWER, DoubleToString(last, Digits()), myfont, inpFontSize, clrHoneydew, 0.0, ANCHOR_RIGHT_LOWER, False, False, True, 0):
            return 0
        if prevCl < last:
            if not LabelCreate(0, prefix + _SymbolName, 0, inpXOffSet, inpYOffSet, CORNER_RIGHT_UPPER, Value + '%\r ' + gmt + ' ' + IntegerToString(_int(symID)) + '/\r\r\r' + IntegerToString(_int(symTotal)), myfont, inpFontSize, inpTextColorPositive, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0):
                return 0
        else:
            if not LabelCreate(0, prefix + _SymbolName, 0, inpXOffSet, inpYOffSet, CORNER_RIGHT_UPPER, Value + '%\r ' + gmt + ' ' + IntegerToString(_int(symID)) + '/\r\r\r' + IntegerToString(_int(symTotal)), myfont, inpFontSize, inpTextColorNegative, 0.0, ANCHOR_RIGHT_UPPER, False, False, True, 0):
                return 0
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global scale
    if id_ == CHARTEVENT_KEYDOWN:
        _sw1 = _int(lparam)
        if _sw1 == 37:
            PrevSymbol()
        elif _sw1 == 39:
            NextSymbol()
    if id_ == CHARTEVENT_MOUSE_WHEEL:
        if dparam > 0:
            scale = _int(ChartGetInteger(ChartID(), CHART_SCALE))
            scale += 1
            if scale > 5:
                scale = 5
            ChartSetInteger(ChartID(), CHART_MOUSE_SCROLL, False)
            ChartSetInteger(ChartID(), CHART_EVENT_MOUSE_MOVE, False)
            if ChartSetInteger(ChartID(), CHART_SCALE, scale) == False:
                Print(GetLastError())
            ChartSetInteger(ChartID(), CHART_MOUSE_SCROLL, True)
            ChartSetInteger(ChartID(), CHART_EVENT_MOUSE_MOVE, True)
            ChartRedraw(ChartID())
        if dparam < 0:
            scale = _int(ChartGetInteger(ChartID(), CHART_SCALE))
            scale -= 1
            if scale < 0:
                scale = 0
            if ChartSetInteger(ChartID(), CHART_MOUSE_SCROLL, False) == False:
                Print(GetLastError())
            if ChartSetInteger(ChartID(), CHART_EVENT_MOUSE_MOVE, False) == False:
                Print(GetLastError())
            if ChartSetInteger(ChartID(), CHART_SCALE, scale) == False:
                Print(GetLastError())
            if ChartSetInteger(ChartID(), CHART_EVENT_MOUSE_MOVE, True) == False:
                Print(GetLastError())
            if ChartSetInteger(ChartID(), CHART_MOUSE_SCROLL, True) == False:
                Print(GetLastError())
            ChartRedraw(ChartID())

def GetTimeFrame(lPeriod):
    _sw2 = lPeriod
    if _sw2 == PERIOD_M1:
        return 'M1'
    elif _sw2 == PERIOD_M2:
        return 'M2'
    elif _sw2 == PERIOD_M3:
        return 'M3'
    elif _sw2 == PERIOD_M4:
        return 'M4'
    elif _sw2 == PERIOD_M5:
        return 'M5'
    elif _sw2 == PERIOD_M6:
        return 'M6'
    elif _sw2 == PERIOD_M10:
        return 'M10'
    elif _sw2 == PERIOD_M12:
        return 'M12'
    elif _sw2 == PERIOD_M15:
        return 'M15'
    elif _sw2 == PERIOD_M20:
        return 'M20'
    elif _sw2 == PERIOD_M30:
        return 'M30'
    elif _sw2 == PERIOD_H1:
        return 'H1'
    elif _sw2 == PERIOD_H2:
        return 'H2'
    elif _sw2 == PERIOD_H3:
        return 'H3'
    elif _sw2 == PERIOD_H4:
        return 'H4'
    elif _sw2 == PERIOD_H6:
        return 'H6'
    elif _sw2 == PERIOD_H8:
        return 'H8'
    elif _sw2 == PERIOD_H12:
        return 'H12'
    elif _sw2 == PERIOD_D1:
        return 'D1'
    elif _sw2 == PERIOD_W1:
        return 'W1'
    elif _sw2 == PERIOD_MN1:
        return 'MN1'
    return EnumToString(lPeriod, 'ENUM_TIMEFRAMES')

def PrevSymbol():
    currentIndex = 0
    GetSymbols()
    currentIndex = GetIndex()
    currentIndex -= 1
    if currentIndex < 0:
        currentIndex = NumSymbols - 1
        ChartSetSymbolPeriod(0, StringSymbolList[currentIndex], 0)
    else:
        ChartSetSymbolPeriod(0, StringSymbolList[currentIndex], 0)

def NextSymbol():
    currentIndex = 0
    GetSymbols()
    currentIndex = GetIndex()
    currentIndex += 1
    if currentIndex >= NumSymbols:
        ChartSetSymbolPeriod(0, StringSymbolList[0], 0)
    else:
        ChartSetSymbolPeriod(0, StringSymbolList[currentIndex], 0)

def GetSymbols():
    global NumSymbols
    numSymbolsMarketWatch = SymbolsTotal(True)
    NumSymbols = numSymbolsMarketWatch
    ArrayResize(StringSymbolList, numSymbolsMarketWatch)
    for i in range(0, numSymbolsMarketWatch):
        StringSymbolList[i] = SymbolName(i, True)

def GetIndex():
    index = 0
    for i in range(0, NumSymbols):
        if Symbol() == StringSymbolList[i]:
            index = i
            break
    return index

def ChartScaleGet(chart_ID=0):
    result = Box(-1)
    ResetLastError()
    if not ChartGetInteger(chart_ID, CHART_SCALE, 0, result):
        Print('ChartScaleGet' + ', Error Code = ', GetLastError())
    return _int(result.v)

def ChartScaleSet(value, chart_ID=0):
    ResetLastError()
    if not ChartSetInteger(chart_ID, CHART_SCALE, 0, value):
        Print('ChartScaleSet' + ', Error Code = ', GetLastError())
        return False
    return True

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

def TextCreate(chart_ID=0, name='Text', sub_window=0, time=0, price=0.0, text2='Text', font='Arial', font_size=10, clr=clrRed, angle=0.0, anchor=ANCHOR_LEFT_UPPER, back=False, selection=False, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_TEXT, sub_window, time, price):
        Print('TextCreate', ': failed to create "Text" object! Error code = ', GetLastError())
        return False
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text2)
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

def LabelCreate(chart_ID=0, name='Label', sub_window=0, x=0, y=0, corner=CORNER_LEFT_UPPER, text2='Label3', font='Arial', font_size=10, clr=clrRed, angle=0.0, anchor=ANCHOR_LEFT_UPPER, back=False, selection=False, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_LABEL, sub_window, 0, 0):
        Print('LabelCreate', ': failed to create text label! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner)
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text2)
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceLineRenko(_MQL5Indicator):
    name = 'PriceLine_renko'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFontSize': 10,  # Font size
        'InpAngle': 0.0,  # Slope angle in degrees
        'InpAnchor': _Choice({0: 'ANCHOR_LEFT_UPPER', 1: 'ANCHOR_LEFT', 2: 'ANCHOR_LEFT_LOWER', 3: 'ANCHOR_LOWER', 4: 'ANCHOR_RIGHT_LOWER', 5: 'ANCHOR_RIGHT', 6: 'ANCHOR_RIGHT_UPPER', 7: 'ANCHOR_UPPER', 8: 'ANCHOR_CENTER'}, default=8),  # Anchor type
        'InpBack': False,  # Background object
        'InpSelection': False,  # Highlight to move
        'InpHidden': True,  # Hidden in the object list
        'InpZOrder': 0,  # Priority for mouse click
    }

