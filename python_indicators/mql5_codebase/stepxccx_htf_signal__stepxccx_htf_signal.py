"""stepxccx_htf_signal_ — converted from MQL5: MQL5 Indicators/StepXCCX_HTF_Signal/stepxccx_htf_signal_.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'stepxccx_htf_signal_', 'source': 'MQL5 Indicators/StepXCCX_HTF_Signal/stepxccx_htf_signal_.mq5', 'folder': 'StepXCCX_HTF_Signal', 'inputs': [{'mql': 'Symbol_', 'py': 'Symbol_', 'param': None, 'type': 'string', 'default': '', 'label': 'Financial asset', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Indicator timeframe for the indicator calculation', 'sinput': False}, {'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 4, 'label': 'Price smoothing method', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 30, 'label': 'Moving average period', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 100, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'MSmoothMethod', 'py': 'MSmoothMethod', 'param': 'MSmoothMethod', 'type': 'int', 'default': 7, 'label': 'Deviation smoothing method', 'sinput': False}, {'mql': 'MPeriod', 'py': 'MPeriod', 'param': 'MPeriod', 'type': 'int', 'default': 7, 'label': 'Average deviation period', 'sinput': False}, {'mql': 'MPhase', 'py': 'MPhase', 'param': 'MPhase', 'type': 'int', 'default': 15, 'label': 'Deviation smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 6, 'label': 'Applied price', 'sinput': False}, {'mql': 'StepSizeFast', 'py': 'StepSizeFast', 'param': 'StepSizeFast', 'type': 'int', 'default': 5, 'label': 'Fast step', 'sinput': False}, {'mql': 'StepSizeSlow', 'py': 'StepSizeSlow', 'param': 'StepSizeSlow', 'type': 'int', 'default': 30, 'label': 'Slow step', 'sinput': False}, {'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'StepXCCX_', 'label': 'Indicator labels name', 'sinput': False}, {'mql': 'UpSymbol_Color', 'py': 'UpSymbol_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Growth symbol color', 'sinput': False}, {'mql': 'DnSymbol_Color', 'py': 'DnSymbol_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Downfall symbol color', 'sinput': False}, {'mql': 'IndName_Color', 'py': 'IndName_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Indicator name color', 'sinput': False}, {'mql': 'Symbols_Size', 'py': 'Symbols_Size', 'param': 'Symbols_Size', 'type': 'uint', 'default': 34, 'label': 'Signal symbols size', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'uint', 'default': 15, 'label': 'Indicator name font size', 'sinput': False}, {'mql': 'X_3', 'py': 'X_3', 'param': 'X_3', 'type': 'int', 'default': 120, 'label': 'Horizontal shift of the name', 'sinput': False}, {'mql': 'Y_3', 'py': 'Y_3', 'param': 'Y_3', 'type': 'int', 'default': 10, 'label': 'Vertical shift of the name', 'sinput': False}, {'mql': 'ShowIndName', 'py': 'ShowIndName', 'param': 'ShowIndName', 'type': 'bool', 'default': True, 'label': 'Indicator name display', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 3, 'label': 'Location corner', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 0, 'label': 'Horizontal shift', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 0, 'label': 'Vertical shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

DarkOrchid = 0xCC3299  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name
Teal = 0x808000  # MQL4 colour name

# enum APPLIED_PRICE
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('APPLIED_PRICE', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
Symbol_ = _input('Symbol_', '')  # Financial asset
Timeframe = _input('Timeframe', PERIOD_H6)  # Indicator timeframe for the indicator calculation
DSmoothMethod = _input('DSmoothMethod', MODE_JJMA)  # Price smoothing method
DPeriod = _input('DPeriod', 30)  # Moving average period
DPhase = _input('DPhase', 100)  # Smoothing parameter
MSmoothMethod = _input('MSmoothMethod', MODE_T3)  # Deviation smoothing method
MPeriod = _input('MPeriod', 7)  # Average deviation period
MPhase = _input('MPhase', 15)  # Deviation smoothing parameter
IPC = _input('IPC', PRICE_TYPICAL)  # Applied price
StepSizeFast = _input('StepSizeFast', 5)  # Fast step
StepSizeSlow = _input('StepSizeSlow', 30)  # Slow step
Symbols_Sirname = _input('Symbols_Sirname', 'StepXCCX_')  # Indicator labels name
Symbols_Size = _input('Symbols_Size', 34)  # Signal symbols size
Font_Size = _input('Font_Size', 15)  # Indicator name font size
X_3 = _input('X_3', 120)  # Horizontal shift of the name
Y_3 = _input('Y_3', 10)  # Vertical shift of the name
ShowIndName = _input('ShowIndName', True)  # Indicator name display
WhatCorner = _input('WhatCorner', CORNER_RIGHT_UPPER)  # Location corner
X_ = _input('X_', 0)  # Horizontal shift
Y_ = _input('Y_', 0)  # Vertical shift
StepXCCX_Handle = 0
min_rates_total = 0
X_0 = 0
X_1 = 0
X_2 = 0
X_3_ = 0
Yn = 0
Y_3_ = 0
name0 = ""
name1 = ""
name2 = ""
name3 = ""
IndName = ""
Symb = ""

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size):
    ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(chart_id, name, OBJPROP_CORNER, corner)
    ObjectSetInteger(chart_id, name, OBJPROP_ANCHOR, point)
    ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
    ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size):
    if ObjectFind(chart_id, name) == -1:
        CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
        ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
        ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)

def OnInit():
    global StepXCCX_Handle, Symb, X_0, X_1, X_2, X_3_, Y_3_, Yn, min_rates_total, name0, name1, name2, name3
    XMA = CXMA()
    min_rates_total = XMA.GetStartBars(DSmoothMethod, DPeriod, DPhase) + XMA.GetStartBars(MSmoothMethod, MPeriod, MPhase) + 3
    if Symbol_ != '':
        Symb = Symbol_
    else:
        Symb = Symbol()
    X_0 = X_
    X_1 = _uint(X_0 + (Symbols_Size * 1.1))
    X_2 = _uint(X_1 + (Symbols_Size * 1.1))
    Yn = Y_ + 5
    name0 = Symbols_Sirname + '0'
    name1 = Symbols_Sirname + '1'
    name2 = Symbols_Sirname + '2'
    if ShowIndName:
        Y_3_ = Yn + Y_3
        X_3_ = X_0 + X_3
        name3 = Symbols_Sirname + '3'
        StringConcatenate(_GlobRef(globals(), 'IndName'), 'StepXCCX(', Symb, ' ', GetStringTimeframe(Timeframe), ')')
    StepXCCX_Handle = iCustom(Symb, Timeframe, 'ColorStepXCCX', DSmoothMethod, DPeriod, DPhase, MSmoothMethod, MPeriod, MPhase, IPC, StepSizeFast, StepSizeSlow, 0)
    if StepXCCX_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ColorStepXCCX indicator')
    shortname = Box("")
    SmoothD = ""
    SmoothM = ""
    SmoothD = XMA.GetString_MA_Method(DSmoothMethod)
    SmoothM = XMA.GetString_MA_Method(MSmoothMethod)
    StringConcatenate(shortname, 'StepXCCX(', _str(DPeriod), ',', _str(MPeriod), ',', SmoothD, ',', SmoothM, StepSizeFast, ', ', StepSizeSlow, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def Deinit():
    if ObjectFind(0, name0) != -1:
        ObjectDelete(0, name0)
    if ObjectFind(0, name1) != -1:
        ObjectDelete(0, name1)
    if ObjectFind(0, name2) != -1:
        ObjectDelete(0, name2)
    if ObjectFind(0, name3) != -1:
        ObjectDelete(0, name3)

def OnDeinit(reason):
    Deinit()
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(StepXCCX_Handle) < min_rates_total:
        return 0
    to_copy = 3
    dxccx0 = 0.0
    dxccx1 = 0.0
    dxccx2 = 0.0
    XCCX1 = Arr(3, 0.0, dyn=False)
    XCCX2 = Arr(3, 0.0, dyn=False)
    Color0 = 0
    Color1 = 0
    Color2 = 0
    if CopyBuffer(StepXCCX_Handle, 0, 0, to_copy, XCCX1) <= 0:
        return 0
    if CopyBuffer(StepXCCX_Handle, 1, 0, to_copy, XCCX2) <= 0:
        return 0
    dxccx0 = XCCX1[2] - XCCX2[2]
    dxccx1 = XCCX1[1] - XCCX2[1]
    dxccx2 = XCCX1[0] - XCCX2[0]
    if dxccx0 < 0:
        Color0 = DnSymbol_Color
    else:
        Color0 = UpSymbol_Color
    if dxccx1 < 0:
        Color1 = DnSymbol_Color
    else:
        Color1 = UpSymbol_Color
    if dxccx2 < 0:
        Color2 = DnSymbol_Color
    else:
        Color2 = UpSymbol_Color
    if ShowIndName:
        SetTLabel(0, name3, 0, WhatCorner, 2 * WhatCorner, X_3_, Y_3_, IndName, IndName_Color, 'Georgia', Font_Size)
    SetTLabel(0, name0, 0, WhatCorner, 2 * WhatCorner, X_0, Yn, 'l', Color0, 'Wingdings', Symbols_Size)
    SetTLabel(0, name1, 0, WhatCorner, 2 * WhatCorner, X_1, Yn, 'l', Color1, 'Wingdings', Symbols_Size)
    SetTLabel(0, name2, 0, WhatCorner, 2 * WhatCorner, X_2, Yn, 'l', Color2, 'Wingdings', Symbols_Size)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
UpSymbol_Color = _input('UpSymbol_Color', _uint(Teal))  # Growth symbol color
DnSymbol_Color = _input('DnSymbol_Color', _uint(Magenta))  # Downfall symbol color
IndName_Color = _input('IndName_Color', _uint(DarkOrchid))  # Indicator name color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StepxccxHtfSignal(_MQL5Indicator):
    name = 'stepxccx_htf_signal_'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Indicator timeframe for the indicator calculation
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Price smoothing method
        'DPeriod': 30,  # Moving average period
        'DPhase': 100,  # Smoothing parameter
        'MSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Deviation smoothing method
        'MPeriod': 7,  # Average deviation period
        'MPhase': 15,  # Deviation smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=6),  # Applied price
        'StepSizeFast': 5,  # Fast step
        'StepSizeSlow': 30,  # Slow step
        'Symbols_Size': 34,  # Signal symbols size
        'Font_Size': 15,  # Indicator name font size
        'X_3': 120,  # Horizontal shift of the name
        'Y_3': 10,  # Vertical shift of the name
        'ShowIndName': True,  # Indicator name display
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Location corner
        'X_': 0,  # Horizontal shift
        'Y_': 0,  # Vertical shift
    }

