"""plombiers — converted from MQL5: MQL5 Indicators/Plombiers - oscillator in the channel/plombiers.mq5

Constructing a stochastic oscillator in the
channel  where  the channel  walls formed a 
standard deviation of an arbitrary polynomial,
which is approximated  least  squares.
_____________________________________
Copyright: 2009-2010, Avatara@bigmir.net; Link: Avatara@bigmir.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009-2010, Avatara@bigmir.net', 'link': 'Avatara@bigmir.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [14772545], 2: [3329330], 3: [3329330], 4: [15128749], 5: [15128749], 6: [15660543]}, 'widths': {1: 1, 2: 2, 3: 2, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 2}, 'labels': {1: 'Means', 2: 'Resistance', 3: 'Support', 4: 'Resistance+', 5: 'Support-', 6: 'Signal'}, 'levels': [], 'description': ['Constructing a stochastic oscillator in the', 'channel  where  the channel  walls formed a ', 'standard deviation of an arbitrary polynomial,', 'which is approximated  least  squares.', '_____________________________________'], 'name': 'plombiers', 'source': 'MQL5 Indicators/Plombiers - oscillator in the channel/plombiers.mq5', 'folder': 'Plombiers - oscillator in the channel', 'inputs': [{'mql': 'bars_IN', 'py': 'bars_IN', 'param': 'bars_IN', 'type': 'int', 'default': 145, 'label': 'data length', 'sinput': False}, {'mql': 'SP', 'py': 'SP', 'param': 'SP', 'type': 'int', 'default': 2, 'label': "curve's order", 'sinput': False}, {'mql': 'N_Shift1', 'py': 'N_Shift1', 'param': 'N_Shift1', 'type': 'int', 'default': 0, 'label': 'shift back into the history', 'sinput': False}, {'mql': 'Forecast', 'py': 'Forecast', 'param': 'Forecast', 'type': 'int', 'default': 0, 'label': 'length of channel into the "future"', 'sinput': False}, {'mql': 'kstd', 'py': 'kstd', 'param': 'kstd', 'type': 'double', 'default': 2.1415, 'label': 'standart deviation factor', 'sinput': False}, {'mql': 'Oscilator', 'py': 'Oscilator', 'param': 'Oscilator', 'type': 'bool', 'default': True, 'label': 'Is oscillator on the display?', 'sinput': False}, {'mql': 'N_Buff', 'py': 'N_Buff', 'param': 'N_Buff', 'type': 'int', 'default': 1, 'label': "displayed oscillator's buffer", 'sinput': False}, {'mql': 'Ka', 'py': 'Ka', 'param': 'Ka', 'type': 'int', 'default': 21, 'label': 'Line calculation period %K.', 'sinput': False}, {'mql': 'La', 'py': 'La', 'param': 'La', 'type': 'int', 'default': 7, 'label': 'Averaging period %D', 'sinput': False}, {'mql': 'Za', 'py': 'Za', 'param': 'Za', 'type': 'int', 'default': 1, 'label': 'Deceleration', 'sinput': False}, {'mql': 'Oe', 'py': 'Oe', 'param': 'Oe', 'type': 'int', 'default': 0, 'label': 'Averaging method', 'sinput': False}, {'mql': 'Me', 'py': 'Me', 'param': 'Me', 'type': 'int', 'default': 1, 'label': "Stochastic's price value", 'sinput': False}, {'mql': 'DIGf', 'py': 'DIGf', 'param': 'DIGf', 'type': 'int', 'default': -99, 'label': 'Number of decimal points.-99 Digits', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum intType
i0 = 0
i1 = 1
i2 = 2
i3 = 3
i4 = 4
_enum('intType', {0: 'i0', 1: 'i1', 2: 'i2', 3: 'i3', 4: 'i4'})

# ---- inputs and global variables
bars_IN = _input('bars_IN', 145)  # data length
SP = _input('SP', i2)  # curve's order
N_Shift1 = _input('N_Shift1', 0)  # shift back into the history
Forecast = _input('Forecast', 0)  # length of channel into the "future"
kstd = _input('kstd', 2.1415)  # standart deviation factor
Oscilator = _input('Oscilator', True)  # Is oscillator on the display?
N_Buff = _input('N_Buff', 1)  # displayed oscillator's buffer
Ka = _input('Ka', 21)  # Line calculation period %K.
La = _input('La', 7)  # Averaging period %D
Za = _input('Za', 1)  # Deceleration
Oe = _input('Oe', MODE_SMA)  # Averaging method
Me = _input('Me', STO_CLOSECLOSE)  # Stochastic's price value
DIGf = _input('DIGf', -99)  # Number of decimal points.-99 Digits
sName = 'Plombiers 1.0'
ai = Arr(12, 0.0, dyn=False, dims=(12,))
b = Arr(12, 0.0, dyn=False)
x = Arr(12, 0.0, dyn=False)
sx = Arr(12, 0.0, dyn=False)
sum_ = 0.0
Mnog = 0.0
COG = Arr(0, 0.0)
N = 0
i = 0
N1 = 0
j = 0
k = 0
LM = 0
hOsc = 0
Dig = 0
hFl = 0
N_Shift = 0
qq = 0.0
mm = 0.0
tt = 0.0
sq = 0.0
std = 0.0
Means = Arr(0, 0.0)
level1h = Arr(0, 0.0)
level1l = Arr(0, 0.0)
level2h = Arr(0, 0.0)
level2l = Arr(0, 0.0)
S = Arr(0, 0.0)

def OnInit():
    global Dig, N, N1, N_Shift, hOsc, sName
    SetIndexBuffer(0, Means, INDICATOR_DATA)
    SetIndexBuffer(1, level1h, INDICATOR_DATA)
    SetIndexBuffer(2, level1l, INDICATOR_DATA)
    SetIndexBuffer(3, level2h, INDICATOR_DATA)
    SetIndexBuffer(4, level2l, INDICATOR_DATA)
    SetIndexBuffer(5, S, INDICATOR_DATA)
    ArraySetAsSeries(Means, True)
    ArraySetAsSeries(S, True)
    ArraySetAsSeries(level1h, True)
    ArraySetAsSeries(level2h, True)
    ArraySetAsSeries(level1l, True)
    ArraySetAsSeries(level2l, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    N_Shift = N_Shift1
    if N_Shift < 0:
        N_Shift = -N_Shift
    N = bars_IN + N_Shift
    N1 = Bars(Symbol(), PERIOD_CURRENT)
    if N1 < N:
        N = N1
    else:
        N1 = N
    sName = sName + ' (' + IntegerToString(bars_IN, 4) + ',' + IntegerToString(N_Shift, 3) + ',' + IntegerToString(Forecast, 3) + ')'
    if DIGf < 0:
        Dig = Digits()
    else:
        Dig = DIGf
    PlotIndexSetInteger(0, PLOT_SHIFT, Forecast)
    PlotIndexSetInteger(1, PLOT_SHIFT, Forecast)
    PlotIndexSetInteger(2, PLOT_SHIFT, Forecast)
    PlotIndexSetInteger(3, PLOT_SHIFT, Forecast)
    PlotIndexSetInteger(4, PLOT_SHIFT, Forecast)
    PlotIndexSetInteger(5, PLOT_SHIFT, Forecast)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, N1 + Forecast)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, N1 + Forecast)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, N1 + Forecast)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, N1 + Forecast)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, N1 + Forecast)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, N1 + Forecast)
    IndicatorSetString(INDICATOR_SHORTNAME, sName)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0.0)
    hOsc = iStochastic(Symbol(), Period(), Ka, La, Za, Oe, Me)
    return 0

def deinit():
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    global LM, N, N1, i, j, k, mm, qq, sq, std, sum_, tt
    mi = 0
    N1 = rates_total
    N = bars_IN + N_Shift
    if N1 < N:
        N1 = bars_IN + N1 - N
        N = N1
        N1 = N + 1
        Print('Not presentative DATA! bars present ', N)
    else:
        N1 = bars_IN + 1
    if not ArrayGetAsSeries(price):
        ArraySetAsSeries(price, True)
    copied = CopyBuffer(hOsc, N_Buff, N_Shift, N1 - 1, S)
    if copied <= 0:
        Print("Unable to copy indicator's value. Error =", GetLastError(), ',  copied =', copied)
        return 0
    sx[1] = N1 - 1.0
    mi = 1
    for mi in range(mi, ((SP + 1) * 2) - 2 + 1):
        sum_ = 0.0
        i = N_Shift
        while i < N:
            sum_ += MathPow(i, mi)
            i += 1
        sx[mi + 1] = sum_
    else:
        mi = _range_end(mi, ((SP + 1) * 2) - 2 + 1, 1)
    mi = 1
    for mi in range(mi, SP + 1 + 1):
        sum_ = 0.0
        i = N_Shift
        while i < N:
            if mi == 1:
                sum_ += price[i]
            else:
                sum_ += price[i] * MathPow(i, mi - 1)
            i += 1
        b[mi] = sum_
    else:
        mi = _range_end(mi, SP + 1 + 1, 1)
    j = 1
    while j <= (SP + 1):
        i = 1
        while i <= (SP + 1):
            k = i + j - 1
            ai[i][j] = sx[k]
            i += 1
        j += 1
    k = 1
    while k <= SP:
        LM = 0
        mm = 0.0
        i = k
        while i <= (SP + 1):
            if MathAbs(ai[i][k]) > mm:
                mm = MathAbs(ai[i][k])
                LM = i
            i += 1
        if LM == 0:
            return 0
        if LM != k:
            j = 1
            while j <= (SP + 1):
                tt = ai[k][j]
                ai[k][j] = ai[LM][j]
                ai[LM][j] = tt
                j += 1
            tt = b[k]
            b[k] = b[LM]
            b[LM] = tt
        i = k + 1
        while i <= (SP + 1):
            if MathAbs(ai[k][k]) > 1e-05:
                qq = _fdiv(ai[i][k], ai[k][k])
            else:
                qq = 1.0
            j = 1
            while j <= (SP + 1):
                if j == k:
                    ai[i][j] = 0.0
                else:
                    ai[i][j] = ai[i][j] - (qq * ai[k][j])
                j += 1
            b[i] = b[i] - (qq * b[k])
            i += 1
        k += 1
    k = SP + 1
    if ai[k][k] == 0.0:
        Print('singular')
        return rates_total
    x[k] = _fdiv(b[k], ai[k][k])
    i = SP
    while i >= 1:
        tt = 0.0
        j = 1
        while j <= (k - i):
            tt = tt + (ai[i][i + j] * x[i + j])
            x[i] = _fdiv(1.0, ai[i][i]) * (b[i] - tt)
            j += 1
        i -= 1
    i = N_Shift - Forecast
    while i < N:
        sum_ = 0.0
        k = 1
        while k <= SP:
            sum_ += x[k + 1] * MathPow(i, k)
            k += 1
        Means[i + Forecast] = NormalizeDouble(x[1] + sum_, Dig)
        i += 1
    sq = 0.0
    i = N_Shift
    while i < N:
        qq = price[i - N_Shift] - Means[i + Forecast]
        sq += qq * qq
        i += 1
    tt = float(N1 - 1)
    sq = MathSqrt(_fdiv(sq, tt)) * kstd
    std = myStdDev(N1 - 1, price, N_Shift) * kstd
    i = N_Shift - Forecast
    while i < N:
        level1h[i + Forecast] = Means[i + Forecast] + sq
        level1l[i + Forecast] = Means[i + Forecast] - sq
        level2h[i + Forecast] = Means[i + Forecast] + std
        level2l[i + Forecast] = Means[i + Forecast] - std
        i += 1
    if Oscilator:
        i = N - 1
        while i >= N_Shift:
            S[i + Forecast] = Means[i + Forecast] + ((sq * (S[i] - 50.0)) / 44.9999)
            i -= 1
        i = 0
        while i < (N_Shift + Forecast):
            S[i] = 0.0
            i += 1
    return rates_total

def myStdDev(period_N, Cena, Shift):
    sum__ = 0.0
    sred = 0.0
    std_ = 0.0
    j_ = 0
    k_ = period_N - 1
    sum__ = 0.0
    std_ = 0.0
    j_ = 0
    for j_ in range(j_, period_N):
        sum__ += Cena[j_ + Shift]
    else:
        j_ = _range_end(j_, period_N, 1)
    sred = _fdiv(sum__, period_N)
    j_ = 0
    for j_ in range(j_, period_N):
        sum__ = Cena[j_ + Shift] - sred
        std_ += sum__ * sum__
    else:
        j_ = _range_end(j_, period_N, 1)
    sum__ = _fdiv(std_, k_)
    std_ = MathSqrt(sum__)
    return std_


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Plombiers(_MQL5Indicator):
    name = 'plombiers'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'bars_IN': 145,  # data length
        'SP': _Choice({0: '0 - simple average', 1: '1 - straight line', 2: 'parabola 2-nd degrees', 3: 'parabola 3-d degrees', 4: '4-th degrees'}, default=2),  # curve's order
        'N_Shift1': 0,  # shift back into the history
        'Forecast': 0,  # length of channel into the "future"
        'kstd': 2.1415,  # standart deviation factor
        'Oscilator': True,  # Is oscillator on the display?
        'N_Buff': 1,  # displayed oscillator's buffer
        'Ka': 21,  # Line calculation period %K.
        'La': 7,  # Averaging period %D
        'Za': 1,  # Deceleration
        'Oe': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Averaging method
        'Me': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=1),  # Stochastic's price value
        'DIGf': -99,  # Number of decimal points.-99 Digits
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

