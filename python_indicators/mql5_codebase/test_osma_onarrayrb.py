"""test_osma_onarrayrb — converted from MQL5: MQL5 Indicators/The class for drawing the OsCD using the ring buffer/test_osma_onarrayrb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_cosmaonringbuffer import *  # #include cosmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_cmacdonringbuffer import *  # #include cmacdonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # #include cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [13959039]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'test_osma_onarrayrb', 'source': 'MQL5 Indicators/The class for drawing the OsCD using the ring buffer/test_osma_onarrayrb.mq5', 'folder': 'The class for drawing the OsCD using the ring buffer', 'inputs': [{'mql': 'OsMAFastPeriod', 'py': 'OsMAFastPeriod', 'param': 'OsMAFastPeriod', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'OsMASlowPeriod', 'py': 'OsMASlowPeriod', 'param': 'OsMASlowPeriod', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'OsMASignalPeriod', 'py': 'OsMASignalPeriod', 'param': 'OsMASignalPeriod', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'OsMAFastMetod', 'py': 'OsMAFastMetod', 'param': 'OsMAFastMetod', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'OsMASlowMethod', 'py': 'OsMASlowMethod', 'param': 'OsMASlowMethod', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'OsMASignalMethod', 'py': 'OsMASignalMethod', 'param': 'OsMASignalMethod', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['cosmaonringbuffer.mqh', 'cmacdonringbuffer.mqh', 'cmaonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
OsMAFastPeriod = _input('OsMAFastPeriod', 12)
OsMASlowPeriod = _input('OsMASlowPeriod', 26)
OsMASignalPeriod = _input('OsMASignalPeriod', 9)
OsMAFastMetod = _input('OsMAFastMetod', MODE_EMA)
OsMASlowMethod = _input('OsMASlowMethod', MODE_EMA)
OsMASignalMethod = _input('OsMASignalMethod', MODE_SMA)
OsMABuffer = Arr(0, 0.0)

def OnInit():
    if not osma.Init(OsMAFastPeriod, OsMASlowPeriod, OsMASignalPeriod, OsMAFastMetod, OsMASlowMethod, OsMASignalMethod):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 2)
    SetIndexBuffer(0, OsMABuffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, osma.Name())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    osma.MainOnArray(rates_total, prev_calculated, price)
    start = 0
    if prev_calculated == 0:
        start = rates_total - osma.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        ArrayInitialize(OsMABuffer, EMPTY_VALUE)
    else:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        OsMABuffer[i] = osma[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
osma = _alloc(COsMAOnRingBuffer)
osma.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestOsmaOnarrayrb(_MQL5Indicator):
    name = 'test_osma_onarrayrb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'OsMAFastPeriod': 12,
        'OsMASlowPeriod': 26,
        'OsMASignalPeriod': 9,
        'OsMAFastMetod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'OsMASlowMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'OsMASignalMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

