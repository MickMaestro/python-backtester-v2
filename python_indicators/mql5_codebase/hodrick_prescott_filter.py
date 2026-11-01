"""hodrick-prescott_filter — converted from MQL5: MQL5 Indicators/The Hodrick-Prescott Filter/hodrick-prescott_filter.mq5

Hodrick-Prescott Filter
Copyright: gpwr; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'gpwr', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'filter'}, 'levels': [], 'description': ['Hodrick-Prescott Filter'], 'name': 'hodrick-prescott_filter', 'source': 'MQL5 Indicators/The Hodrick-Prescott Filter/hodrick-prescott_filter.mq5', 'folder': 'The Hodrick-Prescott Filter', 'inputs': [{'mql': 'Per', 'py': 'Per', 'param': 'Per', 'type': 'int', 'default': 50, 'label': 'HP filter period', 'sinput': False}, {'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 500, 'label': '# of prices to smooth', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Per = _input('Per', 50)  # HP filter period
N = _input('N', 500)  # # of prices to smooth
PrevBars = 0
Lambda = 0.0
hpf = Arr(0, 0.0)

def OnInit():
    global Lambda, PrevBars
    PrevBars = Bars(Symbol(), Period()) - 1
    Lambda = _fdiv(0.0625, MathPow(MathSin(M_PI / Per), 4))
    ArraySetAsSeries(hpf, True)
    SetIndexBuffer(0, hpf, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'HPF(' + _str(Per) + ')')

def OnCalculate(bars, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    global PrevBars
    if bars < N:
        Print('Error: not enough bars in history!')
        return 0
    if PrevBars == bars:
        return bars
    PrevBars = bars
    ArrayInitialize(hpf, EMPTY_VALUE)
    ArraySetAsSeries(Open, True)
    for i in range(0, N):
        hpf[i] = Open[i]
    HPF(N, Lambda, hpf)
    return bars

def HPF(n, lambda_, x):
    a = Arr(0, 0.0)
    b = Arr(0, 0.0)
    c = Arr(0, 0.0)
    h1 = 0.0
    h2 = 0.0
    h3 = 0.0
    h4 = 0.0
    h5 = 0.0
    hh1 = 0.0
    hh2 = 0.0
    hh3 = 0.0
    hh5 = 0.0
    hb = 0.0
    hc = 0.0
    z = 0.0
    ArrayResize(a, n)
    ArrayResize(b, n)
    ArrayResize(c, n)
    ArrayInitialize(a, 0.0)
    ArrayInitialize(b, 0.0)
    ArrayInitialize(c, 0.0)
    a[0] = 1.0 + lambda_
    b[0] = -2.0 * lambda_
    c[0] = lambda_
    for i in range(1, n - 2):
        a[i] = (6.0 * lambda_) + 1.0
        b[i] = -4.0 * lambda_
        c[i] = lambda_
    a[1] = (5.0 * lambda_) + 1
    a[n - 1] = 1.0 + lambda_
    a[n - 2] = (5.0 * lambda_) + 1.0
    b[n - 2] = -2.0 * lambda_
    b[n - 1] = 0.0
    c[n - 2] = 0.0
    c[n - 1] = 0.0
    for i in range(0, n):
        z = a[i] - (h4 * h1) - (hh5 * hh2)
        hb = b[i]
        hh1 = h1
        h1 = _fdiv(hb - (h4 * h2), z)
        b[i] = h1
        hc = c[i]
        hh2 = h2
        h2 = _fdiv(hc, z)
        c[i] = h2
        a[i] = _fdiv(x[i] - (hh3 * hh5) - (h3 * h4), z)
        hh3 = h3
        h3 = a[i]
        h4 = hb - (h5 * hh1)
        hh5 = h5
        h5 = hc
    h2 = 0.0
    h1 = a[n - 1]
    x[n - 1] = h1
    for i in range(n - 2, 0 - 1, -1):
        x[i] = a[i] - (b[i] * h1) - (c[i] * h2)
        h2 = h1
        h1 = x[i]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HodrickPrescottFilter(_MQL5Indicator):
    name = 'hodrick-prescott_filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Per': 50,  # HP filter period
        'N': 500,  # # of prices to smooth
    }

