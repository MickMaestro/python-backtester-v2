"""test_atr_onarrayrb — converted from MQL5: MQL5 Indicators/The class for drawing the ATR using the ring buffer/test_atr_onarrayrb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_catronringbuffer import *  # #include catronringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # #include cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'test_atr_onarrayrb', 'source': 'MQL5 Indicators/The class for drawing the ATR using the ring buffer/test_atr_onarrayrb.mq5', 'folder': 'The class for drawing the ATR using the ring buffer', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['catronringbuffer.mqh', 'cmaonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 14)
MAMethod = _input('MAMethod', MODE_SMA)
ATR_Buffer = Arr(0, 0.0)

def OnInit():
    if not atr.Init(MAPeriod, MAMethod):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, ATR_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, atr.Name())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    atr.MainOnArray(rates_total, prev_calculated, high, low, close)
    start = 0
    if prev_calculated == 0:
        start = rates_total - atr.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        ArrayInitialize(ATR_Buffer, EMPTY_VALUE)
    else:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        ATR_Buffer[i] = atr[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
atr = _alloc(CATROnRingBuffer)
atr.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestAtrOnarrayrb(_MQL5Indicator):
    name = 'test_atr_onarrayrb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MAPeriod': 14,
        'MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
    }

