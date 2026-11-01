"""Laguerre — converted from MQL5: MQL5 Indicators/Laguerre MT5/Laguerre.mq5

Laguerre - shows weighted trendline in a separate indicator window.
Link: https://t.me/ForexEaPremium; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'link': 'https://t.me/ForexEaPremium', 'version': '1.02', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 1.0}, 'types': {1: 1}, 'colors': {1: [16711935]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [0.8, 0.5, 0.2], 'description': ['Laguerre - shows weighted trendline in a separate indicator window.'], 'name': 'Laguerre', 'source': 'MQL5 Indicators/Laguerre MT5/Laguerre.mq5', 'folder': 'Laguerre MT5', 'inputs': [{'mql': 'Gamma', 'py': 'Gamma', 'param': 'Gamma', 'type': 'double', 'default': 0.7, 'label': '', 'sinput': False}, {'mql': 'CountBars', 'py': 'CountBars', 'param': 'CountBars', 'type': 'int', 'default': 950, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Gamma = _input('Gamma', 0.7)
CountBars = _input('CountBars', 950)
Laguerre = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, Laguerre, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Laguerre')
    ArraySetAsSeries(Laguerre, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, Close, tick_volume, volume, spread):
    i = rates_total - 1
    if i >= CountBars:
        i = CountBars - 1
    ArraySetAsSeries(Close, True)
    L0 = 0.0
    L1 = 0.0
    L2 = 0.0
    L3 = 0.0
    LRSI = 0.0
    while i >= 0:
        L0A = L0
        L1A = L1
        L2A = L2
        L3A = L3
        L0 = ((1 - Gamma) * Close[i]) + (Gamma * L0A)
        L1 = ((-Gamma) * L0) + L0A + (Gamma * L1A)
        L2 = ((-Gamma) * L1) + L1A + (Gamma * L2A)
        L3 = ((-Gamma) * L2) + L2A + (Gamma * L3A)
        CU = 0.0
        CD = 0.0
        if L0 >= L1:
            CU = L0 - L1
        else:
            CD = L1 - L0
        if L1 >= L2:
            CU = CU + L1 - L2
        else:
            CD = CD + L2 - L1
        if L2 >= L3:
            CU = CU + L2 - L3
        else:
            CD = CD + L3 - L2
        if (CU + CD) != 0:
            LRSI = _fdiv(CU, CU + CD)
        Laguerre[i] = LRSI
        i -= 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LaguerreIndicator(_MQL5Indicator):
    name = 'Laguerre'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Gamma': 0.7,
        'CountBars': 950,
    }
    y_range = (0.0, 1.0)

