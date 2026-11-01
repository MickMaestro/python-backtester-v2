"""nonlagma_v5 — converted from MQL5: MQL5 Indicators/NonLagMA_v5/nonlagma_v5.mq5

Copyright: Copyright © 2006, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 32768, 16711935]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'NonLagMA_v5'}, 'levels': [], 'description': [], 'name': 'nonlagma_v5', 'source': 'MQL5 Indicators/NonLagMA_v5/nonlagma_v5.mq5', 'folder': 'NonLagMA_v5', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 13, 'label': 'Период', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': 'Тип усреднения', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': 'Цена', 'sinput': False}, {'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'uint', 'default': 0, 'label': 'Static filter in points', 'sinput': False}, {'mql': 'ColorBarBack', 'py': 'ColorBarBack', 'param': 'ColorBarBack', 'type': 'uint', 'default': 1, 'label': 'Bar back for color mode', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 0.0, 'label': 'Up/down deviation', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 13)  # Период
MAType = _input('MAType', MODE_EMA)  # Тип усреднения
MAPrice = _input('MAPrice', PRICE_CLOSE)  # Цена
Filter = _input('Filter', 0)  # Static filter in points
ColorBarBack = _input('ColorBarBack', 1)  # Bar back for color mode
Deviation = _input('Deviation', 0.0)  # Up/down deviation
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
alfa = Arr(0, 0.0)
Phase = 0
Len = 0
Cycle = 0
size = 0
Coeff = 0.0
beta = 0.0
t = 0.0
Sum = 0.0
Weight = 0.0
g = 0.0
pi = 0.0
dFilter = 0.0
MA_Handle = 0
dPriceShift = 0.0
min_rates_total = 0
Count = Arr(0, 0)
Trend = Arr(0, 0.0)

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

def OnInit():
    global Coeff, Cycle, Len, MA_Handle, Phase, Weight, beta, dFilter, g, min_rates_total, pi, size, t
    MA_Handle = iMA(None, 0, MAPeriod, 0, MAType, MAPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    dFilter = Filter * Point()
    Cycle = 4
    pi = 3.1415926535
    Coeff = 3 * pi
    Phase = MAPeriod - 1
    Len = (MAPeriod * Cycle) + Phase
    if ArrayResize(alfa, Len) < Len:
        Print('Не удалось распределить память под массив alfa[]')
        return INIT_FAILED
    Weight = 0.0
    for iii in range(0, Len):
        if iii <= (Phase - 1):
            t = _fdiv(1.0 * iii, Phase - 1)
        else:
            t = 1.0 + _fdiv((iii - Phase + 1) * ((2.0 * Cycle) - 1.0), (Cycle * MAPeriod) - 1.0)
        beta = MathCos(pi * t)
        g = _fdiv(1.0, (Coeff * t) + 1)
        if t <= 0.5:
            g = 1.0
        alfa[iii] = g * beta
        Weight += alfa[iii]
    min_rates_total = _int(MAPeriod + ColorBarBack + Len)
    size = _int(ColorBarBack + 1)
    if ArrayResize(Count, size) < size:
        Print('Не удалось распределить память под массив Count[]')
        return INIT_FAILED
    if ArrayResize(Trend, size) < size:
        Print('Не удалось распределить память под массив Trend[]')
        return INIT_FAILED
    ArrayInitialize(Count, 0)
    ArrayInitialize(Trend, 0.0)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'NonLagMA_v5(', MAPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Sum
    if BarsCalculated(MA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MA = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + Len + 1
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    ArraySetAsSeries(MA, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Sum = 0.0
        for kkk in range(0, Len):
            Sum += alfa[kkk] * MA[bar + kkk]
        if Weight:
            IndBuffer[bar] = _fdiv((1.0 + (Deviation / 100)) * Sum, Weight)
        if Filter > 0:
            if MathAbs(IndBuffer[bar] - IndBuffer[bar + 1]) < dFilter:
                IndBuffer[bar] = IndBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorIndBuffer[bar] = 0.0
        Trend[Count[0]] = Trend[Count[1]]
        if (IndBuffer[bar] - IndBuffer[bar + 1]) > dFilter:
            Trend[Count[0]] = 1.0
        if (IndBuffer[bar + 1] - IndBuffer[bar]) > dFilter:
            Trend[Count[0]] = -1.0
        if Trend[Count[0]] > 0:
            ColorIndBuffer[bar] = 1.0
            if Trend[Count[ColorBarBack]] < 0:
                ColorIndBuffer[bar + ColorBarBack] = 1.0
        if Trend[Count[0]] < 0:
            ColorIndBuffer[bar] = 2.0
            if Trend[Count[ColorBarBack]] > 0:
                ColorIndBuffer[bar + ColorBarBack] = 2.0
        if bar:
            Recount_ArrayZeroPos(Count, size)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NonlagmaV5(_MQL5Indicator):
    name = 'nonlagma_v5'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 13,  # Период
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Тип усреднения
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена
        'Filter': 0,  # Static filter in points
        'ColorBarBack': 1,  # Bar back for color mode
        'Deviation': 0.0,  # Up/down deviation
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

