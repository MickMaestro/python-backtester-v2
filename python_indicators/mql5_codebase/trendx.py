"""TrendX — converted from MQL5: MQL5 Indicators/TrendX/TrendX.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'TrendX Fast', 2: 'TrendX Slow'}, 'levels': [], 'description': [], 'name': 'TrendX', 'source': 'MQL5 Indicators/TrendX/TrendX.mq5', 'folder': 'TrendX', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 1, 'label': 'метод усреднения быстрого сглаживания', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 21, 'label': 'глубина быстрого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр быстрого сглаживания,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 1, 'label': 'метод усреднения медленного сглаживания', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 80, 'label': 'глубина медленного сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'параметр медленного сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
MA_Method1 = _input('MA_Method1', MODE_EMA_)  # метод усреднения быстрого сглаживания
Length1 = _input('Length1', 21)  # глубина быстрого сглаживания
Phase1 = _input('Phase1', 15)  # параметр быстрого сглаживания,
MA_Method2 = _input('MA_Method2', MODE_EMA_)  # метод усреднения медленного сглаживания
Length2 = _input('Length2', 80)  # глубина медленного сглаживания
Phase2 = _input('Phase2', 15)  # параметр медленного сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
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

def OnInit():
    global min_rates_total
    min_rates_total = _int(MathMax(Length1, Length2))
    ArrayResize(Count, min_rates_total)
    ArrayResize(Value1, min_rates_total)
    ArrayResize(Value2, min_rates_total)
    SetIndexBuffer(0, IndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, IndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    short_name = 'TrendX(' + _str(Length1) + ' ,' + _str(Length2) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    Sign = 0
    price = 0.0
    Fast = 0.0
    Fast2 = 0.0
    Slow = 0.0
    Slow2 = 0.0
    Diff = 0.0
    Diff2 = 0.0
    Percent = 0.0
    absmacd = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        ArrayInitialize(Count, 0)
        ArrayInitialize(Value1, 0.0)
        ArrayInitialize(Value2, 0.0)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        Value1[Count[0]] = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price, bar, False)
        Fast = Value1[Count[0]]
        Value2[Count[0]] = XMA2.XMASeries(0, prev_calculated, rates_total, MA_Method2, Phase2, Length2, price, bar, False)
        Slow = Value2[Count[0]]
        Fast2 = Value1[Count[Length1 - 1]]
        Slow2 = Value2[Count[Length2 - 1]]
        absmacd = MathAbs(Fast - Slow)
        Diff = MathAbs(absmacd - MathAbs(Fast - Slow2))
        Diff2 = absmacd + (MathAbs(Fast2 - Slow2) / 2)
        Percent = Diff * 100 * ((Fast + Fast2) / 2) * Diff2
        if (absmacd - MathAbs(Fast - Slow2)) < 0:
            Sign = -1
        else:
            Sign = 1
        IndBuffer1[bar] = Percent * Sign
        IndBuffer2[bar] = Slow - Fast + (Fast - Fast2)
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, min_rates_total)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendX(_MQL5Indicator):
    name = 'TrendX'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # метод усреднения быстрого сглаживания
        'Length1': 21,  # глубина быстрого сглаживания
        'Phase1': 15,  # параметр быстрого сглаживания,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # метод усреднения медленного сглаживания
        'Length2': 80,  # глубина медленного сглаживания
        'Phase2': 15,  # параметр медленного сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

