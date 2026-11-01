"""LWMA_MA — converted from MQL5: MQL5 Indicators/LWMA_MA/LWMA_MA.mq5

LWMA/SMA ratio oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [65280, 36095, 14474460]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'LWMA/SMA'}, 'levels': [], 'description': ['LWMA/SMA ratio oscillator'], 'name': 'LWMA_MA', 'source': 'MQL5 Indicators/LWMA_MA/LWMA_MA.mq5', 'folder': 'LWMA_MA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
BufferDMA = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferLWMA = Arr(0, 0.0)
period = 0
handle_sma = 0
handle_lwma = 0

def OnInit():
    global handle_lwma, handle_sma, period
    period = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferDMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferLWMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferSMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'LWMA/SMA ratio (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDMA, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferLWMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ResetLastError()
    handle_sma = iMA(None, PERIOD_CURRENT, period, 0, MODE_SMA, PRICE_CLOSE)
    if handle_sma == INVALID_HANDLE:
        Print(55, ': The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_lwma = iMA(None, PERIOD_CURRENT, period, 0, MODE_LWMA, PRICE_CLOSE)
    if handle_lwma == INVALID_HANDLE:
        Print(61, ': The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferDMA, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferLWMA, 0)
        ArrayInitialize(BufferSMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_lwma, 0, 0, count, BufferLWMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferDMA[i] = ((_fdiv(BufferLWMA[i], BufferSMA[i]) - 1.0) if (BufferSMA[i] != 0) else 0)
        BufferColors[i] = (0 if (BufferDMA[i] > BufferDMA[i + 1]) else 1 if (BufferDMA[i] < BufferDMA[i + 1]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LWMAMA(_MQL5Indicator):
    name = 'LWMA_MA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
    }

