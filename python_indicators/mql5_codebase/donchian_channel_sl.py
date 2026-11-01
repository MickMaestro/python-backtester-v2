"""Donchian channel (sl) — converted from MQL5: MQL5 Indicators/Donchian channel - extended/Donchian channel (sl).mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [14478300], 2: [14474475], 3: [7451452], 4: [7451452], 5: [17919], 6: [17919]}, 'widths': {}, 'styles': {4: 2, 6: 2}, 'labels': {1: 'High fill', 2: 'Low fill', 3: 'Highest high', 4: 'Lowest high', 5: 'Lowest low', 6: 'Highest low'}, 'levels': [], 'description': [], 'name': 'Donchian channel (sl)', 'source': 'MQL5 Indicators/Donchian channel - extended/Donchian channel (sl).mq5', 'folder': 'Donchian channel - extended', 'inputs': [{'mql': 'inpChannelPeriod', 'py': 'inpChannelPeriod', 'param': 'inpChannelPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpChannelPeriod = _input('inpChannelPeriod', 20)  # Period
valuu = Arr(0, 0.0)
valud = Arr(0, 0.0)
valdd = Arr(0, 0.0)
valdu = Arr(0, 0.0)
filluu = Arr(0, 0.0)
fillud = Arr(0, 0.0)
filldd = Arr(0, 0.0)
filldu = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, filluu, INDICATOR_DATA)
    SetIndexBuffer(1, fillud, INDICATOR_DATA)
    SetIndexBuffer(2, filldu, INDICATOR_DATA)
    SetIndexBuffer(3, filldd, INDICATOR_DATA)
    SetIndexBuffer(4, valuu, INDICATOR_DATA)
    SetIndexBuffer(5, valud, INDICATOR_DATA)
    SetIndexBuffer(6, valdd, INDICATOR_DATA)
    SetIndexBuffer(7, valdu, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_hh, _s_OnCalculate_prev_hl, _s_OnCalculate_prev_lh, _s_OnCalculate_prev_ll
    i = prev_calculated
    while i < rates_total:
        if _s_OnCalculate_prev_i != i:
            start = i - inpChannelPeriod
            if start < 0:
                start = 0
            _s_OnCalculate_prev_hh = high[ArrayMaximum(high, start, inpChannelPeriod)]
            _s_OnCalculate_prev_hl = low[ArrayMaximum(low, start, inpChannelPeriod)]
            _s_OnCalculate_prev_ll = low[ArrayMinimum(low, start, inpChannelPeriod)]
            _s_OnCalculate_prev_lh = high[ArrayMinimum(high, start, inpChannelPeriod)]
        filluu[i] = _s_OnCalculate_prev_hh
        valuu[i] = filluu[i]
        fillud[i] = _s_OnCalculate_prev_hl
        valud[i] = fillud[i]
        filldd[i] = _s_OnCalculate_prev_ll
        valdd[i] = filldd[i]
        filldu[i] = _s_OnCalculate_prev_lh
        valdu[i] = filldu[i]
        i += 1
    return i

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_hh = 0.0
_s_OnCalculate_prev_hl = 0.0
_s_OnCalculate_prev_ll = 0.0
_s_OnCalculate_prev_lh = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DonchianChannelSl(_MQL5Indicator):
    name = 'Donchian channel (sl)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpChannelPeriod': 20,  # Period
    }

