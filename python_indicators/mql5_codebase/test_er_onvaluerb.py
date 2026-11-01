"""test_er_onvaluerb — converted from MQL5: MQL5 Indicators/The class for drawing the ER using the ring buffer/test_er_onvaluerb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_ceronringbuffer import *  # #include ceronringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Label1', 2: 'Label2'}, 'levels': [], 'description': [], 'name': 'test_er_onvaluerb', 'source': 'MQL5 Indicators/The class for drawing the ER using the ring buffer/test_er_onvaluerb.mq5', 'folder': 'The class for drawing the ER using the ring buffer', 'inputs': [{'mql': 'InpPeriodER', 'py': 'InpPeriodER', 'param': 'InpPeriodER', 'type': 'int', 'default': 34, 'label': 'ER period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['ceronringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
InpPeriodER = _input('InpPeriodER', 34)  # ER period
ER_Buffer = Arr(0, 0.0)
ER_RingBuffer = Arr(0, 0.0)

def OnInit():
    if not er.Init(InpPeriodER):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    SetIndexBuffer(0, ER_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, er.Name())
    SetIndexBuffer(1, ER_RingBuffer, INDICATOR_DATA)
    PlotIndexSetString(1, PLOT_LABEL, 'RB ' + er.Name())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    start = 0
    start1 = 0
    if prev_calculated == 0:
        start1 = rates_total - er.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start1 + er.BarsRequired())
        ArrayInitialize(ER_Buffer, EMPTY_VALUE)
        ArrayInitialize(ER_RingBuffer, EMPTY_VALUE)
    else:
        start1 = prev_calculated - 1
        start = start1
    for i in range(start, rates_total):
        ER_Buffer[i] = er.MainOnValue(rates_total, prev_calculated, begin, price[i], i)
    for i in range(start1, rates_total):
        ER_RingBuffer[i] = er[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
er = _alloc(CEROnRingBuffer)
er.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestErOnvaluerb(_MQL5Indicator):
    name = 'test_er_onvaluerb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriodER': 34,  # ER period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

