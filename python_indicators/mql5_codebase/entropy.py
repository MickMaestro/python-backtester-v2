"""entropy — converted from MQL5: MQL5 Indicators/Entropy/entropy.mq5

Copyright: Copyright © 2008, Korey; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, Korey', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [6053069]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Entropy'}, 'levels': [0.0], 'description': [], 'name': 'entropy', 'source': 'MQL5 Indicators/Entropy/entropy.mq5', 'folder': 'Entropy', 'inputs': [{'mql': 'Period_', 'py': 'Period_', 'param': 'Period_', 'type': 'int', 'default': 15, 'label': 'Period of the indicator', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period_ = _input('Period_', 15)  # Period of the indicator
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'Entropy(', Period_, ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Period_)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 4)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (Period_ + begin):
        return 0
    first = 0
    bar = 0
    kkk = 0
    sumx = 0.0
    sumx2 = 0.0
    avgx = 0.0
    rmsx = 0.0
    Price0 = 0.0
    Price1 = 0.0
    fPrice = 0.0
    P = 0.0
    G = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = Period_ + begin
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        sumx = 0.0
        sumx2 = 0.0
        for jjj in range(0, Period_):
            kkk = bar - jjj
            Price0 = price[kkk]
            Price1 = price[kkk - 1]
            fPrice = MathLog(_fdiv(Price0, Price1))
            sumx += fPrice
            sumx2 += fPrice * fPrice
        avgx = sumx / Period_
        rmsx = MathSqrt(sumx2 / Period_)
        P = (1.0 + _fdiv(avgx, rmsx)) / 2.0
        G = (P * MathLog(1.0 + rmsx)) + ((1.0 - P) * MathLog(1.0 - rmsx))
        ExtBuffer[bar] = G
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Entropy(_MQL5Indicator):
    name = 'entropy'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_': 15,  # Period of the indicator
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

