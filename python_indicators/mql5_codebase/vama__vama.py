"""vama — converted from MQL5: MQL5 Indicators/VAMA/vama.mq5

Copyright: Copyright © 2013, J.B; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2013, J.B', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14772545]}, 'widths': {1: 3}, 'styles': {}, 'labels': {1: 'vaMA'}, 'levels': [], 'description': [], 'name': 'vama', 'source': 'MQL5 Indicators/VAMA/vama.mq5', 'folder': 'VAMA', 'inputs': [{'mql': 'vaMA_period', 'py': 'vaMA_period', 'param': 'vaMA_period', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'use_double_smooth', 'py': 'use_double_smooth', 'param': 'use_double_smooth', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
vaMA_period = _input('vaMA_period', 15)
use_double_smooth = _input('use_double_smooth', (1 != 0))
vaMA_buffer = Arr(0, 0.0)
EMA = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, vaMA_buffer, INDICATOR_DATA)
    SetIndexBuffer(1, EMA, INDICATOR_CALCULATIONS)

def OnCalculate(rates_total, prev_calculated, begin, price):
    first = 0
    bar = 0
    vel = 0.0
    acc = 0.0
    aaa = 0.0
    ExponentialMAOnBuffer(rates_total, prev_calculated, begin, vaMA_period, price, EMA)
    if rates_total < (vaMA_period - 1):
        return 0
    if prev_calculated == 0:
        first = vaMA_period - 1 + begin
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        vel = EMA[bar] - EMA[bar - _idiv(vaMA_period, 4)]
        acc = EMA[bar] - (2 * EMA[bar - _idiv(vaMA_period, 4)]) + EMA[bar - _idiv(vaMA_period, 8)]
        aaa = EMA[bar] - (3 * EMA[bar - _idiv(vaMA_period, 4)]) + (3 * EMA[bar - _idiv(vaMA_period, 8)]) - EMA[bar - _idiv(vaMA_period, 12)]
        vaMA_buffer[bar] = EMA[bar] + vel + (acc / 2) + (aaa / 6)
    else:
        bar = _range_end(bar, rates_total, 1)
    if use_double_smooth:
        ExponentialMAOnBuffer(rates_total, prev_calculated, begin, _idiv(vaMA_period, 4), vaMA_buffer, vaMA_buffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vama(_MQL5Indicator):
    name = 'vama'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'vaMA_period': 15,
        'use_double_smooth': True,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

