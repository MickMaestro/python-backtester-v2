"""Stochastic_Chaikins_Volatility — converted from MQL5: MQL5 Indicators/Stochastic_Chaikins_Volatility_HTF/Stochastic_Chaikins_Volatility.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [13749760, 6053069]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Stochastic_Chaikins_Volatility'}, 'levels': [], 'description': [], 'name': 'Stochastic_Chaikins_Volatility', 'source': 'MQL5 Indicators/Stochastic_Chaikins_Volatility_HTF/Stochastic_Chaikins_Volatility.mq5', 'folder': 'Stochastic_Chaikins_Volatility_HTF', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 10, 'label': 'глубина  первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр первого сглаживания,', 'sinput': False}, {'mql': 'StocLength', 'py': 'StocLength', 'param': 'StocLength', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'метод усреднения второго сглаживания', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 5, 'label': 'глубина  второго сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'параметр второго сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 80, 'label': '', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'uint', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 20, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_SMA_)  # метод усреднения первого сглаживания
Length1 = _input('Length1', 10)  # глубина  первого сглаживания
Phase1 = _input('Phase1', 15)  # параметр первого сглаживания,
StocLength = _input('StocLength', 5)
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # метод усреднения второго сглаживания
Length2 = _input('Length2', 5)  # глубина  второго сглаживания
Phase2 = _input('Phase2', 15)  # параметр второго сглаживания,
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
HighLevel = _input('HighLevel', 80)
MiddleLevel = _input('MiddleLevel', 50)
LowLevel = _input('LowLevel', 20)
IndBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
Count = Arr(0, 0)
chakin = Arr(0, 0.0)

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
    min_rates_1 = GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_2 = min_rates_1 + _int(StocLength) + 1
    min_rates_total = min_rates_2 + GetStartBars(MA_Method2, Length2, Phase2)
    ArrayResize(Count, StocLength)
    ArrayResize(chakin, StocLength)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    shortname = 'Stochastic_Chaikins_Volatility'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        ArrayInitialize(Count, None)
        ArrayInitialize(chakin, None)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        chakin[Count[0]] = XMA1.XMASeries(1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, high[bar] - low[bar], bar, False)
        hh = chakin[Count[0]]
        ll = chakin[Count[0]]
        for iii in range(0, _int(StocLength)):
            hh = MathMax(hh, chakin[iii])
            ll = MathMin(ll, chakin[iii])
        Value1 = chakin[Count[0]] - ll
        Value2 = MathMax(1 * Point(), hh - ll)
        IndBuffer[bar] = 100 * XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, MA_Method2, Phase2, Length2, _fdiv(Value1, Value2), bar, False)
        TriggerBuffer[bar] = IndBuffer[bar - 1]
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


class StochasticChaikinsVolatility(_MQL5Indicator):
    name = 'Stochastic_Chaikins_Volatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения первого сглаживания
        'Length1': 10,  # глубина  первого сглаживания
        'Phase1': 15,  # параметр первого сглаживания,
        'StocLength': 5,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения второго сглаживания
        'Length2': 5,  # глубина  второго сглаживания
        'Phase2': 15,  # параметр второго сглаживания,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'HighLevel': 80,
        'MiddleLevel': 50,
        'LowLevel': 20,
    }

