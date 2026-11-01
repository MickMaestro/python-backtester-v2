"""blau_ergodic_csi — converted from MQL5: MQL5 Indicators/Ergodic CSI-Oscillator Blau_Ergodic_CSI/blau_ergodic_csi.mq5

Ergodic CSI-Oscillator (William Blau)
Copyright: Copyright 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.williamblau import *  # #include williamblau.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 14, 'indicator_plots': 2, 'indicator_minimum': -100.0, 'indicator_maximum': 100.0}, 'types': {1: 3, 2: 1}, 'colors': {1: [12632256], 2: [255]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Ergodic', 2: 'Signal'}, 'levels': [-25.0, 25.0], 'description': ['Ergodic CSI-Oscillator (William Blau)'], 'name': 'blau_ergodic_csi', 'source': 'MQL5 Indicators/Ergodic CSI-Oscillator Blau_Ergodic_CSI/blau_ergodic_csi.mq5', 'folder': 'Ergodic CSI-Oscillator Blau_Ergodic_CSI', 'inputs': [{'mql': 'q', 'py': 'q', 'param': 'q', 'type': 'int', 'default': 1, 'label': 'q - period of Candlestick Momentum', 'sinput': False}, {'mql': 'r', 'py': 'r', 'param': 'r', 'type': 'int', 'default': 20, 'label': 'r - 1st EMA, applied to Candlestick Momentum', 'sinput': False}, {'mql': 's', 'py': 's', 'param': 's', 'type': 'int', 'default': 5, 'label': 's - 2nd EMA, applied to the 1st smoothing', 'sinput': False}, {'mql': 'u', 'py': 'u', 'param': 'u', 'type': 'int', 'default': 3, 'label': 'u - 3rd EMA, applied to the 2nd smoothing', 'sinput': False}, {'mql': 'ul', 'py': 'ul', 'param': 'ul', 'type': 'int', 'default': 3, 'label': 'ul - period of a Signal Line', 'sinput': False}, {'mql': 'AppliedPrice1', 'py': 'AppliedPrice1', 'param': 'AppliedPrice1', 'type': 'int', 'default': 1, 'label': 'AppliedPrice1 - price type [close]', 'sinput': False}, {'mql': 'AppliedPrice2', 'py': 'AppliedPrice2', 'param': 'AppliedPrice2', 'type': 'int', 'default': 2, 'label': 'AppliedPrice2 - price type [open]', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['williamblau.mqh']}

# ---- inputs and global variables
q = _input('q', 1)  # q - period of Candlestick Momentum
r = _input('r', 20)  # r - 1st EMA, applied to Candlestick Momentum
s = _input('s', 5)  # s - 2nd EMA, applied to the 1st smoothing
u = _input('u', 3)  # u - 3rd EMA, applied to the 2nd smoothing
ul = _input('ul', 3)  # ul - period of a Signal Line
AppliedPrice1 = _input('AppliedPrice1', PRICE_CLOSE)  # AppliedPrice1 - price type [close]
AppliedPrice2 = _input('AppliedPrice2', PRICE_OPEN)  # AppliedPrice2 - price type [open]
MainBuffer = Arr(0, 0.0)  # Ergodic (graphic plot #0)
SignalBuffer = Arr(0, 0.0)  # Signal Line: EMA(ul), applied to Ergodic (graphic plot #1)
Price1Buffer = Arr(0, 0.0)  # price array [close]
Price2Buffer = Arr(0, 0.0)  # price array [open]
LLBuffer = Arr(0, 0.0)  # lowest prices (q bars)
HHBuffer = Arr(0, 0.0)  # highest prices (q bars)
CMtmBuffer = Arr(0, 0.0)  # q-period Candlestick Momentum
EMA_CMtmBuffer = Arr(0, 0.0)  # r-period 1st EMA
DEMA_CMtmBuffer = Arr(0, 0.0)  # s-period 2nd EMA
TEMA_CMtmBuffer = Arr(0, 0.0)  # u-period 3rd EMA
HHLLBuffer = Arr(0, 0.0)  # Price range (q bars)
EMA_HHLLBuffer = Arr(0, 0.0)  # r-period 1st EMA (price range)
DEMA_HHLLBuffer = Arr(0, 0.0)  # s-period 2nd EMA (price range)
TEMA_HHLLBuffer = Arr(0, 0.0)  # u-period 3rd EMA (price range)
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
    SetIndexBuffer(2, Price1Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, Price2Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, LLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, HHBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, CMtmBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, EMA_CMtmBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, DEMA_CMtmBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, TEMA_CMtmBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, HHLLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, EMA_HHLLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, DEMA_HHLLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, TEMA_HHLLBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    begin1 = q - 1
    begin2 = begin1 + r - 1
    begin3 = begin2 + s - 1
    begin4 = begin3 + u - 1
    begin5 = begin4 + ul - 1
    rates_total_min = begin5 + 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin4)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, begin5)
    shortname = PriceName(AppliedPrice1) + ',' + PriceName(AppliedPrice2) + ',' + _str(q) + ',' + _str(r) + ',' + _str(s) + ',' + _str(u) + ',' + _str(ul)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Blau_Ergodic_CSI(' + shortname + ')')
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
    CalculatePriceBuffer(AppliedPrice1, rates_total, prev_calculated, Open, High, Low, Close, Price1Buffer)
    CalculatePriceBuffer(AppliedPrice2, rates_total, prev_calculated, Open, High, Low, Close, Price2Buffer)
    if prev_calculated == 0:
        pos = begin1
        i = 0
        for i in range(i, pos):
            CMtmBuffer[i] = 0.0
            HHLLBuffer[i] = 0.0
            LLBuffer[i] = 0.0
            HHBuffer[i] = 0.0
        else:
            i = _range_end(i, pos, 1)
    else:
        pos = prev_calculated - 1
    i = pos
    for i in range(i, rates_total):
        CMtmBuffer[i] = Price1Buffer[i] - Price2Buffer[i - (q - 1)]
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
        HHLLBuffer[i] = HHBuffer[i] - LLBuffer[i]
    else:
        i = _range_end(i, rates_total, 1)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin1, r, CMtmBuffer, EMA_CMtmBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin1, r, HHLLBuffer, EMA_HHLLBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin2, s, EMA_CMtmBuffer, DEMA_CMtmBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin2, s, EMA_HHLLBuffer, DEMA_HHLLBuffer)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin3, u, DEMA_CMtmBuffer, TEMA_CMtmBuffer)
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
        value1 = 100 * TEMA_CMtmBuffer[i]
        value2 = TEMA_HHLLBuffer[i]
        MainBuffer[i] = (_fdiv(value1, value2) if (value2 > 0) else 0)
    else:
        i = _range_end(i, rates_total, 1)
    ExponentialMAOnBufferWB(rates_total, prev_calculated, begin4, ul, MainBuffer, SignalBuffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BlauErgodicCsi(_MQL5Indicator):
    name = 'blau_ergodic_csi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'q': 1,  # q - period of Candlestick Momentum
        'r': 20,  # r - 1st EMA, applied to Candlestick Momentum
        's': 5,  # s - 2nd EMA, applied to the 1st smoothing
        'u': 3,  # u - 3rd EMA, applied to the 2nd smoothing
        'ul': 3,  # ul - period of a Signal Line
        'AppliedPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # AppliedPrice1 - price type [close]
        'AppliedPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=2),  # AppliedPrice2 - price type [open]
    }
    y_range = (-100.0, 100.0)

