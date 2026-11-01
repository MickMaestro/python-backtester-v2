"""TOSC — converted from MQL5: MQL5 Indicators/TOSC/TOSC.mq5

Difference between the recursive trendline value
      and the exponential moving average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TOSC'}, 'levels': [], 'description': ['Difference between the recursive trendline value', '      and the exponential moving average'], 'name': 'TOSC', 'source': 'MQL5 Indicators/TOSC/TOSC.mq5', 'folder': 'TOSC', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferTOSC = Arr(0, 0.0)
BufferTMP0 = Arr(0, 0.0)
BufferTMP1 = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferEMA = Arr(0, 0.0)
alpha = 0.0
period = 0
handle_ma = 0
handle_ema = 0

def OnInit():
    global alpha, handle_ema, handle_ma, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    alpha = _fdiv(2.0, float(period) + 1)
    SetIndexBuffer(0, BufferTOSC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTMP0, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferTMP1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferEMA, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'TOSC(' + _str(period) + ')')
    ArraySetAsSeries(BufferTOSC, True)
    ArraySetAsSeries(BufferTMP0, True)
    ArraySetAsSeries(BufferTMP1, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferEMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_ema = iMA(None, PERIOD_CURRENT, period, 0, MODE_EMA, InpAppliedPrice)
    if handle_ema == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferTOSC, EMPTY_VALUE)
        ArrayInitialize(BufferTMP0, 0)
        ArrayInitialize(BufferTMP1, 0)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferEMA, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ema, 0, 0, count, BufferEMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferTMP0[i] = ((1 - alpha) * BufferTMP0[i + 1]) + BufferMA[i]
        BufferTMP1[i] = ((1 - alpha) * BufferTMP1[i + 1]) + (alpha * (BufferMA[i] + BufferTMP0[i] - BufferTMP0[i + 1]))
        BufferTOSC[i] = _fdiv(BufferTMP1[i] - BufferEMA[i], Point())
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TOSC(_MQL5Indicator):
    name = 'TOSC'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

