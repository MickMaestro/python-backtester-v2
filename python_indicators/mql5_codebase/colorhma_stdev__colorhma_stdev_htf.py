"""colorhma_stdev — converted from MQL5: MQL5 Indicators/ColorHMA_StDev_HTF/colorhma_stdev.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 8, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [8421504, 14381203, 255], 2: [16711935], 3: [16711680], 4: [16711935], 5: [16711680]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 4, 5: 4}, 'styles': {1: 0}, 'labels': {2: 'Dn_Signal 1', 3: 'Up_Signal 1', 4: 'Dn_Signal 2', 5: 'Up_Signal 2'}, 'levels': [], 'description': [], 'name': 'colorhma_stdev', 'source': 'MQL5 Indicators/ColorHMA_StDev_HTF/colorhma_stdev.mq5', 'folder': 'ColorHMA_StDev_HTF', 'inputs': [{'mql': 'HMA_Period', 'py': 'HMA_Period', 'param': 'HMA_Period', 'type': 'uint', 'default': 13, 'label': 'Период мувинга', 'sinput': False}, {'mql': 'dK1', 'py': 'dK1', 'param': 'dK1', 'type': 'double', 'default': 1.5, 'label': 'Коэффициент 1 для квадратичного фильтра', 'sinput': False}, {'mql': 'dK2', 'py': 'dK2', 'param': 'dK2', 'type': 'double', 'default': 2.5, 'label': 'Коэффициент 2 для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'Период квадратичного фильтра', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг Фатла по вертикали в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг мувинга по горизонтали в барах', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
HMA_Period = _input('HMA_Period', 13)  # Период мувинга
dK1 = _input('dK1', 1.5)  # Коэффициент 1 для квадратичного фильтра
dK2 = _input('dK2', 2.5)  # Коэффициент 2 для квадратичного фильтра
std_period = _input('std_period', 9)  # Период квадратичного фильтра
PriceShift = _input('PriceShift', 0)  # Сдвиг Фатла по вертикали в пунктах
Shift = _input('Shift', 0)  # Сдвиг мувинга по горизонтали в барах
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
BearsBuffer1 = Arr(0, 0.0)
BullsBuffer1 = Arr(0, 0.0)
BearsBuffer2 = Arr(0, 0.0)
BullsBuffer2 = Arr(0, 0.0)
Hma2_Period = 0
Sqrt_Period = 0
min_rates_total = 0
min_rates = 0
dPriceShift = 0.0
dHMA = Arr(0, 0.0)

def OnInit():
    global Hma2_Period, Sqrt_Period, dPriceShift, min_rates, min_rates_total
    Hma2_Period = _int(MathFloor(_idiv(HMA_Period, 2)))
    Sqrt_Period = _int(MathFloor(MathSqrt(HMA_Period)))
    dPriceShift = Point() * PriceShift
    min_rates = _int(HMA_Period) + Sqrt_Period
    min_rates_total = min_rates + _int(std_period)
    ArrayResize(dHMA, std_period)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
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
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    short_name = 'ColorHMA_StDev'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + '(' + _str(HMA_Period) + ')')

def OnCalculate(rates_total, prev_calculated, begin, price):
    begin0 = min_rates_total + begin
    if rates_total < begin0:
        return 0
    first = 0
    bar = 0
    begin1 = 0
    lwma1 = 0.0
    lwma2 = 0.0
    dma = 0.0
    hma = 0.0
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
    begin1 = _int(HMA_Period) + begin
    if prev_calculated == 0:
        first = begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin0 + 1)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, begin0 + 1)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, begin0 + 1)
        PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, begin0 + 1)
        PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, begin0 + 1)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        lwma1 = _s_OnCalculate_MA1.LWMASeries(begin, prev_calculated, rates_total, Hma2_Period, price[bar], bar, False)
        lwma2 = _s_OnCalculate_MA2.LWMASeries(begin, prev_calculated, rates_total, HMA_Period, price[bar], bar, False)
        dma = (2 * lwma1) - lwma2
        ExtLineBuffer[bar] = _s_OnCalculate_MA3.LWMASeries(begin1, prev_calculated, rates_total, Sqrt_Period, dma, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = begin0
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
        first = begin0
    bar = first
    for bar in range(bar, rates_total):
        for iii in range(0, _int(std_period)):
            dHMA[iii] = ExtLineBuffer[bar - iii] - ExtLineBuffer[bar - iii - 1]
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += dHMA[iii]
        SMAdif = Sum / std_period
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += MathPow(dHMA[iii] - SMAdif, 2)
        StDev = MathSqrt(Sum / std_period)
        dig = Digits() + 2
        dstd = NormalizeDouble(dHMA[0], dig)
        Filter1 = NormalizeDouble(dK1 * StDev, dig)
        Filter2 = NormalizeDouble(dK2 * StDev, dig)
        BEARS1 = EMPTY_VALUE
        BULLS1 = EMPTY_VALUE
        BEARS2 = EMPTY_VALUE
        BULLS2 = EMPTY_VALUE
        hma = ExtLineBuffer[bar]
        if dstd < (-Filter1) and dstd >= (-Filter2):
            BEARS1 = hma
        if dstd < (-Filter2):
            BEARS2 = hma
        if dstd > Filter1 and dstd <= Filter2:
            BULLS1 = hma
        if dstd > Filter2:
            BULLS2 = hma
        BullsBuffer1[bar] = BULLS1
        BearsBuffer1[bar] = BEARS1
        BullsBuffer2[bar] = BULLS2
        BearsBuffer2[bar] = BEARS2
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_MA1 = CMoving_Average()
_s_OnCalculate_MA2 = CMoving_Average()
_s_OnCalculate_MA3 = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorhmaStdev(_MQL5Indicator):
    name = 'colorhma_stdev'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HMA_Period': 13,  # Период мувинга
        'dK1': 1.5,  # Коэффициент 1 для квадратичного фильтра
        'dK2': 2.5,  # Коэффициент 2 для квадратичного фильтра
        'std_period': 9,  # Период квадратичного фильтра
        'PriceShift': 0,  # Сдвиг Фатла по вертикали в пунктах
        'Shift': 0,  # Сдвиг мувинга по горизонтали в барах
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

