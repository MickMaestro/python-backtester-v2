"""zigzagcolor — converted from MQL5: MQL5 Indicators/ZigZagColor/zigzagcolor.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 13}, 'colors': {1: [16748574, 255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'zigzagcolor', 'source': 'MQL5 Indicators/ZigZagColor/zigzagcolor.mq5', 'folder': 'ZigZagColor', 'inputs': [{'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
level = 3  # recounting's depth
ZigzagPeakBuffer = Arr(0, 0.0)
ZigzagLawnBuffer = Arr(0, 0.0)
HighMapBuffer = Arr(0, 0.0)
LowMapBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ZigzagPeakBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ZigzagLawnBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, HighMapBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, LowMapBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'ZigZag(' + _str(ExtDepth) + ',' + _str(ExtDeviation) + ',' + _str(ExtBackstep) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'ZigzagColor')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)

def Highest(array, range_, fromIndex):
    res = 0.0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res < array[i]:
            res = array[i]
        i -= 1
    return res

def Lowest(array, range_, fromIndex):
    res = 0.0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res > array[i]:
            res = array[i]
        i -= 1
    return res

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    if rates_total < 100:
        ArrayInitialize(ZigzagPeakBuffer, 0.0)
        ArrayInitialize(ZigzagLawnBuffer, 0.0)
        ArrayInitialize(HighMapBuffer, 0.0)
        ArrayInitialize(LowMapBuffer, 0.0)
        ArrayInitialize(ColorBuffer, 0.0)
        return 0
    counterZ = 0
    whatlookfor = 0
    shift = 0
    back = 0
    lasthighpos = 0
    lastlowpos = 0
    val = 0.0
    res = 0.0
    curlow = 0.0
    curhigh = 0.0
    lasthigh = 0.0
    lastlow = 0.0
    if prev_calculated == 0:
        ArrayInitialize(ZigzagPeakBuffer, 0.0)
        ArrayInitialize(ZigzagLawnBuffer, 0.0)
        ArrayInitialize(HighMapBuffer, 0.0)
        ArrayInitialize(LowMapBuffer, 0.0)
        limit = ExtDepth - 1
    if prev_calculated > 0:
        i = rates_total - 1
        while counterZ < level and i > (rates_total - 100):
            res = ZigzagPeakBuffer[i] + ZigzagLawnBuffer[i]
            if res != 0:
                counterZ += 1
            i -= 1
        i += 1
        limit = i
        if LowMapBuffer[i] != 0:
            curlow = LowMapBuffer[i]
            whatlookfor = 1
        else:
            curhigh = HighMapBuffer[i]
            whatlookfor = -1
        i = limit + 1
        for i in range(i, rates_total):
            ZigzagPeakBuffer[i] = 0.0
            ZigzagLawnBuffer[i] = 0.0
            LowMapBuffer[i] = 0.0
            HighMapBuffer[i] = 0.0
        else:
            i = _range_end(i, rates_total, 1)
    shift = limit
    for shift in range(shift, rates_total):
        val = Lowest(Low, ExtDepth, shift)
        if val == lastlow:
            val = 0.0
        else:
            lastlow = val
            if (Low[shift] - val) > (ExtDeviation * Point()):
                val = 0.0
            else:
                back = ExtBackstep
                for back in range(back, 1 - 1, -1):
                    res = LowMapBuffer[shift - back]
                    if res != 0 and res > val:
                        LowMapBuffer[shift - back] = 0.0
                else:
                    back = _range_end(back, 1 - 1, -1)
        if Low[shift] == val:
            LowMapBuffer[shift] = val
        else:
            LowMapBuffer[shift] = 0.0
        val = Highest(High, ExtDepth, shift)
        if val == lasthigh:
            val = 0.0
        else:
            lasthigh = val
            if (val - High[shift]) > (ExtDeviation * Point()):
                val = 0.0
            else:
                back = ExtBackstep
                for back in range(back, 1 - 1, -1):
                    res = HighMapBuffer[shift - back]
                    if res != 0 and res < val:
                        HighMapBuffer[shift - back] = 0.0
                else:
                    back = _range_end(back, 1 - 1, -1)
        if High[shift] == val:
            HighMapBuffer[shift] = val
        else:
            HighMapBuffer[shift] = 0.0
    else:
        shift = _range_end(shift, rates_total, 1)
    if whatlookfor == 0:
        lastlow = 0.0
        lasthigh = 0.0
    else:
        lastlow = curlow
        lasthigh = curhigh
    shift = limit
    for shift in range(shift, rates_total):
        res = 0.0
        _sw1 = whatlookfor
        if _sw1 == 0:
            if lastlow == 0 and lasthigh == 0:
                if HighMapBuffer[shift] != 0:
                    lasthigh = High[shift]
                    lasthighpos = shift
                    whatlookfor = -1
                    ZigzagPeakBuffer[shift] = lasthigh
                    ColorBuffer[shift] = 0.0
                    res = 1.0
                if LowMapBuffer[shift] != 0:
                    lastlow = Low[shift]
                    lastlowpos = shift
                    whatlookfor = 1
                    ZigzagLawnBuffer[shift] = lastlow
                    ColorBuffer[shift] = 1.0
                    res = 1.0
        elif _sw1 == 1:
            if (LowMapBuffer[shift] != 0.0 and LowMapBuffer[shift] < lastlow) and HighMapBuffer[shift] == 0.0:
                ZigzagLawnBuffer[lastlowpos] = 0.0
                lastlowpos = shift
                lastlow = LowMapBuffer[shift]
                ZigzagLawnBuffer[shift] = lastlow
                ColorBuffer[shift] = 1.0
                res = 1.0
            if HighMapBuffer[shift] != 0.0 and LowMapBuffer[shift] == 0.0:
                lasthigh = HighMapBuffer[shift]
                lasthighpos = shift
                ZigzagPeakBuffer[shift] = lasthigh
                ColorBuffer[shift] = 0.0
                whatlookfor = -1
                res = 1.0
        elif _sw1 == -1:
            if (HighMapBuffer[shift] != 0.0 and HighMapBuffer[shift] > lasthigh) and LowMapBuffer[shift] == 0.0:
                ZigzagPeakBuffer[lasthighpos] = 0.0
                lasthighpos = shift
                lasthigh = HighMapBuffer[shift]
                ZigzagPeakBuffer[shift] = lasthigh
                ColorBuffer[shift] = 0.0
            if LowMapBuffer[shift] != 0.0 and HighMapBuffer[shift] == 0.0:
                lastlow = LowMapBuffer[shift]
                lastlowpos = shift
                ZigzagLawnBuffer[shift] = lastlow
                ColorBuffer[shift] = 1.0
                whatlookfor = 1
        else:
            return rates_total
    else:
        shift = _range_end(shift, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Zigzagcolor(_MQL5Indicator):
    name = 'zigzagcolor'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
    }

