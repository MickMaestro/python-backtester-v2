"""chande_momentum_oscillator — converted from MQL5: MQL5 Indicators/Chande_Momentum_Oscillator_HTF/chande_momentum_oscillator.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [55295]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'CMO'}, 'levels': [50.0, 0.0, -50.0], 'description': [], 'name': 'chande_momentum_oscillator', 'source': 'MQL5 Indicators/Chande_Momentum_Oscillator_HTF/chande_momentum_oscillator.mq5', 'folder': 'Chande_Momentum_Oscillator_HTF', 'inputs': [{'mql': 'CMO_period', 'py': 'CMO_period', 'param': 'CMO_period', 'type': 'int', 'default': 9, 'label': 'Период CMO', 'sinput': False}, {'mql': 'CMO_Shift', 'py': 'CMO_Shift', 'param': 'CMO_Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
CMO_period = _input('CMO_period', 9)  # Период CMO
CMO_Shift = _input('CMO_Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtLineBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, CMO_Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, CMO_period)
    shortname = Box("")
    StringConcatenate(shortname, 'CMO(', CMO_period, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (CMO_period + 1 + begin):
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0 + begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, CMO_period + 2 + begin)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ExtLineBuffer[bar] = (_s_OnCalculate_CMO.CMOSeries(begin, prev_calculated, rates_total, CMO_period, price[bar], bar, False) * 200) - 100
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_CMO = CCMO()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChandeMomentumOscillator(_MQL5Indicator):
    name = 'chande_momentum_oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CMO_period': 9,  # Период CMO
        'CMO_Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

