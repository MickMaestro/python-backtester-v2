"""GAPO — converted from MQL5: MQL5 Indicators/GAPO/GAPO.mq5

Gopalakrishnan Range Index
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13434880]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'GAPO'}, 'levels': [], 'description': ['Gopalakrishnan Range Index'], 'name': 'GAPO', 'source': 'MQL5 Indicators/GAPO/GAPO.mq5', 'folder': 'GAPO', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 5, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 5)  # Period
BufferGAPO = Arr(0, 0.0)
period = 0
log_period = 0.0

def OnInit():
    global log_period, period
    period = (2 if (InpPeriod < 2) else InpPeriod)
    log_period = log(period)
    SetIndexBuffer(0, BufferGAPO, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'GAPO(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferGAPO, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferGAPO, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        bl = Lowest(period, i)
        bh = Highest(period, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = low[bl]
        max_ = high[bh]
        BufferGAPO[i] = (_fdiv(log(max_ - min_), log_period) if (min_ != max_) else EMPTY_VALUE)
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMinimum(array) + start
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GAPO(_MQL5Indicator):
    name = 'GAPO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 5,  # Period
    }

