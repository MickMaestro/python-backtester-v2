"""3_level_zz_semafor — converted from MQL5: MQL5 Indicators/3_Level_ZZ_Semafor/3_level_zz_semafor.mq5

Copyright: 2000, asystem2000; Link: asystem2000@yandex.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2000, asystem2000', 'link': 'asystem2000@yandex.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5}, 'colors': {1: [16776960], 2: [16711935], 3: [16776960], 4: [16711935], 5: [16776960], 6: [16711935]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {}, 'labels': {1: 'Low', 2: 'High', 3: 'Low', 4: 'High', 5: 'Low', 6: 'High'}, 'levels': [], 'description': [], 'name': '3_level_zz_semafor', 'source': 'MQL5 Indicators/3_Level_ZZ_Semafor/3_level_zz_semafor.mq5', 'folder': '3_Level_ZZ_Semafor', 'inputs': [{'mql': 'Period1', 'py': 'Period1', 'param': 'Period1', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Deviation1', 'py': 'Deviation1', 'param': 'Deviation1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Backstep1', 'py': 'Backstep1', 'param': 'Backstep1', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'HighSymbol1', 'py': 'HighSymbol1', 'param': 'HighSymbol1', 'type': 'int', 'default': 159, 'label': '', 'sinput': False}, {'mql': 'LowSymbol1', 'py': 'LowSymbol1', 'param': 'LowSymbol1', 'type': 'int', 'default': 159, 'label': '', 'sinput': False}, {'mql': 'Period2', 'py': 'Period2', 'param': 'Period2', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'Deviation2', 'py': 'Deviation2', 'param': 'Deviation2', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Backstep2', 'py': 'Backstep2', 'param': 'Backstep2', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'HighSymbol2', 'py': 'HighSymbol2', 'param': 'HighSymbol2', 'type': 'int', 'default': 108, 'label': '', 'sinput': False}, {'mql': 'LowSymbol2', 'py': 'LowSymbol2', 'param': 'LowSymbol2', 'type': 'int', 'default': 108, 'label': '', 'sinput': False}, {'mql': 'Period3', 'py': 'Period3', 'param': 'Period3', 'type': 'int', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'Deviation3', 'py': 'Deviation3', 'param': 'Deviation3', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Backstep3', 'py': 'Backstep3', 'param': 'Backstep3', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'HighSymbol3', 'py': 'HighSymbol3', 'param': 'HighSymbol3', 'type': 'int', 'default': 163, 'label': '', 'sinput': False}, {'mql': 'LowSymbol3', 'py': 'LowSymbol3', 'param': 'LowSymbol3', 'type': 'int', 'default': 163, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period1 = _input('Period1', 5)
Deviation1 = _input('Deviation1', 1)
Backstep1 = _input('Backstep1', 3)
HighSymbol1 = _input('HighSymbol1', 159)
LowSymbol1 = _input('LowSymbol1', 159)
Period2 = _input('Period2', 13)
Deviation2 = _input('Deviation2', 8)
Backstep2 = _input('Backstep2', 5)
HighSymbol2 = _input('HighSymbol2', 108)
LowSymbol2 = _input('LowSymbol2', 108)
Period3 = _input('Period3', 34)
Deviation3 = _input('Deviation3', 21)
Backstep3 = _input('Backstep3', 12)
HighSymbol3 = _input('HighSymbol3', 163)
LowSymbol3 = _input('LowSymbol3', 163)
HighBuffer1 = Arr(0, 0.0)
LowBuffer1 = Arr(0, 0.0)
HighBuffer2 = Arr(0, 0.0)
LowBuffer2 = Arr(0, 0.0)
HighBuffer3 = Arr(0, 0.0)
LowBuffer3 = Arr(0, 0.0)
StartBar1 = 0
StartBar2 = 0
StartBar3 = 0
StartBar = 0
Handle1 = 0
Handle2 = 0
Handle3 = 0

def OnInit():
    global Handle1, Handle2, Handle3, StartBar, StartBar1, StartBar2, StartBar3
    StartBar1 = Period1 + Deviation1 + Backstep1 + 1
    StartBar2 = Period2 + Deviation2 + Backstep2 + 1
    StartBar3 = Period3 + Deviation3 + Backstep3 + 1
    StartBar = MathMax(StartBar1, MathMax(StartBar2, StartBar3))
    SetIndexBuffer(0, LowBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetString(0, PLOT_LABEL, 'Low1')
    PlotIndexSetInteger(0, PLOT_ARROW, LowSymbol1)
    ArraySetAsSeries(LowBuffer1, True)
    SetIndexBuffer(1, HighBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetString(1, PLOT_LABEL, 'High1')
    PlotIndexSetInteger(1, PLOT_ARROW, HighSymbol1)
    ArraySetAsSeries(HighBuffer1, True)
    SetIndexBuffer(2, LowBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetString(2, PLOT_LABEL, 'Low2')
    PlotIndexSetInteger(2, PLOT_ARROW, LowSymbol2)
    ArraySetAsSeries(LowBuffer2, True)
    SetIndexBuffer(3, HighBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetString(3, PLOT_LABEL, 'High2')
    PlotIndexSetInteger(3, PLOT_ARROW, HighSymbol2)
    ArraySetAsSeries(HighBuffer2, True)
    SetIndexBuffer(4, LowBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetString(4, PLOT_LABEL, 'Low3')
    PlotIndexSetInteger(4, PLOT_ARROW, LowSymbol3)
    ArraySetAsSeries(LowBuffer3, True)
    SetIndexBuffer(5, HighBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetString(5, PLOT_LABEL, 'High3')
    PlotIndexSetInteger(5, PLOT_ARROW, HighSymbol3)
    ArraySetAsSeries(HighBuffer3, True)
    IndicatorSetString(INDICATOR_SHORTNAME, '3_Level_ZZ_Semafor')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    Handle1 = iCustom(None, 0, 'ExamplesZigZag', Period1, Deviation1, Backstep1)
    if Handle1 == INVALID_HANDLE:
        Print(' Failed to get handle of the ZigZag1 indicator')
    Handle2 = iCustom(None, 0, 'ExamplesZigZag', Period2, Deviation2, Backstep2)
    if Handle2 == INVALID_HANDLE:
        Print(' Failed to get handle of the ZigZag2 indicator')
    Handle3 = iCustom(None, 0, 'ExamplesZigZag', Period3, Deviation3, Backstep3)
    if Handle3 == INVALID_HANDLE:
        Print(' Failed to get handle of the ZigZag3 indicator')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBar:
        return 0
    limit = 0
    to_copy1 = 0
    to_copy2 = 0
    to_copy3 = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBar
        to_copy1 = rates_total
        to_copy2 = rates_total
        to_copy3 = rates_total
    else:
        limit = rates_total - prev_calculated
        to_copy1 = limit + StartBar1
        to_copy2 = limit + StartBar2
        to_copy3 = limit + StartBar3
    if CopyBuffer(Handle1, 1, 0, to_copy1, HighBuffer1) <= 0:
        return 0
    if CopyBuffer(Handle1, 2, 0, to_copy1, LowBuffer1) <= 0:
        return 0
    if CopyBuffer(Handle2, 1, 0, to_copy2, HighBuffer2) <= 0:
        return 0
    if CopyBuffer(Handle2, 2, 0, to_copy2, LowBuffer2) <= 0:
        return 0
    if CopyBuffer(Handle3, 1, 0, to_copy3, HighBuffer3) <= 0:
        return 0
    if CopyBuffer(Handle3, 2, 0, to_copy3, LowBuffer3) <= 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind3LevelZzSemafor(_MQL5Indicator):
    name = '3_level_zz_semafor'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period1': 5,
        'Deviation1': 1,
        'Backstep1': 3,
        'HighSymbol1': 159,
        'LowSymbol1': 159,
        'Period2': 13,
        'Deviation2': 8,
        'Backstep2': 5,
        'HighSymbol2': 108,
        'LowSymbol2': 108,
        'Period3': 34,
        'Deviation3': 21,
        'Backstep3': 12,
        'HighSymbol3': 163,
        'LowSymbol3': 163,
    }

