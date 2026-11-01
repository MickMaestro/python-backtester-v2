"""Fibo_Bar — converted from MQL5: MQL5 Indicators/Fibo Bar MT5/Fibo_Bar.mq5

This indicator draws Fibo levels on the last bar.
Copyright: © Tecciztecatl 2016; Link: https://www.mql5.com/en/users/tecciztecatl; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© Tecciztecatl 2016', 'link': 'https://www.mql5.com/en/users/tecciztecatl', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['This indicator draws Fibo levels on the last bar.'], 'name': 'Fibo_Bar', 'source': 'MQL5 Indicators/Fibo Bar MT5/Fibo_Bar.mq5', 'folder': 'Fibo Bar MT5', 'inputs': [{'mql': 'comm0', 'py': 'comm0', 'param': None, 'type': 'string', 'default': '', 'label': '---- FIBO ----', 'sinput': False}, {'mql': 'Fibo_Bar', 'py': 'Fibo_Bar', 'param': 'Fibo_Bar', 'type': 'int', 'default': 16408, 'label': 'Last Bar for Fibo', 'sinput': False}, {'mql': 'fibo_color1', 'py': 'fibo_color1', 'param': None, 'type': 'color', 'default': 15453831, 'label': 'Upper color', 'sinput': False}, {'mql': 'fibo_color0', 'py': 'fibo_color0', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Main color', 'sinput': False}, {'mql': 'fibo_color2', 'py': 'fibo_color2', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Lower color', 'sinput': False}, {'mql': 'fibo_style', 'py': 'fibo_style', 'param': 'fibo_style', 'type': 'int', 'default': 2, 'label': 'Style lines', 'sinput': False}, {'mql': 'fibo_width', 'py': 'fibo_width', 'param': 'fibo_width', 'type': 'int', 'default': 1, 'label': 'Line Width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
comm0 = _input('comm0', '')  # ---- FIBO ----
Fibo_Bar = _input('Fibo_Bar', PERIOD_D1)  # Last Bar for Fibo
fibo_color1 = _input('fibo_color1', clrSkyBlue)  # Upper color
fibo_color0 = _input('fibo_color0', clrLimeGreen)  # Main color
fibo_color2 = _input('fibo_color2', clrOrange)  # Lower color
fibo_style = _input('fibo_style', STYLE_DOT)  # Style lines
fibo_width = _input('fibo_width', 1)  # Line Width
FIBO_levels = Arr(0, 0.0)
FIBO_prices = Arr(0, 0.0)
fibo_txt = Arr(0, "")
fibo_levels0 = '0 23.6 38.2 50 61.8 76.4 100'
fibo_levels1 = '123.6 138.2 150 161.8 176.4 200 223.6 238.2 250 261.8 276.4 300 323.6 338.2 350 361.8 376.4 400'
fibo_levels2 = '-23.6 -38.2 -50 -61.8 -76.4 -100 -123.6 -138.2 -150 -161.8 -176.4 -200 -223.6 -238.2 -250 -261.8 -276.4 -300 -323.6 -338.2 -350 -361.8 -376.4 -400'
Label_prefix = 'Fibo_'
allBars = 0
chart_ID = 0

def OnDeinit(reason):
    DeleteObjects()

def OnInit():
    global chart_ID
    chart_ID = ChartID()
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global allBars
    if allBars != Bars(Symbol(), Fibo_Bar) or ObjectFind(chart_ID, Label_prefix + 'f0') < 0:
        allBars = Bars(Symbol(), Fibo_Bar)
        BuildLevels()
    return rates_total

def BuildLevels():
    Maximum = iHigh(None, Fibo_Bar, 1)
    Minimum = iLow(None, Fibo_Bar, 1)
    time1 = iTime(None, Fibo_Bar, 0) + (PeriodSeconds(Fibo_Bar) * 7)
    time2 = iTime(None, Fibo_Bar, 1)
    tf = TFtoStr(Fibo_Bar)
    MakeFibo(fibo_levels0)
    SetFibo(Label_prefix + 'f0', time1, Maximum, time2, Minimum, fibo_color0, fibo_width, clrNONE)
    ObjectSetString(chart_ID, Label_prefix + 'f0', OBJPROP_LEVELTEXT, 6, 'High last ' + tf + ' ' + ObjectGetString(chart_ID, Label_prefix + 'f0', OBJPROP_LEVELTEXT, 6))
    ObjectSetString(chart_ID, Label_prefix + 'f0', OBJPROP_LEVELTEXT, 0, 'Low last ' + tf + ' ' + ObjectGetString(chart_ID, Label_prefix + 'f0', OBJPROP_LEVELTEXT, 0))
    MakeFibo(fibo_levels1)
    SetFibo(Label_prefix + 'f1', time1, Maximum, time2, Minimum, fibo_color1, fibo_width, clrNONE)
    MakeFibo(fibo_levels2)
    SetFibo(Label_prefix + 'f2', time1, Maximum, time2, Minimum, fibo_color2, fibo_width, clrNONE)

def SetFibo(nname, time1, price1, time2, price2, cvet, wiDth, cvet_full):
    levels = ArraySize(FIBO_levels)
    if ObjectFind(chart_ID, nname) < 0:
        ObjectCreate(chart_ID, nname, OBJ_FIBO, 0, time1, price1, time2, price2)
        ObjectSetInteger(chart_ID, nname, OBJPROP_COLOR, cvet_full)
        ObjectSetInteger(chart_ID, nname, OBJPROP_STYLE, STYLE_DOT)
        ObjectSetInteger(chart_ID, nname, OBJPROP_WIDTH, 1)
        ObjectSetInteger(chart_ID, nname, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(chart_ID, nname, OBJPROP_SELECTED, False)
        ObjectSetInteger(chart_ID, nname, OBJPROP_BACK, True)
        ObjectSetInteger(chart_ID, nname, OBJPROP_RAY_RIGHT, False)
        ObjectSetInteger(chart_ID, nname, OBJPROP_HIDDEN, True)
    else:
        ObjectMove(chart_ID, nname, 0, time1, price1)
        ObjectMove(chart_ID, nname, 1, time2, price2)
    ObjectSetInteger(chart_ID, nname, OBJPROP_LEVELS, levels)
    for i in range(0, levels):
        FIBO_prices[i] = NormalizeDouble(((price1 - price2) * FIBO_levels[i]) + price2, Digits())
        ObjectSetDouble(chart_ID, nname, OBJPROP_LEVELVALUE, i, FIBO_levels[i])
        ObjectSetString(chart_ID, nname, OBJPROP_LEVELTEXT, i, '(' + DoubleToString(100 * FIBO_levels[i], 1) + ') ' + DoubleToString(FIBO_prices[i], Digits()))
        ObjectSetInteger(chart_ID, nname, OBJPROP_LEVELCOLOR, i, cvet)
        ObjectSetInteger(chart_ID, nname, OBJPROP_LEVELWIDTH, i, wiDth)
        ObjectSetInteger(chart_ID, nname, OBJPROP_LEVELSTYLE, i, fibo_style)

def TFtoStr(TimeFrameInt):
    TimeFrame = ""
    if TimeFrameInt == PERIOD_M1:
        TimeFrame = 'M1'
    if TimeFrameInt == PERIOD_M2:
        TimeFrame = 'M2'
    if TimeFrameInt == PERIOD_M3:
        TimeFrame = 'M3'
    if TimeFrameInt == PERIOD_M4:
        TimeFrame = 'M4'
    if TimeFrameInt == PERIOD_M5:
        TimeFrame = 'M5'
    if TimeFrameInt == PERIOD_M6:
        TimeFrame = 'M6'
    if TimeFrameInt == PERIOD_M10:
        TimeFrame = 'M10'
    if TimeFrameInt == PERIOD_M12:
        TimeFrame = 'M12'
    if TimeFrameInt == PERIOD_M15:
        TimeFrame = 'M15'
    if TimeFrameInt == PERIOD_M30:
        TimeFrame = 'M20'
    if TimeFrameInt == PERIOD_M30:
        TimeFrame = 'M30'
    if TimeFrameInt == PERIOD_H1:
        TimeFrame = 'H1'
    if TimeFrameInt == PERIOD_H2:
        TimeFrame = 'H2'
    if TimeFrameInt == PERIOD_H3:
        TimeFrame = 'H3'
    if TimeFrameInt == PERIOD_H4:
        TimeFrame = 'H4'
    if TimeFrameInt == PERIOD_H6:
        TimeFrame = 'H6'
    if TimeFrameInt == PERIOD_H8:
        TimeFrame = 'H8'
    if TimeFrameInt == PERIOD_H12:
        TimeFrame = 'H12'
    if TimeFrameInt == PERIOD_D1:
        TimeFrame = 'D1'
    if TimeFrameInt == PERIOD_W1:
        TimeFrame = 'W1'
    if TimeFrameInt == PERIOD_MN1:
        TimeFrame = 'MN1'
    return TimeFrame

def MakeFibo(text):
    u_sep = StringGetCharacter(' ', 0)
    num_levels = StringSplit(text, u_sep, fibo_txt)
    ArrayResize(FIBO_levels, num_levels)
    ArrayResize(FIBO_prices, num_levels)
    for i in range(0, num_levels):
        FIBO_levels[i] = NormalizeDouble(StringToDouble(fibo_txt[i]) / 100, 3)
    ArraySort(FIBO_levels)

def DeleteObjects():
    ObjectsDeleteAll(chart_ID, Label_prefix, -1, -1)
    ChartRedraw(chart_ID)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FiboBar(_MQL5Indicator):
    name = 'Fibo_Bar'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fibo_Bar': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Last Bar for Fibo
        'fibo_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Style lines
        'fibo_width': 1,  # Line Width
    }

