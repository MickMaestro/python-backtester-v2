"""Zigzag fibo oscillator — converted from MQL5: MQL5 Indicators/Zigzag fibo oscillator/Zigzag fibo oscillator.mq5

Copyright: Copyright 2000-2025, MetaQuotes Ltd. // advancements by phade 2025; Link: https://www.mql5.com; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2000-2025, MetaQuotes Ltd. // advancements by phade 2025', 'link': 'https://www.mql5.com', 'version': '1.02', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 2}, 'types': {1: 13, 2: 17}, 'colors': {1: [16748574, 255, 8421504], 2: [16748574, 255, 8421504]}, 'widths': {1: 2, 2: 1}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Zigzag fibo oscillator', 'source': 'MQL5 Indicators/Zigzag fibo oscillator/Zigzag fibo oscillator.mq5', 'folder': 'Zigzag fibo oscillator', 'inputs': [{'mql': 'InpDepth', 'py': 'InpDepth', 'param': 'InpDepth', 'type': 'int', 'default': 12, 'label': 'Depth', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'int', 'default': 5, 'label': 'Deviation', 'sinput': False}, {'mql': 'InpBackstep', 'py': 'InpBackstep', 'param': 'InpBackstep', 'type': 'int', 'default': 3, 'label': 'Back Step', 'sinput': False}, {'mql': 'zzStyle', 'py': 'zzStyle', 'param': 'zzStyle', 'type': 'int', 'default': 1, 'label': 'Type of ZigZag', 'sinput': False}, {'mql': 'useFibLevels', 'py': 'useFibLevels', 'param': 'useFibLevels', 'type': 'bool', 'default': True, 'label': 'Fibonacci Retracement Levels', 'sinput': False}, {'mql': 'trackCurrentBar', 'py': 'trackCurrentBar', 'param': 'trackCurrentBar', 'type': 'bool', 'default': True, 'label': 'Track current price', 'sinput': False}, {'mql': 'priceType', 'py': 'priceType', 'param': 'priceType', 'type': 'int', 'default': 0, 'label': 'Current price tracking', 'sinput': False}, {'mql': 'vol', 'py': 'vol', 'param': 'vol', 'type': 'long', 'default': 60, 'label': 'Volume threshold (for unconfirmed leg color)', 'sinput': False}, {'mql': 'scaling_offset', 'py': 'scaling_offset', 'param': 'scaling_offset', 'type': 'double', 'default': 0.2, 'label': 'Window scaling offset', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum EnZigZagStyle
Oscillator = 0
HighLow = 1
_enum('EnZigZagStyle', {0: 'Oscillator', 1: 'HighLow'})

# enum EnPriceType
PR_OPEN = 0
PR_CLOSE = 1
PR_HIGH = 2
PR_LOW = 3
PR_WEIGHTED = 4
PR_TYPICAL = 5
_enum('EnPriceType', {0: 'PR_OPEN', 1: 'PR_CLOSE', 2: 'PR_HIGH', 3: 'PR_LOW', 4: 'PR_WEIGHTED', 5: 'PR_TYPICAL'})

# enum EnSearchMode
Extremum = 0
Peak = 1
Bottom = -1
_enum('EnSearchMode', {0: 'Extremum', 1: 'Peak', -1: 'Bottom'})

# ---- inputs and global variables
InpDepth = _input('InpDepth', 12)  # Depth
InpDeviation = _input('InpDeviation', 5)  # Deviation
InpBackstep = _input('InpBackstep', 3)  # Back Step
zzStyle = _input('zzStyle', HighLow)  # Type of ZigZag
useFibLevels = _input('useFibLevels', True)  # Fibonacci Retracement Levels
trackCurrentBar = _input('trackCurrentBar', True)  # Track current price
priceType = _input('priceType', PR_OPEN)  # Current price tracking
vol = _input('vol', 60)  # Volume threshold (for unconfirmed leg color)
scaling_offset = _input('scaling_offset', 0.2)  # Window scaling offset
ZigzagPeakBuffer = Arr(0, 0.0)
ZigzagBottomBuffer = Arr(0, 0.0)
HighMapBuffer = Arr(0, 0.0)
LowMapBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
opens = Arr(0, 0.0)
closes = Arr(0, 0.0)
highs = Arr(0, 0.0)
lows = Arr(0, 0.0)
candleColor = Arr(0, 0.0)
ExtRecalc = 3  # recounting's depth

def OnInit():
    SetIndexBuffer(0, ZigzagPeakBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ZigzagBottomBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, opens, INDICATOR_DATA)
    SetIndexBuffer(4, closes, INDICATOR_DATA)
    SetIndexBuffer(5, highs, INDICATOR_DATA)
    SetIndexBuffer(6, lows, INDICATOR_DATA)
    SetIndexBuffer(7, candleColor, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, HighMapBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, LowMapBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = StringFormat('ZigZag Oscillator (%d,%d,%d)', InpDepth, InpDeviation, InpBackstep)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    if useFibLevels and zzStyle == HighLow:
        IndicatorSetInteger(INDICATOR_LEVELS, 7)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrGray)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrGray)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrGray)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 4, clrGray)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 5, clrGray)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 6, clrGray)
    elif zzStyle == Oscillator:
        IndicatorSetInteger(INDICATOR_LEVELS, 0)
    if not useFibLevels:
        IndicatorSetInteger(INDICATOR_LEVELS, 0)
    ChartNavigate(0, CHART_END)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = ((prev_calculated - 1) if (prev_calculated > 0) else 1)
    if zzStyle == HighLow:
        for i in range(start, rates_total - 1):
            opens[i] = open[i]
            closes[i] = close[i]
            highs[i] = high[i]
            lows[i] = low[i]
            if open[i] < close[i]:
                candleColor[i] = 0.0
            elif open[i] > close[i]:
                candleColor[i] = 1.0
            else:
                candleColor[i] = 2.0
        for i in range(rates_total - 50, 0 - 1, -1):
            opens[i] = EMPTY_VALUE
            closes[i] = EMPTY_VALUE
            highs[i] = EMPTY_VALUE
            lows[i] = EMPTY_VALUE
    else:
        for i in range(0, rates_total):
            opens[i] = EMPTY_VALUE
            closes[i] = EMPTY_VALUE
            highs[i] = EMPTY_VALUE
            lows[i] = EMPTY_VALUE
    zigzag(rates_total, prev_calculated, open, low, high, close)
    return rates_total

def zigzag(rates_total, prev_calculated, open, low, high, close):
    global _s_zigzag_bufMax, _s_zigzag_bufMin, _s_zigzag_legEnd, _s_zigzag_legStart
    if rates_total < 100:
        return 0
    i = 0
    start = 0
    extreme_counter = 0
    extreme_search = Extremum
    shift = 0
    back = 0
    last_high_pos = 0
    last_low_pos = 0
    val = 0.0
    res = 0.0
    cur_low = 0.0
    cur_high = 0.0
    last_high = 0.0
    last_low = 0.0
    if prev_calculated == 0:
        ArrayInitialize(ZigzagPeakBuffer, 0.0)
        ArrayInitialize(ZigzagBottomBuffer, 0.0)
        ArrayInitialize(HighMapBuffer, 0.0)
        ArrayInitialize(LowMapBuffer, 0.0)
        start = InpDepth - 1
    if prev_calculated > 0:
        i = rates_total - 1
        while extreme_counter < ExtRecalc and i > (rates_total - 100):
            res = ZigzagPeakBuffer[i] + ZigzagBottomBuffer[i]
            if res != 0:
                extreme_counter += 1
            i -= 1
        i += 1
        start = i
        if LowMapBuffer[i] != 0:
            cur_low = LowMapBuffer[i]
            extreme_search = Peak
        else:
            cur_high = HighMapBuffer[i]
            extreme_search = Bottom
        i = start + 1
        for i in range(i, rates_total):
            ZigzagPeakBuffer[i] = 0.0
            ZigzagBottomBuffer[i] = 0.0
            LowMapBuffer[i] = 0.0
            HighMapBuffer[i] = 0.0
        else:
            i = _range_end(i, rates_total, 1)
    shift = start
    for shift in range(shift, rates_total):
        val = Lowest(low, InpDepth, shift)
        if val == last_low:
            val = 0.0
        else:
            last_low = val
            if (low[shift] - val) > (InpDeviation * Point()):
                val = 0.0
            else:
                back = InpBackstep
                for back in range(back, 1 - 1, -1):
                    res = LowMapBuffer[shift - back]
                    if res != 0 and res > val:
                        LowMapBuffer[shift - back] = 0.0
                else:
                    back = _range_end(back, 1 - 1, -1)
        if low[shift] == val:
            LowMapBuffer[shift] = val
        else:
            LowMapBuffer[shift] = 0.0
        val = Highest(high, InpDepth, shift)
        if val == last_high:
            val = 0.0
        else:
            last_high = val
            if (val - high[shift]) > (InpDeviation * Point()):
                val = 0.0
            else:
                back = InpBackstep
                for back in range(back, 1 - 1, -1):
                    res = HighMapBuffer[shift - back]
                    if res != 0 and res < val:
                        HighMapBuffer[shift - back] = 0.0
                else:
                    back = _range_end(back, 1 - 1, -1)
        if high[shift] == val:
            HighMapBuffer[shift] = val
        else:
            HighMapBuffer[shift] = 0.0
    else:
        shift = _range_end(shift, rates_total, 1)
    if extreme_search == 0:
        last_low = 0.0
        last_high = 0.0
    else:
        last_low = cur_low
        last_high = cur_high
    range_ = 0.0
    adaptiveScalingOffset = (ChartGetDouble(0, CHART_PRICE_MAX, 1) - ChartGetDouble(0, CHART_PRICE_MIN, 1)) * scaling_offset
    price_range = 0.0
    normalized_high = 0.0
    normalized_low = 0.0
    shift = start
    for shift in range(shift, rates_total):
        res = 0.0
        if _s_zigzag_bufMax < ZigzagPeakBuffer[shift]:
            _s_zigzag_bufMax = ZigzagPeakBuffer[shift]
        if _s_zigzag_bufMin > ZigzagBottomBuffer[shift]:
            _s_zigzag_bufMin = ZigzagBottomBuffer[shift]
        if zzStyle == HighLow:
            if extreme_search == Peak:
                if (LowMapBuffer[shift] != 0.0 and LowMapBuffer[shift] < last_low) and HighMapBuffer[shift] == 0.0:
                    _s_zigzag_legStart = last_high
                    _s_zigzag_legEnd = LowMapBuffer[shift]
                    if useFibLevels:
                        CalculateBullFibLevels(_s_zigzag_legStart, _s_zigzag_legEnd)
                    maxLevel = _s_zigzag_legStart + adaptiveScalingOffset
                    minLevel = _s_zigzag_legEnd - adaptiveScalingOffset
                    IndicatorSetDouble(INDICATOR_MAXIMUM, MathMax(maxLevel, _s_zigzag_legStart))
                    IndicatorSetDouble(INDICATOR_MINIMUM, MathMin(minLevel, _s_zigzag_legEnd))
                if HighMapBuffer[shift] != 0.0 and LowMapBuffer[shift] == 0.0:
                    _s_zigzag_legStart = last_low
                    _s_zigzag_legEnd = HighMapBuffer[shift]
                    if useFibLevels:
                        CalculateBearFibLevels(_s_zigzag_legStart, _s_zigzag_legEnd)
                    maxLevel = _s_zigzag_legEnd + adaptiveScalingOffset
                    minLevel = _s_zigzag_legStart - adaptiveScalingOffset
                    IndicatorSetDouble(INDICATOR_MAXIMUM, MathMax(maxLevel, _s_zigzag_legEnd))
                    IndicatorSetDouble(INDICATOR_MINIMUM, MathMin(minLevel, _s_zigzag_legStart))
            elif extreme_search == Bottom:
                if (HighMapBuffer[shift] != 0.0 and HighMapBuffer[shift] > last_high) and LowMapBuffer[shift] == 0.0:
                    _s_zigzag_legStart = last_low
                    _s_zigzag_legEnd = HighMapBuffer[shift]
                    if useFibLevels:
                        CalculateBearFibLevels(_s_zigzag_legStart, _s_zigzag_legEnd)
                    maxLevel = _s_zigzag_legEnd + adaptiveScalingOffset
                    minLevel = _s_zigzag_legStart - adaptiveScalingOffset
                    IndicatorSetDouble(INDICATOR_MAXIMUM, MathMax(maxLevel, _s_zigzag_legEnd))
                    IndicatorSetDouble(INDICATOR_MINIMUM, MathMin(minLevel, _s_zigzag_legStart))
                if LowMapBuffer[shift] != 0.0 and HighMapBuffer[shift] == 0.0:
                    _s_zigzag_legStart = last_high
                    _s_zigzag_legEnd = LowMapBuffer[shift]
                    if useFibLevels:
                        CalculateBullFibLevels(_s_zigzag_legStart, _s_zigzag_legEnd)
                    maxLevel = _s_zigzag_legStart + adaptiveScalingOffset
                    minLevel = _s_zigzag_legEnd - adaptiveScalingOffset
                    IndicatorSetDouble(INDICATOR_MAXIMUM, MathMax(maxLevel, _s_zigzag_legStart))
                    IndicatorSetDouble(INDICATOR_MINIMUM, MathMin(minLevel, _s_zigzag_legEnd))
        _sw1 = extreme_search
        if _sw1 == Extremum:
            if last_low == 0 and last_high == 0:
                if HighMapBuffer[shift] != 0:
                    last_high = high[shift]
                    last_high_pos = shift
                    extreme_search = -1
                    ColorBuffer[shift] = 0.0
                    res = 1.0
                if LowMapBuffer[shift] != 0:
                    last_low = low[shift]
                    last_low_pos = shift
                    extreme_search = 1
                    ColorBuffer[shift] = 1.0
                    res = 1.0
        elif _sw1 == Peak:
            if (LowMapBuffer[shift] != 0.0 and LowMapBuffer[shift] < last_low) and HighMapBuffer[shift] == 0.0:
                ZigzagBottomBuffer[last_low_pos] = 0.0
                last_low_pos = shift
                last_low = LowMapBuffer[shift]
                if zzStyle == Oscillator:
                    ZigzagBottomBuffer[shift] = Point()
                if zzStyle == HighLow:
                    ZigzagBottomBuffer[shift] = last_low
                ColorBuffer[shift] = 1.0
                res = 1.0
            if HighMapBuffer[shift] != 0.0 and LowMapBuffer[shift] == 0.0:
                last_high = HighMapBuffer[shift]
                last_high_pos = shift
                price_range = HighMapBuffer[shift] - LowMapBuffer[shift - 1]
                normalized_high = _fdiv(HighMapBuffer[shift] - LowMapBuffer[shift - 1], price_range)
                if zzStyle == Oscillator:
                    ZigzagPeakBuffer[shift] = normalized_high
                if zzStyle == HighLow:
                    ZigzagPeakBuffer[shift] = last_high
                ColorBuffer[shift] = 0.0
                extreme_search = Bottom
                res = 1.0
        elif _sw1 == Bottom:
            if (HighMapBuffer[shift] != 0.0 and HighMapBuffer[shift] > last_high) and LowMapBuffer[shift] == 0.0:
                ZigzagPeakBuffer[last_high_pos] = 0.0
                last_high_pos = shift
                last_high = HighMapBuffer[shift]
                price_range = HighMapBuffer[shift] - LowMapBuffer[shift - 1]
                normalized_high = _fdiv(HighMapBuffer[shift] - LowMapBuffer[shift - 1], price_range)
                if zzStyle == Oscillator:
                    ZigzagPeakBuffer[shift] = normalized_high
                if zzStyle == HighLow:
                    ZigzagPeakBuffer[shift] = last_high
                ColorBuffer[shift] = 0.0
            if LowMapBuffer[shift] != 0.0 and HighMapBuffer[shift] == 0.0:
                last_low = LowMapBuffer[shift]
                last_low_pos = shift
                if zzStyle == Oscillator:
                    ZigzagBottomBuffer[shift] = Point()
                if zzStyle == HighLow:
                    ZigzagBottomBuffer[shift] = last_low
                ColorBuffer[shift] = 1.0
                extreme_search = Peak
        else:
            return rates_total
    else:
        shift = _range_end(shift, rates_total, 1)
    current_bar_index = rates_total - 1
    if trackCurrentBar and current_bar_index != 0:
        if zzStyle == HighLow:
            ZigzagPeakBuffer[current_bar_index] = GetPrice(priceType, current_bar_index, open, high, low, close)
            ZigzagBottomBuffer[current_bar_index] = GetPrice(priceType, current_bar_index, open, high, low, close)
        if zzStyle == Oscillator:
            pr_range = MathAbs(high[current_bar_index] - low[current_bar_index])
            normalized_range = _fdiv(high[current_bar_index] - MathMin(low[current_bar_index], high[current_bar_index]), pr_range)
            ZigzagPeakBuffer[current_bar_index] = normalized_range
            ZigzagBottomBuffer[current_bar_index] = normalized_range
        currentVolume = iVolume(Symbol(), 0, 0)
        volumeThreshold = vol
        shift = start
        for shift in range(shift, rates_total):
            if shift == (rates_total - 1):
                if extreme_search == Peak and close[shift] < open[shift]:
                    ColorBuffer[shift] = 2.0
                elif extreme_search == Bottom and close[shift] > open[shift]:
                    ColorBuffer[shift] = 2.0
                if close[shift] > open[shift] and currentVolume >= volumeThreshold:
                    ColorBuffer[shift] = 0.0
                elif close[shift] < open[shift] and currentVolume >= volumeThreshold:
                    ColorBuffer[shift] = 1.0
        else:
            shift = _range_end(shift, rates_total, 1)
    if zzStyle == Oscillator:
        IndicatorSetDouble(INDICATOR_MINIMUM, Point() - adaptiveScalingOffset)
        IndicatorSetDouble(INDICATOR_MAXIMUM, 1.0 + adaptiveScalingOffset)
    return rates_total

def GetPrice(type_, barIndex, open, high, low, close):
    _sw2 = type_
    if _sw2 == PR_OPEN:
        return open[barIndex]
    elif _sw2 == PR_CLOSE:
        return close[barIndex]
    elif _sw2 == PR_HIGH:
        return high[barIndex]
    elif _sw2 == PR_LOW:
        return low[barIndex]
    elif _sw2 == PR_WEIGHTED:
        return (high[barIndex] + low[barIndex] + (close[barIndex] * 2.0)) / 4.0
    elif _sw2 == PR_TYPICAL:
        return (high[barIndex] + low[barIndex] + close[barIndex]) / 3.0
    else:
        return 0.0

def Highest(array, count, start):
    res = array[start]
    i = start - 1
    while i > (start - count) and i >= 0:
        if res < array[i]:
            res = array[i]
        i -= 1
    return res

def Lowest(array, count, start):
    res = array[start]
    i = start - 1
    while i > (start - count) and i >= 0:
        if res > array[i]:
            res = array[i]
        i -= 1
    return res

def CalculateBearFibLevels(start, end):
    range_ = MathAbs(end - start)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, start)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, start + (0.236 * range_))
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, start + (0.382 * range_))
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, start + (0.5 * range_))
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, start + (0.618 * range_))
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 5, start + (0.764 * range_))
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 6, end)

def CalculateBullFibLevels(start, end):
    range_ = MathAbs(start - end)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, end)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, end + (0.236 * range_))
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, end + (0.382 * range_))
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, end + (0.5 * range_))
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, end + (0.618 * range_))
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 5, end + (0.764 * range_))
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 6, start)

# ---- static local variables
_s_zigzag_bufMax = -DBL_MAX
_s_zigzag_bufMin = DBL_MAX
_s_zigzag_legStart = 0.0
_s_zigzag_legEnd = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigzagFiboOscillator(_MQL5Indicator):
    name = 'Zigzag fibo oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpDepth': 12,  # Depth
        'InpDeviation': 5,  # Deviation
        'InpBackstep': 3,  # Back Step
        'zzStyle': _Choice({0: 'Oscillator', 1: 'HighLow'}, default=1),  # Type of ZigZag
        'useFibLevels': True,  # Fibonacci Retracement Levels
        'trackCurrentBar': True,  # Track current price
        'priceType': _Choice({0: 'Open', 1: 'Close', 2: 'High', 3: 'Low', 4: 'Weighted', 5: 'Typical'}, default=0),  # Current price tracking
        'vol': 60,  # Volume threshold (for unconfirmed leg color)
        'scaling_offset': 0.2,  # Window scaling offset
    }

