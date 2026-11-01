"""smpricebend-t01 — converted from MQL5: MQL5 Indicators/SmPriceBend-T01/smpricebend-t01.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [9639167, 8388736, 8421504, 16711680, 16760576]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'SmPriceBend-T01'}, 'levels': [], 'description': [], 'name': 'smpricebend-t01', 'source': 'MQL5 Indicators/SmPriceBend-T01/smpricebend-t01.mq5', 'folder': 'SmPriceBend-T01', 'inputs': [{'mql': 'XMA_Method1', 'py': 'XMA_Method1', 'param': 'XMA_Method1', 'type': 'int', 'default': 0, 'label': 'smoothing method', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 21, 'label': 'smoothing depth of moving average', 'sinput': False}, {'mql': 'XPhase1', 'py': 'XPhase1', 'param': 'XPhase1', 'type': 'int', 'default': 15, 'label': 'moving average smoothing parameter,', 'sinput': False}, {'mql': 'XMA_Method2', 'py': 'XMA_Method2', 'param': 'XMA_Method2', 'type': 'int', 'default': 7, 'label': 'smoothing method', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'uint', 'default': 6, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'XPhase2', 'py': 'XPhase2', 'param': 'XPhase2', 'type': 'int', 'default': 70, 'label': 'smoothing parameter,', 'sinput': False}, {'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'uint', 'default': 2, 'label': 'Momentum period', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 30, 'label': 'trigger top level', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': 'middle of the range', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -30, 'label': 'trigger bottom level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method1 = _input('XMA_Method1', MODE_SMA)  # smoothing method
XLength1 = _input('XLength1', 21)  # smoothing depth of moving average
XPhase1 = _input('XPhase1', 15)  # moving average smoothing parameter,
XMA_Method2 = _input('XMA_Method2', MODE_T3)  # smoothing method
XLength2 = _input('XLength2', 6)  # smoothing depth
XPhase2 = _input('XPhase2', 70)  # smoothing parameter,
MomPeriod = _input('MomPeriod', 2)  # Momentum period
IPC = _input('IPC', PRICE_CLOSE)  # price constant
HighLevel = _input('HighLevel', 30)  # trigger top level
MiddleLevel = _input('MiddleLevel', 0)  # middle of the range
LowLevel = _input('LowLevel', -30)  # trigger bottom level
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = XMA1.GetStartBars(XMA_Method1, XLength1, XPhase1)
    min_rates_2 = _int(min_rates_1 + MomPeriod)
    min_rates_total = XMA1.GetStartBars(XMA_Method2, XLength2, XPhase2)
    XMA1.XMALengthCheck('XLength1', XLength1)
    XMA1.XMAPhaseCheck('XPhase1', XPhase1, XMA_Method1)
    XMA1.XMALengthCheck('XLength2', XLength2)
    XMA1.XMAPhaseCheck('XPhase2', XPhase2, XMA_Method2)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SmPriceBend-T01')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrDarkViolet)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrDarkViolet)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    x1xma = 0.0
    bend = 0.0
    xbend = 0.0
    first = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        x1xma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method1, XPhase1, XLength1, price, bar, False)
        bend = _fdiv(Mom.MomentumSeries(min_rates_1, prev_calculated, rates_total, MomPeriod, x1xma, bar, False), Point())
        xbend = XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method2, XPhase2, XLength2, bend, bar, False)
        IndBuffer[bar] = xbend
        clr = 2
        if xbend > MiddleLevel:
            if xbend > HighLevel:
                clr = 4
            else:
                clr = 3
        if xbend < MiddleLevel:
            if xbend < LowLevel:
                clr = 0
            else:
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
Mom = _alloc(CMomentum)
Mom.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmpricebendT01(_MQL5Indicator):
    name = 'smpricebend-t01'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # smoothing method
        'XLength1': 21,  # smoothing depth of moving average
        'XPhase1': 15,  # moving average smoothing parameter,
        'XMA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # smoothing method
        'XLength2': 6,  # smoothing depth
        'XPhase2': 70,  # smoothing parameter,
        'MomPeriod': 2,  # Momentum period
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # price constant
        'HighLevel': 30,  # trigger top level
        'MiddleLevel': 0,  # middle of the range
        'LowLevel': -30,  # trigger bottom level
    }

