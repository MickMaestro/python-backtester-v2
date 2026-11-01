"""gaus_ma_stdev — converted from MQL5: MQL5 Indicators/Gaus_MA_StDev/gaus_ma_stdev.mq5

Усреднение (Сглаживание кривой цен) цен при помощи модифицированного алгоритма
линейно-взвешенного скользящего среднего, где коэффициенты сглаживания расчитываются
при помощи радиально-базисной функци (функция Гауса).
Дополнительная индикациея силы тренда цветными точками на основе алгоритма стандартного отклонения
Copyright: Copyright © 2009, Gregory A. Kakhiani; Link: gkakhiani@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Gregory A. Kakhiani', 'link': 'gkakhiani@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 8, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [8421504, 8421376, 3937500], 2: [255], 3: [16776960], 4: [255], 5: [16776960]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 4, 5: 4}, 'styles': {1: 0}, 'labels': {1: 'GaussAverage', 2: 'Dn_Signal 1', 3: 'Up_Signal 1', 4: 'Dn_Signal 2', 5: 'Up_Signal 2'}, 'levels': [], 'description': ['Усреднение (Сглаживание кривой цен) цен при помощи модифицированного алгоритма', 'линейно-взвешенного скользящего среднего, где коэффициенты сглаживания расчитываются', 'при помощи радиально-базисной функци (функция Гауса).', 'Дополнительная индикациея силы тренда цветными точками на основе алгоритма стандартного отклонения'], 'name': 'gaus_ma_stdev', 'source': 'MQL5 Indicators/Gaus_MA_StDev/gaus_ma_stdev.mq5', 'folder': 'Gaus_MA_StDev', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 10, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'N_', 'py': 'N_', 'param': 'N_', 'type': 'double', 'default': 2.0, 'label': 'Степень экспоненты', 'sinput': False}, {'mql': 'A', 'py': 'A', 'param': 'A', 'type': 'double', 'default': -0.001, 'label': 'Коэфициент степени е', 'sinput': False}, {'mql': 'Vol', 'py': 'Vol', 'param': 'Vol', 'type': 'bool', 'default': False, 'label': 'Умножить на объем', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Объём', 'sinput': False}, {'mql': 'Applied_Price', 'py': 'Applied_Price', 'param': 'Applied_Price', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'dK1', 'py': 'dK1', 'param': 'dK1', 'type': 'double', 'default': 1.5, 'label': 'Коэффициент 1 для квадратичного фильтра', 'sinput': False}, {'mql': 'dK2', 'py': 'dK2', 'param': 'dK2', 'type': 'double', 'default': 2.5, 'label': 'Коэффициент 2 для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'Период квадратичного фильтра', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
period = _input('period', 10)  # Период усреднения
N_ = _input('N_', 2.0)  # Степень экспоненты
A = _input('A', -0.001)  # Коэфициент степени е
Vol = _input('Vol', False)  # Умножить на объем
VolumeType = _input('VolumeType', VOLUME_TICK)  # Объём
Applied_Price = _input('Applied_Price', PRICE_CLOSE_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
dK1 = _input('dK1', 1.5)  # Коэффициент 1 для квадратичного фильтра
dK2 = _input('dK2', 2.5)  # Коэффициент 2 для квадратичного фильтра
std_period = _input('std_period', 9)  # Период квадратичного фильтра
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
BearsBuffer1 = Arr(0, 0.0)
BullsBuffer1 = Arr(0, 0.0)
BearsBuffer2 = Arr(0, 0.0)
BullsBuffer2 = Arr(0, 0.0)
N = 0.0
dPriceShift = 0.0
dGausMA = Arr(0, 0.0)
Coefs = Arr(0, 0.0)  # массив для хранения коэффициентов
min_rates_1 = 0
min_rates_total = 0
AvPeriod = 0

def OnInit():
    global AvPeriod, N, dPriceShift, min_rates_1, min_rates_total
    if dK1 >= dK2:
        Print(' Некрректные значения входных параметров для коэффициентов 1 и 2 для квадратичного фильтра!')
        return INIT_FAILED
    AvPeriod = _int(period)
    min_rates_1 = AvPeriod
    min_rates_total = min_rates_1 + 1 + _int(std_period)
    ArrayResize(Coefs, AvPeriod)
    N = N_
    if MathAbs(N) > 5:
        N = 5.0
    ArrayResize(dGausMA, std_period)
    for iii in range(0, AvPeriod):
        Coefs[iii] = MathExp(A * MathPow(iii, N))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Gaus_MA_StDev')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
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
    dPriceShift = Point() * PriceShift
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    sum_ = 0.0
    W = 0.0
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
    GausMA = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        sum_ = 0.0
        W = 0.0
        kkk = 0
        while kkk < AvPeriod:
            if Vol:
                if VolumeType == VOLUME_TICK:
                    sum_ += PriceSeries(Applied_Price, bar - kkk, open, low, high, close) * tick_volume[bar] * Coefs[kkk]
                    W += Coefs[kkk] * tick_volume[bar]
                else:
                    sum_ += PriceSeries(Applied_Price, bar - kkk, open, low, high, close) * volume[bar] * Coefs[kkk]
                    W += Coefs[kkk] * volume[bar]
            else:
                sum_ += PriceSeries(Applied_Price, bar - kkk, open, low, high, close) * Coefs[kkk]
                W += Coefs[kkk]
            kkk += 1
        ExtLineBuffer[bar] = _fdiv(sum_, W) + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        ColorExtLineBuffer[bar] = 0.0
        if ExtLineBuffer[bar - 1] < ExtLineBuffer[bar]:
            ColorExtLineBuffer[bar] = 1.0
        if ExtLineBuffer[bar - 1] > ExtLineBuffer[bar]:
            ColorExtLineBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        for iii in range(0, _int(std_period)):
            dGausMA[iii] = ExtLineBuffer[bar - iii] - ExtLineBuffer[bar - iii - 1]
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += dGausMA[iii]
        SMAdif = Sum / std_period
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += MathPow(dGausMA[iii] - SMAdif, 2)
        StDev = MathSqrt(Sum / std_period)
        dstd = NormalizeDouble(dGausMA[0], Digits() + 2)
        Filter1 = NormalizeDouble(dK1 * StDev, Digits() + 2)
        Filter2 = NormalizeDouble(dK2 * StDev, Digits() + 2)
        BEARS1 = EMPTY_VALUE
        BULLS1 = EMPTY_VALUE
        BEARS2 = EMPTY_VALUE
        BULLS2 = EMPTY_VALUE
        GausMA = ExtLineBuffer[bar]
        if dstd < (-Filter1) and dstd >= (-Filter2):
            BEARS1 = GausMA
        if dstd < (-Filter2):
            BEARS2 = GausMA
        if dstd > Filter1 and dstd <= Filter2:
            BULLS1 = GausMA
        if dstd > Filter2:
            BULLS2 = GausMA
        BullsBuffer1[bar] = BULLS1
        BearsBuffer1[bar] = BEARS1
        BullsBuffer2[bar] = BULLS2
        BearsBuffer2[bar] = BEARS2
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GausMaStdev(_MQL5Indicator):
    name = 'gaus_ma_stdev'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 10,  # Период усреднения
        'N_': 2.0,  # Степень экспоненты
        'A': -0.001,  # Коэфициент степени е
        'Vol': False,  # Умножить на объем
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Объём
        'Applied_Price': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'dK1': 1.5,  # Коэффициент 1 для квадратичного фильтра
        'dK2': 2.5,  # Коэффициент 2 для квадратичного фильтра
        'std_period': 9,  # Период квадратичного фильтра
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

