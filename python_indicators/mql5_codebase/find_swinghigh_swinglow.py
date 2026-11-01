"""Find_SwingHigh_SwingLow — converted from MQL5: MQL5 Indicators/Find Swing Highs  Swing Lows/Find_SwingHigh_SwingLow.mq5

 Finds swing highs and swing lows, use it with any \\n 
 market structure strategy
Copyright: Copyright 2024, Indices Group (Pty) Ltd; Link: https://indices-investment-group.thinkific.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Indices Group (Pty) Ltd', 'link': 'https://indices-investment-group.thinkific.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Swing High', 2: 'Swing Low'}, 'levels': [], 'description': [' Finds swing highs and swing lows, use it with any \\n ', ' market structure strategy'], 'name': 'Find_SwingHigh_SwingLow', 'source': 'MQL5 Indicators/Find Swing Highs  Swing Lows/Find_SwingHigh_SwingLow.mq5', 'folder': 'Find Swing Highs  Swing Lows', 'inputs': [{'mql': 'InpRangeBars', 'py': 'InpRangeBars', 'param': 'InpRangeBars', 'type': 'int', 'default': 12, 'label': 'Number of bars to check on each side', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpRangeBars = _input('InpRangeBars', 12)  # Number of bars to check on each side
SwingHighBuffer = Arr(0, 0.0)
SwingLowBuffer = Arr(0, 0.0)
H1 = 0.0
L1 = 0.0
H1Time = 0
L1Time = 0

def OnInit():
    SetIndexBuffer(0, SwingHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SwingLowBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Improved Swing High/Low Identifier'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global H1, H1Time, L1, L1Time
    start = 0
    if prev_calculated == 0:
        start = InpRangeBars
    else:
        start = prev_calculated - 1
    for i in range(start, rates_total - InpRangeBars):
        SwingHighBuffer[i] = EMPTY_VALUE
        SwingLowBuffer[i] = EMPTY_VALUE
        isSwingHigh = True
        isSwingLow = True
        for j in range(1, InpRangeBars + 1):
            if high[i] <= high[i + j] or high[i] <= high[i - j]:
                isSwingHigh = False
                break
        for j in range(1, InpRangeBars + 1):
            if low[i] >= low[i + j] or low[i] >= low[i - j]:
                isSwingLow = False
                break
        if isSwingHigh:
            SwingHighBuffer[i] = high[i]
            CreateLabel('SwingHigh_' + IntegerToString(i), time[i], high[i], 'H', clrRed)
            if high[i] > H1 or H1 == 0:
                H1 = high[i]
                H1Time = time[i]
        if isSwingLow:
            SwingLowBuffer[i] = low[i]
            CreateLabel('SwingLow_' + IntegerToString(i), time[i], low[i], 'L', clrBlue)
            if low[i] < L1 or L1 == 0:
                L1 = low[i]
                L1Time = time[i]
    return rates_total

def CreateLabel(name, time, price, text, clr):
    ObjectCreate(0, name, OBJ_TEXT, 0, time, price)
    ObjectSetString(0, name, OBJPROP_TEXT, text)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 8)
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'SwingHigh_')
    ObjectsDeleteAll(0, 'SwingLow_')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FindSwingHighSwingLow(_MQL5Indicator):
    name = 'Find_SwingHigh_SwingLow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpRangeBars': 12,  # Number of bars to check on each side
    }

