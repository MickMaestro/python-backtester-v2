"""dinapolitargets — converted from MQL5: MQL5 Indicators/DinapoliTargets/dinapolitargets.mq5

Copyright: mishanya; Link: mishanya_fx@yahoo.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mishanya', 'link': 'mishanya_fx@yahoo.com', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'DinapoliTargets'}, 'levels': [], 'description': [], 'name': 'dinapolitargets', 'source': 'MQL5 Indicators/DinapoliTargets/dinapolitargets.mq5', 'folder': 'DinapoliTargets', 'inputs': [{'mql': 'barn', 'py': 'barn', 'param': 'barn', 'type': 'int', 'default': 300, 'label': '', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DarkOrchid = 0xCC3299  # MQL4 colour name
Green = 0x008000  # MQL4 colour name
Honeydew = 0xF0FFF0  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name

# ---- inputs and global variables
barn = _input('barn', 300)
Length = _input('Length', 6)
ExtMapBuffer = Arr(0, 0.0)
Name = Arr.of(['Start Line', 'Stop line', 'Target1 Line', 'Target2 Line', 'Target3 Line'], fill="", dyn=False, size=5)
Price = Arr(5, 0.0, dyn=False)

def OnInit():
    SetIndexBuffer(0, ExtMapBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetString(0, PLOT_LABEL, 'DinapoliTargets(' + _str(Length) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnDeinit(reason):
    for i in range(0, 5):
        ObjectDelete(0, Name[i])
    return

def OnCalculate(rates_total, prev_calculated, Time, open, High, Low, close, tick_volume, volume, spread):
    if rates_total < barn:
        return 0
    if prev_calculated == 0:
        ArrayInitialize(ExtMapBuffer, 0.0)
    Time0 = 0
    shift = 0
    Swing = 0
    Swing_n = 0
    uzl = 0
    i = 0
    zu = 0
    zd = 0
    PointA = 0.0
    PointB = 0.0
    PointC = 0.0
    LL = 0.0
    HH = 0.0
    BH = 0.0
    BL = 0.0
    Spread = 0.0
    Uzel = Arr(10000, 0.0, dyn=False)
    Swing_n = 0
    Swing = 0
    uzl = 0
    i = rates_total - barn - 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, i)
    BH = High[i]
    BL = Low[i]
    zu = i
    zd = i
    shift = i
    for shift in range(shift, rates_total):
        LL = 10000000.0
        HH = -100000000.0
        i = shift - Length
        for i in range(i, shift):
            if Low[i] < LL:
                LL = Low[i]
            if High[i] > HH:
                HH = High[i]
        else:
            i = _range_end(i, shift, 1)
        if Low[shift] < LL and High[shift] > HH:
            Swing = 2
            if Swing_n == 1:
                zu = shift - 1
            if Swing_n == -1:
                zd = shift - 1
        else:
            if Low[shift] < LL:
                Swing = -1
            if High[shift] > HH:
                Swing = 1
        if Swing != Swing_n and Swing_n != 0:
            if Swing == 2:
                Swing = -Swing_n
                BH = High[shift]
                BL = Low[shift]
            uzl += 1
            if Swing == 1:
                Uzel[uzl] = BL
                ExtMapBuffer[zd] = BL
            if Swing == -1:
                Uzel[uzl] = BH
                ExtMapBuffer[zu] = BH
            BH = High[shift]
            BL = Low[shift]
        if Swing == 1:
            if High[shift] >= BH:
                BH = High[shift]
                zu = shift
        if Swing == -1:
            if Low[shift] <= BL:
                BL = Low[shift]
                zd = shift
        Swing_n = Swing
    else:
        shift = _range_end(shift, rates_total, 1)
    PointA = Uzel[uzl - 2]
    PointB = Uzel[uzl - 1]
    PointC = Uzel[uzl]
    Comment(PointA, ' ', PointB, ' ', PointC)
    Price[2] = NormalizeDouble(((PointB - PointA) * 0.618) + PointC, Digits())
    Price[3] = PointB - PointA + PointC
    Price[4] = NormalizeDouble(((PointB - PointA) * 1.618) + PointC, Digits())
    Spread = SymbolInfoInteger(Symbol(), SYMBOL_SPREAD) * Point()
    if PointB < PointC:
        Price[0] = NormalizeDouble(((PointB - PointA) * 0.318) + PointC, Digits()) - Spread
        Price[1] = PointC + (2 * Spread)
    if PointB > PointC:
        Price[0] = NormalizeDouble(((PointB - PointA) * 0.318) + PointC, Digits()) + Spread
        Price[1] = PointC - (2 * Spread)
    Time0 = Time[rates_total - 1]
    i = 0
    for i in range(i, 5):
        if ObjectFind(0, Name[i]) != 0:
            ObjectCreate(0, Name[i], OBJ_HLINE, 0, Time0, Price[i])
            ObjectSetInteger(0, Name[i], OBJPROP_COLOR, Color[i])
            ObjectSetInteger(0, Name[i], OBJPROP_WIDTH, 1)
            ObjectSetInteger(0, Name[i], OBJPROP_STYLE, STYLE_DOT)
        else:
            ObjectMove(0, Name[i], 0, Time0, Price[i])
    else:
        i = _range_end(i, 5, 1)
    ChartRedraw()
    return rates_total

# ---- global variables initialised from expressions
Color = Arr.of([_uint(Honeydew), _uint(Red), _uint(Green), _uint(Yellow), _uint(DarkOrchid)], fill=0, dyn=False, size=5)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dinapolitargets(_MQL5Indicator):
    name = 'dinapolitargets'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'barn': 300,
        'Length': 6,
    }

