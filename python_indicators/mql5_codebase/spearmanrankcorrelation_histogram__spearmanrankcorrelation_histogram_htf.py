"""SpearmanRankCorrelation_Histogram — converted from MQL5: MQL5 Indicators/SpearmanRankCorrelation_Histogram_HTF/SpearmanRankCorrelation_Histogram.mq5

Copyright: Copyright © 2007, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': -1.0, 'indicator_maximum': 1.0}, 'types': {1: 10}, 'colors': {1: [16711935, 8388736, 8421504, 16711680, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'SpearmanRankCorrelation_Histogram', 'source': 'MQL5 Indicators/SpearmanRankCorrelation_Histogram_HTF/SpearmanRankCorrelation_Histogram.mq5', 'folder': 'SpearmanRankCorrelation_Histogram_HTF', 'inputs': [{'mql': 'rangeN', 'py': 'rangeN', 'param': 'rangeN', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'CalculatedBars', 'py': 'CalculatedBars', 'param': 'CalculatedBars', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Maxrange', 'py': 'Maxrange', 'param': 'Maxrange', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'direction', 'py': 'direction', 'param': 'direction', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'inHighLevel', 'py': 'inHighLevel', 'param': 'inHighLevel', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}, {'mql': 'inLowLevel', 'py': 'inLowLevel', 'param': 'inLowLevel', 'type': 'double', 'default': -0.5, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
rangeN = _input('rangeN', 14)
CalculatedBars = _input('CalculatedBars', 0)
Maxrange = _input('Maxrange', 30)
direction = _input('direction', True)
inHighLevel = _input('inHighLevel', 0.5)
inLowLevel = _input('inLowLevel', -0.5)
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
multiply = 0.0
R2 = Arr(0, 0.0)
TrueRanks = Arr(0, 0.0)
PriceInt = Arr(0, 0)
SortInt = Arr(0, 0)
Maxrange_ = 0

def SpearmanRankCorrelation(Ranks, N):
    res = 0.0
    z2 = 0.0
    for iii in range(0, N):
        z2 += MathPow(Ranks[iii] - iii - 1, 2)
    res = 1 - _fdiv(6 * z2, MathPow(N, 3) - N)
    return res

def RankPrices(TrueRanks_, InitialArray):
    i = 0
    k = 0
    m = 0
    dublicat = 0
    counter = 0
    etalon = 0
    dcounter = 0.0
    averageRank = 0.0
    ArrayCopy(SortInt, InitialArray, 0, 0, WHOLE_ARRAY)
    i = 0
    for i in range(i, rangeN):
        TrueRanks_[i] = i + 1
    else:
        i = _range_end(i, rangeN, 1)
    ArraySort(SortInt)
    i = 0
    while i < (rangeN - 1):
        if SortInt[i] != SortInt[i + 1]:
            i += 1
            continue
        dublicat = SortInt[i]
        k = i + 1
        counter = 1
        averageRank = i + 1
        while k < rangeN:
            if SortInt[k] == dublicat:
                counter += 1
                averageRank += k + 1
                k += 1
            else:
                break
        dcounter = counter
        averageRank = _fdiv(averageRank, dcounter)
        m = i
        for m in range(m, k):
            TrueRanks_[m] = averageRank
        else:
            m = _range_end(m, k, 1)
        i = k
        i += 1
    i = 0
    for i in range(i, rangeN):
        etalon = InitialArray[i]
        k = 0
        while k < rangeN:
            if etalon == SortInt[k]:
                R2[i] = TrueRanks_[k]
                break
            k += 1
    else:
        i = _range_end(i, rangeN, 1)
    return

def OnInit():
    global Maxrange_, multiply
    ArrayResize(R2, rangeN)
    ArrayResize(PriceInt, rangeN)
    ArrayResize(SortInt, rangeN)
    if direction:
        ArraySetAsSeries(SortInt, True)
    ArrayResize(TrueRanks, rangeN)
    if Maxrange <= 0:
        Maxrange_ = 10
    else:
        Maxrange_ = Maxrange
    multiply = MathPow(10, Digits())
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rangeN)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    if rangeN > Maxrange_:
        shortname.v = 'Decrease rangeN input!'
    else:
        StringConcatenate(shortname, 'SpearmanRankCorrelation_Histogram(', rangeN, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inHighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, inLowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (rangeN + begin):
        return 0
    if rangeN > Maxrange_:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2 - rangeN - begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rangeN + begin)
    else:
        if not CalculatedBars:
            limit = rates_total - prev_calculated
        else:
            limit = CalculatedBars
    ArraySetAsSeries(price, True)
    for bar in range(limit, 0 - 1, -1):
        for k in range(0, rangeN):
            PriceInt[k] = _int(price[bar + k] * multiply)
        RankPrices(TrueRanks, PriceInt)
        IndBuffer[bar] = SpearmanRankCorrelation(R2, rangeN)
        clr = 2
        res = IndBuffer[bar]
        if res > 0:
            if res > inHighLevel:
                clr = 4
            else:
                clr = 3
        if res < 0:
            if res < inLowLevel:
                clr = 0
            else:
                clr = 1
        ColorIndBuffer[bar] = clr
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SpearmanRankCorrelationHistogram(_MQL5Indicator):
    name = 'SpearmanRankCorrelation_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'rangeN': 14,
        'CalculatedBars': 0,
        'Maxrange': 30,
        'direction': True,
        'inHighLevel': 0.5,
        'inLowLevel': -0.5,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }
    y_range = (-1.0, 1.0)

