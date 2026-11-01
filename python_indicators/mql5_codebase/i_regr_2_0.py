"""i-Regr-2.0 — converted from MQL5: MQL5 Indicators/Regression Channel with variable polynomial degree/i-Regr-2.0.mq5

Copyright: © 2008 BJF Trading Group; Link: www.iticsoftware.com; Version: 2.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© 2008 BJF Trading Group', 'link': 'www.iticsoftware.com', 'version': '2.0', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 8, 2: 8, 3: 8}, 'colors': {1: [55295, 755384], 2: [3329330, 16711680], 3: [55295, 755384]}, 'widths': {1: 3, 2: 3, 3: 3}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'up', 2: 'middle', 3: 'down'}, 'levels': [], 'description': [], 'name': 'i-Regr-2.0', 'source': 'MQL5 Indicators/Regression Channel with variable polynomial degree/i-Regr-2.0.mq5', 'folder': 'Regression Channel with variable polynomial degree', 'inputs': [{'mql': 'degree', 'py': 'degree', 'param': 'degree', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'kstd', 'py': 'kstd', 'param': 'kstd', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'bars', 'py': 'bars', 'param': 'bars', 'type': 'int', 'default': 500, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
degree = _input('degree', 5)
kstd = _input('kstd', 2.0)
bars = _input('bars', 500)
hBuffer = Arr(0, 0.0)
hcBuffer = Arr(0, 0.0)
mBuffer = Arr(0, 0.0)
mcBuffer = Arr(0, 0.0)
lBuffer = Arr(0, 0.0)
lcBuffer = Arr(0, 0.0)
dBuffer = Arr(0, 0.0)
ai = Arr((10, 10)[-1], 0.0, dyn=False)
b = Arr(10, 0.0, dyn=False)
x = Arr(10, 0.0, dyn=False)
sx = Arr(20, 0.0, dyn=False)
f = 0
qq = 0.0
mm = 0.0
tt = 0.0
ii = 0
jj = 0
kk = 0
ll = 0
i0 = 0

def OnInit():
    SetIndexBuffer(0, hBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, hcBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, mBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, mcBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, lBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, lcBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, dBuffer, INDICATOR_CALCULATIONS)
    sx[1] = bars + 1
    for i in range(1, ((degree + 1) * 2) - 2 + 1):
        sum_ = 0.0
        for n in range(0, bars + 1):
            sum_ += MathPow(1 + ((n + 0.0) / bars), i)
        sx[i + 1] = sum_
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global i0, ii, jj, kk, ll, mm, qq, tt
    if rates_total < bars:
        return -1
    if rates_total > prev_calculated:
        pass
    else:
        return rates_total
    i0 = rates_total - bars - 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - bars - 1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, rates_total - bars - 1)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, rates_total - bars - 1)
    jj = 1
    while jj <= (degree + 1):
        ii = 1
        while ii <= (degree + 1):
            ai[(ii, jj)[-1]] = sx[ii + jj - 1]
            ii += 1
        jj += 1
    for mi in range(1, degree + 1 + 1):
        sum_ = 0.0
        for n in range(i0, i0 + bars + 1):
            if mi == 1:
                sum_ += open[n]
            else:
                sum_ += open[n] * MathPow(1 + ((n - i0 + 0.0) / bars), mi - 1)
        b[mi] = sum_
    kk = 1
    while kk <= degree:
        ll = 0
        mm = 0.0
        ii = kk
        while ii <= (degree + 1):
            if MathAbs(ai[(ii, kk)[-1]]) > mm:
                mm = MathAbs(ai[(ii, kk)[-1]])
                ll = ii
            ii += 1
        if ll == 0:
            return rates_total
        if ll != kk:
            jj = 1
            while jj <= (degree + 1):
                tt = ai[(kk, jj)[-1]]
                ai[(kk, jj)[-1]] = ai[(ll, jj)[-1]]
                ai[(ll, jj)[-1]] = tt
                jj += 1
            tt = b[kk]
            b[kk] = b[ll]
            b[ll] = tt
        ii = kk + 1
        while ii <= (degree + 1):
            qq = _fdiv(ai[(ii, kk)[-1]], ai[(kk, kk)[-1]])
            jj = 1
            while jj <= (degree + 1):
                if jj == kk:
                    ai[(ii, jj)[-1]] = 0.0
                else:
                    ai[(ii, jj)[-1]] = ai[(ii, jj)[-1]] - (qq * ai[(kk, jj)[-1]])
                jj += 1
            b[ii] = b[ii] - (qq * b[kk])
            ii += 1
        kk += 1
    x[degree + 1] = _fdiv(b[degree + 1], ai[(degree + 1, degree + 1)[-1]])
    ii = degree
    while ii >= 1:
        tt = 0.0
        jj = 1
        while jj <= (degree + 1 - ii):
            tt = tt + (ai[(ii, ii + jj)[-1]] * x[ii + jj])
            x[ii] = _fdiv(1, ai[(ii, ii)[-1]]) * (b[ii] - tt)
            jj += 1
        ii -= 1
    for n in range(i0, i0 + bars + 1):
        sum_ = 0.0
        kk = 1
        while kk <= degree:
            sum_ += x[kk + 1] * MathPow(1 + ((n - i0 + 0.0) / bars), kk)
            kk += 1
        mBuffer[n] = x[1] + sum_
    for n in range(i0 + bars, i0, -1):
        if mBuffer[n] > mBuffer[n - 1]:
            mcBuffer[n] = 0.0
        else:
            mcBuffer[n] = 1.0
    mcBuffer[i0] = mcBuffer[i0 + 1]
    for n in range(i0 + bars, i0 + 1, -1):
        if (mBuffer[n] - (2 * mBuffer[n - 1]) + mBuffer[n - 2]) > 0:
            hcBuffer[n] = 0.0
            lcBuffer[n] = 0.0
        else:
            hcBuffer[n] = 1.0
            lcBuffer[n] = 1.0
    hcBuffer[i0 + 1] = hcBuffer[i0 + 2]
    lcBuffer[i0 + 1] = lcBuffer[i0 + 2]
    hcBuffer[i0] = hcBuffer[i0 + 2]
    lcBuffer[i0] = lcBuffer[i0 + 2]
    sq = 0.0
    for n in range(i0, i0 + bars + 1):
        sq += MathPow(open[n] - mBuffer[n], 2)
    sq = MathSqrt(sq / (bars + 1)) * kstd
    for n in range(i0, i0 + bars + 1):
        hBuffer[n] = mBuffer[n] + sq
        lBuffer[n] = mBuffer[n] - sq
        dBuffer[n] = sq
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IRegr20(_MQL5Indicator):
    name = 'i-Regr-2.0'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'degree': 5,
        'kstd': 2.0,
        'bars': 500,
    }

