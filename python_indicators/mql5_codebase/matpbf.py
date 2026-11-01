"""matpbf — converted from MQL5: MQL5 Indicators/Moving Average_ 3-Pole Butterworth Filter/matpbf.mq5

Copyright: BECEMAL; Link: http://www.becemal.ru/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'BECEMAL', 'link': 'http://www.becemal.ru/', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711935]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TPBF'}, 'levels': [], 'description': [], 'name': 'matpbf', 'source': 'MQL5 Indicators/Moving Average_ 3-Pole Butterworth Filter/matpbf.mq5', 'folder': 'Moving Average_ 3-Pole Butterworth Filter', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 24, 'label': 'period of MA', 'sinput': False}, {'mql': 'MAShift', 'py': 'MAShift', 'param': 'MAShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the average in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 24)  # period of MA
MAShift = _input('MAShift', 0)  # Horizontal shift of the average in bars
BF = Arr(0, 0.0)
B1 = 0.0
B2 = 0.0
B3 = 0.0
B4 = 0.0

def TPBF(InPeriod, R1, R2, R3, R4):
    CutOffPeriod = InPeriod
    if CutOffPeriod < 4.0:
        CutOffPeriod = 4.0
    a1 = MathExp(_fdiv(-1.0 * M_PI, CutOffPeriod))
    b1 = 2.0 * a1 * MathCos(_fdiv(M_PI * MathSqrt(3.0), CutOffPeriod))
    c1 = a1 * a1
    R2.v = b1 + c1
    R3.v = -(c1 + (b1 * c1))
    R4.v = c1 * c1
    R1.v = 1.0 - R2.v - R3.v - R4.v
    return True

def OnInit():
    SetIndexBuffer(0, BF, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, MAShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MAPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'TPBF(', MAPeriod, ', ', MAShift, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    TPBF(float(MAPeriod), _GlobRef(globals(), 'B1'), _GlobRef(globals(), 'B2'), _GlobRef(globals(), 'B3'), _GlobRef(globals(), 'B4'))

def OnCalculate(rates_total, prev_calculated, begin, price):
    i = 0
    limit = 0
    if prev_calculated == 0:
        limit = MAPeriod + begin - 1
        t = price[limit + 1]
        i = 0
        for i in range(i, limit):
            BF[i] = t
        else:
            i = _range_end(i, limit, 1)
        firstValue = 0.0
        limit += 1
        i = begin
        for i in range(i, limit):
            firstValue += price[i]
        else:
            i = _range_end(i, limit, 1)
        firstValue = firstValue / MAPeriod
        BF[limit - 1] = firstValue
        BF[limit - 2] = firstValue
        BF[limit - 3] = firstValue
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        BF[i] = (B1 * price[i]) + (B2 * BF[i - 1]) + (B3 * BF[i - 2]) + (B4 * BF[i - 3])
    else:
        i = _range_end(i, rates_total, 1)
    if False:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Matpbf(_MQL5Indicator):
    name = 'matpbf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 24,  # period of MA
        'MAShift': 0,  # Horizontal shift of the average in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

