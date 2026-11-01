"""zigzag — converted from MQL5: MQL5 Indicators/ZigZag/zigzag.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Zigzag'}, 'levels': [], 'description': [], 'name': 'zigzag', 'source': 'MQL5 Indicators/ZigZag/zigzag.mq5', 'folder': 'ZigZag', 'inputs': [{'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
ZigzagBuffer = Arr(0, 0.0)  # main buffer
HighMapBuffer = Arr(0, 0.0)  # highs
LowMapBuffer = Arr(0, 0.0)  # lows
level = 3  # recounting depth
deviation = 0.0  # deviation in points

def OnInit():
    global deviation
    SetIndexBuffer(0, ZigzagBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighMapBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, LowMapBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetString(0, PLOT_LABEL, 'ZigZag(' + _str(ExtDepth) + ',' + _str(ExtDeviation) + ',' + _str(ExtBackstep) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    deviation = ExtDeviation * Point()
    return INIT_SUCCEEDED

def iHighest_u(array, depth, startPos):
    index = startPos
    if startPos < 0:
        Print('Invalid parameter in the function iHighest, startPos =', startPos)
        return 0
    size = ArraySize(array)
    if (startPos - depth) < 0:
        depth = startPos
    max_ = array[startPos]
    for i in range(startPos, startPos - depth, -1):
        if array[i] > max_:
            index = i
            max_ = array[i]
    return index

def iLowest_u(array, depth, startPos):
    index = startPos
    if startPos < 0:
        Print('Invalid parameter in the function iLowest, startPos =', startPos)
        return 0
    size = ArraySize(array)
    if (startPos - depth) < 0:
        depth = startPos
    min_ = array[startPos]
    for i in range(startPos, startPos - depth, -1):
        if array[i] < min_:
            index = i
            min_ = array[i]
    return index

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    limit = 0
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
    Pike = 1
    Sill = -1
    if prev_calculated == 0:
        ArrayInitialize(ZigzagBuffer, 0.0)
        ArrayInitialize(HighMapBuffer, 0.0)
        ArrayInitialize(LowMapBuffer, 0.0)
    if rates_total < 100:
        return 0
    if prev_calculated == 0:
        limit = ExtDepth
    if prev_calculated > 0:
        i = rates_total - 1
        while counterZ < level and i > (rates_total - 100):
            res = ZigzagBuffer[i]
            if res != 0:
                counterZ += 1
            i -= 1
        i += 1
        limit = i
        if LowMapBuffer[i] != 0:
            curlow = LowMapBuffer[i]
            whatlookfor = Pike
        else:
            curhigh = HighMapBuffer[i]
            whatlookfor = Sill
        i = limit + 1
        for i in range(i, rates_total):
            ZigzagBuffer[i] = 0.0
            LowMapBuffer[i] = 0.0
            HighMapBuffer[i] = 0.0
        else:
            i = _range_end(i, rates_total, 1)
    shift = limit
    for shift in range(shift, rates_total):
        val = low[iLowest_u(low, ExtDepth, shift)]
        if val == lastlow:
            val = 0.0
        else:
            lastlow = val
            if (low[shift] - val) > deviation:
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = LowMapBuffer[shift - back]
                    if res != 0 and res > val:
                        LowMapBuffer[shift - back] = 0.0
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        if low[shift] == val:
            LowMapBuffer[shift] = val
        else:
            LowMapBuffer[shift] = 0.0
        val = high[iHighest_u(high, ExtDepth, shift)]
        if val == lasthigh:
            val = 0.0
        else:
            lasthigh = val
            if (val - high[shift]) > deviation:
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = HighMapBuffer[shift - back]
                    if res != 0 and res < val:
                        HighMapBuffer[shift - back] = 0.0
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        if high[shift] == val:
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
                    lasthigh = high[shift]
                    lasthighpos = shift
                    whatlookfor = Sill
                    ZigzagBuffer[shift] = lasthigh
                    res = 1.0
                if LowMapBuffer[shift] != 0:
                    lastlow = low[shift]
                    lastlowpos = shift
                    whatlookfor = Pike
                    ZigzagBuffer[shift] = lastlow
                    res = 1.0
        elif _sw1 == Pike:
            if (LowMapBuffer[shift] != 0.0 and LowMapBuffer[shift] < lastlow) and HighMapBuffer[shift] == 0.0:
                ZigzagBuffer[lastlowpos] = 0.0
                lastlowpos = shift
                lastlow = LowMapBuffer[shift]
                ZigzagBuffer[shift] = lastlow
                res = 1.0
            if HighMapBuffer[shift] != 0.0 and LowMapBuffer[shift] == 0.0:
                lasthigh = HighMapBuffer[shift]
                lasthighpos = shift
                ZigzagBuffer[shift] = lasthigh
                whatlookfor = Sill
                res = 1.0
        elif _sw1 == Sill:
            if (HighMapBuffer[shift] != 0.0 and HighMapBuffer[shift] > lasthigh) and LowMapBuffer[shift] == 0.0:
                ZigzagBuffer[lasthighpos] = 0.0
                lasthighpos = shift
                lasthigh = HighMapBuffer[shift]
                ZigzagBuffer[shift] = lasthigh
            if LowMapBuffer[shift] != 0.0 and HighMapBuffer[shift] == 0.0:
                lastlow = LowMapBuffer[shift]
                lastlowpos = shift
                ZigzagBuffer[shift] = lastlow
                whatlookfor = Pike
        else:
            return rates_total
    else:
        shift = _range_end(shift, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Zigzag(_MQL5Indicator):
    name = 'zigzag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
    }

