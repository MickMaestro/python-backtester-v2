"""nearest_neighbor_-_weighted_corr — converted from MQL5: MQL5 Indicators/Price prediction by Nearest Neighbor found by a weighted correlation coefficient/nearest_neighbor_-_weighted_corr.mq5

Prediction of future based on the nearest neighbor in the past
Copyright: gpwr; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'gpwr', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'NN future', 2: 'NN past'}, 'levels': [], 'description': ['Prediction of future based on the nearest neighbor in the past'], 'name': 'nearest_neighbor_-_weighted_corr', 'source': 'MQL5 Indicators/Price prediction by Nearest Neighbor found by a weighted correlation coefficient/nearest_neighbor_-_weighted_corr.mq5', 'folder': 'Price prediction by Nearest Neighbor found by a weighted correlation coefficient', 'inputs': [{'mql': 'Npast', 'py': 'Npast', 'param': 'Npast', 'type': 'int', 'default': 300, 'label': '# of past bars in a pattern', 'sinput': False}, {'mql': 'Nfut', 'py': 'Nfut', 'param': 'Nfut', 'type': 'int', 'default': 50, 'label': '# of future bars in a pattern (must be < Npast)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Npast = _input('Npast', 300)  # # of past bars in a pattern
Nfut = _input('Nfut', 50)  # # of future bars in a pattern (must be < Npast)
PrevBars = 0
si = 0
mx = Arr(0, 0.0)
sxx = Arr(0, 0.0)
denx = Arr(0, 0.0)
sumx = 0.0
sumxx = 0.0
FirstTime = False
ynn = Arr(0, 0.0)
xnn = Arr(0, 0.0)

def OnInit():
    global FirstTime, PrevBars, si
    PrevBars = Bars(Symbol(), Period()) - 1
    FirstTime = True
    si = _idiv(Npast * (Npast + 1), 2)
    SetIndexBuffer(0, ynn, INDICATOR_DATA)
    SetIndexBuffer(1, xnn, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, '1NN(' + _str(Npast) + ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, Nfut)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    global FirstTime, PrevBars, sumx, sumxx
    bars = rates_total
    if bars < (Npast + Nfut):
        Print('Error: not enough bars in history!')
        return 0
    if PrevBars == bars:
        return rates_total
    PrevBars = bars
    ArrayInitialize(xnn, EMPTY_VALUE)
    ArrayInitialize(ynn, EMPTY_VALUE)
    my = 0.0
    syy = 0.0
    for i in range(0, Npast):
        y = Open[bars - Npast + i]
        my += y * (i + 1)
        syy += y * y * (i + 1)
    deny = (syy * si) - (my * my)
    if deny <= 0:
        Print('Zero or negative syy*si-my*my = ', deny)
        return 0
    deny = MathSqrt(deny)
    ArrayResize(mx, bars - Npast - Nfut + 1)
    ArrayResize(sxx, bars - Npast - Nfut + 1)
    ArrayResize(denx, bars - Npast - Nfut + 1)
    kstart = 0
    if FirstTime:
        kstart = 0
    else:
        kstart = bars - Npast - Nfut
    FirstTime = False
    for k in range(kstart, bars - Npast - Nfut + 1):
        if k == 0:
            mx[0] = 0.0
            sxx[0] = 0.0
            sumx = 0.0
            sumxx = 0.0
            for i in range(0, Npast):
                x = Open[i]
                xx = x * x
                mx[0] += x * (i + 1)
                sxx[0] += xx * (i + 1)
                sumx += x
                sumxx += xx
        else:
            xnew = Open[k + Npast - 1]
            xold = Open[k - 1]
            mx[k] = mx[k - 1] - sumx + (xnew * Npast)
            sxx[k] = sxx[k - 1] - sumxx + (xnew * xnew * Npast)
            sumx += xnew - xold
            sumxx += (xnew * xnew) - (xold * xold)
        denx[k] = (sxx[k] * si) - (mx[k] * mx[k])
    sxy = Arr(0, 0.0)
    ArrayResize(sxy, bars - Npast - Nfut + 1)
    b = 0.0
    corrMax = 0.0
    knn = 0
    for k in range(0, bars - Npast - Nfut + 1):
        sxy[k] = 0.0
        for i in range(0, Npast):
            sxy[k] += Open[k + i] * Open[bars - Npast + i] * (i + 1)
        if denx[k] <= 0:
            Print('Zero or negative sxx[k]*si-mx[k]*mx[k]. Skipping pattern # ', k)
            continue
        num = (sxy[k] * si) - (mx[k] * my)
        corr = _fdiv(_fdiv(num, MathSqrt(denx[k])), deny)
        if corr > corrMax:
            corrMax = corr
            knn = k
            b = _fdiv(num, denx[k])
    Print('Nearest neighbor starts on ', Time[knn], ' and ends on ', Time[knn + Npast - 1], '. Its correlation coefficient with current pattern is ', corrMax)
    delta = Open[bars - 1] - (b * Open[knn + Npast - 1])
    for i in range(0, Npast + Nfut):
        if i <= (Npast - 1):
            xnn[bars - Npast + i] = (b * Open[knn + i]) + delta
        if i >= (Npast - 1):
            ynn[bars - Npast - Nfut + i] = (b * Open[knn + i]) + delta
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NearestNeighborWeightedCorr(_MQL5Indicator):
    name = 'nearest_neighbor_-_weighted_corr'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Npast': 300,  # # of past bars in a pattern
        'Nfut': 50,  # # of future bars in a pattern (must be < Npast)
    }

