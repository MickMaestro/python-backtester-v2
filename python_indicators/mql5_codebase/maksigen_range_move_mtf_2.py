"""maksigen_range_move_mtf_2 — converted from MQL5: MQL5 Indicators/MaksiGen_Range_Move MTF/maksigen_range_move_mtf_2.mq5

Copyright: MaksiGen - MT3 by OlegVS ( olegvs2003@yahoo.com )

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'MaksiGen - MT3 by OlegVS ( olegvs2003@yahoo.com )', 'link': '', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'maksigen_range_move_mtf_2', 'source': 'MQL5 Indicators/MaksiGen_Range_Move MTF/maksigen_range_move_mtf_2.mq5', 'folder': 'MaksiGen_Range_Move MTF', 'inputs': [{'mql': 'Pfast', 'py': 'Pfast', 'param': 'Pfast', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Pslow', 'py': 'Pslow', 'param': 'Pslow', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'K_RangeOpen', 'py': 'K_RangeOpen', 'param': 'K_RangeOpen', 'type': 'double', 'default': 1.4, 'label': '', 'sinput': False}, {'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UniqueID', 'py': 'UniqueID', 'param': None, 'type': 'string', 'default': 'MaksiGen1', 'label': '', 'sinput': False}, {'mql': 'HiColor1', 'py': 'HiColor1', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LoColor1', 'py': 'LoColor1', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'HiColor2', 'py': 'HiColor2', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LoColor2', 'py': 'LoColor2', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Bar1Color', 'py': 'Bar1Color', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'BarFastColor', 'py': 'BarFastColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'BarSlowColor', 'py': 'BarSlowColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'TrendHighColor', 'py': 'TrendHighColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'TrendLowColor', 'py': 'TrendLowColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'SellStopColor', 'py': 'SellStopColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'BuyStopColor', 'py': 'BuyStopColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Gold = 0x00D7FF  # MQL4 colour name
LightSkyBlue = 0xFACE87  # MQL4 colour name
OliveDrab = 0x238E6B  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
Silver = 0xC0C0C0  # MQL4 colour name

# ---- inputs and global variables
Pfast = _input('Pfast', 5)
Pslow = _input('Pslow', 8)
K_RangeOpen = _input('K_RangeOpen', 1.4)
TimeFrame = _input('TimeFrame', 0)
UniqueID = _input('UniqueID', 'MaksiGen1')
tf = 0
hi1 = 0.0
lo1 = 0.0
hi2 = 0.0
lo2 = 0.0
Range = 0.0

def OnInit():
    global tf
    if TimeFrame <= Period():
        tf = Period()
    else:
        tf = TimeFrame
    ObjectCreate(0, UniqueID + 'hi1', OBJ_HLINE, 0, 0, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, UniqueID + 'hi1', OBJPROP_COLOR, HiColor1)
    ObjectSetInteger(0, UniqueID + 'hi1', OBJPROP_STYLE, STYLE_DOT)
    ObjectCreate(0, UniqueID + 'lo1', OBJ_HLINE, 0, 0, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, UniqueID + 'lo1', OBJPROP_COLOR, LoColor1)
    ObjectSetInteger(0, UniqueID + 'lo1', OBJPROP_STYLE, STYLE_DOT)
    ObjectCreate(0, UniqueID + 'hi2', OBJ_HLINE, 0, 0, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, UniqueID + 'hi2', OBJPROP_COLOR, HiColor2)
    ObjectSetInteger(0, UniqueID + 'hi2', OBJPROP_STYLE, STYLE_DASH)
    ObjectCreate(0, UniqueID + 'lo2', OBJ_HLINE, 0, 0, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, UniqueID + 'lo2', OBJPROP_COLOR, LoColor2)
    ObjectSetInteger(0, UniqueID + 'lo2', OBJPROP_STYLE, STYLE_DASH)
    ObjectCreate(0, UniqueID + 'Bar#1', OBJ_VLINE, 0, 0, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, UniqueID + 'Bar#1', OBJPROP_COLOR, Bar1Color)
    ObjectSetInteger(0, UniqueID + 'Bar#1', OBJPROP_STYLE, STYLE_DOT)
    ObjectCreate(0, UniqueID + 'Bar#Pfast', OBJ_VLINE, 0, 0, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, UniqueID + 'Bar#Pfast', OBJPROP_COLOR, BarFastColor)
    ObjectSetInteger(0, UniqueID + 'Bar#Pfast', OBJPROP_STYLE, STYLE_DOT)
    ObjectCreate(0, UniqueID + 'Bar#Pslow', OBJ_VLINE, 0, 0, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, UniqueID + 'Bar#Pslow', OBJPROP_COLOR, BarSlowColor)
    ObjectSetInteger(0, UniqueID + 'Bar#Pslow', OBJPROP_STYLE, STYLE_DOT)
    ObjectCreate(0, UniqueID + 'TrendHIGH', OBJ_TREND, 0, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, UniqueID + 'TrendHIGH', OBJPROP_COLOR, TrendHighColor)
    ObjectSetInteger(0, UniqueID + 'TrendHIGH', OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(0, UniqueID + 'TrendHIGH', OBJPROP_RAY_RIGHT, 1)
    ObjectCreate(0, UniqueID + 'Trend_LOW', OBJ_TREND, 0, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, UniqueID + 'Trend_LOW', OBJPROP_COLOR, TrendLowColor)
    ObjectSetInteger(0, UniqueID + 'Trend_LOW', OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(0, UniqueID + 'Trend_LOW', OBJPROP_RAY_RIGHT, 1)
    ObjectCreate(0, UniqueID + 'SELLSTOP', OBJ_HLINE, 0, 0, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, UniqueID + 'SELLSTOP', OBJPROP_COLOR, SellStopColor)
    ObjectSetInteger(0, UniqueID + 'SELLSTOP', OBJPROP_STYLE, STYLE_DOT)
    ObjectCreate(0, UniqueID + 'BUY_STOP', OBJ_HLINE, 0, 0, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, UniqueID + 'BUY_STOP', OBJPROP_COLOR, BuyStopColor)
    ObjectSetInteger(0, UniqueID + 'BUY_STOP', OBJPROP_STYLE, STYLE_DOT)

def OnDeinit(reason):
    deleteObj(UniqueID)
    return

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global Range, hi1, hi2, lo1, lo2
    copied = 0
    TimesArray = Arr(0, 0)
    HighArray = Arr(0, 0.0)
    LowArray = Arr(0, 0.0)
    ArraySetAsSeries(HighArray, True)
    copied = CopyHigh(Symbol(), tf, _DT(Time[rates_total - 1]), _DT(Time[0]), HighArray)
    if copied <= 0:
        Print('not all rates copied. Will try on next tick')
        return 0
    ArraySetAsSeries(LowArray, True)
    copied = CopyLow(Symbol(), tf, _DT(Time[rates_total - 1]), _DT(Time[0]), LowArray)
    if copied <= 0:
        Print('not all rates copied. Will try on next tick')
        return 0
    ArraySetAsSeries(TimesArray, True)
    copied = CopyTime(Symbol(), tf, _DT(Time[rates_total - 1]), _DT(Time[0]), TimesArray)
    if copied <= 0:
        Print('not all times copied. Will try on next tick')
        return 0
    hi1 = Highest(HighArray, Pfast, 1)
    lo1 = Lowest(LowArray, Pfast, 1)
    hi2 = Highest(HighArray, Pslow, 1)
    lo2 = Lowest(LowArray, Pslow, 1)
    ObjectMove(0, UniqueID + 'hi1', 0, Time[Pfast - 1], hi1)
    ObjectMove(0, UniqueID + 'lo1', 0, Time[Pfast - 1], lo1)
    ObjectMove(0, UniqueID + 'hi2', 0, Time[Pslow - 1], hi2)
    ObjectMove(0, UniqueID + 'lo2', 0, Time[Pslow - 1], lo2)
    ObjectMove(0, UniqueID + 'Bar#1', 0, TimesArray[1], HighArray[1])
    ObjectMove(0, UniqueID + 'Bar#Pfast', 0, TimesArray[Pfast], HighArray[1])
    ObjectMove(0, UniqueID + 'Bar#Pslow', 0, TimesArray[Pslow], HighArray[1])
    ObjectSetInteger(0, UniqueID + 'TrendHIGH', OBJPROP_TIME, 0, TimesArray[Pslow])
    ObjectSetDouble(0, UniqueID + 'TrendHIGH', OBJPROP_PRICE, 0, hi2)
    ObjectSetInteger(0, UniqueID + 'TrendHIGH', OBJPROP_TIME, 1, TimesArray[Pfast])
    ObjectSetDouble(0, UniqueID + 'TrendHIGH', OBJPROP_PRICE, 1, hi1)
    ObjectSetInteger(0, UniqueID + 'Trend_LOW', OBJPROP_TIME, 0, TimesArray[Pslow])
    ObjectSetDouble(0, UniqueID + 'Trend_LOW', OBJPROP_PRICE, 0, lo2)
    ObjectSetInteger(0, UniqueID + 'Trend_LOW', OBJPROP_TIME, 1, TimesArray[Pfast])
    ObjectSetDouble(0, UniqueID + 'Trend_LOW', OBJPROP_PRICE, 1, lo1)
    if (hi1 - lo1) == (hi2 - lo2):
        Range = (hi1 - lo1) * K_RangeOpen
        ObjectMove(0, UniqueID + 'SELLSTOP', 0, TimesArray[Pfast - 1], lo1 - Range)
        ObjectMove(0, UniqueID + 'BUY_STOP', 0, TimesArray[Pfast - 1], hi1 + Range)
        ObjectSetInteger(0, UniqueID + 'TrendHIGH', OBJPROP_TIME, 0, TimesArray[Pslow - 1])
        ObjectSetDouble(0, UniqueID + 'TrendHIGH', OBJPROP_PRICE, 0, hi2)
        ObjectSetInteger(0, UniqueID + 'TrendHIGH', OBJPROP_TIME, 1, TimesArray[Pfast - 1])
        ObjectSetDouble(0, UniqueID + 'TrendHIGH', OBJPROP_PRICE, 1, hi1)
        ObjectSetInteger(0, UniqueID + 'Trend_LOW', OBJPROP_TIME, 0, TimesArray[Pslow] - 1)
        ObjectSetDouble(0, UniqueID + 'Trend_LOW', OBJPROP_PRICE, 0, lo2)
        ObjectSetInteger(0, UniqueID + 'Trend_LOW', OBJPROP_TIME, 1, TimesArray[Pfast] - 1)
        ObjectSetDouble(0, UniqueID + 'Trend_LOW', OBJPROP_PRICE, 1, lo1)
    ChartRedraw()
    return rates_total

def Highest(array, range_, fromIndex):
    res = 0.0
    res = array[fromIndex]
    for i in range(fromIndex, fromIndex + range_):
        if res < array[i]:
            res = array[i]
    return res

def Lowest(array, range_, fromIndex):
    res = 0.0
    res = array[fromIndex]
    for i in range(fromIndex, fromIndex + range_):
        if res > array[i]:
            res = array[i]
    return res

def deleteObj(prefix):
    name = ''
    total = ObjectsTotal(0) - 1
    for i in range(total, 0 - 1, -1):
        name = ObjectName(0, i)
        if StringFind(name, prefix) >= 0:
            ObjectDelete(0, name)

# ---- global variables initialised from expressions
HiColor1 = _input('HiColor1', _uint(Silver))
LoColor1 = _input('LoColor1', _uint(Silver))
HiColor2 = _input('HiColor2', _uint(Silver))
LoColor2 = _input('LoColor2', _uint(Silver))
Bar1Color = _input('Bar1Color', _uint(OliveDrab))
BarFastColor = _input('BarFastColor', _uint(LightSkyBlue))
BarSlowColor = _input('BarSlowColor', _uint(Blue))
TrendHighColor = _input('TrendHighColor', _uint(Gold))
TrendLowColor = _input('TrendLowColor', _uint(Gold))
SellStopColor = _input('SellStopColor', _uint(Red))
BuyStopColor = _input('BuyStopColor', _uint(Blue))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MaksigenRangeMoveMtf2(_MQL5Indicator):
    name = 'maksigen_range_move_mtf_2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Pfast': 5,
        'Pslow': 8,
        'K_RangeOpen': 1.4,
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
    }

