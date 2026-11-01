"""blau_tsi — converted from MQL5: MQL5 Indicators/Blau_TSI/blau_tsi.mq5

True Strength Index (William Blau)
Copyright: Copyright 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.williamblau import *  # #include williamblau.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 1, 'indicator_minimum': -100.0, 'indicator_maximum': 100.0}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TSI'}, 'levels': [-25.0, 25.0], 'description': ['True Strength Index (William Blau)'], 'name': 'blau_tsi', 'source': 'MQL5 Indicators/Blau_TSI/blau_tsi.mq5', 'folder': 'Blau_TSI', 'inputs': [{'mql': 'q', 'py': 'q', 'param': 'q', 'type': 'int', 'default': 2, 'label': 'q - period of Momentum', 'sinput': False}, {'mql': 'r', 'py': 'r', 'param': 'r', 'type': 'int', 'default': 20, 'label': 'r - 1st EMA, applied to Momentum', 'sinput': False}, {'mql': 's', 'py': 's', 'param': 's', 'type': 'int', 'default': 5, 'label': 's - 2nd EMA, applied to the 1st smoothing', 'sinput': False}, {'mql': 'u', 'py': 'u', 'param': 'u', 'type': 'int', 'default': 3, 'label': 'u - 3rd EMA, applied to the 2nd smoothing', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'AppliedPrice - price type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['williamblau.mqh']}

# ---- inputs and global variables
q = _input('q', 2)  # q - period of Momentum
r = _input('r', 20)  # r - 1st EMA, applied to Momentum
s = _input('s', 5)  # s - 2nd EMA, applied to the 1st smoothing
u = _input('u', 3)  # u - 3rd EMA, applied to the 2nd smoothing
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)  # AppliedPrice - price type
MainBuffer = Arr(0, 0.0)  # TSI (graphic plot #0)
PriceBuffer = Arr(0, 0.0)  # price array
MtmBuffer = Arr(0, 0.0)  # q-period Momentum
EMA_MtmBuffer = Arr(0, 0.0)  # r-period 1st EMA
DEMA_MtmBuffer = Arr(0, 0.0)  # s-period 2nd EMA
TEMA_MtmBuffer = Arr(0, 0.0)  # u-period 3rd EMA
AbsMtmBuffer = Arr(0, 0.0)  # q-period Momentum (absolute value)
EMA_AbsMtmBuffer = Arr(0, 0.0)  # r-period 1st EMA (absolute value)
DEMA_AbsMtmBuffer = Arr(0, 0.0)  # s-period 2nd EMA (absolute value)
TEMA_AbsMtmBuffer = Arr(0, 0.0)  # u-period 3rd EMA (absolute value)
begin1 = 0  # starting index
begin2 = 0  # starting index
begin3 = 0  # starting index
begin4 = 0  # starting index
rates_total_min = 0  # rates total min

def OnInit():
    global begin1, begin2, begin3, begin4, rates_total_min
    SetIndexBuffer(0, MainBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, PriceBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, MtmBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, EMA_MtmBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, DEMA_MtmBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, TEMA_MtmBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, AbsMtmBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, EMA_AbsMtmBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, DEMA_AbsMtmBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, TEMA_AbsMtmBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    begin1 = q - 1
    begin2 = begin1 + r - 1
    begin3 = begin2 + s - 1
    begin4 = begin3 + u - 1
    rates_total_min = begin4 + 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin4)
    shortname = PriceName(AppliedPrice) + ',' + _str(q) + ',' + _str(r) + ',' + _str(s) + ',' + _str(u)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Blau_TSI(' + shortname + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    pos = 0
    value1 = 0.0
    value2 = 0.0
    if rates_total < rates_total_min:
        return 0
    CalculatePriceBuffer(AppliedPrice, rates_total, prev_calculated, Open, High, Low, Close, PriceBuffer)
    if prev_calculated == 0:
        pos = begin1
        i = 0
        for i in range(i, pos):
            MtmBuffer[i] = 0.0
            AbsMtmBuffer[i] = 0.0
        else:
            i = _range_end(i, pos, 1)
    else:
        pos = prev_calculated - 1
    i = pos
    for i in range(i, rates_total):
        MtmBuffer[i] = PriceBuffer[i] - PriceBuffer[i - (q - 1)]
        AbsMtmBuffer[i] = MathAbs(MtmBuffer[i])
    else:
        i = _range_end(i, rates_total, 1)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin1, r, MtmBuffer, EMA_MtmBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin1, r, AbsMtmBuffer, EMA_AbsMtmBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin2, s, EMA_MtmBuffer, DEMA_MtmBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin2, s, EMA_AbsMtmBuffer, DEMA_AbsMtmBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin3, u, DEMA_MtmBuffer, TEMA_MtmBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin3, u, DEMA_AbsMtmBuffer, TEMA_AbsMtmBuffer)
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
        value1 = 100 * TEMA_MtmBuffer[i]
        value2 = TEMA_AbsMtmBuffer[i]
        MainBuffer[i] = (_fdiv(value1, value2) if (value2 > 0) else 0)
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BlauTsi(_MQL5Indicator):
    name = 'blau_tsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'q': 2,  # q - period of Momentum
        'r': 20,  # r - 1st EMA, applied to Momentum
        's': 5,  # s - 2nd EMA, applied to the 1st smoothing
        'u': 3,  # u - 3rd EMA, applied to the 2nd smoothing
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # AppliedPrice - price type
    }
    y_range = (-100.0, 100.0)

