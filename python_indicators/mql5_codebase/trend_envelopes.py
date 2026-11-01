"""Trend envelopes — converted from MQL5: MQL5 Indicators/Trend Envelopes/Trend envelopes.mq5

Trend envelopes - basic version
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [16748574], 2: [3937500], 3: [16748574], 4: [3937500]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {}, 'labels': {1: 'Trend envelope up trend line', 2: 'Trend envelope down trend line', 3: 'Trend envelope up trend start', 4: 'Trend envelope down trend start'}, 'levels': [], 'description': ['Trend envelopes - basic version'], 'name': 'Trend envelopes', 'source': 'MQL5 Indicators/Trend Envelopes/Trend envelopes.mq5', 'folder': 'Trend Envelopes', 'inputs': [{'mql': 'inpDeviation', 'py': 'inpDeviation', 'param': 'inpDeviation', 'type': 'double', 'default': 0.1, 'label': 'Trend envelopes deviation %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpDeviation = _input('inpDeviation', 0.1)  # Trend envelopes deviation %
lineup = Arr(0, 0.0)
linedn = Arr(0, 0.0)
arrowup = Arr(0, 0.0)
arrowdn = Arr(0, 0.0)
workTrendEnvelopes = Arr(0, 0.0, dims=(3,))

class sTrendEnvelope(MqlObject):
    _q_fields = ('upline', 'downline', 'trend', 'trendChange')
    def __init__(self, *args):
        self.upline = 0.0
        self.downline = 0.0
        self.trend = 0
        self.trendChange = False

def OnInit():
    SetIndexBuffer(0, lineup, INDICATOR_DATA)
    SetIndexBuffer(1, linedn, INDICATOR_DATA)
    SetIndexBuffer(2, arrowup, INDICATOR_DATA)
    PlotIndexGetInteger(2, PLOT_ARROW, 159)
    SetIndexBuffer(3, arrowdn, INDICATOR_DATA)
    PlotIndexGetInteger(3, PLOT_ARROW, 159)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _result = iTrendEnvelope(high[i], low[i], close[i], inpDeviation, i, rates_total)
        lineup[i] = _result.upline
        linedn[i] = _result.downline
        arrowup[i] = (lineup[i] if (_result.trendChange and _result.trend == 1) else EMPTY_VALUE)
        arrowdn[i] = (linedn[i] if (_result.trendChange and _result.trend == -1) else EMPTY_VALUE)
    return rates_total

def iTrendEnvelope(valueh, valuel, value, deviation, i, bars, instanceNo=0):
    if ArrayRange(workTrendEnvelopes, 0) != bars:
        ArrayResize(workTrendEnvelopes, bars)
    instanceNo *= 3
    workTrendEnvelopes[i][instanceNo + 1] = (1 + (deviation / 100)) * valueh
    workTrendEnvelopes[i][instanceNo + 0] = (1 - (deviation / 100)) * valuel
    workTrendEnvelopes[i][instanceNo + 2] = ((1 if (value > workTrendEnvelopes[i - 1][instanceNo + 1]) else -1 if (value < workTrendEnvelopes[i - 1][instanceNo + 0]) else workTrendEnvelopes[i - 1][instanceNo + 2]) if (i > 0) else 0)
    if (i > 0 and workTrendEnvelopes[i][instanceNo + 2] > 0) and workTrendEnvelopes[i][instanceNo + 0] < workTrendEnvelopes[i - 1][instanceNo + 0]:
        workTrendEnvelopes[i][instanceNo + 0] = workTrendEnvelopes[i - 1][instanceNo + 0]
    if (i > 0 and workTrendEnvelopes[i][instanceNo + 2] < 0) and workTrendEnvelopes[i][instanceNo + 1] > workTrendEnvelopes[i - 1][instanceNo + 1]:
        workTrendEnvelopes[i][instanceNo + 1] = workTrendEnvelopes[i - 1][instanceNo + 1]
    _result = sTrendEnvelope()
    _result.trend = _int(workTrendEnvelopes[i][instanceNo + 2])
    _result.trendChange = ((workTrendEnvelopes[i][instanceNo + 2] != workTrendEnvelopes[i - 1][instanceNo + 2]) if (i > 0) else False)
    _result.upline = (workTrendEnvelopes[i][instanceNo + 0] if (workTrendEnvelopes[i][instanceNo + 2] == 1) else EMPTY_VALUE)
    _result.downline = (workTrendEnvelopes[i][instanceNo + 1] if (workTrendEnvelopes[i][instanceNo + 2] == -1) else EMPTY_VALUE)
    return _copy(_result)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendEnvelopes(_MQL5Indicator):
    name = 'Trend envelopes'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpDeviation': 0.1,  # Trend envelopes deviation %
    }

