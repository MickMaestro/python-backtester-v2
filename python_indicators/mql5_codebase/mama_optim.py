"""mama_optim — converted from MQL5: MQL5 Indicators/MAMA/mama_optim.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65280], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MAMA', 2: 'FAMA'}, 'levels': [], 'description': [], 'name': 'mama_optim', 'source': 'MQL5 Indicators/MAMA/mama_optim.mq5', 'folder': 'MAMA', 'inputs': [], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastLimit = 0.5
SlowLimit = 0.05
MAMABuffer = Arr(0, 0.0)
FAMABuffer = Arr(0, 0.0)
StartBar = 0

def CountVelue(CoArr, Array1, Array2):
    Resalt = ((0.0962 * Array1[CoArr[0]]) + (0.5769 * Array1[CoArr[2]]) - (0.5769 * Array1[CoArr[4]]) - (0.0962 * Array1[CoArr[6]])) * ((0.075 * Array2[CoArr[1]]) + 0.54)
    return Resalt

def SmoothVelue(CoArr, Array):
    return (0.2 * Array[CoArr[0]]) + (0.8 * Array[CoArr[1]])

def Recount_ArrayZeroPos(CoArr):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = 6
    for iii in range(0, 7):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > 6:
            numb -= 7
        CoArr[iii] = numb

def OnInit():
    global StartBar
    StartBar = 7 + 1
    SetIndexBuffer(0, MAMABuffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'MAMA')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBar)
    SetIndexBuffer(1, FAMABuffer, INDICATOR_DATA)
    PlotIndexSetString(1, PLOT_LABEL, 'FAMA')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBar + 1)
    shortname = Box("")
    StringConcatenate(shortname, 'The MESA Adaptive Moving Average(', FastLimit, ', ', SlowLimit, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (StartBar + begin):
        return 0
    first = 0
    bar = 0
    Bar0 = 0
    Bar1 = 0
    Bar3 = 0
    DeltaPhase = 0.0
    alpha = 0.0
    if prev_calculated == 0:
        first = StartBar + begin
        ArrayInitialize(_s_OnCalculate_smooth, 0.0)
        ArrayInitialize(_s_OnCalculate_detrender, 0.0)
        ArrayInitialize(_s_OnCalculate_period, 0.0)
        ArrayInitialize(_s_OnCalculate_Phase, 0.0)
        ArrayInitialize(_s_OnCalculate_Q1, 0.0)
        ArrayInitialize(_s_OnCalculate_I1, 0.0)
        ArrayInitialize(_s_OnCalculate_I2, 0.0)
        ArrayInitialize(_s_OnCalculate_Q2, 0.0)
        ArrayInitialize(_s_OnCalculate_jI, 0.0)
        ArrayInitialize(_s_OnCalculate_jQ, 0.0)
        ArrayInitialize(_s_OnCalculate_Re, 0.0)
        ArrayInitialize(_s_OnCalculate_Im, 0.0)
        MAMABuffer[first - 1] = price[first - 1]
        FAMABuffer[first - 1] = price[first - 1]
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Bar0 = _s_OnCalculate_Count[0]
        Bar1 = _s_OnCalculate_Count[1]
        Bar3 = _s_OnCalculate_Count[3]
        _s_OnCalculate_smooth[Bar0] = ((4 * price[bar - 0]) + (3 * price[bar - 1]) + (2 * price[bar - 2]) + (1 * price[bar - 3])) / 10.0
        _s_OnCalculate_detrender[Bar0] = CountVelue(_s_OnCalculate_Count, _s_OnCalculate_smooth, _s_OnCalculate_period)
        _s_OnCalculate_Q1[Bar0] = CountVelue(_s_OnCalculate_Count, _s_OnCalculate_detrender, _s_OnCalculate_period)
        _s_OnCalculate_I1[Bar0] = _s_OnCalculate_detrender[Bar3]
        _s_OnCalculate_jI[Bar0] = CountVelue(_s_OnCalculate_Count, _s_OnCalculate_I1, _s_OnCalculate_I1)
        _s_OnCalculate_jQ[Bar0] = CountVelue(_s_OnCalculate_Count, _s_OnCalculate_Q1, _s_OnCalculate_Q1)
        _s_OnCalculate_I2[Bar0] = _s_OnCalculate_I1[Bar0] - _s_OnCalculate_jQ[Bar0]
        _s_OnCalculate_Q2[Bar0] = _s_OnCalculate_Q1[Bar0] - _s_OnCalculate_jI[Bar0]
        _s_OnCalculate_I2[Bar0] = SmoothVelue(_s_OnCalculate_Count, _s_OnCalculate_I2)
        _s_OnCalculate_Q2[Bar0] = SmoothVelue(_s_OnCalculate_Count, _s_OnCalculate_Q2)
        _s_OnCalculate_Re[Bar0] = (_s_OnCalculate_I2[Bar0] * _s_OnCalculate_I2[Bar1]) + (_s_OnCalculate_Q2[Bar0] * _s_OnCalculate_Q2[Bar1])
        _s_OnCalculate_Im[Bar0] = (_s_OnCalculate_I2[Bar0] * _s_OnCalculate_Q2[Bar1]) - (_s_OnCalculate_Q2[Bar0] * _s_OnCalculate_I2[Bar1])
        _s_OnCalculate_Re[Bar0] = SmoothVelue(_s_OnCalculate_Count, _s_OnCalculate_Re)
        _s_OnCalculate_Im[Bar0] = SmoothVelue(_s_OnCalculate_Count, _s_OnCalculate_Im)
        if _s_OnCalculate_Im[Bar0] != 0 and _s_OnCalculate_Re[Bar0] != 0:
            _s_OnCalculate_period[Bar0] = _fdiv(6.285714, MathArctan(_fdiv(_s_OnCalculate_Im[Bar0], _s_OnCalculate_Re[Bar0])))
        if _s_OnCalculate_period[Bar0] > (1.5 * _s_OnCalculate_period[Bar1]):
            _s_OnCalculate_period[Bar0] = 1.5 * _s_OnCalculate_period[Bar1]
        if _s_OnCalculate_period[Bar0] < (0.67 * _s_OnCalculate_period[Bar1]):
            _s_OnCalculate_period[Bar0] = 0.67 * _s_OnCalculate_period[Bar1]
        if _s_OnCalculate_period[Bar0] < 6.0:
            _s_OnCalculate_period[Bar0] = 6.0
        if _s_OnCalculate_period[Bar0] > 50.0:
            _s_OnCalculate_period[Bar0] = 50.0
        _s_OnCalculate_period[Bar0] = (0.2 * _s_OnCalculate_period[Bar0]) + (0.8 * _s_OnCalculate_period[Bar1])
        if _s_OnCalculate_I1[Bar0] != 0:
            _s_OnCalculate_Phase[Bar0] = 57.27272987 * MathArctan(_fdiv(_s_OnCalculate_Q1[Bar0], _s_OnCalculate_I1[Bar0]))
        DeltaPhase = _s_OnCalculate_Phase[Bar1] - _s_OnCalculate_Phase[Bar0]
        if DeltaPhase < 1:
            DeltaPhase = 1.0
        alpha = _fdiv(FastLimit, DeltaPhase)
        if alpha < SlowLimit:
            alpha = SlowLimit
        MAMABuffer[bar] = (alpha * price[bar]) + ((1.0 - alpha) * MAMABuffer[bar - 1])
        FAMABuffer[bar] = (0.5 * alpha * MAMABuffer[bar]) + ((1.0 - (0.5 * alpha)) * FAMABuffer[bar - 1])
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(_s_OnCalculate_Count)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_smooth = Arr(7, 0.0, dyn=False)
_s_OnCalculate_detrender = Arr(7, 0.0, dyn=False)
_s_OnCalculate_Q1 = Arr(7, 0.0, dyn=False)
_s_OnCalculate_I1 = Arr(7, 0.0, dyn=False)
_s_OnCalculate_I2 = Arr(7, 0.0, dyn=False)
_s_OnCalculate_Q2 = Arr(7, 0.0, dyn=False)
_s_OnCalculate_jI = Arr(7, 0.0, dyn=False)
_s_OnCalculate_jQ = Arr(7, 0.0, dyn=False)
_s_OnCalculate_Re = Arr(7, 0.0, dyn=False)
_s_OnCalculate_Im = Arr(7, 0.0, dyn=False)
_s_OnCalculate_period = Arr(7, 0.0, dyn=False)
_s_OnCalculate_Phase = Arr(7, 0.0, dyn=False)
_s_OnCalculate_Count = Arr(7, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MamaOptim(_MQL5Indicator):
    name = 'mama_optim'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

