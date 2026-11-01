"""Beginner — converted from MQL5: MQL5 Indicators/Beginner indicator MT5/Beginner.mq5

Beginner - basic indicator for marking chart's highs and lows.
Repaints.
Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.02', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [16711680, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ["Beginner - basic indicator for marking chart's highs and lows.", 'Repaints.'], 'name': 'Beginner', 'source': 'MQL5 Indicators/Beginner indicator MT5/Beginner.mq5', 'folder': 'Beginner indicator MT5', 'inputs': [{'mql': 'AllBars', 'py': 'AllBars', 'param': 'AllBars', 'type': 'int', 'default': 0, 'label': 'AllBars: How many bars to calculate on. 0 - all.', 'sinput': False}, {'mql': 'Otstup', 'py': 'Otstup', 'param': 'Otstup', 'type': 'int', 'default': 30, 'label': 'Otstup: Percentage distance to consider new low/high.', 'sinput': False}, {'mql': 'Per', 'py': 'Per', 'param': 'Per', 'type': 'int', 'default': 9, 'label': 'Period: Number of bars to seek high/low on.', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AllBars = _input('AllBars', 0)  # AllBars: How many bars to calculate on. 0 - all.
Otstup = _input('Otstup', 30)  # Otstup: Percentage distance to consider new low/high.
Per = _input('Per', 9)  # Period: Number of bars to seek high/low on.
Buf = Arr(0, 0.0)
BufCol = Arr(0, 0.0)
NB = 0
UD = 0

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'Beginner(' + IntegerToString(Per) + ')')
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    SetIndexBuffer(0, Buf, INDICATOR_DATA)
    SetIndexBuffer(1, BufCol, INDICATOR_COLOR_INDEX)

def OnCalculate(rates_total, prev_calculated, time, open, High, Low, Close, tick_volume, volume, spread):
    global NB, UD
    dbOtstup = Otstup
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    if rates_total < (AllBars + Per) or AllBars == 0:
        NB = rates_total - Per
    else:
        NB = AllBars
    CB = prev_calculated
    if CB < 0:
        return -1
    elif NB > (rates_total - CB):
        NB = rates_total - CB + 100
    for SH in range(1, NB):
        R = 0.0
        i = 0
        R = 0.0
        i = SH
        while i < (SH + 10):
            R += (10 + SH - i) * (High[i] - Low[i])
            i += 1
        R = R / 55
        SHMax = High[ArrayMaximum(High, SH, Per)]
        SHMin = Low[ArrayMinimum(Low, SH, Per)]
        diff = ((SHMax - SHMin) * dbOtstup) / 100.0
        Buf[rates_total - SH - 1] = EMPTY_VALUE
        if Close[SH] < (SHMin + diff) and UD != -1:
            Buf[rates_total - SH - 1] = Low[SH] - (R * 0.5)
            BufCol[rates_total - SH - 1] = 0.0
            UD = -1
        elif Close[SH] > (SHMax - diff) and UD != 1:
            Buf[rates_total - SH - 1] = High[SH] + (R * 0.5)
            BufCol[rates_total - SH - 1] = 1.0
            UD = 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Beginner(_MQL5Indicator):
    name = 'Beginner'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'AllBars': 0,  # AllBars: How many bars to calculate on. 0 - all.
        'Otstup': 30,  # Otstup: Percentage distance to consider new low/high.
        'Per': 9,  # Period: Number of bars to seek high/low on.
    }

