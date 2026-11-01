"""Intraday ATR — converted from MQL5: MQL5 Indicators/Intra-day ATR/Intraday ATR.mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [9662683]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ATR'}, 'levels': [], 'description': [], 'name': 'Intraday ATR', 'source': 'MQL5 Indicators/Intra-day ATR/Intraday ATR.mq5', 'folder': 'Intra-day ATR', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # period
val = Arr(0, 0.0)
tr = Arr(0, 0.0)
_timeFrame = PERIOD_D1
_timeFrameName = 'day'

def OnInit():
    global _timeFrame, _timeFrameName
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, tr, INDICATOR_CALCULATIONS)
    if Period() == PERIOD_D1:
        _timeFrame = PERIOD_W1
        _timeFrameName = 'week'
    if Period() == PERIOD_W1 or Period() == PERIOD_MN1:
        _timeFrame = PERIOD_MN1
        _timeFrameName = 'month'
    IndicatorSetString(INDICATOR_SHORTNAME, 'Intra-' + _timeFrameName + ' ATR (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _highTfBar = iBarShift(Symbol(), _timeFrame, time[i])
        _highTfTime = iTime(Symbol(), _timeFrame, _highTfBar)
        _firstBar = iBarShift(Symbol(), Period(), _highTfTime)
        tr[i] = (((high[i] if (high[i] > close[i - 1]) else close[i - 1]) - (low[i] if (low[i] < close[i - 1]) else close[i - 1])) if (i > 0) else (high[i] - low[i]))
        k = 1
        _period = (inpPeriod if (_timeFrame == PERIOD_MN1) else (i - (rates_total - _firstBar - 1) + 1))
        if _period > inpPeriod:
            _period = inpPeriod
        val[i] = tr[i]
        while k < _period and i >= k:
            val[i] += tr[i - k]
            k += 1
        val[i] = _fdiv(val[i], float(k))
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IntradayATR(_MQL5Indicator):
    name = 'Intraday ATR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # period
    }

