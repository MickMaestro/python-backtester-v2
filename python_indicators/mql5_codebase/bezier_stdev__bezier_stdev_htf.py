"""Bezier_StDev — converted from MQL5: MQL5 Indicators/Bezier_StDev_HTF/Bezier_StDev.mq5

Copyright: Copyright © 2007, Lizhniyk E; Link: Lizhniyk E; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Lizhniyk E', 'link': 'Lizhniyk E', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 8, 2: 5, 3: 5}, 'colors': {1: [8421504, 16748574, 1993170], 2: [16711935], 3: [65280]}, 'widths': {1: 3, 2: 3, 3: 3}, 'styles': {1: 0}, 'labels': {1: 'Bezier', 2: 'Dn_Signal', 3: 'Up_Signal'}, 'levels': [], 'description': [], 'name': 'Bezier_StDev', 'source': 'MQL5 Indicators/Bezier_StDev_HTF/Bezier_StDev.mq5', 'folder': 'Bezier_StDev_HTF', 'inputs': [{'mql': 'BPeriod', 'py': 'BPeriod', 'param': 'BPeriod', 'type': 'uint', 'default': 8, 'label': 'период усреднения', 'sinput': False}, {'mql': 'T', 'py': 'T_v', 'param': 'T_v', 'type': 'double', 'default': 0.5, 'label': 'коэффициент чувствительности (от 0 до 1)', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 7, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'dK', 'py': 'dK', 'param': 'dK', 'type': 'double', 'default': 2.0, 'label': 'коэффициент для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'период квадратичного фильтра', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum Signal_mode
Trend = 0
Kalman = 1
_enum('Signal_mode', {0: 'Trend', 1: 'Kalman'})

# ---- inputs and global variables
BPeriod = _input('BPeriod', 8)  # период усреднения
T_v = _input('T_v', 0.5)  # коэффициент чувствительности (от 0 до 1)
IPC = _input('IPC', PRICE_WEIGHTED_)  # ценовая константа
dK = _input('dK', 2.0)  # коэффициент для квадратичного фильтра
std_period = _input('std_period', 9)  # период квадратичного фильтра
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
BezierBuffer = Arr(0, 0.0)
ColorBezierBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
BullsBuffer = Arr(0, 0.0)
dPriceShift = 0.0
t = 0.0
dBezier = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global dPriceShift, min_rates_1, min_rates_total, t
    min_rates_1 = _int(BPeriod)
    min_rates_total = min_rates_1 + 1 + _int(std_period)
    dPriceShift = Point() * PriceShift
    t = MathMin(MathMax(T_v, 0), 1)
    ArrayResize(dBezier, std_period)
    SetIndexBuffer(0, BezierBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorBezierBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(2, BearsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(3, BullsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'Bezier(', BPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    SMAdif = 0.0
    Sum = 0.0
    StDev = 0.0
    dstd = 0.0
    BEARS = 0.0
    BULLS = 0.0
    Filter = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1 + 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        r = 0.0
        for iii in range(_int(BPeriod), 0 - 1, -1):
            r += PriceSeries(IPC, bar - iii, open, low, high, close) * _idiv(factorial(BPeriod), factorial(iii) * factorial(BPeriod - iii)) * MathPow(t, iii) * MathPow(1 - t, BPeriod - iii)
        BezierBuffer[bar] = r + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        ColorBezierBuffer[bar] = 0.0
        if BezierBuffer[bar - 1] < BezierBuffer[bar]:
            ColorBezierBuffer[bar] = 1.0
        if BezierBuffer[bar - 1] > BezierBuffer[bar]:
            ColorBezierBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
        for iii in range(0, _int(std_period)):
            dBezier[iii] = BezierBuffer[bar - iii - 0] - BezierBuffer[bar - iii - 1]
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += dBezier[iii]
        SMAdif = Sum / std_period
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += MathPow(dBezier[iii] - SMAdif, 2)
        StDev = MathSqrt(Sum / std_period)
        dstd = NormalizeDouble(dBezier[0], Digits() + 2)
        Filter = NormalizeDouble(dK * StDev, Digits() + 2)
        BEARS = 0.0
        BULLS = 0.0
        if dstd < (-Filter):
            BEARS = BezierBuffer[bar]
        if dstd > Filter:
            BULLS = BezierBuffer[bar]
        BullsBuffer[bar] = BULLS
        BearsBuffer[bar] = BEARS
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def factorial(value):
    res = 1
    for j in range(2, value + 1):
        res *= j
    return res

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
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BezierStDev(_MQL5Indicator):
    name = 'Bezier_StDev'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BPeriod': 8,  # период усреднения
        'T_v': 0.5,  # коэффициент чувствительности (от 0 до 1)
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=7),  # ценовая константа
        'dK': 2.0,  # коэффициент для квадратичного фильтра
        'std_period': 9,  # период квадратичного фильтра
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
    }

