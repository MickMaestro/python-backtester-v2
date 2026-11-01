"""test_stochastic_onvaluerb — converted from MQL5: MQL5 Indicators/The class for drawing the Stochastic using the ring buffer/test_stochastic_onvaluerb.mq5

Copyright: Copyright 2012, Konstantin Gruzdev; Link: https://login.mql5.com/ru/users/Lizar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.inconringbuffer_cstochasticonringbuffer import *  # #include cstochasticonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_cmaonringbuffer import *  # #include cmaonringbuffer.mqh
from backtester.mql5.lib.inconringbuffer_carrayring import *  # #include carrayring.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Konstantin Gruzdev', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [255], 2: [16711680], 3: [32768], 4: [8421504]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 2, 3: 0, 4: 2}, 'labels': {1: 'Label1', 2: 'Label2', 3: 'Label3', 4: 'Label4'}, 'levels': [], 'description': [], 'name': 'test_stochastic_onvaluerb', 'source': 'MQL5 Indicators/The class for drawing the Stochastic using the ring buffer/test_stochastic_onvaluerb.mq5', 'folder': 'The class for drawing the Stochastic using the ring buffer', 'inputs': [{'mql': 'STPeriodK', 'py': 'STPeriodK', 'param': 'STPeriodK', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'STPeriodD', 'py': 'STPeriodD', 'param': 'STPeriodD', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'STPeriodS', 'py': 'STPeriodS', 'param': 'STPeriodS', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'STMethod', 'py': 'STMethod', 'param': 'STMethod', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['cstochasticonringbuffer.mqh', 'cmaonringbuffer.mqh', 'carrayring.mqh']}

# ---- inputs and global variables
STPeriodK = _input('STPeriodK', 5)
STPeriodD = _input('STPeriodD', 3)
STPeriodS = _input('STPeriodS', 3)
STMethod = _input('STMethod', MODE_SMA)
MainBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
MainRingBuffer = Arr(0, 0.0)
SignalRingBuffer = Arr(0, 0.0)

def OnInit():
    if not st.Init(STPeriodK, STPeriodD, STPeriodS, STMethod):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    SetIndexBuffer(0, MainBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, MainRingBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, SignalRingBuffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, st.Name())
    PlotIndexSetString(1, PLOT_LABEL, st.NameSignal())
    PlotIndexSetString(2, PLOT_LABEL, 'RB ' + st.Name())
    PlotIndexSetString(3, PLOT_LABEL, 'RB ' + st.NameSignal())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = 0
    start1 = 0
    if prev_calculated == 0:
        start1 = rates_total - st.Size() + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, start1)
        PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, start1)
        ArrayInitialize(MainBuffer, EMPTY_VALUE)
        ArrayInitialize(SignalBuffer, EMPTY_VALUE)
        ArrayInitialize(MainRingBuffer, EMPTY_VALUE)
        ArrayInitialize(SignalRingBuffer, EMPTY_VALUE)
    else:
        start1 = prev_calculated - 1
        start = start1
    for i in range(start, rates_total):
        MainBuffer[i] = st.MainOnValue(rates_total, prev_calculated, 0, high[i], low[i], close[i], i)
        SignalBuffer[i] = st.signal.Last_0()
    for i in range(start1, rates_total):
        MainRingBuffer[i] = st[rates_total - 1 - i]
        SignalRingBuffer[i] = st.signal[rates_total - 1 - i]
    return rates_total

# ---- global variables initialised from expressions
st = _alloc(CStochasticOnRingBuffer)
st.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestStochasticOnvaluerb(_MQL5Indicator):
    name = 'test_stochastic_onvaluerb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'STPeriodK': 5,
        'STPeriodD': 3,
        'STPeriodS': 3,
        'STMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
    }

