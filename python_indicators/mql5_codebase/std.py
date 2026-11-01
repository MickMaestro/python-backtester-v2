"""STD — converted from MQL5: MQL5 Indicators/STD_HTF/STD.mq5

The Simple Trend Detector. Based on code RSI
Copyright: Copyright © 2010, BECEMAL; Link: http://www.becemal.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, BECEMAL', 'link': 'http://www.becemal.ru/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 1}, 'colors': {1: [15631086]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Simple Trend Detector'}, 'levels': [80.0, 50.0, 20.0], 'description': ['The Simple Trend Detector. Based on code RSI'], 'name': 'STD', 'source': 'MQL5 Indicators/STD_HTF/STD.mq5', 'folder': 'STD_HTF', 'inputs': [{'mql': 'STDPeriod', 'py': 'STDPeriod', 'param': 'STDPeriod', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
STDPeriod = _input('STDPeriod', 15)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
STDBuffer = Arr(0, 0.0)
min_rates_total = 0
Count = Arr(0, 0)
Pos = Arr(0, 0.0)
Neg = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global min_rates_total
    min_rates_total = _int(STDPeriod)
    ArrayResize(Count, STDPeriod)
    ArrayResize(Pos, STDPeriod)
    ArrayResize(Neg, STDPeriod)
    SetIndexBuffer(0, STDBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(STDBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Simple Trend Detector')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        ArrayInitialize(Count, 0)
        ArrayInitialize(Pos, 0.0)
        ArrayInitialize(Neg, 0.0)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        positive = 0.0
        negative = 0.0
        rel = close[bar] - open[bar]
        if rel > 0:
            positive = rel
        else:
            negative = -rel
        Pos[Count[0]] = positive
        Neg[Count[0]] = negative
        for kkk in range(0, _int(STDPeriod)):
            Norm = _int(STDPeriod) - kkk + 1
            positive += Norm * Pos[Count[kkk]]
            negative += Norm * Neg[Count[kkk]]
        Den = positive + negative
        if not Den:
            STDBuffer[bar] = 100.0
        else:
            STDBuffer[bar] = _fdiv(100 * positive, Den)
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, STDPeriod)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class STD(_MQL5Indicator):
    name = 'STD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'STDPeriod': 15,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }
    y_range = (0.0, 100.0)

