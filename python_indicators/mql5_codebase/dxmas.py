"""dxmas — converted from MQL5: MQL5 Indicators/DXMA/dxmas.mq5

DMI expanded MA
Copyright: 2010, kurl; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, kurl', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [15453831]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'DXMAs'}, 'levels': [], 'description': ['DMI expanded MA'], 'name': 'dxmas', 'source': 'MQL5 Indicators/DXMA/dxmas.mq5', 'folder': 'DXMA', 'inputs': [{'mql': 'MAperiod', 'py': 'MAperiod', 'param': 'MAperiod', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAperiod = _input('MAperiod', 20)
D = Arr(0, 0.0)
C = Arr(0, 0.0)
P = Arr(0, 0.0)
M = Arr(0, 0.0)
hADX = 0  # handle

def OnInit():
    global hADX
    label = 'DXMA(' + _str(MAperiod) + ')'
    SetIndexBuffer(0, D, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MAperiod)
    PlotIndexSetString(0, PLOT_LABEL, label)
    SetIndexBuffer(1, P, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, C, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, M, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    hADX = iADX(Symbol(), Period(), MAperiod)

def OnCalculate(rates_total, prev_calculated, begin, price):
    hi = Arr(0, 0.0)
    lo = Arr(0, 0.0)
    ArrayResize(hi, MAperiod)
    ArrayResize(lo, MAperiod)
    n = 0
    i = 0
    limit = 0
    if prev_calculated == 0:
        n = rates_total
    else:
        n = rates_total - prev_calculated + 1
    if CopyBuffer(hADX, 1, 0, n, P) <= 0:
        return 0
    if CopyBuffer(hADX, 2, 0, n, M) <= 0:
        return 0
    if prev_calculated == 0:
        limit = MAperiod
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        s = rates_total - 1 - i
        if CopyHigh(Symbol(), Period(), s, MAperiod, hi) <= 0:
            return 0
        if CopyLow(Symbol(), Period(), s, MAperiod, lo) <= 0:
            return 0
        ydi = P[i] - M[i] + 50
        h = NormalizeDouble(hi[ArrayMaximum(hi)], Digits() - 1)
        l = NormalizeDouble(lo[ArrayMinimum(lo)], Digits() - 1)
        C[i] = ((h - l) * ydi * 0.01) + l
    else:
        i = _range_end(i, rates_total, 1)
    i = limit
    for i in range(i, rates_total):
        sum_ = 0.0
        for j in range(0, MAperiod):
            sum_ += C[i - j]
        D[i] = sum_ / MAperiod
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dxmas(_MQL5Indicator):
    name = 'dxmas'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAperiod': 20,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

