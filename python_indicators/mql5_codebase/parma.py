"""parma — converted from MQL5: MQL5 Indicators/ParMA/parma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'parma', 'source': 'MQL5 Indicators/ParMA/parma.mq5', 'folder': 'ParMA', 'inputs': [{'mql': 'ParMAPeriod', 'py': 'ParMAPeriod', 'param': 'ParMAPeriod', 'type': 'int', 'default': 13, 'label': 'ParMA period', 'sinput': False}, {'mql': 'ParMAShift', 'py': 'ParMAShift', 'param': 'ParMAShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of ParMA in bars', 'sinput': False}, {'mql': 'ParMAPriceShift', 'py': 'ParMAPriceShift', 'param': 'ParMAPriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of ParMA in points', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
ParMAPeriod = _input('ParMAPeriod', 13)  # ParMA period
ParMAShift = _input('ParMAShift', 0)  # Horizontal shift of ParMA in bars
ParMAPriceShift = _input('ParMAPriceShift', 0)  # Vertical shift of ParMA in points
ExtLineBuffer = Arr(0, 0.0)
dPriceShift = 0.0

def OnInit():
    global dPriceShift
    short_name = 'ParMA'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + '(' + _str(ParMAPeriod) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ParMAPeriod)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, ParMAShift)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    dPriceShift = Point() * ParMAPriceShift

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (begin + ParMAPeriod):
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = begin
        bar = 0
        for bar in range(bar, begin + 1):
            ExtLineBuffer[bar] = 0.0
        else:
            bar = _range_end(bar, begin + 1, 1)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ExtLineBuffer[bar] = _s_OnCalculate_ParMA1.ParMASeries(begin, prev_calculated, rates_total, ParMAPeriod, price[bar], bar, False) + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_ParMA1 = CParMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Parma(_MQL5Indicator):
    name = 'parma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ParMAPeriod': 13,  # ParMA period
        'ParMAShift': 0,  # Horizontal shift of ParMA in bars
        'ParMAPriceShift': 0,  # Vertical shift of ParMA in points
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

