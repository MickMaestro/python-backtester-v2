"""cronexrsi — converted from MQL5: MQL5 Indicators/CronexRSI_HTF/cronexrsi.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [13749760, 11823615]}, 'widths': {}, 'styles': {}, 'labels': {1: 'CronexRSI'}, 'levels': [70.0, 50.0, 30.0], 'description': [], 'name': 'cronexrsi', 'source': 'MQL5 Indicators/CronexRSI_HTF/cronexrsi.mq5', 'folder': 'CronexRSI_HTF', 'inputs': [{'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 25, 'label': 'Период индикатора RSI', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': 'Цена индикатора RSI', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'uint', 'default': 14, 'label': 'Период быстрого усреднения', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'uint', 'default': 25, 'label': 'Метод медленного усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
RSIPeriod = _input('RSIPeriod', 25)  # Период индикатора RSI
RSIPrice = _input('RSIPrice', PRICE_CLOSE)  # Цена индикатора RSI
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
FastPeriod = _input('FastPeriod', 14)  # Период быстрого усреднения
SlowPeriod = _input('SlowPeriod', 25)  # Метод медленного усреднения
XPhase = _input('XPhase', 15)  # Параметр сглаживания
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
Ind_Handle = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_total = 0

def OnInit():
    global Ind_Handle, min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = _int(RSIPeriod)
    min_rates_2 = min_rates_1 + XMA1.GetStartBars(XMA_Method, FastPeriod, XPhase)
    min_rates_total = min_rates_2 + XMA1.GetStartBars(XMA_Method, SlowPeriod, XPhase)
    Ind_Handle = iRSI(Symbol(), PERIOD_CURRENT, RSIPeriod, RSIPrice)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
        return INIT_FAILED
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CronexRSI')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
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


class Cronexrsi(_MQL5Indicator):
    name = 'cronexrsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIPeriod': 25,  # Период индикатора RSI
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена индикатора RSI
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'FastPeriod': 14,  # Период быстрого усреднения
        'SlowPeriod': 25,  # Метод медленного усреднения
        'XPhase': 15,  # Параметр сглаживания
    }

