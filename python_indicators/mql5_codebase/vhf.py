"""vhf — converted from MQL5: MQL5 Indicators/VHF (Vertical Horizontal Filter)/vhf.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'VHF'}, 'levels': [], 'description': [], 'name': 'vhf', 'source': 'MQL5 Indicators/VHF (Vertical Horizontal Filter)/vhf.mq5', 'folder': 'VHF (Vertical Horizontal Filter)', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 28, 'label': 'Indicator period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N = _input('N', 28)  # Indicator period
ExtLineBuffer = Arr(0, 0.0)
min_rates_total = 0
Count = Arr(0, 0)
Temp = Arr(0, 0.0)

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
    min_rates_total = N + 1
    ArrayResize(Count, N)
    ArrayResize(Temp, N)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Temp, 0.0)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'VHF( N = ', N, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    hh = 0.0
    ll = 0.0
    a = 0.0
    b = 0.0
    res = 0.0
    limit = 0
    bar = 0
    maxbar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    maxbar = rates_total - min_rates_total - 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Temp[Count[0]] = MathAbs(close[bar] - close[bar + 1])
        if bar < maxbar:
            hh = high[ArrayMaximum(high, bar, N)]
            ll = low[ArrayMinimum(low, bar, N)]
            a = hh - ll
            b = 0.0
            for kkk in range(0, N):
                b += Temp[Count[kkk]]
            if b:
                res = _fdiv(a, b)
            else:
                res = 0.0
        else:
            res = EMPTY_VALUE
        ExtLineBuffer[bar] = res
        if bar > 0:
            Recount_ArrayZeroPos(Count, N)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vhf(_MQL5Indicator):
    name = 'vhf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'N': 28,  # Indicator period
    }

