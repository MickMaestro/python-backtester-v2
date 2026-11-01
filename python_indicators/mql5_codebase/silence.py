"""silence — converted from MQL5: MQL5 Indicators/Silence/silence.mq5

Copyright: Copyright © 2009, Trofimov Evgeniy Vitalyevich; Link: http://TrofimovVBA.narod.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Trofimov Evgeniy Vitalyevich', 'link': 'http://TrofimovVBA.narod.ru/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Aggressiveness', 2: 'Volatility'}, 'levels': [50.0], 'description': [], 'name': 'silence', 'source': 'MQL5 Indicators/Silence/silence.mq5', 'folder': 'Silence', 'inputs': [{'mql': 'MyPeriod1', 'py': 'MyPeriod1', 'param': 'MyPeriod1', 'type': 'uint', 'default': 12, 'label': 'volatility period', 'sinput': False}, {'mql': 'MyPeriod2', 'py': 'MyPeriod2', 'param': 'MyPeriod2', 'type': 'uint', 'default': 96, 'label': 'extremums searching period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MyPeriod1 = _input('MyPeriod1', 12)  # volatility period
MyPeriod2 = _input('MyPeriod2', 96)  # extremums searching period
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
min_rates_ = 0
min_rates_total = 0
Count = Arr(0, 0)
Aggress = Arr(0, 0.0)
Volatility = Arr(0, 0.0)

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

def Interpolation(a, b, c, d, X):
    if (b - a) == 0:
        return 10000000.0
    else:
        return d - _fdiv((b - X) * (d - c), b - a)

def OnInit():
    global min_rates_, min_rates_total
    min_rates_ = _int(MyPeriod1 + 1)
    min_rates_total = min_rates_ + _int(MyPeriod2)
    ArrayResize(Count, MyPeriod2)
    ArrayResize(Aggress, MyPeriod2)
    ArrayResize(Volatility, MyPeriod2)
    ArrayInitialize(Aggress, 0.0)
    ArrayInitialize(Volatility, 0.0)
    ArraySetAsSeries(Count, True)
    ArraySetAsSeries(Aggress, True)
    ArraySetAsSeries(Volatility, True)
    SetIndexBuffer(0, IndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(IndBuffer1, True)
    SetIndexBuffer(1, IndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(IndBuffer2, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Silence(', MyPeriod1, ', ', MyPeriod2, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    bar0 = 0
    Sum = 0.0
    HH = 0.0
    LL = 0.0
    MAX = 0.0
    MIN = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_ - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        bar0 = Count[0]
        Sum = 0.0
        for x in range(0, _int(MyPeriod1)):
            barx = bar + x
            if close[barx] > open[barx]:
                Sum += close[barx] - close[barx + 1]
            else:
                Sum += close[barx + 1] - close[barx]
        Aggress[bar0] = _fdiv(Sum, Point() * MyPeriod1)
        MAX = Aggress[ArrayMaximum(Aggress, 0, WHOLE_ARRAY)]
        MIN = Aggress[ArrayMinimum(Aggress, 0, WHOLE_ARRAY)]
        IndBuffer1[bar] = Interpolation(MAX, MIN, 100.0, 0.0, Aggress[bar0])
        HH = high[ArrayMaximum(high, bar, MyPeriod1)]
        LL = low[ArrayMinimum(low, bar, MyPeriod1)]
        Volatility[bar0] = _fdiv(HH - LL, Point() * MyPeriod1)
        MAX = Volatility[ArrayMaximum(Volatility, 0, WHOLE_ARRAY)]
        MIN = Volatility[ArrayMinimum(Volatility, 0, WHOLE_ARRAY)]
        IndBuffer2[bar] = Interpolation(MAX, MIN, 100.0, 0.0, Volatility[bar0])
        if bar > 0:
            Recount_ArrayZeroPos(Count, MyPeriod2)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Silence(_MQL5Indicator):
    name = 'silence'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MyPeriod1': 12,  # volatility period
        'MyPeriod2': 96,  # extremums searching period
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

