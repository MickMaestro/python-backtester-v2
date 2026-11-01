"""chande_kroll_stop_v1 — converted from MQL5: MQL5 Indicators/Chande_Kroll_Stop_v1_HTF/chande_kroll_stop_v1.mq5

Copyright: Copyright © 2006, Forex-TSD.com ; Link: http://www.forex-tsd.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Forex-TSD.com ', 'link': 'http://www.forex-tsd.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16760576, 8421504]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Chande_Kroll_Stop_v1'}, 'levels': [], 'description': [''], 'name': 'chande_kroll_stop_v1', 'source': 'MQL5 Indicators/Chande_Kroll_Stop_v1_HTF/chande_kroll_stop_v1.mq5', 'folder': 'Chande_Kroll_Stop_v1_HTF', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 20)
ATRPeriod = _input('ATRPeriod', 10)
Kv = _input('Kv', 3.0)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpTrend = Arr(0, 0.0)
DnTrend = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0
Count = Arr(0, 0)
smin = Arr(0, 0.0)
smax = Arr(0, 0.0)

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
    global ATR_Handle, min_rates_total
    min_rates_total = _int(ATRPeriod + Length)
    ATR_Handle = iATR(None, 0, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    ArrayResize(Count, Length)
    ArrayResize(smin, Length)
    ArrayResize(smax, Length)
    ArrayInitialize(smin, -999999)
    ArrayInitialize(smax, 999999)
    ArraySetAsSeries(smin, True)
    ArraySetAsSeries(smax, True)
    SetIndexBuffer(0, UpTrend, INDICATOR_DATA)
    ArraySetAsSeries(UpTrend, True)
    SetIndexBuffer(1, DnTrend, INDICATOR_DATA)
    ArraySetAsSeries(DnTrend, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'Chande_Kroll_Stop_v1(', Length, ', ', ATRPeriod, ', ', Kv, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    ATR = Arr(0, 0.0)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - _int(ATRPeriod)
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        smin[Count[0]] = high[ArrayMaximum(high, bar, ATRPeriod)] - (Kv * ATR[bar])
        smax[Count[0]] = low[ArrayMinimum(low, bar, ATRPeriod)] + (Kv * ATR[bar])
        UpTrend[bar] = smin[ArrayMaximum(smin, 0, WHOLE_ARRAY)]
        DnTrend[bar] = smax[ArrayMinimum(smax, 0, WHOLE_ARRAY)]
        if bar:
            Recount_ArrayZeroPos(Count, Length)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChandeKrollStopV1(_MQL5Indicator):
    name = 'chande_kroll_stop_v1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 20,
        'ATRPeriod': 10,
        'Kv': 3.0,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

