"""colorjccx — converted from MQL5: MQL5 Indicators/ColorJCCX/colorjccx.mq5

Commodity Chanel Index
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 10}, 'colors': {1: [8421504], 2: [255, 36095, 8421504, 16760576, 16711680]}, 'widths': {1: 1, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'JCCX', 2: 'High Short;Short;Flat;Long;High Long'}, 'levels': [], 'description': ['Commodity Chanel Index'], 'name': 'colorjccx', 'source': 'MQL5 Indicators/ColorJCCX/colorjccx.mq5', 'folder': 'ColorJCCX', 'inputs': [{'mql': 'JMAPeriod', 'py': 'JMAPeriod', 'param': 'JMAPeriod', 'type': 'uint', 'default': 8, 'label': 'JMA period', 'sinput': False}, {'mql': 'JMAPhase', 'py': 'JMAPhase', 'param': 'JMAPhase', 'type': 'int', 'default': 100, 'label': 'JMA smoothing parameter, for JJMA it varies within the range -100 ... +100 and influences the quality of the transient period;', 'sinput': False}, {'mql': 'JurXPeriod', 'py': 'JurXPeriod', 'param': 'JurXPeriod', 'type': 'uint', 'default': 8, 'label': 'JurX period', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'Style', 'py': 'Style', 'param': 'Style', 'type': 'int', 'default': 10, 'label': 'JCCX display style', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 20, 'label': 'trigger top level', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': 'middle of the range', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -20, 'label': 'trigger bottom level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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

# enum IndStyle
COLOR_LINE = 8
COLOR_HISTOGRAM = 10
COLOR_ARROW = 12
_enum('IndStyle', {8: 'COLOR_LINE', 10: 'COLOR_HISTOGRAM', 12: 'COLOR_ARROW'})

# ---- inputs and global variables
JMAPeriod = _input('JMAPeriod', 8)  # JMA period
JMAPhase = _input('JMAPhase', 100)
JurXPeriod = _input('JurXPeriod', 8)  # JurX period
IPC = _input('IPC', PRICE_CLOSE)  # price constant
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
Style = _input('Style', COLOR_HISTOGRAM)  # JCCX display style
HighLevel = _input('HighLevel', 20)  # trigger top level
MiddleLevel = _input('MiddleLevel', 0)  # middle of the range
LowLevel = _input('LowLevel', -20)  # trigger bottom level
JCCX = Arr(0, 0.0)
JCCX_ = Arr(0, 0.0)
ColorJCCX = Arr(0, 0.0)
min_rates_total = 0
min_rates_ = 0

def OnInit():
    global min_rates_, min_rates_total
    min_rates_ = 30 + 1
    min_rates_total = min_rates_ + 3
    SetIndexBuffer(0, JCCX_, INDICATOR_DATA)
    SetIndexBuffer(1, JCCX, INDICATOR_DATA)
    SetIndexBuffer(2, ColorJCCX, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, Style)
    shortname = Box("")
    StringConcatenate(shortname, 'Commodity Chanel Index(', _str(JMAPeriod), ',', _str(JMAPhase), ',', _str(JurXPeriod), ',', EnumToString(IPC, 'Applied_price_'), ',', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrPurple)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrPurple)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    jprice = 0.0
    upccx = 0.0
    dnccx = 0.0
    jupccx = 0.0
    jdnccx = 0.0
    first = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    for bar in range(first, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        JCCX[bar] = EMPTY_VALUE
        jprice = JMA.JJMASeries(1, prev_calculated, rates_total, 0, JMAPhase, JMAPeriod, price, bar, False)
        upccx = price - jprice
        dnccx = MathAbs(upccx)
        jupccx = UpJurX.JurXSeries(min_rates_, prev_calculated, rates_total, 0, JurXPeriod, upccx, bar, False)
        jdnccx = DnJurX.JurXSeries(min_rates_, prev_calculated, rates_total, 0, JurXPeriod, dnccx, bar, False)
        if jupccx:
            JCCX[bar] = _fdiv(100 * jupccx, jdnccx)
        JCCX_[bar] = JCCX[bar]
        clr = 2
        if JCCX[bar] > JCCX[bar - 1]:
            if JCCX[bar] > HighLevel:
                clr = 4
            else:
                clr = 3
        if JCCX[bar] < JCCX[bar - 1]:
            if JCCX[bar] < LowLevel:
                clr = 0
            else:
                clr = 1
        ColorJCCX[bar] = clr
    return rates_total

# ---- global variables initialised from expressions
JMA = _alloc(CJJMA)
JMA.__init__()
UpJurX = _alloc(CJurX)
UpJurX.__init__()
DnJurX = _alloc(CJurX)
DnJurX.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorjccx(_MQL5Indicator):
    name = 'colorjccx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JMAPeriod': 8,  # JMA period
        'JMAPhase': 100,  # JMA smoothing parameter, for JJMA it varies within the range -100 ... +100 and influences the quality of the transient period;
        'JurXPeriod': 8,  # JurX period
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # price constant
        'Shift': 0,  # horizontal shift of the indicator in bars
        'Style': _Choice({8: 'Colored line', 10: 'Colored histogram', 12: 'Colored labels'}, default=10),  # JCCX display style
        'HighLevel': 20,  # trigger top level
        'MiddleLevel': 0,  # middle of the range
        'LowLevel': -20,  # trigger bottom level
    }

