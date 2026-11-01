"""colorzerolagx10ma_stdev — converted from MQL5: MQL5 Indicators/ColorZerolagX10MA_StDev/colorzerolagx10ma_stdev.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 8, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [255, 8421504, 8421376], 2: [255], 3: [16776960], 4: [255], 5: [16776960]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 4, 5: 4}, 'styles': {1: 0}, 'labels': {1: 'ColorZerolagX10MA', 2: 'Dn_Signal 1', 3: 'Up_Signal 1', 4: 'Dn_Signal 2', 5: 'Up_Signal 2'}, 'levels': [], 'description': [], 'name': 'colorzerolagx10ma_stdev', 'source': 'MQL5 Indicators/ColorZerolagX10MA_StDev/colorzerolagx10ma_stdev.mq5', 'folder': 'ColorZerolagX10MA_StDev', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 3, 'label': 'Глубина усреднения 1', 'sinput': False}, {'mql': 'Factor1', 'py': 'Factor1', 'param': 'Factor1', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 5, 'label': 'Глубина усреднения 2', 'sinput': False}, {'mql': 'Factor2', 'py': 'Factor2', 'param': 'Factor2', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'Length3', 'py': 'Length3', 'param': 'Length3', 'type': 'uint', 'default': 7, 'label': 'Глубина усреднения 3', 'sinput': False}, {'mql': 'Factor3', 'py': 'Factor3', 'param': 'Factor3', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'Length4', 'py': 'Length4', 'param': 'Length4', 'type': 'uint', 'default': 9, 'label': 'Глубина усреднения 4', 'sinput': False}, {'mql': 'Factor4', 'py': 'Factor4', 'param': 'Factor4', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'Length5', 'py': 'Length5', 'param': 'Length5', 'type': 'uint', 'default': 11, 'label': 'Глубина усреднения 5', 'sinput': False}, {'mql': 'Factor5', 'py': 'Factor5', 'param': 'Factor5', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'Length6', 'py': 'Length6', 'param': 'Length6', 'type': 'uint', 'default': 13, 'label': 'Глубина усреднения 6', 'sinput': False}, {'mql': 'Factor6', 'py': 'Factor6', 'param': 'Factor6', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'Length7', 'py': 'Length7', 'param': 'Length7', 'type': 'uint', 'default': 15, 'label': 'Глубина усреднения 7', 'sinput': False}, {'mql': 'Factor7', 'py': 'Factor7', 'param': 'Factor7', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'Length8', 'py': 'Length8', 'param': 'Length8', 'type': 'uint', 'default': 17, 'label': 'Глубина усреднения 8', 'sinput': False}, {'mql': 'Factor8', 'py': 'Factor8', 'param': 'Factor8', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'Length9', 'py': 'Length9', 'param': 'Length9', 'type': 'uint', 'default': 21, 'label': 'Глубина усреднения 9', 'sinput': False}, {'mql': 'Factor9', 'py': 'Factor9', 'param': 'Factor9', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'Length10', 'py': 'Length10', 'param': 'Length10', 'type': 'uint', 'default': 23, 'label': 'Глубина усреднения 10', 'sinput': False}, {'mql': 'Factor10', 'py': 'Factor10', 'param': 'Factor10', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр усреднений', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'uint', 'default': 3, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'SmoothPhase', 'py': 'SmoothPhase', 'param': 'SmoothPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'dK1', 'py': 'dK1', 'param': 'dK1', 'type': 'double', 'default': 1.5, 'label': 'Коэффициент 1 для квадратичного фильтра', 'sinput': False}, {'mql': 'dK2', 'py': 'dK2', 'param': 'dK2', 'type': 'double', 'default': 2.5, 'label': 'Коэффициент 2 для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'Период квадратичного фильтра', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_JJMA)  # Метод усреднения
Length1 = _input('Length1', 3)  # Глубина усреднения 1
Factor1 = _input('Factor1', 0.1)
Length2 = _input('Length2', 5)  # Глубина усреднения 2
Factor2 = _input('Factor2', 0.1)
Length3 = _input('Length3', 7)  # Глубина усреднения 3
Factor3 = _input('Factor3', 0.1)
Length4 = _input('Length4', 9)  # Глубина усреднения 4
Factor4 = _input('Factor4', 0.1)
Length5 = _input('Length5', 11)  # Глубина усреднения 5
Factor5 = _input('Factor5', 0.1)
Length6 = _input('Length6', 13)  # Глубина усреднения 6
Factor6 = _input('Factor6', 0.1)
Length7 = _input('Length7', 15)  # Глубина усреднения 7
Factor7 = _input('Factor7', 0.1)
Length8 = _input('Length8', 17)  # Глубина усреднения 8
Factor8 = _input('Factor8', 0.1)
Length9 = _input('Length9', 21)  # Глубина усреднения 9
Factor9 = _input('Factor9', 0.1)
Length10 = _input('Length10', 23)  # Глубина усреднения 10
Factor10 = _input('Factor10', 0.1)
XPhase = _input('XPhase', 15)  # Параметр усреднений
SmoothMethod = _input('SmoothMethod', MODE_SMA)  # Метод сглаживания
Smooth = _input('Smooth', 3)  # Глубина сглаживания
SmoothPhase = _input('SmoothPhase', 15)  # Параметр сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
dK1 = _input('dK1', 1.5)  # Коэффициент 1 для квадратичного фильтра
dK2 = _input('dK2', 2.5)  # Коэффициент 2 для квадратичного фильтра
std_period = _input('std_period', 9)  # Период квадратичного фильтра
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
BearsBuffer1 = Arr(0, 0.0)
BullsBuffer1 = Arr(0, 0.0)
BearsBuffer2 = Arr(0, 0.0)
BullsBuffer2 = Arr(0, 0.0)
dPriceShift = 0.0
dXZLagMA = Arr(0, 0.0)
min_rates_total = 0
min_rates_ = 0

def OnInit():
    global dPriceShift, min_rates_, min_rates_total
    min_rates = Arr(10, 0, dyn=False)
    min_rates[0] = GetStartBars(XMA_Method, Length1, XPhase)
    min_rates[1] = GetStartBars(XMA_Method, Length2, XPhase)
    min_rates[2] = GetStartBars(XMA_Method, Length3, XPhase)
    min_rates[3] = GetStartBars(XMA_Method, Length4, XPhase)
    min_rates[4] = GetStartBars(XMA_Method, Length5, XPhase)
    min_rates[5] = GetStartBars(XMA_Method, Length6, XPhase)
    min_rates[6] = GetStartBars(XMA_Method, Length7, XPhase)
    min_rates[7] = GetStartBars(XMA_Method, Length8, XPhase)
    min_rates[8] = GetStartBars(XMA_Method, Length9, XPhase)
    min_rates[9] = GetStartBars(XMA_Method, Length10, XPhase)
    min_rates_ = min_rates[ArrayMaximum(min_rates)]
    min_rates_total = min_rates_ + GetStartBars(SmoothMethod, Smooth, SmoothPhase) + _int(std_period)
    dPriceShift = Point() * PriceShift
    ArrayResize(dXZLagMA, std_period)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(2, BearsBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, BullsBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, BearsBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(5, BullsBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ColorZerolagX10MA')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    xma = Arr(10, 0.0, dyn=False)
    zlagxma = 0.0
    xzlagxma = 0.0
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
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        xma[0] = XMA[0].XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Length1, price, bar, False)
        xma[1] = XMA[1].XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Length2, price, bar, False)
        xma[2] = XMA[2].XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Length3, price, bar, False)
        xma[3] = XMA[3].XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Length4, price, bar, False)
        xma[4] = XMA[4].XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Length5, price, bar, False)
        xma[5] = XMA[5].XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Length6, price, bar, False)
        xma[6] = XMA[6].XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Length7, price, bar, False)
        xma[7] = XMA[7].XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Length8, price, bar, False)
        xma[8] = XMA[8].XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Length9, price, bar, False)
        xma[9] = XMA[9].XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Length10, price, bar, False)
        xma[9] = XMA[9].XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Length10, price, bar, False)
        zlagxma = (Factor1 * xma[0]) + (Factor2 * xma[1]) + (Factor3 * xma[2]) + (Factor4 * xma[3]) + (Factor5 * xma[4]) + (Factor6 * xma[5]) + (Factor7 * xma[6]) + (Factor8 * xma[7]) + (Factor9 * xma[8]) + (Factor10 * xma[9])
        IndBuffer[bar] = XMA[10].XMASeries(min_rates_, prev_calculated, rates_total, SmoothMethod, SmoothPhase, Smooth, zlagxma, bar, False)
        IndBuffer[bar] += dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        ColorIndBuffer[bar] = 1.0
        if IndBuffer[bar - 1] < IndBuffer[bar]:
            ColorIndBuffer[bar] = 2.0
        if IndBuffer[bar - 1] > IndBuffer[bar]:
            ColorIndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        for iii in range(0, _int(std_period)):
            dXZLagMA[iii] = IndBuffer[bar - iii] - IndBuffer[bar - iii - 1]
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += dXZLagMA[iii]
        SMAdif = Sum / std_period
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += MathPow(dXZLagMA[iii] - SMAdif, 2)
        StDev = MathSqrt(Sum / std_period)
        dstd = NormalizeDouble(dXZLagMA[0], Digits() + 2)
        Filter1 = NormalizeDouble(dK1 * StDev, Digits() + 2)
        Filter2 = NormalizeDouble(dK2 * StDev, Digits() + 2)
        BEARS1 = EMPTY_VALUE
        BULLS1 = EMPTY_VALUE
        BEARS2 = EMPTY_VALUE
        BULLS2 = EMPTY_VALUE
        xzlagxma = IndBuffer[bar]
        if dstd < (-Filter1) and dstd >= (-Filter2):
            BEARS1 = xzlagxma
        if dstd < (-Filter2):
            BEARS2 = xzlagxma
        if dstd > Filter1 and dstd <= Filter2:
            BULLS1 = xzlagxma
        if dstd > Filter2:
            BULLS2 = xzlagxma
        BullsBuffer1[bar] = BULLS1
        BearsBuffer1[bar] = BEARS1
        BullsBuffer2[bar] = BULLS2
        BearsBuffer2[bar] = BEARS2
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA = Arr(11, 0, dyn=False, factory=CXMA)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorzerolagx10maStdev(_MQL5Indicator):
    name = 'colorzerolagx10ma_stdev'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'Length1': 3,  # Глубина усреднения 1
        'Factor1': 0.1,
        'Length2': 5,  # Глубина усреднения 2
        'Factor2': 0.1,
        'Length3': 7,  # Глубина усреднения 3
        'Factor3': 0.1,
        'Length4': 9,  # Глубина усреднения 4
        'Factor4': 0.1,
        'Length5': 11,  # Глубина усреднения 5
        'Factor5': 0.1,
        'Length6': 13,  # Глубина усреднения 6
        'Factor6': 0.1,
        'Length7': 15,  # Глубина усреднения 7
        'Factor7': 0.1,
        'Length8': 17,  # Глубина усреднения 8
        'Factor8': 0.1,
        'Length9': 21,  # Глубина усреднения 9
        'Factor9': 0.1,
        'Length10': 23,  # Глубина усреднения 10
        'Factor10': 0.1,
        'XPhase': 15,  # Параметр усреднений
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод сглаживания
        'Smooth': 3,  # Глубина сглаживания
        'SmoothPhase': 15,  # Параметр сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'dK1': 1.5,  # Коэффициент 1 для квадратичного фильтра
        'dK2': 2.5,  # Коэффициент 2 для квадратичного фильтра
        'std_period': 9,  # Период квадратичного фильтра
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

