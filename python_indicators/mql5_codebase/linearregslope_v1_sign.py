"""LinearRegSlope_V1_Sign — converted from MQL5: MQL5 Indicators/LinearRegSlope_V1_Sign/LinearRegSlope_V1_Sign.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'LinearRegSlope_V1 Sell', 2: 'LinearRegSlope_V1 Buy'}, 'levels': [], 'description': [], 'name': 'LinearRegSlope_V1_Sign', 'source': 'MQL5 Indicators/LinearRegSlope_V1_Sign/LinearRegSlope_V1_Sign.mq5', 'folder': 'LinearRegSlope_V1_Sign', 'inputs': [{'mql': 'SlMethod', 'py': 'SlMethod', 'param': 'SlMethod', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'SlLength', 'py': 'SlLength', 'param': 'SlLength', 'type': 'int', 'default': 12, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'SlPhase', 'py': 'SlPhase', 'param': 'SlPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'TriggerShift', 'py': 'TriggerShift', 'param': 'TriggerShift', 'type': 'uint', 'default': 1, 'label': 'cдвиг бара для тригера', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
SlMethod = _input('SlMethod', MODE_SMA)  # метод усреднения
SlLength = _input('SlLength', 12)  # глубина сглаживания
SlPhase = _input('SlPhase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
TriggerShift = _input('TriggerShift', 1)  # cдвиг бара для тригера
min_rates_total = 0
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
TriggerShift_ = 0
Num2 = 0.0
SumBars = 0.0
Count1 = Arr(0, 0)
Count2 = Arr(0, 0)
Smooth = Arr(0, 0.0)
RegSlope = Arr(0, 0.0)
ATR_Handle = 0

def Recount_ArrayZeroPos1(CoArr, Size):
    global _s_Recount_ArrayZeroPos1_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos1_count -= 1
    if _s_Recount_ArrayZeroPos1_count < 0:
        _s_Recount_ArrayZeroPos1_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos1_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def Recount_ArrayZeroPos2(CoArr, Size):
    global _s_Recount_ArrayZeroPos2_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos2_count -= 1
    if _s_Recount_ArrayZeroPos2_count < 0:
        _s_Recount_ArrayZeroPos2_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos2_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global ATR_Handle, Num2, SumBars, TriggerShift_, min_rates_total
    ATR_Period = 15
    min_rates_total = GetStartBars(SlMethod, SlLength, SlPhase)
    min_rates_total = MathMax(ATR_Period, min_rates_total) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    XMA1.XMALengthCheck('SlLength', SlLength)
    XMA1.XMAPhaseCheck('SlPhase', SlPhase, SlMethod)
    SumBars = SlLength * (SlLength - 1) * 0.5
    SumSqrBars = ((SlLength - 1.0) * SlLength * ((2.0 * SlLength) - 1.0)) / 6.0
    Num2 = (SumBars * SumBars) - (SlLength * SumSqrBars)
    TriggerShift_ = _int(min_rates_total + TriggerShift - 1)
    ArrayResize(Count1, SlLength)
    ArrayResize(Smooth, SlLength)
    ArrayResize(Count2, TriggerShift + 1)
    ArrayResize(RegSlope, TriggerShift + 1)
    ArrayInitialize(Count1, 0)
    ArrayInitialize(Count2, 0)
    ArrayInitialize(Smooth, 0.0)
    ArrayInitialize(RegSlope, 0.0)
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 172)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 172)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(SlMethod)
    StringConcatenate(shortname, 'Linear Reg Slope(', SlLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_trend_
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    price = 0.0
    Sum1 = 0.0
    Sum2 = 0.0
    SumY = 0.0
    Num1 = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    Trigger = 0.0
    trend = 0.0
    first = 0
    bar = 0
    iii = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_trend_ = 0.0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        Smooth[Count1[0]] = XMA1.XMASeries(0, prev_calculated, rates_total, SlMethod, SlPhase, SlLength, price, bar, False)
        Sum1 = 0.0
        SumY = 0.0
        if bar > SlLength:
            iii = 0
            for iii in range(iii, SlLength):
                SumY += Smooth[Count1[iii]]
                Sum1 += iii * Smooth[Count1[iii]]
            else:
                iii = _range_end(iii, SlLength, 1)
        Sum2 = SumBars * SumY
        Num1 = (SlLength * Sum1) - Sum2
        if Num2:
            RegSlope[Count2[0]] = _fdiv(100 * Num1, Num2)
        else:
            RegSlope[Count2[0]] = EMPTY_VALUE
        if bar > TriggerShift_:
            Trigger = RegSlope[Count2[TriggerShift]]
        else:
            Trigger = EMPTY_VALUE
        trend = RegSlope[Count2[0]] - Trigger
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        if _s_OnCalculate_trend_ <= 0 and trend > 0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_trend_ >= 0 and trend < 0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos1(Count1, SlLength)
            Recount_ArrayZeroPos2(Count2, TriggerShift + 1)
            if trend:
                _s_OnCalculate_trend_ = trend
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos1_count = 1
_s_Recount_ArrayZeroPos2_count = 1
_s_OnCalculate_trend_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LinearRegSlopeV1Sign(_MQL5Indicator):
    name = 'LinearRegSlope_V1_Sign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SlMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'SlLength': 12,  # глубина сглаживания
        'SlPhase': 15,  # параметр сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'TriggerShift': 1,  # cдвиг бара для тригера
    }

