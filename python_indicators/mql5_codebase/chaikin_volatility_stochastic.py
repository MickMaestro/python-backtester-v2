"""Chaikin_Volatility_Stochastic — converted from MQL5: MQL5 Indicators/Chaikin_Volatility_Stochastic/Chaikin_Volatility_Stochastic.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16711680, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Chaikin_Volatility_Stochastic'}, 'levels': [], 'description': [], 'name': 'Chaikin_Volatility_Stochastic', 'source': 'MQL5 Indicators/Chaikin_Volatility_Stochastic/Chaikin_Volatility_Stochastic.mq5', 'folder': 'Chaikin_Volatility_Stochastic', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 10, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'StocLength', 'py': 'StocLength', 'param': 'StocLength', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'WMALength', 'py': 'WMALength', 'param': 'WMALength', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_EMA_)  # метод усреднения
XLength = _input('XLength', 10)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
StocLength = _input('StocLength', 5)
WMALength = _input('WMALength', 5)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
Count = Arr(0, 0)
xrange = Arr(0, 0.0)

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

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    min_rates_2 = min_rates_1 + _int(StocLength)
    min_rates_total = min_rates_2 + _int(WMALength + 1)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    ArrayResize(Count, StocLength)
    ArrayResize(xrange, StocLength)
    ArrayInitialize(Count, 0.0)
    ArrayInitialize(xrange, 0.0)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Chaikin_Volatility_Stochastic')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        ArrayInitialize(Count, 0.0)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        range_ = high[bar] - low[bar]
        xrange[Count[0]] = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, range_, bar, False)
        _chakin = xrange[Count[0]]
        hh = _chakin
        ll = _chakin
        for iii in range(0, _int(StocLength)):
            tmp = xrange[Count[iii]]
            hh = MathMax(hh, tmp)
            ll = MathMin(ll, tmp)
        Value1 = _chakin - ll
        Value2 = hh - ll
        Value3 = 0.0
        if Value2:
            Value3 = _fdiv(Value1, Value2)
        IndBuffer[bar] = 100 * XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, MODE_LWMA_, 0, WMALength, Value3, bar, False)
        TriggerBuffer[bar] = IndBuffer[MathMax(bar - 1, 0)]
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, StocLength)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChaikinVolatilityStochastic(_MQL5Indicator):
    name = 'Chaikin_Volatility_Stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # метод усреднения
        'XLength': 10,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'StocLength': 5,
        'WMALength': 5,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

