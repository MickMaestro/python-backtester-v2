"""AdvancedFractals — converted from MQL5: MQL5 Indicators/Advanced Fractals/AdvancedFractals.mq5

Draws fractals of any dimension (Frames)
------------------------------------
If the Frames is less than one,
then one Frames will be used.
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Factal Up', 2: 'Fractal Down'}, 'levels': [], 'description': ['Draws fractals of any dimension (Frames)', '------------------------------------', 'If the Frames is less than one,', 'then one Frames will be used.'], 'name': 'AdvancedFractals', 'source': 'MQL5 Indicators/Advanced Fractals/AdvancedFractals.mq5', 'folder': 'Advanced Fractals', 'inputs': [{'mql': 'Frames', 'py': 'Frames', 'param': 'Frames', 'type': 'uint', 'default': 2, 'label': 'Frames', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Frames = _input('Frames', 2)  # Frames
BufferUpFactal = Arr(0, 0.0)
BufferDownFractal = Arr(0, 0.0)
frames = 0

def OnInit():
    global frames
    frames = (1 if (Frames < 1) else Frames)
    SetIndexBuffer(0, BufferUpFactal, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDownFractal, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 4)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 4)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Advanced fractals(' + _str(frames) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < ((frames * 2) + 2):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - frames - 1
        ArrayInitialize(BufferUpFactal, 0.0)
        ArrayInitialize(BufferDownFractal, 0.0)
    for i in range(limit, frames, -1):
        FrUp = True
        FrDn = True
        for n in range(1, frames + 1):
            if high[i + n] >= high[i] or high[i - n] >= high[i]:
                FrUp = False
            if low[i + n] <= low[i] or low[i - n] <= low[i]:
                FrDn = False
        if FrUp:
            BufferUpFactal[i] = high[i]
        if FrDn:
            BufferDownFractal[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdvancedFractals(_MQL5Indicator):
    name = 'AdvancedFractals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Frames': 2,  # Frames
    }

