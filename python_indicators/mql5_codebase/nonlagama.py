"""nonlagama — converted from MQL5: MQL5 Indicators/NonLagAMA/nonlagama.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16711935, 8421504, 16760576]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'NonLagAMA'}, 'levels': [], 'description': [], 'name': 'nonlagama', 'source': 'MQL5 Indicators/NonLagAMA/nonlagama.mq5', 'folder': 'NonLagAMA', 'inputs': [{'mql': 'Length0', 'py': 'Length0', 'param': 'Length0', 'type': 'uint', 'default': 12, 'label': 'depth of averaging NonLagAMA', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 0.0, 'label': 'deviation', 'sinput': False}, {'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'uint', 'default': 0, 'label': 'price measurement value, not considered by the Moving Average in points', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'smoothing method', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 12, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'smoothing parameter,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
PRICE_NAVEL_ = 13
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_', 13: 'PRICE_NAVEL_'})

# ---- inputs and global variables
Length0 = _input('Length0', 12)  # depth of averaging NonLagAMA
Deviation = _input('Deviation', 0.0)  # deviation
Filter = _input('Filter', 0)  # price measurement value, not considered by the Moving Average in points
MA_Method1 = _input('MA_Method1', MODE_SMA)  # smoothing method
Length1 = _input('Length1', 12)  # smoothing depth
Phase1 = _input('Phase1', 15)  # smoothing parameter,
IPC = _input('IPC', PRICE_CLOSE)  # price constant
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # vertical shift of the indicator in points
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Coeff = 0.0
pi = 0.0
Cycle = 0.0
res1 = 0.0
res2 = 0.0
FPoint = 0.0
dPriceShift = 0.0
min_rates_total = 0
Length0_ = 0
Len = 0
Count = Arr(0, 0)
Value = Arr(0, 0.0)

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
    global Coeff, Cycle, FPoint, Len, Length0_, dPriceShift, min_rates_total, pi, res1, res2
    min_rates_total = XMA.GetStartBars(MA_Method1, Length1, Phase1)
    XMA.XMALengthCheck('Length1', Length1)
    XMA.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    dPriceShift = Point() * PriceShift
    pi = 3.1415926535
    Cycle = 4.0
    Coeff = 3 * pi
    Length0_ = _int(MathMin(Length0 - 1, 2))
    Len = _int((Length0 * Cycle) + Length0_)
    res1 = _fdiv(1.0, Length0_ - 1)
    res = (Cycle * Length0) - 1
    if not res:
        res = 1.0
    res2 = _fdiv((2 * Cycle) - 1, res)
    FPoint = Filter * Point()
    ArrayResize(Count, Len)
    ArrayResize(Value, Len)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Value, 0.0)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'NonLagAMA')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    alfa = 0.0
    t = 0.0
    Sum = 0.0
    Weight = 0.0
    g = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        Value[Count[0]] = XMA.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price, bar, False)
        Weight = 0.0
        Sum = 0.0
        t = 0.0
        for iii in range(0, Len):
            g = _fdiv(1.0, (Coeff * t) + 1)
            if t <= 0.5:
                g = 1.0
            alfa = g * MathCos(pi * t)
            Sum += alfa * Value[Count[iii]]
            Weight += alfa
            if t < 1:
                t += res1
            elif t < (Len - 1):
                t += res2
        if Weight:
            IndBuffer[bar] = dPriceShift + _fdiv((1.0 + (Deviation / 100)) * Sum, Weight)
        if bar and MathAbs(IndBuffer[bar] - IndBuffer[bar - 1]) < FPoint:
            IndBuffer[bar] = IndBuffer[bar - 1]
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, Len)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        ColorIndBuffer[bar] = 1.0
        if IndBuffer[bar - 1] < IndBuffer[bar]:
            ColorIndBuffer[bar] = 2.0
        if IndBuffer[bar - 1] > IndBuffer[bar]:
            ColorIndBuffer[bar] = 0.0
        if IndBuffer[bar - 1] == IndBuffer[bar]:
            ColorIndBuffer[bar] = ColorIndBuffer[bar - 1]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Nonlagama(_MQL5Indicator):
    name = 'nonlagama'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length0': 12,  # depth of averaging NonLagAMA
        'Deviation': 0.0,  # deviation
        'Filter': 0,  # price measurement value, not considered by the Moving Average in points
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # smoothing method
        'Length1': 12,  # smoothing depth
        'Phase1': 15,  # smoothing parameter,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price', 13: 'Navel Price'}, default=1),  # price constant
        'Shift': 0,  # horizontal shift of the indicator in bars
        'PriceShift': 0,  # vertical shift of the indicator in points
    }

