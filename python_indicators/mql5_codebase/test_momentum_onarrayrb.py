"""test_momentum_onarrayrb — converted from MQL5: MQL5 Indicators/The class for drawing the Momentum using the ring buffer/test_momentum_onarrayrb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_cmomentumonringbuffer import *  # #include cmomentumonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'test_momentum_onarrayrb', 'source': 'MQL5 Indicators/The class for drawing the Momentum using the ring buffer/test_momentum_onarrayrb.mq5', 'folder': 'The class for drawing the Momentum using the ring buffer', 'inputs': [{'mql': 'MomentumPeriod', 'py': 'MomentumPeriod', 'param': 'MomentumPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['cmomentumonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
MomentumPeriod = _input('MomentumPeriod', 14)  # Period
Momentum_Buffer = Arr(0, 0.0)

def OnInit():
    if not momentum.Init(MomentumPeriod):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    SetIndexBuffer(0, Momentum_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, momentum.Name())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    momentum.MainOnArray(rates_total, prev_calculated, price)
    start = 0
    if prev_calculated == 0:
        start = rates_total - momentum.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        ArrayInitialize(Momentum_Buffer, EMPTY_VALUE)
    else:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        Momentum_Buffer[i] = momentum[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
momentum = _alloc(CMomentumOnRingBuffer)
momentum.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestMomentumOnarrayrb(_MQL5Indicator):
    name = 'test_momentum_onarrayrb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MomentumPeriod': 14,  # Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

