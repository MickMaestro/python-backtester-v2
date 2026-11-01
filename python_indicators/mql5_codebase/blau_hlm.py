"""blau_hlm — converted from MQL5: MQL5 Indicators/Composite High_Low Momentum Blau_HLM/blau_hlm.mq5

q-period Composite High-Low Momentum (William Blau)
Copyright: Copyright 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.williamblau import *  # #include williamblau.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'HLM'}, 'levels': [], 'description': ['q-period Composite High-Low Momentum (William Blau)'], 'name': 'blau_hlm', 'source': 'MQL5 Indicators/Composite High_Low Momentum Blau_HLM/blau_hlm.mq5', 'folder': 'Composite High_Low Momentum Blau_HLM', 'inputs': [{'mql': 'q', 'py': 'q', 'param': 'q', 'type': 'int', 'default': 2, 'label': 'q - period of Momentum', 'sinput': False}, {'mql': 'r', 'py': 'r', 'param': 'r', 'type': 'int', 'default': 20, 'label': 'r - 1st EMA, applied to Momentum', 'sinput': False}, {'mql': 's', 'py': 's', 'param': 's', 'type': 'int', 'default': 5, 'label': 's - 2nd EMA, applied to the 1st smoothing', 'sinput': False}, {'mql': 'u', 'py': 'u', 'param': 'u', 'type': 'int', 'default': 3, 'label': 'u - 3rd EMA, applied to the 2nd smoothing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['williamblau.mqh']}

# ---- inputs and global variables
q = _input('q', 2)  # q - period of Momentum
r = _input('r', 20)  # r - 1st EMA, applied to Momentum
s = _input('s', 5)  # s - 2nd EMA, applied to the 1st smoothing
u = _input('u', 3)  # u - 3rd EMA, applied to the 2nd smoothing
MainBuffer = Arr(0, 0.0)  # u-period 3rd EMA (graphic plot #0)
HMUBuffer = Arr(0, 0.0)  # q-period Up Trend Momentum
LMDBuffer = Arr(0, 0.0)  # q-period Down Trend Momentum
HLMBuffer = Arr(0, 0.0)  # Composite High/Low Momentum (H)
EMA_HLMBuffer = Arr(0, 0.0)  # r-period 1st EMA
DEMA_HLMBuffer = Arr(0, 0.0)  # s-period 2nd EMA
begin1 = 0  # starting indexes
begin2 = 0  # starting indexes
begin3 = 0  # starting indexes
begin4 = 0  # starting indexes
rates_total_min = 0  # rates total min

def OnInit():
    global begin1, begin2, begin3, begin4, rates_total_min
    SetIndexBuffer(0, MainBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HMUBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, LMDBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, HLMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, EMA_HLMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, DEMA_HLMBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    begin1 = q - 1
    begin2 = begin1 + r - 1
    begin3 = begin2 + s - 1
    begin4 = begin3 + u - 1
    rates_total_min = begin4 + 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin4)
    shortname = _str(q) + ',' + _str(r) + ',' + _str(s) + ',' + _str(u)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Blau_HLM(' + shortname + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    pos = 0
    if rates_total < rates_total_min:
        return 0
    if prev_calculated == 0:
        pos = begin1
        i = 0
        for i in range(i, pos):
            HLMBuffer[i] = 0.0
            HMUBuffer[i] = 0.0
            LMDBuffer[i] = 0.0
        else:
            i = _range_end(i, pos, 1)
    else:
        pos = prev_calculated - 1
    i = pos
    for i in range(i, rates_total):
        HMUBuffer[i] = High[i] - High[i - (q - 1)]
        HMUBuffer[i] = (HMUBuffer[i] if (HMUBuffer[i] > 0) else 0)
        LMDBuffer[i] = -1 * (Low[i] - Low[i - (q - 1)])
        LMDBuffer[i] = (LMDBuffer[i] if (LMDBuffer[i] > 0) else 0)
        HLMBuffer[i] = HMUBuffer[i] - LMDBuffer[i]
    else:
        i = _range_end(i, rates_total, 1)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin1, r, HLMBuffer, EMA_HLMBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin2, s, EMA_HLMBuffer, DEMA_HLMBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin3, u, DEMA_HLMBuffer, MainBuffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BlauHlm(_MQL5Indicator):
    name = 'blau_hlm'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'q': 2,  # q - period of Momentum
        'r': 20,  # r - 1st EMA, applied to Momentum
        's': 5,  # s - 2nd EMA, applied to the 1st smoothing
        'u': 3,  # u - 3rd EMA, applied to the 2nd smoothing
    }

