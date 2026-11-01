"""blautsstochastic — converted from MQL5: MQL5 Indicators/BlauTSStochastic_HTF/blautsstochastic.mq5

 William Blau's stochastic oscillator
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 10}, 'colors': {1: [65280, 255], 2: [36095, 15631086, 8421504, 3329434, 32768]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'Blau TS Stochastic Signal', 2: 'Blau TS Stochastic'}, 'levels': [30.0, 0.0, -30.0], 'description': [" William Blau's stochastic oscillator"], 'name': 'blautsstochastic', 'source': 'MQL5 Indicators/BlauTSStochastic_HTF/blautsstochastic.mq5', 'folder': 'BlauTSStochastic_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'Averaging method', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 5, 'label': 'Period of Stochastic momentum', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 20, 'label': 'Depth of the first averaging', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'uint', 'default': 5, 'label': 'Depth of the second averaging', 'sinput': False}, {'mql': 'XLength3', 'py': 'XLength3', 'param': 'XLength3', 'type': 'uint', 'default': 3, 'label': 'Depth of the third averaging', 'sinput': False}, {'mql': 'XLength4', 'py': 'XLength4', 'param': 'XLength4', 'type': 'uint', 'default': 3, 'label': 'Signal line averaging depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_EMA)  # Averaging method
XLength = _input('XLength', 5)  # Period of Stochastic momentum
XLength1 = _input('XLength1', 20)  # Depth of the first averaging
XLength2 = _input('XLength2', 5)  # Depth of the second averaging
XLength3 = _input('XLength3', 3)  # Depth of the third averaging
XLength4 = _input('XLength4', 3)  # Signal line averaging depth
XPhase = _input('XPhase', 15)  # Smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
Count = Arr(0, 0)
iHigh_v = Arr(0, 0.0)
iLow_v = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0
min_rates_4 = 0

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global min_rates_1, min_rates_2, min_rates_3, min_rates_4, min_rates_total
    min_rates_1 = _int(XLength)
    min_rates_2 = min_rates_1 + XMA1.GetStartBars(XMA_Method, XLength1, XPhase)
    min_rates_3 = min_rates_2 + XMA1.GetStartBars(XMA_Method, XLength2, XPhase)
    min_rates_4 = min_rates_3 + XMA1.GetStartBars(XMA_Method, XLength3, XPhase)
    min_rates_total = min_rates_4 + XMA1.GetStartBars(XMA_Method, XLength4, XPhase)
    ArrayResize(Count, XLength)
    ArrayResize(iHigh_v, XLength)
    ArrayResize(iLow_v, XLength)
    ArrayInitialize(Count, 0)
    ArrayInitialize(iHigh_v, 0.0)
    ArrayInitialize(iLow_v, 999999999.9)
    ArraySetAsSeries(iHigh_v, True)
    ArraySetAsSeries(iLow_v, True)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BlauTSStochastic')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    LL = 0.0
    HH = 0.0
    price = 0.0
    Stoch = 0.0
    xStoch = 0.0
    xxStoch = 0.0
    xxxStoch = 0.0
    Range = 0.0
    xRange = 0.0
    xxRange = 0.0
    xxxRange = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        iLow_v[Count[0]] = low[bar]
        iHigh_v[Count[0]] = high[bar]
        LL = iLow_v[ArrayMinimum(iLow_v, 0, XLength)]
        HH = iHigh_v[ArrayMaximum(iHigh_v, 0, XLength)]
        price = PriceSeries(IPC, bar, open, low, high, close)
        Stoch = price - LL
        xStoch = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, Stoch, bar, False)
        xxStoch = XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, xStoch, bar, False)
        xxxStoch = XMA3.XMASeries(min_rates_3, prev_calculated, rates_total, XMA_Method, XPhase, XLength3, xxStoch, bar, False)
        Range = HH - LL
        xRange = XMA4.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, Range, bar, False)
        xxRange = XMA5.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, xRange, bar, False)
        xxxRange = XMA6.XMASeries(min_rates_3, prev_calculated, rates_total, XMA_Method, XPhase, XLength3, xxRange, bar, False)
        if xxxRange:
            IndBuffer[bar] = _fdiv(200 * xxxStoch, xxxRange) - 100
        else:
            IndBuffer[bar] = 0.0
        UpBuffer[bar] = IndBuffer[bar]
        DnBuffer[bar] = XMA7.XMASeries(min_rates_4, prev_calculated, rates_total, XMA_Method, XPhase, XLength3, IndBuffer[bar], bar, False)
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, XLength)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 4
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 3
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 0
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()
XMA4 = _alloc(CXMA)
XMA4.__init__()
XMA5 = _alloc(CXMA)
XMA5.__init__()
XMA6 = _alloc(CXMA)
XMA6.__init__()
XMA7 = _alloc(CXMA)
XMA7.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Blautsstochastic(_MQL5Indicator):
    name = 'blautsstochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Averaging method
        'XLength': 5,  # Period of Stochastic momentum
        'XLength1': 20,  # Depth of the first averaging
        'XLength2': 5,  # Depth of the second averaging
        'XLength3': 3,  # Depth of the third averaging
        'XLength4': 3,  # Signal line averaging depth
        'XPhase': 15,  # Smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Price constant
    }

