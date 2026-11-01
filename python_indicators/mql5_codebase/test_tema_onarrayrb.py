"""test_tema_onarrayrb — converted from MQL5: MQL5 Indicators/The class for drawing the TEMA using the ring buffer/test_tema_onarrayrb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_ctemaonringbuffer import *  # #include ctemaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_cdemaonringbuffer import *  # #include cdemaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # #include cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'test_tema_onarrayrb', 'source': 'MQL5 Indicators/The class for drawing the TEMA using the ring buffer/test_tema_onarrayrb.mq5', 'folder': 'The class for drawing the TEMA using the ring buffer', 'inputs': [{'mql': 'TEMAPeriod', 'py': 'TEMAPeriod', 'param': 'TEMAPeriod', 'type': 'int', 'default': 12, 'label': 'Period', 'sinput': False}, {'mql': 'TEMAMethod', 'py': 'TEMAMethod', 'param': 'TEMAMethod', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['ctemaonringbuffer.mqh', 'cdemaonringbuffer.mqh', 'cmaonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
TEMAPeriod = _input('TEMAPeriod', 12)  # Period
TEMAMethod = _input('TEMAMethod', MODE_EMA)  # Method
TEMA_Buffer = Arr(0, 0.0)

def OnInit():
    if not tema.Init(TEMAPeriod, TEMAMethod):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    SetIndexBuffer(0, TEMA_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, tema.Name())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    tema.MainOnArray(rates_total, prev_calculated, price)
    start = 0
    if prev_calculated == 0:
        start = rates_total - tema.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        ArrayInitialize(TEMA_Buffer, EMPTY_VALUE)
    else:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        TEMA_Buffer[i] = tema[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
tema = _alloc(CTEMAOnRingBuffer)
tema.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestTemaOnarrayrb(_MQL5Indicator):
    name = 'test_tema_onarrayrb'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TEMAPeriod': 12,  # Period
        'TEMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Method
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

