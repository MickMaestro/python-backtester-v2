"""Sidus_V1_Cloud — converted from MQL5: MQL5 Indicators/Sidus_V1_Cloud/Sidus_V1_Cloud.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 7}, 'colors': {1: [16711680], 2: [16748574], 3: [255], 4: [42495], 5: [15130800, 14804223]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'LWMA1', 2: 'LWMA2', 3: 'EMA1', 4: 'EMA2', 5: 'Cloud'}, 'levels': [], 'description': [], 'name': 'Sidus_V1_Cloud', 'source': 'MQL5 Indicators/Sidus_V1_Cloud/Sidus_V1_Cloud.mq5', 'folder': 'Sidus_V1_Cloud', 'inputs': [{'mql': 'InpPeriodLWMA1', 'py': 'InpPeriodLWMA1', 'param': 'InpPeriodLWMA1', 'type': 'uint', 'default': 5, 'label': 'First LWMA period', 'sinput': False}, {'mql': 'InpPeriodLWMA2', 'py': 'InpPeriodLWMA2', 'param': 'InpPeriodLWMA2', 'type': 'uint', 'default': 8, 'label': 'Second LWMA period', 'sinput': False}, {'mql': 'InpPeriodEMA1', 'py': 'InpPeriodEMA1', 'param': 'InpPeriodEMA1', 'type': 'uint', 'default': 18, 'label': 'First EMA period', 'sinput': False}, {'mql': 'InpPeriodEMA2', 'py': 'InpPeriodEMA2', 'param': 'InpPeriodEMA2', 'type': 'uint', 'default': 28, 'label': 'Second EMA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodLWMA1 = _input('InpPeriodLWMA1', 5)  # First LWMA period
InpPeriodLWMA2 = _input('InpPeriodLWMA2', 8)  # Second LWMA period
InpPeriodEMA1 = _input('InpPeriodEMA1', 18)  # First EMA period
InpPeriodEMA2 = _input('InpPeriodEMA2', 28)  # Second EMA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferLWMA1 = Arr(0, 0.0)
BufferLWMA2 = Arr(0, 0.0)
BufferEMA1 = Arr(0, 0.0)
BufferEMA2 = Arr(0, 0.0)
BufferCloud1 = Arr(0, 0.0)
BufferCloud2 = Arr(0, 0.0)
period_lwma1 = 0
period_lwma2 = 0
period_ema1 = 0
period_ema2 = 0
handle_lwma1 = 0
handle_lwma2 = 0
handle_ema1 = 0
handle_ema2 = 0

def OnInit():
    global handle_ema1, handle_ema2, handle_lwma1, handle_lwma2, period_ema1, period_ema2, period_lwma1, period_lwma2
    period_lwma1 = (1 if (InpPeriodLWMA1 < 1) else InpPeriodLWMA1)
    period_lwma2 = (1 if (InpPeriodLWMA2 < 1) else InpPeriodLWMA2)
    period_ema1 = (1 if (InpPeriodEMA1 < 1) else InpPeriodEMA1)
    period_ema2 = (1 if (InpPeriodEMA2 < 1) else InpPeriodEMA2)
    SetIndexBuffer(0, BufferLWMA1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferLWMA2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferEMA1, INDICATOR_DATA)
    SetIndexBuffer(3, BufferEMA2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferCloud1, INDICATOR_DATA)
    SetIndexBuffer(5, BufferCloud2, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Sidus V1 Cloud (' + _str(period_lwma1) + ',' + _str(period_lwma2) + ',' + _str(period_ema1) + ',' + _str(period_ema2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferLWMA1, True)
    ArraySetAsSeries(BufferLWMA2, True)
    ArraySetAsSeries(BufferEMA1, True)
    ArraySetAsSeries(BufferEMA2, True)
    ArraySetAsSeries(BufferCloud1, True)
    ArraySetAsSeries(BufferCloud2, True)
    ResetLastError()
    handle_lwma1 = iMA(None, PERIOD_CURRENT, period_lwma1, 0, MODE_LWMA, InpAppliedPrice)
    if handle_lwma1 == INVALID_HANDLE:
        Print('The iMA(', _str(period_lwma1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_lwma2 = iMA(None, PERIOD_CURRENT, period_lwma2, 0, MODE_LWMA, InpAppliedPrice)
    if handle_lwma2 == INVALID_HANDLE:
        Print('The iMA(', _str(period_lwma2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ema1 = iMA(None, PERIOD_CURRENT, period_ema1, 0, MODE_EMA, InpAppliedPrice)
    if handle_ema1 == INVALID_HANDLE:
        Print('The iMA(', _str(period_ema1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ema2 = iMA(None, PERIOD_CURRENT, period_ema2, 0, MODE_EMA, InpAppliedPrice)
    if handle_ema2 == INVALID_HANDLE:
        Print('The iMA(', _str(period_ema2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferLWMA1, 0)
        ArrayInitialize(BufferLWMA2, 0)
        ArrayInitialize(BufferEMA1, 0)
        ArrayInitialize(BufferEMA2, 0)
        ArrayInitialize(BufferCloud1, 0)
        ArrayInitialize(BufferCloud2, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_lwma1, 0, 0, count, BufferLWMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_lwma2, 0, 0, count, BufferLWMA2)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ema1, 0, 0, count, BufferEMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ema2, 0, 0, count, BufferEMA2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        MaxEMA = fmax(BufferEMA1[i], BufferEMA2[i])
        MinEMA = fmin(BufferEMA1[i], BufferEMA2[i])
        MaxLWMA = fmax(BufferLWMA1[i], BufferLWMA2[i])
        MinLWMA = fmin(BufferLWMA1[i], BufferLWMA2[i])
        if MinLWMA > MaxEMA:
            BufferCloud1[i] = MinLWMA
            BufferCloud2[i] = MaxEMA
        elif MinEMA > MaxLWMA:
            BufferCloud1[i] = MaxLWMA
            BufferCloud2[i] = MinEMA
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SidusV1Cloud(_MQL5Indicator):
    name = 'Sidus_V1_Cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodLWMA1': 5,  # First LWMA period
        'InpPeriodLWMA2': 8,  # Second LWMA period
        'InpPeriodEMA1': 18,  # First EMA period
        'InpPeriodEMA2': 28,  # Second EMA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

