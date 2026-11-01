"""linearregslope_v2 — converted from MQL5: MQL5 Indicators/LinearRegSlope V2/linearregslope_v2.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [5275647]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Linear Reg Slope line', 2: 'Trigger line'}, 'levels': [], 'description': [], 'name': 'linearregslope_v2', 'source': 'MQL5 Indicators/LinearRegSlope V2/linearregslope_v2.mq5', 'folder': 'LinearRegSlope V2', 'inputs': [{'mql': 'SlMethod', 'py': 'SlMethod', 'param': 'SlMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'SlLength', 'py': 'SlLength', 'param': 'SlLength', 'type': 'int', 'default': 12, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'SlPhase', 'py': 'SlPhase', 'param': 'SlPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'TriggerShift', 'py': 'TriggerShift', 'param': 'TriggerShift', 'type': 'int', 'default': 1, 'label': 'Bar shift for the trigger', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
SlMethod = _input('SlMethod', MODE_SMA)  # Smoothing method
SlLength = _input('SlLength', 12)  # Smoothing depth
SlPhase = _input('SlPhase', 15)  # Smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
TriggerShift = _input('TriggerShift', 1)  # Bar shift for the trigger
min_rates_total = 0
RegSlopeBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
TriggerShift_ = 0
TrigShift = 0
TrigShift_ = 0
SumX = 0.0
Divisor = 0.0
Count = Arr(0, 0)
Smooth = Arr(0, 0.0)

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
    global Divisor, SumX, TrigShift, TrigShift_, TriggerShift_, min_rates_total
    min_rates_total = XMA1.GetStartBars(SlMethod, 1, SlPhase) + SlLength + TriggerShift
    XMA1.XMALengthCheck('SlLength', SlLength)
    XMA1.XMAPhaseCheck('SlPhase', SlPhase, SlMethod)
    if TriggerShift > (SlLength - 2):
        Print('TriggerShift input parameter value cannot exceed SlLength-2')
        TrigShift = 1
        TrigShift_ = SlLength - 2
    else:
        TrigShift = SlLength - 1 - TriggerShift
        TrigShift_ = TriggerShift
    SumX = SlLength * (SlLength - 1) * 0.5
    SumXSqr = ((SlLength - 1.0) * SlLength * ((2.0 * SlLength) - 1.0)) / 6.0
    Divisor = (SumX * SumX) - (SlLength * SumXSqr)
    TriggerShift_ = min_rates_total
    ArrayResize(Count, SlLength)
    ArrayResize(Smooth, SlLength)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Smooth, 0.0)
    SetIndexBuffer(0, RegSlopeBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(SlMethod)
    StringConcatenate(shortname, 'Linear Reg Slope(', SlLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price_ = 0.0
    SumY = 0.0
    SumXY = 0.0
    Intercept = 0.0
    Slope = 0.0
    first = 0
    bar = 0
    iii = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        Smooth[Count[0]] = XMA1.XMASeries(0, prev_calculated, rates_total, SlMethod, SlPhase, SlLength, price_, bar, False)
        SumY = 0.0
        SumXY = 0.0
        iii = 0
        for iii in range(iii, SlLength):
            SumY += Smooth[Count[iii]]
            SumXY += iii * Smooth[Count[iii]]
        else:
            iii = _range_end(iii, SlLength, 1)
        if Divisor != 0:
            Slope = _fdiv((SlLength * SumXY) - (SumX * SumY), Divisor)
        else:
            Slope = EMPTY_VALUE
        if bar >= SlLength:
            Intercept = (SumY - (Slope * SumX)) / SlLength
            RegSlopeBuffer[bar] = Intercept + (Slope * TrigShift)
        if bar > TriggerShift_:
            TriggerBuffer[bar] = (2.0 * RegSlopeBuffer[bar]) - RegSlopeBuffer[bar - TrigShift_]
        else:
            TriggerBuffer[bar] = EMPTY_VALUE
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, SlLength)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LinearregslopeV2(_MQL5Indicator):
    name = 'linearregslope_v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SlMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method
        'SlLength': 12,  # Smoothing depth
        'SlPhase': 15,  # Smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'TriggerShift': 1,  # Bar shift for the trigger
    }

