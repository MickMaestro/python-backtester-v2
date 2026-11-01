"""Trend envelopes - parabolic weighted MA - histo — converted from MQL5: MQL5 Indicators/Trend envelopes - parabolic weighted MA - histo/Trend envelopes - parabolic weighted MA - histo.mq5

Trend envelopes - of parabolic weighted MA - histo
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 1.0}, 'types': {1: 10}, 'colors': {1: [16748574, 3937500]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Trend envelope histo'}, 'levels': [], 'description': ['Trend envelopes - of parabolic weighted MA - histo'], 'name': 'Trend envelopes - parabolic weighted MA - histo', 'source': 'MQL5 Indicators/Trend envelopes - parabolic weighted MA - histo/Trend envelopes - parabolic weighted MA - histo.mq5', 'folder': 'Trend envelopes - parabolic weighted MA - histo', 'inputs': [{'mql': 'inpDeviation', 'py': 'inpDeviation', 'param': 'inpDeviation', 'type': 'double', 'default': 0.1, 'label': 'Trend envelopes deviation %', 'sinput': False}, {'mql': 'inpPwmaPeriod', 'py': 'inpPwmaPeriod', 'param': 'inpPwmaPeriod', 'type': 'int', 'default': 14, 'label': 'PWMA period (<=1 for no smoothing)', 'sinput': False}, {'mql': 'inpPwmaPower', 'py': 'inpPwmaPower', 'param': 'inpPwmaPower', 'type': 'double', 'default': 2.0, 'label': 'PWMA power', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpDeviation = _input('inpDeviation', 0.1)  # Trend envelopes deviation %
inpPwmaPeriod = _input('inpPwmaPeriod', 14)  # PWMA period (<=1 for no smoothing)
inpPwmaPower = _input('inpPwmaPower', 2.0)  # PWMA power
histo = Arr(0, 0.0)
histoc = Arr(0, 0.0)
workPwma = Arr(0, 0.0, dims=(2,))
workTrendEnvelopes = Arr(0, 0.0, dims=(3,))

class sTrendEnvelope(MqlObject):
    _q_fields = ('upline', 'downline', 'trend', 'trendChange')
    def __init__(self, *args):
        self.upline = 0.0
        self.downline = 0.0
        self.trend = 0
        self.trendChange = False

def OnInit():
    SetIndexBuffer(0, histo, INDICATOR_DATA)
    SetIndexBuffer(1, histoc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PWMA Trend envelopes (' + _str(inpDeviation) + ')(' + _str(inpPwmaPeriod) + ' ' + _str(inpPwmaPower) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _high = iPwma(high[i], inpPwmaPeriod, inpPwmaPower, i, rates_total, 0)
        _low = iPwma(low[i], inpPwmaPeriod, inpPwmaPower, i, rates_total, 1)
        _result = iTrendEnvelope(_high, _low, close[i], inpDeviation, i, rates_total)
        histo[i] = 1.0
        histoc[i] = (0 if (_result.trend == 1) else 1)
    return rates_total

def iPwma(price, period, power, i, bars, instanceNo=0):
    if ArraySize(workPwma) != bars:
        ArrayResize(workPwma, bars)
    workPwma[i][instanceNo] = price
    sum_ = 0.0
    sumw = 0.0
    k = 0
    while k < period and (i - k) >= 0:
        weight = MathPow(period - k, power)
        sumw += weight
        sum_ += weight * workPwma[i - k][instanceNo]
        k += 1
    return (_fdiv(sum_, sumw) if (sumw != 0) else price)

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


class TrendEnvelopesParabolicWeightedMAHisto(_MQL5Indicator):
    name = 'Trend envelopes - parabolic weighted MA - histo'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpDeviation': 0.1,  # Trend envelopes deviation %
        'inpPwmaPeriod': 14,  # PWMA period (<=1 for no smoothing)
        'inpPwmaPower': 2.0,  # PWMA power
    }
    y_range = (0.0, 1.0)

