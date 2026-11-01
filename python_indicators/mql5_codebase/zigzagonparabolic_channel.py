"""ZigZagOnParabolic_channel — converted from MQL5: MQL5 Indicators/ZigZagOnParabolic_channel/ZigZagOnParabolic_channel.mq5

ZigZag on Parabolic в виде канала
Copyright: Copyright © 2009, EarnForex; Link: http://www.earnforex.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, EarnForex', 'link': 'http://www.earnforex.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 7, 2: 8, 3: 8, 4: 5, 5: 5}, 'colors': {1: [16443110], 2: [8421376, 8388736], 3: [8421376, 8388736], 4: [16748574], 5: [9639167]}, 'widths': {2: 2, 3: 2, 4: 1, 5: 1}, 'styles': {}, 'labels': {1: 'ZigZagOnParabolic_channel Cloud', 2: 'Up ZigZagOnParabolic_channel', 3: 'Down ZigZagOnParabolic_channel', 4: 'Up ZigZagOnParabolic_Arrows', 5: 'Down ZigZagOnParabolic_Arrows'}, 'levels': [], 'description': ['ZigZag on Parabolic в виде канала'], 'name': 'ZigZagOnParabolic_channel', 'source': 'MQL5 Indicators/ZigZagOnParabolic_channel/ZigZagOnParabolic_channel.mq5', 'folder': 'ZigZagOnParabolic_channel', 'inputs': [{'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'double', 'default': 0.02, 'label': 'SAR шаг', 'sinput': False}, {'mql': 'Maximum', 'py': 'Maximum', 'param': 'Maximum', 'type': 'double', 'default': 0.2, 'label': 'SAR максимум', 'sinput': False}, {'mql': 'ExtremumsShift', 'py': 'ExtremumsShift', 'param': 'ExtremumsShift', 'type': 'bool', 'default': True, 'label': 'флаг сдвига вершины', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'uint', 'default': 163, 'label': 'лейба верхнего фрактала', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'uint', 'default': 163, 'label': 'лейба нижнего фрактала', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Step = _input('Step', 0.02)  # SAR шаг
Maximum = _input('Maximum', 0.2)  # SAR максимум
ExtremumsShift = _input('ExtremumsShift', True)  # флаг сдвига вершины
UpLable = _input('UpLable', 163)  # лейба верхнего фрактала
DnLable = _input('DnLable', 163)  # лейба нижнего фрактала
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
ColorUpperBuffer = Arr(0, 0.0)
ColorLowerBuffer = Arr(0, 0.0)
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
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
        Print(' Не удалось получить хендл индикатора SAR')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, UpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorUpperBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, LowerBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ColorLowerBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, HighestBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, LowestBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(UpBuffer, True)
    ArraySetAsSeries(DnBuffer, True)
    ArraySetAsSeries(UpperBuffer, True)
    ArraySetAsSeries(LowerBuffer, True)
    ArraySetAsSeries(ColorUpperBuffer, True)
    ArraySetAsSeries(ColorLowerBuffer, True)
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, DnLable)
    PlotIndexSetInteger(4, PLOT_ARROW, UpLable)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'ZigZagOnParabolic_channel')
    return INIT_SUCCEEDED

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
    barHH = 0
    barLL = 0
    barHH1 = 0
    barLL1 = 0
    h = 0.0
    l = 0.0
    mid0 = 0.0
    mid1 = 0.0
    SAR = Arr(0, 0.0)
    HH = Box(0.0)
    LL = Box(0.0)
    HH1 = Box(0.0)
    LL1 = Box(0.0)
    dir = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
        _s_OnCalculate_h_ = 0.0
        _s_OnCalculate_l_ = 999999999.0
        _s_OnCalculate_dir_ = False
        _s_OnCalculate_j_ = 0
        _s_OnCalculate_lastcolor_ = 0
        for index in range(rates_total - 1, limit - 1, -1):
            UpBuffer[index] = 0.0
            UpperBuffer[index] = 0.0
            HighestBuffer[index] = 0.0
            DnBuffer[index] = 0.0
            LowerBuffer[index] = 0.0
            LowestBuffer[index] = 0.0
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
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        barHH = FindFirstExtremum(bar, rates_total, HighestBuffer, HH)
        barHH1 = FindFirstExtremum(barHH + 1, rates_total, HighestBuffer, HH1)
        if barHH >= 0 and barHH1 >= 0:
            for index in range(barHH1 - 1, barHH, -1):
                UpBuffer[index] = HH1.v
                UpperBuffer[index] = HH1.v
                ColorUpperBuffer[index] = ColorUpperBuffer[index + 1]
            for index in range(barHH, bar - 1, -1):
                UpBuffer[index] = HH.v
                UpperBuffer[index] = HH.v
                if HH.v > HH1.v:
                    ColorUpperBuffer[index] = 0.0
                elif HH.v < HH1.v:
                    ColorUpperBuffer[index] = 1.0
                else:
                    ColorUpperBuffer[index] = ColorUpperBuffer[index + 1]
        barLL = FindFirstExtremum(bar, rates_total, LowestBuffer, LL)
        barLL1 = FindFirstExtremum(barLL + 1, rates_total, LowestBuffer, LL1)
        if barLL >= 0 and barLL1 >= 0:
            for index in range(barLL1 - 1, barLL, -1):
                DnBuffer[index] = LL1.v
                LowerBuffer[index] = LL1.v
                ColorLowerBuffer[index] = ColorLowerBuffer[index + 1]
            for index in range(barLL, bar - 1, -1):
                DnBuffer[index] = LL.v
                LowerBuffer[index] = LL.v
                if LL.v > LL1.v:
                    ColorLowerBuffer[index] = 0.0
                elif LL.v < LL1.v:
                    ColorLowerBuffer[index] = 1.0
                else:
                    ColorLowerBuffer[index] = ColorLowerBuffer[index + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def FindFirstExtremum(StartPos, Rates_total, Array, Extremum):
    for bar in range(StartPos, Rates_total):
        if Array[bar] and Array[bar] != EMPTY_VALUE:
            Extremum.v = Array[bar]
            return bar
            break
    Extremum.v = 0.0
    return -1

# ---- static local variables
_s_OnCalculate_j_ = 0
_s_OnCalculate_lastcolor_ = 0
_s_OnCalculate_dir_ = False
_s_OnCalculate_h_ = 0.0
_s_OnCalculate_l_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigZagOnParabolicChannel(_MQL5Indicator):
    name = 'ZigZagOnParabolic_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Step': 0.02,  # SAR шаг
        'Maximum': 0.2,  # SAR максимум
        'ExtremumsShift': True,  # флаг сдвига вершины
        'UpLable': 163,  # лейба верхнего фрактала
        'DnLable': 163,  # лейба нижнего фрактала
    }

