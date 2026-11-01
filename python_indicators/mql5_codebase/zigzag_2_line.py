"""ZigZag_2_Line — converted from MQL5: MQL5 Indicators/ZigZag 2 rays/ZigZag_2_Line.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.3

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.3', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Zigzag'}, 'levels': [], 'description': [], 'name': 'ZigZag_2_Line', 'source': 'MQL5 Indicators/ZigZag 2 rays/ZigZag_2_Line.mq5', 'folder': 'ZigZag 2 rays', 'inputs': [{'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'ObjLineDel', 'py': 'ObjLineDel', 'param': 'ObjLineDel', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
ObjLineDel = _input('ObjLineDel', True)
ZigzagBuffer = Arr(0, 0.0)  # main buffer
HighMapBuffer = Arr(0, 0.0)  # highs
LowMapBuffer = Arr(0, 0.0)  # lows
level = 3  # recounting depth
deviation = 0.0  # deviation in points
price_zig = Arr(10, 0.0, dyn=False)  # Last Point Buffer Price
time_zig = Arr(10, 0, dyn=False)  # Last Point Buffer Time
pr_1 = 0.0
pr_2 = 0.0
t_1 = 0
t_2 = 0

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

def OnDeinit(reason):
    if ObjLineDel:
        ObjectDelete(0, 'ZZCR1')
        ObjectDelete(0, 'ZZCR2')

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
    ArraySetAsSeries(ZigzagBuffer, False)
    ArraySetAsSeries(time, False)
    ArraySetAsSeries(low, False)
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
        ArrayInitialize(price_zig, 0.0)
        ArrayInitialize(time_zig, 0.0)
    if prev_calculated == 0:
        limit = ExtDepth
    if rates_total < 100:
        return 0
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
    fl_stop = False
    shift = 0
    n = 0
    fl_low = False
    ArraySetAsSeries(ZigzagBuffer, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(low, True)
    while not fl_stop:
        if ZigzagBuffer[shift] != 0:
            if n > 0:
                if (ND(ZigzagBuffer[shift]) - ND(low[shift])) == 0.0:
                    price_zig[n] = ZigzagBuffer[shift]
                    if (n - 1) == 0:
                        fl_low = True
                else:
                    price_zig[n] = ZigzagBuffer[shift]
                time_zig[n] = iTimeMQL4(Symbol(), Period(), shift)
            n += 1
            if n >= 6:
                fl_stop = True
        shift += 1
    if fl_low:
        SetLowZZ(price_zig[2], price_zig[4], time_zig[2], time_zig[4])
        SetHighZZ(price_zig[1], price_zig[3], time_zig[1], time_zig[3])
    else:
        SetLowZZ(price_zig[1], price_zig[3], time_zig[1], time_zig[3])
        SetHighZZ(price_zig[2], price_zig[4], time_zig[2], time_zig[4])
    return rates_total

def ND(A):
    return NormalizeDouble(A, Digits())

def iTimeMQL4(symbol, tf, index):
    if index < 0:
        return -1
    timeframe = TFMigrate(tf)
    Arr_ = Arr(0, 0)
    if CopyTime(symbol, timeframe, index, 1, Arr_) > 0:
        return Arr_[0]
    else:
        return -1

def SetLowZZ(price_1, price_2, time_1, time_2):
    ObjectDelete(0, 'ZZCR1')
    ObjectCreate(0, 'ZZCR1', OBJ_TREND, 0, time_2, price_2, time_1, price_1)
    ObjectSetInteger(0, 'ZZCR1', OBJPROP_COLOR, clrAqua)
    ObjectSetInteger(0, 'ZZCR1', OBJPROP_WIDTH, 2)
    ObjectSetInteger(0, 'ZZCR1', OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, 'ZZCR1', OBJPROP_BACK, False)
    ObjectSetInteger(0, 'ZZCR1', OBJPROP_RAY_RIGHT, True)

def SetHighZZ(price_1, price_2, time_1, time_2):
    ObjectDelete(0, 'ZZCR2')
    ObjectCreate(0, 'ZZCR2', OBJ_TREND, 0, time_2, price_2, time_1, price_1)
    ObjectSetInteger(0, 'ZZCR2', OBJPROP_COLOR, clrKhaki)
    ObjectSetInteger(0, 'ZZCR2', OBJPROP_WIDTH, 2)
    ObjectSetInteger(0, 'ZZCR2', OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, 'ZZCR2', OBJPROP_BACK, False)
    ObjectSetInteger(0, 'ZZCR2', OBJPROP_RAY_RIGHT, True)

def TFMigrate(tf):
    _sw2 = tf
    if _sw2 == 0:
        return PERIOD_CURRENT
    elif _sw2 == 1:
        return PERIOD_M1
    elif _sw2 == 5:
        return PERIOD_M5
    elif _sw2 == 15:
        return PERIOD_M15
    elif _sw2 == 30:
        return PERIOD_M30
    elif _sw2 == 60:
        return PERIOD_H1
    elif _sw2 == 240:
        return PERIOD_H4
    elif _sw2 == 1440:
        return PERIOD_D1
    elif _sw2 == 10080:
        return PERIOD_W1
    elif _sw2 == 43200:
        return PERIOD_MN1
    elif _sw2 == 2:
        return PERIOD_M2
    elif _sw2 == 3:
        return PERIOD_M3
    elif _sw2 == 4:
        return PERIOD_M4
    elif _sw2 == 6:
        return PERIOD_M6
    elif _sw2 == 10:
        return PERIOD_M10
    elif _sw2 == 12:
        return PERIOD_M12
    elif _sw2 == 16385:
        return PERIOD_H1
    elif _sw2 == 16386:
        return PERIOD_H2
    elif _sw2 == 16387:
        return PERIOD_H3
    elif _sw2 == 16388:
        return PERIOD_H4
    elif _sw2 == 16390:
        return PERIOD_H6
    elif _sw2 == 16392:
        return PERIOD_H8
    elif _sw2 == 16396:
        return PERIOD_H12
    elif _sw2 == 16408:
        return PERIOD_D1
    elif _sw2 == 32769:
        return PERIOD_W1
    elif _sw2 == 49153:
        return PERIOD_MN1
    else:
        return PERIOD_CURRENT


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigZag2Line(_MQL5Indicator):
    name = 'ZigZag_2_Line'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
        'ObjLineDel': True,
    }

