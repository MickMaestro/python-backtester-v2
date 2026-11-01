"""Trading the trend - histogram — converted from MQL5: MQL5 Indicators/Trading the trend - histogram/Trading the trend - histogram.mq5

Trading the trend
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 1.0}, 'types': {1: 10}, 'colors': {1: [11119017, 16760576, 6333684]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Trend histogram'}, 'levels': [], 'description': ['Trading the trend'], 'name': 'Trading the trend - histogram', 'source': 'MQL5 Indicators/Trading the trend - histogram/Trading the trend - histogram.mq5', 'folder': 'Trading the trend - histogram', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 21, 'label': 'Look back period', 'sinput': False}, {'mql': 'inpMultiplier', 'py': 'inpMultiplier', 'param': 'inpMultiplier', 'type': 'double', 'default': 3.0, 'label': 'Multiplier', 'sinput': False}, {'mql': 'inpChannelShift', 'py': 'inpChannelShift', 'param': 'inpChannelShift', 'type': 'int', 'default': 1, 'label': 'Channel shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 21)  # Look back period
inpMultiplier = _input('inpMultiplier', 3.0)  # Multiplier
inpChannelShift = _input('inpChannelShift', 1)  # Channel shift
histo = Arr(0, 0.0)
histoc = Arr(0, 0.0)
line = Arr(0, 0.0)
linecl = Arr(0, 0.0)
workLwma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, histo, INDICATOR_DATA)
    SetIndexBuffer(1, histoc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, line, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, linecl, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trade the trend histogram (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _start = MathMax(i - inpPeriod - inpChannelShift + 1, 0)
        hi = close[ArrayMaximum(close, _start, inpPeriod)]
        lo = close[ArrayMinimum(close, _start, inpPeriod)]
        tr = iLwma(((MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])) if (i > 0) else (high[i] - low[i])), inpPeriod, i, rates_total)
        hiLimit = hi - (tr * inpMultiplier)
        loLimit = lo + (tr * inpMultiplier)
        line[i] = (line[i - 1] if (i > 0) else close[i])
        linecl[i] = (linecl[i - 1] if (i > 0) else 0)
        if close[i] > loLimit and close[i] > hiLimit:
            line[i] = hiLimit
        if close[i] < loLimit and close[i] < hiLimit:
            line[i] = loLimit
        if close[i] > line[i]:
            linecl[i] = 1.0
        if close[i] < line[i]:
            linecl[i] = 2.0
        histo[i] = 1.0
        histoc[i] = linecl[i]
        i += 1
    return i

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TradingTheTrendHistogram(_MQL5Indicator):
    name = 'Trading the trend - histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 21,  # Look back period
        'inpMultiplier': 3.0,  # Multiplier
        'inpChannelShift': 1,  # Channel shift
    }
    y_range = (0.0, 1.0)

