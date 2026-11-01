"""blau_ergodic_dti — converted from MQL5: MQL5 Indicators/Ergodic DTI-Oscillator Blau_Ergodic_DTI/blau_ergodic_dti.mq5

Ergodic DTI-Oscillator (William Blau)
Copyright: Copyright 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.williamblau import *  # #include williamblau.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 12, 'indicator_plots': 2, 'indicator_minimum': -100.0, 'indicator_maximum': 100.0}, 'types': {1: 3, 2: 1}, 'colors': {1: [12632256], 2: [255]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Ergodic', 2: 'Signal'}, 'levels': [-25.0, 25.0], 'description': ['Ergodic DTI-Oscillator (William Blau)'], 'name': 'blau_ergodic_dti', 'source': 'MQL5 Indicators/Ergodic DTI-Oscillator Blau_Ergodic_DTI/blau_ergodic_dti.mq5', 'folder': 'Ergodic DTI-Oscillator Blau_Ergodic_DTI', 'inputs': [{'mql': 'q', 'py': 'q', 'param': 'q', 'type': 'int', 'default': 2, 'label': 'q - period of Momentum', 'sinput': False}, {'mql': 'r', 'py': 'r', 'param': 'r', 'type': 'int', 'default': 20, 'label': 'r - 1st EMA, applied to Momentum', 'sinput': False}, {'mql': 's', 'py': 's', 'param': 's', 'type': 'int', 'default': 5, 'label': 's - 2nd EMA, applied to the 1st smoothing', 'sinput': False}, {'mql': 'u', 'py': 'u', 'param': 'u', 'type': 'int', 'default': 3, 'label': 'u - 3rd EMA, applied to the 2nd smoothing', 'sinput': False}, {'mql': 'ul', 'py': 'ul', 'param': 'ul', 'type': 'int', 'default': 3, 'label': 'ul - period of a Signal Line', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['williamblau.mqh']}

# ---- inputs and global variables
q = _input('q', 2)  # q - period of Momentum
r = _input('r', 20)  # r - 1st EMA, applied to Momentum
s = _input('s', 5)  # s - 2nd EMA, applied to the 1st smoothing
u = _input('u', 3)  # u - 3rd EMA, applied to the 2nd smoothing
ul = _input('ul', 3)  # ul - period of a Signal Line
MainBuffer = Arr(0, 0.0)  # Egrodic Line (graphic plot #0)
SignalBuffer = Arr(0, 0.0)  # Signal Line: EMA(ul), applied to Ergodic Line (graphic plot #1)
HMUBuffer = Arr(0, 0.0)  # q-period Up Trend Momentum
LMDBuffer = Arr(0, 0.0)  # q-period Down Trend Momentum
HLMBuffer = Arr(0, 0.0)  # Composite High/Low Momentum
EMA_HLMBuffer = Arr(0, 0.0)  # r-period 1st EMA
DEMA_HLMBuffer = Arr(0, 0.0)  # s-period 2nd EMA
TEMA_HLMBuffer = Arr(0, 0.0)  # u-period 3rd EMA
AbsHLMBuffer = Arr(0, 0.0)  # Composite High/Low Momemtum (absolute values)
EMA_AbsHLMBuffer = Arr(0, 0.0)  # r-period 1st EMA (absolute values)
DEMA_AbsHLMBuffer = Arr(0, 0.0)  # s-period 2nd EMA (absolute values)
TEMA_AbsHLMBuffer = Arr(0, 0.0)  # u-period 3rd EMA (absolute values)
begin1 = 0  # starting bar index
begin2 = 0  # starting bar index
begin3 = 0  # starting bar index
begin4 = 0  # starting bar index
begin5 = 0  # starting bar index
rates_total_min = 0  # rates total min

def OnInit():
    global begin1, begin2, begin3, begin4, begin5, rates_total_min
    SetIndexBuffer(0, MainBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, HMUBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, LMDBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, HLMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, EMA_HLMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, DEMA_HLMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, TEMA_HLMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, AbsHLMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, EMA_AbsHLMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, DEMA_AbsHLMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, TEMA_AbsHLMBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    begin1 = q - 1
    begin2 = begin1 + r - 1
    begin3 = begin2 + s - 1
    begin4 = begin3 + u - 1
    begin5 = begin4 + ul - 1
    rates_total_min = begin5 + 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin4)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, begin5)
    shortname = _str(q) + ',' + _str(r) + ',' + _str(s) + ',' + _str(u) + ',' + _str(ul)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Blau_Ergodic_DTI(' + shortname + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    pos = 0
    value1 = 0.0
    value2 = 0.0
    if rates_total < rates_total_min:
        return 0
    if prev_calculated == 0:
        pos = begin1
        i = 0
        for i in range(i, pos):
            HLMBuffer[i] = 0.0
            AbsHLMBuffer[i] = 0.0
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
        AbsHLMBuffer[i] = MathAbs(HLMBuffer[i])
    else:
        i = _range_end(i, rates_total, 1)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin1, r, HLMBuffer, EMA_HLMBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin1, r, AbsHLMBuffer, EMA_AbsHLMBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin2, s, EMA_HLMBuffer, DEMA_HLMBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin2, s, EMA_AbsHLMBuffer, DEMA_AbsHLMBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin3, u, DEMA_HLMBuffer, TEMA_HLMBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin3, u, DEMA_AbsHLMBuffer, TEMA_AbsHLMBuffer)
    if prev_calculated == 0:
        pos = begin4
        i = 0
        for i in range(i, pos):
            MainBuffer[i] = 0.0
        else:
            i = _range_end(i, pos, 1)
    else:
        pos = prev_calculated - 1
    i = pos
    for i in range(i, rates_total):
        value1 = 100 * TEMA_HLMBuffer[i]
        value2 = TEMA_AbsHLMBuffer[i]
        MainBuffer[i] = (_fdiv(value1, value2) if (value2 > 0) else 0)
    else:
        i = _range_end(i, rates_total, 1)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin4, ul, MainBuffer, SignalBuffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BlauErgodicDti(_MQL5Indicator):
    name = 'blau_ergodic_dti'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'q': 2,  # q - period of Momentum
        'r': 20,  # r - 1st EMA, applied to Momentum
        's': 5,  # s - 2nd EMA, applied to the 1st smoothing
        'u': 3,  # u - 3rd EMA, applied to the 2nd smoothing
        'ul': 3,  # ul - period of a Signal Line
    }
    y_range = (-100.0, 100.0)

