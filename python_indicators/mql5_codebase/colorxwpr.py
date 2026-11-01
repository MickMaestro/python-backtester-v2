"""colorxwpr — converted from MQL5: MQL5 Indicators/ColorXWPR/colorxwpr.mq5

Larry Williams' Percent Range
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [8421504, 11186720, 11823615], 2: [16711680]}, 'widths': {1: 4, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Signal', 2: 'WPR'}, 'levels': [-20.0, -80.0], 'description': ["Larry Williams' Percent Range"], 'name': 'colorxwpr', 'source': 'MQL5 Indicators/ColorXWPR/colorxwpr.mq5', 'folder': 'ColorXWPR', 'inputs': [{'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 15, 'label': 'WPR period', 'sinput': False}, {'mql': 'SSmoothMethod', 'py': 'SSmoothMethod', 'param': 'SSmoothMethod', 'type': 'int', 'default': 4, 'label': 'Signal line smoothing method', 'sinput': False}, {'mql': 'SPeriod', 'py': 'SPeriod', 'param': 'SPeriod', 'type': 'int', 'default': 7, 'label': 'Signal line period', 'sinput': False}, {'mql': 'SPhase', 'py': 'SPhase', 'param': 'SPhase', 'type': 'int', 'default': 100, 'label': 'Signal line parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'Style', 'py': 'Style', 'param': 'Style', 'type': 'int', 'default': 12, 'label': 'WPR display style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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

# enum IndStyle
COLOR_LINE = 8
COLOR_ARROW = 12
_enum('IndStyle', {8: 'COLOR_LINE', 12: 'COLOR_ARROW'})

# ---- inputs and global variables
DPeriod = _input('DPeriod', 15)  # WPR period
SSmoothMethod = _input('SSmoothMethod', MODE_JJMA)  # Signal line smoothing method
SPeriod = _input('SPeriod', 7)  # Signal line period
SPhase = _input('SPhase', 100)  # Signal line parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Style = _input('Style', DRAW_COLOR_ARROW)  # WPR display style
WPR = Arr(0, 0.0)
XWPR = Arr(0, 0.0)
ColorXWPR = Arr(0, 0.0)
StartBars = 0
StartBarsD = 0
StartBarsS = 0

def OnInit():
    global StartBars, StartBarsD, StartBarsS
    StartBarsD = DPeriod + 1
    StartBarsS = StartBarsD + XSIGN.GetStartBars(SSmoothMethod, SPeriod, SPhase)
    StartBars = StartBarsS
    XSIGN.XMALengthCheck('SPeriod', SPeriod)
    XSIGN.XMAPhaseCheck('SPhase', SPhase, SSmoothMethod)
    SetIndexBuffer(0, XWPR, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorXWPR, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars + 1)
    SetIndexBuffer(2, WPR, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, Style)
    shortname = Box("")
    Smooth = ""
    Smooth = XSIGN.GetString_MA_Method(SSmoothMethod)
    StringConcatenate(shortname, "Larry Williams' Percent Range(", _str(DPeriod), ',', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    HH = 0.0
    LL = 0.0
    price_ = 0.0
    first1 = 0
    first2 = 0
    first3 = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = StartBarsD
        first2 = StartBarsD + 1
        first3 = StartBars + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
        first3 = first1
    bar = first1
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        ArraySetAsSeries(low, True)
        ArraySetAsSeries(high, True)
        rate_ = rates_total - 1 - bar
        LL = low[ArrayMinimum(low, rate_, DPeriod)]
        HH = high[ArrayMaximum(high, rate_, DPeriod)]
        if HH != LL:
            WPR[bar] = _fdiv((-(HH - price_)) * 100, HH - LL)
        else:
            WPR[bar] = WPR[bar - 1]
        XWPR[bar] = XSIGN.XMASeries(StartBarsD, prev_calculated, rates_total, SSmoothMethod, SPhase, SPeriod, WPR[bar], bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first3
    for bar in range(bar, rates_total):
        ColorXWPR[bar] = 0.0
        if XWPR[bar] > XWPR[bar - 1]:
            ColorXWPR[bar] = 1.0
        if XWPR[bar] < XWPR[bar - 1]:
            ColorXWPR[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XSIGN = _alloc(CXMA)
XSIGN.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorxwpr(_MQL5Indicator):
    name = 'colorxwpr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DPeriod': 15,  # WPR period
        'SSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Signal line smoothing method
        'SPeriod': 7,  # Signal line period
        'SPhase': 100,  # Signal line parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'Style': _Choice({8: 'Colored line', 12: 'Colored labels'}, default=12),  # WPR display style
    }

