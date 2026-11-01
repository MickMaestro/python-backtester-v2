"""ticks — converted from MQL5: MQL5 Indicators/Ticks/ticks.mq5

Copyright: 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bid', 2: 'Ask'}, 'levels': [], 'description': [], 'name': 'ticks', 'source': 'MQL5 Indicators/Ticks/ticks.mq5', 'folder': 'Ticks', 'inputs': [{'mql': 'number_of_ticks', 'py': 'number_of_ticks', 'param': 'number_of_ticks', 'type': 'int', 'default': 1000, 'label': '', 'sinput': False}, {'mql': 'points_indent', 'py': 'points_indent', 'param': 'points_indent', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
number_of_ticks = _input('number_of_ticks', 1000)
points_indent = _input('points_indent', 10)
BidBuffer = Arr(0, 0.0)
AskBuffer = Arr(0, 0.0)

def OnDeinit(reason):
    Comment('')

def OnInit():
    SetIndexBuffer(0, BidBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, AskBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ticks
    if _s_OnCalculate_ticks == 0:
        ArrayInitialize(AskBuffer, 0)
        ArrayInitialize(BidBuffer, 0)
    setMaxMinPrice(_s_OnCalculate_ticks, points_indent)
    last_tick = MqlTick()
    if SymbolInfoTick(Symbol(), last_tick):
        BidBuffer[_s_OnCalculate_ticks] = last_tick.bid
        AskBuffer[_s_OnCalculate_ticks] = last_tick.ask
        shift = rates_total - 1 - _s_OnCalculate_ticks
        _s_OnCalculate_ticks += 1
        BidBuffer[rates_total - 1] = last_tick.bid
        AskBuffer[rates_total - 1] = last_tick.ask
        PlotIndexSetInteger(0, PLOT_SHIFT, shift)
        PlotIndexSetInteger(1, PLOT_SHIFT, shift)
        Comment('Bid =', last_tick.bid, '   Ask =', last_tick.ask)
    return rates_total

def setMaxMinPrice(last_values, indent):
    visiblebars = _int(ChartGetInteger(0, CHART_VISIBLE_BARS))
    depth = MathMin(last_values, visiblebars)
    startindex = last_values - depth
    if startindex < 0:
        startindex = 0
    max_index = ArrayMaximum(AskBuffer, startindex, depth)
    max_index = (max_index if (max_index >= 0) else 0)
    min_index = ArrayMinimum(BidBuffer, startindex, depth)
    min_index = (min_index if (min_index >= 0) else 0)
    MaxPrice = AskBuffer[max_index] + (indent * Point())
    MinPrice = BidBuffer[min_index] - (indent * Point())
    IndicatorSetDouble(INDICATOR_MAXIMUM, MaxPrice)
    IndicatorSetDouble(INDICATOR_MINIMUM, MinPrice)

# ---- static local variables
_s_OnCalculate_ticks = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ticks(_MQL5Indicator):
    name = 'ticks'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'number_of_ticks': 1000,
        'points_indent': 10,
    }

