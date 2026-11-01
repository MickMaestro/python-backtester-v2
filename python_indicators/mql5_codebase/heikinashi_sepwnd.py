"""heikinashi_sepwnd — converted from MQL5: MQL5 Indicators/HeikinAshi_SepWnd/heikinashi_sepwnd.mq5

The Heikin Ashi indicator in the sub-window
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16748574, 255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Heikin Ashi Open;Heikin Ashi High;Heikin Ashi Low;Heikin Ashi Close'}, 'levels': [], 'description': ['The Heikin Ashi indicator in the sub-window'], 'name': 'heikinashi_sepwnd', 'source': 'MQL5 Indicators/HeikinAshi_SepWnd/heikinashi_sepwnd.mq5', 'folder': 'HeikinAshi_SepWnd', 'inputs': [{'mql': 'InpHaPeriod', 'py': 'InpHaPeriod', 'param': 'InpHaPeriod', 'type': 'int', 'default': 1, 'label': 'Heikin Ashi period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpHaPeriod = _input('InpHaPeriod', 1)  # Heikin Ashi period
HaOpenBuffer = Arr(0, 0.0)
HaHighBuffer = Arr(0, 0.0)
HaLowBuffer = Arr(0, 0.0)
HaCloseBuffer = Arr(0, 0.0)
HaColors = Arr(0, 0.0)
minRequiredBars = 0

def OnInit():
    global minRequiredBars
    minRequiredBars = InpHaPeriod
    SetIndexBuffer(0, HaOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HaHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, HaLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, HaCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, HaColors, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, minRequiredBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, STYLE_SOLID)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Heikin Ashi (' + _str(InpHaPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    startBar = 0
    haOpen = 0.0
    haHigh = 0.0
    haLow = 0.0
    haClose = 0.0
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
    else:
        startBar = prev_calculated - 1
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
            HaColors[bar] = 0.0
        else:
            HaColors[bar] = 1.0
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, close[rates_total - 1])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HeikinashiSepwnd(_MQL5Indicator):
    name = 'heikinashi_sepwnd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpHaPeriod': 1,  # Heikin Ashi period
    }

