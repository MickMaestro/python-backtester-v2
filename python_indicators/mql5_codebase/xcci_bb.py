"""xcci_bb — converted from MQL5: MQL5 Indicators/XCCI/xcci_bb.mq5

Commodity Chanel Index
Copyright: 2010,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh
from backtester.mql5.lib.indicatorsalgorithms import *  # #include indicatorsalgorithms.mqh

MQL5_META = {'props': {'copyright': '2010,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [13850042], 2: [16711680], 3: [255], 4: [8421504], 5: [255], 6: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4}, 'labels': {1: 'XCCI', 2: '+2Sigma', 3: '+Sigma', 4: 'Middle', 5: '-Sigma', 6: '-2Sigma'}, 'levels': [], 'description': ['Commodity Chanel Index'], 'name': 'xcci_bb', 'source': 'MQL5 Indicators/XCCI/xcci_bb.mq5', 'folder': 'XCCI', 'inputs': [{'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 7, 'label': 'Price smoothing method', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 15, 'label': 'Moving average period', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 15, 'label': 'Moving average smoothing parameter', 'sinput': False}, {'mql': 'MPeriod', 'py': 'MPeriod', 'param': 'MPeriod', 'type': 'int', 'default': 15, 'label': 'Average deviation period', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 6, 'label': 'Price constant', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'int', 'default': 100, 'label': 'The period for Bollinger bands', 'sinput': False}, {'mql': 'BBDeviation1', 'py': 'BBDeviation1', 'param': 'BBDeviation1', 'type': 'double', 'default': 1.6, 'label': 'Big deviation', 'sinput': False}, {'mql': 'BBDeviation2', 'py': 'BBDeviation2', 'param': 'BBDeviation2', 'type': 'double', 'default': 1.0, 'label': 'Small deviation', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh', 'indicatorsalgorithms.mqh']}

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
DSmoothMethod = _input('DSmoothMethod', MODE_T3)  # Price smoothing method
DPeriod = _input('DPeriod', 15)  # Moving average period
DPhase = _input('DPhase', 15)  # Moving average smoothing parameter
MPeriod = _input('MPeriod', 15)  # Average deviation period
IPC = _input('IPC', PRICE_TYPICAL)  # Price constant
BBPeriod = _input('BBPeriod', 100)  # The period for Bollinger bands
BBDeviation1 = _input('BBDeviation1', 1.6)  # Big deviation
BBDeviation2 = _input('BBDeviation2', 1.0)  # Small deviation
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
XCCI = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
quotient = 0.0
StartBars = 0
StartBarsD = 0
StartBarsM = 0

def OnInit():
    global StartBars, StartBarsD, StartBarsM, quotient
    StartBarsD = XMAD.GetStartBars(DSmoothMethod, DPeriod, DPhase) + 1
    StartBarsM = MathMax(StartBarsD, MPeriod)
    StartBars = StartBarsM + BBPeriod
    quotient = BBDeviation2 / BBDeviation1
    XMAD.XMALengthCheck('DPeriod', DPeriod)
    XMAD.XMALengthCheck('MPeriod', MPeriod)
    XMAD.XMALengthCheck('BBPeriod', BBPeriod)
    XMAD.XMAPhaseCheck('DPhase', DPhase, DSmoothMethod)
    SetIndexBuffer(0, XCCI, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'XCCI')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer5, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, '+2Sigma')
    PlotIndexSetString(2, PLOT_LABEL, '+Sigma')
    PlotIndexSetString(3, PLOT_LABEL, 'Middle')
    PlotIndexSetString(4, PLOT_LABEL, '-Sigma')
    PlotIndexSetString(5, PLOT_LABEL, '-2Sigma')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    SmoothD = ""
    SmoothD = XMAD.GetString_MA_Method(DSmoothMethod)
    StringConcatenate(shortname, 'Commodity Chanel Index(', _str(DPeriod), ',', _str(MPeriod), ',', SmoothD, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_MPeriod_
    if rates_total < StartBars:
        return 0
    price_ = 0.0
    xma = 0.0
    Sum = 0.0
    D = 0.0
    M = 0.0
    BB = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        _s_OnCalculate_MPeriod_ = MPeriod / 0.015
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        XCCI[bar] = EMPTY_VALUE
        xma = XMAD.XMASeries(0, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, price_, bar, False)
        M = price_ - xma
        if bar < StartBarsM:
            continue
        Sum = 0.0
        for j in range(0, MPeriod):
            Sum += MathAbs(PriceSeries(IPC, bar - j, open, low, high, close) - xma)
        D = _fdiv(Sum, _s_OnCalculate_MPeriod_)
        if D != 0.0:
            XCCI[bar] = _fdiv(M, D)
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
        BBands.BBandsSeries(StartBarsM, prev_calculated, rates_total, BBPeriod, BBDeviation1, MODE_SMA, XCCI[bar], bar, False, _ElemRef(ExtLineBuffer5, bar), _ElemRef(ExtLineBuffer3, bar), _ElemRef(ExtLineBuffer1, bar))
        BB = (ExtLineBuffer1[bar] - ExtLineBuffer3[bar]) * quotient
        ExtLineBuffer2[bar] = ExtLineBuffer3[bar] + BB
        ExtLineBuffer4[bar] = ExtLineBuffer3[bar] - BB
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMAD = _alloc(CXMA)
XMAD.__init__()
BBands = _alloc(CBBands)
BBands.__init__()

# ---- static local variables
_s_OnCalculate_MPeriod_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XcciBb(_MQL5Indicator):
    name = 'xcci_bb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Price smoothing method
        'DPeriod': 15,  # Moving average period
        'DPhase': 15,  # Moving average smoothing parameter
        'MPeriod': 15,  # Average deviation period
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=6),  # Price constant
        'BBPeriod': 100,  # The period for Bollinger bands
        'BBDeviation1': 1.6,  # Big deviation
        'BBDeviation2': 1.0,  # Small deviation
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

