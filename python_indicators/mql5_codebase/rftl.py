"""rftl — converted from MQL5: MQL5 Indicators/RFTL/rftl.mq5

Copyright: Copyright 2002, Finware.ru Ltd.; Link: http://www.finware.ru/; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2002, Finware.ru Ltd.', 'link': 'http://www.finware.ru/', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13959039]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'RFTL'}, 'levels': [], 'description': [], 'name': 'rftl', 'source': 'MQL5 Indicators/RFTL/rftl.mq5', 'folder': 'RFTL', 'inputs': [{'mql': 'RFTLShift', 'py': 'RFTLShift', 'param': 'RFTLShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of moving average in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RFTLShift = _input('RFTLShift', 0)  # Horizontal shift of moving average in bars
RFTLPeriod = 0
ExtLineBuffer = Arr(0, 0.0)
RFTLTable = Arr.of([-0.0025097319, 0.0513007762, 0.1142800493, 0.169934286, 0.2025269304, 0.2025269304, 0.169934286, 0.1142800493, 0.0513007762, -0.0025097319, -0.0353166244, -0.0433375629, -0.0311244617, -0.0088618137, 0.0120580088, 0.0233183633, 0.0221931304, 0.0115769653, -0.0022157966, -0.0126536111, -0.0157416029, -0.011339583, -0.002590561, 0.0059521459, 0.0105212252, 0.0096970755, 0.0046585685, -0.001707923, -0.0063513565, -0.007453935, -0.0050439973, -0.0007459678, 0.0032271474, 0.0051357867, 0.0044454862, 0.0018784961, -0.0011065767, -0.0031162862, -0.0033443253, -0.0022163335, 0.0002573669, 0.000365079, 0.0060440751, 0.0018747783], fill=0.0)

def OnInit():
    global RFTLPeriod
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, RFTLShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, RFTLPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'RFTL(', RFTLShift, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    RFTLPeriod = ArraySize(RFTLTable)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, RFTLPeriod)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (RFTLPeriod - 1 + begin):
        return 0
    first = 0
    bar = 0
    iii = 0
    RFTL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = RFTLPeriod - 1 + begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin + RFTLPeriod)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        RFTL = 0.0
        iii = 0
        for iii in range(iii, RFTLPeriod):
            RFTL += RFTLTable[iii] * price[bar - iii]
        else:
            iii = _range_end(iii, RFTLPeriod, 1)
        ExtLineBuffer[bar] = RFTL
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rftl(_MQL5Indicator):
    name = 'rftl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RFTLShift': 0,  # Horizontal shift of moving average in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

