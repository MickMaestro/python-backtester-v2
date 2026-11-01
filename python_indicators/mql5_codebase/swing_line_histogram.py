"""Swing line (histogram) — converted from MQL5: MQL5 Indicators/Swing Line - Histogram/Swing line (histogram).mq5

Swing line - histogram
Copyright: Copyright 2018, mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_maximum': 1.0, 'indicator_minimum': 0.0}, 'types': {1: 10}, 'colors': {1: [3329330, 9662683]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'Swing line histogram'}, 'levels': [], 'description': ['Swing line - histogram'], 'name': 'Swing line (histogram)', 'source': 'MQL5 Indicators/Swing Line - Histogram/Swing line (histogram).mq5', 'folder': 'Swing Line - Histogram', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
histo = Arr(0, 0.0)
histoc = Arr(0, 0.0)
work = Arr(0, 0.0, dims=(5,))

def OnInit():
    SetIndexBuffer(0, histo, INDICATOR_DATA)
    SetIndexBuffer(1, histoc, INDICATOR_COLOR_INDEX)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(work, 0) != rates_total:
        ArrayResize(work, rates_total)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        if i == 0:
            work[i][0] = high[i]
            work[i][1] = low[i]
            work[i][2] = high[i]
            work[i][3] = low[i]
            work[i][4] = -1.0
            i += 1
            continue
        work[i][4] = work[i - 1][4]
        work[i][0] = work[i - 1][0]
        work[i][1] = work[i - 1][1]
        work[i][2] = work[i - 1][2]
        work[i][3] = work[i - 1][3]
        if work[i - 1][4] == 1:
            work[i][0] = MathMax(work[i - 1][0], high[i])
            work[i][1] = MathMax(work[i - 1][1], low[i])
            if high[i] < work[i][1]:
                work[i][4] = -1.0
                work[i][2] = high[i]
                work[i][3] = low[i]
        if work[i - 1][4] == -1:
            work[i][2] = MathMin(work[i - 1][2], high[i])
            work[i][3] = MathMin(work[i - 1][3], low[i])
            if low[i] > work[i][2]:
                work[i][4] = 1.0
                work[i][0] = high[i]
                work[i][1] = low[i]
        histo[i] = 1.0
        histoc[i] = (0 if (work[i][4] == 1) else 1 if (work[i][4] == -1) else histoc[i - 1] if (i > 0) else 0)
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SwingLineHistogram(_MQL5Indicator):
    name = 'Swing line (histogram)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }
    y_range = (0.0, 1.0)

