"""blau_ergodic_mdi — converted from MQL5: MQL5 Indicators/Ergodic Mean Deviation Index Oscillator Ergodic_MDI/blau_ergodic_mdi.mq5

Ergodic MDI-Oscillator (William Blau)
Copyright: Copyright 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.williamblau import *  # #include williamblau.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 3, 2: 1}, 'colors': {1: [12632256], 2: [255]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Ergodic', 2: 'Signal'}, 'levels': [], 'description': ['Ergodic MDI-Oscillator (William Blau)'], 'name': 'blau_ergodic_mdi', 'source': 'MQL5 Indicators/Ergodic Mean Deviation Index Oscillator Ergodic_MDI/blau_ergodic_mdi.mq5', 'folder': 'Ergodic Mean Deviation Index Oscillator Ergodic_MDI', 'inputs': [{'mql': 'r', 'py': 'r', 'param': 'r', 'type': 'int', 'default': 20, 'label': 'r - 1st EMA, applied to price', 'sinput': False}, {'mql': 's', 'py': 's', 'param': 's', 'type': 'int', 'default': 5, 'label': 's - 2nd EMA, applied to standard deviation', 'sinput': False}, {'mql': 'u', 'py': 'u', 'param': 'u', 'type': 'int', 'default': 3, 'label': 'u - 3rd EMA, applied to 2nd smoothing', 'sinput': False}, {'mql': 'ul', 'py': 'ul', 'param': 'ul', 'type': 'int', 'default': 3, 'label': 'ul - period of a Signal Line', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'AppliedPrice - price type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['williamblau.mqh']}

# ---- inputs and global variables
r = _input('r', 20)  # r - 1st EMA, applied to price
s = _input('s', 5)  # s - 2nd EMA, applied to standard deviation
u = _input('u', 3)  # u - 3rd EMA, applied to 2nd smoothing
ul = _input('ul', 3)  # ul - period of a Signal Line
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)  # AppliedPrice - price type
MainBuffer = Arr(0, 0.0)  # Ergodic: u-period 3rd EMA (graphic plot #0)
SignalBuffer = Arr(0, 0.0)  # Signal Line: ul-period EMA of Ergodic (graphic plot #1)
PriceBuffer = Arr(0, 0.0)  # price buffer
EMA_PriceBuffer = Arr(0, 0.0)  # r-period 1st EMA (price)
MDBuffer = Arr(0, 0.0)  # average deviation
DEMA_MDBuffer = Arr(0, 0.0)  # s-period 2dn EMA
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
    SetIndexBuffer(3, EMA_PriceBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, MDBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, DEMA_MDBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    begin1 = 0
    begin2 = begin1 + r - 1
    begin3 = begin2 + s - 1
    begin4 = begin3 + u - 1
    begin5 = begin4 + ul - 1
    rates_total_min = begin5 + 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin4)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, begin5)
    shortname = PriceName(AppliedPrice) + ',' + _str(r) + ',' + _str(s) + ',' + _str(u) + ',' + _str(ul)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Blau_Ergodic_MDI(' + shortname + ')')
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
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin4, ul, MainBuffer, SignalBuffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BlauErgodicMdi(_MQL5Indicator):
    name = 'blau_ergodic_mdi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'r': 20,  # r - 1st EMA, applied to price
        's': 5,  # s - 2nd EMA, applied to standard deviation
        'u': 3,  # u - 3rd EMA, applied to 2nd smoothing
        'ul': 3,  # ul - period of a Signal Line
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # AppliedPrice - price type
    }

