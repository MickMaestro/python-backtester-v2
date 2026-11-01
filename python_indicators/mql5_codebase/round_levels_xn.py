"""Round_Levels_XN — converted from MQL5: MQL5 Indicators/Round_Levels_XN/Round_Levels_XN.mq5

This code draws 4 horizontal lines with 00 at the end of
the vertical coordinate (price). This 4 horizontal lines with
this property are closest to current price.
Copyright: Copyright © 2007, Martes; Link: http://championship.mql4.com/2007/ru/users/Martes/

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Martes', 'link': 'http://championship.mql4.com/2007/ru/users/Martes/', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['This code draws 4 horizontal lines with 00 at the end of', 'the vertical coordinate (price). This 4 horizontal lines with', 'this property are closest to current price.'], 'name': 'Round_Levels_XN', 'source': 'MQL5 Indicators/Round_Levels_XN/Round_Levels_XN.mq5', 'folder': 'Round_Levels_XN', 'inputs': [{'mql': 'ZeroCount', 'py': 'ZeroCount', 'param': 'ZeroCount', 'type': 'uint', 'default': 2, 'label': 'количество нулей для округления', 'sinput': False}, {'mql': 'levels_sirname', 'py': 'levels_sirname', 'param': None, 'type': 'string', 'default': 'Price_Level_1', 'label': 'лейба уровней', 'sinput': False}, {'mql': 'XNCount', 'py': 'XNCount', 'param': 'XNCount', 'type': 'uint', 'default': 3, 'label': 'количество повторов всего набора линий', 'sinput': False}, {'mql': 'Up_level_color2', 'py': 'Up_level_color2', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'цвет второго верхнего уровня', 'sinput': False}, {'mql': 'Up_level_style2', 'py': 'Up_level_style2', 'param': 'Up_level_style2', 'type': 'int', 'default': 0, 'label': 'стиль второго верхнего уровня', 'sinput': False}, {'mql': 'Up_level_width2', 'py': 'Up_level_width2', 'param': 'Up_level_width2', 'type': 'int', 'default': 3, 'label': 'толщина второго верхнего уровня', 'sinput': False}, {'mql': 'Up_level_color1', 'py': 'Up_level_color1', 'param': None, 'type': 'color', 'default': 65280, 'label': 'цвет первого верхнего уровня', 'sinput': False}, {'mql': 'Up_level_style1', 'py': 'Up_level_style1', 'param': 'Up_level_style1', 'type': 'int', 'default': 0, 'label': 'стиль первого верхнего уровня', 'sinput': False}, {'mql': 'Up_level_width1', 'py': 'Up_level_width1', 'param': 'Up_level_width1', 'type': 'int', 'default': 3, 'label': 'толщина первого верхнего уровня', 'sinput': False}, {'mql': 'Dn_level_color1', 'py': 'Dn_level_color1', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет первого нижнего уровня', 'sinput': False}, {'mql': 'Dn_level_style1', 'py': 'Dn_level_style1', 'param': 'Dn_level_style1', 'type': 'int', 'default': 0, 'label': 'стиль первого нижнего уровня', 'sinput': False}, {'mql': 'Dn_level_width1', 'py': 'Dn_level_width1', 'param': 'Dn_level_width1', 'type': 'int', 'default': 3, 'label': 'толщина первого нижнего уровня', 'sinput': False}, {'mql': 'Dn_level_color2', 'py': 'Dn_level_color2', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет второго нижнего уровня', 'sinput': False}, {'mql': 'Dn_level_style2', 'py': 'Dn_level_style2', 'param': 'Dn_level_style2', 'type': 'int', 'default': 0, 'label': 'стиль второго нижнего уровня', 'sinput': False}, {'mql': 'Dn_level_width2', 'py': 'Dn_level_width2', 'param': 'Dn_level_width2', 'type': 'int', 'default': 3, 'label': 'толщина второго нижнего уровня', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
ZeroCount = _input('ZeroCount', 2)  # количество нулей для округления
levels_sirname = _input('levels_sirname', 'Price_Level_1')  # лейба уровней
XNCount = _input('XNCount', 3)  # количество повторов всего набора линий
Up_level_color2 = _input('Up_level_color2', clrBlue)  # цвет второго верхнего уровня
Up_level_style2 = _input('Up_level_style2', SOLID_)  # стиль второго верхнего уровня
Up_level_width2 = _input('Up_level_width2', w_3)  # толщина второго верхнего уровня
Up_level_color1 = _input('Up_level_color1', clrLime)  # цвет первого верхнего уровня
Up_level_style1 = _input('Up_level_style1', SOLID_)  # стиль первого верхнего уровня
Up_level_width1 = _input('Up_level_width1', w_3)  # толщина первого верхнего уровня
Dn_level_color1 = _input('Dn_level_color1', clrRed)  # цвет первого нижнего уровня
Dn_level_style1 = _input('Dn_level_style1', SOLID_)  # стиль первого нижнего уровня
Dn_level_width1 = _input('Dn_level_width1', w_3)  # толщина первого нижнего уровня
Dn_level_color2 = _input('Dn_level_color2', clrMagenta)  # цвет второго нижнего уровня
Dn_level_style2 = _input('Dn_level_style2', SOLID_)  # стиль второго нижнего уровня
Dn_level_width2 = _input('Dn_level_width2', w_3)  # толщина второго нижнего уровня
VShift = 0.0
Normalize = 0
UpName2 = Arr(0, "")
UpName1 = Arr(0, "")
DnName1 = Arr(0, "")
DnName2 = Arr(0, "")

def CreateHline(chart_id, name, nwin, price, Color, style, width, background, text):
    ObjectCreate(chart_id, name, OBJ_HLINE, nwin, 0, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, background)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetHline(chart_id, name, nwin, price, Color, style, width, background, text):
    if ObjectFind(chart_id, name) == -1:
        CreateHline(chart_id, name, nwin, price, Color, style, width, background, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, 0, price)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def OnInit():
    global Normalize, VShift
    ArrayResize(UpName2, XNCount + 1)
    ArrayResize(UpName1, XNCount + 1)
    ArrayResize(DnName1, XNCount + 1)
    ArrayResize(DnName2, XNCount + 1)
    for count in range(0, _int(XNCount + 1)):
        UpName2[count] = levels_sirname + '_UpName2.' + _str(count)
        UpName1[count] = levels_sirname + '_UpName1.' + _str(count)
        DnName1[count] = levels_sirname + '_DnName1.' + _str(count)
        DnName2[count] = levels_sirname + '_DnName2.' + _str(count)
    Normalize = Digits() - _int(ZeroCount)
    VShift = Point() * MathPow(10, ZeroCount)

def OnDeinit(reason):
    for count in range(0, _int(XNCount + 1)):
        ObjectDelete(0, UpName2[count])
        ObjectDelete(0, UpName1[count])
        ObjectDelete(0, DnName1[count])
        ObjectDelete(0, DnName2[count])
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_DnLevel1
    UpLevel2 = 0.0
    UpLevel1 = 0.0
    DnLevel2 = 0.0
    _s_OnCalculate_DnLevel1 = NormalizeDouble(close[rates_total - 1], Digits() - ZeroCount)
    UpLevel1 = _s_OnCalculate_DnLevel1 + VShift
    UpLevel2 = UpLevel1 + VShift
    DnLevel2 = _s_OnCalculate_DnLevel1 - VShift
    for count in range(0, _int(XNCount + 1)):
        SetHline(0, UpName2[count], 0, UpLevel2 + (2 * count * VShift), Up_level_color2, Up_level_style2, Up_level_width2, False, UpName1[count])
        SetHline(0, UpName1[count], 0, UpLevel1 + (2 * count * VShift), Up_level_color1, Up_level_style1, Up_level_width1, False, UpName1[count])
        SetHline(0, DnName1[count], 0, _s_OnCalculate_DnLevel1 - (2 * count * VShift), Dn_level_color1, Dn_level_style1, Dn_level_width1, False, DnName1[count])
        SetHline(0, DnName2[count], 0, DnLevel2 - (2 * count * VShift), Dn_level_color2, Dn_level_style2, Dn_level_width2, False, DnName2[count])
    ChartRedraw(0)
    return rates_total

# ---- static local variables
_s_OnCalculate_DnLevel1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RoundLevelsXN(_MQL5Indicator):
    name = 'Round_Levels_XN'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ZeroCount': 2,  # количество нулей для округления
        'XNCount': 3,  # количество повторов всего набора линий
        'Up_level_style2': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль второго верхнего уровня
        'Up_level_width2': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # толщина второго верхнего уровня
        'Up_level_style1': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль первого верхнего уровня
        'Up_level_width1': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # толщина первого верхнего уровня
        'Dn_level_style1': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль первого нижнего уровня
        'Dn_level_width1': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # толщина первого нижнего уровня
        'Dn_level_style2': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=0),  # стиль второго нижнего уровня
        'Dn_level_width2': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # толщина второго нижнего уровня
    }

