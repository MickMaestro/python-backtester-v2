"""camarilla_full — converted from MQL5: MQL5 Indicators/Camarilla_Full/camarilla_full.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 10}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5}, 'colors': {1: [32768], 2: [5197615], 3: [65280], 4: [32768], 5: [5197615], 6: [8388736], 7: [3937500], 8: [255], 9: [3937500], 10: [2763429]}, 'widths': {1: 1, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 2, 10: 1}, 'styles': {}, 'labels': {1: 'Camarilla H5', 2: 'Camarilla H4', 3: 'Camarilla H3', 4: 'Camarilla H2', 5: 'Camarilla H1', 6: 'Camarilla L1', 7: 'Camarilla L2', 8: 'Camarilla L3', 9: 'Camarilla 4', 10: 'Camarilla L5'}, 'levels': [], 'description': [], 'name': 'camarilla_full', 'source': 'MQL5 Indicators/Camarilla_Full/camarilla_full.mq5', 'folder': 'Camarilla_Full', 'inputs': [{'mql': 'CPeriod', 'py': 'CPeriod', 'param': 'CPeriod', 'type': 'int', 'default': 16408, 'label': '', 'sinput': False}, {'mql': 'Symbol_H5', 'py': 'Symbol_H5', 'param': 'Symbol_H5', 'type': 'int', 'default': 119, 'label': 'H5 level label', 'sinput': False}, {'mql': 'Symbol_H4', 'py': 'Symbol_H4', 'param': 'Symbol_H4', 'type': 'int', 'default': 167, 'label': 'H4 level label', 'sinput': False}, {'mql': 'Symbol_H3', 'py': 'Symbol_H3', 'param': 'Symbol_H3', 'type': 'int', 'default': 108, 'label': 'H3 level label', 'sinput': False}, {'mql': 'Symbol_H2', 'py': 'Symbol_H2', 'param': 'Symbol_H2', 'type': 'int', 'default': 158, 'label': 'H2 level label', 'sinput': False}, {'mql': 'Symbol_H1', 'py': 'Symbol_H1', 'param': 'Symbol_H1', 'type': 'int', 'default': 158, 'label': 'H1 level label', 'sinput': False}, {'mql': 'Symbol_L1', 'py': 'Symbol_L1', 'param': 'Symbol_L1', 'type': 'int', 'default': 158, 'label': 'L1 level label', 'sinput': False}, {'mql': 'Symbol_L2', 'py': 'Symbol_L2', 'param': 'Symbol_L2', 'type': 'int', 'default': 158, 'label': 'L2 level label', 'sinput': False}, {'mql': 'Symbol_L3', 'py': 'Symbol_L3', 'param': 'Symbol_L3', 'type': 'int', 'default': 108, 'label': 'L3 level label', 'sinput': False}, {'mql': 'Symbol_L4', 'py': 'Symbol_L4', 'param': 'Symbol_L4', 'type': 'int', 'default': 167, 'label': 'L4 level label', 'sinput': False}, {'mql': 'Symbol_L5', 'py': 'Symbol_L5', 'param': 'Symbol_L5', 'type': 'int', 'default': 119, 'label': 'L5 level label', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum STYLE
STYLE_SOLID_ = 0
STYLE_DASH_ = 1
STYLE_DOT_ = 2
STYLE_DASHDOT_ = 3
STYLE_DASHDOTDOT_ = 4
_enum('STYLE', {0: 'STYLE_SOLID_', 1: 'STYLE_DASH_', 2: 'STYLE_DOT_', 3: 'STYLE_DASHDOT_', 4: 'STYLE_DASHDOTDOT_'})

# ---- inputs and global variables
CPeriod = _input('CPeriod', PERIOD_D1)
Symbol_H5 = _input('Symbol_H5', 119)  # H5 level label
Symbol_H4 = _input('Symbol_H4', 167)  # H4 level label
Symbol_H3 = _input('Symbol_H3', 108)  # H3 level label
Symbol_H2 = _input('Symbol_H2', 158)  # H2 level label
Symbol_H1 = _input('Symbol_H1', 158)  # H1 level label
Symbol_L1 = _input('Symbol_L1', 158)  # L1 level label
Symbol_L2 = _input('Symbol_L2', 158)  # L2 level label
Symbol_L3 = _input('Symbol_L3', 108)  # L3 level label
Symbol_L4 = _input('Symbol_L4', 167)  # L4 level label
Symbol_L5 = _input('Symbol_L5', 119)  # L5 level label
H1_Buffer = Arr(0, 0.0)
H2_Buffer = Arr(0, 0.0)
H3_Buffer = Arr(0, 0.0)
H4_Buffer = Arr(0, 0.0)
H5_Buffer = Arr(0, 0.0)
L1_Buffer = Arr(0, 0.0)
L2_Buffer = Arr(0, 0.0)
L3_Buffer = Arr(0, 0.0)
L4_Buffer = Arr(0, 0.0)
L5_Buffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, H5_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, H4_Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, H3_Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, H2_Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, H1_Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, L1_Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, L2_Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, L3_Buffer, INDICATOR_DATA)
    SetIndexBuffer(8, L4_Buffer, INDICATOR_DATA)
    SetIndexBuffer(9, L5_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, Symbol_H5)
    PlotIndexSetInteger(1, PLOT_ARROW, Symbol_H4)
    PlotIndexSetInteger(2, PLOT_ARROW, Symbol_H3)
    PlotIndexSetInteger(3, PLOT_ARROW, Symbol_H2)
    PlotIndexSetInteger(4, PLOT_ARROW, Symbol_H1)
    PlotIndexSetInteger(5, PLOT_ARROW, Symbol_L1)
    PlotIndexSetInteger(6, PLOT_ARROW, Symbol_L2)
    PlotIndexSetInteger(7, PLOT_ARROW, Symbol_L3)
    PlotIndexSetInteger(8, PLOT_ARROW, Symbol_L4)
    PlotIndexSetInteger(9, PLOT_ARROW, Symbol_L5)
    iii = 0
    while iii > 5:
        PlotIndexSetString(iii, PLOT_LABEL, 'Camarilla ' + 'L' + _str(iii + 1))
        PlotIndexSetDouble(iii, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        iii += 1
    iii = 5
    while iii > 10:
        PlotIndexSetString(iii, PLOT_LABEL, 'Camarilla ' + 'H' + _str(iii + 1))
        PlotIndexSetDouble(iii, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        iii += 1
    IndicatorSetString(INDICATOR_SHORTNAME, 'Camarilla Equation')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Period() >= CPeriod:
        Print('The chart period is more than necessary!!!')
        return 0
    if rates_total < 1:
        return 0
    first = 0
    iClose_ = Arr(0, 0.0)
    iHigh_ = Arr(0, 0.0)
    iLow_ = Arr(0, 0.0)
    Level_H1 = 0.0
    Level_H2 = 0.0
    Level_H3 = 0.0
    Level_H4 = 0.0
    Level_H5 = 0.0
    Level_L1 = 0.0
    Level_L2 = 0.0
    Level_L3 = 0.0
    Level_L4 = 0.0
    Level_L5 = 0.0
    if prev_calculated == 0:
        first = 0
    else:
        first = prev_calculated - 1
    for bar in range(first, rates_total):
        if CopyClose(None, CPeriod, _DT(time[bar]), 2, iClose_) < 1:
            return 0
        if CopyHigh(None, CPeriod, _DT(time[bar]), 2, iHigh_) < 1:
            return 0
        if CopyLow(None, CPeriod, _DT(time[bar]), 2, iLow_) < 1:
            return 0
        Level_H1 = iClose_[0] + (((iHigh_[0] - iLow_[0]) * 1.1) / 12)
        Level_H2 = iClose_[0] + (((iHigh_[0] - iLow_[0]) * 1.1) / 6)
        Level_H3 = iClose_[0] + (((iHigh_[0] - iLow_[0]) * 1.1) / 4)
        Level_H4 = iClose_[0] + (((iHigh_[0] - iLow_[0]) * 1.1) / 2)
        Level_H5 = _fdiv(iHigh_[0], iLow_[0]) * iClose_[0]
        Level_L1 = iClose_[0] - (((iHigh_[0] - iLow_[0]) * 1.1) / 12)
        Level_L2 = iClose_[0] - (((iHigh_[0] - iLow_[0]) * 1.1) / 6)
        Level_L3 = iClose_[0] - (((iHigh_[0] - iLow_[0]) * 1.1) / 4)
        Level_L4 = iClose_[0] - (((iHigh_[0] - iLow_[0]) * 1.1) / 2)
        Level_L5 = iClose_[0] - (Level_H5 - iClose_[0])
        H1_Buffer[bar] = Level_H1
        H2_Buffer[bar] = Level_H2
        H3_Buffer[bar] = Level_H3
        H4_Buffer[bar] = Level_H4
        H5_Buffer[bar] = Level_H5
        L1_Buffer[bar] = Level_L1
        L2_Buffer[bar] = Level_L2
        L3_Buffer[bar] = Level_L3
        L4_Buffer[bar] = Level_L4
        L5_Buffer[bar] = Level_L5
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CamarillaFull(_MQL5Indicator):
    name = 'camarilla_full'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CPeriod': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),
        'Symbol_H5': 119,  # H5 level label
        'Symbol_H4': 167,  # H4 level label
        'Symbol_H3': 108,  # H3 level label
        'Symbol_H2': 158,  # H2 level label
        'Symbol_H1': 158,  # H1 level label
        'Symbol_L1': 158,  # L1 level label
        'Symbol_L2': 158,  # L2 level label
        'Symbol_L3': 108,  # L3 level label
        'Symbol_L4': 167,  # L4 level label
        'Symbol_L5': 119,  # L5 level label
    }

