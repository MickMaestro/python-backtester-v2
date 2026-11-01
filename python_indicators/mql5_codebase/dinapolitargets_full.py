"""dinapolitargets_full — converted from MQL5: MQL5 Indicators/DinapoliTargets_Full/dinapolitargets_full.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [16711935], 2: [32768], 3: [42495], 4: [13382297], 5: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {}, 'labels': {1: 'Dinapoli Start line', 2: 'Dinapoli Target1 line', 3: 'Dinapoli Target2 line', 4: 'Dinapoli Target3 line', 5: 'Dinapoli Stop line'}, 'levels': [], 'description': [], 'name': 'dinapolitargets_full', 'source': 'MQL5 Indicators/DinapoliTargets_Full/dinapolitargets_full.mq5', 'folder': 'DinapoliTargets_Full', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 6, 'label': 'period of averaging', 'sinput': False}, {'mql': 'Symbol_H0', 'py': 'Symbol_H0', 'param': 'Symbol_H0', 'type': 'int', 'default': 119, 'label': 'start level label', 'sinput': False}, {'mql': 'Symbol_H1', 'py': 'Symbol_H1', 'param': 'Symbol_H1', 'type': 'int', 'default': 119, 'label': 'level 1 label', 'sinput': False}, {'mql': 'Symbol_H2', 'py': 'Symbol_H2', 'param': 'Symbol_H2', 'type': 'int', 'default': 119, 'label': 'level 2 label', 'sinput': False}, {'mql': 'Symbol_H3', 'py': 'Symbol_H3', 'param': 'Symbol_H3', 'type': 'int', 'default': 119, 'label': 'level 3 label', 'sinput': False}, {'mql': 'Symbol_H4', 'py': 'Symbol_H4', 'param': 'Symbol_H4', 'type': 'int', 'default': 119, 'label': 'stop level label', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 1, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 6)  # period of averaging
Symbol_H0 = _input('Symbol_H0', 119)  # start level label
Symbol_H1 = _input('Symbol_H1', 119)  # level 1 label
Symbol_H2 = _input('Symbol_H2', 119)  # level 2 label
Symbol_H3 = _input('Symbol_H3', 119)  # level 3 label
Symbol_H4 = _input('Symbol_H4', 119)  # stop level label
Shift = _input('Shift', 1)  # horizontal shift of the indicator in bars
min_rates_total = 0
H0_Buffer = Arr(0, 0.0)
H1_Buffer = Arr(0, 0.0)
H2_Buffer = Arr(0, 0.0)
H3_Buffer = Arr(0, 0.0)
H4_Buffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = Length + 4
    SetIndexBuffer(0, H0_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, H1_Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, H2_Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, H3_Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, H4_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, Symbol_H0)
    PlotIndexSetInteger(1, PLOT_ARROW, Symbol_H1)
    PlotIndexSetInteger(2, PLOT_ARROW, Symbol_H2)
    PlotIndexSetInteger(3, PLOT_ARROW, Symbol_H3)
    PlotIndexSetInteger(4, PLOT_ARROW, Symbol_H4)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(H0_Buffer, True)
    ArraySetAsSeries(H1_Buffer, True)
    ArraySetAsSeries(H2_Buffer, True)
    ArraySetAsSeries(H3_Buffer, True)
    ArraySetAsSeries(H4_Buffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dinapoli Targets')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_volume, Volume, Spread):
    global _s_OnCalculate_BH, _s_OnCalculate_BL, _s_OnCalculate_Swing_n, _s_OnCalculate_Uzel0, _s_OnCalculate_Uzel1, _s_OnCalculate_Uzel2
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Spread, True)
    limit = 0
    bar = 0
    Swing = 0
    i = 0
    PointA = 0.0
    PointB = 0.0
    PointC = 0.0
    Target1 = 0.0
    Target2 = 0.0
    Target3 = 0.0
    Start = 0.0
    Stop = 0.0
    LL = 0.0
    HH = 0.0
    spread = 0.0
    dPointBA = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_Uzel0 = 0.0
        _s_OnCalculate_Uzel1 = 0.0
        _s_OnCalculate_Uzel2 = 0.0
        Swing = 0
        _s_OnCalculate_Swing_n = 0
        startbar = rates_total - min_rates_total
        _s_OnCalculate_BH = High[startbar]
        _s_OnCalculate_BL = Low[startbar]
        Start = 0.0
        Stop = 0.0
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        LL = 10000000.0
        HH = -100000000.0
        H0_Buffer[bar] = EMPTY_VALUE
        H1_Buffer[bar] = EMPTY_VALUE
        H2_Buffer[bar] = EMPTY_VALUE
        H3_Buffer[bar] = EMPTY_VALUE
        H4_Buffer[bar] = EMPTY_VALUE
        i = Length
        for i in range(i, 1 - 1, -1):
            barl = bar + i
            if Low[i] < LL:
                LL = Low[barl]
            if High[i] > HH:
                HH = High[barl]
        else:
            i = _range_end(i, 1 - 1, -1)
        if Low[bar] < LL and High[bar] > HH:
            Swing = 2
        else:
            if Low[bar] < LL:
                Swing = -1
            if High[bar] > HH:
                Swing = 1
        if Swing != _s_OnCalculate_Swing_n and _s_OnCalculate_Swing_n != 0:
            if Swing == 2:
                Swing = -_s_OnCalculate_Swing_n
                _s_OnCalculate_BH = High[bar]
                _s_OnCalculate_BL = Low[bar]
            _s_OnCalculate_Uzel2 = _s_OnCalculate_Uzel1
            _s_OnCalculate_Uzel1 = _s_OnCalculate_Uzel0
            if Swing == 1:
                _s_OnCalculate_Uzel0 = _s_OnCalculate_BL
            if Swing == -1:
                _s_OnCalculate_Uzel0 = _s_OnCalculate_BH
            _s_OnCalculate_BH = High[bar]
            _s_OnCalculate_BL = Low[bar]
        if Swing == 1 and High[bar] >= _s_OnCalculate_BH:
            _s_OnCalculate_BH = High[bar]
        if Swing == -1 and Low[bar] <= _s_OnCalculate_BL:
            _s_OnCalculate_BL = Low[bar]
        _s_OnCalculate_Swing_n = Swing
        PointA = _s_OnCalculate_Uzel2
        PointB = _s_OnCalculate_Uzel1
        PointC = _s_OnCalculate_Uzel0
        dPointBA = PointB - PointA
        Target1 = NormalizeDouble((dPointBA * 0.618) + PointC, Digits())
        Target2 = dPointBA + PointC
        Target3 = NormalizeDouble((dPointBA * 1.618) + PointC, Digits())
        spread = Spread[bar] * Point()
        if PointB <= PointC:
            Start = NormalizeDouble((dPointBA * 0.318) + PointC, Digits()) - spread
            Stop = PointC + (2 * spread)
        if PointB > PointC:
            Start = NormalizeDouble((dPointBA * 0.318) + PointC, Digits()) + spread
            Stop = PointC - (2 * spread)
        H0_Buffer[bar] = Start
        H1_Buffer[bar] = Target1
        H2_Buffer[bar] = Target2
        H3_Buffer[bar] = Target3
        H4_Buffer[bar] = Stop
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Uzel0 = 0.0
_s_OnCalculate_Uzel1 = 0.0
_s_OnCalculate_Uzel2 = 0.0
_s_OnCalculate_BH = 0.0
_s_OnCalculate_BL = 0.0
_s_OnCalculate_Swing_n = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DinapolitargetsFull(_MQL5Indicator):
    name = 'dinapolitargets_full'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Length': 6,  # period of averaging
        'Symbol_H0': 119,  # start level label
        'Symbol_H1': 119,  # level 1 label
        'Symbol_H2': 119,  # level 2 label
        'Symbol_H3': 119,  # level 3 label
        'Symbol_H4': 119,  # stop level label
        'Shift': 1,  # horizontal shift of the indicator in bars
    }

