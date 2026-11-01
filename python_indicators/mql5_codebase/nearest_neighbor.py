"""nearest_neighbor — converted from MQL5: MQL5 Indicators/Price prediction by Nearest Neighbor/nearest_neighbor.mq5

Prediction of future based on the nearest neighbor in the past
Copyright: gpwr; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'gpwr', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'NN future', 2: 'NN past'}, 'levels': [], 'description': ['Prediction of future based on the nearest neighbor in the past'], 'name': 'nearest_neighbor', 'source': 'MQL5 Indicators/Price prediction by Nearest Neighbor/nearest_neighbor.mq5', 'folder': 'Price prediction by Nearest Neighbor', 'inputs': [{'mql': 'Npast', 'py': 'Npast', 'param': 'Npast', 'type': 'int', 'default': 300, 'label': 'Past bars in a pattern', 'sinput': False}, {'mql': 'Nfut', 'py': 'Nfut', 'param': 'Nfut', 'type': 'int', 'default': 50, 'label': 'Future bars in a pattern (must be < Npast)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Npast = _input('Npast', 300)  # Past bars in a pattern
Nfut = _input('Nfut', 50)  # Future bars in a pattern (must be < Npast)
bars = 0
PrevBars = 0
mx = Arr(0, 0.0)
sxx = Arr(0, 0.0)
denx = Arr(0, 0.0)
FirstTime = False
ynn = Arr(0, 0.0)
xnn = Arr(0, 0.0)

def OnInit():
    global FirstTime, PrevBars
    PrevBars = Bars(Symbol(), Period()) - 1
    FirstTime = True
    SetIndexBuffer(0, ynn, INDICATOR_DATA)
    SetIndexBuffer(1, xnn, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, '1NN(' + _str(Npast) + ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, Nfut)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    global FirstTime, PrevBars
    bars_ = rates_total
    if bars_ < (Npast + Nfut):
        Print('Error: not enough bars in history!')
        return 0
    if PrevBars == bars_:
        return rates_total
    PrevBars = bars_
    ArrayInitialize(xnn, EMPTY_VALUE)
    ArrayInitialize(ynn, EMPTY_VALUE)
    my = 0.0
    syy = 0.0
    for i in range(0, Npast):
        y = Open[bars_ - Npast + i]
        my += y
        syy += y * y
    deny = (syy * Npast) - (my * my)
    if deny <= 0:
        Print('Zero or negative syy*Npast-my*my = ', deny)
        return 0
    deny = MathSqrt(deny)
    ArrayResize(mx, bars_ - Npast - Nfut + 1)
    ArrayResize(sxx, bars_ - Npast - Nfut + 1)
    ArrayResize(denx, bars_ - Npast - Nfut + 1)
    kstart = 0
    if FirstTime:
        kstart = 0
    else:
        kstart = bars_ - Npast - Nfut
    FirstTime = False
    for k in range(kstart, bars_ - Npast - Nfut + 1):
        if k == 0:
            mx[0] = 0.0
            sxx[0] = 0.0
            for i in range(0, Npast):
                x = Open[i]
                mx[0] += x
                sxx[0] += x * x
        else:
            xnew = Open[k + Npast - 1]
            xold = Open[k - 1]
            mx[k] = mx[k - 1] + xnew - xold
            sxx[k] = sxx[k - 1] + (xnew * xnew) - (xold * xold)
        denx[k] = (sxx[k] * Npast) - (mx[k] * mx[k])
    sxy = Arr(0, 0.0)
    ArrayResize(sxy, bars_ - Npast - Nfut + 1)
    b = 0.0
    corrMax = 0.0
    knn = 0
    for k in range(0, bars_ - Npast - Nfut + 1):
        sxy[k] = 0.0
        for i in range(0, Npast):
            sxy[k] += Open[k + i] * Open[bars_ - Npast + i]
        if denx[k] <= 0:
            Print('Zero or negative sxx[k]*Npast-mx[k]*mx[k]. Skipping pattern # ', k)
            continue
        num = (sxy[k] * Npast) - (mx[k] * my)
        corr = _fdiv(_fdiv(num, MathSqrt(denx[k])), deny)
        if corr > corrMax:
            corrMax = corr
            knn = k
            b = _fdiv(num, denx[k])
    Print('Nearest neighbor is dated ', Time[knn], ' and has correlation with current pattern of ', corrMax)
    delta = Open[bars_ - 1] - (b * Open[knn + Npast - 1])
    for i in range(0, Npast + Nfut):
        if i <= (Npast - 1):
            xnn[bars_ - Npast + i] = (b * Open[knn + i]) + delta
        if i >= (Npast - 1):
            ynn[bars_ - Npast - Nfut + i] = (b * Open[knn + i]) + delta
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NearestNeighbor(_MQL5Indicator):
    name = 'nearest_neighbor'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Npast': 300,  # Past bars in a pattern
        'Nfut': 50,  # Future bars in a pattern (must be < Npast)
    }

