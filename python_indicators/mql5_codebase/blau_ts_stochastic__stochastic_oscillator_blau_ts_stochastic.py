"""blau_ts_stochastic — converted from MQL5: MQL5 Indicators/Stochastic Oscillator Blau_TS_Stochastic/blau_ts_stochastic.mq5

Stochastic Oscillator (William Blau)
Copyright: Copyright 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.williamblau import *  # #include williamblau.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 13, 'indicator_plots': 2, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 3, 2: 1}, 'colors': {1: [12632256], 2: [255]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: '%k', 2: '%d,Signal'}, 'levels': [40.0, 60.0], 'description': ['Stochastic Oscillator (William Blau)'], 'name': 'blau_ts_stochastic', 'source': 'MQL5 Indicators/Stochastic Oscillator Blau_TS_Stochastic/blau_ts_stochastic.mq5', 'folder': 'Stochastic Oscillator Blau_TS_Stochastic', 'inputs': [{'mql': 'q', 'py': 'q', 'param': 'q', 'type': 'int', 'default': 5, 'label': 'q - period of Stochastic', 'sinput': False}, {'mql': 'r', 'py': 'r', 'param': 'r', 'type': 'int', 'default': 20, 'label': 'r - 1st EMA, applied to Stochastic', 'sinput': False}, {'mql': 's', 'py': 's', 'param': 's', 'type': 'int', 'default': 5, 'label': 's - 2nd EMA, applied to the 1st smoothing', 'sinput': False}, {'mql': 'u', 'py': 'u', 'param': 'u', 'type': 'int', 'default': 3, 'label': 'u - 3rd EMA, applied to the 2nd smoothing', 'sinput': False}, {'mql': 'ul', 'py': 'ul', 'param': 'ul', 'type': 'int', 'default': 3, 'label': 'ul - period of a Signal Line', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'AppliedPrice - price type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['williamblau.mqh']}

# ---- inputs and global variables
q = _input('q', 5)  # q - period of Stochastic
r = _input('r', 20)  # r - 1st EMA, applied to Stochastic
s = _input('s', 5)  # s - 2nd EMA, applied to the 1st smoothing
u = _input('u', 3)  # u - 3rd EMA, applied to the 2nd smoothing
ul = _input('ul', 3)  # ul - period of a Signal Line
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)  # AppliedPrice - price type
MainBuffer = Arr(0, 0.0)  # fast Stochastic (graphic plot #0)
SignalBuffer = Arr(0, 0.0)  # slow Stochastic: ul-period EMA of the fast stochastic (graphic plot #1)
PriceBuffer = Arr(0, 0.0)  # price array
LLBuffer = Arr(0, 0.0)  # minimal value (q bars)
HHBuffer = Arr(0, 0.0)  # maximal value (q bars)
StochBuffer = Arr(0, 0.0)  # q-period Stochastic
EMA_StochBuffer = Arr(0, 0.0)  # r-period of the 1st EMA
DEMA_StochBuffer = Arr(0, 0.0)  # s-period of the 2nd EMA
TEMA_StochBuffer = Arr(0, 0.0)  # u-period of the 3rd EMA
HHLLBuffer = Arr(0, 0.0)  # q-period of price range
EMA_HHLLBuffer = Arr(0, 0.0)  # r-period of the 1st EMA (price range)
DEMA_HHLLBuffer = Arr(0, 0.0)  # s-period of the 2nd EMA (price range)
TEMA_HHLLBuffer = Arr(0, 0.0)  # u-period of the 3rd EMA (price range)
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
    SetIndexBuffer(5, StochBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, EMA_StochBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, DEMA_StochBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, TEMA_StochBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, HHLLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, EMA_HHLLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, DEMA_HHLLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, TEMA_HHLLBuffer, INDICATOR_CALCULATIONS)
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
    IndicatorSetString(INDICATOR_SHORTNAME, 'Blau_TS_Stoch(' + shortname + ')')
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
            StochBuffer[i] = 0.0
            HHLLBuffer[i] = 0.0
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
        StochBuffer[i] = PriceBuffer[i] - LLBuffer[i]
        HHLLBuffer[i] = HHBuffer[i] - LLBuffer[i]
    else:
        i = _range_end(i, rates_total, 1)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin1, r, StochBuffer, EMA_StochBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin1, r, HHLLBuffer, EMA_HHLLBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin2, s, EMA_StochBuffer, DEMA_StochBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin2, s, EMA_HHLLBuffer, DEMA_HHLLBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin3, u, DEMA_StochBuffer, TEMA_StochBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin3, u, DEMA_HHLLBuffer, TEMA_HHLLBuffer)
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
        value1 = 100 * TEMA_StochBuffer[i]
        value2 = TEMA_HHLLBuffer[i]
        MainBuffer[i] = (_fdiv(value1, value2) if (value2 > 0) else 0)
    else:
        i = _range_end(i, rates_total, 1)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin4, ul, MainBuffer, SignalBuffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BlauTsStochastic(_MQL5Indicator):
    name = 'blau_ts_stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'q': 5,  # q - period of Stochastic
        'r': 20,  # r - 1st EMA, applied to Stochastic
        's': 5,  # s - 2nd EMA, applied to the 1st smoothing
        'u': 3,  # u - 3rd EMA, applied to the 2nd smoothing
        'ul': 3,  # ul - period of a Signal Line
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # AppliedPrice - price type
    }
    y_range = (0.0, 100.0)

