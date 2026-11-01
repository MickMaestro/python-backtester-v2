"""xenvelopes3 — converted from MQL5: MQL5 Indicators/XEnvelopes3_HTF/xenvelopes3.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 7, 4: 7, 5: 7}, 'colors': {1: [16436871], 2: [10025880], 3: [16443110], 4: [13353215], 5: [15631086]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Upper XEnvelopes3 Cloud', 2: 'Upper XEnvelopes2 Cloud', 3: 'XEnvelopes1 Cloud', 4: 'Lower XEnvelopes2 Cloud', 5: 'Lower XEnvelopes3 Cloud'}, 'levels': [], 'description': [''], 'name': 'xenvelopes3', 'source': 'MQL5 Indicators/XEnvelopes3_HTF/xenvelopes3.mq5', 'folder': 'XEnvelopes3_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 12, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Deviation1', 'py': 'Deviation1', 'param': 'Deviation1', 'type': 'double', 'default': 0.1, 'label': 'Девиация 1', 'sinput': False}, {'mql': 'Deviation2', 'py': 'Deviation2', 'param': 'Deviation2', 'type': 'double', 'default': 0.3, 'label': 'Девиация 2', 'sinput': False}, {'mql': 'Deviation3', 'py': 'Deviation3', 'param': 'Deviation3', 'type': 'double', 'default': 0.6, 'label': 'Девиация 3', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
XLength = _input('XLength', 12)  # Глубина сглаживания
XPhase = _input('XPhase', 15)  # Параметр сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Deviation1 = _input('Deviation1', 0.1)  # Девиация 1
Deviation2 = _input('Deviation2', 0.3)  # Девиация 2
Deviation3 = _input('Deviation3', 0.6)  # Девиация 3
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
UpBuffer1 = Arr(0, 0.0)
DnBuffer1 = Arr(0, 0.0)
UpBuffer2 = Arr(0, 0.0)
DnBuffer2 = Arr(0, 0.0)
UpBuffer3 = Arr(0, 0.0)
DnBuffer3 = Arr(0, 0.0)
UpBuffer4 = Arr(0, 0.0)
DnBuffer4 = Arr(0, 0.0)
UpBuffer5 = Arr(0, 0.0)
DnBuffer5 = Arr(0, 0.0)
dPriceShift = 0.0
UpKdev1 = 0.0
DnKdev1 = 0.0
UpKdev2 = 0.0
DnKdev2 = 0.0
UpKdev3 = 0.0
DnKdev3 = 0.0
min_rates_total = 0

def OnInit():
    global DnKdev1, DnKdev2, DnKdev3, UpKdev1, UpKdev2, UpKdev3, dPriceShift, min_rates_total
    min_rates_total = XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    if Deviation1 >= Deviation2:
        Print('Входной параметр Девиация 2 всегда должен быть больше входного параметра Девиация 1! Исправьте значения этих входных параметров индикатора!')
        return INIT_FAILED
    if Deviation2 >= Deviation3:
        Print('Входной параметр Девиация 3 всегда должен быть больше входного параметра Девиация 2! Исправьте значения этих входных параметров индикатора!')
        return INIT_FAILED
    UpKdev1 = 1 + (Deviation1 / 100.0)
    DnKdev1 = 1 - (Deviation1 / 100.0)
    UpKdev2 = 1 + (Deviation2 / 100.0)
    DnKdev2 = 1 - (Deviation2 / 100.0)
    UpKdev3 = 1 + (Deviation3 / 100.0)
    DnKdev3 = 1 - (Deviation3 / 100.0)
    SetIndexBuffer(0, UpBuffer4, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer4, INDICATOR_DATA)
    SetIndexBuffer(2, UpBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, DnBuffer2, INDICATOR_DATA)
    SetIndexBuffer(4, UpBuffer1, INDICATOR_DATA)
    SetIndexBuffer(5, DnBuffer1, INDICATOR_DATA)
    SetIndexBuffer(6, UpBuffer3, INDICATOR_DATA)
    SetIndexBuffer(7, DnBuffer3, INDICATOR_DATA)
    SetIndexBuffer(8, UpBuffer5, INDICATOR_DATA)
    SetIndexBuffer(9, DnBuffer5, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Env(' + _str(XLength) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'Env(' + _str(XLength) + ')Upper Cloud3')
    PlotIndexSetString(1, PLOT_LABEL, 'Env(' + _str(XLength) + ')Upper Cloud2')
    PlotIndexSetString(2, PLOT_LABEL, 'Env(' + _str(XLength) + ')Cloud1')
    PlotIndexSetString(3, PLOT_LABEL, 'Env(' + _str(XLength) + ')Lower Cloud2')
    PlotIndexSetString(4, PLOT_LABEL, 'Env(' + _str(XLength) + ')Lower Cloud3')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    xma = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        xma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price, bar, False)
        UpBuffer4[bar] = (UpKdev3 * xma) + dPriceShift
        DnBuffer2[bar] = (UpKdev1 * xma) + dPriceShift
        UpBuffer1[bar] = DnBuffer2[bar]
        UpBuffer3[bar] = (DnKdev1 * xma) + dPriceShift
        DnBuffer1[bar] = UpBuffer3[bar]
        DnBuffer4[bar] = (UpKdev2 * xma) + dPriceShift
        UpBuffer2[bar] = DnBuffer4[bar]
        UpBuffer5[bar] = (DnKdev2 * xma) + dPriceShift
        DnBuffer3[bar] = UpBuffer5[bar]
        DnBuffer5[bar] = (DnKdev3 * xma) + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Xenvelopes3(_MQL5Indicator):
    name = 'xenvelopes3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XLength': 12,  # Глубина сглаживания
        'XPhase': 15,  # Параметр сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Deviation1': 0.1,  # Девиация 1
        'Deviation2': 0.3,  # Девиация 2
        'Deviation3': 0.6,  # Девиация 3
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

