"""PR — converted from MQL5: MQL5 Indicators/PR/PR.mq5

Period Range
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Range'}, 'levels': [], 'description': ['Period Range'], 'name': 'PR', 'source': 'MQL5 Indicators/PR/PR.mq5', 'folder': 'PR', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpUseLastPeriod', 'py': 'InpUseLastPeriod', 'param': 'InpUseLastPeriod', 'type': 'bool', 'default': False, 'label': 'Use last period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpUseLastPeriod = _input('InpUseLastPeriod', False)  # Use last period
BufferCentral = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferCentral, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PR(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 100)
    ArraySetAsSeries(BufferCentral, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 2
        ArrayInitialize(BufferCentral, EMPTY_VALUE)
    min_ = 0.0
    max_ = 0.0
    for i in range(limit, 0 - 1, -1):
        if InpUseLastPeriod:
            lb = Lowest(period, i)
            hb = Highest(period, i)
            if lb == WRONG_VALUE or hb == WRONG_VALUE:
                return 0
            min_ = low[lb]
            max_ = high[hb]
        else:
            lb = Lowest(period, i + 1)
            hb = Highest(period, i + 1)
            if lb == WRONG_VALUE or hb == WRONG_VALUE:
                return 0
            min_ = low[lb]
            max_ = high[hb]
        BufferCentral[i] = (_fdiv(100 * (close[i] - min_), max_ - min_) if (min_ != max_) else EMPTY_VALUE)
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


class PR(_MQL5Indicator):
    name = 'PR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpUseLastPeriod': False,  # Use last period
    }

