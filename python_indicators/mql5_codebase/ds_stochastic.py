"""ds_stochastic — converted from MQL5: MQL5 Indicators/DS_Stochastic/ds_stochastic.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [3329434, 9639167]}, 'widths': {}, 'styles': {}, 'labels': {1: 'DS_Stochastic'}, 'levels': [70.0, 50.0, 30.0], 'description': [], 'name': 'ds_stochastic', 'source': 'MQL5 Indicators/DS_Stochastic/ds_stochastic.mq5', 'folder': 'DS_Stochastic', 'inputs': [{'mql': 'qPeriod', 'py': 'qPeriod', 'param': 'qPeriod', 'type': 'uint', 'default': 13, 'label': 'Период поиска экстремумов', 'sinput': False}, {'mql': 'rMethod', 'py': 'rMethod', 'param': 'rMethod', 'type': 'int', 'default': 1, 'label': 'Метод усреднения 1', 'sinput': False}, {'mql': 'rPeriod', 'py': 'rPeriod', 'param': 'rPeriod', 'type': 'uint', 'default': 32, 'label': 'Период усреднения 1', 'sinput': False}, {'mql': 'rPhase', 'py': 'rPhase', 'param': 'rPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания 1', 'sinput': False}, {'mql': 'fMethod', 'py': 'fMethod', 'param': 'fMethod', 'type': 'int', 'default': 1, 'label': 'Метод усреднения 2', 'sinput': False}, {'mql': 'fPeriod', 'py': 'fPeriod', 'param': 'fPeriod', 'type': 'uint', 'default': 5, 'label': 'Период усреднения 2', 'sinput': False}, {'mql': 'fPhase', 'py': 'fPhase', 'param': 'fPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания 2', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
qPeriod = _input('qPeriod', 13)  # Период поиска экстремумов
rMethod = _input('rMethod', MODE_EMA)  # Метод усреднения 1
rPeriod = _input('rPeriod', 32)  # Период усреднения 1
rPhase = _input('rPhase', 15)  # Параметр сглаживания 1
fMethod = _input('fMethod', MODE_EMA)  # Метод усреднения 2
fPeriod = _input('fPeriod', 5)  # Период усреднения 2
fPhase = _input('fPhase', 15)  # Параметр сглаживания 2
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_2 = 0
min_rates_total = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = _int(qPeriod)
    min_rates_2 = min_rates_1 + XMA1.GetStartBars(rMethod, rPeriod, rPhase)
    min_rates_total = min_rates_2 + XMA1.GetStartBars(fMethod, fPeriod, fPhase)
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DS_Stochastic')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    maxbar1 = 0
    maxbar2 = 0
    HH = 0.0
    LL = 0.0
    DIF1 = 0.0
    DIF2 = 0.0
    CH = 0.0
    RN = 0.0
    XDIF1 = 0.0
    XDIF2 = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    maxbar1 = rates_total - min_rates_1 - 1
    maxbar2 = rates_total - min_rates_2 - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar1
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HH = high[ArrayMaximum(high, bar, qPeriod)]
        LL = low[ArrayMinimum(low, bar, qPeriod)]
        CH = close[bar] - LL
        RN = HH - LL
        DIF1 = XMA1.XMASeries(maxbar1, prev_calculated, rates_total, rMethod, rPhase, rPeriod, CH, bar, True)
        DIF2 = XMA2.XMASeries(maxbar1, prev_calculated, rates_total, rMethod, rPhase, rPeriod, RN, bar, True)
        if DIF2:
            ExtABuffer[bar] = _fdiv(100 * DIF1, DIF2)
        else:
            ExtABuffer[bar] = 100.0
        XDIF1 = XMA3.XMASeries(maxbar2, prev_calculated, rates_total, fMethod, fPhase, fPeriod, DIF1, bar, True)
        XDIF2 = XMA4.XMASeries(maxbar2, prev_calculated, rates_total, fMethod, fPhase, fPeriod, DIF2, bar, True)
        if XDIF2:
            ExtBBuffer[bar] = _fdiv(100 * XDIF1, XDIF2)
        else:
            ExtBBuffer[bar] = 100.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()
XMA4 = _alloc(CXMA)
XMA4.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DsStochastic(_MQL5Indicator):
    name = 'ds_stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'qPeriod': 13,  # Период поиска экстремумов
        'rMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения 1
        'rPeriod': 32,  # Период усреднения 1
        'rPhase': 15,  # Параметр сглаживания 1
        'fMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения 2
        'fPeriod': 5,  # Период усреднения 2
        'fPhase': 15,  # Параметр сглаживания 2
    }

