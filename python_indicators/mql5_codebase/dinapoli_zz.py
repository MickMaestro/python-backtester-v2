"""dinapoli_zz — converted from MQL5: MQL5 Indicators/Dinapoli_ZZ/dinapoli_zz.mq5

Copyright: Copyright © 2005, CrazyChart; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, CrazyChart', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [36095]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Dinapoli_ZZ'}, 'levels': [], 'description': [], 'name': 'dinapoli_zz', 'source': 'MQL5 Indicators/Dinapoli_ZZ/dinapoli_zz.mq5', 'folder': 'Dinapoli_ZZ', 'inputs': [{'mql': 'barn', 'py': 'barn', 'param': 'barn', 'type': 'uint', 'default': 300, 'label': '', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
barn = _input('barn', 300)
Length = _input('Length', 6)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ZZBuffer = Arr(0, 0.0)
min_rates_total = 0
Barn = 0

def OnInit():
    global Barn, min_rates_total
    min_rates_total = _int(Length)
    Barn = _int(barn)
    SetIndexBuffer(0, ZZBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(ZZBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Dinapoli_ZZ(', Length, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    bar = 0
    limit = 0
    Swing = 0
    Swing_n = 0
    uzl = 0
    i = 0
    zu = 0
    zd = 0
    mv = 0
    LL = 0.0
    HH = 0.0
    BH = 0.0
    BL = 0.0
    Uzel = Arr(10000, 0.0, dyn=False, dims=(3,))
    Swing_n = 0
    Swing = 0
    uzl = 0
    BH = High[barn]
    BL = Low[barn]
    zu = _int(barn)
    zd = _int(barn)
    limit = MathMin(Barn, rates_total)
    ArrayInitialize(Uzel, 0.0)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        LL = 10000000.0
        HH = -10000000.0
        i = bar + _int(Length)
        for i in range(i, bar, -1):
            if Low[i] < LL:
                LL = Low[i]
            if High[i] > HH:
                HH = High[i]
        else:
            i = _range_end(i, bar, -1)
        if Low[bar] < LL and High[bar] > HH:
            Swing = 2
            if Swing_n == 1:
                zu = bar + 1
            if Swing_n == -1:
                zd = bar + 1
        else:
            if Low[bar] < LL:
                Swing = -1
            if High[bar] > HH:
                Swing = 1
        if Swing != Swing_n and Swing_n:
            if Swing == 2:
                Swing = -Swing_n
                BH = High[bar]
                BL = Low[bar]
            uzl += 1
            if Swing == 1:
                Uzel[uzl][1] = zd
                Uzel[uzl][2] = BL
            if Swing == -1:
                Uzel[uzl][1] = zu
                Uzel[uzl][2] = BH
            BH = High[bar]
            BL = Low[bar]
        if Swing == 1 and High[bar] >= BH:
            BH = High[bar]
            zu = bar
        if Swing == -1 and Low[bar] <= BL:
            BL = Low[bar]
            zd = bar
        Swing_n = Swing
        ZZBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = 1
    for bar in range(bar, uzl + 1):
        mv = _int(StringToInteger(DoubleToString(Uzel[bar][1], 0)))
        ZZBuffer[mv] = Uzel[bar][2]
    else:
        bar = _range_end(bar, uzl + 1, 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - limit)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DinapoliZz(_MQL5Indicator):
    name = 'dinapoli_zz'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'barn': 300,
        'Length': 6,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

