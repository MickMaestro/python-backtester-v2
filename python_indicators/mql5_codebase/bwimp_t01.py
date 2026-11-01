"""bwimp-t01 — converted from MQL5: MQL5 Indicators/BWImp-T01_HTF/bwimp-t01.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'BWImp-T01'}, 'levels': [], 'description': [], 'name': 'bwimp-t01', 'source': 'MQL5 Indicators/BWImp-T01_HTF/bwimp-t01.mq5', 'folder': 'BWImp-T01_HTF', 'inputs': [{'mql': 'Period1', 'py': 'Period1', 'param': 'Period1', 'type': 'uint', 'default': 96, 'label': 'Период 1', 'sinput': False}, {'mql': 'Period2', 'py': 'Period2', 'param': 'Period2', 'type': 'uint', 'default': 3, 'label': 'Период 2', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 8, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 70, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
Period1 = _input('Period1', 96)  # Период 1
Period2 = _input('Period2', 3)  # Период 2
XMA_Method = _input('XMA_Method', MODE_T3)  # Метод сглаживания
XLength = _input('XLength', 8)  # Глубина сглаживания
XPhase = _input('XPhase', 70)  # Параметр сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
Point10 = 0.0
min_rates_1 = 0
min_rates_total = 0
Count = Arr(0, 0)
impr = Arr(0, 0.0)
impb = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def Get_dPrice(Price1, Price2, index):
    return Price1[index] - Price2[index]

def OnInit():
    global Point10, min_rates_1, min_rates_total
    min_rates_1 = _int(Period1 + Period2)
    min_rates_total = min_rates_1 + XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    Point10 = Point() / 10
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    ArrayResize(Count, Period2)
    ArrayResize(impr, Period2)
    ArrayResize(impb, Period2)
    ArrayInitialize(Count, 0)
    ArrayInitialize(impr, 0.0)
    ArrayInitialize(impb, 0.0)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'BWImp-T01(', XLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    imppr = 0.0
    imppb = 0.0
    sipr = 0.0
    sipb = 0.0
    sum_ = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = _int(Period1)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        imppr = 0.0
        imppb = 0.0
        for kkk in range(0, _int(Period1)):
            diff = Get_dPrice(close, open, bar - kkk)
            if diff > 0:
                imppr += diff
            if diff < 0:
                imppb += diff
        imppr = MathRound(_fdiv(imppr, Point()))
        imppb = MathRound(_fdiv(imppb, Point()))
        if not imppr:
            imppr = Point10
        if not imppb:
            imppb = Point10
        impr[Count[0]] = imppr
        impb[Count[0]] = imppb
        sipr = 0.0
        sipb = 0.0
        for kkk in range(0, _int(Period2)):
            sipr += impr[kkk]
            sipb += impb[kkk]
        sipr = MathRound(sipr / Period2)
        sipb = MathRound(sipb / Period2)
        sum_ = sipr + sipb
        IndBuffer[bar] = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, sum_, bar, False)
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, Period2)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BwimpT01(_MQL5Indicator):
    name = 'bwimp-t01'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period1': 96,  # Период 1
        'Period2': 3,  # Период 2
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Метод сглаживания
        'XLength': 8,  # Глубина сглаживания
        'XPhase': 70,  # Параметр сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

