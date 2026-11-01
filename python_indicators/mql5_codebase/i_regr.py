"""i-Regr — converted from MQL5: MQL5 Indicators/Regression Channel with variable polynomial degree/i-Regr.mq5

Copyright: © 2008 BJF Trading Group; Link: www.iticsoftware.com; Version: 1.2

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© 2008 BJF Trading Group', 'link': 'www.iticsoftware.com', 'version': '1.2', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [55295], 2: [3329330], 3: [55295]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'h', 2: 'm', 3: 'l'}, 'levels': [], 'description': [], 'name': 'i-Regr', 'source': 'MQL5 Indicators/Regression Channel with variable polynomial degree/i-Regr.mq5', 'folder': 'Regression Channel with variable polynomial degree', 'inputs': [{'mql': 'degree', 'py': 'degree', 'param': 'degree', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'kstd', 'py': 'kstd', 'param': 'kstd', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'bars', 'py': 'bars', 'param': 'bars', 'type': 'int', 'default': 250, 'label': '', 'sinput': False}, {'mql': 'shift', 'py': 'shift', 'param': 'shift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
degree = _input('degree', 3)
kstd = _input('kstd', 2.0)
bars = _input('bars', 250)
shift = _input('shift', 0)
hBuffer = Arr(0, 0.0)
mBuffer = Arr(0, 0.0)
lBuffer = Arr(0, 0.0)
ai = Arr((10, 10)[-1], 0.0, dyn=False)
b = Arr(10, 0.0, dyn=False)
x = Arr(10, 0.0, dyn=False)
sx = Arr(20, 0.0, dyn=False)
sum_ = 0.0
ip = 0
p = 0
n = 0
f = 0
qq = 0.0
mm = 0.0
tt = 0.0
ii = 0
jj = 0
kk = 0
ll = 0
nn = 0
sq = 0.0
i0 = 0

def OnInit():
    SetIndexBuffer(0, hBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, mBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, lBuffer, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global i0, ii, ip, jj, kk, ll, mm, n, nn, p, qq, sq, sum_, tt
    if rates_total < bars:
        return -1
    mi = 0
    ip = bars
    p = ip
    sx[1] = p + 1
    nn = degree + 1
    i0 = rates_total - p - 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - p - 1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, rates_total - p - 1)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, rates_total - p - 1)
    mi = 1
    for mi in range(mi, (nn * 2) - 2 + 1):
        sum_ = 0.0
        n = i0
        while n <= (i0 + p):
            sum_ += MathPow(n, mi)
            n += 1
        sx[mi + 1] = sum_
    else:
        mi = _range_end(mi, (nn * 2) - 2 + 1, 1)
    mi = 1
    for mi in range(mi, nn + 1):
        sum_ = 0.0
        n = i0
        while n <= (i0 + p):
            if mi == 1:
                sum_ += close[n]
            else:
                sum_ += close[n] * MathPow(n, mi - 1)
            n += 1
        b[mi] = sum_
    else:
        mi = _range_end(mi, nn + 1, 1)
    jj = 1
    while jj <= nn:
        ii = 1
        while ii <= nn:
            kk = ii + jj - 1
            ai[(ii, jj)[-1]] = sx[kk]
            ii += 1
        jj += 1
    kk = 1
    while kk <= (nn - 1):
        ll = 0
        mm = 0.0
        ii = kk
        while ii <= nn:
            if MathAbs(ai[(ii, kk)[-1]]) > mm:
                mm = MathAbs(ai[(ii, kk)[-1]])
                ll = ii
            ii += 1
        if ll == 0:
            return rates_total
        if ll != kk:
            jj = 1
            while jj <= nn:
                tt = ai[(kk, jj)[-1]]
                ai[(kk, jj)[-1]] = ai[(ll, jj)[-1]]
                ai[(ll, jj)[-1]] = tt
                jj += 1
            tt = b[kk]
            b[kk] = b[ll]
            b[ll] = tt
        ii = kk + 1
        while ii <= nn:
            qq = _fdiv(ai[(ii, kk)[-1]], ai[(kk, kk)[-1]])
            jj = 1
            while jj <= nn:
                if jj == kk:
                    ai[(ii, jj)[-1]] = 0.0
                else:
                    ai[(ii, jj)[-1]] = ai[(ii, jj)[-1]] - (qq * ai[(kk, jj)[-1]])
                jj += 1
            b[ii] = b[ii] - (qq * b[kk])
            ii += 1
        kk += 1
    x[nn] = _fdiv(b[nn], ai[(nn, nn)[-1]])
    ii = nn - 1
    while ii >= 1:
        tt = 0.0
        jj = 1
        while jj <= (nn - ii):
            tt = tt + (ai[(ii, ii + jj)[-1]] * x[ii + jj])
            x[ii] = _fdiv(1, ai[(ii, ii)[-1]]) * (b[ii] - tt)
            jj += 1
        ii -= 1
    n = i0
    while n <= (i0 + p):
        sum_ = 0.0
        kk = 1
        while kk <= degree:
            sum_ += x[kk + 1] * MathPow(n, kk)
            kk += 1
        mBuffer[n] = x[1] + sum_
        n += 1
    sq = 0.0
    n = i0
    while n <= (i0 + p):
        sq += MathPow(close[n] - mBuffer[n], 2)
        n += 1
    sq = MathSqrt(_fdiv(sq, p + 1)) * kstd
    n = i0
    while n <= (i0 + p):
        hBuffer[n] = mBuffer[n] + sq
        lBuffer[n] = mBuffer[n] - sq
        n += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IRegr(_MQL5Indicator):
    name = 'i-Regr'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'degree': 3,
        'kstd': 2.0,
        'bars': 250,
        'shift': 0,
    }

