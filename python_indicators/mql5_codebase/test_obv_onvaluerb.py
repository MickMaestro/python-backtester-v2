"""test_obv_onvaluerb — converted from MQL5: MQL5 Indicators/The class for drawing the OBV using the ring buffer/test_obv_onvaluerb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.cobvonringbuffer import *  # #include cobvonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Label1', 2: 'Label2'}, 'levels': [], 'description': [], 'name': 'test_obv_onvaluerb', 'source': 'MQL5 Indicators/The class for drawing the OBV using the ring buffer/test_obv_onvaluerb.mq5', 'folder': 'The class for drawing the OBV using the ring buffer', 'inputs': [{'mql': 'OBVVolume', 'py': 'OBVVolume', 'param': 'OBVVolume', 'type': 'int', 'default': 0, 'label': 'Volume type', 'sinput': False}, {'mql': 'OBVPeriod', 'py': 'OBVPeriod', 'param': 'OBVPeriod', 'type': 'int', 'default': 0, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['cobvonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
OBVVolume = _input('OBVVolume', VOLUME_TICK)  # Volume type
OBVPeriod = _input('OBVPeriod', 0)  # Period
OBV_Buffer = Arr(0, 0.0)
OBV_RingBuffer = Arr(0, 0.0)

def OnInit():
    if not obv.Init(OBVPeriod):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    SetIndexBuffer(0, OBV_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, obv.Name())
    SetIndexBuffer(1, OBV_RingBuffer, INDICATOR_DATA)
    PlotIndexSetString(1, PLOT_LABEL, 'RB ' + obv.Name())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = 0
    begin = 0
    start1 = 0
    if prev_calculated == 0:
        start1 = rates_total - obv.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start + obv.BarsRequired())
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start1)
        ArrayInitialize(OBV_Buffer, EMPTY_VALUE)
        ArrayInitialize(OBV_RingBuffer, EMPTY_VALUE)
    else:
        start1 = prev_calculated - 1
        start = start1
    if OBVVolume == VOLUME_TICK:
        for i in range(start, rates_total):
            OBV_Buffer[i] = obv.MainOnValue(rates_total, prev_calculated, begin, close[i], tick_volume[i], i)
    else:
        for i in range(start, rates_total):
            OBV_Buffer[i] = obv.MainOnValue(rates_total, prev_calculated, begin, close[i], volume[i], i)
    for i in range(start1, rates_total):
        OBV_RingBuffer[i] = obv[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
obv = _alloc(COBVOnRingBuffer)
obv.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestObvOnvaluerb(_MQL5Indicator):
    name = 'test_obv_onvaluerb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'OBVVolume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume type
        'OBVPeriod': 0,  # Period
    }

