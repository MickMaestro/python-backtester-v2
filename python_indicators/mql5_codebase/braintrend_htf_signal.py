"""braintrend_htf_signal — converted from MQL5: MQL5 Indicators/BrainTrend_HTF_Signal/braintrend_htf_signal.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'braintrend_htf_signal', 'source': 'MQL5 Indicators/BrainTrend_HTF_Signal/braintrend_htf_signal.mq5', 'folder': 'BrainTrend_HTF_Signal', 'inputs': [{'mql': 'Symbol_', 'py': 'Symbol_', 'param': None, 'type': 'string', 'default': '', 'label': 'Financial asset', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Indicator timeframe for the indicator calculation', 'sinput': False}, {'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'int', 'default': 7, 'label': 'ATR period', 'sinput': False}, {'mql': 'STO_Period', 'py': 'STO_Period', 'param': 'STO_Period', 'type': 'int', 'default': 9, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'STO_Price', 'py': 'STO_Price', 'param': 'STO_Price', 'type': 'int', 'default': 0, 'label': 'Prices calculation method', 'sinput': False}, {'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'BrainTrend_Label_', 'label': 'Indicator labels name', 'sinput': False}, {'mql': 'BarTotal', 'py': 'BarTotal', 'param': 'BarTotal', 'type': 'uint', 'default': 4, 'label': 'Number of displayed bars', 'sinput': False}, {'mql': 'UpSymbol_Color', 'py': 'UpSymbol_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Growth symbol color', 'sinput': False}, {'mql': 'FlSymbol_Color', 'py': 'FlSymbol_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Flat symbol color', 'sinput': False}, {'mql': 'DnSymbol_Color', 'py': 'DnSymbol_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Downfall symbol color', 'sinput': False}, {'mql': 'IndName_Color', 'py': 'IndName_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Indicator name color', 'sinput': False}, {'mql': 'Symbols_Size', 'py': 'Symbols_Size', 'param': 'Symbols_Size', 'type': 'uint', 'default': 34, 'label': 'Signal symbols size', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'uint', 'default': 15, 'label': 'Indicator name font size', 'sinput': False}, {'mql': 'Xn', 'py': 'Xn', 'param': 'Xn', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the name', 'sinput': False}, {'mql': 'Yn', 'py': 'Yn', 'param': 'Yn', 'type': 'int', 'default': -60, 'label': 'Vertical shift of the name', 'sinput': False}, {'mql': 'ShowIndName', 'py': 'ShowIndName', 'param': 'ShowIndName', 'type': 'bool', 'default': True, 'label': 'Indicator name display', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 3, 'label': 'Location corner', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 0, 'label': 'Horizontal shift', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 30, 'label': 'Vertical shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

BlueViolet = 0xE22B8A  # MQL4 colour name
DarkOrchid = 0xCC3299  # MQL4 colour name
Gray = 0x808080  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
Symbol_ = _input('Symbol_', '')  # Financial asset
Timeframe = _input('Timeframe', PERIOD_H6)  # Indicator timeframe for the indicator calculation
ATR_Period = _input('ATR_Period', 7)  # ATR period
STO_Period = _input('STO_Period', 9)  # Stochastic period
MA_Method = _input('MA_Method', MODE_SMA)  # Smoothing method
STO_Price = _input('STO_Price', STO_LOWHIGH)  # Prices calculation method
Symbols_Sirname = _input('Symbols_Sirname', 'BrainTrend_Label_')  # Indicator labels name
BarTotal = _input('BarTotal', 4)  # Number of displayed bars
Symbols_Size = _input('Symbols_Size', 34)  # Signal symbols size
Font_Size = _input('Font_Size', 15)  # Indicator name font size
Xn = _input('Xn', 0)  # Horizontal shift of the name
Yn = _input('Yn', -60)  # Vertical shift of the name
ShowIndName = _input('ShowIndName', True)  # Indicator name display
WhatCorner = _input('WhatCorner', CORNER_RIGHT_UPPER)  # Location corner
X_ = _input('X_', 0)  # Horizontal shift
Y_ = _input('Y_', 30)  # Vertical shift
Brain1_Handle = 0
Brain2_Handle = 0
min_rates_total = 0
total = 0
X1 = Arr(0, 0)
Y1 = Arr(0, 0)
X2 = Arr(0, 0)
Y2 = Arr(0, 0)
X_n = 0
Y_n = 0
Brain1 = Arr(0, 0.0)
Brain2 = Arr(0, 0.0)
Color1 = Arr(0, 0)
Color2 = Arr(0, 0)
name1 = Arr(0, "")
name2 = Arr(0, "")
namen = ""
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
    global Brain1_Handle, Brain2_Handle, Symb, X_n, Y_n, min_rates_total, namen, total
    min_rates_total = MathMax(ATR_Period, STO_Period) + 2 + 4
    total = _int(BarTotal)
    if total < 1:
        total = 1
    if ArrayResize(X1, total) < total:
        Print('Failed to distribute the memory for X1[] array')
    if ArrayResize(Y1, total) < total:
        Print('Failed to distribute the memory for Y1[] array')
    if ArrayResize(name1, total) < total:
        Print('Failed to distribute the memory for name1[] array')
    if ArrayResize(Brain1, total) < total:
        Print('Failed to distribute the memory for Brain1[] array')
    if ArrayResize(Color1, total) < total:
        Print('Failed to distribute the memory for Color1[] array')
    if ArrayResize(X2, total) < total:
        Print('Failed to distribute the memory for X2[] array')
    if ArrayResize(Y2, total) < total:
        Print('Failed to distribute the memory for Y2[] array')
    if ArrayResize(name2, total) < total:
        Print('Failed to distribute the memory for name2[] array')
    if ArrayResize(Brain2, total) < total:
        Print('Failed to distribute the memory for Brain2[] array')
    if ArrayResize(Color2, total) < total:
        Print('Failed to distribute the memory for Color2[] array')
    ArraySetAsSeries(Brain1, True)
    ArraySetAsSeries(Brain2, True)
    if Symbol_ != '':
        Symb = Symbol_
    else:
        Symb = Symbol()
    size = _int(Symbols_Size * 1.1)
    shift1 = _int(_idiv(Symbols_Size, 6))
    for numb in range(0, total):
        X1[numb] = X_ + (numb * size)
        Y1[numb] = Y_ + 5
        name1[numb] = Symbols_Sirname + '1_' + _str(numb)
        X2[numb] = X_ + shift1 + (numb * size)
        Y2[numb] = Y_ + 5 + size
        name2[numb] = Symbols_Sirname + '2_' + _str(numb)
    if ShowIndName:
        X_n = X2[0] + Xn
        Y_n = Y2[0] + Yn
        namen = Symbols_Sirname + '0'
    StringConcatenate(_GlobRef(globals(), 'IndName'), 'BrainTrend(', Symb, ' ', GetStringTimeframe(Timeframe), ')')
    Brain1_Handle = iCustom(Symb, Timeframe, 'BrainTrend1', ATR_Period, STO_Period, MA_Method, STO_Price)
    if Brain1_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the BrainTrend1 indicator')
        return INIT_FAILED
    Brain2_Handle = iCustom(Symb, Timeframe, 'BrainTrend2', ATR_Period)
    if Brain2_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the BrainTrend2 indicator')
        return INIT_FAILED
    short_name = 'BrainTrend'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def Deinit():
    for numb in range(0, total):
        if ObjectFind(0, name1[numb]) != -1:
            ObjectDelete(0, name1[numb])
    for numb in range(0, total):
        if ObjectFind(0, name2[numb]) != -1:
            ObjectDelete(0, name2[numb])
    if ObjectFind(0, namen) != -1:
        ObjectDelete(0, namen)

def OnDeinit(reason):
    Deinit()
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Brain1_Handle) < min_rates_total or BarsCalculated(Brain2_Handle) < min_rates_total:
        return 0
    if BarsCalculated(Brain1_Handle) < Bars(Symb, Timeframe) or BarsCalculated(Brain2_Handle) < Bars(Symb, Timeframe):
        return prev_calculated
    if CopyBuffer(Brain1_Handle, 4, 0, total, Brain1) <= 0:
        return 0
    if CopyBuffer(Brain2_Handle, 4, 0, total, Brain2) <= 0:
        return 0
    numb = 0
    while numb < total:
        Br1 = _int(Brain1[numb])
        _sw1 = Br1
        if _sw1 == 0:
            Color1[numb] = FlSymbol_Color
        elif _sw1 == 1:
            Color1[numb] = UpSymbol_Color
        elif _sw1 == 2:
            Color1[numb] = DnSymbol_Color
        SetTLabel(0, name1[numb], 0, WhatCorner, 2 * WhatCorner, X1[numb], Y1[numb], 'u', IndName, Color1[numb], 'Wingdings', Symbols_Size)
        Br2 = _int(Brain2[numb])
        _sw2 = Br2
        if _sw2 == 0:
            Color2[numb] = FlSymbol_Color
        elif _sw2 == 1:
            Color2[numb] = UpSymbol_Color
        elif _sw2 == 2:
            Color2[numb] = DnSymbol_Color
        SetTLabel(0, name2[numb], 0, WhatCorner, 2 * WhatCorner, X2[numb], Y2[numb], 'l', IndName, Color2[numb], 'Wingdings', Symbols_Size)
        numb += 1
    if ShowIndName:
        SetTLabel(0, namen, 0, WhatCorner, 2 * WhatCorner, X_n, Y_n, IndName, IndName, IndName_Color, 'Georgia', Font_Size)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
UpSymbol_Color = _input('UpSymbol_Color', _uint(BlueViolet))  # Growth symbol color
FlSymbol_Color = _input('FlSymbol_Color', _uint(Gray))  # Flat symbol color
DnSymbol_Color = _input('DnSymbol_Color', _uint(Red))  # Downfall symbol color
IndName_Color = _input('IndName_Color', _uint(DarkOrchid))  # Indicator name color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BraintrendHtfSignal(_MQL5Indicator):
    name = 'braintrend_htf_signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Indicator timeframe for the indicator calculation
        'ATR_Period': 7,  # ATR period
        'STO_Period': 9,  # Stochastic period
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
        'STO_Price': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Prices calculation method
        'BarTotal': 4,  # Number of displayed bars
        'Symbols_Size': 34,  # Signal symbols size
        'Font_Size': 15,  # Indicator name font size
        'Xn': 0,  # Horizontal shift of the name
        'Yn': -60,  # Vertical shift of the name
        'ShowIndName': True,  # Indicator name display
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Location corner
        'X_': 0,  # Horizontal shift
        'Y_': 30,  # Vertical shift
    }

