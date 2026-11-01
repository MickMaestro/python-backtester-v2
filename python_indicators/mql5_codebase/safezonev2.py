"""safezonev2 — converted from MQL5: MQL5 Indicators/SafeZoneV2/safezonev2.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper SafeZoneV2', 2: 'Lower SafeZoneV2'}, 'levels': [], 'description': [], 'name': 'safezonev2', 'source': 'MQL5 Indicators/SafeZoneV2/safezonev2.mq5', 'folder': 'SafeZoneV2', 'inputs': [{'mql': 'Median', 'py': 'Median', 'param': 'Median', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Max', 'py': 'Max', 'param': 'Max', 'type': 'uint', 'default': 52, 'label': '', 'sinput': False}, {'mql': 'MASAFE', 'py': 'MASAFE', 'param': 'MASAFE', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
Median = _input('Median', 10)
Max = _input('Max', 52)
MASAFE = _input('MASAFE', 3)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
DnBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
min_rates_total = 0
Count = Arr(0, 0)
SRange = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = _int(Max)
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
    min_rates_total = _int(Median + Max + MASAFE)
    ArrayResize(Count, Max)
    ArrayResize(SRange, Max)
    ArraySetAsSeries(SRange, True)
    ArrayInitialize(SRange, 0.0)
    SetIndexBuffer(0, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'SafeZoneV2(', Median, ', ', Max, ', ', MASAFE, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    range_ = 0.0
    maximum = 0.0
    SmaH = 0.0
    SmaL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        range_ = high[bar] - low[bar]
        SRange[Count[0]] = _s_OnCalculate_SMA.SMASeries(0, prev_calculated, rates_total, Median, range_, bar, False)
        maximum = SRange[ArrayMaximum(SRange, 0, WHOLE_ARRAY)]
        SmaH = _s_OnCalculate_SMAH.SMASeries(0, prev_calculated, rates_total, MASAFE, high[bar], bar, False)
        SmaL = _s_OnCalculate_SMAL.SMASeries(0, prev_calculated, rates_total, MASAFE, low[bar], bar, False)
        DnBuffer[bar] = SmaL - maximum
        UpBuffer[bar] = SmaH + maximum
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_SMA = CMoving_Average()
_s_OnCalculate_SMAH = CMoving_Average()
_s_OnCalculate_SMAL = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Safezonev2(_MQL5Indicator):
    name = 'safezonev2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Median': 10,
        'Max': 52,
        'MASAFE': 3,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

