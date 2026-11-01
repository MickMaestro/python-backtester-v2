"""rangeexpansionindex — converted from MQL5: MQL5 Indicators/Range Expansion Index/rangeexpansionindex.mq5

Calculates Tom DeMark's Range Expansion Index.
Going above 60 and then dropping below 60 signals price weakness.
Going below -60 and the rising above -60 signals price strength.
For more info see The New Science of Technical Analysis.
Copyright: Copyright © 2010, EarnForex.com; Link: http://www.earnforex.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, EarnForex.com', 'link': 'http://www.earnforex.com', 'version': '1.0', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 65280, 16711680, 255, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [60.0, -60.0], 'description': ["Calculates Tom DeMark's Range Expansion Index.", 'Going above 60 and then dropping below 60 signals price weakness.', 'Going below -60 and the rising above -60 signals price strength.', 'For more info see The New Science of Technical Analysis.'], 'name': 'rangeexpansionindex', 'source': 'MQL5 Indicators/Range Expansion Index/rangeexpansionindex.mq5', 'folder': 'Range Expansion Index', 'inputs': [{'mql': 'REI_Period', 'py': 'REI_Period', 'param': 'REI_Period', 'type': 'int', 'default': 8, 'label': 'Smoothing period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
REI_Period = _input('REI_Period', 8)  # Smoothing period
ExtBuffer = Arr(0, 0.0)
ColorExtBuffer = Arr(0, 0.0)
min_rates_total = 0

def SubValue(i, High, Low, Close):
    num_zero1 = 0
    num_zero2 = 0
    diff1 = High[i] - High[i - 2]
    diff2 = Low[i] - Low[i - 2]
    if ((High[i - 2] < Close[i - 7] and High[i - 2] < Close[i - 8]) and High[i] < High[i - 5]) and High[i] < High[i - 6]:
        num_zero1 = 0
    else:
        num_zero1 = 1
    if ((Low[i - 2] > Close[i - 7] and Low[i - 2] > Close[i - 8]) and Low[i] > Low[i - 5]) and Low[i] > Low[i - 6]:
        num_zero2 = 0
    else:
        num_zero2 = 1
    return num_zero1 * num_zero2 * (diff1 + diff2)

def AbsValue(i, High, Low):
    diff1 = MathAbs(High[i] - High[i - 2])
    diff2 = MathAbs(Low[i] - Low[i - 2])
    return diff1 + diff2

def OnInit():
    global min_rates_total
    min_rates_total = REI_Period + 8
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, ColorExtBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'Range Expansion Index(', REI_Period, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first1 = 0
    first2 = 0
    bar = 0
    SubValueSum = 0.0
    AbsValueSum = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = min_rates_total - 1
        first2 = first1 + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
    bar = first1
    for bar in range(bar, rates_total):
        SubValueSum = 0.0
        AbsValueSum = 0.0
        for iii in range(0, REI_Period):
            SubValueSum += SubValue(bar - iii, high, low, close)
            AbsValueSum += AbsValue(bar - iii, high, low)
        if AbsValueSum != 0:
            ExtBuffer[bar] = _fdiv(SubValueSum, AbsValueSum) * 100
        else:
            ExtBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        ColorExtBuffer[bar] = 0.0
        if ExtBuffer[bar] > 0:
            if ExtBuffer[bar] > ExtBuffer[bar - 1]:
                ColorExtBuffer[bar] = 1.0
            if ExtBuffer[bar] < ExtBuffer[bar - 1]:
                ColorExtBuffer[bar] = 2.0
        if ExtBuffer[bar] < 0:
            if ExtBuffer[bar] < ExtBuffer[bar - 1]:
                ColorExtBuffer[bar] = 3.0
            if ExtBuffer[bar] > ExtBuffer[bar - 1]:
                ColorExtBuffer[bar] = 4.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rangeexpansionindex(_MQL5Indicator):
    name = 'rangeexpansionindex'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'REI_Period': 8,  # Smoothing period
    }

