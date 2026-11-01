"""Simple intraday support resistance — converted from MQL5: MQL5 Indicators/Simple intraday support resistance/Simple intraday support resistance.mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 7, 2: 1}, 'colors': {1: [13628367, 13492732], 2: [11119017]}, 'widths': {}, 'styles': {}, 'labels': {1: 'filling', 2: 'Value'}, 'levels': [], 'description': [], 'name': 'Simple intraday support resistance', 'source': 'MQL5 Indicators/Simple intraday support resistance/Simple intraday support resistance.mq5', 'folder': 'Simple intraday support resistance', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
val = Arr(0, 0.0)
hh = Arr(0, 0.0)
ll = Arr(0, 0.0)

def OnInit():
    if Period() >= PERIOD_D1:
        Alert('This indicator must work on time frames less than daily')
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, hh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ll, INDICATOR_CALCULATIONS)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Period() >= PERIOD_D1:
        return rates_total
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if i == 0 or iBarShift(Symbol(), PERIOD_D1, time[i]) != iBarShift(Symbol(), PERIOD_D1, time[i - 1]):
            hh[i] = high[i]
            ll[i] = low[i]
        else:
            hh[i] = (high[i] if (high[i] > hh[i - 1]) else hh[i - 1])
            ll[i] = (low[i] if (low[i] < ll[i - 1]) else ll[i - 1])
        _middle = (hh[i] + ll[i]) / 2.0
        val[i] = _middle
        fup[i] = (low[i] if (high[i] > _middle) else high[i] if (low[i] < _middle) else fup[i - 1] if (i > 0) else close[i])
        fdn[i] = _middle
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SimpleIntradaySupportResistance(_MQL5Indicator):
    name = 'Simple intraday support resistance'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

