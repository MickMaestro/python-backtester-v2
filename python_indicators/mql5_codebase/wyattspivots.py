"""WyattsPivots — converted from MQL5: MQL5 Indicators/WyattsPivots/WyattsPivots.mq5

Copyright: Copyright © 2018, ; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, ', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'WyattsPivots', 'source': 'MQL5 Indicators/WyattsPivots/WyattsPivots.mq5', 'folder': 'WyattsPivots', 'inputs': [{'mql': 'CountPeriods', 'py': 'CountPeriods', 'param': 'CountPeriods', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'TimePeriod', 'py': 'TimePeriod', 'param': 'TimePeriod', 'type': 'int', 'default': 16408, 'label': '', 'sinput': False}, {'mql': 'PlotPivots', 'py': 'PlotPivots', 'param': 'PlotPivots', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'PlotFuturePivots', 'py': 'PlotFuturePivots', 'param': 'PlotFuturePivots', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'PlotFuturePivotsExtendLeft', 'py': 'PlotFuturePivotsExtendLeft', 'param': 'PlotFuturePivotsExtendLeft', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'PlotPivotLabels', 'py': 'PlotPivotLabels', 'param': 'PlotPivotLabels', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'PlotPivotPrices', 'py': 'PlotPivotPrices', 'param': 'PlotPivotPrices', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'StylePivots', 'py': 'StylePivots', 'param': 'StylePivots', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'WidthPivots', 'py': 'WidthPivots', 'param': 'WidthPivots', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'ColorRes', 'py': 'ColorRes', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'ColorPP', 'py': 'ColorPP', 'param': None, 'type': 'color', 'default': 8421504, 'label': '', 'sinput': False}, {'mql': 'ColorSup', 'py': 'ColorSup', 'param': None, 'type': 'color', 'default': 32768, 'label': '', 'sinput': False}, {'mql': 'PlotMidpoints', 'py': 'PlotMidpoints', 'param': 'PlotMidpoints', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'StyleMidpoints', 'py': 'StyleMidpoints', 'param': 'StyleMidpoints', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'WidthMidpoints', 'py': 'WidthMidpoints', 'param': 'WidthMidpoints', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ColorM35', 'py': 'ColorM35', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'ColorM02', 'py': 'ColorM02', 'param': None, 'type': 'color', 'default': 32768, 'label': '', 'sinput': False}, {'mql': 'PlotZones', 'py': 'PlotZones', 'param': 'PlotZones', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'ColorBuyZone', 'py': 'ColorBuyZone', 'param': None, 'type': 'color', 'default': 9498256, 'label': '', 'sinput': False}, {'mql': 'ColorSellZone', 'py': 'ColorSellZone', 'param': None, 'type': 'color', 'default': 13353215, 'label': '', 'sinput': False}, {'mql': 'PlotBorders', 'py': 'PlotBorders', 'param': 'PlotBorders', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'StyleBorder', 'py': 'StyleBorder', 'param': 'StyleBorder', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'WidthBorder', 'py': 'WidthBorder', 'param': 'WidthBorder', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'ColorBorder', 'py': 'ColorBorder', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'PlotFibots', 'py': 'PlotFibots', 'param': 'PlotFibots', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'PlotFibotLabels', 'py': 'PlotFibotLabels', 'param': 'PlotFibotLabels', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'PlotFibotPrices', 'py': 'PlotFibotPrices', 'param': 'PlotFibotPrices', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'StyleFibots1', 'py': 'StyleFibots1', 'param': 'StyleFibots1', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'StyleFibots2', 'py': 'StyleFibots2', 'param': 'StyleFibots2', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'WidthFibots1', 'py': 'WidthFibots1', 'param': 'WidthFibots1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'WidthFibots2', 'py': 'WidthFibots2', 'param': 'WidthFibots2', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ColorFibots', 'py': 'ColorFibots', 'param': None, 'type': 'color', 'default': 16748574, 'label': '', 'sinput': False}, {'mql': 'PlotYesterdayOHLC', 'py': 'PlotYesterdayOHLC', 'param': 'PlotYesterdayOHLC', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'PlotOHLCPrices', 'py': 'PlotOHLCPrices', 'param': 'PlotOHLCPrices', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'StyleOHLC', 'py': 'StyleOHLC', 'param': 'StyleOHLC', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'WidthOHLC', 'py': 'WidthOHLC', 'param': 'WidthOHLC', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ColorO', 'py': 'ColorO', 'param': None, 'type': 'color', 'default': 55295, 'label': '', 'sinput': False}, {'mql': 'ColorH', 'py': 'ColorH', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'ColorL', 'py': 'ColorL', 'param': None, 'type': 'color', 'default': 32768, 'label': '', 'sinput': False}, {'mql': 'ColorC', 'py': 'ColorC', 'param': None, 'type': 'color', 'default': 16711935, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CountPeriods = _input('CountPeriods', 20)
TimePeriod = _input('TimePeriod', PERIOD_D1)
PlotPivots = _input('PlotPivots', True)
PlotFuturePivots = _input('PlotFuturePivots', True)
PlotFuturePivotsExtendLeft = _input('PlotFuturePivotsExtendLeft', True)
PlotPivotLabels = _input('PlotPivotLabels', False)
PlotPivotPrices = _input('PlotPivotPrices', False)
StylePivots = _input('StylePivots', STYLE_SOLID)
WidthPivots = _input('WidthPivots', 2)
ColorRes = _input('ColorRes', clrRed)
ColorPP = _input('ColorPP', clrGray)
ColorSup = _input('ColorSup', clrGreen)
PlotMidpoints = _input('PlotMidpoints', False)
StyleMidpoints = _input('StyleMidpoints', STYLE_DASH)
WidthMidpoints = _input('WidthMidpoints', 1)
ColorM35 = _input('ColorM35', clrRed)
ColorM02 = _input('ColorM02', clrGreen)
PlotZones = _input('PlotZones', True)
ColorBuyZone = _input('ColorBuyZone', clrLightGreen)
ColorSellZone = _input('ColorSellZone', clrPink)
PlotBorders = _input('PlotBorders', True)
StyleBorder = _input('StyleBorder', STYLE_SOLID)
WidthBorder = _input('WidthBorder', 2)
ColorBorder = _input('ColorBorder', clrBlack)
PlotFibots = _input('PlotFibots', True)
PlotFibotLabels = _input('PlotFibotLabels', False)
PlotFibotPrices = _input('PlotFibotPrices', False)
StyleFibots1 = _input('StyleFibots1', STYLE_DOT)
StyleFibots2 = _input('StyleFibots2', STYLE_SOLID)
WidthFibots1 = _input('WidthFibots1', 1)
WidthFibots2 = _input('WidthFibots2', 1)
ColorFibots = _input('ColorFibots', clrDodgerBlue)
PlotYesterdayOHLC = _input('PlotYesterdayOHLC', False)
PlotOHLCPrices = _input('PlotOHLCPrices', False)
StyleOHLC = _input('StyleOHLC', STYLE_DOT)
WidthOHLC = _input('WidthOHLC', 1)
ColorO = _input('ColorO', clrGold)
ColorH = _input('ColorH', clrRed)
ColorL = _input('ColorL', clrGreen)
ColorC = _input('ColorC', clrMagenta)
period = ""
timestart = 0
timeend = 0
open = 0.0
close = 0.0
high = 0.0
low = 0.0
PP = 0.0  # Pivot Levels
R1 = 0.0
R2 = 0.0
R3 = 0.0
S1 = 0.0
S2 = 0.0
S3 = 0.0
M0 = 0.0
M1 = 0.0
M2 = 0.0
M3 = 0.0
M4 = 0.0
M5 = 0.0
f214 = 0.0  # Fibot Levels
f236 = 0.0
f382 = 0.0
f50 = 0.0
f618 = 0.0
f764 = 0.0
f786 = 0.0
rangeopen1 = 0.0  # OHLC Levels
rangeopen2 = 0.0
rangeclose1 = 0.0
rangeclose2 = 0.0
shift = 0
nTimePeriod = 0
nCountPeriods = 1

def LevelsDelete(name):
    ObjectDelete(0, 'R3' + name)
    ObjectDelete(0, 'R2' + name)
    ObjectDelete(0, 'R1' + name)
    ObjectDelete(0, 'PP' + name)
    ObjectDelete(0, 'S1' + name)
    ObjectDelete(0, 'S2' + name)
    ObjectDelete(0, 'S3' + name)
    ObjectDelete(0, 'R3P' + name)
    ObjectDelete(0, 'R2P' + name)
    ObjectDelete(0, 'R1P' + name)
    ObjectDelete(0, 'PPP' + name)
    ObjectDelete(0, 'S1P' + name)
    ObjectDelete(0, 'S2P' + name)
    ObjectDelete(0, 'S3P' + name)
    ObjectDelete(0, 'R3L' + name)
    ObjectDelete(0, 'R2L' + name)
    ObjectDelete(0, 'R1L' + name)
    ObjectDelete(0, 'PPL' + name)
    ObjectDelete(0, 'S1L' + name)
    ObjectDelete(0, 'S2L' + name)
    ObjectDelete(0, 'S3L' + name)
    ObjectDelete(0, 'M0' + name)
    ObjectDelete(0, 'M1' + name)
    ObjectDelete(0, 'M2' + name)
    ObjectDelete(0, 'M3' + name)
    ObjectDelete(0, 'M4' + name)
    ObjectDelete(0, 'M5' + name)
    ObjectDelete(0, 'M0P' + name)
    ObjectDelete(0, 'M1P' + name)
    ObjectDelete(0, 'M2P' + name)
    ObjectDelete(0, 'M3P' + name)
    ObjectDelete(0, 'M4P' + name)
    ObjectDelete(0, 'M5P' + name)
    ObjectDelete(0, 'M0L' + name)
    ObjectDelete(0, 'M1L' + name)
    ObjectDelete(0, 'M2L' + name)
    ObjectDelete(0, 'M3L' + name)
    ObjectDelete(0, 'M4L' + name)
    ObjectDelete(0, 'M5L' + name)
    ObjectDelete(0, 'BZ' + name)
    ObjectDelete(0, 'SZ' + name)
    ObjectDelete(0, 'BDU' + name)
    ObjectDelete(0, 'BDD' + name)
    ObjectDelete(0, 'BDL' + name)
    ObjectDelete(0, 'BDR' + name)
    ObjectDelete(0, 'f214a' + name)
    ObjectDelete(0, 'f236a' + name)
    ObjectDelete(0, 'f382a' + name)
    ObjectDelete(0, 'f50a' + name)
    ObjectDelete(0, 'f618a' + name)
    ObjectDelete(0, 'f764a' + name)
    ObjectDelete(0, 'f786a' + name)
    ObjectDelete(0, 'f214b' + name)
    ObjectDelete(0, 'f236b' + name)
    ObjectDelete(0, 'f382b' + name)
    ObjectDelete(0, 'f50b' + name)
    ObjectDelete(0, 'f618b' + name)
    ObjectDelete(0, 'f764b' + name)
    ObjectDelete(0, 'f786b' + name)
    ObjectDelete(0, 'f214p' + name)
    ObjectDelete(0, 'f236p' + name)
    ObjectDelete(0, 'f382p' + name)
    ObjectDelete(0, 'f50p' + name)
    ObjectDelete(0, 'f618p' + name)
    ObjectDelete(0, 'f764p' + name)
    ObjectDelete(0, 'f786p' + name)
    ObjectDelete(0, 'f214l' + name)
    ObjectDelete(0, 'f236l' + name)
    ObjectDelete(0, 'f382l' + name)
    ObjectDelete(0, 'f50l' + name)
    ObjectDelete(0, 'f618l' + name)
    ObjectDelete(0, 'f764l' + name)
    ObjectDelete(0, 'f786l' + name)
    ObjectDelete(0, 'open' + name)
    ObjectDelete(0, 'high' + name)
    ObjectDelete(0, 'low' + name)
    ObjectDelete(0, 'close' + name)
    ObjectDelete(0, 'openp' + name)
    ObjectDelete(0, 'highp' + name)
    ObjectDelete(0, 'lowp' + name)
    ObjectDelete(0, 'closep' + name)

def PlotTrend(chart_ID=0, name='trendline', subwindow=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrBlack, style=STYLE_SOLID, width=2, back=True, selection=False, ray=False, hidden=True):
    ResetLastError()
    if ObjectFind(chart_ID, name) != subwindow:
        if not ObjectCreate(chart_ID, name, OBJ_TREND, subwindow, time1, price1, time2, price2):
            Print('PlotTrend', ': failed to create arrow = ', GetLastError())
            return False
    else:
        ObjectMove(chart_ID, name, 0, time1, price1)
        ObjectMove(chart_ID, name, 1, time2, price2)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY, ray)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    return True

def PlotRectangle(chart_ID=0, name='rectangle', subwindow=0, time1=0, price1=1.0, time2=0, price2=0.0, clr=clrGray, back=True, selection=False, hidden=True):
    if ObjectFind(chart_ID, name) != subwindow:
        if not ObjectCreate(chart_ID, name, OBJ_RECTANGLE, subwindow, time1, price1, time2, price2):
            Print('PlotRectangle', ': failed to create arrow = ', GetLastError())
            return False
    else:
        ObjectMove(chart_ID, name, 0, time1, price1)
        ObjectMove(chart_ID, name, 1, time2, price2)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_FILL, True)
    return True

def PlotText(chart_ID=0, name='text', subwindow=0, time1=0, price1=0.0, text='text', font='Arial', font_size=10, clr=clrGray, anchor=ANCHOR_RIGHT_UPPER, back=True, selection=False, hidden=True):
    if ObjectFind(chart_ID, name) != subwindow:
        if not ObjectCreate(chart_ID, name, OBJ_TEXT, subwindow, time1, price1):
            Print('PlotText', ': failed to create arrow = ', GetLastError())
            return False
    else:
        ObjectMove(chart_ID, name, 0, time1, price1)
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
    ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
    ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    return True

def LevelsDraw(shft, tmestrt, tmend, name, future, fClose):
    global M0, M1, M2, M3, M4, M5, PP, R1, R2, R3, S1, S2, S3, close, f214, f236, f382, f50, f618, f764, f786, high, low, open, rangeclose1, rangeclose2, rangeopen1, rangeopen2
    high = iHigh(None, TimePeriod, shft)
    low = iLow(None, TimePeriod, shft)
    open = iOpen(None, TimePeriod, shft)
    if future == False:
        close = iClose(None, TimePeriod, shft)
    else:
        close = fClose[shft]
    PP = (high + low + close) / 3.0
    R1 = (2 * PP) - low
    R2 = PP + (high - low)
    R3 = (2 * PP) + (high - (2 * low))
    S1 = (2 * PP) - high
    S2 = PP - (high - low)
    S3 = (2 * PP) - ((2 * high) - low)
    M0 = 0.5 * (S2 + S3)
    M1 = 0.5 * (S1 + S2)
    M2 = 0.5 * (PP + S1)
    M3 = 0.5 * (PP + R1)
    M4 = 0.5 * (R1 + R2)
    M5 = 0.5 * (R2 + R3)
    range_ = (high - low) / 100
    f214 = low + (range_ * (100 - 21.4))
    f236 = low + (range_ * (100 - 23.6))
    f382 = low + (range_ * (100 - 38.2))
    f50 = low + (range_ * (100 - 50))
    f618 = low + (range_ * 38.2)
    f764 = low + (range_ * 23.6)
    f786 = low + (range_ * 21.4)
    if not range_:
        range_ = Point() / 100
    rangeopen1 = _fdiv(open - low, range_)
    rangeopen2 = 100 - _fdiv(open - low, range_)
    rangeclose1 = _fdiv(close - low, range_)
    rangeclose2 = 100 - _fdiv(close - low, range_)
    if PlotPivots:
        PlotTrend(0, 'R3' + name, 0, tmestrt, R3, tmend, R3, ColorRes, StylePivots, WidthPivots, True, False, False, True)
        PlotTrend(0, 'R2' + name, 0, tmestrt, R2, tmend, R2, ColorRes, StylePivots, WidthPivots, True, False, False, True)
        PlotTrend(0, 'R1' + name, 0, tmestrt, R1, tmend, R1, ColorRes, StylePivots, WidthPivots, True, False, False, True)
        PlotTrend(0, 'PP' + name, 0, tmestrt, PP, tmend, PP, ColorPP, StylePivots, WidthPivots, True, False, False, True)
        PlotTrend(0, 'S1' + name, 0, tmestrt, S1, tmend, S1, ColorSup, StylePivots, WidthPivots, True, False, False, True)
        PlotTrend(0, 'S2' + name, 0, tmestrt, S2, tmend, S2, ColorSup, StylePivots, WidthPivots, True, False, False, True)
        PlotTrend(0, 'S3' + name, 0, tmestrt, S3, tmend, S3, ColorSup, StylePivots, WidthPivots, True, False, False, True)
        if PlotPivotLabels:
            PlotText(0, 'R3L' + name, 0, tmend, R3, 'R3', 'Arial', 8, ColorRes, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'R2L' + name, 0, tmend, R2, 'R2', 'Arial', 8, ColorRes, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'R1L' + name, 0, tmend, R1, 'R1', 'Arial', 8, ColorRes, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'PPL' + name, 0, tmend, PP, 'PP', 'Arial', 8, ColorPP, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'S1L' + name, 0, tmend, S1, 'S1', 'Arial', 8, ColorSup, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'S2L' + name, 0, tmend, S2, 'S2', 'Arial', 8, ColorSup, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'S3L' + name, 0, tmend, S3, 'S3', 'Arial', 8, ColorSup, ANCHOR_RIGHT_UPPER)
        if PlotPivotPrices:
            PlotText(0, 'R3P' + name, 0, tmestrt, R3, DoubleToString(R3, 4), 'Arial', 8, ColorRes, ANCHOR_LEFT_UPPER)
            PlotText(0, 'R2P' + name, 0, tmestrt, R2, DoubleToString(R2, 4), 'Arial', 8, ColorRes, ANCHOR_LEFT_UPPER)
            PlotText(0, 'R1P' + name, 0, tmestrt, R1, DoubleToString(R1, 4), 'Arial', 8, ColorRes, ANCHOR_LEFT_UPPER)
            PlotText(0, 'PPP' + name, 0, tmestrt, PP, DoubleToString(PP, 4), 'Arial', 8, ColorPP, ANCHOR_LEFT_UPPER)
            PlotText(0, 'S1P' + name, 0, tmestrt, S1, DoubleToString(S1, 4), 'Arial', 8, ColorSup, ANCHOR_LEFT_UPPER)
            PlotText(0, 'S2P' + name, 0, tmestrt, S2, DoubleToString(S2, 4), 'Arial', 8, ColorSup, ANCHOR_LEFT_UPPER)
            PlotText(0, 'S3P' + name, 0, tmestrt, S3, DoubleToString(S3, 4), 'Arial', 8, ColorSup, ANCHOR_LEFT_UPPER)
    if PlotMidpoints:
        PlotTrend(0, 'M0' + name, 0, tmestrt, M0, tmend, M0, ColorM02, StyleMidpoints, WidthMidpoints, True, False, False, True)
        PlotTrend(0, 'M1' + name, 0, tmestrt, M1, tmend, M1, ColorM02, StyleMidpoints, WidthMidpoints, True, False, False, True)
        PlotTrend(0, 'M2' + name, 0, tmestrt, M2, tmend, M2, ColorM02, StyleMidpoints, WidthMidpoints, True, False, False, True)
        PlotTrend(0, 'M3' + name, 0, tmestrt, M3, tmend, M3, ColorM35, StyleMidpoints, WidthMidpoints, True, False, False, True)
        PlotTrend(0, 'M4' + name, 0, tmestrt, M4, tmend, M4, ColorM35, StyleMidpoints, WidthMidpoints, True, False, False, True)
        PlotTrend(0, 'M5' + name, 0, tmestrt, M5, tmend, M5, ColorM35, StyleMidpoints, WidthMidpoints, True, False, False, True)
        if PlotPivotLabels:
            PlotText(0, 'M0L' + name, 0, tmend, M0, 'M0', 'Arial', 8, ColorSup, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'M1L' + name, 0, tmend, M1, 'M1', 'Arial', 8, ColorSup, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'M2L' + name, 0, tmend, M2, 'M2', 'Arial', 8, ColorSup, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'M3L' + name, 0, tmend, M3, 'M3', 'Arial', 8, ColorRes, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'M4L' + name, 0, tmend, M4, 'M4', 'Arial', 8, ColorRes, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'M5L' + name, 0, tmend, M5, 'M5', 'Arial', 8, ColorRes, ANCHOR_RIGHT_UPPER)
        if PlotPivotPrices:
            PlotText(0, 'M0P' + name, 0, tmestrt, M0, DoubleToString(M0, 4), 'Arial', 8, ColorSup, ANCHOR_LEFT_UPPER)
            PlotText(0, 'M1P' + name, 0, tmestrt, M1, DoubleToString(M1, 4), 'Arial', 8, ColorSup, ANCHOR_LEFT_UPPER)
            PlotText(0, 'M2P' + name, 0, tmestrt, M2, DoubleToString(M2, 4), 'Arial', 8, ColorSup, ANCHOR_LEFT_UPPER)
            PlotText(0, 'M3P' + name, 0, tmestrt, M3, DoubleToString(M3, 4), 'Arial', 8, ColorRes, ANCHOR_LEFT_UPPER)
            PlotText(0, 'M4P' + name, 0, tmestrt, M4, DoubleToString(M4, 4), 'Arial', 8, ColorRes, ANCHOR_LEFT_UPPER)
            PlotText(0, 'M5P' + name, 0, tmestrt, M5, DoubleToString(M5, 4), 'Arial', 8, ColorRes, ANCHOR_LEFT_UPPER)
    if PlotZones:
        PlotRectangle(0, 'BZ' + name, 0, tmestrt, M1, tmend, S2, ColorBuyZone)
        PlotRectangle(0, 'SZ' + name, 0, tmestrt, M4, tmend, R2, ColorSellZone)
    if PlotBorders:
        PlotTrend(0, 'BDL' + name, 0, tmestrt, R2, tmestrt, S2, ColorBorder, StyleBorder, WidthBorder, True, False, False, True)
        PlotTrend(0, 'BDR' + name, 0, tmend, R2, tmend, S2, ColorBorder, StyleBorder, WidthBorder, True, False, False, True)
    if PlotFibots:
        PlotTrend(0, 'f214a' + name, 0, tmestrt, f214, tmend, f214, ColorFibots, StyleFibots1, WidthFibots1)
        PlotTrend(0, 'f382a' + name, 0, tmestrt, f382, tmend, f382, ColorFibots, StyleFibots1, WidthFibots1)
        PlotTrend(0, 'f50a' + name, 0, tmestrt, f50, tmend, f50, ColorFibots, StyleFibots1, WidthFibots1)
        PlotTrend(0, 'f618a' + name, 0, tmestrt, f618, tmend, f618, ColorFibots, StyleFibots1, WidthFibots1)
        PlotTrend(0, 'f786a' + name, 0, tmestrt, f786, tmend, f786, ColorFibots, StyleFibots1, WidthFibots1)
        PlotTrend(0, 'f214b' + name, 0, tmestrt + _idiv(nTimePeriod, 6), f214, tmend, f214, ColorFibots, StyleFibots2)
        PlotTrend(0, 'f382b' + name, 0, tmestrt + _idiv(nTimePeriod, 6), f382, tmend, f382, ColorFibots, StyleFibots2, WidthFibots2)
        PlotTrend(0, 'f50b' + name, 0, tmestrt + _idiv(nTimePeriod, 6), f50, tmend, f50, ColorFibots, StyleFibots2, WidthFibots2)
        PlotTrend(0, 'f618b' + name, 0, tmestrt + _idiv(nTimePeriod, 6), f618, tmend, f618, ColorFibots, StyleFibots2, WidthFibots2)
        PlotTrend(0, 'f786b' + name, 0, tmestrt + _idiv(nTimePeriod, 6), f786, tmend, f786, ColorFibots, StyleFibots2, WidthFibots2)
        if PlotFibotLabels:
            PlotText(0, 'f214l' + name, 0, tmend, f214, '21.4%', 'Arial', 8, ColorFibots, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'f382l' + name, 0, tmend, f382, '38.2%', 'Arial', 8, ColorFibots, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'f50l' + name, 0, tmend, f50, '50%', 'Arial', 8, ColorFibots, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'f618l' + name, 0, tmend, f618, '61.8%', 'Arial', 8, ColorFibots, ANCHOR_RIGHT_UPPER)
            PlotText(0, 'f786l' + name, 0, tmend, f786, '78.6%', 'Arial', 8, ColorFibots, ANCHOR_RIGHT_UPPER)
        if PlotFibotPrices:
            PlotText(0, 'f214p' + name, 0, tmestrt, f214, DoubleToString(f214, 4), 'Arial', 8, ColorFibots, ANCHOR_LEFT_UPPER)
            PlotText(0, 'f382p' + name, 0, tmestrt, f382, DoubleToString(f382, 4), 'Arial', 8, ColorFibots, ANCHOR_LEFT_UPPER)
            PlotText(0, 'f50p' + name, 0, tmestrt, f50, DoubleToString(f50, 4), 'Arial', 8, ColorFibots, ANCHOR_LEFT_UPPER)
            PlotText(0, 'f618p' + name, 0, tmestrt, f618, DoubleToString(f618, 4), 'Arial', 8, ColorFibots, ANCHOR_LEFT_UPPER)
            PlotText(0, 'f786p' + name, 0, tmestrt, f786, DoubleToString(f786, 4), 'Arial', 8, ColorFibots, ANCHOR_LEFT_UPPER)
    if PlotYesterdayOHLC:
        PlotTrend(0, 'open' + name, 0, tmestrt, open, tmestrt + _idiv(nTimePeriod, 6), open, ColorO, StyleOHLC, WidthOHLC, True, False, False, True)
        PlotTrend(0, 'high' + name, 0, tmestrt, high, tmestrt + _idiv(nTimePeriod, 6), high, ColorH, StyleOHLC, WidthOHLC, True, False, False, True)
        PlotTrend(0, 'low' + name, 0, tmestrt, low, tmestrt + _idiv(nTimePeriod, 6), low, ColorL, StyleOHLC, WidthOHLC, True, False, False, True)
        PlotTrend(0, 'close' + name, 0, tmestrt, close, tmestrt + _idiv(nTimePeriod, 6), close, ColorC, StyleOHLC, WidthOHLC, True, False, False, True)
        if PlotOHLCPrices:
            PlotText(0, 'openp' + name, 0, tmestrt + _idiv(nTimePeriod, 6), open, DoubleToString(rangeopen1, 1) + '/' + DoubleToString(rangeopen2, 1) + '%', 'Arial', 8, ColorO, 6)
            PlotText(0, 'closep' + name, 0, tmestrt + _idiv(nTimePeriod, 6), close, DoubleToString(rangeclose1, 1) + '/' + DoubleToString(rangeclose2, 1) + '%', 'Arial', 8, ColorC, 6)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global nCountPeriods, nTimePeriod, period
    period = GetStringTimeframe(TimePeriod)
    nTimePeriod = PeriodSeconds(TimePeriod)
    if ((not MQLInfoInteger(MQL_TESTER)) and (not MQLInfoInteger(MQL_VISUAL_MODE))) and (not MQLInfoInteger(MQL_DEBUG)):
        nCountPeriods = CountPeriods
    ChartRedraw(0)

def OnDeinit(reason):
    global shift
    shift = 0
    while shift <= CountPeriods:
        LevelsDelete(period + _str(shift))
        shift += 1
    LevelsDelete('F' + period)
    Comment('')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global shift, timeend, timestart
    ArraySetAsSeries(Close, True)
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    if (MQLInfoInteger(MQL_TESTER) or MQLInfoInteger(MQL_VISUAL_MODE)) or MQLInfoInteger(MQL_DEBUG):
        if not limit:
            return prev_calculated
    shift = nCountPeriods - 1
    while shift >= 0:
        timestart = iTime(None, TimePeriod, shift)
        timeend = timestart + nTimePeriod
        LevelsDraw(shift + 1, timestart, timeend, period + _str(shift), False, Close)
        shift -= 1
    if PlotFuturePivots:
        if PlotFuturePivotsExtendLeft:
            timestart = iTime(None, TimePeriod, 1) + nTimePeriod
            timeend = iTime(None, TimePeriod, 1) + (nTimePeriod * 2)
        else:
            timestart = iTime(None, TimePeriod, 0) + nTimePeriod
            timeend = iTime(None, TimePeriod, 0) + (nTimePeriod * 2)
        LevelsDraw(0, timestart, timeend, 'F' + period, True, Close)
    ChartRedraw(0)
    return prev_calculated


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WyattsPivots(_MQL5Indicator):
    name = 'WyattsPivots'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CountPeriods': 20,
        'TimePeriod': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),
        'PlotPivots': True,
        'PlotFuturePivots': True,
        'PlotFuturePivotsExtendLeft': True,
        'PlotPivotLabels': False,
        'PlotPivotPrices': False,
        'StylePivots': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'WidthPivots': 2,
        'PlotMidpoints': False,
        'StyleMidpoints': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),
        'WidthMidpoints': 1,
        'PlotZones': True,
        'PlotBorders': True,
        'StyleBorder': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'WidthBorder': 2,
        'PlotFibots': True,
        'PlotFibotLabels': False,
        'PlotFibotPrices': False,
        'StyleFibots1': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),
        'StyleFibots2': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'WidthFibots1': 1,
        'WidthFibots2': 1,
        'PlotYesterdayOHLC': False,
        'PlotOHLCPrices': False,
        'StyleOHLC': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),
        'WidthOHLC': 1,
    }

