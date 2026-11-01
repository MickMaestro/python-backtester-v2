"""Autocorrelation — converted from MQL5: MQL5 Indicators/Autocorrelation/Autocorrelation.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'CRL'}, 'levels': [], 'description': [], 'name': 'Autocorrelation', 'source': 'MQL5 Indicators/Autocorrelation/Autocorrelation.mq5', 'folder': 'Autocorrelation', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 100, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 100)  # Period
BufferCRL = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferCRL, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Autocorrelation(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferCRL, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = period * 2
    if rates_total < max_:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = fmin(max_, rates_total - max_ - 1)
        ArrayInitialize(BufferCRL, EMPTY_VALUE)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    sko = 0.0
    sum_ = 0.0
    sumx = 0.0
    sumy = 0.0
    v1 = 0.0
    v2 = 0.0
    for j in range(0, period + 1):
        sko += close[j] * close[j]
        sumx += float(time[j] - time[period])
        sumy += close[j]
    sko = _fdiv(sko, period)
    sumx = _fdiv(sumx, period + 1)
    sumy = _fdiv(sumy, period + 1)
    for j in range(0, period):
        v1 += (time[j] - time[period] - sumx) * (close[j] - sumy)
        v2 += (time[j] - time[period] - sumx) * (time[j] - time[period] - sumx)
    v1 = _fdiv(v1, v2)
    v2 = sumy - (v1 * sumx)
    for j in range(0, period + 1):
        sum_ = 0.0
        for n in range(0, period + 1):
            if (j + n) <= period:
                sum_ += (close[n] - (v1 * (time[n] - time[period])) - v2) * (close[n + j] - (v1 * (time[n + j] - time[period])) - v2)
        BufferCRL[j] = _fdiv(sum_, sko)
    for i in range(period, 0 - 1, -1):
        BufferCRL[i] = _fdiv(BufferCRL[i], BufferCRL[0])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Autocorrelation(_MQL5Indicator):
    name = 'Autocorrelation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriod': 100,  # Period
    }

