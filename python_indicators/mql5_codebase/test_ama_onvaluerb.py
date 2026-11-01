"""test_ama_onvaluerb — converted from MQL5: MQL5 Indicators/The class for drawing the AMA using the ring buffer/test_ama_onvaluerb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_camaonringbuffer import *  # #include camaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_ceronringbuffer import *  # #include ceronringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Label1', 2: 'Label2'}, 'levels': [], 'description': [], 'name': 'test_ama_onvaluerb', 'source': 'MQL5 Indicators/The class for drawing the AMA using the ring buffer/test_ama_onvaluerb.mq5', 'folder': 'The class for drawing the AMA using the ring buffer', 'inputs': [{'mql': 'InpPeriodAMA', 'py': 'InpPeriodAMA', 'param': 'InpPeriodAMA', 'type': 'int', 'default': 10, 'label': 'AMA period', 'sinput': False}, {'mql': 'InpFastPeriodEMA', 'py': 'InpFastPeriodEMA', 'param': 'InpFastPeriodEMA', 'type': 'int', 'default': 2, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpSlowPeriodEMA', 'py': 'InpSlowPeriodEMA', 'param': 'InpSlowPeriodEMA', 'type': 'int', 'default': 30, 'label': 'Slow EMA period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['camaonringbuffer.mqh', 'ceronringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
InpPeriodAMA = _input('InpPeriodAMA', 10)  # AMA period
InpFastPeriodEMA = _input('InpFastPeriodEMA', 2)  # Fast EMA period
InpSlowPeriodEMA = _input('InpSlowPeriodEMA', 30)  # Slow EMA period
AMA_Buffer = Arr(0, 0.0)
AMA_RingBuffer = Arr(0, 0.0)

def OnInit():
    if not ama.Init(InpPeriodAMA, InpFastPeriodEMA, InpSlowPeriodEMA):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    SetIndexBuffer(0, AMA_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, ama.Name())
    SetIndexBuffer(1, AMA_RingBuffer, INDICATOR_DATA)
    PlotIndexSetString(1, PLOT_LABEL, 'RB ' + ama.Name())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    start = 0
    start1 = 0
    if prev_calculated == 0:
        start1 = rates_total - ama.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start + ama.BarsRequired())
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start1 + ama.BarsRequired())
        ArrayInitialize(AMA_Buffer, EMPTY_VALUE)
        ArrayInitialize(AMA_RingBuffer, EMPTY_VALUE)
    else:
        start1 = prev_calculated - 1
        start = start1
    for i in range(start, rates_total):
        AMA_Buffer[i] = ama.MainOnValue(rates_total, prev_calculated, begin, price[i], i)
    for i in range(start1, rates_total):
        AMA_RingBuffer[i] = ama[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
ama = _alloc(CAMAOnRingBuffer)
ama.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestAmaOnvaluerb(_MQL5Indicator):
    name = 'test_ama_onvaluerb'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodAMA': 10,  # AMA period
        'InpFastPeriodEMA': 2,  # Fast EMA period
        'InpSlowPeriodEMA': 30,  # Slow EMA period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

