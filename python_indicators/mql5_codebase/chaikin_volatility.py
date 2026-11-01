"""chaikin_volatility — converted from MQL5: MQL5 Indicators/Chaikin_Volatility/chaikin_volatility.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [7504122]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Chaikin_Volatility'}, 'levels': [], 'description': [], 'name': 'chaikin_volatility', 'source': 'MQL5 Indicators/Chaikin_Volatility/chaikin_volatility.mq5', 'folder': 'Chaikin_Volatility', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 10, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания,', 'sinput': False}, {'mql': 'ROCPeriod', 'py': 'ROCPeriod', 'param': 'ROCPeriod', 'type': 'uint', 'default': 10, 'label': 'Глубина второго сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_EMA)  # Метод усреднения
XLength = _input('XLength', 10)  # Глубина сглаживания
XPhase = _input('XPhase', 15)  # Параметр сглаживания,
ROCPeriod = _input('ROCPeriod', 10)  # Глубина второго сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
Count = Arr(0, 0)
xrange = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = 7
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
    global min_rates_1, min_rates_total
    min_rates_1 = XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    min_rates_total = min_rates_1 + _int(ROCPeriod + 1)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    ArrayResize(Count, ROCPeriod + 1)
    ArrayResize(xrange, ROCPeriod + 1)
    ArrayInitialize(Count, 0)
    ArrayInitialize(xrange, 0)
    ArrayInitialize(xrange, 0.0)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Chaikin_Volatility')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    range_ = 0.0
    xrangeX = 0.0
    ratio = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        range_ = high[bar] - low[bar]
        xrange[Count[0]] = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, range_, bar, False)
        xrangeX = xrange[Count[ROCPeriod]]
        if xrangeX:
            ratio = _fdiv(xrange[Count[0]] - xrangeX, xrangeX) * 100
        else:
            ratio = 1.0
        IndBuffer[bar] = ratio
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count)
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


class ChaikinVolatility(_MQL5Indicator):
    name = 'chaikin_volatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения
        'XLength': 10,  # Глубина сглаживания
        'XPhase': 15,  # Параметр сглаживания,
        'ROCPeriod': 10,  # Глубина второго сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

