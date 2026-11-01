"""spreads — converted from MQL5: MQL5 Indicators/Spreads/spreads.mq5

Copyright: Copyright 2025, Roman Shiredchenko; Version: 1.3

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, Roman Shiredchenko', 'version': '1.3', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [55295]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Difference'}, 'levels': [], 'description': [], 'name': 'spreads', 'source': 'MQL5 Indicators/Spreads/spreads.mq5', 'folder': 'Spreads', 'inputs': [{'mql': 'Weighting_coefficients1', 'py': 'Weighting_coefficients1', 'param': 'Weighting_coefficients1', 'type': 'double', 'default': 1.0, 'label': 'proportionality factor (position volume) of the first spread symbol', 'sinput': False}, {'mql': 'Coefficient_to_an_integer1', 'py': 'Coefficient_to_an_integer1', 'param': 'Coefficient_to_an_integer1', 'type': 'int', 'default': 100000, 'label': 'number of quotation marks Sym 1', 'sinput': False}, {'mql': 'Symbol2', 'py': 'Symbol2', 'param': None, 'type': 'string', 'default': 'USDCAD', 'label': 'second spread symbol', 'sinput': False}, {'mql': 'Symbol2_Reverse', 'py': 'Symbol2_Reverse', 'param': 'Symbol2_Reverse', 'type': 'bool', 'default': True, 'label': 'inverse correlation', 'sinput': False}, {'mql': 'Weighting_coefficients2', 'py': 'Weighting_coefficients2', 'param': 'Weighting_coefficients2', 'type': 'double', 'default': 1.0, 'label': 'proportionality factor (position volume) of the first spread symbol', 'sinput': False}, {'mql': 'Coefficient_to_an_integer2', 'py': 'Coefficient_to_an_integer2', 'param': 'Coefficient_to_an_integer2', 'type': 'int', 'default': 100000, 'label': 'number of quotation marks Sym 2', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Weighting_coefficients1 = _input('Weighting_coefficients1', 1.0)  # proportionality factor (position volume) of the first spread symbol
Coefficient_to_an_integer1 = _input('Coefficient_to_an_integer1', 100000)  # number of quotation marks Sym 1
Symbol2 = _input('Symbol2', 'USDCAD')  # second spread symbol
Symbol2_Reverse = _input('Symbol2_Reverse', True)  # inverse correlation
Weighting_coefficients2 = _input('Weighting_coefficients2', 1.0)  # proportionality factor (position volume) of the first spread symbol
Coefficient_to_an_integer2 = _input('Coefficient_to_an_integer2', 100000)  # number of quotation marks Sym 2
BufferCurrent = Arr(0, 0.0)  # Current
EMPTY_v = -1
priv = 0

def OnInit():
    if not SymbolSelect(Symbol2, True):
        return INIT_FAILED
    SetIndexBuffer(0, BufferCurrent, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'Spread')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetInteger(0, PLOT_SHIFT, 0)
    ArraySetAsSeries(BufferCurrent, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global priv
    limit = 0
    corr = 0
    if prev_calculated <= 0:
        limit = rates_total - 1
        EventSetTimer(1)
        priv = 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    if Bars(Symbol2, PERIOD_CURRENT) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        time2 = iTime(Symbol2, PERIOD_CURRENT, i - corr)
        if time2 > time[i]:
            corr += 1
            continue
        open2 = iOpen(Symbol2, PERIOD_CURRENT, i)
        if open2 != 0:
            if not Symbol2_Reverse:
                BufferCurrent[i] = NormalizeDouble((Coefficient_to_an_integer1 * Weighting_coefficients1 * open[i]) - (Coefficient_to_an_integer2 * Weighting_coefficients2 * open2), 0)
            else:
                BufferCurrent[i] = NormalizeDouble((Coefficient_to_an_integer1 * Weighting_coefficients1 * open[i]) + (Coefficient_to_an_integer1 * Weighting_coefficients2 * open2), 0)
    priv = rates_total
    return rates_total

def OnTimer():
    if priv <= 0:
        ChartSetSymbolPeriod(0, Symbol(), PERIOD_CURRENT)
    else:
        EventKillTimer()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Spreads(_MQL5Indicator):
    name = 'spreads'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Weighting_coefficients1': 1.0,  # proportionality factor (position volume) of the first spread symbol
        'Coefficient_to_an_integer1': 100000,  # number of quotation marks Sym 1
        'Symbol2_Reverse': True,  # inverse correlation
        'Weighting_coefficients2': 1.0,  # proportionality factor (position volume) of the first spread symbol
        'Coefficient_to_an_integer2': 100000,  # number of quotation marks Sym 2
    }

