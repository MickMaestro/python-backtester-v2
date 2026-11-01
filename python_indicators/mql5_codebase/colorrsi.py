"""colorrsi — converted from MQL5: MQL5 Indicators/ColorRSI/colorrsi.mq5

Copyright: Copyright © 2009, TheXpert; Link: theforexpert@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, TheXpert', 'link': 'theforexpert@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [255, 16711680, 65280]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ColorRSI'}, 'levels': [], 'description': [], 'name': 'colorrsi', 'source': 'MQL5 Indicators/ColorRSI/colorrsi.mq5', 'folder': 'ColorRSI', 'inputs': [{'mql': 'iRSIPeriod', 'py': 'iRSIPeriod', 'param': 'iRSIPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'iRSIPrice', 'py': 'iRSIPrice', 'param': 'iRSIPrice', 'type': 'int', 'default': 1, 'label': 'Price timeseries', 'sinput': False}, {'mql': 'iHighLevel', 'py': 'iHighLevel', 'param': 'iHighLevel', 'type': 'int', 'default': 60, 'label': 'Overbought level', 'sinput': False}, {'mql': 'iMiddleLevel', 'py': 'iMiddleLevel', 'param': 'iMiddleLevel', 'type': 'int', 'default': 50, 'label': 'Medium of the range', 'sinput': False}, {'mql': 'iLowLevel', 'py': 'iLowLevel', 'param': 'iLowLevel', 'type': 'int', 'default': 40, 'label': 'Oversold level', 'sinput': False}, {'mql': 'iColor', 'py': 'iColor', 'param': None, 'type': 'color', 'default': 13828244, 'label': 'Levels color', 'sinput': False}, {'mql': 'iStyle', 'py': 'iStyle', 'param': 'iStyle', 'type': 'int', 'default': 3, 'label': 'levels execution style', 'sinput': False}, {'mql': 'iWidth', 'py': 'iWidth', 'param': 'iWidth', 'type': 'int', 'default': 1, 'label': 'Levels width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum WIDTH
W1 = 1
W2 = 2
W3 = 3
W4 = 4
W5 = 5
_enum('WIDTH', {1: 'W1', 2: 'W2', 3: 'W3', 4: 'W4', 5: 'W5'})

# enum STYLE
SOLID = 0
DASH = 1
DOT = 2
DASHDOT = 3
DASHDOTDOT = 4
_enum('STYLE', {0: 'SOLID', 1: 'DASH', 2: 'DOT', 3: 'DASHDOT', 4: 'DASHDOTDOT'})

# ---- inputs and global variables
iRSIPeriod = _input('iRSIPeriod', 14)  # RSI period
iRSIPrice = _input('iRSIPrice', PRICE_CLOSE)  # Price timeseries
iHighLevel = _input('iHighLevel', 60)  # Overbought level
iMiddleLevel = _input('iMiddleLevel', 50)  # Medium of the range
iLowLevel = _input('iLowLevel', 40)  # Oversold level
iColor = _input('iColor', clrDarkViolet)  # Levels color
iStyle = _input('iStyle', STYLE_DASHDOT)  # levels execution style
iWidth = _input('iWidth', W1)  # Levels width
ColorBuffer = Arr(0, 0.0)
ExtLineBuffer = Arr(0, 0.0)
min_rates_total = 0
RSI_Handle = 0
HighLevel = 0
MiddleLevel = 0
LowLevel = 0

def OnInit():
    global HighLevel, LowLevel, MiddleLevel, RSI_Handle, min_rates_total
    min_rates_total = iRSIPeriod
    HighLevel = MathMin(100, MathMax(0, iHighLevel))
    MiddleLevel = MathMin(100, MathMax(0, iMiddleLevel))
    LowLevel = MathMin(100, MathMax(0, iLowLevel))
    RSI_Handle = iRSI(None, 0, iRSIPeriod, iRSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI indicator')
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'ColorRSI(', iRSIPeriod, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtLineBuffer, True)
    ArraySetAsSeries(ColorBuffer, True)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, iColor)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, iColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, iStyle)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, iStyle)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, iStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, iWidth)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, iWidth)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 2, iWidth)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(RSI_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, ExtLineBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 1
        res = ExtLineBuffer[bar]
        if res > HighLevel:
            clr = 2
        elif res < LowLevel:
            clr = 0
        ColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorrsi(_MQL5Indicator):
    name = 'colorrsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iRSIPeriod': 14,  # RSI period
        'iRSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price timeseries
        'iHighLevel': 60,  # Overbought level
        'iMiddleLevel': 50,  # Medium of the range
        'iLowLevel': 40,  # Oversold level
        'iStyle': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dash-dot-dot line'}, default=3),  # levels execution style
        'iWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Levels width
    }

