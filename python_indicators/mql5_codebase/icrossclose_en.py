"""icrossclose_en — converted from MQL5: MQL5 Indicators/iCrossClose/icrossclose_en.mq5

Copyright: dmffx.com; Link: http://dmffx.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'dmffx.com', 'link': 'http://dmffx.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'CrossClose'}, 'levels': [], 'description': [], 'name': 'icrossclose_en', 'source': 'MQL5 Indicators/iCrossClose/icrossclose_en.mq5', 'folder': 'iCrossClose', 'inputs': [{'mql': 'S1_Symbol', 'py': 'S1_Symbol', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': 'S1_Symbol', 'sinput': False}, {'mql': 'S1_Invert', 'py': 'S1_Invert', 'param': 'S1_Invert', 'type': 'bool', 'default': False, 'label': 'S1_Invert', 'sinput': False}, {'mql': 'S1_K', 'py': 'S1_K', 'param': 'S1_K', 'type': 'double', 'default': 1.0, 'label': 'S1_K', 'sinput': False}, {'mql': 'S1_Plus', 'py': 'S1_Plus', 'param': 'S1_Plus', 'type': 'double', 'default': 0.0, 'label': 'S1_Plus', 'sinput': False}, {'mql': 'S2_Symbol', 'py': 'S2_Symbol', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'S2_Symbol', 'sinput': False}, {'mql': 'S2_Invert', 'py': 'S2_Invert', 'param': 'S2_Invert', 'type': 'bool', 'default': False, 'label': 'S2_Invert', 'sinput': False}, {'mql': 'S2_K', 'py': 'S2_K', 'param': 'S2_K', 'type': 'double', 'default': 1.0, 'label': 'S2_K', 'sinput': False}, {'mql': 'S2_Plus', 'py': 'S2_Plus', 'param': 'S2_Plus', 'type': 'double', 'default': 0.0, 'label': 'S2_Plus', 'sinput': False}, {'mql': 'R_ArithmeticAction', 'py': 'R_ArithmeticAction', 'param': 'R_ArithmeticAction', 'type': 'int', 'default': 4, 'label': 'R_ArithmeticAction', 'sinput': False}, {'mql': 'R_Invert', 'py': 'R_Invert', 'param': 'R_Invert', 'type': 'bool', 'default': False, 'label': 'R_Invert', 'sinput': False}, {'mql': 'R_K', 'py': 'R_K', 'param': 'R_K', 'type': 'double', 'default': 1.0, 'label': 'R_K', 'sinput': False}, {'mql': 'R_Plus', 'py': 'R_Plus', 'param': 'R_Plus', 'type': 'double', 'default': 0.0, 'label': 'R_Plus', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter

# enum eAA
Add = 1
Subtract = 2
Multiply = 3
Divide = 4
_enum('eAA', {1: 'Add', 2: 'Subtract', 3: 'Multiply', 4: 'Divide'})

# ---- inputs and global variables
S1_Symbol = _input('S1_Symbol', 'EURUSD')  # S1_Symbol
S1_Invert = _input('S1_Invert', False)  # S1_Invert
S1_K = _input('S1_K', 1.0)  # S1_K
S1_Plus = _input('S1_Plus', 0.0)  # S1_Plus
S2_Symbol = _input('S2_Symbol', 'GBPUSD')  # S2_Symbol
S2_Invert = _input('S2_Invert', False)  # S2_Invert
S2_K = _input('S2_K', 1.0)  # S2_K
S2_Plus = _input('S2_Plus', 0.0)  # S2_Plus
R_ArithmeticAction = _input('R_ArithmeticAction', Divide)  # R_ArithmeticAction
R_Invert = _input('R_Invert', False)  # R_Invert
R_K = _input('R_K', 1.0)  # R_K
R_Plus = _input('R_Plus', 0.0)  # R_Plus
Buffer = Arr(0, 0.0)
MAHand = 0
TF = 0
TimeX = 0

def OnInit():
    SetIndexBuffer(0, Buffer, INDICATOR_DATA)
    return 0

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_err
    limit = 0
    mav1 = Arr(1, 0.0, dyn=False)
    mav2 = Arr(1, 0.0, dyn=False)
    tm1 = Arr(1, 0, dyn=False)
    tm2 = Arr(1, 0, dyn=False)
    if prev_calculated <= 0 or _s_OnCalculate_err:
        if not SymbolSelect(S1_Symbol, True):
            Alert('No symbol ' + S1_Symbol)
            Buffer[rates_total - 1] = EMPTY_VALUE
            _s_OnCalculate_err = True
            return 0
        if not SymbolSelect(S2_Symbol, True):
            Alert('No symbol ' + S2_Symbol)
            Buffer[rates_total - 1] = EMPTY_VALUE
            _s_OnCalculate_err = True
            return 0
        limit = 1
        b1 = Bars(S1_Symbol, PERIOD_CURRENT)
        b2 = Bars(S2_Symbol, PERIOD_CURRENT)
        if b1 == 0 or b2 == 0:
            Comment(MQL5InfoString(MQL5_PROGRAM_NAME) + ': Please wait...')
            Buffer[rates_total - 1] = EMPTY_VALUE
            _s_OnCalculate_err = True
            return 0
        cr1 = CopyTime(S1_Symbol, PERIOD_CURRENT, b1 - 1, 1, tm1)
        cr2 = CopyTime(S2_Symbol, PERIOD_CURRENT, b2 - 1, 1, tm2)
        if cr1 == -1 or cr2 == -1:
            Buffer[rates_total - 1] = EMPTY_VALUE
            _s_OnCalculate_err = True
            return 0
        for i in range(0, rates_total):
            if time[i] >= tm1[0] and time[i] >= tm2[0]:
                limit = i + 1
                break
        if _s_OnCalculate_err:
            Comment('')
            _s_OnCalculate_err = False
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, limit)
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        CopyClose(S1_Symbol, PERIOD_CURRENT, _DT(time[i]), 1, mav1)
        CopyClose(S2_Symbol, PERIOD_CURRENT, _DT(time[i]), 1, mav2)
        if mav1[0] == 0 or mav2[0] == 0:
            Buffer[i] = Buffer[i - 1]
            continue
        if S1_Invert:
            mav1[0] = _fdiv(1.0, mav1[0])
        if S2_Invert:
            mav2[0] = _fdiv(1.0, mav2[0])
        mav1[0] *= S1_K
        mav2[0] *= S2_K
        mav1[0] += S1_Plus
        mav2[0] += S1_Plus
        _sw1 = R_ArithmeticAction
        if _sw1 == 1:
            Buffer[i] = mav1[0] + mav2[0]
        elif _sw1 == 2:
            Buffer[i] = mav1[0] - mav2[0]
        elif _sw1 == 3:
            Buffer[i] = mav1[0] * mav2[0]
        elif _sw1 == 4:
            if mav2[0] == 0:
                Buffer[i] = Buffer[i - 1]
            else:
                Buffer[i] = _fdiv(mav1[0], mav2[0])
        if R_Invert:
            if Buffer[i] == 0:
                Buffer[i] = Buffer[i - 1]
            else:
                Buffer[i] = _fdiv(1.0, Buffer[i])
        Buffer[i] *= R_K
        Buffer[i] += R_Plus
    return rates_total

# ---- static local variables
_s_OnCalculate_err = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IcrosscloseEn(_MQL5Indicator):
    name = 'icrossclose_en'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'S1_Invert': False,  # S1_Invert
        'S1_K': 1.0,  # S1_K
        'S1_Plus': 0.0,  # S1_Plus
        'S2_Invert': False,  # S2_Invert
        'S2_K': 1.0,  # S2_K
        'S2_Plus': 0.0,  # S2_Plus
        'R_ArithmeticAction': _Choice({1: 'Add', 2: 'Subtract', 3: 'Multiply', 4: 'Divide'}, default=4),  # R_ArithmeticAction
        'R_Invert': False,  # R_Invert
        'R_K': 1.0,  # R_K
        'R_Plus': 0.0,  # R_Plus
    }

