"""DMA — converted from MQL5: MQL5 Indicators/DMA/DMA.mq5

Dynamic MA
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'DMA'}, 'levels': [], 'description': ['Dynamic MA'], 'name': 'DMA', 'source': 'MQL5 Indicators/DMA/DMA.mq5', 'folder': 'DMA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 17, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 17)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferDMA = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
period = 0
handle_ma = 0

def OnInit():
    global handle_ma, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferDMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRAW, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DMA(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDMA, True)
    ArraySetAsSeries(BufferRAW, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferDMA, EMPTY_VALUE)
        ArrayInitialize(BufferRAW, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferRAW)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        A = BufferRAW[i] - BufferRAW[i + period - 1]
        B = 0.0
        for j in range(i, i + period):
            B += fabs(BufferRAW[j] - BufferRAW[j + 1])
        C = _fdiv(A, (B if (B != 0) else Point()))
        D = (C * (2.0 / 31.0)) + ((1 - C) * (2.0 / 3.0))
        E = D * D
        BufferDMA[i] = (E * BufferRAW[i]) + ((1 - E) * BufferDMA[i + 1])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DMA(_MQL5Indicator):
    name = 'DMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 17,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

