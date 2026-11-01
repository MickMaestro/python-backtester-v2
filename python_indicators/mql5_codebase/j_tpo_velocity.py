"""j_tpo_velocity — converted from MQL5: MQL5 Indicators/J_TPO_Velocity/j_tpo_velocity.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 65280, 16711680, 255, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'j_tpo_velocity', 'source': 'MQL5 Indicators/J_TPO_Velocity/j_tpo_velocity.mq5', 'folder': 'J_TPO_Velocity', 'inputs': [{'mql': 'Len_', 'py': 'Len_', 'param': 'Len_', 'type': 'int', 'default': 14, 'label': 'Smoothing period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Len_ = _input('Len_', 14)  # Smoothing period
ExtBuffer = Arr(0, 0.0)
ColorExtBuffer = Arr(0, 0.0)
Len = 0
normalization = 0.0
Lenp1half = 0.0
arr1 = Arr(0, 0.0)
arr2 = Arr(0, 0.0)
arr3 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global Len, Lenp1half, min_rates_total, normalization
    Len = Len_
    if Len < 3:
        Len = 3
    normalization = _fdiv(12.0, Len * (Len - 1) * (Len + 1))
    Lenp1half = (Len + 1) * 0.5
    min_rates_total = (2 * Len) + 1
    size = Len + 2
    if ArrayResize(arr1, size) < size:
        Print('Failed to distribute the memory for arr1[] array')
        return -1
    if ArrayResize(arr2, size) < size:
        Print('Failed to distribute the memory for arr2[] array')
        return -1
    if ArrayResize(arr3, size) < size:
        Print('Failed to distribute the memory for arr3[] array')
        return -1
    ArrayInitialize(arr1, 0)
    ArrayInitialize(arr2, 0)
    ArrayInitialize(arr3, 0)
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, ColorExtBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    ArraySetAsSeries(ExtBuffer, True)
    ArraySetAsSeries(ColorExtBuffer, True)
    return 0

def Range(period, High, Low, shift):
    H = High[ArrayMaximum(High, shift, period)]
    L = Low[ArrayMinimum(Low, shift, period)]
    return _fdiv(H - L, Point())

def J_TPO_value(period, Array, shift):
    value = 0.0
    accum = 0.0
    tmp = 0.0
    maxval = 0.0
    j = 0
    maxloc = 0
    m = 0
    flag = False
    accum = 0.0
    m = 1
    for m in range(m, period + 1):
        arr2[m] = m
        arr3[m] = m
        arr1[m] = Array[shift + period - m]
    else:
        m = _range_end(m, period + 1, 1)
    m = 1
    for m in range(m, period):
        maxval = arr1[m]
        maxloc = m
        j = m + 1
        for j in range(j, period + 1):
            if arr1[j] < maxval:
                maxval = arr1[j]
                maxloc = j
        else:
            j = _range_end(j, period + 1, 1)
        tmp = arr1[m]
        arr1[m] = arr1[maxloc]
        arr1[maxloc] = tmp
        tmp = arr2[m]
        arr2[m] = arr2[maxloc]
        arr2[maxloc] = tmp
    else:
        m = _range_end(m, period, 1)
    m = 1
    while m < Len:
        j = m + 1
        flag = True
        accum = arr3[m]
        while flag:
            if arr1[m] != arr1[j]:
                if (j - m) > 1:
                    accum = _fdiv(accum, j - m)
                    for n in range(m, j - 1 + 1):
                        arr3[n] = accum
                flag = False
            else:
                accum += arr3[j]
                j += 1
        m = j
    accum = 0.0
    m = 1
    while m <= period:
        accum += (arr3[m] - Lenp1half) * (arr2[m] - Lenp1half)
        m += 1
    value = normalization * accum
    return value

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit1 = 0
    limit2 = 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit1 = rates_total - min_rates_total - 1
        limit2 = limit1 - 1
    else:
        limit1 = rates_total - prev_calculated
        limit2 = limit1
    for bar in range(limit1, 0 - 1, -1):
        ExtBuffer[bar] = _fdiv(J_TPO_value(Len, close, bar) * Range(Len, high, low, bar), Len)
    for bar in range(limit2, 0 - 1, -1):
        ColorExtBuffer[bar] = 0.0
        if ExtBuffer[bar] > 0:
            if ExtBuffer[bar] > ExtBuffer[bar + 1]:
                ColorExtBuffer[bar] = 1.0
            if ExtBuffer[bar] < ExtBuffer[bar + 1]:
                ColorExtBuffer[bar] = 2.0
        if ExtBuffer[bar] < 0:
            if ExtBuffer[bar] < ExtBuffer[bar + 1]:
                ColorExtBuffer[bar] = 3.0
            if ExtBuffer[bar] > ExtBuffer[bar + 1]:
                ColorExtBuffer[bar] = 4.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JTpoVelocity(_MQL5Indicator):
    name = 'j_tpo_velocity'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Len_': 14,  # Smoothing period
    }

