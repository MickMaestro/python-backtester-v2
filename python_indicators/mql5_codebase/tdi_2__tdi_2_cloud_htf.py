"""TDI-2 — converted from MQL5: MQL5 Indicators/TDI-2_Cloud_HTF/TDI-2.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [14822282]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Trend Direction Index', 2: 'Direction'}, 'levels': [], 'description': [], 'name': 'TDI-2', 'source': 'MQL5 Indicators/TDI-2_Cloud_HTF/TDI-2.mq5', 'folder': 'TDI-2_Cloud_HTF', 'inputs': [{'mql': 'TdiMethod', 'py': 'TdiMethod', 'param': 'TdiMethod', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'TdiPeriod', 'py': 'TdiPeriod', 'param': 'TdiPeriod', 'type': 'uint', 'default': 20, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'TdiPhase', 'py': 'TdiPhase', 'param': 'TdiPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
TdiMethod = _input('TdiMethod', MODE_SMA_)  # метод усреднения
TdiPeriod = _input('TdiPeriod', 20)  # глубина сглаживания
TdiPhase = _input('TdiPhase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
TDI = Arr(0, 0.0)
Direct = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = _int(TdiPeriod)
    min_rates_2 = min_rates_1 + XMA1.GetStartBars(TdiMethod, TdiPeriod, TdiPhase)
    min_rates_total = min_rates_1 + min_rates_2 + (2 * XMA1.GetStartBars(TdiMethod, TdiPeriod, TdiPhase))
    XMA1.XMALengthCheck('TdiPeriod', TdiPeriod)
    XMA1.XMAPhaseCheck('TdiPhase', TdiPhase, TdiMethod)
    SetIndexBuffer(0, TDI, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, Direct, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(TdiMethod)
    StringConcatenate(shortname, 'Trend Direction Index(', Smooth, ', ', TdiPeriod, ', ', TdiPhase, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    Mom = 0.0
    MomAbs = 0.0
    MomSum = 0.0
    MomSumAbs = 0.0
    MomAbsSum = 0.0
    MomAbsSum2 = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = _int(TdiPeriod)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Mom = PriceSeries(IPC, bar, open, low, high, close) - PriceSeries(IPC, bar - TdiPeriod, open, low, high, close)
        MomAbs = MathAbs(Mom)
        MomSum = TdiPeriod * XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, TdiMethod, TdiPhase, TdiPeriod, Mom, bar, False)
        MomSumAbs = MathAbs(MomSum)
        MomAbsSum = TdiPeriod * XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, TdiMethod, TdiPhase, TdiPeriod, MomAbs, bar, False)
        MomAbsSum2 = 2 * TdiPeriod * XMA3.XMASeries(min_rates_2, prev_calculated, rates_total, TdiMethod, TdiPhase, 2 * TdiPeriod, MomAbs, bar, False)
        TDI[bar] = MomSumAbs - (MomAbsSum2 - MomAbs)
        Direct[bar] = MomSum
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TDI2(_MQL5Indicator):
    name = 'TDI-2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TdiMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'TdiPeriod': 20,  # глубина сглаживания
        'TdiPhase': 15,  # параметр сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

