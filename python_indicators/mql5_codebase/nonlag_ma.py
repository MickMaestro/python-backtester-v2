"""nonlag_ma — converted from MQL5: MQL5 Indicators/NonLag MA/nonlag_ma.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16760576, 9662683, 6908265]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'NonLag ma'}, 'levels': [], 'description': [], 'name': 'nonlag_ma', 'source': 'MQL5 Indicators/NonLag MA/nonlag_ma.mq5', 'folder': 'NonLag MA', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 25, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 25)
nonlagma = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
nlm_values = Arr(3, 0.0, dyn=False, dims=(1,))
nlm_prices = Arr(0, 0.0, dims=(1,))
nlm_alphas = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, nonlagma, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'NonLag ma (' + _str(Length) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        nonlagma[i] = iNoLagMa(price[i], Length, i, 0)
        if i > 0:
            colorBuffer[i] = 2.0
            if nonlagma[i] > nonlagma[i - 1]:
                colorBuffer[i] = 0.0
            if nonlagma[i] < nonlagma[i - 1]:
                colorBuffer[i] = 1.0
    return rates_total

def iNoLagMa(price, length, r, forValue=0):
    if ArrayRange(nlm_prices, 0) != Bars(Symbol(), 0):
        ArrayResize(nlm_prices, Bars(Symbol(), 0))
    nlm_prices[r][forValue] = price
    if length < 3 or r < 3:
        return nlm_prices[r][forValue]
    if nlm_values[0][forValue] != length:
        Cycle = 4.0
        Coeff = 3.0 * 3.141592653589793
        Phase = length - 1
        nlm_values[0][forValue] = length
        nlm_values[1][forValue] = (length * 4) + Phase
        nlm_values[2][forValue] = 0.0
        if ArrayRange(nlm_alphas, 0) < nlm_values[1][forValue]:
            ArrayResize(nlm_alphas, _int(nlm_values[1][forValue]))
        k = 0
        while k < nlm_values[1][forValue]:
            t = 0.0
            if k <= (Phase - 1):
                t = _fdiv(1.0 * k, Phase - 1)
            else:
                t = 1.0 + _fdiv((k - Phase + 1) * ((2.0 * Cycle) - 1.0), (Cycle * length) - 1.0)
            beta = MathCos(3.141592653589793 * t)
            g = _fdiv(1.0, (Coeff * t) + 1)
            if t <= 0.5:
                g = 1.0
            nlm_alphas[k][forValue] = g * beta
            nlm_values[2][forValue] += nlm_alphas[k][forValue]
            k += 1
    if nlm_values[2][forValue] > 0:
        sum_ = 0.0
        k = 0
        while k < nlm_values[1][forValue] and (r - k) >= 0:
            sum_ += nlm_alphas[k][forValue] * nlm_prices[r - k][forValue]
            k += 1
        return _fdiv(sum_, nlm_values[2][forValue])
    else:
        return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NonlagMa(_MQL5Indicator):
    name = 'nonlag_ma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 25,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

