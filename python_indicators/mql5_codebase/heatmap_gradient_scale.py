"""Heatmap_Gradient_Scale — converted from MQL5: MQL5 Indicators/Heatmaps, color gradients and scales in MQL5/Heatmap_Gradient_Scale.mq5

Copyright: Copyright 2014, Rodrigo Malacarne / Alain Verleyen; Link: www.deltatrader.com.br; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014, Rodrigo Malacarne / Alain Verleyen', 'link': 'www.deltatrader.com.br', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Heatmap_Gradient_Scale', 'source': 'MQL5 Indicators/Heatmaps, color gradients and scales in MQL5/Heatmap_Gradient_Scale.mq5', 'folder': 'Heatmaps, color gradients and scales in MQL5', 'inputs': [{'mql': 'indicatorSettings', 'py': 'indicatorSettings', 'param': None, 'type': 'string', 'default': '----- Indicator Settings', 'label': '■ Indicator Management', 'sinput': False}, {'mql': 'indicatorType', 'py': 'indicatorType', 'param': 'indicatorType', 'type': 'int', 'default': 2, 'label': 'Indicator Type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_SCALE_TYPE
DYNAMIC = 0
FIXED = 1
_enum('ENUM_SCALE_TYPE', {0: 'DYNAMIC', 1: 'FIXED'})

# enum ENUM_INDICATOR_TYPE
SCALE = 0
GRADIENT = 1
HEATMAP = 2
_enum('ENUM_INDICATOR_TYPE', {0: 'SCALE', 1: 'GRADIENT', 2: 'HEATMAP'})

# ---- inputs and global variables
indicatorSettings = _input('indicatorSettings', '----- Indicator Settings')  # ■ Indicator Management
indicatorType = _input('indicatorType', HEATMAP)  # Indicator Type
marketWatchSymbolsList = Arr(0, "")
percentChange = Arr(0, 0.0)
colorArray = Arr(0, 0)
symbolsTotal = 0

def OnInit():
    if SymbolsTotal(True) < 5:
        Alert('The minimum number of symbols must be 5 (five).')
        return INIT_PARAMETERS_INCORRECT
    EventSetTimer(1)
    ArraySetAsSeries(DailyBar, True)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    deleteScale(symbolsTotal)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tickVolume, volume, spread):
    return rates_total

def OnTimer():
    global symbolsTotal
    currentSymbolsTotal = SymbolsTotal(True)
    if symbolsTotal != currentSymbolsTotal:
        ArrayResize(marketWatchSymbolsList, currentSymbolsTotal)
        ArrayResize(percentChange, currentSymbolsTotal)
        ArrayResize(colorArray, currentSymbolsTotal)
        for i in range(0, currentSymbolsTotal):
            marketWatchSymbolsList[i] = SymbolName(i, True)
        deleteScale(symbolsTotal, currentSymbolsTotal)
        symbolsTotal = currentSymbolsTotal
    _sw1 = indicatorType
    if _sw1 == SCALE:
        Scale()
    elif _sw1 == GRADIENT:
        Gradient()
    elif _sw1 == HEATMAP:
        Heatmap()
    ChartRedraw()

def Scale():
    length = SymbolsTotal(True)
    for i in range(0, length):
        if CopyRates(marketWatchSymbolsList[i], PERIOD_D1, 0, 2, DailyBar) != 2:
            printf('Not all data available yet (%s) !', marketWatchSymbolsList[i])
            return
        r_1 = 0
        g_1 = 64
        b_1 = 255
        r_2 = 255
        g_2 = 255
        b_2 = 255
        r_value = r_1 - (i * _idiv(r_1 - r_2, length - 1))
        g_value = g_1 - (i * _idiv(g_1 - g_2, length - 1))
        b_value = b_1 - (i * _idiv(b_1 - b_2, length - 1))
        rgbColor = IntegerToString(r_value) + ',' + IntegerToString(g_value) + ',' + IntegerToString(b_value)
        colorArray[i] = StringToColor(rgbColor)
        marketWatchSymbolsList[i] = SymbolName(i, True)
        percentChange[i] = (_fdiv(DailyBar[0].close, DailyBar[1].close) - 1) * 100
        SetPanel('Panel ' + IntegerToString(i), 0, 10, 32 + (i * 32), 50, 30, StringToColor(rgbColor), clrWhite, 1)
        SetText('Text ' + IntegerToString(i), marketWatchSymbolsList[i], 13, 33 + (i * 32), clrBlack, 8)
        if percentChange[i] >= 0:
            SetText('Variation ' + IntegerToString(i), '+' + DoubleToString(percentChange[i], 2) + '%', 17, 46 + (i * 32), clrBlack, 8)
        else:
            SetText('Variation ' + IntegerToString(i), DoubleToString(percentChange[i], 2) + '%', 17, 46 + (i * 32), clrBlack, 8)

def Gradient():
    arrayMax = 0
    arrayMin = 0
    scaleEdge = 0.0
    scaleMax = 0.0
    scaleMin = 0.0
    r_1 = 255
    g_1 = 0
    b_1 = 0
    r_2 = 0
    g_2 = 255
    b_2 = 0
    for i in range(0, symbolsTotal):
        marketWatchSymbolsList[i] = SymbolName(i, True)
        if CopyRates(marketWatchSymbolsList[i], PERIOD_D1, 0, 2, DailyBar) != 2:
            printf('Not all data available yet (%s) !', marketWatchSymbolsList[i])
            return
        percentChange[i] = (_fdiv(DailyBar[0].close, DailyBar[1].close) - 1) * 100
        r_value = r_1 - (i * _idiv(r_1 - r_2, symbolsTotal - 1))
        g_value = g_1 - (i * _idiv(g_1 - g_2, symbolsTotal - 1))
        b_value = b_1 - (i * _idiv(b_1 - b_2, symbolsTotal - 1))
        rgbColor = IntegerToString(r_value) + ',' + IntegerToString(g_value) + ',' + IntegerToString(b_value)
        colorArray[i] = StringToColor(rgbColor)
    i = 0
    while i < symbolsTotal:
        arrayMax = ArrayMaximum(percentChange)
        arrayMin = ArrayMinimum(percentChange)
        if MathAbs(percentChange[arrayMax]) > MathAbs(percentChange[arrayMin]):
            scaleEdge = percentChange[arrayMax]
        else:
            scaleEdge = percentChange[arrayMin]
        scaleMax = scaleEdge
        scaleMin = -scaleEdge
        gradientColor = 0
        gradientColor = _int(MathFloor(_fdiv(scaleMax - percentChange[i], scaleMax - scaleMin) * (symbolsTotal - 1)))
        SetPanel('Panel ' + IntegerToString(i), 0, 10, 32 + (i * 32), 50, 30, colorArray[gradientColor], clrWhite, 1)
        SetText('Text ' + IntegerToString(i), marketWatchSymbolsList[i], 13, 33 + (i * 32), clrBlack, 8)
        if percentChange[i] >= 0:
            SetText('Variation ' + IntegerToString(i), '+' + DoubleToString(percentChange[i], 2) + '%', 17, 46 + (i * 32), clrBlack, 8)
        else:
            SetText('Variation ' + IntegerToString(i), DoubleToString(percentChange[i], 2) + '%', 17, 46 + (i * 32), clrBlack, 8)
        i += 1

def Heatmap():
    scaleMax = 0.0
    scaleMin = 0.0
    scaleEdge = 0.0
    arrayMax = 0
    arrayMin = 0
    r_1 = 0
    g_1 = 255
    b_1 = 0
    r_2 = 255
    g_2 = 255
    b_2 = 255
    r_3 = 255
    g_3 = 0
    b_3 = 0
    midValue = (_idiv(symbolsTotal, 2) if (_imod(symbolsTotal, 2) == 0) else _idiv(symbolsTotal - 1, 2)) - 1
    for i in range(0, symbolsTotal):
        r_value = r_2
        g_value = g_2
        b_value = b_2
        if CopyRates(marketWatchSymbolsList[i], PERIOD_D1, 0, 2, DailyBar) == 2:
            percentChange[i] = (_fdiv(DailyBar[0].close, DailyBar[1].close) - 1) * 100
            if i <= midValue:
                r_value = r_1 - _idiv(i * (r_1 - r_2), midValue)
                g_value = g_1 - _idiv(i * (g_1 - g_2), midValue)
                b_value = b_1 - _idiv(i * (b_1 - b_2), midValue)
            else:
                r_value = r_2 - _idiv((i - midValue - 1) * (r_2 - r_3), midValue)
                g_value = g_2 - _idiv((i - midValue - 1) * (g_2 - g_3), midValue)
                b_value = b_2 - _idiv((i - midValue - 1) * (b_2 - b_3), midValue)
        rgbColor = IntegerToString(r_value) + ',' + IntegerToString(g_value) + ',' + IntegerToString(b_value)
        colorArray[i] = StringToColor(rgbColor)
    arrayMax = ArrayMaximum(percentChange)
    arrayMin = ArrayMinimum(percentChange)
    if arrayMax == -1 or arrayMin == -1:
        return
    scaleEdge = MathMax(MathAbs(percentChange[arrayMax]), MathAbs(percentChange[arrayMin]))
    scaleMax = scaleEdge
    scaleMin = -scaleEdge
    midValue = (_idiv(symbolsTotal, 2) if (_imod(symbolsTotal, 2) == 0) else _idiv(symbolsTotal - 1, 2))
    i = 0
    while i < symbolsTotal:
        heatmapColor = 0
        if percentChange[i] > 0:
            heatmapColor = _int(MathFloor((1 - _fdiv(percentChange[i], scaleMax)) * midValue))
        elif percentChange[i] < 0:
            heatmapColor = _int(MathCeil(_fdiv(percentChange[i], scaleMin) * midValue)) + midValue - 1
        else:
            heatmapColor = midValue
        if heatmapColor < 0:
            Print('Array out of range, heatmapcolor=', heatmapColor)
        if heatmapColor >= ArraySize(colorArray):
            Print('Array out of range, heatmapcolor=', heatmapColor, ' colorArray size=', ArraySize(colorArray))
        SetPanel('Panel ' + IntegerToString(i), 0, 10, 32 + (i * 32), 50, 30, colorArray[heatmapColor], clrWhite, 1)
        SetText('Text ' + IntegerToString(i), marketWatchSymbolsList[i], 13, 33 + (i * 32), clrBlack, 8)
        if percentChange[i] >= 0:
            SetText('Variation ' + IntegerToString(i), '+' + DoubleToString(percentChange[i], 2) + '%', 17, 46 + (i * 32), clrBlack, 8)
        else:
            SetText('Variation ' + IntegerToString(i), DoubleToString(percentChange[i], 2) + '%', 17, 46 + (i * 32), clrBlack, 8)
        i += 1

def deleteScale(from_, to=1):
    from_ -= 1
    to -= 1
    for i in range(from_, to - 1, -1):
        ObjectDelete(0, 'Panel ' + IntegerToString(i))
        ObjectDelete(0, 'Text ' + IntegerToString(i))
        ObjectDelete(0, 'Variation ' + IntegerToString(i))

def SetText(name, text, x, y, colour, fontsize=12):
    if ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0):
        ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x)
        ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y)
        ObjectSetInteger(0, name, OBJPROP_COLOR, colour)
        ObjectSetInteger(0, name, OBJPROP_FONTSIZE, fontsize)
        ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_UPPER)
    ObjectSetString(0, name, OBJPROP_TEXT, text)

def SetPanel(name, sub_window, x, y, width, height, bg_color, border_clr, border_width):
    if ObjectCreate(0, name, OBJ_RECTANGLE_LABEL, sub_window, 0, 0):
        ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x)
        ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y)
        ObjectSetInteger(0, name, OBJPROP_XSIZE, width)
        ObjectSetInteger(0, name, OBJPROP_YSIZE, height)
        ObjectSetInteger(0, name, OBJPROP_COLOR, border_clr)
        ObjectSetInteger(0, name, OBJPROP_BORDER_TYPE, BORDER_FLAT)
        ObjectSetInteger(0, name, OBJPROP_WIDTH, border_width)
        ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID)
        ObjectSetInteger(0, name, OBJPROP_BACK, False)
        ObjectSetInteger(0, name, OBJPROP_SELECTABLE, 0)
        ObjectSetInteger(0, name, OBJPROP_SELECTED, 0)
        ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
        ObjectSetInteger(0, name, OBJPROP_ZORDER, 0)
    ObjectSetInteger(0, name, OBJPROP_BGCOLOR, bg_color)

# ---- global variables initialised from expressions
DailyBar = Arr(0, 0, factory=MqlRates)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HeatmapGradientScale(_MQL5Indicator):
    name = 'Heatmap_Gradient_Scale'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'indicatorType': _Choice({0: 'SCALE', 1: 'GRADIENT', 2: 'HEATMAP'}, default=2),  # Indicator Type
    }

