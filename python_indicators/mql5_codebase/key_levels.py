"""Key_Levels — converted from MQL5: MQL5 Indicators/KeyLevels/Key_Levels.mq5

Version: 2.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'version': '2.0'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Key_Levels', 'source': 'MQL5 Indicators/KeyLevels/Key_Levels.mq5', 'folder': 'KeyLevels', 'inputs': [{'mql': 'H', 'py': 'H', 'param': None, 'type': 'string', 'default': ' --- Mode_Settings ---', 'label': '', 'sinput': False}, {'mql': 'Show_00_50_Levels', 'py': 'Show_00_50_Levels', 'param': 'Show_00_50_Levels', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Show_20_80_Levels', 'py': 'Show_20_80_Levels', 'param': 'Show_20_80_Levels', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Level_00_Color', 'py': 'Level_00_Color', 'param': None, 'type': 'color', 'default': 65280, 'label': '', 'sinput': False}, {'mql': 'Level_50_Color', 'py': 'Level_50_Color', 'param': None, 'type': 'color', 'default': 8421504, 'label': '', 'sinput': False}, {'mql': 'Level_20_Color', 'py': 'Level_20_Color', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'Level_80_Color', 'py': 'Level_80_Color', 'param': None, 'type': 'color', 'default': 32768, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
H = _input('H', ' --- Mode_Settings ---')
Show_00_50_Levels = _input('Show_00_50_Levels', True)
Show_20_80_Levels = _input('Show_20_80_Levels', True)
Level_00_Color = _input('Level_00_Color', clrLime)
Level_50_Color = _input('Level_50_Color', clrGray)
Level_20_Color = _input('Level_20_Color', clrRed)
Level_80_Color = _input('Level_80_Color', clrGreen)
dXPoint = 1.0
Div = 0.0
i = 0.0
HighPrice = 0.0
LowPrice = 0.0
iDigits = 0

def OnInit():
    global Div, dXPoint, iDigits
    iDigits = Digits()
    if Digits() == 5 or Digits() == 3:
        dXPoint = 10.0
    if Digits() == 3:
        iDigits = 2
    if Digits() == 5:
        iDigits = 4
    Div = _fdiv(0.1, Point() * dXPoint)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global HighPrice, LowPrice, i
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    ih = ArrayMaximum(high, 2)
    if ih < 0:
        return rates_total
    il = ArrayMinimum(low, 2)
    if il < 0:
        return rates_total
    HighPrice = MathRound((high[ih] + 1) * Div)
    LowPrice = MathRound((low[il] - 1) * Div)
    if Show_00_50_Levels:
        i = LowPrice
        while i <= HighPrice:
            if MathMod(i, 5) == 0.0:
                name = 'RoundPrice ' + DoubleToString(i, 0)
                if ObjectFind(0, name) != 0:
                    ObjectCreate(0, name, OBJ_HLINE, 0, time[1], _fdiv(i, Div))
                    ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_DOT)
                    if MathMod(i, 10) == 0.0:
                        ObjectSetInteger(0, name, OBJPROP_COLOR, Level_00_Color)
                    else:
                        ObjectSetInteger(0, name, OBJPROP_COLOR, Level_50_Color)
            i += 1
    if Show_20_80_Levels:
        i = LowPrice
        while i <= HighPrice:
            if StringSubstr(DoubleToString(_fdiv(i, Div), iDigits), StringLen(DoubleToString(_fdiv(i, Div), iDigits)) - 2, 2) == '20':
                name = 'RoundPrice ' + DoubleToString(i, 0)
                if ObjectFind(0, name) != 0:
                    ObjectCreate(0, name, OBJ_HLINE, 0, time[1], _fdiv(i, Div))
                    ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_DOT)
                    ObjectSetInteger(0, name, OBJPROP_COLOR, Level_20_Color)
            if StringSubstr(DoubleToString(_fdiv(i, Div), iDigits), StringLen(DoubleToString(_fdiv(i, Div), iDigits)) - 2, 2) == '80':
                name = 'RoundPrice ' + DoubleToString(i, 0)
                if ObjectFind(0, name) != 0:
                    ObjectCreate(0, name, OBJ_HLINE, 0, time[1], _fdiv(i, Div))
                    ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_DOT)
                    ObjectSetInteger(0, name, OBJPROP_COLOR, Level_80_Color)
            i += 1
    return rates_total

def OnDeinit(reason):
    Comment('')
    ObjectsDeleteAll(0, 'Round')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KeyLevels(_MQL5Indicator):
    name = 'Key_Levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Show_00_50_Levels': True,
        'Show_20_80_Levels': True,
    }

