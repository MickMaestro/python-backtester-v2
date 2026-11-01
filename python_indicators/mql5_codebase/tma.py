"""tma — converted from MQL5: MQL5 Indicators/TMA/tma.mq5

Copyright: Copyright © 2006, Matias Romeo; Link: mailto:matias.romeo@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Matias Romeo', 'link': 'mailto:matias.romeo@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TMA'}, 'levels': [], 'description': [], 'name': 'tma', 'source': 'MQL5 Indicators/TMA/tma.mq5', 'folder': 'TMA', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 30, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'vertical shift of the indicator in pointsх', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 30)  # smoothing depth
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # vertical shift of the indicator in pointsх
TMA = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0
divisor = 0
weights = Arr(0, 0)

def OnInit():
    global dPriceShift, divisor, min_rates_total
    min_rates_total = _int(MathCeil(Length / 2.0))
    ArrayResize(weights, min_rates_total)
    for iii in range(0, min_rates_total):
        i1 = iii + 1
        weights[iii] = i1
        weights[min_rates_total - i1] = i1
    divisor = 0
    for kkk in range(0, min_rates_total):
        divisor += weights[kkk]
    SetIndexBuffer(0, TMA, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'TMA')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'TMA(', Length, ',', Shift, ',', PriceShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    dPriceShift = Point() * PriceShift

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    tma_val = 0.0
    tma = 0.0
    if prev_calculated == 0:
        first = min_rates_total + begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        tma_val = 0.0
        for nnn in range(0, min_rates_total):
            tma_val += price[bar - min_rates_total + nnn] * weights[nnn]
        tma = _fdiv(tma_val, divisor)
        TMA[bar] = tma + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Tma(_MQL5Indicator):
    name = 'tma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 30,  # smoothing depth
        'Shift': 0,  # horizontal shift of the indicator in bars
        'PriceShift': 0,  # vertical shift of the indicator in pointsх
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

