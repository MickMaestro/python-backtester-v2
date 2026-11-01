"""test_rsi_onarrayrb — converted from MQL5: MQL5 Indicators/The class for drawing the RSI using the ring buffer/test_rsi_onarrayrb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_crsionringbuffer import *  # #include crsionringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # #include cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'test_rsi_onarrayrb', 'source': 'MQL5 Indicators/The class for drawing the RSI using the ring buffer/test_rsi_onarrayrb.mq5', 'folder': 'The class for drawing the RSI using the ring buffer', 'inputs': [{'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'RSIMethod', 'py': 'RSIMethod', 'param': 'RSIMethod', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['crsionringbuffer.mqh', 'cmaonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
RSIPeriod = _input('RSIPeriod', 14)
RSIMethod = _input('RSIMethod', MODE_SMMA)
RSI_Buffer = Arr(0, 0.0)

def OnInit():
    if not rsi.Init(RSIPeriod, RSIMethod):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    SetIndexBuffer(0, RSI_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, rsi.Name())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    rsi.MainOnArray(rates_total, prev_calculated, price)
    start = 0
    if prev_calculated == 0:
        start = rates_total - rsi.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        ArrayInitialize(RSI_Buffer, EMPTY_VALUE)
    else:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        RSI_Buffer[i] = rsi[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
rsi = _alloc(CRSIOnRingBuffer)
rsi.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestRsiOnarrayrb(_MQL5Indicator):
    name = 'test_rsi_onarrayrb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'RSIPeriod': 14,
        'RSIMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }
    y_range = (0.0, 100.0)

