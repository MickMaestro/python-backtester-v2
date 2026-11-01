"""gaussian_filter — converted from MQL5: MQL5 Indicators/Gaussian Filter/gaussian_filter.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 9662683]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Gaussian filter'}, 'levels': [], 'description': [], 'name': 'gaussian_filter', 'source': 'MQL5 Indicators/Gaussian Filter/gaussian_filter.mq5', 'folder': 'Gaussian Filter', 'inputs': [{'mql': 'GPeriod', 'py': 'GPeriod', 'param': 'GPeriod', 'type': 'int', 'default': 14, 'label': 'Calculation period', 'sinput': False}, {'mql': 'GOrder', 'py': 'GOrder', 'param': 'GOrder', 'type': 'int', 'default': 2, 'label': 'Order', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
GPeriod = _input('GPeriod', 14)  # Calculation period
GOrder = _input('GOrder', 2)  # Order
gf = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
periods = Arr(1, 0, dyn=False)
coeffs = Arr(0, 0.0, dims=(3,))
filters = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, gf, INDICATOR_DATA)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        gf[i] = iGFilter(price[i], GPeriod, GOrder, rates_total, i)
        if i > 0:
            colorBuffer[i] = colorBuffer[i - 1]
            if gf[i] > gf[i - 1]:
                colorBuffer[i] = 0.0
            if gf[i] < gf[i - 1]:
                colorBuffer[i] = 1.0
    return rates_total

def iGFilter(price, period, order, bars, i, instanceNo=0):
    if ArrayRange(filters, 0) != bars:
        ArrayResize(filters, bars)
    if ArrayRange(coeffs, 0) < (order + 1):
        ArrayResize(coeffs, order + 1)
    if periods[instanceNo] != period:
        periods[instanceNo] = period
        b = _fdiv(1.0 - MathCos(_fdiv(2.0 * 3.141592653589793, period)), MathPow(MathSqrt(2.0), _fdiv(2.0, order)) - 1.0)
        a = (-b) + MathSqrt((b * b) + (2.0 * b))
        for r in range(0, order + 1):
            coeffs[r][(instanceNo * 3) + 0] = _fdiv(fact(order), fact(order - r) * fact(r))
            coeffs[r][(instanceNo * 3) + 1] = MathPow(a, r)
            coeffs[r][(instanceNo * 3) + 2] = MathPow(1.0 - a, r)
    if price == EMPTY_VALUE:
        price = 0.0
    filters[i][instanceNo] = price * coeffs[order][(instanceNo * 3) + 1]
    sign = 1.0
    r = 1
    while r <= order and (i - r) >= 0:
        filters[i][instanceNo] += sign * coeffs[r][(instanceNo * 3) + 0] * coeffs[r][(instanceNo * 3) + 2] * filters[i - r][instanceNo]
        r += 1
        sign *= -1.0
    return filters[i][instanceNo]

def fact(n):
    a = 1.0
    for i in range(1, n + 1):
        a *= i
    return a


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GaussianFilter(_MQL5Indicator):
    name = 'gaussian_filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'GPeriod': 14,  # Calculation period
        'GOrder': 2,  # Order
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

