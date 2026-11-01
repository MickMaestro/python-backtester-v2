"""FDI — converted from MQL5: MQL5 Indicators/FDI_HTF/FDI.mq5

Copyright: Copyright © 2008, iliko [arcsin5@netscape.net]; Link: http://fractalfinance.blogspot.com/; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, iliko [arcsin5@netscape.net]', 'link': 'http://fractalfinance.blogspot.com/', 'version': '1.02', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [65535, 255, 14381203]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'FDI'}, 'levels': [], 'description': [], 'name': 'FDI', 'source': 'MQL5 Indicators/FDI_HTF/FDI.mq5', 'folder': 'FDI_HTF', 'inputs': [{'mql': 'e_period', 'py': 'e_period', 'param': 'e_period', 'type': 'uint', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'normal_speed', 'py': 'normal_speed', 'param': 'normal_speed', 'type': 'uint', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'e_random_line', 'py': 'e_random_line', 'param': 'e_random_line', 'type': 'double', 'default': 1.5, 'label': 'Уровень срабатывания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
e_period = _input('e_period', 30)
normal_speed = _input('normal_speed', 20)
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
e_random_line = _input('e_random_line', 1.5)  # Уровень срабатывания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
g_period_minus_1 = 0
Count = Arr(0, 0)
Data = Arr(0, 0.0)
LOG_2 = 0.0

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
    global LOG_2, g_period_minus_1, min_rates_total
    g_period_minus_1 = _int(e_period) - 1
    min_rates_total = _int(e_period) + g_period_minus_1
    LOG_2 = MathLog(2.0)
    ArrayResize(Count, e_period)
    ArrayResize(Data, e_period)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(IndBuffer, True)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'FDI(', e_period, ', ', normal_speed, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, e_random_line)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
        ArrayInitialize(Count, 0)
        ArrayInitialize(Data, 0.0)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Data[Count[0]] = PriceSeries(IPC, bar, open, low, high, close)
        priceMax = 0.0
        for iii in range(0, _int(e_period)):
            if Data[Count[iii]] > priceMax:
                priceMax = Data[Count[iii]]
        priceMin = 99999999.0
        for iii in range(0, _int(e_period)):
            if Data[Count[iii]] < priceMin:
                priceMin = Data[Count[iii]]
        range_ = priceMax - priceMin
        length = 0.0
        fdi = 0.0
        priorDiff = 0.0
        for kkk in range(0, g_period_minus_1 + 1):
            if range_ > 0.0:
                diff = _fdiv(Data[Count[kkk]] - priceMin, range_)
                if kkk > 0:
                    length += MathSqrt(MathPow(diff - priorDiff, 2.0) + _fdiv(1.0, MathPow(e_period, 2.0)))
                priorDiff = diff
        if length > 0.0:
            fdi = 1.0 + _fdiv(MathLog(length) + LOG_2, MathLog(2 * g_period_minus_1))
        else:
            fdi = 0.0
        IndBuffer[bar] = fdi
        if bar:
            Recount_ArrayZeroPos(Count, e_period)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorIndBuffer[bar] = 1.0
        if IndBuffer[bar] > e_random_line:
            ColorIndBuffer[bar] = 0.0
        if IndBuffer[bar] < e_random_line:
            ColorIndBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
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

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FDI(_MQL5Indicator):
    name = 'FDI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'e_period': 30,
        'normal_speed': 20,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'e_random_line': 1.5,  # Уровень срабатывания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

