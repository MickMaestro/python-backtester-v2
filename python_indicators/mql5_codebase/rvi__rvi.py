"""RVI — converted from MQL5: MQL5 Indicators/RVI/RVI.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'RVI', 2: 'Trigger'}, 'levels': [0.0], 'description': [], 'name': 'RVI', 'source': 'MQL5 Indicators/RVI/RVI.mq5', 'folder': 'RVI', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 8, 'label': 'период индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 8)  # период индикатора
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
RVIBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
min_rates_total = 0
Count = Arr(0, 0)
Value1 = Arr(0, 0.0)
Value2 = Arr(0, 0.0)
dPriceHL = Arr(0, 0.0)
dPriceOC = Arr(0, 0.0)

def Get_dPrice(Price1, Price2, bar):
    return Price1[bar] - Price2[bar]

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
    global min_rates_total
    min_rates_total = Length + 3
    ArrayResize(Count, Length)
    ArrayResize(Value1, Length)
    ArrayResize(Value2, Length)
    SetIndexBuffer(0, RVIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'RVI(', Length, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    Num = 0.0
    Denom = 0.0
    rvi = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 3
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
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
            rvi = 0.0
        RVIBuffer[bar] = rvi
        TriggerBuffer[bar] = RVIBuffer[bar - 1]
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, Length)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RVI(_MQL5Indicator):
    name = 'RVI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 8,  # период индикатора
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

