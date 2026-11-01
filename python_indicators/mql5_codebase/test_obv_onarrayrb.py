"""test_obv_onarrayrb — converted from MQL5: MQL5 Indicators/The class for drawing the OBV using the ring buffer/test_obv_onarrayrb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.cobvonringbuffer import *  # #include cobvonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'test_obv_onarrayrb', 'source': 'MQL5 Indicators/The class for drawing the OBV using the ring buffer/test_obv_onarrayrb.mq5', 'folder': 'The class for drawing the OBV using the ring buffer', 'inputs': [{'mql': 'OBVVolume', 'py': 'OBVVolume', 'param': 'OBVVolume', 'type': 'int', 'default': 0, 'label': 'Volume type', 'sinput': False}, {'mql': 'OBVPeriod', 'py': 'OBVPeriod', 'param': 'OBVPeriod', 'type': 'int', 'default': 0, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['cobvonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
OBVVolume = _input('OBVVolume', VOLUME_TICK)  # Volume type
OBVPeriod = _input('OBVPeriod', 0)  # Period
OBV_Buffer = Arr(0, 0.0)

def OnInit():
    if not obv.Init(OBVPeriod):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    SetIndexBuffer(0, OBV_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, obv.Name())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if OBVVolume == VOLUME_TICK:
        obv.MainOnArray(rates_total, prev_calculated, close, tick_volume)
    else:
        obv.MainOnArray(rates_total, prev_calculated, close, volume)
    start = 0
    if prev_calculated == 0:
        start = rates_total - obv.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        ArrayInitialize(OBV_Buffer, EMPTY_VALUE)
    else:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        OBV_Buffer[i] = obv[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
obv = _alloc(COBVOnRingBuffer)
obv.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestObvOnarrayrb(_MQL5Indicator):
    name = 'test_obv_onarrayrb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'OBVVolume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume type
        'OBVPeriod': 0,  # Period
    }

