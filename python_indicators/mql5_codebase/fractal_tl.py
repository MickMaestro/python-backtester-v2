"""Fractal_TL — converted from MQL5: MQL5 Indicators/Fractal_TL/Fractal_TL.mq5

Copyright: Copyright 2017, MetaQuotes Software Corp.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2017, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Fractal_TL', 'source': 'MQL5 Indicators/Fractal_TL/Fractal_TL.mq5', 'folder': 'Fractal_TL', 'inputs': [{'mql': 'base_tf', 'py': 'base_tf', 'param': 'base_tf', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Resistance_Color', 'py': 'Resistance_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'color of the resistance line', 'sinput': False}, {'mql': 'Resistance_Style', 'py': 'Resistance_Style', 'param': 'Resistance_Style', 'type': 'int', 'default': 0, 'label': 'line style of the resistance', 'sinput': False}, {'mql': 'Resistance_Width', 'py': 'Resistance_Width', 'param': 'Resistance_Width', 'type': 'int', 'default': 1, 'label': 'width of the resistance line', 'sinput': False}, {'mql': 'Support_Color', 'py': 'Support_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'color of the support line', 'sinput': False}, {'mql': 'Support_Style', 'py': 'Support_Style', 'param': 'Support_Style', 'type': 'int', 'default': 0, 'label': 'style of the support line', 'sinput': False}, {'mql': 'Support_Width', 'py': 'Support_Width', 'param': 'Support_Width', 'type': 'int', 'default': 1, 'label': 'width of the support line', 'sinput': False}, {'mql': 'Remove_TL', 'py': 'Remove_TL', 'param': 'Remove_TL', 'type': 'bool', 'default': False, 'label': 'Remove_TL', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
base_tf = _input('base_tf', 0)
Resistance_Style = _input('Resistance_Style', 0)  # line style of the resistance
Resistance_Width = _input('Resistance_Width', 1)  # width of the resistance line
Support_Style = _input('Support_Style', 0)  # style of the support line
Support_Width = _input('Support_Width', 1)  # width of the support line
Remove_TL = _input('Remove_TL', False)  # Remove_TL
Fractal_base = 0

def OnInit():
    global Fractal_base
    Fractal_base = iFractals(Symbol(), base_tf)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    n = 0
    UpperFractal_1_base = 0
    LowerFractal_1_base = 0
    UpperFractal_2_base = 0
    LowerFractal_2_base = 0
    FractalDown_base = Arr(0, 0.0)
    FractalUp_base = Arr(0, 0.0)
    UpFractal_1_base = 0.0
    LowFractal_1_base = 0.0
    UpFractal_2_base = 0.0
    LowFractal_2_base = 0.0
    CopyBuffer(Fractal_base, 0, _DT(TimeCurrent()), Bars(Symbol(), base_tf), FractalUp_base)
    CopyBuffer(Fractal_base, 1, _DT(TimeCurrent()), Bars(Symbol(), base_tf), FractalDown_base)
    ArraySetAsSeries(FractalUp_base, True)
    ArraySetAsSeries(FractalDown_base, True)
    n = 0
    while n < Bars(Symbol(), base_tf):
        if FractalUp_base[n] != EMPTY_VALUE:
            break
        n += 1
    UpFractal_1_base = FractalUp_base[n]
    UpperFractal_1_base = n
    n = UpperFractal_1_base + 1
    while n < Bars(Symbol(), base_tf):
        if FractalUp_base[n] != EMPTY_VALUE:
            break
        n += 1
    UpFractal_2_base = FractalUp_base[n]
    UpperFractal_2_base = n
    n = 0
    while n < Bars(Symbol(), base_tf):
        if FractalDown_base[n] != EMPTY_VALUE:
            break
        n += 1
    LowFractal_1_base = FractalDown_base[n]
    LowerFractal_1_base = n
    n = LowerFractal_1_base + 1
    while n < Bars(Symbol(), base_tf):
        if FractalDown_base[n] != EMPTY_VALUE:
            break
        n += 1
    LowFractal_2_base = FractalDown_base[n]
    LowerFractal_2_base = n
    UpFractalTime_1_base = Arr(0, 0)
    LowFractalTime_1_base = Arr(0, 0)
    UpFractalTime_2_base = Arr(0, 0)
    LowFractalTime_2_base = Arr(0, 0)
    ArraySetAsSeries(UpFractalTime_1_base, True)
    ArraySetAsSeries(LowFractalTime_1_base, True)
    ArraySetAsSeries(UpFractalTime_2_base, True)
    ArraySetAsSeries(LowFractalTime_2_base, True)
    CopyTime(Symbol(), base_tf, UpperFractal_1_base, 1, UpFractalTime_1_base)
    CopyTime(Symbol(), base_tf, LowerFractal_1_base, 1, LowFractalTime_1_base)
    CopyTime(Symbol(), base_tf, UpperFractal_2_base, 1, UpFractalTime_2_base)
    CopyTime(Symbol(), base_tf, LowerFractal_2_base, 1, LowFractalTime_2_base)
    ObjectCreate(0, 'UpperFractal_1', OBJ_ARROW, 0, UpFractalTime_1_base[0], UpFractal_1_base)
    ObjectCreate(0, 'UpperFractal_2', OBJ_ARROW, 0, UpFractalTime_2_base[0], UpFractal_2_base)
    ObjectSetInteger(0, 'UpperFractal_1', OBJPROP_COLOR, Resistance_Color)
    ObjectSetInteger(0, 'UpperFractal_2', OBJPROP_COLOR, Resistance_Color)
    ObjectSetInteger(0, 'UpperFractal_1', OBJPROP_ARROWCODE, 217)
    ObjectSetInteger(0, 'UpperFractal_2', OBJPROP_ARROWCODE, 217)
    ObjectSetInteger(0, 'UpperFractal_1', OBJPROP_ANCHOR, ANCHOR_BOTTOM)
    ObjectSetInteger(0, 'UpperFractal_2', OBJPROP_ANCHOR, ANCHOR_BOTTOM)
    ObjectCreate(0, 'LowerFractal_1', OBJ_ARROW, 0, LowFractalTime_1_base[0], LowFractal_1_base)
    ObjectCreate(0, 'LowerFractal_2', OBJ_ARROW, 0, LowFractalTime_2_base[0], LowFractal_2_base)
    ObjectSetInteger(0, 'LowerFractal_1', OBJPROP_COLOR, Support_Color)
    ObjectSetInteger(0, 'LowerFractal_2', OBJPROP_COLOR, Support_Color)
    ObjectSetInteger(0, 'LowerFractal_1', OBJPROP_ARROWCODE, 218)
    ObjectSetInteger(0, 'LowerFractal_2', OBJPROP_ARROWCODE, 218)
    ObjectSetInteger(0, 'LowerFractal_1', OBJPROP_ANCHOR, ANCHOR_TOP)
    ObjectSetInteger(0, 'LowerFractal_2', OBJPROP_ANCHOR, ANCHOR_TOP)
    if ObjectGetInteger(0, 'TL_Support', OBJPROP_TIME) != LowFractalTime_2_base[0]:
        ObjectDelete(0, 'TL_Support')
        ObjectDelete(0, 'LowerFractal_1')
        ObjectDelete(0, 'LowerFractal_2')
    if ObjectGetInteger(0, 'TL_Resistance', OBJPROP_TIME) != UpFractalTime_2_base[0]:
        ObjectDelete(0, 'TL_Resistance')
        ObjectDelete(0, 'UpperFractal_1')
        ObjectDelete(0, 'UpperFractal_2')
    ObjectCreate(0, 'TL_Support', OBJ_TREND, 0, LowFractalTime_2_base[0], LowFractal_2_base, LowFractalTime_1_base[0], LowFractal_1_base)
    ObjectSetInteger(0, 'TL_Support', OBJPROP_RAY_RIGHT, True)
    ObjectSetInteger(0, 'TL_Support', OBJPROP_COLOR, Support_Color)
    ObjectSetInteger(0, 'TL_Support', OBJPROP_STYLE, Support_Style)
    ObjectSetInteger(0, 'TL_Support', OBJPROP_WIDTH, Support_Width)
    ObjectCreate(0, 'TL_Resistance', OBJ_TREND, 0, UpFractalTime_2_base[0], UpFractal_2_base, UpFractalTime_1_base[0], UpFractal_1_base)
    ObjectSetInteger(0, 'TL_Resistance', OBJPROP_RAY_RIGHT, True)
    ObjectSetInteger(0, 'TL_Resistance', OBJPROP_COLOR, Resistance_Color)
    ObjectSetInteger(0, 'TL_Resistance', OBJPROP_STYLE, Resistance_Style)
    ObjectSetInteger(0, 'TL_Resistance', OBJPROP_WIDTH, Resistance_Width)
    if Remove_TL == True:
        ObjectDelete(0, 'TL_Support')
        ObjectDelete(0, 'TL_Resistance')
        ObjectDelete(0, 'LowerFractal_1')
        ObjectDelete(0, 'LowerFractal_2')
        ObjectDelete(0, 'UpperFractal_1')
        ObjectDelete(0, 'UpperFractal_2')
    return rates_total

# ---- global variables initialised from expressions
Resistance_Color = _input('Resistance_Color', _uint(Red))  # color of the resistance line
Support_Color = _input('Support_Color', _uint(Red))  # color of the support line


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalTL(_MQL5Indicator):
    name = 'Fractal_TL'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'base_tf': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
        'Resistance_Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # line style of the resistance
        'Resistance_Width': 1,  # width of the resistance line
        'Support_Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # style of the support line
        'Support_Width': 1,  # width of the support line
        'Remove_TL': False,  # Remove_TL
    }

