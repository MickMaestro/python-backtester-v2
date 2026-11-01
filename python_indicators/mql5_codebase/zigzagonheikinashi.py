"""zigzagonheikinashi — converted from MQL5: MQL5 Indicators/ZigZag On Heikin Ashi/zigzagonheikinashi.mq5

ZigZag on Heikin Ashi.
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 2}, 'types': {1: 13, 2: 17}, 'colors': {1: [9639167, 13458026], 2: [4678655, 16748574]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'ZigZag Lowest;ZigZag Highest', 2: 'Heikin Ashi Open;Heikin Ashi High;Heikin Ashi Low;Heikin Ashi Close'}, 'levels': [], 'description': ['ZigZag on Heikin Ashi.'], 'name': 'zigzagonheikinashi', 'source': 'MQL5 Indicators/ZigZag On Heikin Ashi/zigzagonheikinashi.mq5', 'folder': 'ZigZag On Heikin Ashi', 'inputs': [{'mql': 'InpHaPeriod', 'py': 'InpHaPeriod', 'param': 'InpHaPeriod', 'type': 'int', 'default': 1, 'label': 'Heikin Ashi period', 'sinput': False}, {'mql': 'InpShowHekinAshi', 'py': 'InpShowHekinAshi', 'param': 'InpShowHekinAshi', 'type': 'bool', 'default': False, 'label': 'Show Heikin Ashi', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpHaPeriod = _input('InpHaPeriod', 1)  # Heikin Ashi period
InpShowHekinAshi = _input('InpShowHekinAshi', False)  # Show Heikin Ashi
HaOpenBuffer = Arr(0, 0.0)
HaHighBuffer = Arr(0, 0.0)
HaLowBuffer = Arr(0, 0.0)
HaCloseBuffer = Arr(0, 0.0)
HaColors = Arr(0, 0.0)
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
ZigZagColors = Arr(0, 0.0)
minRequiredBars = 0

def OnInit():
    global minRequiredBars
    minRequiredBars = InpHaPeriod
    SetIndexBuffer(0, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighestBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ZigZagColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, HaOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, HaHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, HaLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, HaCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, HaColors, INDICATOR_COLOR_INDEX)
    for i in range(0, 2):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, minRequiredBars)
        PlotIndexSetInteger(i, PLOT_SHIFT, 0)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0.0)
    if not InpShowHekinAshi:
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_NONE)
    else:
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_COLOR_CANDLES)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'ZigZag On Heikin Ashi (' + _str(InpHaPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate__highValue, _s_OnCalculate__lastHighPos, _s_OnCalculate__lastLowPos, _s_OnCalculate__lowValue, _s_OnCalculate__up
    startBar = 0
    haOpen = 0.0
    haHigh = 0.0
    haLow = 0.0
    haClose = 0.0
    lastHighPos = 0
    lastLowPos = 0
    highValue = 0.0
    lowValue = 0.0
    up = False
    if rates_total < minRequiredBars:
        Print('Not enough data to calculate')
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        startBar = minRequiredBars
        for bar in range(0, startBar):
            HaOpenBuffer[bar] = open[bar]
            HaHighBuffer[bar] = high[bar]
            HaLowBuffer[bar] = low[bar]
            HaCloseBuffer[bar] = close[bar]
        if close[startBar - 1] >= close[startBar - 1]:
            _s_OnCalculate__up = True
            _s_OnCalculate__highValue = high[startBar - 1]
            _s_OnCalculate__lowValue = low[startBar - 1]
            _s_OnCalculate__lastLowPos = startBar - 1
            _s_OnCalculate__lastHighPos = _s_OnCalculate__lastLowPos
    else:
        startBar = prev_calculated - 1
    up = _s_OnCalculate__up
    highValue = _s_OnCalculate__highValue
    lowValue = _s_OnCalculate__lowValue
    lastHighPos = _s_OnCalculate__lastHighPos
    lastLowPos = _s_OnCalculate__lastLowPos
    for bar in range(startBar, rates_total):
        haOpen = (HaOpenBuffer[bar - InpHaPeriod] + HaCloseBuffer[bar - InpHaPeriod]) / 2
        haClose = (open[bar] + high[bar] + low[bar] + close[bar]) / 4
        haHigh = MathMax(high[bar], MathMax(haOpen, haClose))
        haLow = MathMin(low[bar], MathMin(haOpen, haClose))
        if InpHaPeriod > 1:
            haOpen = (MathMax(haOpen, HaOpenBuffer[bar - 1]) if (haClose > haOpen) else MathMin(haOpen, HaOpenBuffer[bar - 1]))
        HaOpenBuffer[bar] = haOpen
        HaHighBuffer[bar] = haHigh
        HaLowBuffer[bar] = haLow
        HaCloseBuffer[bar] = haClose
        if haClose > haOpen:
            HaColors[bar] = 1.0
        else:
            HaColors[bar] = 0.0
        if rates_total != prev_calculated and bar == (rates_total - 1):
            _s_OnCalculate__up = up
            _s_OnCalculate__highValue = highValue
            _s_OnCalculate__lowValue = lowValue
            _s_OnCalculate__lastHighPos = lastHighPos
            _s_OnCalculate__lastLowPos = lastLowPos
        if up:
            ZigZagColors[bar] = 1.0
            if high[bar] > highValue:
                HighestBuffer[lastHighPos] = 0.0
                highValue = high[bar]
                HighestBuffer[bar] = highValue
                lastHighPos = bar
                LowestBuffer[bar] = 0.0
            elif haClose <= haOpen:
                up = False
                lowValue = low[bar]
                LowestBuffer[bar] = lowValue
                lastLowPos = bar
                HighestBuffer[bar] = 0.0
                ZigZagColors[bar] = 0.0
            else:
                HighestBuffer[bar] = 0.0
                LowestBuffer[bar] = 0.0
        else:
            ZigZagColors[bar] = 0.0
            if low[bar] < lowValue:
                LowestBuffer[lastLowPos] = 0.0
                lowValue = low[bar]
                LowestBuffer[bar] = lowValue
                lastLowPos = bar
                HighestBuffer[bar] = 0.0
            elif haClose > haOpen:
                up = True
                highValue = high[bar]
                HighestBuffer[bar] = highValue
                lastHighPos = bar
                LowestBuffer[bar] = 0.0
                ZigZagColors[bar] = 1.0
            else:
                HighestBuffer[bar] = 0.0
                LowestBuffer[bar] = 0.0
    return rates_total

# ---- static local variables
_s_OnCalculate__lastHighPos = 0
_s_OnCalculate__lastLowPos = 0
_s_OnCalculate__highValue = 0.0
_s_OnCalculate__lowValue = 0.0
_s_OnCalculate__up = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Zigzagonheikinashi(_MQL5Indicator):
    name = 'zigzagonheikinashi'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpHaPeriod': 1,  # Heikin Ashi period
        'InpShowHekinAshi': False,  # Show Heikin Ashi
    }

