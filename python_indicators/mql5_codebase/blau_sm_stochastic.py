"""blau_sm_stochastic — converted from MQL5: MQL5 Indicators/Stochastic Momentum Oscillator Blau_SM_Stochastic/blau_sm_stochastic.mq5

Stochastic Oscillator (William Blau)
Copyright: Copyright 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.williamblau import *  # #include williamblau.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 13, 'indicator_plots': 2, 'indicator_minimum': -100.0, 'indicator_maximum': 100.0}, 'types': {1: 3, 2: 1}, 'colors': {1: [12632256], 2: [255]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'SMI', 2: 'Signal'}, 'levels': [-40.0, 40.0], 'description': ['Stochastic Oscillator (William Blau)'], 'name': 'blau_sm_stochastic', 'source': 'MQL5 Indicators/Stochastic Momentum Oscillator Blau_SM_Stochastic/blau_sm_stochastic.mq5', 'folder': 'Stochastic Momentum Oscillator Blau_SM_Stochastic', 'inputs': [{'mql': 'q', 'py': 'q', 'param': 'q', 'type': 'int', 'default': 5, 'label': 'q - period of Stochastic Momentum', 'sinput': False}, {'mql': 'r', 'py': 'r', 'param': 'r', 'type': 'int', 'default': 20, 'label': 'r - 1st EMA, applied to Stochastic Momentum', 'sinput': False}, {'mql': 's', 'py': 's', 'param': 's', 'type': 'int', 'default': 5, 'label': 's - 2nd EMA, applied to the 1st smoothing', 'sinput': False}, {'mql': 'u', 'py': 'u', 'param': 'u', 'type': 'int', 'default': 3, 'label': 'u - 3rd EMA, applied to the 2nd smoothing', 'sinput': False}, {'mql': 'ul', 'py': 'ul', 'param': 'ul', 'type': 'int', 'default': 3, 'label': 'ul - period of a Signal Line', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'AppliedPrice - price type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['williamblau.mqh']}

# ---- inputs and global variables
q = _input('q', 5)  # q - period of Stochastic Momentum
r = _input('r', 20)  # r - 1st EMA, applied to Stochastic Momentum
s = _input('s', 5)  # s - 2nd EMA, applied to the 1st smoothing
u = _input('u', 3)  # u - 3rd EMA, applied to the 2nd smoothing
ul = _input('ul', 3)  # ul - period of a Signal Line
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)  # AppliedPrice - price type
MainBuffer = Arr(0, 0.0)  # Stochastic Momentum Index (graphic plot #0)
SignalBuffer = Arr(0, 0.0)  # Signal Line: ul-period EMA of Stochastic Momentum Index (graphic plot #1)
PriceBuffer = Arr(0, 0.0)  # price array
LLBuffer = Arr(0, 0.0)  # lowest price (q bars)
HHBuffer = Arr(0, 0.0)  # highest price (q bars)
SMBuffer = Arr(0, 0.0)  # q-period of Stochastic Momentum
EMA_SMBuffer = Arr(0, 0.0)  # r-period of the 1st EMA
DEMA_SMBuffer = Arr(0, 0.0)  # s-period of the 2nd EMA
TEMA_SMBuffer = Arr(0, 0.0)  # u-period of the 3rd EMA
HalfHHLLBuffer = Arr(0, 0.0)  # half of the price range (q bars)
EMA_HalfHHLLBuffer = Arr(0, 0.0)  # r-period of the 1st EMA (half of the price range)
DEMA_HalfHHLLBuffer = Arr(0, 0.0)  # s-period of the 2nd EMA (half of the price range)
TEMA_HalfHHLLBuffer = Arr(0, 0.0)  # u-period of the 3rd EMA (half of the price range)
begin1 = 0  # starting index
begin2 = 0  # starting index
begin3 = 0  # starting index
begin4 = 0  # starting index
begin5 = 0  # starting index
rates_total_min = 0  # rates total min

def OnInit():
    global begin1, begin2, begin3, begin4, begin5, rates_total_min
    SetIndexBuffer(0, MainBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, PriceBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, LLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, HHBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, SMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, EMA_SMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, DEMA_SMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, TEMA_SMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, HalfHHLLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, EMA_HalfHHLLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, DEMA_HalfHHLLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, TEMA_HalfHHLLBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    begin1 = q - 1
    begin2 = begin1 + r - 1
    begin3 = begin2 + s - 1
    begin4 = begin3 + u - 1
    begin5 = begin4 + ul - 1
    rates_total_min = begin5 + 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin4)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, begin5)
    shortname = PriceName(AppliedPrice) + ',' + _str(q) + ',' + _str(r) + ',' + _str(s) + ',' + _str(u) + ',' + _str(ul)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Blau_SM_Stoch(' + shortname + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    k = 0
    pos = 0
    min_ = 0.0
    max_ = 0.0
    value1 = 0.0
    value2 = 0.0
    if rates_total < rates_total_min:
        return 0
    CalculatePriceBuffer(AppliedPrice, rates_total, prev_calculated, Open, High, Low, Close, PriceBuffer)
    if prev_calculated == 0:
        pos = begin1
        i = 0
        for i in range(i, pos):
            SMBuffer[i] = 0.0
            HalfHHLLBuffer[i] = 0.0
            LLBuffer[i] = 0.0
            HHBuffer[i] = 0.0
        else:
            i = _range_end(i, pos, 1)
    else:
        pos = prev_calculated - 1
    i = pos
    for i in range(i, rates_total):
        min_ = 1000000.0
        max_ = -1000000.0
        k = i - (q - 1)
        for k in range(k, i + 1):
            if min_ > Low[k]:
                min_ = Low[k]
            if max_ < High[k]:
                max_ = High[k]
        else:
            k = _range_end(k, i + 1, 1)
        LLBuffer[i] = min_
        HHBuffer[i] = max_
        SMBuffer[i] = PriceBuffer[i] - (0.5 * (LLBuffer[i] + HHBuffer[i]))
        HalfHHLLBuffer[i] = 0.5 * (HHBuffer[i] - LLBuffer[i])
    else:
        i = _range_end(i, rates_total, 1)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin1, r, SMBuffer, EMA_SMBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin1, r, HalfHHLLBuffer, EMA_HalfHHLLBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin2, s, EMA_SMBuffer, DEMA_SMBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin2, s, EMA_HalfHHLLBuffer, DEMA_HalfHHLLBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin3, u, DEMA_SMBuffer, TEMA_SMBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin3, u, DEMA_HalfHHLLBuffer, TEMA_HalfHHLLBuffer)
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
        value1 = 100 * TEMA_SMBuffer[i]
        value2 = TEMA_HalfHHLLBuffer[i]
        MainBuffer[i] = (_fdiv(value1, value2) if (value2 > 0) else 0)
    else:
        i = _range_end(i, rates_total, 1)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin4, ul, MainBuffer, SignalBuffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BlauSmStochastic(_MQL5Indicator):
    name = 'blau_sm_stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'q': 5,  # q - period of Stochastic Momentum
        'r': 20,  # r - 1st EMA, applied to Stochastic Momentum
        's': 5,  # s - 2nd EMA, applied to the 1st smoothing
        'u': 3,  # u - 3rd EMA, applied to the 2nd smoothing
        'ul': 3,  # ul - period of a Signal Line
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # AppliedPrice - price type
    }
    y_range = (-100.0, 100.0)

