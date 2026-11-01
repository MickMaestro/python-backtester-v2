"""ColorXTRIX_Histogram — converted from MQL5: MQL5 Indicators/ColorXTRIX_Histogram/ColorXTRIX_Histogram.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421376, 14822282, 6053069, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'XTRIX'}, 'levels': [0.0], 'description': [], 'name': 'ColorXTRIX_Histogram', 'source': 'MQL5 Indicators/ColorXTRIX_Histogram/ColorXTRIX_Histogram.mq5', 'folder': 'ColorXTRIX_Histogram', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 5, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'uint', 'default': 5, 'label': 'глубина сглаживания готового индикатора', 'sinput': False}, {'mql': 'Mom_Period', 'py': 'Mom_Period', 'param': 'Mom_Period', 'type': 'uint', 'default': 1, 'label': 'momentum период индикатора', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_JJMA)  # метод усреднения
XLength = _input('XLength', 5)  # глубина сглаживания
XPhase = _input('XPhase', 100)  # параметр сглаживания,
Smooth = _input('Smooth', 5)  # глубина сглаживания готового индикатора
Mom_Period = _input('Mom_Period', 1)  # momentum период индикатора
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0
MomPeriod = 0
Count = Arr(0, 0)
xxlprice = Arr(0, 0.0)

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
    global MomPeriod, min_rates_1, min_rates_2, min_rates_3, min_rates_total
    min_rates_1 = GetStartBars(XMA_Method, XLength, XPhase)
    min_rates_2 = 2 * min_rates_1
    min_rates_3 = min_rates_2 + _int(Mom_Period) + 1
    min_rates_total = min_rates_3 + GetStartBars(XMA_Method, Smooth, XPhase)
    MomPeriod = _int(Mom_Period) + 1
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMALengthCheck('Smooth', Smooth)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    ArrayResize(Count, MomPeriod)
    ArrayResize(xxlprice, MomPeriod)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'XTRIX(', Smooth1, ', ', Smooth, ', ', XLength, ', ', Mom_Period, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    lprice = 0.0
    xlprice = 0.0
    trix = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        ArrayInitialize(Count, 0)
        ArrayInitialize(xxlprice, 0.0)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        lprice = MathLog(price)
        xlprice = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, lprice, bar, False)
        xxlprice[Count[0]] = XMA2.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, xlprice, bar, False)
        trix = 10000 * (xxlprice[Count[0]] - xxlprice[Count[Mom_Period]])
        IndBuffer[bar] = XMA3.XMASeries(min_rates_3, prev_calculated, rates_total, XMA_Method, XPhase, Smooth, trix, bar, False)
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, MomPeriod)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        bar1 = bar - 1
        clr = 0
        if IndBuffer[bar] >= 0:
            if IndBuffer[bar] > IndBuffer[bar1]:
                clr = 0
            if IndBuffer[bar] < IndBuffer[bar1]:
                clr = 1
            if IndBuffer[bar] == IndBuffer[bar1]:
                clr = _int(ColorIndBuffer[bar1])
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar1]:
                clr = 2
            if IndBuffer[bar] > IndBuffer[bar1]:
                clr = 3
            if IndBuffer[bar] == IndBuffer[bar1]:
                clr = _int(ColorIndBuffer[bar1])
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorXTRIXHistogram(_MQL5Indicator):
    name = 'ColorXTRIX_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'XLength': 5,  # глубина сглаживания
        'XPhase': 100,  # параметр сглаживания,
        'Smooth': 5,  # глубина сглаживания готового индикатора
        'Mom_Period': 1,  # momentum период индикатора
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

