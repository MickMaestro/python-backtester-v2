"""accelerator_signal — converted from MQL5: MQL5 Indicators/Accelerator_Signal/accelerator_signal.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 10}, 'colors': {1: [16760576, 16711935], 2: [9639167, 42495, 8421504, 3329330, 8421376]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'Accelerator Signal', 2: 'Accelerator'}, 'levels': [], 'description': [], 'name': 'accelerator_signal', 'source': 'MQL5 Indicators/Accelerator_Signal/accelerator_signal.mq5', 'folder': 'Accelerator_Signal', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Method of averaging of the Accelerator histogram', 'sinput': False}, {'mql': 'Fast_XMA', 'py': 'Fast_XMA', 'param': 'Fast_XMA', 'type': 'int', 'default': 5, 'label': 'Period of the fast MA', 'sinput': False}, {'mql': 'Slow_XMA', 'py': 'Slow_XMA', 'param': 'Slow_XMA', 'type': 'int', 'default': 34, 'label': 'Period of the slow MA', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'MA averaging parameter', 'sinput': False}, {'mql': 'Sm_Method', 'py': 'Sm_Method', 'param': 'Sm_Method', 'type': 'int', 'default': 0, 'label': 'Method of averaging of the Accelerator histogram', 'sinput': False}, {'mql': 'Sm_XMA', 'py': 'Sm_XMA', 'param': 'Sm_XMA', 'type': 'int', 'default': 5, 'label': 'Signal line period', 'sinput': False}, {'mql': 'Sm_Phase', 'py': 'Sm_Phase', 'param': 'Sm_Phase', 'type': 'int', 'default': 100, 'label': 'Signal line parameter', 'sinput': False}, {'mql': 'Signal_Method', 'py': 'Signal_Method', 'param': 'Signal_Method', 'type': 'int', 'default': 0, 'label': 'Signal line averaging method', 'sinput': False}, {'mql': 'Signal_XMA', 'py': 'Signal_XMA', 'param': 'Signal_XMA', 'type': 'int', 'default': 5, 'label': 'Period of the signal line', 'sinput': False}, {'mql': 'Signal_Phase', 'py': 'Signal_Phase', 'param': 'Signal_Phase', 'type': 'int', 'default': 100, 'label': 'Parameter of the signal line', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_SMA)  # Method of averaging of the Accelerator histogram
Fast_XMA = _input('Fast_XMA', 5)  # Period of the fast MA
Slow_XMA = _input('Slow_XMA', 34)  # Period of the slow MA
XPhase = _input('XPhase', 100)  # MA averaging parameter
Sm_Method = _input('Sm_Method', MODE_SMA)  # Method of averaging of the Accelerator histogram
Sm_XMA = _input('Sm_XMA', 5)  # Signal line period
Sm_Phase = _input('Sm_Phase', 100)  # Signal line parameter
Signal_Method = _input('Signal_Method', MODE_SMA)  # Signal line averaging method
Signal_XMA = _input('Signal_XMA', 5)  # Period of the signal line
Signal_Phase = _input('Signal_Phase', 100)  # Parameter of the signal line
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)  # Price constant
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpSignBuffer = Arr(0, 0.0)
DnSignBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = MathMax(XMA1.GetStartBars(XMA_Method, Fast_XMA, XPhase), XMA1.GetStartBars(XMA_Method, Slow_XMA, XPhase))
    min_rates_2 = min_rates_1 + XMA1.GetStartBars(Sm_Method, Sm_XMA, Sm_Phase)
    min_rates_total = min_rates_2 + XMA1.GetStartBars(Signal_Method, Signal_XMA, Signal_Phase) + 2
    SetIndexBuffer(0, UpSignBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnSignBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    XMA1.XMALengthCheck('Fast_XMA', Fast_XMA)
    XMA1.XMALengthCheck('Slow_XMA', Slow_XMA)
    XMA1.XMALengthCheck('Sm_XMA', Sm_XMA)
    XMA1.XMALengthCheck('Signal_XMA', Signal_XMA)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    XMA1.XMAPhaseCheck('Sm_Phase', Sm_Phase, Sm_Method)
    XMA1.XMAPhaseCheck('Signal_Phase', Signal_Phase, Signal_Method)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    Smooth2 = XMA1.GetString_MA_Method(Signal_Method)
    StringConcatenate(shortname, 'Accelerator( ', Fast_XMA, ', ', Slow_XMA, ', ', Sm_XMA, ', ', Signal_XMA, ', ', Smooth1, ', ', Smooth2, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first1 = 0
    first2 = 0
    bar = 0
    price_ = 0.0
    fast_xma = 0.0
    slow_xma = 0.0
    xmacd = 0.0
    sign_xma = 0.0
    accel = 0.0
    xaccel = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = 0
        first2 = min_rates_1 + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
    bar = first1
    for bar in range(bar, rates_total):
        price_ = PriceSeries(AppliedPrice, bar, open, low, high, close)
        fast_xma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Fast_XMA, price_, bar, False)
        slow_xma = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Slow_XMA, price_, bar, False)
        xmacd = _fdiv(fast_xma - slow_xma, Point())
        sign_xma = XMA3.XMASeries(min_rates_1, prev_calculated, rates_total, Sm_Method, Sm_Phase, Sm_XMA, xmacd, bar, False)
        accel = xmacd - sign_xma
        xaccel = XMA4.XMASeries(min_rates_2, prev_calculated, rates_total, Signal_Method, Signal_Phase, Signal_XMA, accel, bar, False)
        IndBuffer[bar] = accel
        UpSignBuffer[bar] = accel
        DnSignBuffer[bar] = xaccel
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AcceleratorSignal(_MQL5Indicator):
    name = 'accelerator_signal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Method of averaging of the Accelerator histogram
        'Fast_XMA': 5,  # Period of the fast MA
        'Slow_XMA': 34,  # Period of the slow MA
        'XPhase': 100,  # MA averaging parameter
        'Sm_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Method of averaging of the Accelerator histogram
        'Sm_XMA': 5,  # Signal line period
        'Sm_Phase': 100,  # Signal line parameter
        'Signal_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Signal line averaging method
        'Signal_XMA': 5,  # Period of the signal line
        'Signal_Phase': 100,  # Parameter of the signal line
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Price constant
    }

