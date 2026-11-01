"""test_dema_onarrayrb — converted from MQL5: MQL5 Indicators/The class for drawing the DEMA using the ring buffer/test_dema_onarrayrb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_cdemaonringbuffer import *  # #include cdemaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # #include cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'test_dema_onarrayrb', 'source': 'MQL5 Indicators/The class for drawing the DEMA using the ring buffer/test_dema_onarrayrb.mq5', 'folder': 'The class for drawing the DEMA using the ring buffer', 'inputs': [{'mql': 'DEMAPeriod', 'py': 'DEMAPeriod', 'param': 'DEMAPeriod', 'type': 'int', 'default': 12, 'label': 'Period', 'sinput': False}, {'mql': 'DEMAMethod', 'py': 'DEMAMethod', 'param': 'DEMAMethod', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['cdemaonringbuffer.mqh', 'cmaonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
DEMAPeriod = _input('DEMAPeriod', 12)  # Period
DEMAMethod = _input('DEMAMethod', MODE_EMA)  # Method
DEMA_Buffer = Arr(0, 0.0)

def OnInit():
    if not dema.Init(DEMAPeriod, DEMAMethod):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    SetIndexBuffer(0, DEMA_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, dema.Name())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    dema.MainOnArray(rates_total, prev_calculated, price)
    start = 0
    if prev_calculated == 0:
        start = rates_total - dema.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        ArrayInitialize(DEMA_Buffer, EMPTY_VALUE)
    else:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        DEMA_Buffer[i] = dema[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
dema = _alloc(CDEMAOnRingBuffer)
dema.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestDemaOnarrayrb(_MQL5Indicator):
    name = 'test_dema_onarrayrb'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'DEMAPeriod': 12,  # Period
        'DEMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Method
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

