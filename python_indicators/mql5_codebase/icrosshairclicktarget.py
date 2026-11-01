"""iCrosshairClickTarget — converted from MQL5: MQL5 Indicators/iCrosshairClickTarget/iCrosshairClickTarget.mq5

iCrosshairClickTarget indicator is the improved version of iCrosshair indicator for MT4, by adding
'click Target' and the trend line, with text of the 'number of bars between target and crosshair',
and the difference in pips between Price at target level and Price at crosshair level.
version: 1.0 ~ Update number: 02 ~ Last update: 2021/11/21 @00:08 AM WIT (Western Indonesian Time)
Copyright: Copyright 2016, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 2016/12/18; Link: https://www.mql5.com/en/users/3rjfx; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 2016/12/18', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 0}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['iCrosshairClickTarget indicator is the improved version of iCrosshair indicator for MT4, by adding', "'click Target' and the trend line, with text of the 'number of bars between target and crosshair',", 'and the difference in pips between Price at target level and Price at crosshair level.', 'version: 1.0 ~ Update number: 02 ~ Last update: 2021/11/21 @00:08 AM WIT (Western Indonesian Time)'], 'name': 'iCrosshairClickTarget', 'source': 'MQL5 Indicators/iCrosshairClickTarget/iCrosshairClickTarget.mq5', 'folder': 'iCrosshairClickTarget', 'inputs': [{'mql': 'ColorLine', 'py': 'ColorLine', 'param': None, 'type': 'color', 'default': 4678655, 'label': 'Line color', 'sinput': False}, {'mql': 'ColorTarget', 'py': 'ColorTarget', 'param': None, 'type': 'color', 'default': 65535, 'label': 'Target color', 'sinput': False}, {'mql': 'ColorTrendLine', 'py': 'ColorTrendLine', 'param': None, 'type': 'color', 'default': 65280, 'label': 'Trend Line color', 'sinput': False}, {'mql': 'LineStyle', 'py': 'LineStyle', 'param': 'LineStyle', 'type': 'int', 'default': 0, 'label': 'Line style', 'sinput': False}, {'mql': 'LineWidth', 'py': 'LineWidth', 'param': 'LineWidth', 'type': 'int', 'default': 1, 'label': 'Line width', 'sinput': False}, {'mql': 'ShowTooltip', 'py': 'ShowTooltip', 'param': 'ShowTooltip', 'type': 'bool', 'default': True, 'label': 'Show Tooltip or Not', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ColorLine = _input('ColorLine', clrTomato)  # Line color
ColorTarget = _input('ColorTarget', clrYellow)  # Target color
ColorTrendLine = _input('ColorTrendLine', clrLime)  # Trend Line color
LineStyle = _input('LineStyle', STYLE_SOLID)  # Line style
LineWidth = _input('LineWidth', 1)  # Line width
ShowTooltip = _input('ShowTooltip', True)  # Show Tooltip or Not
bar0 = 0
bar1 = 0
ebar = 360
pip = 0.0
Price = 0.0
Price1 = 0.0
ePrice = Arr(0, 0.0)
chart_id = 0
OPEN = Arr(0, 0.0)
HIGH = Arr(0, 0.0)
LOW = Arr(0, 0.0)
CLOSE = Arr(0, 0.0)
VOLUME = Arr(0, 0)
TIME = Arr(0, 0)
tooltip = ""
tooltip1 = ""
short_name = ""

def OnInit():
    global Price, Price1, chart_id, pip, short_name
    SetIndexBuffer(0, ePrice, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'Target')
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, True)
    chart_id = ChartID()
    short_name = 'iCrosshairClickTarget'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    if Digits() == 3 or Digits() == 5:
        pip = Point() * 10
    elif Digits() == 2 or Digits() == 4:
        pip = Point()
    if StringSubstr(Symbol(), 0, 1) == 'X' or StringSubstr(Symbol(), 0, 1) == '#':
        pip = Point() * 10
    ArrayResize(OPEN, ebar)
    ArrayResize(HIGH, ebar)
    ArrayResize(LOW, ebar)
    ArrayResize(CLOSE, ebar)
    ArrayResize(TIME, ebar)
    ArrayResize(VOLUME, ebar)
    ArrayResize(ePrice, ebar)
    ArraySetAsSeries(OPEN, True)
    ArraySetAsSeries(HIGH, True)
    ArraySetAsSeries(LOW, True)
    ArraySetAsSeries(CLOSE, True)
    ArraySetAsSeries(TIME, True)
    ArraySetAsSeries(VOLUME, True)
    ArraySetAsSeries(ePrice, True)
    FillArraysBuffers(0, ebar)
    PriceMin = ChartGetDouble(chart_id, CHART_PRICE_MIN, 0)
    PriceMax = ChartGetDouble(chart_id, CHART_PRICE_MAX, 0)
    Price1 = NormalizeDouble(PriceMin + ((PriceMax - PriceMin) / 2), Digits())
    Price = NormalizeDouble(PriceMin + ((PriceMax - PriceMin) / 2), Digits())
    pi = NormalizeDouble(_fdiv(fabs(Price1 - Price), pip), Digits())
    DrawHVLine(chart_id, 'H Line', OBJ_HLINE, TIME[0], Price1, ColorLine, LineStyle, LineWidth, 'Click me!')
    DrawHVLine(chart_id, 'V Line', OBJ_VLINE, TIME[0], Price1, ColorLine, LineStyle, LineWidth, 'Click me!')
    DrawPriceLevel(chart_id, 'DotStart', OBJ_TEXT, TIME[0], Price1, CharToString(119), 'Wingdings', 14, ColorTarget, 'Click me!')
    DrawPriceLevel(chart_id, 'DotTarget', OBJ_TEXT, TIME[0], Price1, CharToString(164), 'Wingdings', 14, ColorTarget, 'Click me!')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), 0, -1)
    GlobalVariablesDeleteAll()
    return

def OnCalculate(rates_total, prev_calculated, begin, price):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global Price, Price1, _s_OnChartEvent_keyPressed, bar0, bar1, tooltip, tooltip1
    ResetLastError()
    if id_ == CHARTEVENT_OBJECT_CLICK:
        FillArraysBuffers(0, ebar)
        if (sparam == 'H Line' or sparam == 'V Line') or sparam == 'DotTarget':
            if not _s_OnChartEvent_keyPressed:
                _s_OnChartEvent_keyPressed = True
            else:
                _s_OnChartEvent_keyPressed = False
        if _s_OnChartEvent_keyPressed:
            ChartSetInteger(chart_id, CHART_EVENT_MOUSE_MOVE, True)
        else:
            ChartSetInteger(chart_id, CHART_EVENT_MOUSE_MOVE, False)
    if id_ == CHARTEVENT_MOUSE_MOVE:
        FillArraysBuffers(0, ebar)
        x = _int(lparam)
        y = _int(dparam)
        time = Box(0)
        window = Box(0)
        Price = 0.0
        if ChartXYToTimePrice(chart_id, x, y, window, time, _GlobRef(globals(), 'Price')):
            bar0 = iBarShift(Symbol(), 0, time.v, False)
            tooltip = 'Candle: ' + _str(bar0) + '\nOpen: ' + DoubleToString(OPEN[bar0], Digits()) + '\nHigh: ' + DoubleToString(HIGH[bar0], Digits()) + '\nLow: ' + DoubleToString(LOW[bar0], Digits()) + '\nClose: ' + DoubleToString(CLOSE[bar0], Digits()) + '\nVolume: ' + DoubleToString(VOLUME[bar0], 0) + '\n' + '\nPrice: ' + DoubleToString(Price, Digits()) + '\nUp Wick: ' + DoubleToString(upWick(bar0), 0) + '\nBody: ' + DoubleToString(BarBody(bar0), 0) + '\nDn Wick: ' + DoubleToString(dnWick(bar0), 0) + '\nRangeHL: ' + DoubleToString(RangeHL(bar0), 0) + '\n'
            DrawHVLine(chart_id, 'H Line', OBJ_HLINE, time.v, Price, ColorLine, LineStyle, LineWidth, tooltip)
            DrawHVLine(chart_id, 'V Line', OBJ_VLINE, time.v, Price, ColorLine, LineStyle, LineWidth, tooltip)
        x1 = _int(lparam)
        y1 = _int(dparam)
        dt0 = Box(0)
        window1 = Box(0)
        cand = 0
        Price1 = 0.0
        if ChartXYToTimePrice(chart_id, x1, y1, window1, dt0, _GlobRef(globals(), 'Price1')):
            bar1 = iBarShift(Symbol(), 0, dt0.v, False)
            if bar1 <= 0:
                bar1 = 0
            if bar1 <= 2:
                cand = 0
            else:
                cand = bar1 - 2
            bars = fabs(bar1 - bar0)
            pips = _fdiv(fabs(Price1 - Price), pip)
            tooltip = 'Candle: ' + _str(bar0) + '\nOpen: ' + DoubleToString(OPEN[bar0], Digits()) + '\nHigh: ' + DoubleToString(HIGH[bar0], Digits()) + '\nLow: ' + DoubleToString(LOW[bar0], Digits()) + '\nClose: ' + DoubleToString(CLOSE[bar0], Digits()) + '\nVolume: ' + DoubleToString(VOLUME[bar0], 0) + '\n' + '\nPrice: ' + DoubleToString(Price, Digits()) + '\nUp Wick: ' + DoubleToString(upWick(bar0), 0) + '\nBody: ' + DoubleToString(BarBody(bar0), 0) + '\nDn Wick: ' + DoubleToString(dnWick(bar0), 0) + '\nRangeHL: ' + DoubleToString(RangeHL(bar0), 0) + '\n'
            tooltip1 = 'Candle: ' + _str(bar1) + '\nBars Distance: ' + IntegerToString(bars, 2, 32) + '\nPips Distance: ' + DoubleToString(pips, 1) + '\nPrice: ' + DoubleToString(Price1, Digits()) + '\n'
            ObjectDelete(chart_id, 'TrendLine')
            ePrice[bar1] = Price1
            DrawHVLine(chart_id, 'H Line', OBJ_HLINE, TIME[bar1], Price1, ColorLine, LineStyle, LineWidth, tooltip)
            DrawHVLine(chart_id, 'V Line', OBJ_VLINE, TIME[bar1], Price1, ColorLine, LineStyle, LineWidth, tooltip)
            DrawPriceLevel(chart_id, 'DotTarget', OBJ_TEXT, TIME[bar1], Price1, CharToString(164), 'Wingdings', 14, ColorTarget, tooltip1)
            DrawPriceLevel(chart_id, 'DotStart', OBJ_TEXT, TIME[bar0], Price, CharToString(119), 'Wingdings', 14, ColorTarget, tooltip)
            TextTarget(chart_id, 'TargetText', OBJ_TEXT, TIME[cand], Price1, ColorTarget, bars, pips)
    if id_ == CHARTEVENT_CLICK:
        FillArraysBuffers(0, ebar)
        x1 = _int(lparam)
        y1 = _int(dparam)
        dt1 = Box(0)
        window1 = Box(0)
        cand = 0
        Price1 = 0.0
        if ChartXYToTimePrice(chart_id, x1, y1, window1, dt1, _GlobRef(globals(), 'Price1')):
            bar1 = iBarShift(Symbol(), 0, dt1.v, False)
            if bar1 <= 0:
                bar1 = 0
            if bar1 <= 2:
                cand = 0
            else:
                cand = bar1 - 2
            bars = fabs(bar1 - bar0)
            pips = _fdiv(fabs(Price1 - Price), pip)
            tooltip = 'Candle: ' + _str(bar0) + '\nOpen: ' + DoubleToString(OPEN[bar0], Digits()) + '\nHigh: ' + DoubleToString(HIGH[bar0], Digits()) + '\nLow: ' + DoubleToString(LOW[bar0], Digits()) + '\nClose: ' + DoubleToString(CLOSE[bar0], Digits()) + '\nVolume: ' + DoubleToString(VOLUME[bar0], 0) + '\n' + '\nPrice: ' + DoubleToString(Price, Digits()) + '\nUp Wick: ' + DoubleToString(upWick(bar0), 0) + '\nBody: ' + DoubleToString(BarBody(bar0), 0) + '\nDn Wick: ' + DoubleToString(dnWick(bar0), 0) + '\nRangeHL: ' + DoubleToString(RangeHL(bar0), 0) + '\n'
            tooltip1 = 'Candle: ' + _str(bar1) + '\nBars Distance: ' + IntegerToString(bars, 2, 32) + '\nPips Distance: ' + DoubleToString(pips, 1) + '\nPrice: ' + DoubleToString(Price1, Digits()) + '\n'
            ePrice[bar1] = Price1
            TrendLine(chart_id, 'TrendLine', OBJ_TREND, TIME[bar0], Price, TIME[bar1], Price1, ColorTrendLine, 0, LineWidth)
            DrawPriceLevel(chart_id, 'DotTarget', OBJ_TEXT, TIME[bar1], Price1, CharToString(164), 'Wingdings', 14, ColorTarget, tooltip1)
            DrawPriceLevel(chart_id, 'DotStart', OBJ_TEXT, TIME[bar0], Price, CharToString(119), 'Wingdings', 14, ColorTarget, tooltip)
            TextTarget(chart_id, 'TargetText', OBJ_TEXT, TIME[cand], Price1, ColorTarget, bars, pips)

def upWick(i):
    upBody = fmax(OPEN[i], CLOSE[i])
    return _fdiv(fabs(HIGH[i] - upBody), pip)

def BarBody(i):
    return _fdiv(fabs(OPEN[i] - CLOSE[i]), pip)

def dnWick(i):
    dnBody = fmin(OPEN[i], CLOSE[i])
    return _fdiv(fabs(dnBody - LOW[i]), pip)

def RangeHL(i):
    return _fdiv(HIGH[i] - LOW[i], pip)

def DrawHVLine(chartid, name, type_, time, prc, clr, style, width, tooltips):
    ObjectDelete(chartid, name)
    ObjectCreate(chartid, name, type_, 0, time, prc)
    ObjectSetInteger(chartid, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chartid, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chartid, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chartid, name, OBJPROP_BACK, False)
    ObjectSetInteger(chartid, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chartid, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chartid, name, OBJPROP_ZORDER, 0)
    ObjectSetInteger(chartid, name, OBJPROP_HIDDEN, True)
    if ShowTooltip:
        ObjectSetString(chartid, name, OBJPROP_TOOLTIP, tooltips)
    ChartRedraw(0)

def TrendLine(chartid, name, type_, time1, prc1, time2, prc2, clr, style, width):
    ObjectDelete(chartid, name)
    ObjectCreate(chartid, name, type_, 0, time1, prc1, time2, prc2)
    ObjectSetInteger(chartid, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chartid, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chartid, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chartid, name, OBJPROP_BACK, False)
    ObjectSetInteger(chartid, name, OBJPROP_RAY_RIGHT, False)
    ObjectSetInteger(chartid, name, OBJPROP_ZORDER, 0)
    ObjectSetInteger(chartid, name, OBJPROP_HIDDEN, True)
    ChartRedraw(0)

def DrawPriceLevel(chartid, name, type_, time, prc, text, font_mode, font_size, clr, tooltips):
    ObjectDelete(chartid, name)
    ObjectCreate(chartid, name, type_, 0, time, prc)
    ObjectSetString(chartid, name, OBJPROP_TEXT, text)
    ObjectSetString(chartid, name, OBJPROP_FONT, font_mode)
    ObjectSetInteger(chartid, name, OBJPROP_FONTSIZE, font_size)
    ObjectSetInteger(chartid, name, OBJPROP_ANCHOR, ANCHOR_CENTER)
    ObjectSetInteger(chartid, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chartid, name, OBJPROP_BACK, False)
    ObjectSetInteger(chartid, name, OBJPROP_ZORDER, 0)
    ObjectSetInteger(chartid, name, OBJPROP_HIDDEN, True)
    if ShowTooltip:
        ObjectSetString(chartid, name, OBJPROP_TOOLTIP, tooltips)
    ChartRedraw(0)

def TextTarget(chartid, name, type_, time, prc, clr, br, pips):
    ObjectDelete(chartid, name)
    ObjectCreate(chartid, name, type_, 0, time, prc)
    ObjectSetString(chartid, name, OBJPROP_TEXT, '[ ' + _str(br) + '  |  ' + DoubleToString(pips, 1) + '  |  ' + DoubleToString(Price1, Digits()) + ' ]')
    ObjectSetString(chartid, name, OBJPROP_FONT, 'Arial Unicode MS Regular')
    ObjectSetInteger(chartid, name, OBJPROP_FONTSIZE, 8)
    ObjectSetInteger(chartid, name, OBJPROP_ANCHOR, ANCHOR_LEFT)
    ObjectSetInteger(chartid, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chartid, name, OBJPROP_BACK, False)
    ObjectSetInteger(chartid, name, OBJPROP_ZORDER, 0)
    ObjectSetInteger(chartid, name, OBJPROP_HIDDEN, True)
    ChartRedraw(0)

def TFmt5(tf):
    _sw1 = tf
    if _sw1 == 0:
        return PERIOD_CURRENT
    elif _sw1 == 1:
        return PERIOD_M1
    elif _sw1 == 5:
        return PERIOD_M5
    elif _sw1 == 15:
        return PERIOD_M15
    elif _sw1 == 30:
        return PERIOD_M30
    elif _sw1 == 60:
        return PERIOD_H1
    elif _sw1 == 240:
        return PERIOD_H4
    elif _sw1 == 1440:
        return PERIOD_D1
    elif _sw1 == 10080:
        return PERIOD_W1
    elif _sw1 == 43200:
        return PERIOD_MN1
    else:
        return PERIOD_CURRENT

def FillArraysBuffers(period, amount):
    ResetLastError()
    timeframe = TFmt5(period)
    if CopyOpen(Symbol(), timeframe, 0, amount, OPEN) < 1:
        PrintFormat('Failed to copy data OPEN Price, error code %d', GetLastError())
        return False
    if CopyHigh(Symbol(), timeframe, 0, amount, HIGH) < 1:
        PrintFormat('Failed to copy data HIGH Price, error code %d', GetLastError())
        return False
    if CopyLow(Symbol(), timeframe, 0, amount, LOW) < 1:
        PrintFormat('Failed to copy data LOW Price, error code %d', GetLastError())
        return False
    if CopyClose(Symbol(), timeframe, 0, amount, CLOSE) < 1:
        PrintFormat('Failed to copy data CLOSE Price, error code %d', GetLastError())
        return False
    if CopyTime(Symbol(), timeframe, 0, amount, TIME) < 1:
        PrintFormat('Failed to copy data TIME, error code %d', GetLastError())
        return False
    if CopyTickVolume(Symbol(), timeframe, 0, amount, VOLUME) < 1:
        PrintFormat('Failed to copy data TickVolume, error code %d', GetLastError())
        return False
    return True

# ---- static local variables
_s_OnChartEvent_keyPressed = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ICrosshairClickTarget(_MQL5Indicator):
    name = 'iCrosshairClickTarget'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Line style
        'LineWidth': 1,  # Line width
        'ShowTooltip': True,  # Show Tooltip or Not
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

