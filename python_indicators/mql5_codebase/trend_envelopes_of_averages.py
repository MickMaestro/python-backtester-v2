"""Trend envelopes - of averages — converted from MQL5: MQL5 Indicators/Trend Envelopes of Averages/Trend envelopes - of averages.mq5

Trend envelopes - basic version
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [16748574], 2: [3937500], 3: [16748574], 4: [3937500]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {}, 'labels': {1: 'Trend envelope up trend line', 2: 'Trend envelope down trend line', 3: 'Trend envelope up trend start', 4: 'Trend envelope down trend start'}, 'levels': [], 'description': ['Trend envelopes - basic version'], 'name': 'Trend envelopes - of averages', 'source': 'MQL5 Indicators/Trend Envelopes of Averages/Trend envelopes - of averages.mq5', 'folder': 'Trend Envelopes of Averages', 'inputs': [{'mql': 'inpDeviation', 'py': 'inpDeviation', 'param': 'inpDeviation', 'type': 'double', 'default': 0.1, 'label': 'Trend envelopes deviation %', 'sinput': False}, {'mql': 'inpSmtPeriod', 'py': 'inpSmtPeriod', 'param': 'inpSmtPeriod', 'type': 'int', 'default': 14, 'label': 'Smoothing period (<=1 for no smoothing)', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpDeviation = _input('inpDeviation', 0.1)  # Trend envelopes deviation %
inpSmtPeriod = _input('inpSmtPeriod', 14)  # Smoothing period (<=1 for no smoothing)
inpMaMethod = _input('inpMaMethod', ma_sma)  # Smoothing method
lineup = Arr(0, 0.0)
linedn = Arr(0, 0.0)
arrowup = Arr(0, 0.0)
arrowdn = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(2,))
workEma = Arr(0, 0.0, dims=(2,))
workSmma = Arr(0, 0.0, dims=(2,))
workLwma = Arr(0, 0.0, dims=(2,))
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
        _high = iCustomMa(inpMaMethod, high[i], inpSmtPeriod, i, rates_total, 0)
        _low = iCustomMa(inpMaMethod, low[i], inpSmtPeriod, i, rates_total, 1)
        _result = iTrendEnvelope(_high, _low, close[i], inpDeviation, i, rates_total)
        lineup[i] = _result.upline
        linedn[i] = _result.downline
        arrowup[i] = (lineup[i] if (_result.trendChange and _result.trend == 1) else EMPTY_VALUE)
        arrowdn[i] = (linedn[i] if (_result.trendChange and _result.trend == -1) else EMPTY_VALUE)
    return rates_total

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    workSmma[r][instanceNo] = price
    if r > 1 and period > 1:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    if period < 1:
        return price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

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


class TrendEnvelopesOfAverages(_MQL5Indicator):
    name = 'Trend envelopes - of averages'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpDeviation': 0.1,  # Trend envelopes deviation %
        'inpSmtPeriod': 14,  # Smoothing period (<=1 for no smoothing)
        'inpMaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Smoothing method
    }

