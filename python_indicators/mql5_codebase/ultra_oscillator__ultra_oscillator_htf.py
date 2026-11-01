"""ultra_oscillator — converted from MQL5: MQL5 Indicators/Ultra_Oscillator_HTF/ultra_oscillator.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Ultra_Oscillator'}, 'levels': [], 'description': [], 'name': 'ultra_oscillator', 'source': 'MQL5 Indicators/Ultra_Oscillator_HTF/ultra_oscillator.mq5', 'folder': 'Ultra_Oscillator_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 3, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'int', 'default': 7, 'label': 'Глубина сглаживания 1', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'int', 'default': 14, 'label': 'Глубина сглаживания 2', 'sinput': False}, {'mql': 'XLength3', 'py': 'XLength3', 'param': 'XLength3', 'type': 'int', 'default': 28, 'label': 'Глубина сглаживания 3', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_LWMA)  # Метод усреднения
XLength1 = _input('XLength1', 7)  # Глубина сглаживания 1
XLength2 = _input('XLength2', 14)  # Глубина сглаживания 2
XLength3 = _input('XLength3', 28)  # Глубина сглаживания 3
XPhase = _input('XPhase', 15)  # Параметр сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    Length = MathMax(XLength1, MathMax(XLength2, XLength3))
    min_rates_total = GetStartBars(XMA_Method, Length, XPhase)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'Ultra_Oscillator(', XLength1, ', ', XLength2, ', ', XLength3, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        IndBuffer[bar] = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, price, bar, False) + XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, price, bar, False) + XMA3.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength3, price, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UltraOscillator(_MQL5Indicator):
    name = 'ultra_oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения
        'XLength1': 7,  # Глубина сглаживания 1
        'XLength2': 14,  # Глубина сглаживания 2
        'XLength3': 28,  # Глубина сглаживания 3
        'XPhase': 15,  # Параметр сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

