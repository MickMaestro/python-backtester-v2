"""t3maco — converted from MQL5: MQL5 Indicators/T3MACO/t3maco.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'T3MACO'}, 'levels': [], 'description': [], 'name': 't3maco', 'source': 'MQL5 Indicators/T3MACO/t3maco.mq5', 'folder': 'T3MACO', 'inputs': [{'mql': 'FastEMA', 'py': 'FastEMA', 'param': 'FastEMA', 'type': 'uint', 'default': 5, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'SlowEMA', 'py': 'SlowEMA', 'param': 'SlowEMA', 'type': 'uint', 'default': 8, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'T3Length', 'py': 'T3Length', 'param': 'T3Length', 'type': 'uint', 'default': 12, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'T3Phase', 'py': 'T3Phase', 'param': 'T3Phase', 'type': 'int', 'default': 15, 'label': 'smoothing parameter', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
FastEMA = _input('FastEMA', 5)  # Fast EMA period
SlowEMA = _input('SlowEMA', 8)  # Slow EMA period
T3Length = _input('T3Length', 12)  # smoothing depth
T3Phase = _input('T3Phase', 15)  # smoothing parameter
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
T3MACO = Arr(0, 0.0)
min_rates_ = 0
min_rates_total = 0

def OnInit():
    global min_rates_, min_rates_total
    min_rates_ = 2
    min_rates_total = min_rates_ + 1
    SetIndexBuffer(0, T3MACO, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'T3MACO')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ema1 = 0.0
    ema2 = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ema1 = EMA1.EMASeries(0, prev_calculated, rates_total, FastEMA, close[bar], bar, False)
        ema2 = EMA2.EMASeries(0, prev_calculated, rates_total, SlowEMA, open[bar], bar, False)
        T3MACO[bar] = T3.T3Series(1, prev_calculated, rates_total, MODE_T3, T3Phase, T3Length, ema1 - ema2, bar, False)
        T3MACO[bar] = _fdiv(T3MACO[bar], Point())
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
T3 = _alloc(CT3)
T3.__init__()
EMA1 = _alloc(CMoving_Average)
EMA1.__init__()
EMA2 = _alloc(CMoving_Average)
EMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3maco(_MQL5Indicator):
    name = 't3maco'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastEMA': 5,  # Fast EMA period
        'SlowEMA': 8,  # Slow EMA period
        'T3Length': 12,  # smoothing depth
        'T3Phase': 15,  # smoothing parameter
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

