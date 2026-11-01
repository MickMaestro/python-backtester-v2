"""Aroon_Horn — converted from MQL5: MQL5 Indicators/Aroon_Horn/Aroon_Horn.mq5

Aroon Horn oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [11119017, 32768, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Aroon Horn'}, 'levels': [], 'description': ['Aroon Horn oscillator'], 'name': 'Aroon_Horn', 'source': 'MQL5 Indicators/Aroon_Horn/Aroon_Horn.mq5', 'folder': 'Aroon_Horn', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpFilter', 'py': 'InpFilter', 'param': 'InpFilter', 'type': 'double', 'default': 25.0, 'label': 'Filter', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpFilter = _input('InpFilter', 25.0)  # Filter
BufferAH = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
filter_ = 0.0
period = 0

def OnInit():
    global filter_, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    filter_ = fabs(InpFilter)
    SetIndexBuffer(0, BufferAH, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Aroon Horn (' + _str(period) + ',' + DoubleToString(filter_, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferAH, True)
    ArraySetAsSeries(BufferColors, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferAH, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        bl = Lowest(period, i)
        bh = Highest(period, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        up = _fdiv(100.0 * (period - bh + i), period)
        dn = _fdiv(100.0 * (period - bl + i), period)
        BufferAH[i] = _fdiv(10.0 * (up - dn), period)
    for i in range(limit, 0 - 1, -1):
        BufferColors[i] = (1 if (BufferAH[i] >= filter_) else 2 if (BufferAH[i] <= (-filter_)) else 0)
    return rates_total

def Highest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AroonHorn(_MQL5Indicator):
    name = 'Aroon_Horn'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpFilter': 25.0,  # Filter
    }

