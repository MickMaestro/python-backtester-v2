"""x2ma_bbx7 — converted from MQL5: MQL5 Indicators/Bollinger Bands Set/x2ma_bbx7.mq5

X2MA Bollinger Bands
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [14822282], 2: [8388736], 3: [255], 4: [16711680], 5: [16711680], 6: [255], 7: [8388736]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4}, 'labels': {1: 'X2MA', 2: '+3Sigma', 3: '+2Sigma', 4: '+1Sigma', 5: '-1Sigma', 6: '-2Sigma', 7: '-3Sigma'}, 'levels': [], 'description': ['X2MA Bollinger Bands'], 'name': 'x2ma_bbx7', 'source': 'MQL5 Indicators/Bollinger Bands Set/x2ma_bbx7.mq5', 'folder': 'Bollinger Bands Set', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'First smoothing method', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 100, 'label': 'First smoothing depth', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'First smoothing parameter', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'Second smoothing method', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 20, 'label': 'Second smoothing depth', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'Second smoothing parameter', 'sinput': False}, {'mql': 'BandsPeriod', 'py': 'BandsPeriod', 'param': 'BandsPeriod', 'type': 'int', 'default': 100, 'label': 'BB smoothing period', 'sinput': False}, {'mql': 'BandsDeviation1', 'py': 'BandsDeviation1', 'param': 'BandsDeviation1', 'type': 'double', 'default': 1.0, 'label': 'First level deviation', 'sinput': False}, {'mql': 'BandsDeviation2', 'py': 'BandsDeviation2', 'param': 'BandsDeviation2', 'type': 'double', 'default': 2.0, 'label': 'Second level deviation', 'sinput': False}, {'mql': 'BandsDeviation3', 'py': 'BandsDeviation3', 'param': 'BandsDeviation3', 'type': 'double', 'default': 3.0, 'label': 'Third level deviation', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
MA_Method1 = _input('MA_Method1', MODE_SMA)  # First smoothing method
Length1 = _input('Length1', 100)  # First smoothing depth
Phase1 = _input('Phase1', 15)  # First smoothing parameter
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # Second smoothing method
Length2 = _input('Length2', 20)  # Second smoothing depth
Phase2 = _input('Phase2', 100)  # Second smoothing parameter
BandsPeriod = _input('BandsPeriod', 100)  # BB smoothing period
BandsDeviation1 = _input('BandsDeviation1', 1.0)  # First level deviation
BandsDeviation2 = _input('BandsDeviation2', 2.0)  # Second level deviation
BandsDeviation3 = _input('BandsDeviation3', 3.0)  # Third level deviation
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
X2MA = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
quotient2 = 0.0
quotient3 = 0.0
dPriceShift = 0.0
StartBars = 0
StartBars1 = 0
StartBars2 = 0

def OnInit():
    global StartBars, StartBars1, StartBars2, dPriceShift, quotient2, quotient3
    StartBars1 = XMA1.GetStartBars(MA_Method1, Length1, Phase1) + 1
    StartBars2 = StartBars1 + XMA2.GetStartBars(MA_Method2, Length2, Phase2)
    StartBars = StartBars2 + BandsPeriod
    quotient2 = BandsDeviation2 / BandsDeviation1
    quotient3 = BandsDeviation3 / BandsDeviation1
    XMA1.XMALengthCheck('Length1', Length1)
    XMA2.XMALengthCheck('Length2', Length2)
    XMA2.XMALengthCheck('BandsPeriod', BandsPeriod)
    XMA1.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA2.XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, X2MA, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'X2MA')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer5, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer6, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, '+3Sigma')
    PlotIndexSetString(2, PLOT_LABEL, '+2Sigma')
    PlotIndexSetString(3, PLOT_LABEL, '+1Sigma')
    PlotIndexSetString(4, PLOT_LABEL, '-1Sigma')
    PlotIndexSetString(5, PLOT_LABEL, '-2Sigma')
    PlotIndexSetString(6, PLOT_LABEL, '-3Sigma')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(MA_Method1)
    Smooth2 = XMA1.GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'X2MA_Bollinger Bands(', Length1, ', ', Length2, ', ', BandsPeriod, ', ', Smooth1, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    price_ = 0.0
    x1xma = 0.0
    x2xma = 0.0
    stdev1 = 0.0
    stdev2 = 0.0
    stdev3 = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        x1xma = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price_, bar, False)
        x2xma = XMA2.XMASeries(StartBars1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, x1xma, bar, False)
        X2MA[bar] = x2xma + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        stdev1 = STD.StdDevSeries(StartBars2, prev_calculated, rates_total, BandsPeriod, BandsDeviation1, price_, X2MA[bar], bar, False)
        stdev2 = stdev1 * quotient2
        stdev3 = stdev1 * quotient3
        ExtLineBuffer1[bar] = X2MA[bar] + stdev3 + dPriceShift
        ExtLineBuffer2[bar] = X2MA[bar] + stdev2 + dPriceShift
        ExtLineBuffer3[bar] = X2MA[bar] + stdev1 + dPriceShift
        ExtLineBuffer4[bar] = X2MA[bar] - stdev1 + dPriceShift
        ExtLineBuffer5[bar] = X2MA[bar] - stdev2 + dPriceShift
        ExtLineBuffer6[bar] = X2MA[bar] - stdev3 + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
STD = _alloc(CStdDeviation)
STD.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class X2maBbx7(_MQL5Indicator):
    name = 'x2ma_bbx7'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # First smoothing method
        'Length1': 100,  # First smoothing depth
        'Phase1': 15,  # First smoothing parameter
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Second smoothing method
        'Length2': 20,  # Second smoothing depth
        'Phase2': 100,  # Second smoothing parameter
        'BandsPeriod': 100,  # BB smoothing period
        'BandsDeviation1': 1.0,  # First level deviation
        'BandsDeviation2': 2.0,  # Second level deviation
        'BandsDeviation3': 3.0,  # Third level deviation
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
    }

