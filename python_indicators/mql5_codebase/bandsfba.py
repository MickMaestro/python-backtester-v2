"""bandsfba — converted from MQL5: MQL5 Indicators/BandsFBA/bandsfba.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [8388736], 2: [8388736], 3: [8388736], 4: [255], 5: [255], 6: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 4, 2: 4, 3: 4, 4: 0, 5: 0, 6: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'bandsfba', 'source': 'MQL5 Indicators/BandsFBA/bandsfba.mq5', 'folder': 'BandsFBA', 'inputs': [{'mql': 'bMA_Method', 'py': 'bMA_Method', 'param': 'bMA_Method', 'type': 'int', 'default': 0, 'label': 'first smoothing method', 'sinput': False}, {'mql': 'bLength', 'py': 'bLength', 'param': 'bLength', 'type': 'int', 'default': 20, 'label': 'period of averaging of BB', 'sinput': False}, {'mql': 'bPhase', 'py': 'bPhase', 'param': 'bPhase', 'type': 'int', 'default': 15, 'label': 'first smoothing parameter,', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 2.0, 'label': 'Bollinger deviation', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'FrontPeriod', 'py': 'FrontPeriod', 'param': 'FrontPeriod', 'type': 'uint', 'default': 1, 'label': 'front smoothing period; <1', 'sinput': False}, {'mql': 'BackPeriod', 'py': 'BackPeriod', 'param': 'BackPeriod', 'type': 'uint', 'default': 55, 'label': 'damping smoothing period; <1', 'sinput': False}, {'mql': 'BShift', 'py': 'BShift', 'param': 'BShift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'SShift', 'py': 'SShift', 'param': 'SShift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
bMA_Method = _input('bMA_Method', MODE_SMA)  # first smoothing method
bLength = _input('bLength', 20)  # period of averaging of BB
bPhase = _input('bPhase', 15)  # first smoothing parameter,
BandsDeviation = _input('BandsDeviation', 2.0)  # Bollinger deviation
IPC = _input('IPC', PRICE_CLOSE)  # price constant
FrontPeriod = _input('FrontPeriod', 1)  # front smoothing period; <1
BackPeriod = _input('BackPeriod', 55)  # damping smoothing period; <1
BShift = _input('BShift', 0)  # horizontal shift of the indicator in bars
SShift = _input('SShift', 0)  # horizontal shift of the indicator in bars
XMAB = Arr(0, 0.0)  # XMA
TopB = Arr(0, 0.0)  # top line
BotB = Arr(0, 0.0)  # bottom line
XMAS = Arr(0, 0.0)  # top signal line
TopS = Arr(0, 0.0)  # top signal line
BotS = Arr(0, 0.0)  # bottom signal line
per0 = 0.0
per1 = 0.0
FBA = 0  # 1 - front smoothing, -1 - damping smoothing, 0 - normal MA - smooth all!
min_rates_ = 0
min_rates_total = 0

def OnInit():
    global FBA, min_rates_, min_rates_total, per0, per1
    _fr = _str(FrontPeriod)
    _bk = _str(BackPeriod)
    _dv = _str(BandsDeviation)
    ShortName = 'BandsFBA'
    _sg = _fr
    FBA = 0
    if FrontPeriod == BackPeriod:
        FBA = 0
        per0 = 2.0 / (1 + FrontPeriod)
        per1 = 1.0
    if FrontPeriod < BackPeriod:
        FBA = -1
        per0 = 2.0 / (1 + FrontPeriod)
        per1 = 2.0 / (1 + BackPeriod)
    else:
        FBA = 1
        per0 = 2.0 / (1 + BackPeriod)
        per1 = 2.0 / (1 + FrontPeriod)
        _sg = _bk
    min_rates_ = XMA.GetStartBars(bMA_Method, bLength, bPhase)
    min_rates_total = (2 * min_rates_) + 1
    SetIndexBuffer(0, XMAB, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, BShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(0, PLOT_LABEL, 'XMA(' + _str(bLength) + ')')
    SetIndexBuffer(1, TopB, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, BShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(1, PLOT_LABEL, 'TopB(+' + _dv + ')')
    SetIndexBuffer(2, BotB, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, BShift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(2, PLOT_LABEL, 'BotB(-' + _dv + ')')
    SetIndexBuffer(3, XMAS, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, SShift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(3, PLOT_LABEL, 'XMAS(' + _sg + ')')
    SetIndexBuffer(4, TopS, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, SShift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(4, PLOT_LABEL, 'TopS(' + _fr + ',' + _bk + ')')
    SetIndexBuffer(5, BotS, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_SHIFT, SShift)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(5, PLOT_LABEL, 'BotS(' + _fr + ',' + _bk + ')')
    IndicatorSetString(INDICATOR_SHORTNAME, ShortName)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_stdevb, _s_OnCalculate_prev_stdevc, _s_OnCalculate_prev_xmab
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    minbar = 0
    price_ = 0.0
    xmaa = 0.0
    stdeva = 0.0
    xmab = 0.0
    stdevb = 0.0
    stdevc = 0.0
    minbar = min_rates_total - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_prev_stdevb = 1.0
        _s_OnCalculate_prev_stdevc = 1.0
        _s_OnCalculate_prev_xmab = PriceSeries(IPC, first, open, low, high, close)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        xmaa = XMA.XMASeries(0, prev_calculated, rates_total, bMA_Method, bPhase, bLength, price_, bar, False)
        XMAB[bar] = xmaa
        stdeva = STD.StdDevSeries(min_rates_, prev_calculated, rates_total, bLength, BandsDeviation, price_, xmaa, bar, False)
        TopB[bar] = xmaa + stdeva
        BotB[bar] = xmaa - stdeva
        if bar < minbar:
            continue
        elif bar == minbar:
            _s_OnCalculate_prev_stdevb = stdeva
            _s_OnCalculate_prev_stdevc = stdeva
            _s_OnCalculate_prev_xmab = price_
        xmab = EMA_FBA(xmaa, _s_OnCalculate_prev_xmab, per0, 0)
        XMAS[bar] = xmab
        stdevb = EMA_FBA(stdeva, _s_OnCalculate_prev_stdevb, per0, 0)
        stdevc = EMA_FBA(stdevb, _s_OnCalculate_prev_stdevc, per1, FBA)
        TopS[bar] = xmab + stdevc
        BotS[bar] = xmab - stdevc
        if bar < (rates_total - 1):
            _s_OnCalculate_prev_stdevb = stdevb
            _s_OnCalculate_prev_stdevc = stdevc
            _s_OnCalculate_prev_xmab = xmab
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def EMA_FBA(Series_, EMA1, period, fba):
    if period == 1:
        return Series_
    if period > 1:
        period = _fdiv(2.0, 1 + period)
    EMA = (period * Series_) + ((1 - period) * EMA1)
    _sw1 = fba
    if _sw1 == 0:
        return EMA
    elif _sw1 == 1:
        if Series_ > EMA1:
            return EMA
        else:
            return Series_
    elif _sw1 == -1:
        if Series_ < EMA1:
            return EMA
        else:
            return Series_
    return EMA

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()
STD = _alloc(CStdDeviation)
STD.__init__()

# ---- static local variables
_s_OnCalculate_prev_stdevb = 0.0
_s_OnCalculate_prev_stdevc = 0.0
_s_OnCalculate_prev_xmab = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bandsfba(_MQL5Indicator):
    name = 'bandsfba'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'bMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # first smoothing method
        'bLength': 20,  # period of averaging of BB
        'bPhase': 15,  # first smoothing parameter,
        'BandsDeviation': 2.0,  # Bollinger deviation
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # price constant
        'FrontPeriod': 1,  # front smoothing period; <1
        'BackPeriod': 55,  # damping smoothing period; <1
        'BShift': 0,  # horizontal shift of the indicator in bars
        'SShift': 0,  # horizontal shift of the indicator in bars
    }

