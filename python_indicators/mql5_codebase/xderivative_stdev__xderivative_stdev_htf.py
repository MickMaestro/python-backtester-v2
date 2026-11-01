"""XDerivative_StDev — converted from MQL5: MQL5 Indicators/XDerivative_StDev_HTF/XDerivative_StDev.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [16748574], 2: [255], 3: [8388352], 4: [255], 5: [8388352]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 4, 5: 4}, 'styles': {1: 0}, 'labels': {1: 'XDerivative', 2: 'Dn_Signal 1', 3: 'Up_Signal 1', 4: 'Dn_Signal 2', 5: 'Up_Signal 2'}, 'levels': [], 'description': [], 'name': 'XDerivative_StDev', 'source': 'MQL5 Indicators/XDerivative_StDev_HTF/XDerivative_StDev.mq5', 'folder': 'XDerivative_StDev_HTF', 'inputs': [{'mql': 'i_slowing', 'py': 'i_slowing', 'param': 'i_slowing', 'type': 'uint', 'default': 34, 'label': 'Slowing / Запаздывание', 'sinput': False}, {'mql': 'i_price', 'py': 'i_price', 'param': 'i_price', 'type': 'int', 'default': 7, 'label': 'Applied price / Используемая цена', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 7, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'dK1', 'py': 'dK1', 'param': 'dK1', 'type': 'double', 'default': 1.5, 'label': 'коэффициент 1 для квадратичного фильтра', 'sinput': False}, {'mql': 'dK2', 'py': 'dK2', 'param': 'dK2', 'type': 'double', 'default': 2.5, 'label': 'коэффициент 2 для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'период квадратичного фильтра', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_PRICE_TYPE
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
_enum('ENUM_PRICE_TYPE', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
i_slowing = _input('i_slowing', 34)  # Slowing / Запаздывание
i_price = _input('i_price', PRICE_WEIGHTED_)  # Applied price / Используемая цена
XMA_Method = _input('XMA_Method', MODE_JJMA)  # метод усреднения
XLength = _input('XLength', 7)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
dK1 = _input('dK1', 1.5)  # коэффициент 1 для квадратичного фильтра
dK2 = _input('dK2', 2.5)  # коэффициент 2 для квадратичного фильтра
std_period = _input('std_period', 9)  # период квадратичного фильтра
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
BearsBuffer1 = Arr(0, 0.0)
BullsBuffer1 = Arr(0, 0.0)
BearsBuffer2 = Arr(0, 0.0)
BullsBuffer2 = Arr(0, 0.0)
DDer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_total = 0

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = _int(i_slowing)
    min_rates_total = min_rates_1 + GetStartBars(XMA_Method, XLength, XPhase) + _int(std_period)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    ArrayResize(DDer, std_period)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, BearsBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, BullsBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, BearsBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, BullsBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'XDerivative_StDev(', i_slowing, ', ', XLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    der = 0.0
    SMAdif = 0.0
    Sum = 0.0
    StDev = 0.0
    dstd = 0.0
    BEARS1 = 0.0
    BULLS1 = 0.0
    BEARS2 = 0.0
    BULLS2 = 0.0
    Filter1 = 0.0
    Filter2 = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        der = (100.0 * (PriceSeries(i_price, bar, open, low, high, close) - PriceSeries(i_price, bar - i_slowing, open, low, high, close))) / i_slowing
        IndBuffer[bar] = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, der, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        for iii in range(0, _int(std_period)):
            DDer[iii] = IndBuffer[bar - iii] - IndBuffer[bar - iii - 1]
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += DDer[iii]
        SMAdif = Sum / std_period
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += MathPow(DDer[iii] - SMAdif, 2)
        StDev = MathSqrt(Sum / std_period)
        dstd = NormalizeDouble(DDer[0], Digits() + 2)
        Filter1 = NormalizeDouble(dK1 * StDev, Digits() + 2)
        Filter2 = NormalizeDouble(dK2 * StDev, Digits() + 2)
        BEARS1 = EMPTY_VALUE
        BULLS1 = EMPTY_VALUE
        BEARS2 = EMPTY_VALUE
        BULLS2 = EMPTY_VALUE
        der = IndBuffer[bar]
        if dstd < (-Filter1) and dstd >= (-Filter2):
            BEARS1 = der
        if dstd < (-Filter2):
            BEARS2 = der
        if dstd > Filter1 and dstd <= Filter2:
            BULLS1 = der
        if dstd > Filter2:
            BULLS2 = der
        BullsBuffer1[bar] = BULLS1
        BearsBuffer1[bar] = BEARS1
        BullsBuffer2[bar] = BULLS2
        BearsBuffer2[bar] = BEARS2
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XDerivativeStDev(_MQL5Indicator):
    name = 'XDerivative_StDev'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'i_slowing': 34,  # Slowing / Запаздывание
        'i_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=7),  # Applied price / Используемая цена
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'XLength': 7,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'dK1': 1.5,  # коэффициент 1 для квадратичного фильтра
        'dK2': 2.5,  # коэффициент 2 для квадратичного фильтра
        'std_period': 9,  # период квадратичного фильтра
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

