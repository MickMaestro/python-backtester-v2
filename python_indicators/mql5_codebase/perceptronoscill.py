"""perceptronoscill — converted from MQL5: MQL5 Indicators/PerceptronOscill/perceptronoscill.mq5

Copyright: Copyright © 2009, Zar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Zar', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'PerceptronOscill'}, 'levels': [], 'description': [], 'name': 'perceptronoscill', 'source': 'MQL5 Indicators/PerceptronOscill/perceptronoscill.mq5', 'folder': 'PerceptronOscill', 'inputs': [{'mql': 'Numb', 'py': 'Numb', 'param': 'Numb', 'type': 'uint', 'default': 10, 'label': 'Numb', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Numb = _input('Numb', 10)  # Numb
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
Kf = Arr(0, 0.0)
min_rates_total = 0
N = 0

def OnInit():
    global N, min_rates_total
    N = _int(Numb)
    if N < 2:
        N = 2
    if N > 90:
        N = 90
    min_rates_total = N
    ArrayResize(Kf, N)
    D = 300
    kk = _int(NormalizeDouble(_idiv(D, N + 1), 0))
    for ccc in range(N, 0, -1):
        Kf[ccc - 1] = (kk * ccc) - _idiv(D, 2)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'PerceptronOscill(', N, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total + begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        IndBuffer[bar] = perceptronNN(N, price, bar)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def perceptronNN(Nn, Price, index):
    rez = 0.0
    for ccc in range(Nn, 0, -1):
        rez += Kf[ccc - 1] * (Price[index] - Price[index - ccc])
    return rez


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Perceptronoscill(_MQL5Indicator):
    name = 'perceptronoscill'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Numb': 10,  # Numb
        'Shift': 0,  # horizontal shift of the indicator in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

