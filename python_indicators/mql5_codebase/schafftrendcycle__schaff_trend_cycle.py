"""schafftrendcycle — converted from MQL5: MQL5 Indicators/Schaff Trend Cycle/schafftrendcycle.mq5

Schaff Trend Cycle - Cyclical Stoch over Stoch over XMACD.
The code adapted by Nikolay Kositsin.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1, 'indicator_minimum': -10.0, 'indicator_maximum': 110.0}, 'types': {1: 1}, 'colors': {1: [13382297]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Schaff Trend Cycle'}, 'levels': [80.0, 50.0, 20.0], 'description': ['Schaff Trend Cycle - Cyclical Stoch over Stoch over XMACD.', 'The code adapted by Nikolay Kositsin.'], 'name': 'schafftrendcycle', 'source': 'MQL5 Indicators/Schaff Trend Cycle/schafftrendcycle.mq5', 'folder': 'Schaff Trend Cycle', 'inputs': [{'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 1, 'label': 'Histogram smoothing method', 'sinput': False}, {'mql': 'Fast_XMA', 'py': 'Fast_XMA', 'param': 'Fast_XMA', 'type': 'int', 'default': 23, 'label': 'Fast moving average period', 'sinput': False}, {'mql': 'Slow_XMA', 'py': 'Slow_XMA', 'param': 'Slow_XMA', 'type': 'int', 'default': 50, 'label': 'Slow moving average period', 'sinput': False}, {'mql': 'SmPhase', 'py': 'SmPhase', 'param': 'SmPhase', 'type': 'int', 'default': 100, 'label': 'Moving averages smoothing parameter', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Cycle', 'py': 'Cycle', 'param': 'Cycle', 'type': 'int', 'default': 10, 'label': 'Stochastic oscillator period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
MA_SMethod = _input('MA_SMethod', MODE_EMA)  # Histogram smoothing method
Fast_XMA = _input('Fast_XMA', 23)  # Fast moving average period
Slow_XMA = _input('Slow_XMA', 50)  # Slow moving average period
SmPhase = _input('SmPhase', 100)  # Moving averages smoothing parameter
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # Price constant
Cycle = _input('Cycle', 10)  # Stochastic oscillator period
STC_Buffer = Arr(0, 0.0)
Count = Arr(0, 0)
st1_pass = False
st2_pass = False
XMACD = Arr(0, 0.0)
ST = Arr(0, 0.0)
Factor = 0.0
StartBars = 0
StartBars1 = 0
StartBars2 = 0

def Recount_ArrayZeroPos(CoArr, Rates_total, Bar):
    global _s_Recount_ArrayZeroPos_count
    if Bar >= (Rates_total - 1):
        return
    numb = 0
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Cycle - 1
    for iii in range(0, Cycle):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > (Cycle - 1):
            numb -= Cycle
        CoArr[iii] = numb

def OnInit():
    global Factor, StartBars, StartBars1, StartBars2, st1_pass, st2_pass
    StartBars1 = MathMax(XMA1.GetStartBars(MA_SMethod, Fast_XMA, SmPhase), XMA1.GetStartBars(MA_SMethod, Slow_XMA, SmPhase))
    StartBars2 = StartBars1 + Cycle
    StartBars = StartBars2 + Cycle
    if ArrayResize(ST, Cycle) < Cycle:
        Print('Failed to distribute the memory for ST array')
    if ArrayResize(XMACD, Cycle) < Cycle:
        Print('Failed to distribute the memory for XMACD array')
    if ArrayResize(Count, Cycle) < Cycle:
        Print('Failed to distribute the memory for Count array')
    Factor = 0.5
    st1_pass = False
    st2_pass = False
    SetIndexBuffer(0, STC_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(MA_SMethod)
    StringConcatenate(shortname, 'Schaff Trend Cycle( ', Smooth, ', ', Fast_XMA, ', ', Slow_XMA, ', ', Cycle, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    XMA1.XMALengthCheck('Fast_XMA', Fast_XMA)
    XMA1.XMALengthCheck('Slow_XMA', Slow_XMA)
    XMA1.XMAPhaseCheck('Phase', SmPhase, MA_SMethod)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global st1_pass, st2_pass
    if rates_total <= StartBars:
        return 0
    price_ = 0.0
    fastxma = 0.0
    slowxma = 0.0
    LLV = 0.0
    HHV = 0.0
    first = 0
    bar = 0
    Bar0 = 0
    Bar1 = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Bar0 = Count[0]
        Bar1 = Count[1]
        price_ = PriceSeries(AppliedPrice, bar, open, low, high, close)
        fastxma = XMA1.XMASeries(0, prev_calculated, rates_total, MA_SMethod, SmPhase, Fast_XMA, price_, bar, False)
        slowxma = XMA2.XMASeries(0, prev_calculated, rates_total, MA_SMethod, SmPhase, Slow_XMA, price_, bar, False)
        XMACD[Bar0] = fastxma - slowxma
        if bar <= StartBars2:
            Recount_ArrayZeroPos(Count, rates_total, bar)
            continue
        LLV = XMACD[ArrayMinimum(XMACD)]
        HHV = XMACD[ArrayMaximum(XMACD)]
        if (HHV - LLV) != 0:
            ST[Bar0] = _fdiv(XMACD[Bar0] - LLV, HHV - LLV) * 100
        else:
            ST[Bar0] = ST[Bar1]
        if st1_pass:
            ST[Bar0] = (Factor * (ST[Bar0] - ST[Bar1])) + ST[Bar1]
        st1_pass = True
        if bar <= StartBars2:
            Recount_ArrayZeroPos(Count, rates_total, bar)
            continue
        LLV = ST[ArrayMinimum(ST)]
        HHV = ST[ArrayMaximum(ST)]
        if (HHV - LLV) != 0:
            STC_Buffer[bar] = _fdiv(ST[Bar0] - LLV, HHV - LLV) * 100
        else:
            STC_Buffer[bar] = STC_Buffer[bar - 1]
        if st2_pass:
            STC_Buffer[bar] = (Factor * (STC_Buffer[bar] - STC_Buffer[bar - 1])) + STC_Buffer[bar - 1]
        st2_pass = True
        Recount_ArrayZeroPos(Count, rates_total, bar)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Schafftrendcycle(_MQL5Indicator):
    name = 'schafftrendcycle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Histogram smoothing method
        'Fast_XMA': 23,  # Fast moving average period
        'Slow_XMA': 50,  # Slow moving average period
        'SmPhase': 100,  # Moving averages smoothing parameter
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'Cycle': 10,  # Stochastic oscillator period
    }
    y_range = (-10.0, 110.0)

