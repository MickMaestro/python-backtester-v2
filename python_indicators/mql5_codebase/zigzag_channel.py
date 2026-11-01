"""ZigZag_channel — converted from MQL5: MQL5 Indicators/ZigZag_channel/ZigZag_channel.mq5

ZigZag
Copyright: Copyright © 2005, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 7, 2: 8, 3: 8, 4: 5, 5: 5}, 'colors': {1: [16443110], 2: [16748574, 8388736], 3: [16748574, 8388736], 4: [3329330], 5: [9639167]}, 'widths': {2: 2, 3: 2, 4: 2, 5: 2}, 'styles': {}, 'labels': {1: 'ZigZag_NK_channel Cloud', 2: 'Up ZigZag_NK_channel', 3: 'Down ZigZag_NK_channel', 4: 'Up ZigZag_NK_Arrows', 5: 'Down ZigZag_NK_Arrows'}, 'levels': [], 'description': ['ZigZag'], 'name': 'ZigZag_channel', 'source': 'MQL5 Indicators/ZigZag_channel/ZigZag_channel.mq5', 'folder': 'ZigZag_channel', 'inputs': [{'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'uint', 'default': 159, 'label': 'лейба верхнего фрактала', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'uint', 'default': 159, 'label': 'лейба нижнего фрактала', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
UpLable = _input('UpLable', 159)  # лейба верхнего фрактала
DnLable = _input('DnLable', 159)  # лейба нижнего фрактала
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
ColorUpperBuffer = Arr(0, 0.0)
ColorLowerBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
LowestBuffer = Arr(0, 0.0)
LASTlowpos = 0
LASThighpos = 0
LASTlow0 = 0.0
LASTlow1 = 0.0
LASThigh0 = 0.0
LASThigh1 = 0.0
dExtDeviation = 0.0
min_rates_total = 0

def OnInit():
    global dExtDeviation, min_rates_total
    min_rates_total = _int(ExtDepth + ExtBackstep)
    dExtDeviation = ExtDeviation * Point()
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
    shortname = Box("")
    StringConcatenate(shortname, 'ZigZag (ExtDepth=', ExtDepth, 'ExtDeviation = ', ExtDeviation, 'ExtBackstep = ', ExtBackstep, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LASThigh0, LASThigh1, LASThighpos, LASTlow0, LASTlow1, LASTlowpos
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    back = 0
    lasthighpos = 0
    lastlowpos = 0
    barHH = 0
    barLL = 0
    barHH1 = 0
    barLL1 = 0
    curlow = 0.0
    curhigh = 0.0
    lasthigh0 = 0.0
    lastlow0 = 0.0
    lasthigh1 = 0.0
    lastlow1 = 0.0
    val = 0.0
    res = 0.0
    HH = Box(0.0)
    LL = Box(0.0)
    HH1 = Box(0.0)
    LL1 = Box(0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        lastlow1 = -1.0
        lasthigh1 = -1.0
        lastlowpos = -1
        lasthighpos = -1
        for index in range(rates_total - 1, limit - 1, -1):
            UpBuffer[index] = 0.0
            UpperBuffer[index] = 0.0
            HighestBuffer[index] = 0.0
            DnBuffer[index] = 0.0
            LowerBuffer[index] = 0.0
            LowestBuffer[index] = 0.0
    else:
        limit = rates_total - prev_calculated
        lastlow0 = LASTlow0
        lasthigh0 = LASThigh0
        lastlow1 = LASTlow1
        lasthigh1 = LASThigh1
        lastlowpos = LASTlowpos + limit
        lasthighpos = LASThighpos + limit
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            LASTlow0 = lastlow0
            LASThigh0 = lasthigh0
        val = low[ArrayMinimum(low, bar, ExtDepth)]
        if val == lastlow0:
            val = 0.0
        else:
            lastlow0 = val
            if (low[bar] - val) > (ExtDeviation * Point()):
                val = 0.0
            else:
                back = 1
                for back in range(back, _int(ExtBackstep) + 1):
                    res = LowestBuffer[bar + back]
                    if res and res > val:
                        LowestBuffer[bar + back] = 0.0
                else:
                    back = _range_end(back, _int(ExtBackstep) + 1, 1)
        LowestBuffer[bar] = val
        val = high[ArrayMaximum(high, bar, ExtDepth)]
        if val == lasthigh0:
            val = 0.0
        else:
            lasthigh0 = val
            if (val - high[bar]) > (ExtDeviation * Point()):
                val = 0.0
            else:
                back = 1
                for back in range(back, _int(ExtBackstep) + 1):
                    res = HighestBuffer[bar + back]
                    if res and res < val:
                        HighestBuffer[bar + back] = 0.0
                else:
                    back = _range_end(back, _int(ExtBackstep) + 1, 1)
        HighestBuffer[bar] = val
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and (not bar):
            LASTlow1 = lastlow1
            LASThigh1 = lasthigh1
            LASTlowpos = lastlowpos
            LASThighpos = lasthighpos
        curlow = LowestBuffer[bar]
        curhigh = HighestBuffer[bar]
        if (not curlow) and (not curhigh):
            continue
        if curhigh:
            if lasthigh1 > 0:
                if lasthigh1 < curhigh:
                    HighestBuffer[lasthighpos] = 0.0
                else:
                    HighestBuffer[bar] = 0.0
            if lasthigh1 < curhigh or lasthigh1 < 0:
                lasthigh1 = curhigh
                lasthighpos = bar
            lastlow1 = -1.0
        if curlow:
            if lastlow1 > 0:
                if lastlow1 > curlow:
                    LowestBuffer[lastlowpos] = 0.0
                else:
                    LowestBuffer[bar] = 0.0
            if curlow < lastlow1 or lastlow1 < 0:
                lastlow1 = curlow
                lastlowpos = bar
            lasthigh1 = -1.0
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigZagChannel(_MQL5Indicator):
    name = 'ZigZag_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
        'UpLable': 159,  # лейба верхнего фрактала
        'DnLable': 159,  # лейба нижнего фрактала
    }

