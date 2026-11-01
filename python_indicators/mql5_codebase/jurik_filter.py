"""jurik_filter — converted from MQL5: MQL5 Indicators/Jurik Filter/jurik_filter.mq5

Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16760576, 255, 55295]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Jurik filter'}, 'levels': [], 'description': [], 'name': 'jurik_filter', 'source': 'MQL5 Indicators/Jurik Filter/jurik_filter.mq5', 'folder': 'Jurik Filter', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'Phase', 'py': 'Phase', 'param': 'Phase', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 50)
Phase = _input('Phase', 0.0)
jurikFilter = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
wrk = Arr(0, 0.0, dims=(10,))

def OnInit():
    SetIndexBuffer(0, jurikFilter, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Jurik filter(' + _str(Length) + ',' + DoubleToString(Phase, 2) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        jurikFilter[i] = iSmooth(price[i], Length, Phase, i, rates_total)
        if i > 0:
            colorBuffer[i] = 2.0
            if jurikFilter[i] > jurikFilter[i - 1]:
                colorBuffer[i] = 0.0
            if jurikFilter[i] < jurikFilter[i - 1]:
                colorBuffer[i] = 1.0
    return rates_total

def iSmooth(price, length, phase, r, bars):
    if ArrayRange(wrk, 0) != bars:
        ArrayResize(wrk, bars)
    if price == EMPTY_VALUE:
        price = 0.0
    k = 0
    if r == 0:
        while k < 7:
            wrk[0][k] = price
            k += 1
        while k < 10:
            wrk[0][k] = 0.0
            k += 1
        return price
    len1 = MathMax(_fdiv(MathLog(MathSqrt(0.5 * (length - 1))), MathLog(2.0)) + 2.0, 0)
    pow1 = MathMax(len1 - 2.0, 0.5)
    del1 = price - wrk[r - 1][5]
    del2 = price - wrk[r - 1][6]
    div = _fdiv(1.0, 10.0 + ((10.0 * MathMin(MathMax(length - 10, 0), 100)) / 100))
    forBar = MathMin(r, 10)
    wrk[r][7] = 0.0
    if MathAbs(del1) > MathAbs(del2):
        wrk[r][7] = MathAbs(del1)
    if MathAbs(del1) < MathAbs(del2):
        wrk[r][7] = MathAbs(del2)
    wrk[r][8] = wrk[r - 1][8] + ((wrk[r][7] - wrk[r - forBar][7]) * div)
    dVolty = 0.0
    wrk[r][9] = wrk[r - 1][9] + (_fdiv(2.0, MathMax(4.0 * length, 30) + 1.0) * (wrk[r][8] - wrk[r - 1][9]))
    if wrk[r][9] > 0:
        dVolty = _fdiv(wrk[r][7], wrk[r][9])
    else:
        dVolty = 0.0
    if dVolty > MathPow(len1, _fdiv(1.0, pow1)):
        dVolty = MathPow(len1, _fdiv(1.0, pow1))
    if dVolty < 1:
        dVolty = 1.0
    pow2 = MathPow(dVolty, pow1)
    len2 = MathSqrt(0.5 * (length - 1)) * len1
    Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
    if del1 > 0:
        wrk[r][5] = price
    else:
        wrk[r][5] = price - (Kv * del1)
    if del2 < 0:
        wrk[r][6] = price
    else:
        wrk[r][6] = price - (Kv * del2)
    R = (MathMax(MathMin(phase, 100), -100) / 100.0) + 1.5
    beta = _fdiv(0.45 * (length - 1), (0.45 * (length - 1)) + 2)
    alpha = MathPow(beta, pow2)
    wrk[r][0] = price + (alpha * (wrk[r - 1][0] - price))
    wrk[r][1] = ((price - wrk[r][0]) * (1 - beta)) + (beta * wrk[r - 1][1])
    wrk[r][2] = wrk[r][0] + (R * wrk[r][1])
    wrk[r][3] = ((wrk[r][2] - wrk[r - 1][4]) * MathPow(1 - alpha, 2)) + (MathPow(alpha, 2) * wrk[r - 1][3])
    wrk[r][4] = wrk[r - 1][4] + wrk[r][3]
    return wrk[r][4]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JurikFilter(_MQL5Indicator):
    name = 'jurik_filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Length': 50,
        'Phase': 0.0,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

