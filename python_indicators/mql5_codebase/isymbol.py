"""isymbol — converted from MQL5: MQL5 Indicators/2 Symbols on Chart/isymbol.mq5

Copyright: Copyright 2012, iC; Link: http://icreator.biz/; Version: 0.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, iC', 'link': 'http://icreator.biz/', 'version': '0.10', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 14}, 'colors': {1: [3937500]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'isymbol', 'source': 'MQL5 Indicators/2 Symbols on Chart/isymbol.mq5', 'folder': '2 Symbols on Chart', 'inputs': [{'mql': '_InpInst', 'py': '_InpInst', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': 'Symbol', 'sinput': False}, {'mql': '_InpInvert', 'py': '_InpInvert', 'param': '_InpInvert', 'type': 'int', 'default': 1, 'label': 'Invert', 'sinput': False}, {'mql': '_InpScale', 'py': '_InpScale', 'param': '_InpScale', 'type': 'int', 'default': 1, 'label': 'Scale fix', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum CYesNo
Yes = -1
No = 1
_enum('CYesNo', {-1: 'Yes', 1: 'No'})

# ---- inputs and global variables
_InpInst = _input('_InpInst', 'EURUSD')  # Symbol
_InpInvert = _input('_InpInvert', No)  # Invert
_InpScale = _input('_InpScale', No)  # Scale fix
_Inst = ""
_Invert = No
_ScaleFix = No
REDRAW = 0
OBuf = Arr(0, 0.0)
HBuf = Arr(0, 0.0)
LBuf = Arr(0, 0.0)
CBuf = Arr(0, 0.0)
_freeze = No
_startTime = 0
_endTime = 0
_lastChoose = 0
_first = 0
_count = 0
names = Arr(0, "")

def OnInit():
    global _Inst, _Invert, _ScaleFix
    SetIndexBuffer(0, OBuf, INDICATOR_DATA)
    SetIndexBuffer(1, HBuf, INDICATOR_DATA)
    SetIndexBuffer(2, LBuf, INDICATOR_DATA)
    SetIndexBuffer(3, CBuf, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    if not SymbolSelect(_InpInst, True):
        Print('Wrong symbol.')
        return -1
    _Inst = _InpInst
    _Invert = _InpInvert
    _ScaleFix = _InpScale
    GlobalVariableSet(COUNT, GlobalVariableGet(COUNT) + 1)
    GlobalVariableSet(POSITION, 0)
    ObjCreate()
    EventChartCustom(0, 0, 0, 0, None)
    return 0

def OnDeinit(reason):
    ObjectDelete(0, OBJ_INVERT)
    ObjectDelete(0, OBJ_FREEZE)
    ObjectDelete(0, OBJ_SCALE)
    ObjectDelete(0, OBJ_INST)
    ObjectDelete(0, OBJ_INST_TIP)
    ObjectDelete(0, OBJ_BACK)
    ObjectDelete(0, OBJ_BACK2)
    if GlobalVariableGet(COUNT) == 1:
        GlobalVariableDel(COUNT)
    else:
        GlobalVariableSet(COUNT, GlobalVariableGet(COUNT) - 1)
    GlobalVariableDel(POSITION)
    EventChartCustom(0, 0, 0, 0, None)

def OnCalculate(rates_total, prev_calculated, begin, in_):
    global _Inst, _Invert, _ScaleFix, _count, _first, _freeze, _lastChoose
    _Invert = (1 if (ObjectGetInteger(0, OBJ_INVERT, OBJPROP_STATE) == 0) else -1)
    _ScaleFix = (1 if (ObjectGetInteger(0, OBJ_SCALE, OBJPROP_STATE) == 0) else -1)
    _freeze = (1 if (ObjectGetInteger(0, OBJ_FREEZE, OBJPROP_STATE) == 0) else -1)
    _Inst = ObjectGetString(0, OBJ_INST, OBJPROP_TEXT)
    ObjectSetInteger(0, OBJ_BACK, OBJPROP_BGCOLOR, PlotIndexGetInteger(0, PLOT_LINE_COLOR))
    if _freeze == No:
        first = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR))
        count = _int(ChartGetInteger(0, CHART_VISIBLE_BARS))
        if (count - 1) > first:
            return 0
        _first = first
        _count = count
    elif _freeze == Yes:
        if _lastChoose != No:
            _first = _first + _first + 1 - _count
        _count = _first + 1
    _lastChoose = _freeze
    if in_[0] != EMPTY_VALUE:
        if _ScaleFix == Yes:
            ChartSetInteger(0, CHART_SCALEFIX, 0, True)
        else:
            ChartSetInteger(0, CHART_SCALEFIX, 0, False)
    elif in_[2] != EMPTY_VALUE:
        if _freeze == Yes:
            ObjectSetInteger(0, OBJ_FREEZE, OBJPROP_STATE, True)
            ArrayInitialize(OBuf, 0.0)
            ArrayInitialize(HBuf, 0.0)
            ArrayInitialize(LBuf, 0.0)
            ArrayInitialize(CBuf, 0.0)
        else:
            ObjectSetInteger(0, OBJ_FREEZE, OBJPROP_STATE, False)
    elif (in_[1] == EMPTY_VALUE and in_[3] == EMPTY_VALUE) and in_[4] == EMPTY_VALUE:
        return rates_total
    d = 0.0
    tick_size = SymbolInfoDouble(_Inst, SYMBOL_POINT)
    tick_size2 = SymbolInfoDouble(Symbol(), SYMBOL_POINT)
    min_ = DBL_MAX
    max_ = 0.0
    lOp = 0.0
    cnt = -1
    prevTime = 0
    time = Arr(0, 0)
    high = Arr(0, 0.0)
    low = Arr(0, 0.0)
    open = Arr(1, 0.0, dyn=False)
    rt = Arr(1, 0, dyn=False, factory=MqlRates)
    CopyOpen(Symbol(), 0, _first, 1, open)
    CopyTime(Symbol(), 0, _first - _count + 1, _count, time)
    CopyHigh(Symbol(), 0, _first - _count + 1, _count, high)
    CopyLow(Symbol(), 0, _first - _count + 1, _count, low)
    for i in range(rates_total - _first - 1, rates_total - _first + _count - 1):
        CopyRates(_Inst, 0, _DT(time[(cnt := cnt + 1)]), 1, rt)
        if rt[0].time == prevTime:
            OBuf[i] = CBuf[i - 1]
            HBuf[i] = CBuf[i - 1]
            LBuf[i] = CBuf[i - 1]
            CBuf[i] = CBuf[i - 1]
            continue
        if cnt > 0:
            d += _fdiv((rt[0].open - lOp) * _Invert, tick_size) * tick_size2
        lOp = rt[0].open
        OBuf[i] = open[0]
        HBuf[i] = open[0]
        LBuf[i] = open[0]
        CBuf[i] = open[0]
        if prevTime != 0:
            OBuf[i] += d
            HBuf[i] += d + (_fdiv((rt[0].high - rt[0].open) * _Invert, tick_size) * tick_size2)
            LBuf[i] += d + (_fdiv((rt[0].low - rt[0].open) * _Invert, tick_size) * tick_size2)
            CBuf[i] += d + (_fdiv((rt[0].close - rt[0].open) * _Invert, tick_size) * tick_size2)
        prevTime = rt[0].time
        if high[cnt] > max_:
            max_ = high[cnt]
        if HBuf[i] > max_:
            max_ = HBuf[i]
        if LBuf[i] > max_:
            max_ = LBuf[i]
        if low[cnt] < min_:
            min_ = low[cnt]
        if HBuf[i] < min_:
            min_ = HBuf[i]
        if LBuf[i] < min_:
            min_ = LBuf[i]
    if _ScaleFix == Yes:
        ChartSetDouble(0, CHART_FIXED_MAX, max_)
        ChartSetDouble(0, CHART_FIXED_MIN, min_)
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global _s_OnChartEvent_b, _s_OnChartEvent_lastH, _s_OnChartEvent_lastTime
    arr = Arr.of([EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE], fill=0.0)
    _sw1 = id_
    _k2 = 0 if _sw1 == CHARTEVENT_CUSTOM else 1 if _sw1 == CHARTEVENT_OBJECT_CLICK else 2 if _sw1 == CHARTEVENT_OBJECT_ENDEDIT else 3 if _sw1 == CHARTEVENT_CLICK else 4 if _sw1 == CHARTEVENT_CHART_CHANGE else 5
    try:
        if _k2 <= 0:
            _s_OnChartEvent_lastH = 0
            arr[4] = REDRAW
            raise _SwitchBreak
        if _k2 <= 1:
            _s_OnChartEvent_b = False
            if StringCompare(sparam, OBJ_SCALE) == 0:
                arr[0] = float(ObjectGetInteger(0, OBJ_SCALE, OBJPROP_STATE))
            if StringCompare(sparam, OBJ_INVERT) == 0:
                arr[1] = float(ObjectGetInteger(0, OBJ_INVERT, OBJPROP_STATE))
            if StringCompare(sparam, OBJ_FREEZE) == 0:
                arr[2] = float(ObjectGetInteger(0, OBJ_FREEZE, OBJPROP_STATE))
            arr[4] = REDRAW
            raise _SwitchBreak
        if _k2 <= 2:
            if StringCompare(sparam, OBJ_INST) == 0:
                s = ObjectGetString(0, OBJ_INST, OBJPROP_TEXT)
                if SymbolSelect(s, True):
                    arr[3] = True
                else:
                    ObjectSetString(0, OBJ_INST, OBJPROP_TEXT, _Inst)
                arr[4] = REDRAW
            raise _SwitchBreak
        if _k2 <= 3:
            if not _s_OnChartEvent_b:
                _s_OnChartEvent_b = True
                return
            if (GetTickCount() - _s_OnChartEvent_lastTime) > 250:
                _s_OnChartEvent_lastTime = GetTickCount()
                return
            else:
                arr[2] = float(ObjectGetInteger(0, OBJ_FREEZE, OBJPROP_STATE))
                i = 0
                while i < ObjectsTotal(0, 0, OBJ_BUTTON):
                    if ObjectGetString(0, ObjectName(0, i, 0, OBJ_BUTTON), OBJPROP_TEXT) == 'Freeze':
                        ObjectSetInteger(0, ObjectName(0, i, 0, OBJ_BUTTON), OBJPROP_STATE, (False if (_freeze < 0) else True))
                    i += 1
        if _k2 <= 4:
            arr[4] = REDRAW
            raise _SwitchBreak
    except _SwitchBreak:
        pass
    if arr[4] == REDRAW:
        if _s_OnChartEvent_lastH != ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS):
            ObjRePos()
        _s_OnChartEvent_lastH = _int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS))
        OnCalculate(Bars(Symbol(), 0), 0, 0, arr)
        ChartRedraw()

def ObjCreate():
    if ObjectFind(0, OBJ_BACK) < 0:
        ObjectCreate(0, OBJ_BACK, OBJ_RECTANGLE_LABEL, 0, 0, 0)
        ObjectCreate(0, OBJ_BACK, OBJ_RECTANGLE_LABEL, 0, 0, 0)
        ObjectSetInteger(0, OBJ_BACK, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, OBJ_BACK, OBJPROP_XDISTANCE, 0)
        ObjectSetInteger(0, OBJ_BACK, OBJPROP_XSIZE, 357)
        ObjectSetInteger(0, OBJ_BACK, OBJPROP_YSIZE, 26)
        ObjectSetInteger(0, OBJ_BACK, OBJPROP_BACK, True)
    if ObjectFind(0, OBJ_BACK2) < 0:
        ObjectCreate(0, OBJ_BACK2, OBJ_RECTANGLE_LABEL, 0, 0, 0)
        ObjectSetInteger(0, OBJ_BACK2, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, OBJ_BACK2, OBJPROP_XDISTANCE, 229)
        ObjectSetInteger(0, OBJ_BACK2, OBJPROP_XSIZE, 125)
        ObjectSetInteger(0, OBJ_BACK2, OBJPROP_YSIZE, 22)
        ObjectSetInteger(0, OBJ_BACK2, OBJPROP_BGCOLOR, clrWhite)
    if ObjectFind(0, OBJ_SCALE) < 0:
        ObjectCreate(0, OBJ_SCALE, OBJ_BUTTON, 0, 0, 0)
        ObjectSetInteger(0, OBJ_SCALE, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, OBJ_SCALE, OBJPROP_XDISTANCE, 2)
        ObjectSetInteger(0, OBJ_SCALE, OBJPROP_FONTSIZE, 9)
        ObjectSetString(0, OBJ_SCALE, OBJPROP_TEXT, 'Scale fix')
        ObjectSetInteger(0, OBJ_SCALE, OBJPROP_XSIZE, 75)
        ObjectSetInteger(0, OBJ_SCALE, OBJPROP_YSIZE, 22)
        ObjectSetInteger(0, OBJ_SCALE, OBJPROP_STATE, (True if (_InpScale == Yes) else False))
    if ObjectFind(0, OBJ_INVERT) < 0:
        ObjectCreate(0, OBJ_INVERT, OBJ_BUTTON, 0, 0, 0)
        ObjectSetInteger(0, OBJ_INVERT, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, OBJ_INVERT, OBJPROP_XDISTANCE, 77)
        ObjectSetInteger(0, OBJ_INVERT, OBJPROP_FONTSIZE, 9)
        ObjectSetString(0, OBJ_INVERT, OBJPROP_TEXT, 'Invert')
        ObjectSetInteger(0, OBJ_INVERT, OBJPROP_XSIZE, 75)
        ObjectSetInteger(0, OBJ_INVERT, OBJPROP_YSIZE, 22)
        ObjectSetInteger(0, OBJ_INVERT, OBJPROP_STATE, (True if (_InpInvert == Yes) else False))
    if ObjectFind(0, OBJ_FREEZE) < 0:
        ObjectCreate(0, OBJ_FREEZE, OBJ_BUTTON, 0, 0, 0)
        ObjectSetInteger(0, OBJ_FREEZE, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, OBJ_FREEZE, OBJPROP_XDISTANCE, 152)
        ObjectSetInteger(0, OBJ_FREEZE, OBJPROP_FONTSIZE, 9)
        ObjectSetString(0, OBJ_FREEZE, OBJPROP_TEXT, 'Freeze')
        ObjectSetInteger(0, OBJ_FREEZE, OBJPROP_XSIZE, 75)
        ObjectSetInteger(0, OBJ_FREEZE, OBJPROP_YSIZE, 22)
    if ObjectFind(0, OBJ_INST) < 0:
        ObjectCreate(0, OBJ_INST, OBJ_EDIT, 0, 0, 0)
        ObjectSetInteger(0, OBJ_INST, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, OBJ_INST, OBJPROP_XDISTANCE, 278)
        ObjectSetInteger(0, OBJ_INST, OBJPROP_FONTSIZE, 9)
        ObjectSetInteger(0, OBJ_INST, OBJPROP_XSIZE, 75)
        ObjectSetInteger(0, OBJ_INST, OBJPROP_YSIZE, 18)
        ObjectSetInteger(0, OBJ_INST, OBJPROP_BGCOLOR, clrWhite)
        ObjectSetInteger(0, OBJ_INST, OBJPROP_BORDER_COLOR, clrWhite)
        ObjectSetInteger(0, OBJ_INST, OBJPROP_COLOR, clrBlack)
        ObjectCreate(0, OBJ_INST_TIP, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, OBJ_INST_TIP, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, OBJ_INST_TIP, OBJPROP_XDISTANCE, 235)
        ObjectSetInteger(0, OBJ_INST_TIP, OBJPROP_FONTSIZE, 9)
        ObjectSetString(0, OBJ_INST_TIP, OBJPROP_TEXT, 'Symbol:')
        ObjectSetInteger(0, OBJ_INST_TIP, OBJPROP_COLOR, clrGray)
        ObjectSetString(0, OBJ_INST, OBJPROP_TEXT, _InpInst)

def ObjRePos():
    yPos = _int(GlobalVariableGet(POSITION))
    height = _int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)) - (yPos * 27)
    ObjectSetInteger(0, OBJ_SCALE, OBJPROP_YDISTANCE, height - 25)
    ObjectSetInteger(0, OBJ_INVERT, OBJPROP_YDISTANCE, height - 25)
    ObjectSetInteger(0, OBJ_FREEZE, OBJPROP_YDISTANCE, height - 25)
    ObjectSetInteger(0, OBJ_INST_TIP, OBJPROP_YDISTANCE, height - 22)
    ObjectSetInteger(0, OBJ_INST, OBJPROP_YDISTANCE, height - 23)
    ObjectSetInteger(0, OBJ_BACK, OBJPROP_YDISTANCE, height - 27)
    ObjectSetInteger(0, OBJ_BACK2, OBJPROP_YDISTANCE, height - 25)
    if yPos == (GlobalVariableGet(COUNT) - 1):
        GlobalVariableSet(POSITION, 0)
    else:
        GlobalVariableSet(POSITION, (yPos := yPos + 1))

# ---- global variables initialised from expressions
TC = IntegerToString(GetTickCount())
OBJ_NAME = 'PriceDiffLabel' + TC
OBJ_INVERT = 'ObjInvert' + TC
OBJ_SCALE = 'ObjScale' + TC
OBJ_INST = 'ObjSymbol' + TC
OBJ_INST_TIP = 'ObjSymbolTip' + TC
OBJ_FREEZE = 'ObjFreeze' + TC
OBJ_BACK = 'ObjBackgroung' + TC
OBJ_BACK2 = 'ObjBack2' + TC
WH = IntegerToString(ChartGetInteger(0, CHART_WINDOW_HANDLE))
COUNT = 'Count' + WH
POSITION = 'Position' + WH

# ---- static local variables
_s_OnChartEvent_lastTime = 0
_s_OnChartEvent_b = True
_s_OnChartEvent_lastH = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Isymbol(_MQL5Indicator):
    name = 'isymbol'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        '_InpInvert': _Choice({-1: 'Yes', 1: 'No'}, default=1),  # Invert
        '_InpScale': _Choice({-1: 'Yes', 1: 'No'}, default=1),  # Scale fix
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

