"""atr_ma_oscillator — converted from MQL5: MQL5 Indicators/ATR_MA_Oscillator_HTF/atr_ma_oscillator.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ATR_MA_Oscillator'}, 'levels': [], 'description': [], 'name': 'atr_ma_oscillator', 'source': 'MQL5 Indicators/ATR_MA_Oscillator_HTF/atr_ma_oscillator.mq5', 'folder': 'ATR_MA_Oscillator_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 3, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 100, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'SXMA_Method', 'py': 'SXMA_Method', 'param': 'SXMA_Method', 'type': 'int', 'default': 3, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'SXLength', 'py': 'SXLength', 'param': 'SXLength', 'type': 'int', 'default': 100, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'SXPhase', 'py': 'SXPhase', 'param': 'SXPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_LWMA)  # Метод усреднения
XLength = _input('XLength', 100)  # Глубина сглаживания
XPhase = _input('XPhase', 15)  # Параметр сглаживания
SXMA_Method = _input('SXMA_Method', MODE_LWMA)  # Метод усреднения
SXLength = _input('SXLength', 100)  # Глубина сглаживания
SXPhase = _input('SXPhase', 15)  # Параметр сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_ = 0

def OnInit():
    global min_rates_, min_rates_total
    min_rates_ = XATR1.GetStartBars(XMA_Method, XLength, XPhase) + 1
    min_rates_total = min_rates_ + XATR1.GetStartBars(SXMA_Method, SXLength, SXPhase)
    XATR1.XMALengthCheck('XLength', XLength)
    XATR1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    XATR1.XMALengthCheck('SXLength', SXLength)
    XATR1.XMAPhaseCheck('SXPhase', SXPhase, SXMA_Method)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR_MA_Oscillator')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    atr = 0.0
    xatr = 0.0
    xxatr = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        atr = MathMax(high[bar], close[bar - 1]) - MathMin(low[bar], close[bar - 1])
        atr = _fdiv(atr, Point())
        xatr = XATR1.XMASeries(1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, atr, bar, False)
        xxatr = XATR2.XMASeries(min_rates_, prev_calculated, rates_total, SXMA_Method, SXPhase, SXLength, xatr, bar, False)
        IndBuffer[bar] = xatr - xxatr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XATR1 = _alloc(CXMA)
XATR1.__init__()
XATR2 = _alloc(CXMA)
XATR2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AtrMaOscillator(_MQL5Indicator):
    name = 'atr_ma_oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения
        'XLength': 100,  # Глубина сглаживания
        'XPhase': 15,  # Параметр сглаживания
        'SXMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения
        'SXLength': 100,  # Глубина сглаживания
        'SXPhase': 15,  # Параметр сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

