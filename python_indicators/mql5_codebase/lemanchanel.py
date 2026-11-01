"""lemanchanel — converted from MQL5: MQL5 Indicators/LeManChanel/lemanchanel.mq5

Copyright: Copyright © 2009, LeMan.; Link: b-market@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, LeMan.', 'link': 'b-market@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [16711935]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper LeMan', 2: 'Lower LeMan'}, 'levels': [], 'description': [], 'name': 'lemanchanel', 'source': 'MQL5 Indicators/LeManChanel/lemanchanel.mq5', 'folder': 'LeManChanel', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 1, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 12)
Shift = _input('Shift', 1)  # horizontal shift of the indicator in bars
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
Count = Arr(0, 0)
HC = Arr(0, 0.0)
CL = Arr(0, 0.0)
min_rates_total = 0

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
    min_rates_total = _int(period + 1)
    ArrayResize(Count, period)
    ArrayResize(HC, period)
    ArrayResize(CL, period)
    ArraySetAsSeries(HC, True)
    ArraySetAsSeries(CL, True)
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpperBuffer, True)
    SetIndexBuffer(1, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LowerBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'LeManChanel(', period, ',', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HC[Count[0]] = high[bar] - close[bar + 1]
        CL[Count[0]] = close[bar + 1] - low[bar]
        UpperBuffer[bar] = close[bar] + HC[ArrayMaximum(HC, 0, period)]
        LowerBuffer[bar] = close[bar] - CL[ArrayMaximum(CL, 0, period)]
        if bar > 0:
            Recount_ArrayZeroPos(Count, period)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Lemanchanel(_MQL5Indicator):
    name = 'lemanchanel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 12,
        'Shift': 1,  # horizontal shift of the indicator in bars
    }

