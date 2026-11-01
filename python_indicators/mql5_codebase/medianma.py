"""MedianMA — converted from MQL5: MQL5 Indicators/Median Moving Average/MedianMA.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1, 2: 1}, 'colors': {1: [3937500], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MedianMA', 2: 'TMP'}, 'levels': [], 'description': [], 'name': 'MedianMA', 'source': 'MQL5 Indicators/Median Moving Average/MedianMA.mq5', 'folder': 'Median Moving Average', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferMedianMA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
TMP = Arr(0, 0.0)
handle_ma = 0
period = 0
index = 0
even = False

def OnInit():
    global even, handle_ma, index, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    if ArrayResize(TMP, period) == WRONG_VALUE:
        Print('Failed to set the size of the TMP array')
        return INIT_FAILED
    even = (True if ((round(_idiv(period, 2)) * 2) == period) else False)
    index = _int(floor(_idiv(period, 2)))
    SetIndexBuffer(0, BufferMedianMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Median Moving Average(' + _str(period) + ')')
    ArraySetAsSeries(BufferMedianMA, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(Symbol(), PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1 - period
        ArrayInitialize(BufferMedianMA, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        for n in range(0, period):
            TMP[n] = BufferMA[i + n]
        ArraySort(TMP)
        if even:
            BufferMedianMA[i] = (TMP[index] + TMP[index - 1]) / 2
        else:
            BufferMedianMA[i] = TMP[index]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MedianMA(_MQL5Indicator):
    name = 'MedianMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

