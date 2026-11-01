"""multi_rsi — converted from MQL5: MQL5 Indicators/Multi RSI/multi_rsi.mq5

Multi RSI
Copyright: Copyright © 2009, Andrey Matvievskiy; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Andrey Matvievskiy', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 8, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [255], 2: [42495], 3: [55295], 4: [65280], 5: [16776960], 6: [16711680], 7: [8388736], 8: [12632256]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'styles': {}, 'labels': {1: 'RSI 1', 2: 'RSI 2', 3: 'RSI 3', 4: 'RSI 4', 5: 'RSI 5', 6: 'RSI 6', 7: 'RSI 7', 8: 'RSI 8'}, 'levels': [70.0, 50.0, 30.0], 'description': ['Multi RSI'], 'name': 'multi_rsi', 'source': 'MQL5 Indicators/Multi RSI/multi_rsi.mq5', 'folder': 'Multi RSI', 'inputs': [{'mql': 'RSI_Period1', 'py': 'RSI_Period1', 'param': 'RSI_Period1', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'RSI_Price1', 'py': 'RSI_Price1', 'param': 'RSI_Price1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Period2', 'py': 'RSI_Period2', 'param': 'RSI_Period2', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'RSI_Price2', 'py': 'RSI_Price2', 'param': 'RSI_Price2', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Period3', 'py': 'RSI_Period3', 'param': 'RSI_Period3', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'RSI_Price3', 'py': 'RSI_Price3', 'param': 'RSI_Price3', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Period4', 'py': 'RSI_Period4', 'param': 'RSI_Period4', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'RSI_Price4', 'py': 'RSI_Price4', 'param': 'RSI_Price4', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Period5', 'py': 'RSI_Period5', 'param': 'RSI_Period5', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'RSI_Price5', 'py': 'RSI_Price5', 'param': 'RSI_Price5', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Period6', 'py': 'RSI_Period6', 'param': 'RSI_Period6', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'RSI_Price6', 'py': 'RSI_Price6', 'param': 'RSI_Price6', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Period7', 'py': 'RSI_Period7', 'param': 'RSI_Period7', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'RSI_Price7', 'py': 'RSI_Price7', 'param': 'RSI_Price7', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Period8', 'py': 'RSI_Period8', 'param': 'RSI_Period8', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'RSI_Price8', 'py': 'RSI_Price8', 'param': 'RSI_Price8', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RSI_Period1 = _input('RSI_Period1', 2)
RSI_Price1 = _input('RSI_Price1', PRICE_CLOSE)
RSI_Period2 = _input('RSI_Period2', 4)
RSI_Price2 = _input('RSI_Price2', PRICE_CLOSE)
RSI_Period3 = _input('RSI_Period3', 3)
RSI_Price3 = _input('RSI_Price3', PRICE_CLOSE)
RSI_Period4 = _input('RSI_Period4', 6)
RSI_Price4 = _input('RSI_Price4', PRICE_CLOSE)
RSI_Period5 = _input('RSI_Period5', 4)
RSI_Price5 = _input('RSI_Price5', PRICE_CLOSE)
RSI_Period6 = _input('RSI_Period6', 8)
RSI_Price6 = _input('RSI_Price6', PRICE_CLOSE)
RSI_Period7 = _input('RSI_Period7', 5)
RSI_Price7 = _input('RSI_Price7', PRICE_CLOSE)
RSI_Period8 = _input('RSI_Period8', 10)
RSI_Price8 = _input('RSI_Price8', PRICE_CLOSE)
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
Buffer3 = Arr(0, 0.0)
Buffer4 = Arr(0, 0.0)
Buffer5 = Arr(0, 0.0)
Buffer6 = Arr(0, 0.0)
Buffer7 = Arr(0, 0.0)
Buffer8 = Arr(0, 0.0)
min_rates_total = 0
RSI_Handle = Arr(8, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = MathMax(RSI_Period1, MathMax(RSI_Period2, MathMax(RSI_Period3, MathMax(RSI_Period4, MathMax(RSI_Period5, MathMax(RSI_Period6, MathMax(RSI_Period7, RSI_Period8))))))) + 1
    RSI_Handle[0] = iRSI(None, 0, RSI_Period1, RSI_Price1)
    if RSI_Handle[0] == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI 1 indicator')
        return 1
    RSI_Handle[1] = iRSI(None, 0, RSI_Period2, RSI_Price2)
    if RSI_Handle[1] == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI 2 indicator')
        return 1
    RSI_Handle[2] = iRSI(None, 0, RSI_Period3, RSI_Price3)
    if RSI_Handle[2] == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI 3 indicator')
        return 1
    RSI_Handle[3] = iRSI(None, 0, RSI_Period4, RSI_Price4)
    if RSI_Handle[3] == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI 4 indicator')
        return 1
    RSI_Handle[4] = iRSI(None, 0, RSI_Period5, RSI_Price5)
    if RSI_Handle[4] == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI 5 indicator')
        return 1
    RSI_Handle[5] = iRSI(None, 0, RSI_Period6, RSI_Price6)
    if RSI_Handle[5] == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI 6 indicator')
        return 1
    RSI_Handle[6] = iRSI(None, 0, RSI_Period7, RSI_Price7)
    if RSI_Handle[6] == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI 7 indicator')
        return 1
    RSI_Handle[7] = iRSI(None, 0, RSI_Period8, RSI_Price8)
    if RSI_Handle[7] == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI 8 indicator')
        return 1
    SetIndexBuffer(0, Buffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, RSI_Period1)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    ArraySetAsSeries(Buffer1, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, Buffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, RSI_Period2)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    ArraySetAsSeries(Buffer2, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, Buffer3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, RSI_Period3)
    PlotIndexSetInteger(2, PLOT_ARROW, 233)
    ArraySetAsSeries(Buffer3, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, Buffer4, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, RSI_Period4)
    PlotIndexSetInteger(3, PLOT_ARROW, 234)
    ArraySetAsSeries(Buffer4, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(4, Buffer5, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, RSI_Period5)
    PlotIndexSetInteger(4, PLOT_ARROW, 233)
    ArraySetAsSeries(Buffer5, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(5, Buffer6, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, RSI_Period6)
    PlotIndexSetInteger(5, PLOT_ARROW, 234)
    ArraySetAsSeries(Buffer6, True)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(6, Buffer7, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, RSI_Period7)
    PlotIndexSetInteger(6, PLOT_ARROW, 233)
    ArraySetAsSeries(Buffer7, True)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(7, Buffer8, INDICATOR_DATA)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, RSI_Period8)
    PlotIndexSetInteger(7, PLOT_ARROW, 234)
    ArraySetAsSeries(Buffer8, True)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Multi RSI'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for numb in range(0, 8):
        if BarsCalculated(RSI_Handle[numb]) < rates_total:
            return 0
    if rates_total < min_rates_total:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total - 1
    else:
        to_copy = rates_total - prev_calculated + 1
    if CopyBuffer(RSI_Handle[0], 0, 0, to_copy, Buffer1) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[1], 0, 0, to_copy, Buffer2) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[2], 0, 0, to_copy, Buffer3) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[3], 0, 0, to_copy, Buffer4) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[4], 0, 0, to_copy, Buffer5) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[5], 0, 0, to_copy, Buffer6) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[6], 0, 0, to_copy, Buffer7) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[7], 0, 0, to_copy, Buffer8) <= 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultiRsi(_MQL5Indicator):
    name = 'multi_rsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSI_Period1': 2,
        'RSI_Price1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Period2': 4,
        'RSI_Price2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Period3': 3,
        'RSI_Price3': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Period4': 6,
        'RSI_Price4': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Period5': 4,
        'RSI_Price5': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Period6': 8,
        'RSI_Price6': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Period7': 5,
        'RSI_Price7': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Period8': 10,
        'RSI_Price8': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }
    y_range = (0.0, 100.0)

