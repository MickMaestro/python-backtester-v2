"""mass_index_bb — converted from MQL5: MQL5 Indicators/Mass Index (MI)/mass_index_bb.mq5

Mass Index
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 7}, 'types': {1: 10, 2: 8, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [8421504, 32768, 16711935], 2: [8421504, 16711680, 36095], 3: [16711680], 4: [255], 5: [8421504], 6: [255], 7: [16711680]}, 'widths': {1: 3, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {1: 0, 2: 1, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4}, 'labels': {1: 'Mass Index', 2: 'Signal line', 3: '+2Sigma', 4: '+Sigma', 5: 'Middle', 6: '-Sigma', 7: '-2Sigma'}, 'levels': [], 'description': ['Mass Index'], 'name': 'mass_index_bb', 'source': 'MQL5 Indicators/Mass Index (MI)/mass_index_bb.mq5', 'folder': 'Mass Index (MI)', 'inputs': [{'mql': 'APeriod', 'py': 'APeriod', 'param': 'APeriod', 'type': 'int', 'default': 25, 'label': 'Summing period', 'sinput': False}, {'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 1, 'label': 'Indicator smoothing method', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 9, 'label': 'Indicator smoothing period', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 100, 'label': 'Indicator smoothing parameter', 'sinput': False}, {'mql': 'SSmoothMethod', 'py': 'SSmoothMethod', 'param': 'SSmoothMethod', 'type': 'int', 'default': 1, 'label': 'Signal line smoothing method', 'sinput': False}, {'mql': 'SPeriod', 'py': 'SPeriod', 'param': 'SPeriod', 'type': 'int', 'default': 7, 'label': 'Signal line period', 'sinput': False}, {'mql': 'SPhase', 'py': 'SPhase', 'param': 'SPhase', 'type': 'int', 'default': 100, 'label': 'Signal line parameter', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'Style', 'py': 'Style', 'param': 'Style', 'type': 'int', 'default': 10, 'label': 'MI display style', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'int', 'default': 100, 'label': 'Bollinger Bands period', 'sinput': False}, {'mql': 'BBDeviation1', 'py': 'BBDeviation1', 'param': 'BBDeviation1', 'type': 'double', 'default': 1.0, 'label': 'Small deviation', 'sinput': False}, {'mql': 'BBDeviation2', 'py': 'BBDeviation2', 'param': 'BBDeviation2', 'type': 'double', 'default': 1.6, 'label': 'Big deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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

# enum IndStyle
COLOR_LINE = 8
COLOR_HISTOGRAM = 10
COLOR_ARROW = 12
_enum('IndStyle', {8: 'COLOR_LINE', 10: 'COLOR_HISTOGRAM', 12: 'COLOR_ARROW'})

# ---- inputs and global variables
APeriod = _input('APeriod', 25)  # Summing period
DSmoothMethod = _input('DSmoothMethod', MODE_EMA)  # Indicator smoothing method
DPeriod = _input('DPeriod', 9)  # Indicator smoothing period
DPhase = _input('DPhase', 100)  # Indicator smoothing parameter
SSmoothMethod = _input('SSmoothMethod', MODE_EMA)  # Signal line smoothing method
SPeriod = _input('SPeriod', 7)  # Signal line period
SPhase = _input('SPhase', 100)  # Signal line parameter
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Style = _input('Style', COLOR_HISTOGRAM)  # MI display style
BBPeriod = _input('BBPeriod', 100)  # Bollinger Bands period
BBDeviation1 = _input('BBDeviation1', 1.0)  # Small deviation
BBDeviation2 = _input('BBDeviation2', 1.6)  # Big deviation
MIBuffer = Arr(0, 0.0)
XMIBuffer = Arr(0, 0.0)
ColorMIBuffer = Arr(0, 0.0)
ColorXMIBuffer = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
quotient = 0.0
StartBars = 0
StartBarsA = 0
StartBarsD = 0
StartBarsD2 = 0
StartBarsS = 0
StartBarsB = 0

def OnInit():
    global StartBars, StartBarsA, StartBarsB, StartBarsD, StartBarsD2, StartBarsS, quotient
    StartBarsD = XMA1.GetStartBars(DSmoothMethod, DPeriod, DPhase)
    StartBarsA = (2 * StartBarsD) + 1 + APeriod
    StartBarsD2 = (2 * StartBarsD) + 1
    StartBarsS = StartBarsD2 + XMA1.GetStartBars(SSmoothMethod, SPeriod, SPhase)
    StartBarsB = StartBarsD + BBPeriod
    StartBars = MathMax(StartBarsS, StartBarsB)
    XMA1.XMALengthCheck('DPeriod', DPeriod)
    XMA1.XMALengthCheck('SPeriod', SPeriod)
    XMA1.XMAPhaseCheck('DPhase', DPhase, DSmoothMethod)
    XMA1.XMAPhaseCheck('SPhase', SPhase, SSmoothMethod)
    quotient = BBDeviation2 / BBDeviation1
    SetIndexBuffer(0, MIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBarsA + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, Style)
    SetIndexBuffer(1, ColorMIBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBarsA + 1)
    SetIndexBuffer(2, XMIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBarsA + 1)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ColorXMIBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBars + 1)
    SetIndexBuffer(4, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(7, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(8, ExtLineBuffer5, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(8, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth = ""
    Smooth = XMA1.GetString_MA_Method(DSmoothMethod)
    StringConcatenate(shortname, 'Mass Index(', _str(DPeriod), ',', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    dprice_ = 0.0
    x1xma = 0.0
    x2xma = 0.0
    sum_ = 0.0
    mi = 0.0
    xmi = 0.0
    bbxma = 0.0
    stdev1 = 0.0
    stdev2 = 0.0
    first1 = 0
    first2 = 0
    first3 = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = 0
        first2 = StartBarsD + 1
        first3 = StartBarsS + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
        first3 = first1
    bar = first1
    for bar in range(bar, rates_total):
        dprice_ = high[bar] - low[bar]
        x1xma = XMA1.XMASeries(0, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, dprice_, bar, False)
        sum_ = SUM.XMASeries(StartBarsD, prev_calculated, rates_total, MODE_SMA_, 0, APeriod, x1xma, bar, False) * APeriod
        x2xma = XMA2.XMASeries(StartBarsD, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, x1xma, bar, False)
        if x2xma == 0 or x2xma == EMPTY_VALUE:
            mi = EMPTY_VALUE
        else:
            mi = _fdiv(sum_, x2xma)
        MIBuffer[bar] = mi
        xmi = SIGN.XMASeries(StartBarsA, prev_calculated, rates_total, SSmoothMethod, SPhase, SPeriod, mi, bar, False)
        MIBuffer[bar] = mi
        XMIBuffer[bar] = xmi
        bbxma = XMA3.XMASeries(StartBarsA, prev_calculated, rates_total, MODE_SMA_, 0, BBPeriod, mi, bar, False)
        stdev1 = STD.StdDevSeries(StartBarsA, prev_calculated, rates_total, BBPeriod, BBDeviation1, xmi, bbxma, bar, False)
        stdev2 = stdev1 * quotient
        if bar <= (StartBarsB + BBPeriod):
            bbxma = EMPTY_VALUE
            stdev1 = 0.0
            stdev2 = 0.0
        ExtLineBuffer1[bar] = bbxma + stdev2
        ExtLineBuffer2[bar] = bbxma + stdev1
        ExtLineBuffer3[bar] = bbxma
        ExtLineBuffer4[bar] = bbxma - stdev1
        ExtLineBuffer5[bar] = bbxma - stdev2
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first3
    for bar in range(bar, rates_total):
        pass
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        ColorMIBuffer[bar] = 0.0
        if MIBuffer[bar] > 0:
            if MIBuffer[bar] > MIBuffer[bar - 1]:
                ColorMIBuffer[bar] = 1.0
            if MIBuffer[bar] < MIBuffer[bar - 1]:
                ColorMIBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first3
    for bar in range(bar, rates_total):
        ColorXMIBuffer[bar] = 0.0
        if MIBuffer[bar] > XMIBuffer[bar - 1]:
            ColorXMIBuffer[bar] = 1.0
        if MIBuffer[bar] < XMIBuffer[bar - 1]:
            ColorXMIBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()
SUM = _alloc(CXMA)
SUM.__init__()
SIGN = _alloc(CXMA)
SIGN.__init__()
STD = _alloc(CStdDeviation)
STD.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MassIndexBb(_MQL5Indicator):
    name = 'mass_index_bb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'APeriod': 25,  # Summing period
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Indicator smoothing method
        'DPeriod': 9,  # Indicator smoothing period
        'DPhase': 100,  # Indicator smoothing parameter
        'SSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Signal line smoothing method
        'SPeriod': 7,  # Signal line period
        'SPhase': 100,  # Signal line parameter
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'Style': _Choice({8: 'Colored line', 10: 'Colored histogram', 12: 'Colored labels'}, default=10),  # MI display style
        'BBPeriod': 100,  # Bollinger Bands period
        'BBDeviation1': 1.0,  # Small deviation
        'BBDeviation2': 1.6,  # Big deviation
    }

