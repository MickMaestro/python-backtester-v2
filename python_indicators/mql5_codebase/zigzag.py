"""ZigZag — converted from MQL5: MQL5 Indicators/Fibo ZigZag/ZigZag.mq5

Copyright: Сергей Семёнов; Link: https://www.mql5.com/ru/users/namespace; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Сергей Семёнов', 'link': 'https://www.mql5.com/ru/users/namespace', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 9}, 'types': {1: 2, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5}, 'colors': {1: [8519755], 2: [32768], 3: [4678655], 4: [2330219], 5: [2263842], 6: [11186720], 7: [8421376]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ZigzagFibo'}, 'levels': [], 'description': [], 'name': 'ZigZag', 'source': 'MQL5 Indicators/Fibo ZigZag/ZigZag.mq5', 'folder': 'Fibo ZigZag', 'inputs': [{'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
ZigzagBuffer = Arr(0, 0.0)  # main buffer
HighMapBuffer = Arr(0, 0.0)  # highs
LowMapBuffer = Arr(0, 0.0)  # lows
Level236 = Arr(0, 0.0)
Level382 = Arr(0, 0.0)
Level500 = Arr(0, 0.0)
Level618 = Arr(0, 0.0)
SignalLongBuffer = Arr(0, 0.0)
SignalShortBuffer = Arr(0, 0.0)
level = 3  # recounting depth
deviation = 0.0  # deviation in points

def OnInit():
    global deviation
    SetIndexBuffer(0, ZigzagBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SignalLongBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, SignalShortBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, Level236, INDICATOR_DATA)
    SetIndexBuffer(4, Level382, INDICATOR_DATA)
    SetIndexBuffer(5, Level500, INDICATOR_DATA)
    SetIndexBuffer(6, Level618, INDICATOR_DATA)
    SetIndexBuffer(7, HighMapBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, LowMapBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetString(0, PLOT_LABEL, 'ZigZagFibo(' + _str(ExtDepth) + ',' + _str(ExtDeviation) + ',' + _str(ExtBackstep) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    PlotIndexSetInteger(2, PLOT_ARROW, 108)
    PlotIndexSetInteger(3, PLOT_ARROW, 140)
    PlotIndexSetInteger(4, PLOT_ARROW, 141)
    PlotIndexSetInteger(5, PLOT_ARROW, 142)
    PlotIndexSetInteger(6, PLOT_ARROW, 143)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 2)
    PlotIndexSetInteger(2, PLOT_LINE_WIDTH, 2)
    PlotIndexSetInteger(3, PLOT_LINE_WIDTH, 2)
    PlotIndexSetInteger(4, PLOT_LINE_WIDTH, 2)
    PlotIndexSetInteger(5, PLOT_LINE_WIDTH, 2)
    PlotIndexSetInteger(6, PLOT_LINE_WIDTH, 2)
    deviation = ExtDeviation * Point()
    return 0

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
    global _s_OnCalculate_lastSignalHigh, _s_OnCalculate_lastSignalLow
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
        ArrayInitialize(SignalLongBuffer, 0.0)
        ArrayInitialize(SignalShortBuffer, 0.0)
        ArrayInitialize(Level236, 0.0)
        ArrayInitialize(Level382, 0.0)
        ArrayInitialize(Level500, 0.0)
        ArrayInitialize(Level618, 0.0)
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
                if lastlow != _s_OnCalculate_lastSignalLow:
                    if lasthigh:
                        Level236[shift] = lastlow - getFiboLevel(_s_OnCalculate_lastSignalHigh, lastlow, 0.236)
                        Level382[shift] = lastlow - getFiboLevel(_s_OnCalculate_lastSignalHigh, lastlow, 0.382)
                        Level500[shift] = lastlow - getFiboLevel(_s_OnCalculate_lastSignalHigh, lastlow, 0.5)
                        Level618[shift] = lastlow - getFiboLevel(_s_OnCalculate_lastSignalHigh, lastlow, 0.618)
                    SignalShortBuffer[shift] = lastlow
                    _s_OnCalculate_lastSignalLow = SignalShortBuffer[shift]
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
                if lastlow and lasthigh != _s_OnCalculate_lastSignalHigh:
                    if lastlow:
                        Level236[shift] = lasthigh + getFiboLevel(lasthigh, _s_OnCalculate_lastSignalLow, 0.236)
                        Level382[shift] = lasthigh + getFiboLevel(lasthigh, _s_OnCalculate_lastSignalLow, 0.382)
                        Level500[shift] = lasthigh + getFiboLevel(lasthigh, _s_OnCalculate_lastSignalLow, 0.5)
                        Level618[shift] = lasthigh + getFiboLevel(lasthigh, _s_OnCalculate_lastSignalLow, 0.618)
                    SignalLongBuffer[shift] = lasthigh
                    _s_OnCalculate_lastSignalHigh = SignalLongBuffer[shift]
        else:
            return rates_total
    else:
        shift = _range_end(shift, rates_total, 1)
    return rates_total

def getFiboLevel(high, low, fibo):
    range_ = (high - low) * fibo
    return NormalizeDouble(range_, Digits())

# ---- static local variables
_s_OnCalculate_lastSignalHigh = 0.0
_s_OnCalculate_lastSignalLow = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigZag(_MQL5Indicator):
    name = 'ZigZag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
    }

