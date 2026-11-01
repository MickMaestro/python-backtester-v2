"""rjt_matches — converted from MQL5: MQL5 Indicators/RJT Matches/rjt_matches.mq5

We recommend adjust the body and head size of the matches for better visualization.
Copyright: Copyright 2015, Rafael Jimenez Tocino; Link: http://www.tradingrafa.com/indicadores/rjt_matches; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2015, Rafael Jimenez Tocino', 'link': 'http://www.tradingrafa.com/indicadores/rjt_matches', 'version': '2.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 5, 5: 5}, 'colors': {1: [16777215], 2: [16777215], 3: [16777215], 4: [255], 5: [65280]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'match1', 2: 'match2', 3: 'match3', 4: 'headred', 5: 'headgreen'}, 'levels': [], 'description': ['We recommend adjust the body and head size of the matches for better visualization.'], 'name': 'rjt_matches', 'source': 'MQL5 Indicators/RJT Matches/rjt_matches.mq5', 'folder': 'RJT Matches', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LineBuffer1 = Arr(0, 0.0)
LineBuffer2 = Arr(0, 0.0)
LineBuffer3 = Arr(0, 0.0)
LineBuffer4 = Arr(0, 0.0)
LineBuffer5 = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, LineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, LineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, LineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, LineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, LineBuffer5, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    c = 0
    p = 0
    i = 1
    for i in range(i, rates_total):
        if close[i] > open[i - 1]:
            LineBuffer4[i] = EMPTY_VALUE
            LineBuffer5[i] = close[i]
        else:
            LineBuffer4[i] = close[i]
            LineBuffer5[i] = EMPTY_VALUE
        _sw1 = p
        if _sw1 == 0:
            LineBuffer1[i] = open[i]
            LineBuffer2[i] = EMPTY_VALUE
            LineBuffer3[i] = close[i]
        elif _sw1 == 1:
            LineBuffer1[i] = close[i]
            LineBuffer2[i] = open[i]
            LineBuffer3[i] = EMPTY_VALUE
        elif _sw1 == 2:
            LineBuffer1[i] = EMPTY_VALUE
            LineBuffer2[i] = close[i]
            LineBuffer3[i] = open[i]
        p += 1
        p = (0 if (p == 3) else p)
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def OnDeinit(reason):
    Print('RJT Matches - Finished')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RjtMatches(_MQL5Indicator):
    name = 'rjt_matches'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

