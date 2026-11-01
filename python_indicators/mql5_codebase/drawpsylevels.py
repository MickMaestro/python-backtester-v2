"""drawpsylevels — converted from MQL5: MQL5 Indicators/Draw Psy Levels/drawpsylevels.mq5

Copyright: Copyright © 2012, Im_hungry; Link: Transl_DrawPsyLevels_v_1-01 by Im_hungry; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Im_hungry', 'version': '1.01', 'link': 'Transl_DrawPsyLevels_v_1-01 by Im_hungry', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 5}, 'colors': {1: [16711935]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'drawpsylevels', 'source': 'MQL5 Indicators/Draw Psy Levels/drawpsylevels.mq5', 'folder': 'Draw Psy Levels', 'inputs': [{'mql': 'Section_1', 'py': 'Section_1', 'param': None, 'type': 'string', 'default': '========  Level', 'label': '', 'sinput': False}, {'mql': 'MaxPrice', 'py': 'MaxPrice', 'param': 'MaxPrice', 'type': 'double', 'default': 1.4, 'label': '', 'sinput': False}, {'mql': 'MinPrice', 'py': 'MinPrice', 'param': 'MinPrice', 'type': 'double', 'default': 1.1, 'label': '', 'sinput': False}, {'mql': 'PriceStep', 'py': 'PriceStep', 'param': 'PriceStep', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'Levelwidth', 'py': 'Levelwidth', 'param': 'Levelwidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'LevelsColor', 'py': 'LevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LevelsStyle', 'py': 'LevelsStyle', 'param': 'LevelsStyle', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'Section_2', 'py': 'Section_2', 'param': None, 'type': 'string', 'default': '========  Arrow', 'label': '', 'sinput': False}, {'mql': 'DrawArrows', 'py': 'DrawArrows', 'param': 'DrawArrows', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Yellow = 0x00FFFF  # MQL4 colour name

# ---- inputs and global variables
Section_1 = _input('Section_1', '========  Level')
MaxPrice = _input('MaxPrice', 1.4)
MinPrice = _input('MinPrice', 1.1)
PriceStep = _input('PriceStep', 50)
Levelwidth = _input('Levelwidth', 1)
LevelsStyle = _input('LevelsStyle', STYLE_DOT)
Section_2 = _input('Section_2', '========  Arrow')
DrawArrows = _input('DrawArrows', True)
Arrow = Arr(0, 0.0)
aPivot = Arr(0, 0.0)
md_Point = 0.0
PivotsNum = 0
pTouchTime = 0

def OnInit():
    global PivotsNum, md_Point
    SetIndexBuffer(0, Arrow, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'Arrow')
    IndicatorSetString(INDICATOR_SHORTNAME, 'Transl_DrawPsyLevels ' + '  ( ' + Symbol() + ' )  ')
    PlotIndexSetInteger(0, PLOT_ARROW, 169)
    kp = 1
    if (Digits() == 5 or Digits() == 3) or Digits() == 1:
        kp = 10
    md_Point = SymbolInfoDouble(Symbol(), SYMBOL_POINT) * kp
    Max = MaxPrice
    if MaxPrice == 0.0:
        High = Arr(1, 0.0, dyn=False)
        CopyHigh(Symbol(), 0, 0, 1, High)
        Max = (MathRound(_fdiv(High[0], PriceStep * md_Point)) + 2) * (PriceStep * md_Point)
    Min = MinPrice
    if MinPrice == 0.0:
        Low = Arr(1, 0.0, dyn=False)
        CopyLow(Symbol(), 0, 0, 1, Low)
        Min = (MathRound(_fdiv(Low[0], PriceStep * md_Point)) - 2) * (PriceStep * md_Point)
    PivotsNum = _int(_fdiv(Max - Min, PriceStep * md_Point) + 1)
    ArrayResize(aPivot, PivotsNum)
    i = 0
    while i < PivotsNum:
        aPivot[i] = NormalizeDouble(Min + (PriceStep * md_Point * i), Digits())
        str_name = 'lev # ' + _str(i) + ' = ' + DoubleToString(aPivot[i], Digits())
        PlotLine(str_name, aPivot[i])
        i += 1
    return 0

def OnDeinit(reason):
    name_obj = ""
    for i in range(ObjectsTotal(0), 0 - 1, -1):
        name_obj = ObjectName(0, i)
        if StringFind(name_obj, 'lev', 0) != -1:
            ObjectDelete(0, name_obj)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global pTouchTime
    touch = 0
    i = 0
    ZeroLevel = 0.0
    TouchTime = 0
    for t in range(rates_total - 1, 0 - 1, -1):
        i = 0
        while i < PivotsNum:
            if high[t] >= aPivot[i] and low[t] <= aPivot[i]:
                touch = 1
                ZeroLevel = aPivot[i] - ((PriceStep * md_Point) / 10)
                TouchTime = time[t]
                break
            i += 1
        if (DrawArrows == True and touch > 0) and TouchTime != pTouchTime:
            Arrow[t] = ZeroLevel
            pTouchTime = TouchTime
    return rates_total

def PlotLine(name, value):
    if value > 0:
        ObjectDelete(0, name)
        ObjectCreate(0, name, OBJ_HLINE, 0, 0, value)
        ObjectSetInteger(0, name, OBJPROP_WIDTH, Levelwidth)
        ObjectSetInteger(0, name, OBJPROP_STYLE, LevelsStyle)
        ObjectSetInteger(0, name, OBJPROP_COLOR, LevelsColor)

def drawArrow(time, price, size, clr):
    c_name = 'lev _ ' + _str(PriceStep) + ' = ' + TimeToString(time)
    ObjectCreate(0, c_name, OBJ_TEXT, 0, time, price)
    ObjectSetInteger(0, c_name, OBJPROP_WIDTH, size)
    ObjectSetInteger(0, c_name, OBJPROP_COLOR, clr)

# ---- global variables initialised from expressions
LevelsColor = _input('LevelsColor', _uint(Yellow))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Drawpsylevels(_MQL5Indicator):
    name = 'drawpsylevels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MaxPrice': 1.4,
        'MinPrice': 1.1,
        'PriceStep': 50,
        'Levelwidth': 1,
        'LevelsStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),
        'DrawArrows': True,
    }

