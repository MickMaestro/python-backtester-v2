"""test_macd_onarrayrb — converted from MQL5: MQL5 Indicators/The class to draw MACD using the ring buffer/test_macd_onarrayrb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_cmacdonringbuffer import *  # #include cmacdonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # #include cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 1}, 'colors': {1: [13959039], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Label1', 2: 'Label2'}, 'levels': [], 'description': [], 'name': 'test_macd_onarrayrb', 'source': 'MQL5 Indicators/The class to draw MACD using the ring buffer/test_macd_onarrayrb.mq5', 'folder': 'The class to draw MACD using the ring buffer', 'inputs': [{'mql': 'MACDFastPeriod', 'py': 'MACDFastPeriod', 'param': 'MACDFastPeriod', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'MACDSlowPeriod', 'py': 'MACDSlowPeriod', 'param': 'MACDSlowPeriod', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'MACDSignalPeriod', 'py': 'MACDSignalPeriod', 'param': 'MACDSignalPeriod', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'MACDFastMetod', 'py': 'MACDFastMetod', 'param': 'MACDFastMetod', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MACDSlowMethod', 'py': 'MACDSlowMethod', 'param': 'MACDSlowMethod', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MACDSignalMethod', 'py': 'MACDSignalMethod', 'param': 'MACDSignalMethod', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['cmacdonringbuffer.mqh', 'cmaonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
MACDFastPeriod = _input('MACDFastPeriod', 12)
MACDSlowPeriod = _input('MACDSlowPeriod', 26)
MACDSignalPeriod = _input('MACDSignalPeriod', 9)
MACDFastMetod = _input('MACDFastMetod', MODE_EMA)
MACDSlowMethod = _input('MACDSlowMethod', MODE_EMA)
MACDSignalMethod = _input('MACDSignalMethod', MODE_SMA)
MainBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)

def OnInit():
    if not macd.Init(MACDFastPeriod, MACDSlowPeriod, MACDSignalPeriod, MACDFastMetod, MACDSlowMethod, MACDSignalMethod):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    SetIndexBuffer(0, MainBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, macd.NameMain())
    PlotIndexSetString(1, PLOT_LABEL, macd.NameSignal())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    macd.MainOnArray(rates_total, prev_calculated, price)
    start = 0
    if prev_calculated == 0:
        start = rates_total - macd.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start)
        ArrayInitialize(MainBuffer, EMPTY_VALUE)
        ArrayInitialize(SignalBuffer, EMPTY_VALUE)
    else:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        MainBuffer[i] = macd[rates_total - 1 - i]
        SignalBuffer[i] = macd.signal[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
macd = _alloc(CMACDOnRingBuffer)
macd.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestMacdOnarrayrb(_MQL5Indicator):
    name = 'test_macd_onarrayrb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MACDFastPeriod': 12,
        'MACDSlowPeriod': 26,
        'MACDSignalPeriod': 9,
        'MACDFastMetod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MACDSlowMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MACDSignalMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

