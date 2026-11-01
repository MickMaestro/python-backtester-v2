"""parabolic_htf_signal — converted from MQL5: MQL5 Indicators/Parabolic_HTF_Signal/parabolic_htf_signal.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'parabolic_htf_signal', 'source': 'MQL5 Indicators/Parabolic_HTF_Signal/parabolic_htf_signal.mq5', 'folder': 'Parabolic_HTF_Signal', 'inputs': [{'mql': 'Symbol_', 'py': 'Symbol_', 'param': None, 'type': 'string', 'default': '', 'label': 'Financial asset', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Indicator calculation timeframe', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'double', 'default': 0.02, 'label': 'Step', 'sinput': False}, {'mql': 'Maximum', 'py': 'Maximum', 'param': 'Maximum', 'type': 'double', 'default': 0.2, 'label': 'Maximum', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 0, 'label': 'Signal bar index, 0 is a current bar', 'sinput': False}, {'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'Parabolic_Label_', 'label': 'Indicator labels names', 'sinput': False}, {'mql': 'Up1Symbol_Color', 'py': 'Up1Symbol_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Symbol color for long', 'sinput': False}, {'mql': 'UpSymbol_Color', 'py': 'UpSymbol_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Growth symbol color', 'sinput': False}, {'mql': 'DnSymbol_Color', 'py': 'DnSymbol_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Downfall symbol color', 'sinput': False}, {'mql': 'Dn1Symbol_Color', 'py': 'Dn1Symbol_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Symbol color for short', 'sinput': False}, {'mql': 'IndName_Color', 'py': 'IndName_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Indicator name color', 'sinput': False}, {'mql': 'Symbols_Size', 'py': 'Symbols_Size', 'param': 'Symbols_Size', 'type': 'uint', 'default': 60, 'label': 'Signal symbols size', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'uint', 'default': 10, 'label': 'Indicator name font size', 'sinput': False}, {'mql': 'X_1', 'py': 'X_1', 'param': 'X_1', 'type': 'int', 'default': 5, 'label': 'Horizontal shift of the name', 'sinput': False}, {'mql': 'Y_1', 'py': 'Y_1', 'param': 'Y_1', 'type': 'int', 'default': -15, 'label': 'Vertical shift of the name', 'sinput': False}, {'mql': 'ShowIndName', 'py': 'ShowIndName', 'param': 'ShowIndName', 'type': 'bool', 'default': True, 'label': 'Indicator name display', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 3, 'label': 'Location corner', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 0, 'label': 'Horizontal shift', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'Vertical shift', 'sinput': False}, {'mql': 'alert_mode', 'py': 'alert_mode', 'param': 'alert_mode', 'type': 'int', 'default': 0, 'label': 'Actuation indication version', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'Number of submitted alerts', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

BlueViolet = 0xE22B8A  # MQL4 colour name
DarkOrchid = 0xCC3299  # MQL4 colour name
DeepPink = 0x9314FF  # MQL4 colour name
MediumBlue = 0xCD0000  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# enum ENUM_ALERT_MODE
OnlySound = 0
OnlyAlert = 1
_enum('ENUM_ALERT_MODE', {0: 'OnlySound', 1: 'OnlyAlert'})

# ---- inputs and global variables
Symbol_ = _input('Symbol_', '')  # Financial asset
Timeframe = _input('Timeframe', PERIOD_H6)  # Indicator calculation timeframe
Step = _input('Step', 0.02)  # Step
Maximum = _input('Maximum', 0.2)  # Maximum
SignalBar = _input('SignalBar', 0)  # Signal bar index, 0 is a current bar
Symbols_Sirname = _input('Symbols_Sirname', 'Parabolic_Label_')  # Indicator labels names
Symbols_Size = _input('Symbols_Size', 60)  # Signal symbols size
Font_Size = _input('Font_Size', 10)  # Indicator name font size
X_1 = _input('X_1', 5)  # Horizontal shift of the name
Y_1 = _input('Y_1', -15)  # Vertical shift of the name
ShowIndName = _input('ShowIndName', True)  # Indicator name display
WhatCorner = _input('WhatCorner', CORNER_RIGHT_UPPER)  # Location corner
X_ = _input('X_', 0)  # Horizontal shift
Y_ = _input('Y_', 20)  # Vertical shift
alert_mode = _input('alert_mode', OnlySound)  # Actuation indication version
AlertCount = _input('AlertCount', 0)  # Number of submitted alerts
Parabolic_Handle = 0
min_rates_total = 0
X_0 = 0
Yn = 0
X_1_ = 0
Y_1_ = 0
name0 = ""
name1 = ""
IndName = ""
Symb = ""

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, textTT, Color, Font, Size):
    ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(chart_id, name, OBJPROP_CORNER, corner)
    ObjectSetInteger(chart_id, name, OBJPROP_ANCHOR, point)
    ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
    ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)
    ObjectSetString(chart_id, name, OBJPROP_TOOLTIP, textTT)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetTLabel(chart_id, name, nwin, corner, point, X, Y, text, textTT, Color, Font, Size):
    if ObjectFind(chart_id, name) == -1:
        CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, textTT, Color, Font, Size)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
        ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
        ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)

def OnInit():
    global Parabolic_Handle, Symb, X_0, X_1_, Y_1_, Yn, min_rates_total, name0, name1
    min_rates_total = 10 + _int(SignalBar)
    if Symbol_ != '':
        Symb = Symbol_
    else:
        Symb = Symbol()
    X_0 = X_
    Yn = Y_ + 5
    name0 = Symbols_Sirname + '0'
    if ShowIndName:
        Y_1_ = Yn + Y_1
        X_1_ = X_0 + X_1
        name1 = Symbols_Sirname + '1'
        StringConcatenate(_GlobRef(globals(), 'IndName'), 'Parabolic(', Symb, ' ', GetStringTimeframe(Timeframe), ')')
    Parabolic_Handle = iCustom(Symb, Timeframe, 'Color_Parabolic', Step, Maximum)
    if Parabolic_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Parabolic indicator')
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Parabolic')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_FAILED

def Deinit():
    if ObjectFind(0, name0) != -1:
        ObjectDelete(0, name0)
    if ObjectFind(0, name1) != -1:
        ObjectDelete(0, name1)

def OnDeinit(reason):
    Deinit()
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_bartime, _s_OnCalculate_buycount, _s_OnCalculate_sellcount
    if BarsCalculated(Parabolic_Handle) < min_rates_total:
        return 0
    if BarsCalculated(Parabolic_Handle) < Bars(Symb, Timeframe):
        return prev_calculated
    limit = rates_total - prev_calculated
    if limit < _int(SignalBar) and limit >= 0:
        return rates_total
    UpSar = Arr(1, 0.0, dyn=False)
    DnSar = Arr(1, 0.0, dyn=False)
    BuySar = Arr(1, 0.0, dyn=False)
    SellSar = Arr(1, 0.0, dyn=False)
    Color0 = clrNONE
    SignSymbol = ""
    if CopyBuffer(Parabolic_Handle, 0, SignalBar, 1, DnSar) <= 0:
        return 0
    if CopyBuffer(Parabolic_Handle, 1, SignalBar, 1, UpSar) <= 0:
        return 0
    if CopyBuffer(Parabolic_Handle, 2, SignalBar, 1, SellSar) <= 0:
        return 0
    if CopyBuffer(Parabolic_Handle, 3, SignalBar, 1, BuySar) <= 0:
        return 0
    if CopyTime(Symb, Timeframe, SignalBar, 1, _s_OnCalculate_TIME) <= 0:
        return 0
    if _s_OnCalculate_TIME[0] != _s_OnCalculate_bartime and AlertCount:
        _s_OnCalculate_buycount = AlertCount
        _s_OnCalculate_sellcount = AlertCount
        _s_OnCalculate_bartime = _s_OnCalculate_TIME[0]
    if BuySar[0]:
        Color0 = Up1Symbol_Color
        SignSymbol = 'й'
        if _s_OnCalculate_buycount:
            if alert_mode == OnlyAlert:
                Alert(IndName + ': Signal for buying')
            if alert_mode == OnlySound:
                PlaySound('alert.wav')
            _s_OnCalculate_buycount -= 1
    if SellSar[0]:
        Color0 = Dn1Symbol_Color
        SignSymbol = 'к'
        if _s_OnCalculate_sellcount:
            if alert_mode == OnlyAlert:
                Alert(IndName + ': Signal for selling')
            if alert_mode == OnlySound:
                PlaySound('alert.wav')
            _s_OnCalculate_sellcount -= 1
    if (not BuySar[0]) and (not SellSar[0]):
        if UpSar[0]:
            Color0 = UpSymbol_Color
            SignSymbol = 'l'
        if DnSar[0]:
            Color0 = DnSymbol_Color
            SignSymbol = 'l'
    if ShowIndName:
        SetTLabel(0, name1, 0, WhatCorner, 2 * WhatCorner, X_1_, Y_1_, IndName, IndName, IndName_Color, 'Georgia', Font_Size)
    SetTLabel(0, name0, 0, WhatCorner, 2 * WhatCorner, X_0, Yn, SignSymbol, IndName, Color0, 'Wingdings', Symbols_Size)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
Up1Symbol_Color = _input('Up1Symbol_Color', _uint(BlueViolet))  # Symbol color for long
UpSymbol_Color = _input('UpSymbol_Color', _uint(MediumBlue))  # Growth symbol color
DnSymbol_Color = _input('DnSymbol_Color', _uint(Red))  # Downfall symbol color
Dn1Symbol_Color = _input('Dn1Symbol_Color', _uint(DeepPink))  # Symbol color for short
IndName_Color = _input('IndName_Color', _uint(DarkOrchid))  # Indicator name color

# ---- static local variables
_s_OnCalculate_TIME = Arr(1, 0, dyn=False)
_s_OnCalculate_bartime = 0
_s_OnCalculate_buycount = 0
_s_OnCalculate_sellcount = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ParabolicHtfSignal(_MQL5Indicator):
    name = 'parabolic_htf_signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Indicator calculation timeframe
        'Step': 0.02,  # Step
        'Maximum': 0.2,  # Maximum
        'SignalBar': 0,  # Signal bar index, 0 is a current bar
        'Symbols_Size': 60,  # Signal symbols size
        'Font_Size': 10,  # Indicator name font size
        'X_1': 5,  # Horizontal shift of the name
        'Y_1': -15,  # Vertical shift of the name
        'ShowIndName': True,  # Indicator name display
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Location corner
        'X_': 0,  # Horizontal shift
        'Y_': 20,  # Vertical shift
        'alert_mode': _Choice({0: 'only sound', 1: 'only alert'}, default=0),  # Actuation indication version
        'AlertCount': 0,  # Number of submitted alerts
    }

