"""dots — converted from MQL5: MQL5 Indicators/Dots_HTF/dots.mq5

Copyright: Copyright © 2011, EarnForex; Link: http://www.earnforex.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, EarnForex', 'link': 'http://www.earnforex.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [16711680, 255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Dots'}, 'levels': [], 'description': [], 'name': 'dots', 'source': 'MQL5 Indicators/Dots_HTF/dots.mq5', 'folder': 'Dots_HTF', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 10, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'uint', 'default': 0, 'label': 'Параметр, позволяющий фильтровать всплески цен без добавления задержек в отображение', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
Length = _input('Length', 10)  # Глубина сглаживания
Filter = _input('Filter', 0)  # Параметр, позволяющий фильтровать всплески цен без добавления задержек в отображение
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
dPriceShift = 0.0
Coeff = 0.0
Phase = 0.0
Res1 = 0.0
Res2 = 0.0
dFilter = 0.0
Len = 0
Cycle = 0
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def OnInit():
    global Coeff, Cycle, Len, Phase, Res1, Res2, dFilter, dPriceShift, min_rates_total
    Coeff = 3 * 3.1415926535
    Phase = Length - 1
    Cycle = 4
    Len = _int((Length * Cycle) + Phase)
    Res1 = _fdiv(1.0, Phase - 1)
    Res2 = _fdiv((2.0 * Cycle) - 1.0, (Cycle * Length) - 1.0)
    min_rates_total = Len + 1
    dPriceShift = Point() * PriceShift
    dFilter = Point() * Filter
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    shortname = Box("")
    StringConcatenate(shortname, 'Dots(', Length, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    alfa = 0.0
    beta = 0.0
    t = 0.0
    Sum = 0.0
    Weight = 0.0
    g = 0.0
    price = 0.0
    MA = 0.0
    MA_prev = 0.0
    first = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
        bar = first - 1
        IndBuffer[bar] = close[bar] + dPriceShift
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Weight = 0.0
        Sum = 0.0
        t = 0.0
        iii = 0
        while iii < Len:
            g = _fdiv(1.0, (Coeff * t) + 1)
            if t <= 0.5:
                g = 1.0
            beta = MathCos(3.1415926535 * t)
            alfa = g * beta
            price = PriceSeries(IPC, bar - iii, open, low, high, close)
            Sum += alfa * price
            Weight += alfa
            if t < 1:
                t += Res1
            elif t < (Len - 1):
                t += Res2
            iii += 1
        MA_prev = IndBuffer[bar - 1] - dPriceShift
        if Weight:
            MA = _fdiv(Sum, MathAbs(Weight))
        else:
            MA = MA_prev
        if Filter and MathAbs(MA - MA_prev) < dFilter:
            MA = MA_prev
        if (MA - MA_prev) > dFilter:
            clr = 0
        elif (MA_prev - MA) > dFilter:
            clr = 1
        IndBuffer[bar] = MA + dPriceShift
        ColorIndBuffer[bar] = clr
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


class Dots(_MQL5Indicator):
    name = 'dots'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # Глубина сглаживания
        'Filter': 0,  # Параметр, позволяющий фильтровать всплески цен без добавления задержек в отображение
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

