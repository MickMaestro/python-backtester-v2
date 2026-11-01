"""silvertrend_htf_signal — converted from MQL5: MQL5 Indicators/SilverTrend_HTF_Signal/silvertrend_htf_signal.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'indicator_buffers': 0, 'indicator_plots': 0, 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'silvertrend_htf_signal', 'source': 'MQL5 Indicators/SilverTrend_HTF_Signal/silvertrend_htf_signal.mq5', 'folder': 'SilverTrend_HTF_Signal', 'inputs': [{'mql': 'Symbol_', 'py': 'Symbol_', 'param': None, 'type': 'string', 'default': '', 'label': 'Financial asset', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Indicator timeframe for the indicator calculation', 'sinput': False}, {'mql': 'RISK', 'py': 'RISK', 'param': 'RISK', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 0, 'label': 'Signal bar index, 0 is a current bar', 'sinput': False}, {'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'SilverTrend_Label_', 'label': 'Indicator labels name', 'sinput': False}, {'mql': 'UpSymbol_Color', 'py': 'UpSymbol_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Growth symbol color', 'sinput': False}, {'mql': 'DnSymbol_Color', 'py': 'DnSymbol_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Downfall symbol color', 'sinput': False}, {'mql': 'IndName_Color', 'py': 'IndName_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Indicator name color', 'sinput': False}, {'mql': 'Symbols_Size', 'py': 'Symbols_Size', 'param': 'Symbols_Size', 'type': 'uint', 'default': 60, 'label': 'Signal symbols size', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'uint', 'default': 10, 'label': 'Indicator name font size', 'sinput': False}, {'mql': 'X_1', 'py': 'X_1', 'param': 'X_1', 'type': 'int', 'default': 5, 'label': 'Horizontal shift of the name', 'sinput': False}, {'mql': 'Y_1', 'py': 'Y_1', 'param': 'Y_1', 'type': 'int', 'default': -15, 'label': 'Vertical shift of the name', 'sinput': False}, {'mql': 'ShowIndName', 'py': 'ShowIndName', 'param': 'ShowIndName', 'type': 'bool', 'default': True, 'label': 'Indicator name display', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 3, 'label': 'Location corner', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 0, 'label': 'Horizontal shift', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'Vertical shift', 'sinput': False}, {'mql': 'alert_mode', 'py': 'alert_mode', 'param': 'alert_mode', 'type': 'int', 'default': 0, 'label': 'Actuation indication version', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'Number of submitted alerts', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DarkOrchid = 0xCC3299  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name

# enum ENUM_ALERT_MODE
OnlySound = 0
OnlyAlert = 1
_enum('ENUM_ALERT_MODE', {0: 'OnlySound', 1: 'OnlyAlert'})

# ---- inputs and global variables
Symbol_ = _input('Symbol_', '')  # Financial asset
Timeframe = _input('Timeframe', PERIOD_H6)  # Indicator timeframe for the indicator calculation
RISK = _input('RISK', 3)
SignalBar = _input('SignalBar', 0)  # Signal bar index, 0 is a current bar
Symbols_Sirname = _input('Symbols_Sirname', 'SilverTrend_Label_')  # Indicator labels name
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
SilverTrend_Handle = 0
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
        ObjectSetString(chart_id, name, OBJPROP_FONT, Font)

def OnInit():
    global SilverTrend_Handle, Symb, X_0, X_1_, Y_1_, Yn, min_rates_total, name0, name1
    min_rates_total = (MathMax(3 + (RISK * 2), 4) + 1) + _int(SignalBar)
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
        StringConcatenate(_GlobRef(globals(), 'IndName'), 'SilverTrend', '(', Symb, ' ', GetStringTimeframe(Timeframe), ')')
    SilverTrend_Handle = iCustom(Symb, Timeframe, 'SilverTrend_Signal', RISK, 0)
    if SilverTrend_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the SilverTrend_Signal indicator')
        return INIT_FAILED
    shortname = Box("")
    StringConcatenate(shortname, 'SilverTrend', '( ', RISK, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
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
    global _s_OnCalculate_buycount, _s_OnCalculate_prev_time, _s_OnCalculate_sellcount, _s_OnCalculate_trend_
    if BarsCalculated(SilverTrend_Handle) < min_rates_total:
        return 0
    if BarsCalculated(SilverTrend_Handle) < Bars(Symb, Timeframe):
        return prev_calculated
    limit = 0
    trend = 0
    UpSTR = Arr(0, 0.0)
    DnSTR = Arr(0, 0.0)
    rates_time = 0
    TIME = Arr(1, 0, dyn=False)
    Color0 = clrNONE
    SignSymbol = ""
    signal = False
    if CopyTime(Symb, Timeframe, SignalBar, 1, TIME) <= 0:
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        _s_OnCalculate_prev_time = time[0]
        _s_OnCalculate_trend_ = 0
    rates_time = TimeCurrent()
    if CopyBuffer(SilverTrend_Handle, 0, _DT(rates_time), _DT(_s_OnCalculate_prev_time), DnSTR) <= 0:
        return 0
    if CopyBuffer(SilverTrend_Handle, 1, _DT(rates_time), _DT(_s_OnCalculate_prev_time), UpSTR) <= 0:
        return 0
    limit = ArraySize(UpSTR) - 1
    trend = _s_OnCalculate_trend_
    ArraySetAsSeries(DnSTR, True)
    ArraySetAsSeries(UpSTR, True)
    if TIME[0] != _s_OnCalculate_prev_time and AlertCount:
        _s_OnCalculate_buycount = AlertCount
        _s_OnCalculate_sellcount = AlertCount
    for bar in range(limit, 0 - 1, -1):
        if UpSTR[bar] and UpSTR[bar] != EMPTY_VALUE:
            trend = 1
            if not bar:
                signal = True
        if DnSTR[bar] and DnSTR[bar] != EMPTY_VALUE:
            trend = -1
            if not bar:
                signal = True
        if bar or SignalBar:
            _s_OnCalculate_trend_ = trend
    if trend > 0:
        Color0 = UpSymbol_Color
        if signal:
            SignSymbol = 'г'
            if _s_OnCalculate_buycount > 0:
                _sw1 = alert_mode
                if _sw1 == OnlyAlert:
                    Alert(IndName + ': ' + 'Buy signal')
                elif _sw1 == OnlySound:
                    PlaySound('alert.wav')
                _s_OnCalculate_buycount -= 1
        else:
            SignSymbol = 'х'
    if trend < 0:
        Color0 = DnSymbol_Color
        if signal:
            SignSymbol = 'д'
            if _s_OnCalculate_sellcount > 0:
                _sw2 = alert_mode
                if _sw2 == OnlyAlert:
                    Alert(IndName + ': ' + 'Sell signal')
                elif _sw2 == OnlySound:
                    PlaySound('alert.wav')
                _s_OnCalculate_sellcount -= 1
        else:
            SignSymbol = 'х'
    if trend:
        if ShowIndName:
            SetTLabel(0, name1, 0, WhatCorner, 2 * WhatCorner, X_1_, Y_1_, IndName, IndName, IndName_Color, 'Georgia', Font_Size)
        if signal:
            SetTLabel(0, name0, 0, WhatCorner, 2 * WhatCorner, X_0, Yn, SignSymbol, IndName, Color0, 'Wingdings 3', Symbols_Size)
        else:
            SetTLabel(0, name0, 0, WhatCorner, 2 * WhatCorner, X_0, Yn, SignSymbol, IndName, Color0, 'Wingdings 2', Symbols_Size)
    else:
        Deinit()
    ChartRedraw(0)
    _s_OnCalculate_prev_time = TIME[0]
    return rates_total

# ---- global variables initialised from expressions
UpSymbol_Color = _input('UpSymbol_Color', _uint(Lime))  # Growth symbol color
DnSymbol_Color = _input('DnSymbol_Color', _uint(Magenta))  # Downfall symbol color
IndName_Color = _input('IndName_Color', _uint(DarkOrchid))  # Indicator name color

# ---- static local variables
_s_OnCalculate_prev_time = 0
_s_OnCalculate_trend_ = 0
_s_OnCalculate_buycount = 0
_s_OnCalculate_sellcount = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SilvertrendHtfSignal(_MQL5Indicator):
    name = 'silvertrend_htf_signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Indicator timeframe for the indicator calculation
        'RISK': 3,
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

