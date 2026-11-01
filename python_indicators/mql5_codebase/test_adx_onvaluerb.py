"""test_adx_onvaluerb — converted from MQL5: MQL5 Indicators/The class for drawing the ADX using the ring buffer/test_adx_onvaluerb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_cadxonringbuffer import *  # #include cadxonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # #include cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [255], 2: [16711680], 3: [65535], 4: [255], 5: [16711680], 6: [65535]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {2: 2, 3: 2, 5: 2, 6: 2}, 'labels': {1: 'Label1', 2: 'Label2', 3: 'Label3', 4: 'Label4', 5: 'Label5', 6: 'Label6'}, 'levels': [], 'description': [], 'name': 'test_adx_onvaluerb', 'source': 'MQL5 Indicators/The class for drawing the ADX using the ring buffer/test_adx_onvaluerb.mq5', 'folder': 'The class for drawing the ADX using the ring buffer', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['cadxonringbuffer.mqh', 'cmaonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 14)
MAMethod = _input('MAMethod', MODE_EMA)
ADX_Buffer = Arr(0, 0.0)
PDI_Buffer = Arr(0, 0.0)
NDI_Buffer = Arr(0, 0.0)
ADX_RingBuffer = Arr(0, 0.0)
PDI_RingBuffer = Arr(0, 0.0)
NDI_RingBuffer = Arr(0, 0.0)

def OnInit():
    if not adx.Init(MAPeriod, MAMethod):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    SetIndexBuffer(0, ADX_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, adx.NameADX())
    SetIndexBuffer(1, PDI_Buffer, INDICATOR_DATA)
    PlotIndexSetString(1, PLOT_LABEL, adx.NamePDI())
    SetIndexBuffer(2, NDI_Buffer, INDICATOR_DATA)
    PlotIndexSetString(2, PLOT_LABEL, adx.NameNDI())
    SetIndexBuffer(3, ADX_RingBuffer, INDICATOR_DATA)
    PlotIndexSetString(3, PLOT_LABEL, 'RB' + adx.NameADX())
    SetIndexBuffer(4, PDI_RingBuffer, INDICATOR_DATA)
    PlotIndexSetString(4, PLOT_LABEL, 'RB' + adx.NamePDI())
    SetIndexBuffer(5, NDI_RingBuffer, INDICATOR_DATA)
    PlotIndexSetString(5, PLOT_LABEL, 'RB' + adx.NameNDI())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = 0
    begin = 0
    start1 = 0
    if prev_calculated == 0:
        start1 = rates_total - adx.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, start)
        ArrayInitialize(ADX_Buffer, EMPTY_VALUE)
        ArrayInitialize(PDI_Buffer, EMPTY_VALUE)
        ArrayInitialize(NDI_Buffer, EMPTY_VALUE)
        PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, start1)
        PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, start1)
        PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, start1)
        ArrayInitialize(ADX_RingBuffer, EMPTY_VALUE)
        ArrayInitialize(PDI_RingBuffer, EMPTY_VALUE)
        ArrayInitialize(NDI_RingBuffer, EMPTY_VALUE)
    else:
        start1 = prev_calculated - 1
        start = start1
    for i in range(start, rates_total):
        ADX_Buffer[i] = adx.MainOnValue(rates_total, prev_calculated, begin, high[i], low[i], close[i], i)
        PDI_Buffer[i] = adx.pdi.Last_0()
        NDI_Buffer[i] = adx.ndi.Last_0()
    for i in range(start1, rates_total):
        ADX_RingBuffer[i] = adx[rates_total - 1 - i]
        PDI_RingBuffer[i] = adx.pdi[rates_total - 1 - i]
        NDI_RingBuffer[i] = adx.ndi[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
adx = _alloc(CADXOnRingBuffer)
adx.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestAdxOnvaluerb(_MQL5Indicator):
    name = 'test_adx_onvaluerb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MAPeriod': 14,
        'MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
    }

