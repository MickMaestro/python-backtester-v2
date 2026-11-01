"""colorschafftrendcycle — converted from MQL5: MQL5 Indicators/ColorSchaffTrendCycle_HTF/colorschafftrendcycle.mq5

Schaff Trend Cycle - Cyclical Stoch over Stoch over XMACD.
The code adapted Nikolay Kositsin.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': -110.0, 'indicator_maximum': 110.0}, 'types': {1: 10}, 'colors': {1: [16711935, 13850042, 36095, 4163021, 16711680, 16748574, 7451452, 65280]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Schaff Trend Cycle'}, 'levels': [], 'description': ['Schaff Trend Cycle - Cyclical Stoch over Stoch over XMACD.', 'The code adapted Nikolay Kositsin.'], 'name': 'colorschafftrendcycle', 'source': 'MQL5 Indicators/ColorSchaffTrendCycle_HTF/colorschafftrendcycle.mq5', 'folder': 'ColorSchaffTrendCycle_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'Метод усреднения гистограммы', 'sinput': False}, {'mql': 'Fast_XMA', 'py': 'Fast_XMA', 'param': 'Fast_XMA', 'type': 'uint', 'default': 23, 'label': 'Период быстрой скользящей средней', 'sinput': False}, {'mql': 'Slow_XMA', 'py': 'Slow_XMA', 'param': 'Slow_XMA', 'type': 'uint', 'default': 50, 'label': 'Период медленной скользящей средней', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения скользящих средних', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Cycle', 'py': 'Cycle', 'param': 'Cycle', 'type': 'uint', 'default': 10, 'label': 'Период стохастического осциллятора', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 60, 'label': '', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -60, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_EMA)  # Метод усреднения гистограммы
Fast_XMA = _input('Fast_XMA', 23)  # Период быстрой скользящей средней
Slow_XMA = _input('Slow_XMA', 50)  # Период медленной скользящей средней
XPhase = _input('XPhase', 100)  # Параметр усреднения скользящих средних
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # Ценовая константа
Cycle = _input('Cycle', 10)  # Период стохастического осциллятора
HighLevel = _input('HighLevel', 60)
MiddleLevel = _input('MiddleLevel', 0)
LowLevel = _input('LowLevel', -60)
STC_Buffer = Arr(0, 0.0)
ColorSTC_Buffer = Arr(0, 0.0)
Count = Arr(0, 0)
st1_pass = False
st2_pass = False
XMACD = Arr(0, 0.0)
ST = Arr(0, 0.0)
Factor = 0.0
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0

def Recount_ArrayZeroPos(CoArr, Rates_total, Bar):
    global _s_Recount_ArrayZeroPos_count
    if Bar >= (Rates_total - 1):
        return
    numb = 0
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = _int(Cycle) - 1
    for iii in range(0, _int(Cycle)):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > (_int(Cycle) - 1):
            numb -= _int(Cycle)
        CoArr[iii] = numb

def OnInit():
    global Factor, min_rates_1, min_rates_2, min_rates_total, st1_pass, st2_pass
    min_rates_1 = MathMax(XMA1.GetStartBars(XMA_Method, Fast_XMA, XPhase), XMA1.GetStartBars(XMA_Method, Slow_XMA, XPhase))
    min_rates_2 = min_rates_1 + _int(Cycle)
    min_rates_total = min_rates_2 + _int(Cycle) + 1
    if ArrayResize(ST, Cycle) < _int(Cycle):
        Print('Не удалось распределить память под массив ST')
    if ArrayResize(XMACD, Cycle) < _int(Cycle):
        Print('Не удалось распределить память под массив XMACD')
    if ArrayResize(Count, Cycle) < _int(Cycle):
        Print('Не удалось распределить память под массив Count')
    Factor = 0.5
    st1_pass = False
    st2_pass = False
    SetIndexBuffer(0, STC_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorSTC_Buffer, INDICATOR_COLOR_INDEX)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'Schaff Trend Cycle( ', Smooth, ', ', Fast_XMA, ', ', Slow_XMA, ', ', Cycle, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    XMA1.XMALengthCheck('Fast_XMA', Fast_XMA)
    XMA1.XMALengthCheck('Slow_XMA', Slow_XMA)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMediumSeaGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global st1_pass, st2_pass
    if rates_total <= min_rates_total:
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
        fastxma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Fast_XMA, price_, bar, False)
        slowxma = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Slow_XMA, price_, bar, False)
        XMACD[Bar0] = fastxma - slowxma
        if bar <= min_rates_2:
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
        if bar <= min_rates_2:
            Recount_ArrayZeroPos(Count, rates_total, bar)
            continue
        LLV = ST[ArrayMinimum(ST)]
        HHV = ST[ArrayMaximum(ST)]
        if (HHV - LLV) != 0:
            STC_Buffer[bar] = (_fdiv(ST[Bar0] - LLV, HHV - LLV) * 200) - 100
        else:
            STC_Buffer[bar] = STC_Buffer[bar - 1]
        if st2_pass:
            STC_Buffer[bar] = (Factor * (STC_Buffer[bar] - STC_Buffer[bar - 1])) + STC_Buffer[bar - 1]
        st2_pass = True
        Recount_ArrayZeroPos(Count, rates_total, bar)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        Sts = STC_Buffer[bar]
        dSts = Sts - STC_Buffer[bar - 1]
        clr = 4
        if Sts > 0:
            if Sts > HighLevel:
                if dSts >= 0:
                    clr = 7
                else:
                    clr = 6
            else:
                if dSts >= 0:
                    clr = 5
                else:
                    clr = 4
        if Sts < 0:
            if Sts < LowLevel:
                if dSts < 0:
                    clr = 0
                else:
                    clr = 1
            else:
                if dSts < 0:
                    clr = 2
                else:
                    clr = 3
        ColorSTC_Buffer[bar] = clr
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


class Colorschafftrendcycle(_MQL5Indicator):
    name = 'colorschafftrendcycle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения гистограммы
        'Fast_XMA': 23,  # Период быстрой скользящей средней
        'Slow_XMA': 50,  # Период медленной скользящей средней
        'XPhase': 100,  # Параметр усреднения скользящих средних
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Cycle': 10,  # Период стохастического осциллятора
        'HighLevel': 60,
        'MiddleLevel': 0,
        'LowLevel': -60,
    }
    y_range = (-110.0, 110.0)

