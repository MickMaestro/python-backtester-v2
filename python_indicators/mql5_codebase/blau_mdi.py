"""blau_mdi — converted from MQL5: MQL5 Indicators/Mean Deviation Index Blau_MDI/blau_mdi.mq5

Mean Deviation Index (William Blau)
Copyright: Copyright 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.williamblau import *  # #include williamblau.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'MDI'}, 'levels': [], 'description': ['Mean Deviation Index (William Blau)'], 'name': 'blau_mdi', 'source': 'MQL5 Indicators/Mean Deviation Index Blau_MDI/blau_mdi.mq5', 'folder': 'Mean Deviation Index Blau_MDI', 'inputs': [{'mql': 'r', 'py': 'r', 'param': 'r', 'type': 'int', 'default': 20, 'label': 'r - 1st EMA, applied to price', 'sinput': False}, {'mql': 's', 'py': 's', 'param': 's', 'type': 'int', 'default': 5, 'label': 's - 2nd EMA, applied to average deviation', 'sinput': False}, {'mql': 'u', 'py': 'u', 'param': 'u', 'type': 'int', 'default': 3, 'label': 'u - 3rd EMA, applied to the 2nd smoothing', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'AppliedPrice - price type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['williamblau.mqh']}

# ---- inputs and global variables
r = _input('r', 20)  # r - 1st EMA, applied to price
s = _input('s', 5)  # s - 2nd EMA, applied to average deviation
u = _input('u', 3)  # u - 3rd EMA, applied to the 2nd smoothing
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)  # AppliedPrice - price type
MainBuffer = Arr(0, 0.0)  # u-period 3rd EMA (graphic plot #0)
PriceBuffer = Arr(0, 0.0)  # price array
EMA_PriceBuffer = Arr(0, 0.0)  # r-period 1st EMA (price)
MDBuffer = Arr(0, 0.0)  # average deviation
DEMA_MDBuffer = Arr(0, 0.0)  # s-period 2nd EMA
begin1 = 0  # starting index
begin2 = 0  # starting index
begin3 = 0  # starting index
begin4 = 0  # starting index
rates_total_min = 0  # rates total min

def OnInit():
    global begin1, begin2, begin3, begin4, rates_total_min
    SetIndexBuffer(0, MainBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, PriceBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, EMA_PriceBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, MDBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, DEMA_MDBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    begin1 = 0
    begin2 = begin1 + r - 1
    begin3 = begin2 + s - 1
    begin4 = begin3 + u - 1
    rates_total_min = begin4 + 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin4)
    shortname = PriceName(AppliedPrice) + ',' + _str(r) + ',' + _str(s) + ',' + _str(u)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Blau_MDI(' + shortname + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    pos = 0
    if rates_total < rates_total_min:
        return 0
    CalculatePriceBuffer(AppliedPrice, rates_total, prev_calculated, Open, High, Low, Close, PriceBuffer)
    if prev_calculated == 0:
        pos = begin2
        i = 0
        for i in range(i, pos):
            MDBuffer[i] = 0.0
        else:
            i = _range_end(i, pos, 1)
    else:
        pos = prev_calculated - 1
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin1, r, PriceBuffer, EMA_PriceBuffer)
    i = pos
    for i in range(i, rates_total):
        MDBuffer[i] = PriceBuffer[i] - EMA_PriceBuffer[i]
    else:
        i = _range_end(i, rates_total, 1)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin2, s, MDBuffer, DEMA_MDBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin3, u, DEMA_MDBuffer, MainBuffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BlauMdi(_MQL5Indicator):
    name = 'blau_mdi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'r': 20,  # r - 1st EMA, applied to price
        's': 5,  # s - 2nd EMA, applied to average deviation
        'u': 3,  # u - 3rd EMA, applied to the 2nd smoothing
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # AppliedPrice - price type
    }

