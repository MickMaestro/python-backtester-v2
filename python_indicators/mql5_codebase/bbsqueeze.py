"""bbsqueeze — converted from MQL5: MQL5 Indicators/BBSqueeze/bbsqueeze.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 3, 2: 3, 3: 5, 4: 5}, 'colors': {1: [8421376], 2: [16711935], 3: [16711680], 4: [14381203]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Uptrend', 2: 'Downtrend', 3: 'Strong trend', 4: 'Weak trend'}, 'levels': [], 'description': [], 'name': 'bbsqueeze', 'source': 'MQL5 Indicators/BBSqueeze/bbsqueeze.mq5', 'folder': 'BBSqueeze', 'inputs': [{'mql': 'BB_Method', 'py': 'BB_Method', 'param': 'BB_Method', 'type': 'int', 'default': 1, 'label': 'Histogram smoothing method', 'sinput': False}, {'mql': 'BB_Period', 'py': 'BB_Period', 'param': 'BB_Period', 'type': 'int', 'default': 20, 'label': 'Bollinger Bands period', 'sinput': False}, {'mql': 'BB_Phase', 'py': 'BB_Phase', 'param': 'BB_Phase', 'type': 'int', 'default': 100, 'label': 'Bollinger Bands smoothing parameter', 'sinput': False}, {'mql': 'BB_Deviation', 'py': 'BB_Deviation', 'param': 'BB_Deviation', 'type': 'double', 'default': 2.0, 'label': 'Number of deviations', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'double', 'default': 20.0, 'label': 'ATR period', 'sinput': False}, {'mql': 'ATR_Factor', 'py': 'ATR_Factor', 'param': 'ATR_Factor', 'type': 'double', 'default': 1.5, 'label': 'ATR ratio', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
BB_Method = _input('BB_Method', MODE_EMA_)  # Histogram smoothing method
BB_Period = _input('BB_Period', 20)  # Bollinger Bands period
BB_Phase = _input('BB_Phase', 100)  # Bollinger Bands smoothing parameter
BB_Deviation = _input('BB_Deviation', 2.0)  # Number of deviations
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # Applied price
ATR_Period = _input('ATR_Period', 20.0)  # ATR period
ATR_Factor = _input('ATR_Factor', 1.5)  # ATR ratio
min_rates_total = 0
min_rates_xma = 0
Count = Arr(0, 0)
Xma = Arr(0, 0.0)
ATR_Handle = 0
STD_Handle = 0
UpHistBuffer = Arr(0, 0.0)
DnHistBuffer = Arr(0, 0.0)
UpArrBuffer = Arr(0, 0.0)
DnArrBuffer = Arr(0, 0.0)

def OnInit():
    global ATR_Handle, STD_Handle, min_rates_total, min_rates_xma
    min_rates_xma = XMA1.GetStartBars(BB_Method, BB_Period, BB_Phase)
    min_rates_total = _int(MathMax(min_rates_xma, ATR_Period))
    STD_Handle = iStdDev(None, 0, BB_Period, 0, MODE_SMA, PRICE_CLOSE)
    if STD_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStdDev indicator')
        return 1
    ATR_Handle = iATR(None, 0, 15)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iATR indicator')
        return 1
    if ArrayResize(Count, BB_Period) < BB_Period:
        Print('Failed to distribute the memory for Count[] array')
    if ArrayResize(Xma, BB_Period) < BB_Period:
        Print('Failed to distribute the memory for Xma[] array')
    ArrayInitialize(Count, 0)
    ArrayInitialize(Xma, 0)
    SetIndexBuffer(0, UpHistBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpHistBuffer, True)
    SetIndexBuffer(1, DnHistBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DnHistBuffer, True)
    SetIndexBuffer(2, UpArrBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    ArraySetAsSeries(UpArrBuffer, True)
    SetIndexBuffer(3, DnArrBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    ArraySetAsSeries(DnArrBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BBSqueeze')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(STD_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    maxbar1 = 0
    STD = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    lregress = 0.0
    bbs = 0.0
    price_ = 0.0
    maxbar = rates_total - 1
    maxbar1 = maxbar - min_rates_xma - (2 * BB_Period)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(STD_Handle, 0, 0, to_copy, STD) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(STD, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        price_ = PriceSeries(AppliedPrice, bar, open, low, high, close)
        Xma[Count[0]] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, BB_Method, BB_Phase, BB_Period, price_, bar, True)
        if bar > maxbar1:
            Recount_ArrayZeroPos(Count, BB_Period)
            continue
        lregress = LinearRegressionValue(BB_Period, bar, open, low, high, close)
        if lregress < 0:
            UpHistBuffer[bar] = EMPTY_VALUE
            DnHistBuffer[bar] = lregress
        else:
            UpHistBuffer[bar] = lregress
            DnHistBuffer[bar] = EMPTY_VALUE
        bbs = _fdiv(BB_Deviation * STD[bar], ATR[bar] * ATR_Factor)
        if bbs < 1:
            DnArrBuffer[bar] = 0.0
            UpArrBuffer[bar] = EMPTY_VALUE
        else:
            UpArrBuffer[bar] = 0.0
            DnArrBuffer[bar] = EMPTY_VALUE
        if bar:
            Recount_ArrayZeroPos(Count, BB_Period)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def LinearRegressionValue(Len, index, Open, Low, High, Close):
    SumBars = 0.0
    Sum1 = 0.0
    Sum2 = 0.0
    SumY = 0.0
    Slope = 0.0
    SumSqrBars = 0.0
    dxma = 0.0
    Num1 = 0.0
    Num2 = 0.0
    HH = 0.0
    LL = 0.0
    Intercept = 0.0
    LinearRegValue = 0.0
    SumY = 0.0
    Sum1 = 0.0
    SumBars = Len * (Len - 1) * 0.5
    SumSqrBars = _idiv((Len - 1) * Len * ((2 * Len) - 1), 6)
    for x in range(0, Len):
        HH = Low[index + x]
        LL = High[index + x]
        for y in range(x, x + Len):
            HH = MathMax(HH, High[index + y])
            LL = MathMin(LL, Low[index + y])
        dxma = Close[index + x] - ((((HH + LL) / 2) + Xma[Count[x]]) / 2)
        Sum1 += x * dxma
        SumY += dxma
    Sum2 = SumBars * SumY
    Num1 = (Len * Sum1) - Sum2
    Num2 = (SumBars * SumBars) - (Len * SumSqrBars)
    if Num2 != 0.0:
        Slope = _fdiv(Num1, Num2)
    else:
        Slope = 0.0
    Intercept = _fdiv(SumY - (Slope * SumBars), Len)
    LinearRegValue = Intercept + (Slope * (Len - 1))
    return LinearRegValue

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max1 = _int(Size - 1)
    Max2 = _int(Size)
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bbsqueeze(_MQL5Indicator):
    name = 'bbsqueeze'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BB_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Histogram smoothing method
        'BB_Period': 20,  # Bollinger Bands period
        'BB_Phase': 100,  # Bollinger Bands smoothing parameter
        'BB_Deviation': 2.0,  # Number of deviations
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Applied price
        'ATR_Period': 20.0,  # ATR period
        'ATR_Factor': 1.5,  # ATR ratio
    }

