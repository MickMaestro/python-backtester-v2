"""adaptivervisign — converted from MQL5: MQL5 Indicators/AdaptiveRVISign/adaptivervisign.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [9639167], 2: [16748574]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'AdaptiveRVI Sell', 2: 'AdaptiveRVI Buy'}, 'levels': [], 'description': [], 'name': 'adaptivervisign', 'source': 'MQL5 Indicators/AdaptiveRVISign/adaptivervisign.mq5', 'folder': 'AdaptiveRVISign', 'inputs': [{'mql': 'Alpha', 'py': 'Alpha', 'param': 'Alpha', 'type': 'double', 'default': 0.07, 'label': 'Коэффициент усреднения индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Alpha = _input('Alpha', 0.07)  # Коэффициент усреднения индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
CP_Handle = 0
ATR_Handle = 0
min_rates_total = 0
Count = Arr(0, 0)
Value1 = Arr(0, 0.0)
Value2 = Arr(0, 0.0)

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

def Get_dPrice(Price1, Price2, bar):
    return Price1[bar] - Price2[bar]

def OnInit():
    global ATR_Handle, CP_Handle, min_rates_total
    ATR_Period = 10
    min_rates_total = MathMax(4, ATR_Period)
    CP_Handle = iCustom(None, 0, 'CyclePeriod', Alpha)
    if CP_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора CyclePeriod')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    ArrayResize(Count, 100)
    ArrayResize(Value1, 100)
    ArrayResize(Value2, 100)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Value1, 0.0)
    ArrayInitialize(Value2, 0.0)
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 172)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 172)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Adaptive RVI Sign(', DoubleToString(Alpha, 4), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ARVI1, _s_OnCalculate_Trigger1
    if (BarsCalculated(CP_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    Length = 0
    Num = 0.0
    Denom = 0.0
    rvi = 0.0
    ARVI0 = 0.0
    Trigger0 = 0.0
    period = Arr(4, 0.0, dyn=False)
    ATR = Arr(1, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 3
        _s_OnCalculate_ARVI1 = 0.0
        _s_OnCalculate_Trigger1 = 0.0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if CopyBuffer(CP_Handle, 0, rates_total - 1 - bar, 4, period) <= 0:
            return 0
        Length = _int(MathFloor(((4.0 * period[3]) + (3.0 * period[2]) + (2.0 * period[1]) + period[0]) / 20.0))
        if bar < Length:
            Length = bar
        Value1[Count[0]] = (Get_dPrice(close, open, bar) + (2.0 * Get_dPrice(close, open, bar - 1)) + (2.0 * Get_dPrice(close, open, bar - 2)) + Get_dPrice(close, open, bar - 3)) / 6.0
        Value2[Count[0]] = (Get_dPrice(high, low, bar) + (2.0 * Get_dPrice(high, low, bar - 1)) + (2.0 * Get_dPrice(high, low, bar - 2)) + Get_dPrice(high, low, bar - 3)) / 6.0
        Num = 0.0
        Denom = 0.0
        for iii in range(0, Length):
            Num += Value1[Count[iii]]
            Denom += Value2[Count[iii]]
        if Denom != 0.0:
            rvi = _fdiv(Num, Denom)
        else:
            rvi = EMPTY_VALUE
        ARVI0 = rvi
        Trigger0 = _s_OnCalculate_ARVI1
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_ARVI1 < _s_OnCalculate_Trigger1 and ARVI0 > Trigger0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_ARVI1 > _s_OnCalculate_Trigger1 and ARVI0 < Trigger0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if bar < (rates_total - 1):
            _s_OnCalculate_ARVI1 = ARVI0
            _s_OnCalculate_Trigger1 = Trigger0
            Recount_ArrayZeroPos(Count, 100)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_ARVI1 = 0.0
_s_OnCalculate_Trigger1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Adaptivervisign(_MQL5Indicator):
    name = 'adaptivervisign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alpha': 0.07,  # Коэффициент усреднения индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

