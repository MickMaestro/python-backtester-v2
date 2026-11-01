"""b_kaufman_efficiency_ratio — converted from MQL5: MQL5 Indicators/Kaufman Efficiency Ratio/b_kaufman_efficiency_ratio.mq5

Kaufman Efficiency Ratio (also called \\"generalized fractal
efficiency\\") according to Perry Kaufman books \\"Smarter Trading\\"
and \\"Trading Systems & Methods\\".
Copyright: Copyright © 2011, barmenteros; Link: barmenteros.fx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, barmenteros', 'link': 'barmenteros.fx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 1.0}, 'types': {}, 'colors': {1: [255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Kaufman Efficiency Ratio'}, 'levels': [], 'description': ['Kaufman Efficiency Ratio (also called \\"generalized fractal', 'efficiency\\") according to Perry Kaufman books \\"Smarter Trading\\"', 'and \\"Trading Systems & Methods\\".'], 'name': 'b_kaufman_efficiency_ratio', 'source': 'MQL5 Indicators/Kaufman Efficiency Ratio/b_kaufman_efficiency_ratio.mq5', 'folder': 'Kaufman Efficiency Ratio', 'inputs': [{'mql': 'ERperiod', 'py': 'ERperiod', 'param': 'ERperiod', 'type': 'uchar', 'default': 10, 'label': 'Efficiency ratio period', 'sinput': False}, {'mql': 'histogram', 'py': 'histogram', 'param': 'histogram', 'type': 'int', 'default': 1, 'label': 'Histogram switch', 'sinput': False}, {'mql': 'shift', 'py': 'shift', 'param': 'shift', 'type': 'char', 'default': 0, 'label': 'Horizontal shift (in bars)', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum his_switch
On = 0
Off = 1
_enum('his_switch', {0: 'On', 1: 'Off'})

# ---- inputs and global variables
ERperiod = _input('ERperiod', 10)  # Efficiency ratio period
histogram = _input('histogram', Off)  # Histogram switch
shift = _input('shift', 0)  # Horizontal shift (in bars)
ERBfr = Arr(0, 0.0)

def NetPriceMovement(initialbar, period, price):
    n = 0.0
    n = MathAbs(price[initialbar] - price[initialbar - period])
    return n

def Volatility(initialbar, period, price):
    j = 0
    v = 0.0
    j = 0
    for j in range(j, period):
        v += MathAbs(price[initialbar - j] - price[initialbar - 1 - j])
    else:
        j = _range_end(j, period, 1)
    return v

def OnInit():
    SetIndexBuffer(0, ERBfr)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    if histogram == Off:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
    else:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    PlotIndexSetInteger(0, PLOT_SHIFT, shift)
    short_name = 'KEffRatio('
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + _str(ERperiod) + ')')
    PlotIndexSetString(0, PLOT_LABEL, short_name + _str(ERperiod) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ERperiod)

def OnCalculate(rates_total, prev_calculated, begin, price):
    limit = 0
    i = 0
    direction = 0.0
    noise = 0.0
    if rates_total < (ERperiod - 1 + begin):
        return 0
    if prev_calculated == 0:
        limit = ERperiod + begin
        ArrayInitialize(ERBfr, EMPTY_VALUE)
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        direction = NetPriceMovement(i, ERperiod, price)
        noise = Volatility(i, ERperiod, price)
        if noise == 0.0:
            noise = 1e-09
        ERBfr[i] = _fdiv(direction, noise)
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BKaufmanEfficiencyRatio(_MQL5Indicator):
    name = 'b_kaufman_efficiency_ratio'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ERperiod': 10,  # Efficiency ratio period
        'histogram': _Choice({0: 'On', 1: 'Off'}, default=1),  # Histogram switch
        'shift': 0,  # Horizontal shift (in bars)
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }
    y_range = (0.0, 1.0)

