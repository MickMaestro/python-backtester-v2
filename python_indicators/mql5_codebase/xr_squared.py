"""xr-squared — converted from MQL5: MQL5 Indicators/XR-squared/xr-squared.mq5

R-Squared
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [9639167], 2: [16748574]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 4}, 'labels': {1: 'R-Squared', 2: 'Signal'}, 'levels': [70.0, 30.0], 'description': ['R-Squared'], 'name': 'xr-squared', 'source': 'MQL5 Indicators/XR-squared/xr-squared.mq5', 'folder': 'XR-squared', 'inputs': [{'mql': 'XPeriod', 'py': 'XPeriod', 'param': 'XPeriod', 'type': 'int', 'default': 14, 'label': 'Indicator period', 'sinput': False}, {'mql': 'RMethod', 'py': 'RMethod', 'param': 'RMethod', 'type': 'int', 'default': 4, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'RPeriod', 'py': 'RPeriod', 'param': 'RPeriod', 'type': 'int', 'default': 3, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'RPhase', 'py': 'RPhase', 'param': 'RPhase', 'type': 'int', 'default': 100, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'SignMethod', 'py': 'SignMethod', 'param': 'SignMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'SignPeriod', 'py': 'SignPeriod', 'param': 'SignPeriod', 'type': 'int', 'default': 14, 'label': 'Signal line smoothing period', 'sinput': False}, {'mql': 'SignPhase', 'py': 'SignPhase', 'param': 'SignPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XPeriod = _input('XPeriod', 14)  # Indicator period
RMethod = _input('RMethod', MODE_JJMA)  # Smoothing method
RPeriod = _input('RPeriod', 3)  # Smoothing period
RPhase = _input('RPhase', 100)  # Smoothing parameter
SignMethod = _input('SignMethod', MODE_SMA)  # Smoothing method
SignPeriod = _input('SignPeriod', 14)  # Signal line smoothing period
SignPhase = _input('SignPhase', 15)  # Smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Applied price
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
RSquared = Arr(0, 0.0)
XRSquared = Arr(0, 0.0)
StartBars = 0
StartBarsR = 0
StartBarsX = 0
Count = Arr(0, 0)
MA = Arr(0, 0.0)
SumX = 0
SumX2 = 0

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
    global StartBars, StartBarsR, StartBarsX, SumX, SumX2
    StartBarsR = XMA.GetStartBars(RMethod, RPeriod, RPhase) + 1
    StartBarsX = StartBarsR + XPeriod + 1
    StartBars = StartBarsX + XMA.GetStartBars(SignMethod, SignPeriod, SignPhase)
    XMA.XMALengthCheck('SignPeriod', SignPeriod)
    XMA.XMAPhaseCheck('SignPhase', SignPhase, SignMethod)
    XMA.XMALengthCheck('RPeriod', RPeriod)
    XMA.XMAPhaseCheck('RPhase', RPhase, RMethod)
    ArrayResize(Count, XPeriod)
    ArrayResize(MA, XPeriod)
    ArrayInitialize(Count, 0)
    ArrayInitialize(MA, 0.0)
    SumX = 0
    for iii in range(0, XPeriod):
        SumX += iii + 1
    SumX2 = 0
    for iii in range(0, XPeriod):
        SumX2 += (iii + 1) * (iii + 1)
    SetIndexBuffer(0, RSquared, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, RPeriod)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, XRSquared, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth = ""
    Smooth = XMA.GetString_MA_Method(SignMethod)
    StringConcatenate(shortname, 'XR-Squared(', _str(RPeriod), ',', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    price_ = 0.0
    SumY = 0.0
    SumY2 = 0.0
    SumXY = 0.0
    Q1 = 0.0
    Q2 = 0.0
    Q3 = 0.0
    Q23 = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        MA[Count[0]] = XMA.XMASeries(0, prev_calculated, rates_total, RMethod, RPhase, RPeriod, price_, bar, False)
        if bar < StartBarsX:
            if bar < (rates_total - 2):
                Recount_ArrayZeroPos(Count, XPeriod)
            continue
        SumY = 0.0
        for iii in range(0, XPeriod):
            SumY += MA[Count[iii]]
        SumY2 = 0.0
        for iii in range(0, XPeriod):
            SumY2 += MathPow(MA[Count[iii]], 2)
        SumXY = 0.0
        for iii in range(0, XPeriod):
            SumXY += (iii + 1) * MA[Count[iii]]
        Q1 = SumXY - ((SumX * SumY) / XPeriod)
        Q2 = SumX2 - _idiv(SumX * SumX, XPeriod)
        Q3 = SumY2 - ((SumY * SumY) / XPeriod)
        Q23 = Q2 * Q3
        if Q23:
            RSquared[bar] = _fdiv(100 * Q1 * Q1, Q23)
        else:
            RSquared[bar] = 0.0
        if bar < (rates_total - 2):
            Recount_ArrayZeroPos(Count, XPeriod)
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


class XrSquared(_MQL5Indicator):
    name = 'xr-squared'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'XPeriod': 14,  # Indicator period
        'RMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Smoothing method
        'RPeriod': 3,  # Smoothing period
        'RPhase': 100,  # Smoothing parameter
        'SignMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method
        'SignPeriod': 14,  # Signal line smoothing period
        'SignPhase': 15,  # Smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Applied price
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

