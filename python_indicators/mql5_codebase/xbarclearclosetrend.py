"""xbarclearclosetrend — converted from MQL5: MQL5 Indicators/X Bar Clear Close Trend/xbarclearclosetrend.mq5

Alternative trend indicator. Trend reversal appears in the case, 
if bar closing is higher than high (lower than low) of other bars pattern.
Copyright: Copyright 2013, Rone; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, Rone', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 0, 2: 17}, 'colors': {2: [255, 16711680, 4678655, 42495, 14772545, 16760576]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Value', 2: 'XBCC Open;XBCC High;XBCC Low;XBCC Close'}, 'levels': [], 'description': ['Alternative trend indicator. Trend reversal appears in the case, ', 'if bar closing is higher than high (lower than low) of other bars pattern.'], 'name': 'xbarclearclosetrend', 'source': 'MQL5 Indicators/X Bar Clear Close Trend/xbarclearclosetrend.mq5', 'folder': 'X Bar Clear Close Trend', 'inputs': [{'mql': 'InpBarsInPattern', 'py': 'InpBarsInPattern', 'param': 'InpBarsInPattern', 'type': 'int', 'default': 5, 'label': 'Bars In Pattern', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBarsInPattern = _input('InpBarsInPattern', 5)  # Bars In Pattern
ValueBuffer = Arr(0, 0.0)
OpenXbccBuffer = Arr(0, 0.0)
HighXbccBuffer = Arr(0, 0.0)
LowXbccBuffer = Arr(0, 0.0)
CloseXbccBuffer = Arr(0, 0.0)
XbccColors = Arr(0, 0.0)
bars_in_pattern = 0
min_required_bars = 0

def IsXBarUpClearClose(current, bars, high, low, close):
    for bar in range(current - bars + 1, current):
        if high[bar] >= close[current]:
            return False
    return True

def IsXBarDownClearClose(current, bars, high, low, close):
    for bar in range(current - bars + 1, current):
        if low[bar] <= close[current]:
            return False
    return True

def OnInit():
    global bars_in_pattern, min_required_bars
    if InpBarsInPattern < 2:
        bars_in_pattern = 5
        printf('Incorrected input value for InpBarsInPattern = %d. Indicator will use value %d.', InpBarsInPattern, bars_in_pattern)
    else:
        bars_in_pattern = InpBarsInPattern
    min_required_bars = bars_in_pattern + 1
    SetIndexBuffer(0, ValueBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, OpenXbccBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, HighXbccBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, LowXbccBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, CloseXbccBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, XbccColors, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_required_bars)
    PlotIndexSetInteger(1, PLOT_SHIFT, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'XBarClearCloseTrend (' + _str(bars_in_pattern) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate__up_trend
    if rates_total < min_required_bars:
        Print('Not enough bars for calculation.')
        return 0
    start_bar = 0
    up_trend = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        start_bar = min_required_bars
        if close[start_bar] >= close[start_bar - 1]:
            _s_OnCalculate__up_trend = True
        else:
            _s_OnCalculate__up_trend = False
    else:
        start_bar = prev_calculated - 1
    up_trend = _s_OnCalculate__up_trend
    for bar in range(start_bar, rates_total):
        prev_bar = bar - 1
        OpenXbccBuffer[bar] = open[bar]
        HighXbccBuffer[bar] = high[bar]
        LowXbccBuffer[bar] = low[bar]
        CloseXbccBuffer[bar] = close[bar]
        if up_trend:
            if IsXBarUpClearClose(bar, bars_in_pattern, high, low, close):
                ValueBuffer[bar] = ValueBuffer[prev_bar] + 1.0
                XbccColors[bar] = 1.0
            elif IsXBarDownClearClose(bar, bars_in_pattern, high, low, close):
                ValueBuffer[bar] = -1.0
                XbccColors[bar] = 0.0
                up_trend = False
            else:
                ValueBuffer[bar] = ValueBuffer[prev_bar]
                if close[bar] >= close[prev_bar]:
                    XbccColors[bar] = 4.0
                else:
                    XbccColors[bar] = 5.0
        else:
            if IsXBarDownClearClose(bar, bars_in_pattern, high, low, close):
                ValueBuffer[bar] = ValueBuffer[prev_bar] - 1.0
                XbccColors[bar] = 0.0
            elif IsXBarUpClearClose(bar, bars_in_pattern, high, low, close):
                ValueBuffer[bar] = 1.0
                XbccColors[bar] = 1.0
                up_trend = True
            else:
                ValueBuffer[bar] = ValueBuffer[prev_bar]
                if close[bar] <= close[prev_bar]:
                    XbccColors[bar] = 2.0
                else:
                    XbccColors[bar] = 3.0
        if bar < (rates_total - 1):
            _s_OnCalculate__up_trend = up_trend
    return rates_total

# ---- static local variables
_s_OnCalculate__up_trend = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Xbarclearclosetrend(_MQL5Indicator):
    name = 'xbarclearclosetrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBarsInPattern': 5,  # Bars In Pattern
    }

