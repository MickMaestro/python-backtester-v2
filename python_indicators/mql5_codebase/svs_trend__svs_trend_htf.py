"""SVS_Trend — converted from MQL5: MQL5 Indicators/SVS_Trend_HTF/SVS_Trend.mq5

SVS_Trend
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3}, 'colors': {1: [14599344], 2: [14822282], 3: [0], 4: [13434880], 5: [255], 6: [65280]}, 'widths': {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['SVS_Trend'], 'name': 'SVS_Trend', 'source': 'MQL5 Indicators/SVS_Trend_HTF/SVS_Trend.mq5', 'folder': 'SVS_Trend_HTF', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'метод первого усреднения', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 100, 'label': 'глубина  первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр первого среднения,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 9, 'label': 'цена', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_SMA_)  # метод первого усреднения
Length1 = _input('Length1', 100)  # глубина  первого сглаживания
Phase1 = _input('Phase1', 15)  # параметр первого среднения,
IPC = _input('IPC', PRICE_QUARTER_)  # цена
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
ExtMapBuffer3 = Arr(0, 0.0)
ExtMapBuffer4 = Arr(0, 0.0)
ExtMapBuffer5 = Arr(0, 0.0)
ExtMapBuffer6 = Arr(0, 0.0)
min_rates_total = 0
StartBars1 = 0

def OnInit():
    global StartBars1, min_rates_total
    StartBars1 = XMA1.GetStartBars(MA_Method1, Length1, Phase1) + 1
    min_rates_total = StartBars1 + XMA1.GetStartBars(MA_Method1, Length1, Phase1)
    XMA1.XMALengthCheck('Length1', Length1)
    XMA1.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    SetIndexBuffer(0, ExtMapBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMapBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtMapBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ExtMapBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ExtMapBuffer5, INDICATOR_DATA)
    SetIndexBuffer(5, ExtMapBuffer6, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(MA_Method1)
    StringConcatenate(shortname, 'SVS_Trend(', Length1, ', ', Phase1, ', ', EnumToString(IPC, 'Applied_price_'), ', ', Shift, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    z = 0.0
    s1 = 0.0
    v1 = 0.0
    vv = 0.0
    sv = 0.0
    svz = 0.0
    vj = 0.0
    vk = 0.0
    vd = 0.0
    ff = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        z = _fdiv(PriceSeries(IPC, bar, open, low, high, close), Point())
        s1 = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, z, bar, False)
        v1 = XMA2.XMASeries(StartBars1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, s1, bar, False)
        sv = (s1 + v1) / 2
        svz = (sv + z) / 2
        ff = svz - sv
        vv = s1 - v1
        vk = (vv + ff) / 2
        vd = ff / 2
        vj = vv - vd
        ExtMapBuffer1[bar] = vv
        ExtMapBuffer2[bar] = vk
        ExtMapBuffer3[bar] = vd
        ExtMapBuffer4[bar] = EMPTY_VALUE
        ExtMapBuffer5[bar] = EMPTY_VALUE
        ExtMapBuffer6[bar] = EMPTY_VALUE
        if vd > 0:
            ExtMapBuffer4[bar] = vj
        if vd < 0:
            ExtMapBuffer5[bar] = vj
        if vd > 0 and vk < vj:
            ExtMapBuffer6[bar] = vj
        if vd < 0 and vk > vj:
            ExtMapBuffer6[bar] = vj
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SVSTrend(_MQL5Indicator):
    name = 'SVS_Trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод первого усреднения
        'Length1': 100,  # глубина  первого сглаживания
        'Phase1': 15,  # параметр первого среднения,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=9),  # цена
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

