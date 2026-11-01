"""extremum — converted from MQL5: MQL5 Indicators/Extremum/extremum.mq5

Copyright: Copyright © 2010, Egor; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Egor', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 3, 5: 3, 6: 3}, 'colors': {1: [16711680], 2: [8421376], 3: [16711935], 4: [255], 5: [16711680], 6: [65280]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Extremum Line', 2: 'Upper Line', 3: 'Lower Line', 4: 'Lower Histogram', 5: 'Signal Histogram', 6: 'Upper Histogram'}, 'levels': [], 'description': [], 'name': 'extremum', 'source': 'MQL5 Indicators/Extremum/extremum.mq5', 'folder': 'Extremum', 'inputs': [{'mql': 'NBars', 'py': 'NBars', 'param': 'NBars', 'type': 'uint', 'default': 20, 'label': 'indicator period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
NBars = _input('NBars', 20)  # indicator period
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
LineBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnhBuffer = Arr(0, 0.0)
FlhBuffer = Arr(0, 0.0)
UphBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, NBars)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, NBars)
    SetIndexBuffer(2, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, NBars)
    SetIndexBuffer(3, DnhBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, NBars)
    SetIndexBuffer(4, FlhBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, NBars)
    SetIndexBuffer(5, UphBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, NBars)
    shortname = Box("")
    StringConcatenate(shortname, 'Extremum(', NBars, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < _int(NBars):
        return 0
    first = 0
    bar = 0
    i = 0
    n = 0.0
    m = 0.0
    sum_ = 0.0
    dif = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = _int(NBars - 1)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        FlhBuffer[bar] = 0.0
        DnhBuffer[bar] = 0.0
        UphBuffer[bar] = 0.0
        n = 0.0
        m = 0.0
        i = 0
        for i in range(i, _int(NBars)):
            if High[bar] > High[bar - i] and (High[bar] - High[bar - i]) > n:
                n = High[bar] - High[bar - i]
        else:
            i = _range_end(i, _int(NBars), 1)
        i = 0
        for i in range(i, _int(NBars)):
            if Low[bar] < Low[bar - i] and (Low[bar] - Low[bar - i]) < m:
                m = High[bar] - Low[bar - i]
        else:
            i = _range_end(i, _int(NBars), 1)
        sum_ = n + m
        dif = m - n
        LineBuffer[bar] = sum_
        UpBuffer[bar] = dif
        DnBuffer[bar] = -dif
        if sum_ == dif or sum_ == (-dif):
            FlhBuffer[bar] = (-sum_) / 2
        if sum_ < 0:
            DnhBuffer[bar] = sum_
        if sum_ > 0:
            UphBuffer[bar] = sum_
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Extremum(_MQL5Indicator):
    name = 'extremum'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'NBars': 20,  # indicator period
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

