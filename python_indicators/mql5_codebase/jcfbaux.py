"""jcfbaux — converted from MQL5: MQL5 Indicators/JCFBaux/jcfbaux.mq5

Copyright: Copyright © 2005, Weld; Link: http://weld.torguem.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Weld', 'link': 'http://weld.torguem.net', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711935]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'JCFBaux'}, 'levels': [], 'description': [], 'name': 'jcfbaux', 'source': 'MQL5 Indicators/JCFBaux/jcfbaux.mq5', 'folder': 'JCFBaux', 'inputs': [{'mql': 'Depth', 'py': 'Depth', 'param': 'Depth', 'type': 'int', 'default': 15, 'label': 'Indicator smoothing period', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
Depth = _input('Depth', 15)  # Indicator smoothing period
IPC = _input('IPC', PRICE_CLOSE_)  # Applied price
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
min_rates_total = 0
Count = Arr(0, 0)
Series_v = Arr(0, 0.0)

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
    min_rates_total = (Depth * 2) + 1
    ArrayResize(Count, min_rates_total)
    ArrayResize(Series_v, min_rates_total)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'JCFBaux(', Depth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_JRC04, _s_OnCalculate_JRC05, _s_OnCalculate_JRC06
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    jrc04 = 0.0
    jrc05 = 0.0
    jrc06 = 0.0
    jrc08 = 0.0
    jrc03 = 0.0
    jrc13 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    jrc04 = _s_OnCalculate_JRC04
    jrc05 = _s_OnCalculate_JRC05
    jrc06 = _s_OnCalculate_JRC06
    bar = first
    for bar in range(bar, rates_total):
        if rates_total != prev_calculated and bar == (rates_total - 1):
            _s_OnCalculate_JRC04 = jrc04
            _s_OnCalculate_JRC05 = jrc05
            _s_OnCalculate_JRC06 = jrc06
        Series_v[Count[0]] = PriceSeries(IPC, bar, open, low, high, close)
        if bar < Depth:
            if bar < (rates_total - 1):
                Recount_ArrayZeroPos(Count, min_rates_total)
            continue
        if bar >= min_rates_total:
            jrc04 = 0.0
            jrc05 = 0.0
            jrc06 = 0.0
            for iii in range(Depth - 1, 0 - 1, -1):
                jrc03 = MathAbs(Series_v[Count[iii]] - Series_v[Count[iii + 1]])
                jrc04 += jrc03
                jrc05 += (Depth + iii) * jrc03
                jrc06 += Series_v[Count[iii + 1]]
        else:
            jrc03 = MathAbs(Series_v[Count[0]] - Series_v[Count[1]])
            jrc13 = MathAbs(Series_v[Count[Depth]] - Series_v[Count[Depth + 1]])
            jrc04 += jrc03 - jrc13
            jrc05 += (jrc03 * Depth) - jrc04
            jrc06 += Series_v[Count[1]] - Series_v[Count[Depth + 1]]
        jrc08 = MathAbs((Depth * Series_v[Count[0]]) - jrc06)
        if not jrc05:
            IndBuffer[bar] = EMPTY_VALUE
        else:
            IndBuffer[bar] = _fdiv(jrc08, jrc05)
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, min_rates_total)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    else:
        return Close[bar]

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_JRC04 = 0.0
_s_OnCalculate_JRC05 = 0.0
_s_OnCalculate_JRC06 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Jcfbaux(_MQL5Indicator):
    name = 'jcfbaux'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Depth': 15,  # Indicator smoothing period
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Applied price
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

