"""test_mfi_onvaluerb — converted from MQL5: MQL5 Indicators/The class for drawing the MFI using the ring buffer/test_mfi_onvaluerb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_cmfionringbuffer import *  # #include cmfionringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # #include cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Label1', 2: 'Label2'}, 'levels': [20.0, 80.0], 'description': [], 'name': 'test_mfi_onvaluerb', 'source': 'MQL5 Indicators/The class for drawing the MFI using the ring buffer/test_mfi_onvaluerb.mq5', 'folder': 'The class for drawing the MFI using the ring buffer', 'inputs': [{'mql': 'MFIPeriod', 'py': 'MFIPeriod', 'param': 'MFIPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'MFIMethod', 'py': 'MFIMethod', 'param': 'MFIMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'MFIPriceType', 'py': 'MFIPriceType', 'param': 'MFIPriceType', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'MFIVolumeType', 'py': 'MFIVolumeType', 'param': 'MFIVolumeType', 'type': 'int', 'default': 0, 'label': 'Volumes', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['cmfionringbuffer.mqh', 'cmaonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
MFIPeriod = _input('MFIPeriod', 14)  # Period
MFIMethod = _input('MFIMethod', MODE_SMA)  # Method
MFIPriceType = _input('MFIPriceType', PRICE_TYPICAL)  # Price
MFIVolumeType = _input('MFIVolumeType', VOLUME_TICK)  # Volumes
MFI_Buffer = Arr(0, 0.0)
MFI_RingBuffer = Arr(0, 0.0)

def OnInit():
    if not mfi.Init(MFIPeriod, MFIMethod, MFIPriceType, MFIVolumeType):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, MFI_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, mfi.Name())
    SetIndexBuffer(1, MFI_RingBuffer, INDICATOR_DATA)
    PlotIndexSetString(1, PLOT_LABEL, 'RB ' + mfi.Name())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = 0
    begin = 0
    start1 = 0
    if prev_calculated == 0:
        start1 = rates_total - mfi.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start + mfi.BarsRequired())
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start1)
        ArrayInitialize(MFI_Buffer, EMPTY_VALUE)
        ArrayInitialize(MFI_RingBuffer, EMPTY_VALUE)
    else:
        start1 = prev_calculated - 1
        start = start1
    for i in range(start, rates_total):
        MFI_Buffer[i] = mfi.MainOnValue(rates_total, prev_calculated, begin, open[i], high[i], low[i], close[i], tick_volume[i], volume[i], i)
    for i in range(start1, rates_total):
        MFI_RingBuffer[i] = mfi[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
mfi = _alloc(CMFIOnRingBuffer)
mfi.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestMfiOnvaluerb(_MQL5Indicator):
    name = 'test_mfi_onvaluerb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MFIPeriod': 14,  # Period
        'MFIMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'MFIPriceType': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'MFIVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volumes
    }
    y_range = (0.0, 100.0)

