"""range — converted from MQL5: MQL5 Indicators/Range/range.mq5

Copyright: Copyright © 2005, Jason Robinson; Link: http://www.jnrtrading.co.uk; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Jason Robinson', 'link': 'http://www.jnrtrading.co.uk', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [1993170, 8421504, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Range'}, 'levels': [], 'description': [], 'name': 'range', 'source': 'MQL5 Indicators/Range/range.mq5', 'folder': 'Range', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Range')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    Range = 0
    Prev_Range = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
        IndBuffer[first - 1] = _fdiv(High[first - 1] - Low[first - 1], Point())
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Range = _uint(_fdiv(High[bar] - Low[bar], Point()))
        IndBuffer[bar] = Range
        Prev_Range = _uint(IndBuffer[bar - 1])
        if Range > Prev_Range:
            clr = 2
        elif Range < Prev_Range:
            clr = 0
        else:
            clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Range(_MQL5Indicator):
    name = 'range'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

