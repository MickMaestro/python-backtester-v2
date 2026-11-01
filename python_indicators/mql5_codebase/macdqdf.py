"""macdqdf — converted from MQL5: MQL5 Indicators/The Moving Average Indicator, based on the Quasi-Digital Filter/macdqdf.mq5

Moving Average Convergence/Divergence. Used QDF
Copyright: 2010, Vlad; Link: http://www.becemal.ru/mql

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, Vlad', 'link': 'http://www.becemal.ru/mql', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 1}, 'colors': {1: [14772545], 2: [1993170]}, 'widths': {1: 2, 2: 1}, 'styles': {}, 'labels': {1: 'MACD', 2: 'Signal'}, 'levels': [], 'description': ['Moving Average Convergence/Divergence. Used QDF'], 'name': 'macdqdf', 'source': 'MQL5 Indicators/The Moving Average Indicator, based on the Quasi-Digital Filter/macdqdf.mq5', 'folder': 'The Moving Average Indicator, based on the Quasi-Digital Filter', 'inputs': [{'mql': 'FastMA', 'py': 'FastMA', 'param': 'FastMA', 'type': 'int', 'default': 12, 'label': 'Fast QDF Period', 'sinput': False}, {'mql': 'SlowMA', 'py': 'SlowMA', 'param': 'SlowMA', 'type': 'int', 'default': 36, 'label': 'Slow QDF Period', 'sinput': False}, {'mql': 'SignalMA', 'py': 'SignalMA', 'param': 'SignalMA', 'type': 'int', 'default': 9, 'label': 'Signal QDF Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastMA = _input('FastMA', 12)  # Fast QDF Period
SlowMA = _input('SlowMA', 36)  # Slow QDF Period
SignalMA = _input('SignalMA', 9)  # Signal QDF Period
MacdBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
FastMultiplier = Arr(0, 0.0)
SlowMultiplier = Arr(0, 0.0)
SignalMultiplier = Arr(0, 0.0)

def CalcMultiplier(M, P):
    i = 0
    SM = 0.0
    ArrayResize(M, P, 256)
    ArrayInitialize(M, 0.0)
    i = 0
    for i in range(i, P):
        M[i] = MathExp(_fdiv(_fdiv(-2.0 * M_PI * i * i, P), P))
    else:
        i = _range_end(i, P, 1)
    SM = 0.0
    i = 0
    for i in range(i, P):
        SM += M[i]
    else:
        i = _range_end(i, P, 1)
    i = 0
    for i in range(i, P):
        M[i] = _fdiv(M[i], SM)
    else:
        i = _range_end(i, P, 1)

def OnInit():
    SetIndexBuffer(0, MacdBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, SignalMA - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD(' + _str(FastMA) + ',' + _str(SlowMA) + ',' + _str(SignalMA) + ')')
    CalcMultiplier(FastMultiplier, FastMA)
    CalcMultiplier(SlowMultiplier, SlowMA)
    CalcMultiplier(SignalMultiplier, SignalMA)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < SignalMA:
        return 0
    if rates_total < SlowMA:
        return 0
    limit = prev_calculated - 1
    if limit < SlowMA:
        limit = SlowMA
    i = limit
    while i < rates_total:
        SF = 0.0
        for j in range(0, FastMA):
            SF += price[i - j] * FastMultiplier[j]
        SS = 0.0
        for j in range(0, SlowMA):
            SS += price[i - j] * SlowMultiplier[j]
        MacdBuffer[i] = SF - SS
        i += 1
    limit = prev_calculated - 1
    if limit < SignalMA:
        limit = SignalMA
    i = limit
    while i < rates_total:
        SS = 0.0
        for j in range(0, SignalMA):
            SS += MacdBuffer[i - j] * SignalMultiplier[j]
        SignalBuffer[i] = SS
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Macdqdf(_MQL5Indicator):
    name = 'macdqdf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastMA': 12,  # Fast QDF Period
        'SlowMA': 36,  # Slow QDF Period
        'SignalMA': 9,  # Signal QDF Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

