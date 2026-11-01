"""XPFE — converted from MQL5: MQL5 Indicators/XPFE_HTF/XPFE.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'XPFE'}, 'levels': [], 'description': [], 'name': 'XPFE', 'source': 'MQL5 Indicators/XPFE_HTF/XPFE.mq5', 'folder': 'XPFE_HTF', 'inputs': [{'mql': 'PfePeriod', 'py': 'PfePeriod', 'param': 'PfePeriod', 'type': 'uint', 'default': 5, 'label': 'период PFE', 'sinput': False}, {'mql': 'PfeMA_Method', 'py': 'PfeMA_Method', 'param': 'PfeMA_Method', 'type': 'int', 'default': 1, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'PfeLength', 'py': 'PfeLength', 'param': 'PfeLength', 'type': 'uint', 'default': 5, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'PfePhase', 'py': 'PfePhase', 'param': 'PfePhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
PfePeriod = _input('PfePeriod', 5)  # период PFE
PfeMA_Method = _input('PfeMA_Method', MODE_EMA_)  # метод усреднения
PfeLength = _input('PfeLength', 5)  # глубина сглаживания
PfePhase = _input('PfePhase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
XPFE = Arr(0, 0.0)
min_rates_total = 0
min_rates_Pfe = 0

def OnInit():
    global min_rates_Pfe, min_rates_total
    min_rates_Pfe = _int(PfePeriod) + 1
    min_rates_total = min_rates_Pfe + XMA1.GetStartBars(PfeMA_Method, PfeLength, PfePhase)
    XMA1.XMALengthCheck('PfeLength', PfeLength)
    XMA1.XMAPhaseCheck('PfePhase', PfePhase, PfeMA_Method)
    SetIndexBuffer(0, XPFE, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, PLOT_EMPTY_VALUE)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(PfeMA_Method)
    StringConcatenate(shortname, 'XPFE(', PfeLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    x1xma = 0.0
    noise = 0.0
    pfe = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_Pfe
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        noise = 1e-09
        for k in range(0, _int(PfePeriod)):
            noise += MathAbs(PriceSeries(IPC, bar - k, open, low, high, close) - PriceSeries(IPC, bar - k - 1, open, low, high, close))
        pfe = _fdiv(PriceSeries(IPC, bar, open, low, high, close) - PriceSeries(IPC, bar - PfePeriod, open, low, high, close), noise)
        x1xma = XMA1.XMASeries(min_rates_Pfe, prev_calculated, rates_total, PfeMA_Method, PfePhase, PfeLength, pfe, bar, False)
        XPFE[bar] = x1xma
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XPFEIndicator(_MQL5Indicator):
    name = 'XPFE'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PfePeriod': 5,  # период PFE
        'PfeMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # метод усреднения
        'PfeLength': 5,  # глубина сглаживания
        'PfePhase': 15,  # параметр сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

