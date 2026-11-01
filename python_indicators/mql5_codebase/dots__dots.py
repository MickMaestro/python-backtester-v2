"""dots — converted from MQL5: MQL5 Indicators/Dots/dots.mq5

Uses price curve angle calculations to come up with simple price indication.
Simple strategy: enter when 2 dots of same color appear; exit, when different color dot appears.
Copyright: Copyright © 2011, www.EarnForex.com; Link: http://www.earnforex.com/; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, www.EarnForex.com', 'link': 'http://www.earnforex.com/', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [14772545, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['Uses price curve angle calculations to come up with simple price indication.', 'Simple strategy: enter when 2 dots of same color appear; exit, when different color dot appears.'], 'name': 'dots', 'source': 'MQL5 Indicators/Dots/dots.mq5', 'folder': 'Dots', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 10)
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)
Filter = _input('Filter', 0)
Deviation = _input('Deviation', 0.0)
Shift = _input('Shift', 0)
Buffer = Arr(0, 0.0)
Color = Arr(0, 0.0)
MAB = Arr(0, 0.0)
Cycle = 4.0

def OnInit():
    SetIndexBuffer(0, Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Color, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, _int((Length * Cycle) + Length))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dots(' + IntegerToString(Length) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tickvolume, volume, spread):
    i = 0
    shift = 0
    counted_bars = prev_calculated
    limit = 0
    trend = 0
    myMA = 0
    alfa = 0.0
    beta = 0.0
    t = 0.0
    Sum = 0.0
    Weight = 0.0
    g = 0.0
    price = 0.0
    MABuffer_prev = 0.0
    MABuffer = 0.0
    Coeff = 3 * M_PI
    Phase = Length - 1
    Len = _int((Length * Cycle) + Phase)
    if counted_bars < 0:
        return 0
    if counted_bars > 0:
        limit = counted_bars - 1
    else:
        limit = Len - 1
    shift = limit
    for shift in range(shift, rates_total):
        Weight = 0.0
        Sum = 0.0
        t = 0.0
        myMA = iMA(None, 0, 1, 0, MODE_SMA, AppliedPrice)
        if CopyBuffer(myMA, 0, rates_total - shift - 1, Len, MAB) != Len:
            return 0
        i = Len - 1
        for i in range(i, 0 - 1, -1):
            g = _fdiv(1.0, (Coeff * t) + 1)
            if t <= 0.5:
                g = 1.0
            beta = MathCos(M_PI * t)
            alfa = g * beta
            price = MAB[i]
            Sum += alfa * price
            Weight += alfa
            if t < 1:
                t += _fdiv(1.0, Phase - 1)
            elif t < (Len - 1):
                t += _fdiv((2 * Cycle) - 1, (Cycle * Length) - 1)
        else:
            i = _range_end(i, 0 - 1, -1)
        MABuffer_prev = MABuffer
        if Weight > 0:
            MABuffer = _fdiv((1.0 + (Deviation / 100)) * Sum, Weight)
        if Filter > 0:
            if MathAbs(MABuffer - MABuffer_prev) < (Filter * Point()):
                MABuffer = MABuffer_prev
        if (MABuffer - MABuffer_prev) > (Filter * Point()):
            trend = 1
        elif (MABuffer_prev - MABuffer) > (Filter * Point()):
            trend = -1
        if trend != 0:
            Buffer[shift] = MABuffer
        if trend > 0:
            Color[shift] = 0.0
        elif trend < 0:
            Color[shift] = 1.0
    else:
        shift = _range_end(shift, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dots(_MQL5Indicator):
    name = 'dots'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,
        'AppliedPrice': 1,
        'Filter': 0,
        'Deviation': 0.0,
        'Shift': 0,
    }

