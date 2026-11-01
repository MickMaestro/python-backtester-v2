"""test_fractals_onarrayrb — converted from MQL5: MQL5 Indicators/The class for drawing the Fractals using the ring buffer/test_fractals_onarrayrb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_cfractalsonringbuffer import *  # #include cfractalsonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [65535], 2: [65535]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'test_fractals_onarrayrb', 'source': 'MQL5 Indicators/The class for drawing the Fractals using the ring buffer/test_fractals_onarrayrb.mq5', 'folder': 'The class for drawing the Fractals using the ring buffer', 'inputs': [{'mql': 'BarsRight', 'py': 'BarsRight', 'param': 'BarsRight', 'type': 'int', 'default': 2, 'label': 'Of bars on the right', 'sinput': False}, {'mql': 'BarsLeft', 'py': 'BarsLeft', 'param': 'BarsLeft', 'type': 'int', 'default': 2, 'label': 'Of bars on the left', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['cfractalsonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
BarsRight = _input('BarsRight', 2)  # Of bars on the right
BarsLeft = _input('BarsLeft', 2)  # Of bars on the left
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
ext_arrow_shift = -10

def OnInit():
    if not fractals.Init(BarsRight, BarsLeft):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'Upper ' + fractals.Name())
    SetIndexBuffer(1, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetString(1, PLOT_LABEL, 'Lower ' + fractals.Name())
    PlotIndexSetInteger(0, PLOT_ARROW, 217)
    PlotIndexSetInteger(1, PLOT_ARROW, 218)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, ext_arrow_shift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -ext_arrow_shift)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    fractals.MainOnArray(rates_total, prev_calculated, high, low)
    start = 0
    if prev_calculated == 0:
        start = rates_total - fractals.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start)
        ArrayInitialize(UpperBuffer, EMPTY_VALUE)
        ArrayInitialize(LowerBuffer, EMPTY_VALUE)
    else:
        start = prev_calculated - BarsRight - 1
    for i in range(start, rates_total - BarsRight):
        UpperBuffer[i] = fractals.upper[rates_total - 1 - i]
        LowerBuffer[i] = fractals.lower[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
fractals = _alloc(CFractalsOnRingBuffer)
fractals.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestFractalsOnarrayrb(_MQL5Indicator):
    name = 'test_fractals_onarrayrb'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'BarsRight': 2,  # Of bars on the right
        'BarsLeft': 2,  # Of bars on the left
    }

