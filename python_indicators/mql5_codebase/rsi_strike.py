"""rsi_strike — converted from MQL5: MQL5 Indicators/RSI Strike/rsi_strike.mq5

RSI Strike
Copyright: Copyright © 2009, Andrey Matvievskiy; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Andrey Matvievskiy', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 'colors': {1: [16776960], 2: [16776960], 3: [12632256], 4: [12632256], 5: [42495], 6: [42495], 7: [255], 8: [255]}, 'widths': {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4}, 'styles': {}, 'labels': {1: 'RSI_Strike 1 Buy', 2: 'RSI_Strike 1 Sell', 3: 'RSI_Strike 2 Buy', 4: 'RSI_Strike 2 Sell', 5: 'RSI_Strike 3 Buy', 6: 'RSI_Strike 3 Sell', 7: 'RSI_Strike 4 Buy', 8: 'RSI_Strike 4 Sell'}, 'levels': [], 'description': ['RSI Strike'], 'name': 'rsi_strike', 'source': 'MQL5 Indicators/RSI Strike/rsi_strike.mq5', 'folder': 'RSI Strike', 'inputs': [{'mql': 'RSI_Period1', 'py': 'RSI_Period1', 'param': 'RSI_Period1', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'RSI_Period2', 'py': 'RSI_Period2', 'param': 'RSI_Period2', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'RSI_Price1', 'py': 'RSI_Price1', 'param': 'RSI_Price1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Price2', 'py': 'RSI_Price2', 'param': 'RSI_Price2', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Period3', 'py': 'RSI_Period3', 'param': 'RSI_Period3', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'RSI_Period4', 'py': 'RSI_Period4', 'param': 'RSI_Period4', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'RSI_Price3', 'py': 'RSI_Price3', 'param': 'RSI_Price3', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Price4', 'py': 'RSI_Price4', 'param': 'RSI_Price4', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Period5', 'py': 'RSI_Period5', 'param': 'RSI_Period5', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'RSI_Period6', 'py': 'RSI_Period6', 'param': 'RSI_Period6', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'RSI_Price5', 'py': 'RSI_Price5', 'param': 'RSI_Price5', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Price6', 'py': 'RSI_Price6', 'param': 'RSI_Price6', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Period7', 'py': 'RSI_Period7', 'param': 'RSI_Period7', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'RSI_Period8', 'py': 'RSI_Period8', 'param': 'RSI_Period8', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'RSI_Price7', 'py': 'RSI_Price7', 'param': 'RSI_Price7', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSI_Price8', 'py': 'RSI_Price8', 'param': 'RSI_Price8', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RSI_Period1 = _input('RSI_Period1', 2)
RSI_Period2 = _input('RSI_Period2', 4)
RSI_Price1 = _input('RSI_Price1', PRICE_CLOSE)
RSI_Price2 = _input('RSI_Price2', PRICE_CLOSE)
RSI_Period3 = _input('RSI_Period3', 3)
RSI_Period4 = _input('RSI_Period4', 6)
RSI_Price3 = _input('RSI_Price3', PRICE_CLOSE)
RSI_Price4 = _input('RSI_Price4', PRICE_CLOSE)
RSI_Period5 = _input('RSI_Period5', 4)
RSI_Period6 = _input('RSI_Period6', 8)
RSI_Price5 = _input('RSI_Price5', PRICE_CLOSE)
RSI_Price6 = _input('RSI_Price6', PRICE_CLOSE)
RSI_Period7 = _input('RSI_Period7', 5)
RSI_Period8 = _input('RSI_Period8', 10)
RSI_Price7 = _input('RSI_Price7', PRICE_CLOSE)
RSI_Price8 = _input('RSI_Price8', PRICE_CLOSE)
CrossUp1 = Arr(0, 0.0)
CrossDown1 = Arr(0, 0.0)
CrossUp2 = Arr(0, 0.0)
CrossDown2 = Arr(0, 0.0)
CrossUp3 = Arr(0, 0.0)
CrossDown3 = Arr(0, 0.0)
CrossUp4 = Arr(0, 0.0)
CrossDown4 = Arr(0, 0.0)
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
    SetIndexBuffer(0, CrossUp1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    ArraySetAsSeries(CrossUp1, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, CrossDown1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    ArraySetAsSeries(CrossDown1, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, CrossUp2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 233)
    ArraySetAsSeries(CrossUp2, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, CrossDown2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 234)
    ArraySetAsSeries(CrossDown2, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(4, CrossUp3, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 233)
    ArraySetAsSeries(CrossUp3, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(5, CrossDown3, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_ARROW, 234)
    ArraySetAsSeries(CrossDown3, True)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(6, CrossUp4, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_ARROW, 233)
    ArraySetAsSeries(CrossUp4, True)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(7, CrossDown4, INDICATOR_DATA)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(7, PLOT_ARROW, 234)
    ArraySetAsSeries(CrossDown4, True)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'RSI_Strike'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for numb in range(0, 8):
        if BarsCalculated(RSI_Handle[numb]) < rates_total:
            return 0
    if rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Range = 0.0
    AvgRange = 0.0
    RSI1 = Arr(0, 0.0)
    RSI2 = Arr(0, 0.0)
    RSI3 = Arr(0, 0.0)
    RSI4 = Arr(0, 0.0)
    RSI5 = Arr(0, 0.0)
    RSI6 = Arr(0, 0.0)
    RSI7 = Arr(0, 0.0)
    RSI8 = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(RSI_Handle[0], 0, 0, to_copy, RSI1) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[1], 0, 0, to_copy, RSI2) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[2], 0, 0, to_copy, RSI3) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[3], 0, 0, to_copy, RSI4) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[4], 0, 0, to_copy, RSI5) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[5], 0, 0, to_copy, RSI6) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[6], 0, 0, to_copy, RSI7) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[7], 0, 0, to_copy, RSI8) <= 0:
        return 0
    ArraySetAsSeries(RSI1, True)
    ArraySetAsSeries(RSI2, True)
    ArraySetAsSeries(RSI3, True)
    ArraySetAsSeries(RSI4, True)
    ArraySetAsSeries(RSI5, True)
    ArraySetAsSeries(RSI6, True)
    ArraySetAsSeries(RSI7, True)
    ArraySetAsSeries(RSI8, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        AvgRange = 0.0
        for count in range(bar, bar + 9 + 1):
            AvgRange += MathAbs(high[count] - low[count])
        Range = AvgRange / 10
        CrossUp1[bar] = 0.0
        CrossDown1[bar] = 0.0
        CrossUp2[bar] = 0.0
        CrossDown2[bar] = 0.0
        CrossUp3[bar] = 0.0
        CrossDown3[bar] = 0.0
        CrossUp4[bar] = 0.0
        CrossDown4[bar] = 0.0
        if RSI1[bar] > RSI2[bar] and RSI1[bar + 1] < RSI2[bar + 1]:
            CrossUp1[bar] = low[bar] - (Range * 0.2)
        elif RSI1[bar] < RSI2[bar] and RSI1[bar + 1] > RSI2[bar + 1]:
            CrossDown1[bar] = high[bar] + (Range * 0.2)
        if RSI3[bar] > RSI4[bar] and RSI3[bar + 1] < RSI4[bar + 1]:
            CrossUp2[bar] = low[bar] - (Range * 0.4)
        elif RSI3[bar] < RSI4[bar] and RSI3[bar + 1] > RSI4[bar + 1]:
            CrossDown2[bar] = high[bar] + (Range * 0.4)
        if RSI5[bar] > RSI6[bar] and RSI5[bar + 1] < RSI6[bar + 1]:
            CrossUp3[bar] = low[bar] - (Range * 0.6)
        elif RSI5[bar] < RSI6[bar] and RSI5[bar + 1] > RSI6[bar + 1]:
            CrossDown3[bar] = high[bar] + (Range * 0.6)
        if RSI7[bar] > RSI8[bar] and RSI7[bar + 1] < RSI8[bar + 1]:
            CrossUp4[bar] = low[bar] - (Range * 0.8)
        elif RSI7[bar] < RSI8[bar] and RSI7[bar + 1] > RSI8[bar + 1]:
            CrossDown4[bar] = high[bar] + (Range * 0.8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RsiStrike(_MQL5Indicator):
    name = 'rsi_strike'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSI_Period1': 2,
        'RSI_Period2': 4,
        'RSI_Price1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Price2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Period3': 3,
        'RSI_Period4': 6,
        'RSI_Price3': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Price4': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Period5': 4,
        'RSI_Period6': 8,
        'RSI_Price5': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Price6': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Period7': 5,
        'RSI_Period8': 10,
        'RSI_Price7': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSI_Price8': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

