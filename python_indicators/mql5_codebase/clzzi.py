"""clzzi — converted from MQL5: MQL5 Indicators/Nonparametric Zig Zag, A-la Clyde Lee Patterns/clzzi.mq5

Zig Zag indicator bases on a-la Clyde Lee 4-point patterns.
Uptrend monotonicity condition starts with simultaneous 
appearence of bullish patterns for highs and lows.
Similar logic applies for downtrend.
Copyright: Copyright 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 11}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 2}, 'colors': {1: [255], 2: [255], 3: [255], 4: [255], 5: [255], 6: [16711680], 7: [16711680], 8: [16711680], 9: [16711680], 10: [16711680], 11: [16777215]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}, 'labels': {1: 'P0', 2: 'P1', 3: 'P2', 4: 'P3', 5: 'P4', 6: 'P5', 7: 'P6', 8: 'P7', 9: 'P8', 10: 'P9', 11: 'ZigZagLine'}, 'levels': [], 'description': ['Zig Zag indicator bases on a-la Clyde Lee 4-point patterns.', 'Uptrend monotonicity condition starts with simultaneous ', 'appearence of bullish patterns for highs and lows.', 'Similar logic applies for downtrend.'], 'name': 'clzzi', 'source': 'MQL5 Indicators/Nonparametric Zig Zag, A-la Clyde Lee Patterns/clzzi.mq5', 'folder': 'Nonparametric Zig Zag, A-la Clyde Lee Patterns', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
P0 = Arr(0, 0.0)
P1 = Arr(0, 0.0)
P2 = Arr(0, 0.0)
P3 = Arr(0, 0.0)
P4 = Arr(0, 0.0)
P5 = Arr(0, 0.0)
P6 = Arr(0, 0.0)
P7 = Arr(0, 0.0)
P8 = Arr(0, 0.0)
P9 = Arr(0, 0.0)
PT = Arr(0, 0.0)
ZigZagLineBuffer = Arr(0, 0.0)
lastz = 0
patterns = Arr.of([0, 5, -1, 7, 1, -1, -1, 8, 3, -1, -1, 6, 2, -1, 4, 9], fill=0, dyn=False, size=16)

def OnInit():
    SetIndexBuffer(0, P0, INDICATOR_DATA)
    SetIndexBuffer(1, P1, INDICATOR_DATA)
    SetIndexBuffer(2, P2, INDICATOR_DATA)
    SetIndexBuffer(3, P3, INDICATOR_DATA)
    SetIndexBuffer(4, P4, INDICATOR_DATA)
    SetIndexBuffer(5, P5, INDICATOR_DATA)
    SetIndexBuffer(6, P6, INDICATOR_DATA)
    SetIndexBuffer(7, P7, INDICATOR_DATA)
    SetIndexBuffer(8, P8, INDICATOR_DATA)
    SetIndexBuffer(9, P9, INDICATOR_DATA)
    SetIndexBuffer(10, ZigZagLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(11, PT, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_ARROW, 139)
    PlotIndexSetInteger(1, PLOT_ARROW, 140)
    PlotIndexSetInteger(2, PLOT_ARROW, 141)
    PlotIndexSetInteger(3, PLOT_ARROW, 142)
    PlotIndexSetInteger(4, PLOT_ARROW, 143)
    PlotIndexSetInteger(5, PLOT_ARROW, 144)
    PlotIndexSetInteger(6, PLOT_ARROW, 145)
    PlotIndexSetInteger(7, PLOT_ARROW, 146)
    PlotIndexSetInteger(8, PLOT_ARROW, 147)
    PlotIndexSetInteger(9, PLOT_ARROW, 148)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, 10)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, 10)
    PlotIndexSetInteger(2, PLOT_ARROW_SHIFT, 10)
    PlotIndexSetInteger(3, PLOT_ARROW_SHIFT, 10)
    PlotIndexSetInteger(4, PLOT_ARROW_SHIFT, 10)
    PlotIndexSetInteger(5, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetInteger(6, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetInteger(7, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetInteger(8, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetInteger(9, PLOT_ARROW_SHIFT, -10)
    return 0

def GetPatternNumber(rate, bar):
    D = rate[bar - 0]
    cnt = bar - 1
    while cnt > 0 and rate[bar - 0] == rate[cnt]:
        cnt -= 1
    if cnt <= 0:
        return -1
    if rate[cnt] < rate[cnt + 1]:
        while cnt > 1 and rate[cnt - 1] <= rate[cnt]:
            cnt -= 1
    else:
        while cnt > 1 and rate[cnt - 1] >= rate[cnt]:
            cnt -= 1
    if cnt <= 1:
        return -1
    C = rate[cnt]
    if rate[cnt - 1] < rate[cnt]:
        while cnt > 1 and rate[cnt - 1] <= rate[cnt]:
            cnt -= 1
    else:
        while cnt > 1 and rate[cnt - 1] >= rate[cnt]:
            cnt -= 1
    if cnt <= 1:
        return -1
    B = rate[cnt]
    if rate[cnt - 1] < rate[cnt]:
        while cnt > 1 and rate[cnt - 1] <= rate[cnt]:
            cnt -= 1
    else:
        while cnt > 1 and rate[cnt - 1] >= rate[cnt]:
            cnt -= 1
    if cnt <= 1:
        return -1
    A = rate[cnt]
    code = 0
    if B > A:
        code += 1
    if D > A:
        code += 2
    if D > B:
        code += 4
    if C > A:
        code += 8
    return patterns[code]

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global lastz
    if (rates_total - prev_calculated) == 0:
        return rates_total
    shift = 0
    trend = 0
    last_bar = rates_total - 1
    if prev_calculated == 0:
        ArrayInitialize(ZigZagLineBuffer, EMPTY_VALUE)
        ArrayInitialize(P0, EMPTY_VALUE)
        ArrayInitialize(P1, EMPTY_VALUE)
        ArrayInitialize(P2, EMPTY_VALUE)
        ArrayInitialize(P3, EMPTY_VALUE)
        ArrayInitialize(P4, EMPTY_VALUE)
        ArrayInitialize(P5, EMPTY_VALUE)
        ArrayInitialize(P6, EMPTY_VALUE)
        ArrayInitialize(P7, EMPTY_VALUE)
        ArrayInitialize(P8, EMPTY_VALUE)
        ArrayInitialize(P9, EMPTY_VALUE)
        ArrayInitialize(PT, EMPTY_VALUE)
        shift = 2
        lastz = 0
    else:
        for cnt in range(prev_calculated, rates_total):
            ZigZagLineBuffer[cnt] = EMPTY_VALUE
            P0[cnt] = EMPTY_VALUE
            P1[cnt] = EMPTY_VALUE
            P2[cnt] = EMPTY_VALUE
            P3[cnt] = EMPTY_VALUE
            P4[cnt] = EMPTY_VALUE
            P5[cnt] = EMPTY_VALUE
            P6[cnt] = EMPTY_VALUE
            P7[cnt] = EMPTY_VALUE
            P8[cnt] = EMPTY_VALUE
            P9[cnt] = EMPTY_VALUE
            PT[cnt] = EMPTY_VALUE
        shift = prev_calculated - 2
        if ZigZagLineBuffer[lastz] == 0:
            Print("WTF! lastz doesn't fit")
            lastz = prev_calculated - 1
            while lastz > 0 and ZigZagLineBuffer[lastz] == 0:
                lastz -= 1
    while (shift := shift + 1) < last_bar:
        ph = GetPatternNumber(high, shift)
        pl = GetPatternNumber(low, shift)
        _sw1 = ph
        if _sw1 in (0, 1, 2, 3, 4):
            _sw2 = pl
            if _sw2 in (0, 1, 2, 3, 4):
                trend = -1
            elif _sw2 in (5, 6, 7, 8, 9):
                trend = 0
            else:
                trend = 0
        elif _sw1 in (5, 6, 7, 8, 9):
            _sw3 = pl
            if _sw3 in (0, 1, 2, 3, 4):
                trend = 0
            elif _sw3 in (5, 6, 7, 8, 9):
                trend = 1
            else:
                trend = 0
        else:
            trend = 0
        if trend != 0:
            PT[shift] = trend
        else:
            PT[shift] = PT[shift - 1]
    shift = lastz + 1
    while shift < last_bar and (PT[shift] == PT[lastz] or PT[shift] == 0):
        shift += 1
    while shift < last_bar:
        iminlow = shift
        imaxhigh = shift
        while shift < last_bar and PT[shift] == PT[iminlow]:
            if low[iminlow] > low[shift]:
                iminlow = shift
            if high[imaxhigh] < high[shift]:
                imaxhigh = shift
            shift += 1
        if shift < last_bar:
            if PT[iminlow] == -1:
                lastz = iminlow
                ZigZagLineBuffer[lastz] = low[lastz]
            else:
                lastz = imaxhigh
                ZigZagLineBuffer[lastz] = high[lastz]
            pattern = 0
            if PT[lastz] == 1:
                pattern = GetPatternNumber(high, lastz)
            else:
                pattern = GetPatternNumber(low, lastz)
            _sw4 = pattern
            if _sw4 == 0:
                P0[lastz] = low[lastz]
            elif _sw4 == 1:
                P1[lastz] = low[lastz]
            elif _sw4 == 2:
                P2[lastz] = low[lastz]
            elif _sw4 == 3:
                P3[lastz] = low[lastz]
            elif _sw4 == 4:
                P4[lastz] = low[lastz]
            elif _sw4 == 5:
                P5[lastz] = high[lastz]
            elif _sw4 == 6:
                P6[lastz] = high[lastz]
            elif _sw4 == 7:
                P7[lastz] = high[lastz]
            elif _sw4 == 8:
                P8[lastz] = high[lastz]
            elif _sw4 == 9:
                P9[lastz] = high[lastz]
            else:
                pass
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Clzzi(_MQL5Indicator):
    name = 'clzzi'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

