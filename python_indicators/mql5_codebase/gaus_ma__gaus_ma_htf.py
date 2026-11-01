"""gaus_ma — converted from MQL5: MQL5 Indicators/Gaus_MA_HTF/gaus_ma.mq5

Усреднение (Сглаживание кривой цен) цен при помощи модифицированного алгоритма
линейно-взвешенного скользящего среднего, где коэффициенты сглаживания расcчитываются
при помощи радиально-базисной функци (функция Гаусса)
Copyright: Copyright © 2009, Gregory A. Kakhiani; Link: gkakhiani@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Gregory A. Kakhiani', 'link': 'gkakhiani@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 8421376, 3937500]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'GaussAverage'}, 'levels': [], 'description': ['Усреднение (Сглаживание кривой цен) цен при помощи модифицированного алгоритма', 'линейно-взвешенного скользящего среднего, где коэффициенты сглаживания расcчитываются', 'при помощи радиально-базисной функци (функция Гаусса)'], 'name': 'gaus_ma', 'source': 'MQL5 Indicators/Gaus_MA_HTF/gaus_ma.mq5', 'folder': 'Gaus_MA_HTF', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 10, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'N_', 'py': 'N_', 'param': 'N_', 'type': 'double', 'default': 2.0, 'label': 'Степень экспоненты', 'sinput': False}, {'mql': 'A', 'py': 'A', 'param': 'A', 'type': 'double', 'default': -0.001, 'label': 'Коэффициент степени е', 'sinput': False}, {'mql': 'Vol', 'py': 'Vol', 'param': 'Vol', 'type': 'bool', 'default': False, 'label': 'Умножить на объем', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Объем', 'sinput': False}, {'mql': 'Applied_Price', 'py': 'Applied_Price', 'param': 'Applied_Price', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
period = _input('period', 10)  # Период усреднения
N_ = _input('N_', 2.0)  # Степень экспоненты
A = _input('A', -0.001)  # Коэффициент степени е
Vol = _input('Vol', False)  # Умножить на объем
VolumeType = _input('VolumeType', VOLUME_TICK)  # Объем
Applied_Price = _input('Applied_Price', PRICE_CLOSE_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
N = 0.0
dPriceShift = 0.0
Coefs = Arr(0, 0.0)  # массив для хранения коэффициентов
min_rates_total = 0
AvPeriod = 0

def OnInit():
    global AvPeriod, N, dPriceShift, min_rates_total
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    AvPeriod = _int(period)
    min_rates_total = AvPeriod + 1
    ArrayResize(Coefs, AvPeriod)
    N = N_
    if MathAbs(N) > 5:
        N = 5.0
    for iii in range(0, AvPeriod):
        Coefs[iii] = MathExp(A * MathPow(iii, N))
    IndicatorSetString(INDICATOR_SHORTNAME, 'GaussAverage')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    dPriceShift = Point() * PriceShift

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    sum_ = 0.0
    W = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
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


class GausMa(_MQL5Indicator):
    name = 'gaus_ma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 10,  # Период усреднения
        'N_': 2.0,  # Степень экспоненты
        'A': -0.001,  # Коэффициент степени е
        'Vol': False,  # Умножить на объем
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Объем
        'Applied_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

