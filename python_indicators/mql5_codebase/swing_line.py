"""swing_line — converted from MQL5: MQL5 Indicators/Swing Line/swing_line.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 9662683]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'Swing line'}, 'levels': [], 'description': [], 'name': 'swing_line', 'source': 'MQL5 Indicators/Swing Line/swing_line.mq5', 'folder': 'Swing Line', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
swli = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
work = Arr(0, 0.0, dims=(5,))

def OnInit():
    SetIndexBuffer(0, swli, INDICATOR_DATA)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ArrayRange(work, 0) != rates_total:
        ArrayResize(work, rates_total)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        if i == 0:
            work[i][0] = high[i]
            work[i][1] = low[i]
            work[i][2] = high[i]
            work[i][3] = low[i]
            work[i][4] = -1.0
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
        if work[i][4] == 1:
            swli[i] = work[i][1]
        else:
            swli[i] = work[i][2]
        colorBuffer[i] = colorBuffer[i - 1]
        if work[i][4] == 1:
            colorBuffer[i] = 0.0
        if work[i][4] == -1:
            colorBuffer[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SwingLine(_MQL5Indicator):
    name = 'swing_line'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

