"""ttm-trend — converted from MQL5: MQL5 Indicators/TTM-Trend_HTF/ttm-trend.mq5

Copyright: Copyright © 2005, Nick Bilak; Link: beluck[AT]gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Nick Bilak', 'link': 'beluck[AT]gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [9639167, 8388736, 8421504, 8421376, 65280]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ttm-trend'}, 'levels': [], 'description': [], 'name': 'ttm-trend', 'source': 'MQL5 Indicators/TTM-Trend_HTF/ttm-trend.mq5', 'folder': 'TTM-Trend_HTF', 'inputs': [{'mql': 'CompBars', 'py': 'CompBars', 'param': 'CompBars', 'type': 'uint', 'default': 6, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CompBars = _input('CompBars', 6)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Count = Arr(0, 0)
haOpen = Arr(0, 0.0)
haClose = Arr(0, 0.0)

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
    min_rates_total = _int(CompBars + 1)
    ArrayResize(Count, CompBars)
    ArrayResize(haOpen, CompBars)
    ArrayResize(haClose, CompBars)
    ArrayInitialize(Count, 0)
    ArrayInitialize(haOpen, 0.0)
    ArrayInitialize(haClose, 0.0)
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnIndBuffer, True)
    SetIndexBuffer(2, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ttm-trend')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        barc = limit + _int(CompBars - 1)
        haOpen[Count[0]] = Open[barc]
        haClose[Count[0]] = (Open[barc] + High[barc] + Low[barc] + Close[barc]) / 4.0
        Recount_ArrayZeroPos(Count, CompBars)
        for index in range(_int(CompBars - 1) - 1, 0 - 1, -1):
            barl = limit + index
            haOpen[Count[0]] = (haOpen[Count[1]] + haClose[Count[1]]) / 2.0
            haClose[Count[0]] = (Open[barl] + High[barl] + Low[barl] + Close[barl]) / 4.0
            Recount_ArrayZeroPos(Count, CompBars)
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpIndBuffer[bar] = High[bar]
        DnIndBuffer[bar] = Low[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        haOpen[Count[0]] = (haOpen[Count[1]] + haClose[Count[1]]) / 2.0
        haClose[Count[0]] = (Open[bar] + High[bar] + Low[bar] + Close[bar]) / 4.0
        clr = 2
        if haClose[Count[0]] > haOpen[Count[0]]:
            if Open[bar] <= Close[bar]:
                clr = 4
            if Open[bar] > Close[bar]:
                clr = 3
        if haClose[Count[0]] < haOpen[Count[0]]:
            if Open[bar] > Close[bar]:
                clr = 0
            if Open[bar] <= Close[bar]:
                clr = 1
        for index in range(1, _int(CompBars)):
            HH = MathMax(haOpen[Count[index]], haClose[Count[index]])
            LL = MathMin(haOpen[Count[index]], haClose[Count[index]])
            if ((haOpen[Count[0]] <= HH and haOpen[Count[0]] >= LL) and haClose[Count[0]] <= HH) and haClose[Count[0]] >= LL:
                clr = _int(ColorIndBuffer[bar + index])
                break
        ColorIndBuffer[bar] = clr
        if bar:
            Recount_ArrayZeroPos(Count, CompBars)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TtmTrend(_MQL5Indicator):
    name = 'ttm-trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CompBars': 6,
    }

