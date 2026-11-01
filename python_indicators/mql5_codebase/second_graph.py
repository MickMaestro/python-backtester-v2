"""second_graph — converted from MQL5: MQL5 Indicators/Second Graph/second_graph.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'second_graph', 'source': 'MQL5 Indicators/Second Graph/second_graph.mq5', 'folder': 'Second Graph', 'inputs': [{'mql': 'symbol1', 'py': 'symbol1', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
symbol1 = _input('symbol1', 'EURUSD')
i = 0
ind1 = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ind1, INDICATOR_DATA)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global i
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    ArraySetAsSeries(volume, True)
    ArraySetAsSeries(spread, True)
    ArraySetAsSeries(ind1, True)
    rates1 = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(rates1, True)
    if prev_calculated < rates_total:
        i = 0
        while i < rates_total:
            CopyRates(symbol1, 0, _DT(time[i]), 1, rates1)
            ind1[i] = rates1[0].close
            i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SecondGraph(_MQL5Indicator):
    name = 'second_graph'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

