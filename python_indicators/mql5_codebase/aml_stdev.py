"""aml_stdev — converted from MQL5: MQL5 Indicators/AML_StDev/aml_stdev.mq5

Copyright: Adaptive Market Level; Link: andreybs@yandex.ru; Version: 1.11

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Adaptive Market Level', 'link': 'andreybs@yandex.ru', 'version': '1.11', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 8, 2: 5, 3: 5}, 'colors': {1: [8421504, 16760576, 15631086], 2: [255], 3: [65280]}, 'widths': {1: 3, 2: 3, 3: 3}, 'styles': {1: 0}, 'labels': {1: 'AML', 2: 'Dn_Signal', 3: 'Up_Signal'}, 'levels': [], 'description': [], 'name': 'aml_stdev', 'source': 'MQL5 Indicators/AML_StDev/aml_stdev.mq5', 'folder': 'AML_StDev', 'inputs': [{'mql': 'Fractal', 'py': 'Fractal', 'param': 'Fractal', 'type': 'uint', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'Lag', 'py': 'Lag', 'param': 'Lag', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'dK', 'py': 'dK', 'param': 'dK', 'type': 'double', 'default': 3.0, 'label': 'Коэффициент для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'Период квадратичного фильтра', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Fractal = _input('Fractal', 6)
Lag = _input('Lag', 7)
dK = _input('dK', 3.0)  # Коэффициент для квадратичного фильтра
std_period = _input('std_period', 9)  # Период квадратичного фильтра
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
AMLBuffer = Arr(0, 0.0)
ColorAMLBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
BullsBuffer = Arr(0, 0.0)
dAML = Arr(0, 0.0)
dPriceShift = 0.0
LagLagPoint = 0.0
min_rates_1 = 0
min_rates_total = 0
size = 0
Fractal2 = 0
Count = Arr(0, 0)
Smooth = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def Range(period, start, High, Low):
    max_ = High[ArrayMaximum(High, start, period)]
    min_ = Low[ArrayMinimum(Low, start, period)]
    return max_ - min_

def OnInit():
    global Fractal2, LagLagPoint, dPriceShift, min_rates_1, min_rates_total, size
    Fractal2 = _int(2 * Fractal)
    min_rates_1 = _int(MathMax(Fractal + Lag, Fractal2))
    min_rates_total = min_rates_1 + 1 + _int(std_period)
    dPriceShift = Point() * PriceShift
    ArrayResize(dAML, std_period)
    LagLagPoint = Lag * Lag * Point()
    size = Lag + 1
    ArrayResize(Count, size)
    ArrayResize(Smooth, size)
    SetIndexBuffer(0, AMLBuffer, INDICATOR_DATA)
    ArraySetAsSeries(AMLBuffer, True)
    SetIndexBuffer(1, ColorAMLBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorAMLBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(2, BearsBuffer, INDICATOR_DATA)
    ArraySetAsSeries(BearsBuffer, True)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(3, BullsBuffer, INDICATOR_DATA)
    ArraySetAsSeries(BullsBuffer, True)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'AML(', Fractal, ', ', Lag, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    SMAdif = 0.0
    Sum = 0.0
    StDev = 0.0
    dstd = 0.0
    BEARS = 0.0
    BULLS = 0.0
    Filter = 0.0
    limit = 0
    bar = 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_1 - 1
        bar = limit
        price = (high[bar] + low[bar] + (2 * open[bar]) + (2 * close[bar])) / 6
        ArrayInitialize(Smooth, price)
        ArrayInitialize(Count, 0.0)
        AMLBuffer[bar + 1] = price
        ColorAMLBuffer[bar + 1] = 0.0
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        R1 = Range(Fractal, bar, high, low) / Fractal
        R2 = Range(Fractal, bar + Fractal, high, low) / Fractal
        R3 = _fdiv(Range(Fractal2, bar, high, low), Fractal2)
        dim = 0.0
        if (R1 + R2) > 0 and R3 > 0:
            dim = (MathLog(R1 + R2) - MathLog(R3)) * 1.44269504088896
        alpha = MathExp((-Lag) * (dim - 1.0))
        alpha = MathMin(alpha, 1.0)
        alpha = MathMax(alpha, 0.01)
        price = (high[bar] + low[bar] + (2 * open[bar]) + (2 * close[bar])) / 6
        Smooth[Count[0]] = (alpha * price) + ((1.0 - alpha) * Smooth[Count[1]])
        if MathAbs(Smooth[Count[0]] - Smooth[Count[Lag]]) >= LagLagPoint:
            AMLBuffer[bar] = Smooth[Count[0]]
        else:
            AMLBuffer[bar] = AMLBuffer[bar + 1]
        AMLBuffer[bar] += PriceShift
        if bar:
            Recount_ArrayZeroPos(Count, size)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorAMLBuffer[bar] = 0.0
        if AMLBuffer[bar + 1] < AMLBuffer[bar]:
            ColorAMLBuffer[bar] = 1.0
        if AMLBuffer[bar + 1] > AMLBuffer[bar]:
            ColorAMLBuffer[bar] = 2.0
        if AMLBuffer[bar + 1] == AMLBuffer[bar]:
            ColorAMLBuffer[bar] = ColorAMLBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        for iii in range(0, _int(std_period)):
            dAML[iii] = AMLBuffer[bar + iii] - AMLBuffer[bar + iii + 1]
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += dAML[iii]
        SMAdif = Sum / std_period
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += MathPow(dAML[iii] - SMAdif, 2)
        StDev = MathSqrt(Sum / std_period)
        dstd = NormalizeDouble(dAML[0], Digits() + 2)
        Filter = NormalizeDouble(dK * StDev, Digits() + 2)
        BEARS = 0.0
        BULLS = 0.0
        if dstd < (-Filter):
            BEARS = AMLBuffer[bar]
        if dstd > Filter:
            BULLS = AMLBuffer[bar]
        BullsBuffer[bar] = BULLS
        BearsBuffer[bar] = BEARS
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AmlStdev(_MQL5Indicator):
    name = 'aml_stdev'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fractal': 6,
        'Lag': 7,
        'dK': 3.0,  # Коэффициент для квадратичного фильтра
        'std_period': 9,  # Период квадратичного фильтра
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

