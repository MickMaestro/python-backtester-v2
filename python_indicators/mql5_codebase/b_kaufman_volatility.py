"""b_kaufman_volatility — converted from MQL5: MQL5 Indicators/Kaufman Volatility/b_kaufman_volatility.mq5

Kaufman Volatility according to Perry Kaufman books \\"Smarter Trading\\".
Copyright: Copyright © 2011, barmenteros; Link: barmenteros.fx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, barmenteros', 'link': 'barmenteros.fx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {1: [255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Kaufman Volatility'}, 'levels': [], 'description': ['Kaufman Volatility according to Perry Kaufman books \\"Smarter Trading\\".'], 'name': 'b_kaufman_volatility', 'source': 'MQL5 Indicators/Kaufman Volatility/b_kaufman_volatility.mq5', 'folder': 'Kaufman Volatility', 'inputs': [{'mql': 'ERperiod', 'py': 'ERperiod', 'param': 'ERperiod', 'type': 'uchar', 'default': 10, 'label': 'Efficiency ratio period', 'sinput': False}, {'mql': 'histogram', 'py': 'histogram', 'param': 'histogram', 'type': 'int', 'default': 1, 'label': 'Histogram switch', 'sinput': False}, {'mql': 'shift', 'py': 'shift', 'param': 'shift', 'type': 'char', 'default': 0, 'label': 'Horizontal shift (in bars)', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum his_switch
On = 0
Off = 1
_enum('his_switch', {0: 'On', 1: 'Off'})

# ---- inputs and global variables
ERperiod = _input('ERperiod', 10)  # Efficiency ratio period
histogram = _input('histogram', Off)  # Histogram switch
shift = _input('shift', 0)  # Horizontal shift (in bars)
KVBfr = Arr(0, 0.0)

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
    SetIndexBuffer(0, KVBfr)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    if histogram == Off:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
    else:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    PlotIndexSetInteger(0, PLOT_SHIFT, shift)
    short_name = 'KVolatility('
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + _str(ERperiod) + ')')
    PlotIndexSetString(0, PLOT_LABEL, short_name + _str(ERperiod) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ERperiod)

def OnCalculate(rates_total, prev_calculated, begin, price):
    limit = 0
    i = 0
    if rates_total < (ERperiod - 1 + begin):
        return 0
    if prev_calculated == 0:
        limit = ERperiod + begin
        ArrayInitialize(KVBfr, EMPTY_VALUE)
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        KVBfr[i] = Volatility(i, ERperiod, price)
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BKaufmanVolatility(_MQL5Indicator):
    name = 'b_kaufman_volatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ERperiod': 10,  # Efficiency ratio period
        'histogram': _Choice({0: 'On', 1: 'Off'}, default=1),  # Histogram switch
        'shift': 0,  # Horizontal shift (in bars)
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

