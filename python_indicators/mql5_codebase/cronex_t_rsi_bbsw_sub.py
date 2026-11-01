"""Cronex_T_RSI_BBSW_sub — converted from MQL5: MQL5 Indicators/Cronex T RSI BBSW/Cronex_T_RSI_BBSW_sub.mq5

Copyright: Copyright © 2017, Cronex; Link: http://www.metaquotes.net/

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Cronex', 'link': 'http://www.metaquotes.net/', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {}, 'colors': {1: [36095], 2: [11829830]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [10.0, -10.0], 'description': [], 'name': 'Cronex_T_RSI_BBSW_sub', 'source': 'MQL5 Indicators/Cronex T RSI BBSW/Cronex_T_RSI_BBSW_sub.mq5', 'folder': 'Cronex T RSI BBSW', 'inputs': [{'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'int', 'default': 16, 'label': '', 'sinput': False}, {'mql': 'TCurvature', 'py': 'TCurvature', 'param': 'TCurvature', 'type': 'double', 'default': 0.618, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RSIPeriod = _input('RSIPeriod', 16)
TCurvature = _input('TCurvature', 0.618)
RSITArray = Arr(0, 0.0)
RSIArray = Arr(0, 0.0)
e1 = 0.0
e2 = 0.0
e3 = 0.0
e4 = 0.0
e5 = 0.0
e6 = 0.0
c1 = 0.0
c2 = 0.0
c3 = 0.0
c4 = 0.0
n = 0.0
w1 = 0.0
w2 = 0.0
b2 = 0.0
b3 = 0.0
RSIHandle0 = 0
RSIHandle1 = 0
RSIHandle2 = 0
RSIHandle3 = 0
RSIBuffer0 = Arr(0, 0.0)
RSIBuffer1 = Arr(0, 0.0)
RSIBuffer2 = Arr(0, 0.0)
RSIBuffer3 = Arr(0, 0.0)

def OnInit():
    global RSIHandle0, RSIHandle1, RSIHandle2, RSIHandle3, b2, b3, c1, c2, c3, c4, e1, e2, e3, e4, e5, e6, n, w1, w2
    SetIndexBuffer(0, RSITArray, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, RSIArray, INDICATOR_DATA)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetString(0, PLOT_LABEL, 'RSI T')
    PlotIndexSetString(1, PLOT_LABEL, 'RSI')
    IndicatorSetInteger(INDICATOR_DIGITS, _int(SymbolInfoInteger(None, SYMBOL_DIGITS)))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Cronex T RSI BBS (' + IntegerToString(RSIPeriod) + ')')
    e1 = 0.0
    e2 = 0.0
    e3 = 0.0
    e4 = 0.0
    e5 = 0.0
    e6 = 0.0
    c1 = 0.0
    c2 = 0.0
    c3 = 0.0
    c4 = 0.0
    n = 0.0
    w1 = 0.0
    w2 = 0.0
    b2 = 0.0
    b3 = 0.0
    b2 = TCurvature * TCurvature
    b3 = b2 * TCurvature
    c1 = -b3
    c2 = 3 * (b2 + b3)
    c3 = -3 * ((2 * b2) + TCurvature + b3)
    c4 = 1 + (3 * TCurvature) + b3 + (3 * b2)
    n = float(RSIPeriod)
    if n < 1:
        n = 1.0
    n = 1 + (0.5 * (n - 1))
    w1 = _fdiv(2, n + 1)
    w2 = 1 - w1
    RSIHandle0 = iRSI(None, 0, RSIPeriod + (4 * 0), PRICE_WEIGHTED)
    RSIHandle1 = iRSI(None, 0, RSIPeriod + (4 * 1), PRICE_WEIGHTED)
    RSIHandle2 = iRSI(None, 0, RSIPeriod + (4 * 2), PRICE_WEIGHTED)
    RSIHandle3 = iRSI(None, 0, RSIPeriod + (4 * 3), PRICE_WEIGHTED)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global e1, e2, e3, e4, e5, e6
    to_calc = rates_total - prev_calculated
    CopyBuffer(RSIHandle0, 0, 0, to_calc, RSIBuffer0)
    CopyBuffer(RSIHandle1, 0, 0, to_calc, RSIBuffer1)
    CopyBuffer(RSIHandle2, 0, 0, to_calc, RSIBuffer2)
    CopyBuffer(RSIHandle3, 0, 0, to_calc, RSIBuffer3)
    i = 0
    c = 0
    i = 0
    for i in range(i, to_calc):
        c = prev_calculated + i
        RSIArray[c] = ((RSIBuffer0[i] + RSIBuffer1[i] + RSIBuffer2[i] + RSIBuffer3[i]) / 4) - 50
        if RSIArray[c] <= 100 and RSIArray[c] >= -100:
            e1 = (w1 * RSIArray[c]) + (w2 * e1)
            e2 = (w1 * e1) + (w2 * e2)
            e3 = (w1 * e2) + (w2 * e3)
            e4 = (w1 * e3) + (w2 * e4)
            e5 = (w1 * e4) + (w2 * e5)
            e6 = (w1 * e5) + (w2 * e6)
            RSITArray[c] = (c1 * e6) + (c2 * e5) + (c3 * e4) + (c4 * e3)
        else:
            RSIArray[c] = 0.0
            RSITArray[c] = 0.0
    else:
        i = _range_end(i, to_calc, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CronexTRSIBBSWSub(_MQL5Indicator):
    name = 'Cronex_T_RSI_BBSW_sub'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIPeriod': 16,
        'TCurvature': 0.618,
    }

