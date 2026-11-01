"""vortexindicator — converted from MQL5: MQL5 Indicators/VortexIndicator/vortexindicator.mq5

Copyright: Copyright © 2010, Scratchman; Link: http://creativecommons.org/licenses/by-sa/3.0/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Scratchman', 'link': 'http://creativecommons.org/licenses/by-sa/3.0/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [36095, 65280]}, 'widths': {}, 'styles': {}, 'labels': {1: 'VortexIndicator'}, 'levels': [0.0], 'description': [], 'name': 'vortexindicator', 'source': 'MQL5 Indicators/VortexIndicator/vortexindicator.mq5', 'folder': 'VortexIndicator', 'inputs': [{'mql': 'VI_Length', 'py': 'VI_Length', 'param': 'VI_Length', 'type': 'uint', 'default': 14, 'label': 'indicator period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
VI_Length = _input('VI_Length', 14)  # indicator period
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
DnBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0
Count = Arr(0, 0)
UpVM = Arr(0, 0.0)
DnVM = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = _int(VI_Length)
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
    global ATR_Handle, min_rates_total
    min_rates_total = _int(VI_Length + 1)
    ArrayResize(Count, VI_Length)
    ArrayResize(UpVM, VI_Length)
    ArrayResize(DnVM, VI_Length)
    ArrayInitialize(UpVM, 0.0)
    ArrayInitialize(DnVM, 0.0)
    ATR_Handle = iATR(None, 0, 1)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of iATR indicator')
    SetIndexBuffer(0, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(1, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'VortexIndicator(', VI_Length, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    MaxBar = 0
    limit = 0
    bar = 0
    kkk = 0
    SumUpVM = 0.0
    SumDnVM = 0.0
    SumTR = 0.0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
        to_copy = limit + 1
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1 + _int(VI_Length)
    MaxBar = rates_total - min_rates_total - 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpVM[Count[0]] = MathAbs(high[bar] - low[bar + 1])
        DnVM[Count[0]] = MathAbs(low[bar] - high[bar + 1])
        if bar > MaxBar:
            Recount_ArrayZeroPos(Count)
            continue
        SumUpVM = 0.0
        SumDnVM = 0.0
        SumTR = 0.0
        kkk = 0
        for kkk in range(kkk, _int(VI_Length)):
            SumUpVM += UpVM[kkk]
            SumDnVM += DnVM[kkk]
            SumTR += ATR[bar + kkk]
        else:
            kkk = _range_end(kkk, _int(VI_Length), 1)
        if SumTR:
            UpBuffer[bar] = _fdiv(SumUpVM, SumTR)
            DnBuffer[bar] = _fdiv(SumDnVM, SumTR)
        else:
            UpBuffer[bar] = EMPTY_VALUE
            DnBuffer[bar] = EMPTY_VALUE
        if bar:
            Recount_ArrayZeroPos(Count)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vortexindicator(_MQL5Indicator):
    name = 'vortexindicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'VI_Length': 14,  # indicator period
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

