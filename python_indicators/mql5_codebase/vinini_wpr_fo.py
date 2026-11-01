"""vinini_wpr_fo — converted from MQL5: MQL5 Indicators/VininI WPR FO/vinini_wpr_fo.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': -1.25, 'indicator_maximum': 1.25}, 'types': {1: 12}, 'colors': {1: [16711680, 65280, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'VininI WPR FO'}, 'levels': [], 'description': [], 'name': 'vinini_wpr_fo', 'source': 'MQL5 Indicators/VininI WPR FO/vinini_wpr_fo.mq5', 'folder': 'VininI WPR FO', 'inputs': [{'mql': 'WPR_Period', 'py': 'WPR_Period', 'param': 'WPR_Period', 'type': 'int', 'default': 5, 'label': 'WPR period', 'sinput': False}, {'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'int', 'default': 9, 'label': 'Moving average period', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 1, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'double', 'default': -0.5, 'label': '', 'sinput': False}, {'mql': 'Style', 'py': 'Style', 'param': 'Style', 'type': 'int', 'default': 10, 'label': 'Indicator display style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

Gray = 0x808080  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name

# enum ENUM_IND_STYLE
COLOR_LINE = 8
COLOR_HISTOGRAM = 10
COLOR_ARROW = 12
_enum('ENUM_IND_STYLE', {8: 'COLOR_LINE', 10: 'COLOR_HISTOGRAM', 12: 'COLOR_ARROW'})

# ---- inputs and global variables
WPR_Period = _input('WPR_Period', 5)  # WPR period
MA_Period = _input('MA_Period', 9)  # Moving average period
MA_Method_ = _input('MA_Method_', MODE_EMA)  # Smoothing method
HighLevel = _input('HighLevel', 0.5)
MiddleLevel = _input('MiddleLevel', 0.0)
LowLevel = _input('LowLevel', -0.5)
Style = _input('Style', COLOR_HISTOGRAM)  # Indicator display style
ColorBuffer = Arr(0, 0.0)
ExtLineBuffer = Arr(0, 0.0)
WPR_Handle = 0
min_rates_total = 0

def OnInit():
    global WPR_Handle, min_rates_total
    min_rates_total = WPR_Period + MA_Period + 1
    WPR_Handle = iWPR(None, 0, WPR_Period)
    if WPR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the WPR indicator')
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, Style)
    ArraySetAsSeries(ExtLineBuffer, True)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorBuffer, True)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, Magenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, Gray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, Magenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    shortname = Box("")
    StringConcatenate(shortname, 'VininI WPR FO(', WPR_Period, ', ', MA_Period, ', ', EnumToString(MA_Method_, 'ENUM_MA_METHOD'), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(WPR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    WPR = Arr(0, 0.0)
    velue = 0.0
    ma = 0.0
    expma = 0.0
    fish = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - WPR_Period
    else:
        limit = rates_total - prev_calculated
    maxbar = rates_total - 1 - WPR_Period
    to_copy = limit + 1
    if CopyBuffer(WPR_Handle, 0, 0, to_copy, WPR) <= 0:
        return 0
    ArraySetAsSeries(WPR, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        velue = 0.1 * (WPR[bar] + 50)
        ma = _s_OnCalculate_MA.MASeries(maxbar, prev_calculated, rates_total, MA_Period, MA_Method_, velue, bar, True)
        if bar < maxbar:
            expma = MathExp(2.0 * ma)
            fish = _fdiv(expma - 1.0, expma + 1.0)
        else:
            fish = EMPTY_VALUE
        ExtLineBuffer[bar] = fish
        ColorBuffer[bar] = 0.0
        if ma > HighLevel and ma != EMPTY_VALUE:
            ColorBuffer[bar] = 1.0
        if ma < LowLevel and ma != EMPTY_VALUE:
            ColorBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_MA = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VininiWprFo(_MQL5Indicator):
    name = 'vinini_wpr_fo'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WPR_Period': 5,  # WPR period
        'MA_Period': 9,  # Moving average period
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Smoothing method
        'HighLevel': 0.5,
        'MiddleLevel': 0.0,
        'LowLevel': -0.5,
        'Style': _Choice({8: 'Colored line', 10: 'Colored histogram', 12: 'Colored labels'}, default=10),  # Indicator display style
    }
    y_range = (-1.25, 1.25)

