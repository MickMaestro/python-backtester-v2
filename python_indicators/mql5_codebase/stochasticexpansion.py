"""stochasticexpansion — converted from MQL5: MQL5 Indicators/StochasticExpansion/stochasticexpansion.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 16711935, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'StochasticExpansion'}, 'levels': [], 'description': [], 'name': 'stochasticexpansion', 'source': 'MQL5 Indicators/StochasticExpansion/stochasticexpansion.mq5', 'folder': 'StochasticExpansion', 'inputs': [{'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'NoiseFilter', 'py': 'NoiseFilter', 'param': 'NoiseFilter', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'Filter_Method', 'py': 'Filter_Method', 'param': 'Filter_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'Filter_Phase', 'py': 'Filter_Phase', 'param': 'Filter_Phase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
KPeriod = _input('KPeriod', 13)
Slowing = _input('Slowing', 6)
NoiseFilter = _input('NoiseFilter', 6)
Filter_Method = _input('Filter_Method', MODE_SMA)  # Smoothing method
Filter_Phase = _input('Filter_Phase', 15)  # Smoothing parameter
Shift = _input('Shift', 0)  # Horizontal shift in bars
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
Count = Arr(0, 0)
Lowest = Arr(0, 0.0)
Highest = Arr(0, 0.0)
min_rates_total = 0
min_rates_total_1 = 0

def OnInit():
    global min_rates_total, min_rates_total_1
    min_rates_total_1 = KPeriod + Slowing
    min_rates_total = min_rates_total_1 + XMA1.GetStartBars(Filter_Method, NoiseFilter, Filter_Phase) + 1
    XMA1.XMALengthCheck('KPeriod', KPeriod)
    XMA1.XMALengthCheck('Slowing', Slowing)
    XMA1.XMALengthCheck('NoiseFilter', NoiseFilter)
    XMA1.XMAPhaseCheck('Filter_Phase', Filter_Phase, Filter_Method)
    if ArrayResize(Count, Slowing) < Slowing:
        Print('Failed to distribute the memory for Count[] array')
    if ArrayResize(Lowest, Slowing) < Slowing:
        Print('Failed to distribute the memory for Lowest[] array')
    if ArrayResize(Highest, Slowing) < Slowing:
        Print('Failed to distribute the memory for Highest[] array')
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer, True)
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorExtLineBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'StochasticExpansion(', KPeriod, ' ,', Slowing, ' ,', NoiseFilter, ' ,', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def Recount_ArrayZeroPos(CountArray, Size):
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
        CountArray[iii] = numb

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    maxbar = 0
    KLine1 = 0.0
    KLine2 = 0.0
    KLine = 0.0
    value = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total_1 - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    maxbar = rates_total - min_rates_total_1 - 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Lowest[Count[0]] = low[ArrayMinimum(low, bar, KPeriod)]
        Highest[Count[0]] = high[ArrayMaximum(high, bar, KPeriod)]
        if bar > maxbar:
            ExtLineBuffer[bar] = EMPTY_VALUE
            ColorExtLineBuffer[bar] = 0.0
            Recount_ArrayZeroPos(Count, Slowing)
            continue
        sumlow = 0.0
        sumhigh = 0.0
        for k in range(0, Slowing):
            bark = bar + k
            r = Count[k]
            sumlow += close[bark] - Lowest[r]
            sumhigh += Highest[r] - close[bark]
        if sumhigh:
            KLine1 = _fdiv(sumlow, sumhigh)
        if sumlow:
            KLine2 = _fdiv(-sumhigh, sumlow)
        KLine = KLine1 + KLine2
        ExtLineBuffer[bar] = KLine
        value = XMA1.XMASeries(maxbar, prev_calculated, rates_total, Filter_Method, Filter_Phase, NoiseFilter, KLine, bar, True)
        if KLine < value:
            ColorExtLineBuffer[bar] = 1.0
        elif KLine > value:
            ColorExtLineBuffer[bar] = 2.0
        else:
            ColorExtLineBuffer[bar] = 0.0
        if bar:
            Recount_ArrayZeroPos(Count, Slowing)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Stochasticexpansion(_MQL5Indicator):
    name = 'stochasticexpansion'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'KPeriod': 13,
        'Slowing': 6,
        'NoiseFilter': 6,
        'Filter_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method
        'Filter_Phase': 15,  # Smoothing parameter
        'Shift': 0,  # Horizontal shift in bars
    }

