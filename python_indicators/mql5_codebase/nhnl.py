"""NHNL — converted from MQL5: MQL5 Indicators/NHNL/NHNL.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [32768], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'High Index', 2: 'Low Index', 3: 'Index HL'}, 'levels': [], 'description': [], 'name': 'NHNL', 'source': 'MQL5 Indicators/NHNL/NHNL.mq5', 'folder': 'NHNL', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)
BufferHigh = Arr(0, 0.0)
BufferLow = Arr(0, 0.0)
BufferHL = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferHigh, INDICATOR_DATA)
    SetIndexBuffer(1, BufferLow, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHL, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'New High, New Low Index(' + _str(period) + ')')
    ArraySetAsSeries(BufferHigh, True)
    ArraySetAsSeries(BufferLow, True)
    ArraySetAsSeries(BufferHL, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 2
        ArrayInitialize(BufferHigh, EMPTY_VALUE)
        ArrayInitialize(BufferLow, EMPTY_VALUE)
        ArrayInitialize(BufferHL, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        count_h = 0
        count_l = 0
        for n in range(0, period):
            if high[i + n] > high[i + n + 1]:
                count_h += 1
            if low[i + n] < low[i + n + 1]:
                count_l -= 1
        BufferHigh[i] = count_h
        BufferLow[i] = count_l
        BufferHL[i] = count_h + count_l
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NHNL(_MQL5Indicator):
    name = 'NHNL'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,
    }

