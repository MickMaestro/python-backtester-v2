"""slow-stoch_htf_signal — converted from MQL5: MQL5 Indicators/Slow-Stoch_HTF_Signal/slow-stoch_htf_signal.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'slow-stoch_htf_signal', 'source': 'MQL5 Indicators/Slow-Stoch_HTF_Signal/slow-stoch_htf_signal.mq5', 'folder': 'Slow-Stoch_HTF_Signal', 'inputs': [{'mql': 'Symbol_', 'py': 'Symbol_', 'param': None, 'type': 'string', 'default': '', 'label': 'Financial asset', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Timeframe for the indicator calculation', 'sinput': False}, {'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'STO_Method', 'py': 'STO_Method', 'param': 'STO_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'Method of averaging', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 5, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 0, 'label': 'Signal bar index, 0 is a current bar', 'sinput': False}, {'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'Slow-Stoch_Label_', 'label': 'Indicator labels name', 'sinput': False}, {'mql': 'UpSymol_Color', 'py': 'UpSymol_Color', 'param': None, 'type': 'color', 'default': 16760576, 'label': 'Growth symbol color', 'sinput': False}, {'mql': 'DnSymol_Color', 'py': 'DnSymol_Color', 'param': None, 'type': 'color', 'default': 9639167, 'label': 'Fall symbol color', 'sinput': False}, {'mql': 'IndName_Color', 'py': 'IndName_Color', 'param': None, 'type': 'color', 'default': 13382297, 'label': 'Indicator name color', 'sinput': False}, {'mql': 'Symbols_Size', 'py': 'Symbols_Size', 'param': 'Symbols_Size', 'type': 'uint', 'default': 60, 'label': 'Signal symbols size', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'uint', 'default': 10, 'label': 'Indicator name font size', 'sinput': False}, {'mql': 'X_1', 'py': 'X_1', 'param': 'X_1', 'type': 'int', 'default': 5, 'label': 'Horizontal shift of the name', 'sinput': False}, {'mql': 'Y_1', 'py': 'Y_1', 'param': 'Y_1', 'type': 'int', 'default': -15, 'label': 'Vertical shift of the name', 'sinput': False}, {'mql': 'ShowIndName', 'py': 'ShowIndName', 'param': 'ShowIndName', 'type': 'bool', 'default': True, 'label': 'Indicator name display', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 3, 'label': 'Location corner', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 0, 'label': 'Horizontal shift', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'Vertical shift', 'sinput': False}, {'mql': 'alert_mode', 'py': 'alert_mode', 'param': 'alert_mode', 'type': 'int', 'default': 0, 'label': 'Triggering indication option', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'Number of produced alerts', 'sinput': False}, {'mql': 'Push', 'py': 'Push', 'param': 'Push', 'type': 'bool', 'default': True, 'label': 'Allow push notifications', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_ALERT_MODE
OnlySound = 0
OnlyAlert = 1
_enum('ENUM_ALERT_MODE', {0: 'OnlySound', 1: 'OnlyAlert'})

# ---- inputs and global variables
Symbol_ = _input('Symbol_', '')  # Financial asset
Timeframe = _input('Timeframe', PERIOD_H6)  # Timeframe for the indicator calculation
KPeriod = _input('KPeriod', 5)
DPeriod = _input('DPeriod', 3)
Slowing = _input('Slowing', 3)
STO_Method = _input('STO_Method', MODE_SMA)
Price_field = _input('Price_field', STO_LOWHIGH)
XMA_Method = _input('XMA_Method', MODE_JJMA)  # Method of averaging
XLength = _input('XLength', 5)  # Smoothing depth
XPhase = _input('XPhase', 15)  # Smoothing parameter
SignalBar = _input('SignalBar', 0)  # Signal bar index, 0 is a current bar
Symbols_Sirname = _input('Symbols_Sirname', 'Slow-Stoch_Label_')  # Indicator labels name
UpSymol_Color = _input('UpSymol_Color', clrDeepSkyBlue)  # Growth symbol color
DnSymol_Color = _input('DnSymol_Color', clrDeepPink)  # Fall symbol color
IndName_Color = _input('IndName_Color', clrDarkOrchid)  # Indicator name color
Symbols_Size = _input('Symbols_Size', 60)  # Signal symbols size
Font_Size = _input('Font_Size', 10)  # Indicator name font size
X_1 = _input('X_1', 5)  # Horizontal shift of the name
Y_1 = _input('Y_1', -15)  # Vertical shift of the name
ShowIndName = _input('ShowIndName', True)  # Indicator name display
WhatCorner = _input('WhatCorner', CORNER_RIGHT_UPPER)  # Location corner
X_ = _input('X_', 0)  # Horizontal shift
Y_ = _input('Y_', 20)  # Vertical shift
alert_mode = _input('alert_mode', OnlySound)  # Triggering indication option
AlertCount = _input('AlertCount', 0)  # Number of produced alerts
Push = _input('Push', True)  # Allow push notifications
SlowStoch_Handle = 0
min_rates_total = 0
X_0 = 0
Yn = 0
X_1_ = 0
Y_1_ = 0
name0 = ""
name1 = ""
IndName = ""
Symb = ""
BuySignal = ""
SellSignal = ""

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
    global BuySignal, SellSignal, SlowStoch_Handle, Symb, X_0, X_1_, Y_1_, Yn, min_rates_total, name0, name1
    min_rates_total = _int(KPeriod + DPeriod + Slowing)
    min_rates_total += GetStartBars(XMA_Method, XLength, XPhase)
    min_rates_total += _int(SignalBar)
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
        StringConcatenate(_GlobRef(globals(), 'IndName'), 'Slow-Stoch', '(', Symb, ' ', GetStringTimeframe(Timeframe), ')')
    SlowStoch_Handle = iCustom(Symb, Timeframe, 'Slow-Stoch', KPeriod, DPeriod, Slowing, STO_Method, Price_field, XMA_Method, XLength, XPhase, 0)
    if SlowStoch_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the Slow-Stoch indicator')
        return INIT_FAILED
    BuySignal = IndName + ': ' + 'Buy signal'
    SellSignal = IndName + ': ' + 'Sell signal'
    shortname = name1
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def Deinit():
    if ObjectFind(0, name0) != -1:
        ObjectDelete(0, name0)
    if ObjectFind(0, name1) != -1:
        ObjectDelete(0, name1)

def OnDeinit(reason):
    Deinit()
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_RePush, _s_OnCalculate_buycount, _s_OnCalculate_sellcount
    if BarsCalculated(SlowStoch_Handle) < min_rates_total:
        return 0
    if BarsCalculated(SlowStoch_Handle) < Bars(Symb, Timeframe):
        return prev_calculated
    trend = 0
    Up = Arr(2, 0.0, dyn=False)
    Dn = Arr(2, 0.0, dyn=False)
    Color0 = clrNONE
    SignSymbol = ""
    signal = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        _s_OnCalculate_buycount = 0
        _s_OnCalculate_sellcount = 0
    else:
        if (prev_calculated == rates_total and SignalBar) and ((not _s_OnCalculate_buycount) or (not _s_OnCalculate_sellcount)):
            return rates_total
    if CopyBuffer(SlowStoch_Handle, 0, SignalBar, 2, Up) <= 0:
        return prev_calculated
    if CopyBuffer(SlowStoch_Handle, 1, SignalBar, 2, Dn) <= 0:
        return prev_calculated
    if Up[1] > Dn[1]:
        trend = 1
        if Up[0] >= Dn[0]:
            signal = True
    if Up[1] < Dn[1]:
        trend = -1
        if Up[0] <= Dn[0]:
            signal = True
    if (prev_calculated != rates_total and AlertCount) and signal:
        _s_OnCalculate_buycount = AlertCount
        _s_OnCalculate_sellcount = AlertCount
    if trend > 0:
        Color0 = UpSymol_Color
        if signal:
            SignSymbol = 'ж'
            if (Push and SignalBar) and prev_calculated != rates_total:
                _s_OnCalculate_RePush = True
            if _s_OnCalculate_RePush:
                if SendNotification(BuySignal):
                    _s_OnCalculate_RePush = False
            if _s_OnCalculate_buycount and SignalBar:
                _sw1 = alert_mode
                if _sw1 == OnlyAlert:
                    Alert(BuySignal)
                elif _sw1 == OnlySound:
                    PlaySound('alert.wav')
                _s_OnCalculate_buycount -= 1
        else:
            SignSymbol = 'в'
    if trend < 0:
        Color0 = DnSymol_Color
        if signal:
            SignSymbol = 'и'
            if (Push and SignalBar) and prev_calculated != rates_total:
                _s_OnCalculate_RePush = True
            if _s_OnCalculate_RePush:
                if SendNotification(SellSignal):
                    _s_OnCalculate_RePush = False
            if _s_OnCalculate_sellcount and SignalBar:
                _sw2 = alert_mode
                if _sw2 == OnlyAlert:
                    Alert(SellSignal)
                elif _sw2 == OnlySound:
                    PlaySound('alert.wav')
                _s_OnCalculate_sellcount -= 1
        else:
            SignSymbol = 'в'
    if trend:
        if ShowIndName:
            SetTLabel(0, name1, 0, WhatCorner, 2 * WhatCorner, X_1_, Y_1_, IndName, IndName, IndName_Color, 'Georgia', Font_Size)
        if signal:
            SetTLabel(0, name0, 0, WhatCorner, 2 * WhatCorner, X_0, Yn, SignSymbol, IndName, Color0, 'Wingdings 3', Symbols_Size)
        else:
            SetTLabel(0, name0, 0, WhatCorner, 2 * WhatCorner, X_0, Yn, SignSymbol, IndName, Color0, 'Wingdings 3', Symbols_Size)
    else:
        Deinit()
    ChartRedraw(0)
    return rates_total

# ---- static local variables
_s_OnCalculate_buycount = 0
_s_OnCalculate_sellcount = 0
_s_OnCalculate_RePush = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SlowStochHtfSignal(_MQL5Indicator):
    name = 'slow-stoch_htf_signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Timeframe for the indicator calculation
        'KPeriod': 5,
        'DPeriod': 3,
        'Slowing': 3,
        'STO_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Method of averaging
        'XLength': 5,  # Smoothing depth
        'XPhase': 15,  # Smoothing parameter
        'SignalBar': 0,  # Signal bar index, 0 is a current bar
        'Symbols_Size': 60,  # Signal symbols size
        'Font_Size': 10,  # Indicator name font size
        'X_1': 5,  # Horizontal shift of the name
        'Y_1': -15,  # Vertical shift of the name
        'ShowIndName': True,  # Indicator name display
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Location corner
        'X_': 0,  # Horizontal shift
        'Y_': 20,  # Vertical shift
        'alert_mode': _Choice({0: 'only sound', 1: 'only alert'}, default=0),  # Triggering indication option
        'AlertCount': 0,  # Number of produced alerts
        'Push': True,  # Allow push notifications
    }

