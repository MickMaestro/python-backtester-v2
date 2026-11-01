"""demobufferpattern — converted from MQL5: MQL5 Indicators/DemoBufferPattern/demobufferpattern.mq5

Copyright: 2010, Loong@forum.mql4.com; Link: http://login.mql5.com/en/users/Loong; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, Loong@forum.mql4.com', 'link': 'http://login.mql5.com/en/users/Loong', 'version': '1.00', 'window': 'separate', 'indicator_plots': 5, 'indicator_buffers': 15}, 'types': {1: 17, 2: 5, 3: 5, 4: 13, 5: 8}, 'colors': {1: [255, 65280], 2: [255], 3: [65280], 4: [255, 16711680], 5: [16711935, 65535, 16760576]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'demobufferpattern', 'source': 'MQL5 Indicators/DemoBufferPattern/demobufferpattern.mq5', 'folder': 'DemoBufferPattern', 'inputs': [{'mql': 'ExtPeriod', 'py': 'ExtPeriod', 'param': 'ExtPeriod', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtPeriod = _input('ExtPeriod', 10)
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
level = 3  # recounting's depth
P1B1 = Arr(0, 0.0)  # data buffer
P1B2 = Arr(0, 0.0)
P1B3 = Arr(0, 0.0)
P1B4 = Arr(0, 0.0)
P1BC = Arr(0, 0.0)  # color buffer
P2B1 = Arr(0, 0.0)  # data buffer
P3B1 = Arr(0, 0.0)  # data buffer
P4B1 = Arr(0, 0.0)  # data buffer
P4B2 = Arr(0, 0.0)  # data buffer
P4BC = Arr(0, 0.0)  # color buffer
P4M1 = Arr(0, 0.0)  # calc buffer
P4M2 = Arr(0, 0.0)  # calc buffer
P5B1 = Arr(0, 0.0)  # data buffer
P5BC = Arr(0, 0.0)  # color buffer
iArrowShift = 10
maHandle = 0

def OnInit():
    global maHandle
    SetIndexBuffer(0, P1B1, INDICATOR_DATA)
    SetIndexBuffer(1, P1B2, INDICATOR_DATA)
    SetIndexBuffer(2, P1B3, INDICATOR_DATA)
    SetIndexBuffer(3, P1B4, INDICATOR_DATA)
    SetIndexBuffer(4, P1BC, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, P2B1, INDICATOR_DATA)
    SetIndexBuffer(6, P3B1, INDICATOR_DATA)
    SetIndexBuffer(7, P4B1, INDICATOR_DATA)
    SetIndexBuffer(8, P4B2, INDICATOR_DATA)
    SetIndexBuffer(9, P4BC, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(10, P5B1, INDICATOR_DATA)
    SetIndexBuffer(11, P5BC, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(12, P4M1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, P4M2, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_ARROW, 217)
    PlotIndexSetInteger(2, PLOT_ARROW, 218)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -iArrowShift)
    PlotIndexSetInteger(2, PLOT_ARROW_SHIFT, iArrowShift)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    maHandle = iMA(Symbol(), 0, ExtPeriod, 0, MODE_EMA, PRICE_CLOSE)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    CalcCandles(rates_total, prev_calculated, open, high, low, close)
    CalcFractal(rates_total, prev_calculated, high, low, P2B1, P3B1)
    CalcZigzag(rates_total, prev_calculated, high, low, P4B1, P4B2, P4BC, P4M1, P4M2)
    CalcColorMA(rates_total, prev_calculated, P5B1, P5BC)
    return rates_total

def CalcCandles(rates_total, prev_calculated, open, high, low, close):
    i = 0
    if i < prev_calculated:
        i = prev_calculated - 1
    while i < rates_total:
        P1B1[i] = open[i]
        P1B2[i] = high[i]
        P1B3[i] = low[i]
        P1B4[i] = close[i]
        P1BC[i] = float((0 if (close[i] > open[i]) else 1))
        i += 1
    return rates_total

def CalcFractal(rates_total, prev_calculated, High, Low, Upper, Lower):
    i = 0
    limit = 0
    if rates_total < 5:
        return 0
    if prev_calculated < 7:
        limit = 2
        ArrayInitialize(Upper, EMPTY_VALUE)
        ArrayInitialize(Lower, EMPTY_VALUE)
    else:
        limit = rates_total - 5
    i = limit
    for i in range(i, rates_total - 3):
        if ((High[i] > High[i + 1] and High[i] > High[i + 2]) and High[i] >= High[i - 1]) and High[i] >= High[i - 2]:
            Upper[i] = High[i]
        else:
            Upper[i] = EMPTY_VALUE
        if ((Low[i] < Low[i + 1] and Low[i] < Low[i + 2]) and Low[i] <= Low[i - 1]) and Low[i] <= Low[i - 2]:
            Lower[i] = Low[i]
        else:
            Lower[i] = EMPTY_VALUE
    else:
        i = _range_end(i, rates_total - 3, 1)
    return rates_total

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

def CalcZigzag(rates_total, prev_calculated, High, Low, ZigzagPeakBuffer, ZigzagLawnBuffer, ColorBuffer, HighMapBuffer, LowMapBuffer):
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

def getIndexOfColor(i):
    j = _imod(i, 300)
    if j < 100:
        return 0
    if j < 200:
        return 1
    return 2

def CalcColorMA(rates_total, prev_calculated, ColorLineBuffer, ColorsBuffer):
    calculated = BarsCalculated(maHandle)
    if calculated < rates_total:
        Print('Not all data of maHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    if prev_calculated == 0:
        if CopyBuffer(maHandle, 0, 0, rates_total, ColorLineBuffer) <= 0:
            return 0
        for i in range(0, rates_total):
            ColorsBuffer[i] = getIndexOfColor(i)
    else:
        to_copy = 0
        if prev_calculated > rates_total or prev_calculated < 0:
            to_copy = rates_total
        else:
            to_copy = rates_total - prev_calculated
            if prev_calculated > 0:
                to_copy += 1
        copied = CopyBuffer(maHandle, 0, 0, rates_total, ColorLineBuffer)
        if copied <= 0:
            return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Demobufferpattern(_MQL5Indicator):
    name = 'demobufferpattern'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtPeriod': 10,
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
    }

