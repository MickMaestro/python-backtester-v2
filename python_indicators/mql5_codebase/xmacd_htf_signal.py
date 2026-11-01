"""xmacd_htf_signal — converted from MQL5: MQL5 Indicators/XMACD_HTF_Signal/xmacd_htf_signal.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'xmacd_htf_signal', 'source': 'MQL5 Indicators/XMACD_HTF_Signal/xmacd_htf_signal.mq5', 'folder': 'XMACD_HTF_Signal', 'inputs': [{'mql': 'Symbol_', 'py': 'Symbol_', 'param': None, 'type': 'string', 'default': '', 'label': 'Financial asset', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Indicator timeframe for the indicator calculation', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'Histogram smoothing method', 'sinput': False}, {'mql': 'Fast_XMA', 'py': 'Fast_XMA', 'param': 'Fast_XMA', 'type': 'int', 'default': 12, 'label': 'Fast moving average period', 'sinput': False}, {'mql': 'Slow_XMA', 'py': 'Slow_XMA', 'param': 'Slow_XMA', 'type': 'int', 'default': 26, 'label': 'Slow moving average period', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'Signal_Method', 'py': 'Signal_Method', 'param': 'Signal_Method', 'type': 'int', 'default': 4, 'label': 'Signal line smoothing method', 'sinput': False}, {'mql': 'Signal_XMA', 'py': 'Signal_XMA', 'param': 'Signal_XMA', 'type': 'int', 'default': 9, 'label': 'Signal line period', 'sinput': False}, {'mql': 'Signal_XPhase', 'py': 'Signal_XPhase', 'param': 'Signal_XPhase', 'type': 'int', 'default': 100, 'label': 'Signal line parameter', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'symbols_Sirname', 'py': 'symbols_Sirname', 'param': None, 'type': 'string', 'default': 'XMACD_Label_', 'label': 'Indicator labels name', 'sinput': False}, {'mql': 'Upsymbol_Color', 'py': 'Upsymbol_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Growth symbol color', 'sinput': False}, {'mql': 'Dnsymbol_Color', 'py': 'Dnsymbol_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Downfall symbol color', 'sinput': False}, {'mql': 'IndName_Color', 'py': 'IndName_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Indicator name color', 'sinput': False}, {'mql': 'symbols_Size', 'py': 'symbols_Size', 'param': 'symbols_Size', 'type': 'uint', 'default': 34, 'label': 'Signal symbols size', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'uint', 'default': 15, 'label': 'Indicator name font size', 'sinput': False}, {'mql': 'X_3', 'py': 'X_3', 'param': 'X_3', 'type': 'int', 'default': 120, 'label': 'Horizontal shift of the name', 'sinput': False}, {'mql': 'Y_3', 'py': 'Y_3', 'param': 'Y_3', 'type': 'int', 'default': 10, 'label': 'Vertical shift of the name', 'sinput': False}, {'mql': 'ShowIndName', 'py': 'ShowIndName', 'param': 'ShowIndName', 'type': 'bool', 'default': True, 'label': 'Indicator name display', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 3, 'label': 'Location corner', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 0, 'label': 'Horizontal shift', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 0, 'label': 'Vertical shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

DarkOrchid = 0xCC3299  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

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
XMA_Method = _input('XMA_Method', MODE_T3)  # Histogram smoothing method
Fast_XMA = _input('Fast_XMA', 12)  # Fast moving average period
Slow_XMA = _input('Slow_XMA', 26)  # Slow moving average period
XPhase = _input('XPhase', 100)  # Smoothing parameter
Signal_Method = _input('Signal_Method', MODE_JJMA)  # Signal line smoothing method
Signal_XMA = _input('Signal_XMA', 9)  # Signal line period
Signal_XPhase = _input('Signal_XPhase', 100)  # Signal line parameter
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # Price constant
symbols_Sirname = _input('symbols_Sirname', 'XMACD_Label_')  # Indicator labels name
symbols_Size = _input('symbols_Size', 34)  # Signal symbols size
Font_Size = _input('Font_Size', 15)  # Indicator name font size
X_3 = _input('X_3', 120)  # Horizontal shift of the name
Y_3 = _input('Y_3', 10)  # Vertical shift of the name
ShowIndName = _input('ShowIndName', True)  # Indicator name display
WhatCorner = _input('WhatCorner', CORNER_RIGHT_UPPER)  # Location corner
X_ = _input('X_', 0)  # Horizontal shift
Y_ = _input('Y_', 0)  # Vertical shift
XMACD_Handle = 0
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
    global Symb, XMACD_Handle, X_0, X_1, X_2, X_3_, Y_3_, Yn, min_rates_total, name0, name1, name2, name3
    min_rates_total = MathMax(Fast_XMA, XMA.GetStartBars(XMA_Method, Slow_XMA, XPhase)) + XMA.GetStartBars(Signal_Method, Signal_XMA, Signal_XPhase) + 3
    if Symbol_ != '':
        Symb = Symbol_
    else:
        Symb = Symbol()
    X_0 = X_
    X_1 = _uint(X_0 + (symbols_Size * 1.1))
    X_2 = _uint(X_1 + (symbols_Size * 1.1))
    Yn = Y_ + 5
    name0 = symbols_Sirname + '0'
    name1 = symbols_Sirname + '1'
    name2 = symbols_Sirname + '2'
    if ShowIndName:
        Y_3_ = Yn + Y_3
        X_3_ = X_0 + X_3
        name3 = symbols_Sirname + '3'
        StringConcatenate(_GlobRef(globals(), 'IndName'), 'XMACD(', Symb, ' ', GetStringTimeframe(Timeframe), ')')
    XMACD_Handle = iCustom(Symb, Timeframe, 'XMACD', XMA_Method, Fast_XMA, Slow_XMA, XPhase, Signal_Method, Signal_XMA, Signal_XPhase, AppliedPrice)
    if XMACD_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of XMACD indicator')
        return INIT_FAILED
    shortname = Box("")
    Smooth1 = XMA.GetString_MA_Method(XMA_Method)
    Smooth2 = XMA.GetString_MA_Method(Signal_Method)
    StringConcatenate(shortname, 'XMACD( ', Fast_XMA, ', ', Slow_XMA, ', ', Signal_XMA, ', ', Smooth1, ', ', Smooth2, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

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
    if BarsCalculated(XMACD_Handle) < min_rates_total:
        return 0
    if BarsCalculated(XMACD_Handle) < Bars(Symbol(), Timeframe):
        return prev_calculated
    to_copy = 3
    dxmacd0 = 0.0
    dxmacd1 = 0.0
    dxmacd2 = 0.0
    XMACD = Arr(3, 0.0, dyn=False)
    SIGN = Arr(3, 0.0, dyn=False)
    Color0 = 0
    Color1 = 0
    Color2 = 0
    if CopyBuffer(XMACD_Handle, 0, 0, to_copy, XMACD) <= 0:
        return 0
    if CopyBuffer(XMACD_Handle, 1, 0, to_copy, SIGN) <= 0:
        return 0
    dxmacd0 = XMACD[2] - SIGN[2]
    dxmacd1 = XMACD[1] - SIGN[1]
    dxmacd2 = XMACD[0] - SIGN[0]
    if dxmacd0 < 0:
        Color0 = Dnsymbol_Color
    else:
        Color0 = Upsymbol_Color
    if dxmacd1 < 0:
        Color1 = Dnsymbol_Color
    else:
        Color1 = Upsymbol_Color
    if dxmacd2 < 0:
        Color2 = Dnsymbol_Color
    else:
        Color2 = Upsymbol_Color
    if ShowIndName:
        SetTLabel(0, name3, 0, WhatCorner, 2 * WhatCorner, X_3_, Y_3_, IndName, IndName_Color, 'Georgia', Font_Size)
    SetTLabel(0, name0, 0, WhatCorner, 2 * WhatCorner, X_0, Yn, 't', Color0, 'Wingdings 2', symbols_Size)
    SetTLabel(0, name1, 0, WhatCorner, 2 * WhatCorner, X_1, Yn, 'u', Color1, 'Wingdings 2', symbols_Size)
    SetTLabel(0, name2, 0, WhatCorner, 2 * WhatCorner, X_2, Yn, 'v', Color2, 'Wingdings 2', symbols_Size)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
Upsymbol_Color = _input('Upsymbol_Color', _uint(Lime))  # Growth symbol color
Dnsymbol_Color = _input('Dnsymbol_Color', _uint(Red))  # Downfall symbol color
IndName_Color = _input('IndName_Color', _uint(DarkOrchid))  # Indicator name color
XMA = _alloc(CXMA)
XMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XmacdHtfSignal(_MQL5Indicator):
    name = 'xmacd_htf_signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Indicator timeframe for the indicator calculation
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Histogram smoothing method
        'Fast_XMA': 12,  # Fast moving average period
        'Slow_XMA': 26,  # Slow moving average period
        'XPhase': 100,  # Smoothing parameter
        'Signal_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Signal line smoothing method
        'Signal_XMA': 9,  # Signal line period
        'Signal_XPhase': 100,  # Signal line parameter
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'symbols_Size': 34,  # Signal symbols size
        'Font_Size': 15,  # Indicator name font size
        'X_3': 120,  # Horizontal shift of the name
        'Y_3': 10,  # Vertical shift of the name
        'ShowIndName': True,  # Indicator name display
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Location corner
        'X_': 0,  # Horizontal shift
        'Y_': 0,  # Vertical shift
    }

