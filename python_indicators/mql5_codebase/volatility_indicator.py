"""Volatility_indicator — converted from MQL5: MQL5 Indicators/Volatility Indicator/Volatility_indicator.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Volatility_indicator', 'source': 'MQL5 Indicators/Volatility Indicator/Volatility_indicator.mq5', 'folder': 'Volatility Indicator', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'MAShift', 'py': 'MAShift', 'param': 'MAShift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 5)
MAShift = _input('MAShift', 0)
ExtLineBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, MAShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MAPeriod - 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (MAPeriod - 1):
        return 0
    first = 0
    bar = 0
    iii = 0
    Sum = 0.0
    SMA = 0.0
    if prev_calculated == 0:
        first = MAPeriod - 1 + begin
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Sum = 0.0
        iii = 0
        for iii in range(iii, MAPeriod):
            Sum += price[bar - iii]
        else:
            iii = _range_end(iii, MAPeriod, 1)
        SMA = Sum / MAPeriod
        SMA = SMA - price[bar]
        ExtLineBuffer[bar] = SMA
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityIndicator(_MQL5Indicator):
    name = 'Volatility_indicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 5,
        'MAShift': 0,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

