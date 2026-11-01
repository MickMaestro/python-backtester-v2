"""test_momentum_onvaluerb — converted from MQL5: MQL5 Indicators/The class for drawing the Momentum using the ring buffer/test_momentum_onvaluerb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_cmomentumonringbuffer import *  # #include cmomentumonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Label1', 2: 'Label2'}, 'levels': [], 'description': [], 'name': 'test_momentum_onvaluerb', 'source': 'MQL5 Indicators/The class for drawing the Momentum using the ring buffer/test_momentum_onvaluerb.mq5', 'folder': 'The class for drawing the Momentum using the ring buffer', 'inputs': [{'mql': 'MomentumPeriod', 'py': 'MomentumPeriod', 'param': 'MomentumPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['cmomentumonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
MomentumPeriod = _input('MomentumPeriod', 14)  # Period
Momentum_Buffer = Arr(0, 0.0)
Momentum_RingBuffer = Arr(0, 0.0)

def OnInit():
    if not momentum.Init(MomentumPeriod):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    SetIndexBuffer(0, Momentum_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, momentum.Name())
    SetIndexBuffer(1, Momentum_RingBuffer, INDICATOR_DATA)
    PlotIndexSetString(1, PLOT_LABEL, 'RB ' + momentum.Name())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    start = 0
    start1 = 0
    if prev_calculated == 0:
        start1 = rates_total - momentum.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start + momentum.BarsRequired())
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start1)
        ArrayInitialize(Momentum_Buffer, EMPTY_VALUE)
        ArrayInitialize(Momentum_RingBuffer, EMPTY_VALUE)
    else:
        start1 = prev_calculated - 1
        start = start1
    for i in range(start, rates_total):
        Momentum_Buffer[i] = momentum.MainOnValue(rates_total, prev_calculated, begin, price[i], i)
    for i in range(start1, rates_total):
        Momentum_RingBuffer[i] = momentum[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
momentum = _alloc(CMomentumOnRingBuffer)
momentum.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestMomentumOnvaluerb(_MQL5Indicator):
    name = 'test_momentum_onvaluerb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MomentumPeriod': 14,  # Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

