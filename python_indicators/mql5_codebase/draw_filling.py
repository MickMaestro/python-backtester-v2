"""draw_filling — converted from MQL5: MQL5 Indicators/DRAW_FILLING/draw_filling.mq5

An indicator to demonstrate DRAW_FILLING
It draws a channel between two MAs in a separate window
The fill color is changed randomly
after every N ticks
Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [255, 16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Intersection'}, 'levels': [], 'description': ['An indicator to demonstrate DRAW_FILLING', 'It draws a channel between two MAs in a separate window', 'The fill color is changed randomly', 'after every N ticks'], 'name': 'draw_filling', 'source': 'MQL5 Indicators/DRAW_FILLING/draw_filling.mq5', 'folder': 'DRAW_FILLING', 'inputs': [{'mql': 'Fast', 'py': 'Fast', 'param': 'Fast', 'type': 'int', 'default': 13, 'label': 'The period of a fast MA', 'sinput': False}, {'mql': 'Slow', 'py': 'Slow', 'param': 'Slow', 'type': 'int', 'default': 21, 'label': 'The period of a slow MA', 'sinput': False}, {'mql': 'shift', 'py': 'shift', 'param': 'shift', 'type': 'int', 'default': 1, 'label': 'A shift of MAs towards the future (positive)', 'sinput': False}, {'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 5, 'label': 'Number of ticks to change', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Fast = _input('Fast', 13)  # The period of a fast MA
Slow = _input('Slow', 21)  # The period of a slow MA
shift = _input('shift', 1)  # A shift of MAs towards the future (positive)
N = _input('N', 5)  # Number of ticks to change
IntersectionBuffer1 = Arr(0, 0.0)
IntersectionBuffer2 = Arr(0, 0.0)
fast_handle = 0
slow_handle = 0
colors = Arr.of([clrRed, clrBlue, clrGreen, clrAquamarine, clrBlanchedAlmond, clrBrown, clrCoral, clrDarkSlateGray], fill=0)

def OnInit():
    global fast_handle, slow_handle
    SetIndexBuffer(0, IntersectionBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, IntersectionBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, shift)
    fast_handle = iMA(Symbol(), Period(), Fast, 0, MODE_SMA, PRICE_CLOSE)
    slow_handle = iMA(Symbol(), Period(), Slow, 0, MODE_SMA, PRICE_CLOSE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ticks
    _s_OnCalculate_ticks += 1
    if _s_OnCalculate_ticks >= N:
        ChangeLineAppearance()
        _s_OnCalculate_ticks = 0
    if prev_calculated == 0:
        copied1 = CopyBuffer(fast_handle, 0, 0, rates_total, IntersectionBuffer1)
        copied2 = CopyBuffer(slow_handle, 0, 0, rates_total, IntersectionBuffer2)
    else:
        to_copy = rates_total - prev_calculated
        if to_copy == 0:
            to_copy = 1
        copied1 = CopyBuffer(fast_handle, 0, 0, to_copy, IntersectionBuffer1)
        copied2 = CopyBuffer(slow_handle, 0, 0, to_copy, IntersectionBuffer2)
    return rates_total

def ChangeLineAppearance():
    comm = ''
    number = MathRand()
    size = ArraySize(colors)
    color_index1 = _imod(number, size)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, colors[color_index1])
    comm = comm + '\r\nColor1 ' + _str(colors[color_index1])
    number = MathRand()
    color_index2 = _imod(number, size)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, colors[color_index2])
    comm = comm + '\r\nColor2 ' + _str(colors[color_index2])
    Comment(comm)

# ---- static local variables
_s_OnCalculate_ticks = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DrawFilling(_MQL5Indicator):
    name = 'draw_filling'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fast': 13,  # The period of a fast MA
        'Slow': 21,  # The period of a slow MA
        'shift': 1,  # A shift of MAs towards the future (positive)
        'N': 5,  # Number of ticks to change
    }

