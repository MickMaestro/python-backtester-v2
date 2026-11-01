"""Candle GainLossInfo — converted from MQL5: MQL5 Indicators/Voitto Tappio Candle Gain Candle Loss MT5/Candle GainLossInfo.mq5

Shows percentage and point gain/loss for a candle.
Can calculate gain/loss compared either to the previous Close or to the current Open.
Copyright: Copyright 2024, Kursustrading.my.id; Link: https://belajarfx.my.id; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Kursustrading.my.id', 'link': 'https://belajarfx.my.id', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Shows percentage and point gain/loss for a candle.', 'Can calculate gain/loss compared either to the previous Close or to the current Open.'], 'name': 'Candle GainLossInfo', 'source': 'MQL5 Indicators/Voitto Tappio Candle Gain Candle Loss MT5/Candle GainLossInfo.mq5', 'folder': 'Voitto Tappio Candle Gain Candle Loss MT5', 'inputs': [{'mql': 'PercentageLimit', 'py': 'PercentageLimit', 'param': 'PercentageLimit', 'type': 'double', 'default': 1.0, 'label': 'PercentageLimit - Will not display number if percentage gain/loss is below limit.', 'sinput': False}, {'mql': 'PointsLimit', 'py': 'PointsLimit', 'param': 'PointsLimit', 'type': 'int', 'default': 1000, 'label': 'PointsLimit - Will not display number if points gain/loss is below limit.', 'sinput': False}, {'mql': 'CloseToClose', 'py': 'CloseToClose', 'param': 'CloseToClose', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'DisplayLossColor', 'py': 'DisplayLossColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'DisplayGainColor', 'py': 'DisplayGainColor', 'param': None, 'type': 'color', 'default': 3329330, 'label': '', 'sinput': False}, {'mql': 'MaxBars', 'py': 'MaxBars', 'param': 'MaxBars', 'type': 'int', 'default': 100, 'label': 'MaxBars: More bars - more objects - more lag and memory usage.', 'sinput': False}, {'mql': 'FontFace', 'py': 'FontFace', 'param': None, 'type': 'string', 'default': 'Verdana', 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'ObjectPrefix', 'py': 'ObjectPrefix', 'param': None, 'type': 'string', 'default': 'GLI-', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PercentageLimit = _input('PercentageLimit', 1.0)  # PercentageLimit - Will not display number if percentage gain/loss is below limit.
PointsLimit = _input('PointsLimit', 1000)  # PointsLimit - Will not display number if points gain/loss is below limit.
CloseToClose = _input('CloseToClose', True)
DisplayLossColor = _input('DisplayLossColor', clrRed)
DisplayGainColor = _input('DisplayGainColor', clrLimeGreen)
MaxBars = _input('MaxBars', 100)  # MaxBars: More bars - more objects - more lag and memory usage.
FontFace = _input('FontFace', 'Verdana')
FontSize = _input('FontSize', 10)
ObjectPrefix = _input('ObjectPrefix', 'GLI-')

def OnDeinit(reason):
    ObjectsDeleteAll(0, ObjectPrefix, -1, OBJ_TEXT)

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        RedrawVisibleLabels()

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    name = ""
    perc = ""
    points = ""
    index = rates_total - 1
    start = 0.0
    counted_bars = prev_calculated
    if counted_bars > 0:
        counted_bars -= 1
    limit = counted_bars
    if (rates_total - counted_bars) > MaxBars:
        limit = rates_total - MaxBars
    for i in range(rates_total - 1, limit - 1, -1):
        if CloseToClose and i > 0:
            start = Close[i - 1]
        else:
            start = Open[i]
        name = ObjectPrefix + 'Percent-' + TimeToString(Time[i], TIME_DATE | TIME_MINUTES)
        ObjectDelete(0, name)
        if (_fdiv(Close[i] - start, start) * 100) >= PercentageLimit:
            perc = DoubleToString(_fdiv(Close[i] - start, start) * 100, 1) + '%'
            ObjectCreate(0, name, OBJ_TEXT, 0, Time[i], High[i])
            ObjectSetString(0, name, OBJPROP_TEXT, perc)
            ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
            ObjectSetString(0, name, OBJPROP_FONT, FontFace)
            ObjectSetInteger(0, name, OBJPROP_COLOR, DisplayGainColor)
            visible_bars = _int(ChartGetInteger(0, CHART_VISIBLE_BARS))
            first_bar = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR))
            last_bar = first_bar - visible_bars + 1
            if i <= first_bar and i >= last_bar:
                RedrawOneLabel(i, last_bar)
            ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_UPPER)
            ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
            ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
        elif (_fdiv(start - Close[i], start) * 100) >= PercentageLimit:
            perc = DoubleToString(_fdiv(start - Close[i], start) * 100, 1) + '%'
            ObjectCreate(0, name, OBJ_TEXT, 0, Time[i], High[i])
            ObjectSetString(0, name, OBJPROP_TEXT, perc)
            ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
            ObjectSetString(0, name, OBJPROP_FONT, FontFace)
            ObjectSetInteger(0, name, OBJPROP_COLOR, DisplayLossColor)
            visible_bars = _int(ChartGetInteger(0, CHART_VISIBLE_BARS))
            first_bar = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR))
            last_bar = first_bar - visible_bars + 1
            if i <= first_bar and i >= last_bar:
                RedrawOneLabel(i, last_bar)
            ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_UPPER)
            ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
            ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
        name = ObjectPrefix + 'Points-' + TimeToString(Time[i], TIME_DATE | TIME_MINUTES)
        ObjectDelete(0, name)
        if _fdiv(Close[i] - start, Point()) >= PointsLimit:
            points = DoubleToString(_fdiv(Close[i] - start, Point()), 0)
            ObjectCreate(0, name, OBJ_TEXT, 0, Time[i], Low[i])
            ObjectSetString(0, name, OBJPROP_TEXT, points)
            ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
            ObjectSetString(0, name, OBJPROP_FONT, FontFace)
            ObjectSetInteger(0, name, OBJPROP_COLOR, DisplayGainColor)
            ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_UPPER)
            ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
            ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
        elif _fdiv(start - Close[i], Point()) >= PointsLimit:
            points = DoubleToString(_fdiv(start - Close[i], Point()), 0)
            ObjectCreate(0, name, OBJ_TEXT, 0, Time[i], Low[i])
            ObjectSetString(0, name, OBJPROP_TEXT, points)
            ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
            ObjectSetString(0, name, OBJPROP_FONT, FontFace)
            ObjectSetInteger(0, name, OBJPROP_COLOR, DisplayLossColor)
            ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_UPPER)
            ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
            ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    return rates_total

def RedrawVisibleLabels():
    visible_bars = _int(ChartGetInteger(0, CHART_VISIBLE_BARS))
    first_bar = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR))
    last_bar = first_bar - visible_bars + 1
    for i in range(first_bar, last_bar - 1, -1):
        RedrawOneLabel(i, last_bar)

def RedrawOneLabel(i, last_bar):
    x = Box(0)
    y = Box(0)
    cw = Box(0)
    w = Box(0)
    h = Box(0)
    t = Box(0)
    p = Box(0.0)
    high = 0.0
    length = ""
    name = ""
    high = iHigh(None, 0, i)
    name = GenerateObjectName('Percent-', iTime(None, Period(), i))
    if ObjectFind(0, name) == -1:
        return
    ChartTimePriceToXY(0, 0, iTime(None, Period(), last_bar), high, x, y)
    TextSetFont(FontFace, FontSize * -10)
    length = DoubleToString(MathRound(_fdiv(high - MathMax(iOpen(None, 0, i), iClose(None, 0, i)), Point())), 0)
    TextGetSize(length, w, h)
    if (y.v - _int(h.v) - 2) < 0:
        if not ChartXYToTimePrice(0, x.v, y.v + h.v + 2, cw, t, p):
            Print('Error: ', GetLastError())
        diff = high - p.v
        p.v = high + diff
    else:
        ChartXYToTimePrice(0, x.v, y.v - h.v - 2, cw, t, p)
    ObjectSetDouble(0, name, OBJPROP_PRICE, p.v)

def GenerateObjectName(prefix, time):
    return ObjectPrefix + prefix + TimeToString(time, TIME_DATE | TIME_MINUTES)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleGainLossInfo(_MQL5Indicator):
    name = 'Candle GainLossInfo'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PercentageLimit': 1.0,  # PercentageLimit - Will not display number if percentage gain/loss is below limit.
        'PointsLimit': 1000,  # PointsLimit - Will not display number if points gain/loss is below limit.
        'CloseToClose': True,
        'MaxBars': 100,  # MaxBars: More bars - more objects - more lag and memory usage.
        'FontSize': 10,
    }

