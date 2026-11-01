"""test_ma_onvaluerb — converted from MQL5: MQL5 Indicators/The class for drawing Moving Average using the ring buffer/test_ma_onvaluerb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # #include cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Label1', 2: 'MA RB'}, 'levels': [], 'description': [], 'name': 'test_ma_onvaluerb', 'source': 'MQL5 Indicators/The class for drawing Moving Average using the ring buffer/test_ma_onvaluerb.mq5', 'folder': 'The class for drawing Moving Average using the ring buffer', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['cmaonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 14)
MAMethod = _input('MAMethod', MODE_SMA)
MA_Buffer = Arr(0, 0.0)
MA_RingBuffer = Arr(0, 0.0)

def OnInit():
    if not ma.Init(MAPeriod, MAMethod):
        return INIT_FAILED
    if not ma_rb.Init(MAPeriod, MAMethod):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, MA_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, ma.Name())
    SetIndexBuffer(1, MA_RingBuffer, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    start = 0
    start1 = 0
    begin1 = 0
    if prev_calculated == 0:
        start = begin
        start1 = rates_total - ma.Size() + 1
        begin1 = start1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start1 + ma.BarsRequired())
        ArrayInitialize(MA_Buffer, EMPTY_VALUE)
        ArrayInitialize(MA_RingBuffer, EMPTY_VALUE)
    else:
        start1 = prev_calculated - 1
        start = start1
    for i in range(start, rates_total):
        MA_Buffer[i] = ma.MainOnValue(rates_total, prev_calculated, begin, price[i], i)
    for i in range(start1, rates_total):
        MA_RingBuffer[i] = ma_rb.MainOnValue(rates_total, prev_calculated, begin1, ma[rates_total - 1 - i], i)
    return rates_total

# ---- global variables initialised from expressions
ma = _alloc(CMAOnRingBuffer)
ma.__init__()
ma_rb = _alloc(CMAOnRingBuffer)
ma_rb.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestMaOnvaluerb(_MQL5Indicator):
    name = 'test_ma_onvaluerb'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MAPeriod': 14,
        'MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

