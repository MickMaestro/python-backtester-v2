"""cronexac — converted from MQL5: MQL5 Indicators/CronexAC_Signal/cronexac.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16748574, 42495]}, 'widths': {}, 'styles': {}, 'labels': {1: 'CronexAC'}, 'levels': [], 'description': [], 'name': 'cronexac', 'source': 'MQL5 Indicators/CronexAC_Signal/cronexac.mq5', 'folder': 'CronexAC_Signal', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'uint', 'default': 14, 'label': 'Period of fast smoothing', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'uint', 'default': 25, 'label': 'Period of slow smoothing', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_SMA)  # Smoothing method
FastPeriod = _input('FastPeriod', 14)  # Period of fast smoothing
SlowPeriod = _input('SlowPeriod', 25)  # Period of slow smoothing
XPhase = _input('XPhase', 15)  # Smoothing parameter
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
Ind_Handle = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_total = 0

def OnInit():
    global Ind_Handle, min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = 37
    min_rates_2 = min_rates_1 + XMA1.GetStartBars(XMA_Method, FastPeriod, XPhase)
    min_rates_total = min_rates_2 + XMA1.GetStartBars(XMA_Method, SlowPeriod, XPhase)
    Ind_Handle = iAC(Symbol(), PERIOD_CURRENT)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iAC indicator')
        return INIT_FAILED
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CronexAC')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or BarsCalculated(Ind_Handle) < rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar1 = 0
    maxbar2 = 0
    iInd = Arr(0, 0.0)
    ArraySetAsSeries(iInd, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_1 - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle, 0, 0, to_copy, iInd) <= 0:
        return 0
    maxbar1 = rates_total - min_rates_1 - 1
    maxbar2 = rates_total - min_rates_2 - 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtABuffer[bar] = XMA1.XMASeries(maxbar1, prev_calculated, rates_total, XMA_Method, XPhase, FastPeriod, iInd[bar], bar, True)
        ExtBBuffer[bar] = XMA2.XMASeries(maxbar2, prev_calculated, rates_total, XMA_Method, XPhase, SlowPeriod, ExtABuffer[bar], bar, True)
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


class Cronexac(_MQL5Indicator):
    name = 'cronexac'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method
        'FastPeriod': 14,  # Period of fast smoothing
        'SlowPeriod': 25,  # Period of slow smoothing
        'XPhase': 15,  # Smoothing parameter
    }

