"""fourier_extrapolator_of_price — converted from MQL5: MQL5 Indicators/Fourier extrapolation of price/fourier_extrapolator_of_price.mq5

Extrapolation of open prices by trigonometric (multitone) model
Copyright: gpwr; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'gpwr', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Modeled future', 2: 'Modeled past'}, 'levels': [], 'description': ['Extrapolation of open prices by trigonometric (multitone) model'], 'name': 'fourier_extrapolator_of_price', 'source': 'MQL5 Indicators/Fourier extrapolation of price/fourier_extrapolator_of_price.mq5', 'folder': 'Fourier extrapolation of price', 'inputs': [{'mql': 'Npast', 'py': 'Npast', 'param': 'Npast', 'type': 'int', 'default': 300, 'label': 'Past bars, to which trigonometric series is fitted', 'sinput': False}, {'mql': 'Nfut', 'py': 'Nfut', 'param': 'Nfut', 'type': 'int', 'default': 50, 'label': 'Predicted future bars', 'sinput': False}, {'mql': 'Nharm', 'py': 'Nharm', 'param': 'Nharm', 'type': 'int', 'default': 20, 'label': 'Narmonics in model', 'sinput': False}, {'mql': 'FreqTOL', 'py': 'FreqTOL', 'param': 'FreqTOL', 'type': 'double', 'default': 1e-05, 'label': 'Tolerance of frequency calculations', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Npast = _input('Npast', 300)  # Past bars, to which trigonometric series is fitted
Nfut = _input('Nfut', 50)  # Predicted future bars
Nharm = _input('Nharm', 20)  # Narmonics in model
FreqTOL = _input('FreqTOL', 1e-05)  # Tolerance of frequency calculations
N = 0
ym = Arr(0, 0.0)
xm = Arr(0, 0.0)

def OnInit():
    global N
    N = MathMax(Npast, Nfut + 1)
    ArraySetAsSeries(xm, True)
    ArraySetAsSeries(ym, True)
    SetIndexBuffer(0, ym, INDICATOR_DATA)
    SetIndexBuffer(1, xm, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fourier(' + _str(Npast) + ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, Nfut)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    if rates_total < Npast:
        Print('Error: not enough bars in history!')
        return 0
    ArrayInitialize(xm, EMPTY_VALUE)
    ArrayInitialize(ym, EMPTY_VALUE)
    rates = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(rates, True)
    if CopyRates(None, 0, 0, Npast, rates) <= 0:
        return 0
    x = Arr(0, 0.0)
    ArrayResize(x, Npast)
    av = 0.0
    for i in range(0, Npast):
        x[i] = rates[i].open
        av += x[i]
    av = av / Npast
    for i in range(0, N):
        xm[i] = av
        if i <= Nfut:
            ym[i] = av
    for harm in range(1, Nharm + 1):
        w = Box(0.0)
        m = Box(0.0)
        a = Box(0.0)
        b = Box(0.0)
        Freq(x, Npast, w, m, a, b)
        for i in range(0, N):
            xm[i] += m.v + (a.v * MathCos(w.v * i)) + (b.v * MathSin(w.v * i))
            if i <= Nfut:
                ym[Nfut - i] += m.v + (a.v * MathCos(w.v * i)) - (b.v * MathSin(w.v * i))
    return rates_total

def Freq(x, n, w, m, a, b):
    z = Arr(0, 0.0)
    ArrayResize(z, n)
    alpha = 0.0
    beta = 2.0
    z[0] = x[0] - xm[0]
    while MathAbs(alpha - beta) > FreqTOL:
        alpha = beta
        z[1] = x[1] - xm[1] + (alpha * z[0])
        num = z[0] * z[1]
        den = z[0] * z[0]
        for i in range(2, n):
            z[i] = x[i] - xm[i] + (alpha * z[i - 1]) - z[i - 2]
            num += z[i - 1] * (z[i] + z[i - 2])
            den += z[i - 1] * z[i - 1]
        beta = _fdiv(num, den)
    w.v = MathArccos(beta / 2.0)
    TrigFit(x, n, w.v, m, a, b)

def TrigFit(x, n, w, m, a, b):
    Sc = 0.0
    Ss = 0.0
    Scc = 0.0
    Sss = 0.0
    Scs = 0.0
    Sx = 0.0
    Sxc = 0.0
    Sxs = 0.0
    for i in range(0, n):
        c = MathCos(w * i)
        s = MathSin(w * i)
        dx = x[i] - xm[i]
        Sc += c
        Ss += s
        Scc += c * c
        Sss += s * s
        Scs += c * s
        Sx += dx
        Sxc += dx * c
        Sxs += dx * s
    Sc = _fdiv(Sc, n)
    Ss = _fdiv(Ss, n)
    Scc = _fdiv(Scc, n)
    Sss = _fdiv(Sss, n)
    Scs = _fdiv(Scs, n)
    Sx = _fdiv(Sx, n)
    Sxc = _fdiv(Sxc, n)
    Sxs = _fdiv(Sxs, n)
    if w == 0.0:
        m.v = Sx
        a.v = 0.0
        b.v = 0.0
    else:
        den = MathPow(Scs - (Sc * Ss), 2) - ((Scc - (Sc * Sc)) * (Sss - (Ss * Ss)))
        a.v = _fdiv(((Sxs - (Sx * Ss)) * (Scs - (Sc * Ss))) - ((Sxc - (Sx * Sc)) * (Sss - (Ss * Ss))), den)
        b.v = _fdiv(((Sxc - (Sx * Sc)) * (Scs - (Sc * Ss))) - ((Sxs - (Sx * Ss)) * (Scc - (Sc * Sc))), den)
        m.v = Sx - (a.v * Sc) - (b.v * Ss)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FourierExtrapolatorOfPrice(_MQL5Indicator):
    name = 'fourier_extrapolator_of_price'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Npast': 300,  # Past bars, to which trigonometric series is fitted
        'Nfut': 50,  # Predicted future bars
        'Nharm': 20,  # Narmonics in model
        'FreqTOL': 1e-05,  # Tolerance of frequency calculations
    }

