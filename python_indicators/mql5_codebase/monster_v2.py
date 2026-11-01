"""monster_v2 — converted from MQL5: MQL5 Indicators/Dual Trix 15 and 30/monster_v2.mq5

Copyright: Q-Import; Version: 2.3

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Q-Import', 'version': '2.3', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Plot1', 2: 'Plot2'}, 'levels': [], 'description': [], 'name': 'monster_v2', 'source': 'MQL5 Indicators/Dual Trix 15 and 30/monster_v2.mq5', 'folder': 'Dual Trix 15 and 30', 'inputs': [{'mql': 'State1', 'py': 'State1', 'param': 'State1', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Plot1', 'py': 'Plot1', 'param': 'Plot1', 'type': 'int', 'default': 15, 'label': 'Period Of The First Plot', 'sinput': False}, {'mql': 'Plot2', 'py': 'Plot2', 'param': 'Plot2', 'type': 'int', 'default': 30, 'label': 'Period Of The Second Plot', 'sinput': False}, {'mql': 'ToClose', 'py': 'ToClose', 'param': 'ToClose', 'type': 'int', 'default': 1, 'label': 'Price Applied To Both Plots', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
State1 = _input('State1', True)
Plot1 = _input('Plot1', 15)  # Period Of The First Plot
Plot2 = _input('Plot2', 30)  # Period Of The Second Plot
ToClose = _input('ToClose', PRICE_CLOSE)  # Price Applied To Both Plots
TriX_Handle1 = 0  # handle for our Trix First Plot
TriX_Handle2 = 0  # handle for our Trix Second Plot
TriX1 = Arr(0, 0.0)  # Dynamic array to hold the values of Trix for each bars Plot 1
TriX2 = Arr(0, 0.0)  # Dynamic array to hold the values of Trix for each bars Plot 2

def OnInit():
    global TriX_Handle1, TriX_Handle2
    SetIndexBuffer(0, TriX1, INDICATOR_DATA)
    SetIndexBuffer(1, TriX2, INDICATOR_DATA)
    Print('Parameter AsSeries =', State1)
    ArraySetAsSeries(TriX1, State1)
    ArraySetAsSeries(TriX2, State1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trix CrossOver(' + IntegerToString(Plot1) + ')( ' + IntegerToString(Plot2) + ')' + _str(State1))
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, 6)
    TriX_Handle1 = iTriX(Symbol(), 0, Plot1, ToClose)
    TriX_Handle2 = iTriX(Symbol(), 0, Plot2, ToClose)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    calculated = BarsCalculated(TriX_Handle1)
    if calculated < rates_total:
        Print('Not all data of TriX_Handle1 is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(TriX_Handle2)
    if calculated < rates_total:
        Print('Not all data of TriX_Handle2 is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        to_copy += 1
    if CopyBuffer(TriX_Handle1, 0, 0, to_copy, TriX1) <= 0:
        return 0
    if CopyBuffer(TriX_Handle2, 0, 0, to_copy, TriX2) <= 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MonsterV2(_MQL5Indicator):
    name = 'monster_v2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'State1': True,
        'Plot1': 15,  # Period Of The First Plot
        'Plot2': 30,  # Period Of The Second Plot
        'ToClose': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price Applied To Both Plots
    }

