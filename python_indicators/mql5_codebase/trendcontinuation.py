"""trendcontinuation — converted from MQL5: MQL5 Indicators/TrendСontinuation/trendcontinuation.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [65280, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'TrendСontinuation Minus'}, 'levels': [], 'description': [], 'name': 'trendcontinuation', 'source': 'MQL5 Indicators/TrendСontinuation/trendcontinuation.mq5', 'folder': 'TrendСontinuation', 'inputs': [{'mql': 'NPeriod', 'py': 'NPeriod', 'param': 'NPeriod', 'type': 'uint', 'default': 20, 'label': 'calculation period', 'sinput': False}, {'mql': 'XMethod', 'py': 'XMethod', 'param': 'XMethod', 'type': 'int', 'default': 7, 'label': 'smoothing method', 'sinput': False}, {'mql': 'XPeriod', 'py': 'XPeriod', 'param': 'XPeriod', 'type': 'uint', 'default': 5, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 61, 'label': 'smoothing parameter,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
NPeriod = _input('NPeriod', 20)  # calculation period
XMethod = _input('XMethod', MODE_T3)  # smoothing method
XPeriod = _input('XPeriod', 5)  # smoothing depth
XPhase = _input('XPhase', 61)  # smoothing parameter,
IPC = _input('IPC', PRICE_CLOSE)  # price constant
PlusBuffer = Arr(0, 0.0)
MinusBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_ = 0
nsize = 0
Count = Arr(0, 0)
Change_p = Arr(0, 0.0)
Change_n = Arr(0, 0.0)
CF_p = Arr(0, 0.0)
CF_n = Arr(0, 0.0)

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
    global min_rates_, min_rates_total, nsize
    min_rates_ = _int(NPeriod + 1)
    min_rates_total = _int(NPeriod + XMA1.GetStartBars(XMethod, XPeriod, XPhase))
    nsize = _int(NPeriod)
    ArrayResize(Count, nsize)
    ArrayResize(Change_p, nsize)
    ArrayResize(Change_n, nsize)
    ArrayResize(CF_p, nsize)
    ArrayResize(CF_n, nsize)
    ArrayInitialize(Count, 0.0)
    ArrayInitialize(Change_p, 0.0)
    ArrayInitialize(Change_n, 0.0)
    ArrayInitialize(CF_p, 0.0)
    ArrayInitialize(CF_n, 0.0)
    SetIndexBuffer(0, PlusBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MinusBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrendСontinuation')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    dprice = 0.0
    k_p = 0.0
    k_n = 0.0
    ch_p = 0.0
    ch_n = 0.0
    cff_n = 0.0
    cff_p = 0.0
    first = 0
    bar = 0
    iii = 0
    i0 = 0
    i1 = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        dprice = PriceSeries(IPC, bar, open, low, high, close) - PriceSeries(IPC, bar - 1, open, low, high, close)
        i0 = Count[0]
        i1 = Count[1]
        Change_p[i0] = 0.0
        CF_p[i0] = 0.0
        Change_n[i0] = 0.0
        CF_n[i0] = 0.0
        if dprice > 0:
            Change_p[i0] = -dprice
            CF_p[i0] = Change_p[i0] + CF_p[i1]
        elif dprice < 0:
            Change_n[i0] = dprice
            CF_n[i0] = Change_n[i0] + CF_n[i1]
        ch_p = 0.0
        ch_n = 0.0
        cff_p = 0.0
        cff_n = 0.0
        iii = 0
        for iii in range(iii, nsize):
            ch_p += Change_p[iii]
        else:
            iii = _range_end(iii, nsize, 1)
        iii = 0
        for iii in range(iii, nsize):
            ch_n += Change_n[iii]
        else:
            iii = _range_end(iii, nsize, 1)
        iii = 0
        for iii in range(iii, nsize):
            cff_p += CF_p[iii]
        else:
            iii = _range_end(iii, nsize, 1)
        iii = 0
        for iii in range(iii, nsize):
            cff_n += CF_n[iii]
        else:
            iii = _range_end(iii, nsize, 1)
        k_p = ch_p - cff_n
        k_n = ch_n - cff_p
        PlusBuffer[bar] = _fdiv(XMA1.XMASeries(min_rates_, prev_calculated, rates_total, XMethod, XPhase, XMethod, k_p, bar, False), Point())
        MinusBuffer[bar] = _fdiv(XMA2.XMASeries(min_rates_, prev_calculated, rates_total, XMethod, XPhase, XMethod, k_n, bar, False), Point())
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, nsize)
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


class Trendcontinuation(_MQL5Indicator):
    name = 'trendcontinuation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'NPeriod': 20,  # calculation period
        'XMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # smoothing method
        'XPeriod': 5,  # smoothing depth
        'XPhase': 61,  # smoothing parameter,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # price constant
    }

