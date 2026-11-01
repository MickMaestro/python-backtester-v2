"""fir_filter — converted from MQL5: MQL5 Indicators/FIR_filter/fir_filter.mq5

Copyright: gpwr; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'gpwr', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'FIR filter'}, 'levels': [], 'description': [], 'name': 'fir_filter', 'source': 'MQL5 Indicators/FIR_filter/fir_filter.mq5', 'folder': 'FIR_filter', 'inputs': [{'mql': 'Per', 'py': 'Per', 'param': 'Per', 'type': 'int', 'default': 50, 'label': '# of filter taps (period)', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Per = _input('Per', 50)  # # of filter taps (period)
w = Arr(0, 0.0)
wsum = 0.0
x = Arr(0, 0.0)

def OnInit():
    global wsum
    ArrayResize(w, Per)
    ArrayInitialize(w, 0)
    for k in range(0, Per):
        w[k] = 0.5 - (0.5 * MathCos((2.0 * 3.141592653589793 * (k + 1)) / (Per + 1)))
        wsum += w[k]
    SetIndexBuffer(0, x, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 5)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FIR_filter(' + _str(Per) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Per)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < Per:
        return 0
    i = prev_calculated - 1
    if i < (Per - 1):
        i = Per - 1
    while i < rates_total:
        x[i] = 0.0
        for k in range(0, Per):
            x[i] += price[i - k] * w[k]
        x[i] = _fdiv(x[i], wsum)
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FirFilter(_MQL5Indicator):
    name = 'fir_filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Per': 50,  # # of filter taps (period)
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

