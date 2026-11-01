"""CHO — converted from MQL5: MQL5 Indicators/CHOWithFlat/CHO.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13749760]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'CHO'}, 'levels': [], 'description': [], 'name': 'CHO', 'source': 'MQL5 Indicators/CHOWithFlat/CHO.mq5', 'folder': 'CHOWithFlat', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'uint', 'default': 3, 'label': 'период быстрого усреднения', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'uint', 'default': 10, 'label': 'метод медленного усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_SMA)  # метод усреднения
FastPeriod = _input('FastPeriod', 3)  # период быстрого усреднения
SlowPeriod = _input('SlowPeriod', 10)  # метод медленного усреднения
XPhase = _input('XPhase', 15)  # параметр сглаживания,
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
ExtBuffer = Arr(0, 0.0)
Ind_Handle = 0
min_rates_ = 0
min_rates_total = 0

def OnInit():
    global Ind_Handle, min_rates_, min_rates_total
    min_rates_ = 2
    min_rates_1 = XMA1.GetStartBars(XMA_Method, FastPeriod, XPhase)
    min_rates_2 = XMA1.GetStartBars(XMA_Method, SlowPeriod, XPhase)
    min_rates_total = min_rates_ + MathMax(min_rates_1, min_rates_2)
    Ind_Handle = iAD(Symbol(), PERIOD_CURRENT, VolumeType)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iAD')
        return INIT_FAILED
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CHO')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or BarsCalculated(Ind_Handle) < rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    AD = Arr(0, 0.0)
    Fast = 0.0
    Slow = 0.0
    ArraySetAsSeries(AD, True)
    maxbar = rates_total - min_rates_ - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle, 0, 0, to_copy, AD) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Fast = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, FastPeriod, AD[bar], bar, True)
        Slow = XMA2.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, SlowPeriod, AD[bar], bar, True)
        ExtBuffer[bar] = Fast - Slow
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CHO(_MQL5Indicator):
    name = 'CHO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'FastPeriod': 3,  # период быстрого усреднения
        'SlowPeriod': 10,  # метод медленного усреднения
        'XPhase': 15,  # параметр сглаживания,
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
    }

