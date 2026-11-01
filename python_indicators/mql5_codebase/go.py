"""go — converted from MQL5: MQL5 Indicators/Go/go.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 65280, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Go'}, 'levels': [], 'description': [], 'name': 'go', 'source': 'MQL5 Indicators/Go/go.mq5', 'folder': 'Go', 'inputs': [{'mql': 'Period_', 'py': 'Period_', 'param': 'Period_', 'type': 'int', 'default': 174, 'label': 'Period of the indicator', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
Period_ = _input('Period_', 174)  # Period of the indicator
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtBuffer = Arr(0, 0.0)
ColorExtBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'Go(', Period_, ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Period_)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorExtBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Period_)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (Period_ + 1):
        return 0
    first1 = 0
    first2 = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = 0
        first2 = Period_ + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
    bar = first1
    for bar in range(bar, rates_total):
        ExtBuffer[bar] = _fdiv(_s_OnCalculate_MA.MASeries(0, prev_calculated, rates_total, Period_, MODE_SMA, close[bar] - open[bar], bar, False), Point())
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        ColorExtBuffer[bar] = 0.0
        if ExtBuffer[bar] > 0:
            ColorExtBuffer[bar] = 1.0
        if ExtBuffer[bar] < 0:
            ColorExtBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_MA = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Go(_MQL5Indicator):
    name = 'go'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_': 174,  # Period of the indicator
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

