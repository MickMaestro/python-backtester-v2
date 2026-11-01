"""zigzagonparabolic — converted from MQL5: MQL5 Indicators/ZigZag on Parabolic/zigzagonparabolic.mq5

ZigZag on Parabolic
Copyright: Copyright © 2009, EarnForex; Link: http://www.earnforex.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, EarnForex', 'link': 'http://www.earnforex.com', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 13}, 'colors': {1: [8034025, 16748574]}, 'widths': {1: 1}, 'styles': {1: 1}, 'labels': {1: 'ZigZag'}, 'levels': [], 'description': ['ZigZag on Parabolic'], 'name': 'zigzagonparabolic', 'source': 'MQL5 Indicators/ZigZag on Parabolic/zigzagonparabolic.mq5', 'folder': 'ZigZag on Parabolic', 'inputs': [{'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'double', 'default': 0.02, 'label': 'SAR step', 'sinput': False}, {'mql': 'Maximum', 'py': 'Maximum', 'param': 'Maximum', 'type': 'double', 'default': 0.2, 'label': 'SAR maximum', 'sinput': False}, {'mql': 'ExtremumsShift', 'py': 'ExtremumsShift', 'param': 'ExtremumsShift', 'type': 'bool', 'default': True, 'label': 'Top shift flag', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Step = _input('Step', 0.02)  # SAR step
Maximum = _input('Maximum', 0.2)  # SAR maximum
ExtremumsShift = _input('ExtremumsShift', True)  # Top shift flag
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
EShift = 0
min_rates_total = 0
SAR_Handle = 0

def OnInit():
    global EShift, SAR_Handle, min_rates_total
    min_rates_total = 1
    if ExtremumsShift:
        EShift = 1
    else:
        EShift = 0
    SAR_Handle = iSAR(None, 0, Step, Maximum)
    if SAR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the SAR indicator')
    SetIndexBuffer(0, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighestBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetString(0, PLOT_LABEL, 'ZigZag Lowest')
    PlotIndexSetString(1, PLOT_LABEL, 'ZigZag Highest')
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    ArraySetAsSeries(ColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'ZigZag on Parabolic(', Step, ', ', Maximum, ', ', ExtremumsShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_dir_, _s_OnCalculate_h_, _s_OnCalculate_j_, _s_OnCalculate_l_, _s_OnCalculate_lastcolor_
    if BarsCalculated(SAR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    j = 0
    limit = 0
    climit = 0
    to_copy = 0
    bar = 0
    shift = 0
    NewBar = 0
    lastcolor = 0
    h = 0.0
    l = 0.0
    mid0 = 0.0
    mid1 = 0.0
    SAR = Arr(0, 0.0)
    dir = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
        _s_OnCalculate_h_ = 0.0
        _s_OnCalculate_l_ = 999999999.0
        _s_OnCalculate_dir_ = False
        _s_OnCalculate_j_ = 0
        _s_OnCalculate_lastcolor_ = 0
    else:
        limit = rates_total - prev_calculated
    climit = limit
    to_copy = limit + 2
    if limit == 0:
        NewBar = 1
    else:
        NewBar = 0
    ArraySetAsSeries(SAR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if CopyBuffer(SAR_Handle, 0, 0, to_copy, SAR) <= 0:
        return 0
    j = _s_OnCalculate_j_
    dir = _s_OnCalculate_dir_
    h = _s_OnCalculate_h_
    l = _s_OnCalculate_l_
    lastcolor = _s_OnCalculate_lastcolor_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_j_ = j
            _s_OnCalculate_dir_ = dir
            _s_OnCalculate_h_ = h
            _s_OnCalculate_l_ = l
        mid0 = (high[bar] + low[bar]) / 2
        mid1 = (high[bar + 1] + low[bar + 1]) / 2
        HighestBuffer[bar] = 0.0
        LowestBuffer[bar] = 0.0
        if bar > 0:
            j += 1
        if dir:
            if h < high[bar]:
                h = high[bar]
                j = NewBar
            if SAR[bar + 1] <= mid1 and SAR[bar] > mid0:
                shift = bar + (EShift * (j + NewBar))
                if shift > (rates_total - 1):
                    shift = rates_total - 1
                HighestBuffer[shift] = h
                dir = False
                l = low[bar]
                j = 0
                if shift > climit:
                    climit = shift
        else:
            if l > low[bar]:
                l = low[bar]
                j = NewBar
            if SAR[bar + 1] >= mid1 and SAR[bar] < mid0:
                shift = bar + (EShift * (j + NewBar))
                if shift > (rates_total - 1):
                    shift = rates_total - 1
                LowestBuffer[shift] = l
                dir = True
                h = high[bar]
                j = 0
                if shift > climit:
                    climit = shift
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = climit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_lastcolor_ = lastcolor
        if HighestBuffer[bar] == 0.0 or LowestBuffer[bar] == 0.0:
            ColorBuffer[bar] = lastcolor
        if HighestBuffer[bar] != 0.0 or LowestBuffer[bar] != 0.0:
            if lastcolor == 0:
                ColorBuffer[bar] = 1.0
                lastcolor = 1
            else:
                ColorBuffer[bar] = 0.0
                lastcolor = 0
        if HighestBuffer[bar] != 0.0 or LowestBuffer[bar] == 0.0:
            ColorBuffer[bar] = 1.0
            lastcolor = 1
        if HighestBuffer[bar] == 0.0 or LowestBuffer[bar] != 0.0:
            ColorBuffer[bar] = 0.0
            lastcolor = 0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_j_ = 0
_s_OnCalculate_lastcolor_ = 0
_s_OnCalculate_dir_ = False
_s_OnCalculate_h_ = 0.0
_s_OnCalculate_l_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Zigzagonparabolic(_MQL5Indicator):
    name = 'zigzagonparabolic'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Step': 0.02,  # SAR step
        'Maximum': 0.2,  # SAR maximum
        'ExtremumsShift': True,  # Top shift flag
    }

