"""Equity and Balance — converted from MQL5: MQL5 Indicators/Equity and Balance as an indicator for MT5/Equity and Balance.mq5

Copyright: ABFS Inc; Link: https://www.abfs.tech; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'ABFS Inc', 'link': 'https://www.abfs.tech', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65280], 2: [16755200]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Equity', 2: 'Balance'}, 'levels': [], 'description': [''], 'name': 'Equity and Balance', 'source': 'MQL5 Indicators/Equity and Balance as an indicator for MT5/Equity and Balance.mq5', 'folder': 'Equity and Balance as an indicator for MT5', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)

def AccountBalance_u():
    return AccountInfoDouble(ACCOUNT_BALANCE)

def AccountEquity_u():
    return AccountInfoDouble(ACCOUNT_EQUITY)

def OnInit():
    SetIndexBuffer(0, Buffer1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, Buffer2)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = rates_total - prev_calculated
    ArraySetAsSeries(Buffer1, True)
    ArraySetAsSeries(Buffer2, True)
    if prev_calculated < 1:
        ArrayInitialize(Buffer1, EMPTY_VALUE)
        ArrayInitialize(Buffer2, EMPTY_VALUE)
    else:
        limit += 1
    for i in range(limit - 1, 0 - 1, -1):
        if i >= MathMin(5000 - 1, rates_total - 1 - 50):
            continue
        if True:
            Buffer1[i] = AccountEquity_u()
        else:
            Buffer1[i] = EMPTY_VALUE
        if True:
            Buffer2[i] = AccountBalance_u()
        else:
            Buffer2[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EquityAndBalance(_MQL5Indicator):
    name = 'Equity and Balance'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

