"""ar_extrapolator_of_price — converted from MQL5: MQL5 Indicators/AR extrapolation of price/ar_extrapolator_of_price.mq5

Extrapolation of open prices by autoregressive (AR) model
Copyright: gpwr; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'gpwr', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Modeled future', 2: 'Modeled past'}, 'levels': [], 'description': ['Extrapolation of open prices by autoregressive (AR) model'], 'name': 'ar_extrapolator_of_price', 'source': 'MQL5 Indicators/AR extrapolation of price/ar_extrapolator_of_price.mq5', 'folder': 'AR extrapolation of price', 'inputs': [{'mql': 'UseDiff', 'py': 'UseDiff', 'param': 'UseDiff', 'type': 'bool', 'default': False, 'label': 'Use price difference', 'sinput': False}, {'mql': 'Ncoef', 'py': 'Ncoef', 'param': 'Ncoef', 'type': 'int', 'default': 150, 'label': 'Model coefficients (model order)', 'sinput': False}, {'mql': 'Nfut', 'py': 'Nfut', 'param': 'Nfut', 'type': 'int', 'default': 100, 'label': 'Future bars', 'sinput': False}, {'mql': 'kPast', 'py': 'kPast', 'param': 'kPast', 'type': 'double', 'default': 3.0, 'label': 'Past bars in increments of Ncoef (must be >=1)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UseDiff = _input('UseDiff', False)  # Use price difference
Ncoef = _input('Ncoef', 150)  # Model coefficients (model order)
Nfut = _input('Nfut', 100)  # Future bars
kPast = _input('kPast', 3.0)  # Past bars in increments of Ncoef (must be >=1)
Npast = 0
dN = 0
ym = Arr(0, 0.0)
xm = Arr(0, 0.0)

def OnInit():
    global Npast, dN
    Npast = _int(kPast * Ncoef)
    if UseDiff:
        dN = 1
    else:
        dN = 0
    ArraySetAsSeries(xm, True)
    ArraySetAsSeries(ym, True)
    SetIndexBuffer(0, ym, INDICATOR_DATA)
    SetIndexBuffer(1, xm, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'AR(' + _str(Npast) + ',' + _str(Ncoef) + ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, Nfut)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    if rates_total < (Npast + 1):
        Print('Error: not enough bars in history!')
        return 0
    ArrayInitialize(xm, EMPTY_VALUE)
    ArrayInitialize(ym, EMPTY_VALUE)
    rates = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(rates, True)
    if CopyRates(None, 0, 0, Npast + 1, rates) <= 0:
        return 0
    x = Arr(0, 0.0)
    ArrayResize(x, Npast)
    for i in range(0, Npast):
        x[Npast - 1 - i] = rates[i].open - (rates[i + 1].open * dN)
    a = Arr(0, 0.0)
    ArrayResize(a, Ncoef + 1)
    Burg(x, Npast, Ncoef, a)
    for n in range(Ncoef, Npast + Nfut):
        sum_ = 0.0
        for i in range(1, Ncoef + 1):
            if (n - i) < Npast:
                sum_ -= a[i] * x[n - i]
            else:
                sum_ -= a[i] * ym[Nfut + Npast - (n - i)]
        if n < Npast:
            xm[Npast - 1 - n] = sum_
        else:
            ym[Nfut + Npast - n] = sum_
    if UseDiff:
        tmp = xm[0]
        xm[0] = rates[0].open
        for i in range(1, Npast - Ncoef):
            tmp2 = xm[i]
            xm[i] = xm[i - 1] - tmp
            tmp = tmp2
    ym[Nfut] = xm[0]
    if UseDiff:
        for i in range(1, Nfut + 1):
            ym[Nfut - i] += ym[Nfut - i + 1]
    return rates_total

def Burg(x, n, p, a):
    df = Arr(0, 0.0)
    db = Arr(0, 0.0)
    ArrayResize(df, n)
    ArrayResize(db, n)
    tmp = 0.0
    num = 0.0
    den = 0.0
    r = 0.0
    for i in range(0, n):
        df[i] = x[i]
        db[i] = x[i]
    for k in range(1, p + 1):
        num = 0.0
        den = 0.0
        if k == 1:
            for i in range(2, n):
                num += x[i - 1] * (x[i] + x[i - 2])
                den += x[i - 1] * x[i - 1]
            r = _fdiv(-num, den) / 2.0
            if r > 1.0:
                r = 1.0
            if r < -1.0:
                r = -1.0
        else:
            for i in range(k, n):
                num += df[i] * db[i - 1]
                den += (df[i] * df[i]) + (db[i - 1] * db[i - 1])
            r = _fdiv(-2.0 * num, den)
        a[k] = r
        kh = _idiv(k, 2)
        for i in range(1, kh + 1):
            ki = k - i
            tmp = a[i]
            a[i] += r * a[ki]
            if i != ki:
                a[ki] += r * tmp
        if k < p:
            for i in range(n - 1, k - 1, -1):
                tmp = df[i]
                df[i] += r * db[i - 1]
                db[i] = db[i - 1] + (r * tmp)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ArExtrapolatorOfPrice(_MQL5Indicator):
    name = 'ar_extrapolator_of_price'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'UseDiff': False,  # Use price difference
        'Ncoef': 150,  # Model coefficients (model order)
        'Nfut': 100,  # Future bars
        'kPast': 3.0,  # Past bars in increments of Ncoef (must be >=1)
    }

