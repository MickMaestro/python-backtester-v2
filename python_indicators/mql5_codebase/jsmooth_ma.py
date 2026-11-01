"""JSmooth_MA — converted from MQL5: MQL5 Indicators/JSmooth_MA/JSmooth_MA.mq5

JSmooth Moving Average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [1993170]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'JSMA'}, 'levels': [], 'description': ['JSmooth Moving Average'], 'name': 'JSmooth_MA', 'source': 'MQL5 Indicators/JSmooth_MA/JSmooth_MA.mq5', 'folder': 'JSmooth_MA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferJSMA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferA1 = Arr(0, 0.0)
BufferA2 = Arr(0, 0.0)
BufferA3 = Arr(0, 0.0)
BufferA4 = Arr(0, 0.0)
alpha = 0.0
alpha2 = 0.0
alpha12 = 0.0
period = 0
handle_ma = 0

def OnInit():
    global alpha, alpha12, alpha2, handle_ma, period
    period = (2 if (InpPeriod < 2) else InpPeriod)
    alpha = _fdiv(0.45 * float(period - 1), (0.45 * (period - 1)) + 2)
    alpha2 = alpha * alpha
    alpha12 = (1 - alpha) * (1 - alpha)
    SetIndexBuffer(0, BufferJSMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferA4, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'JSMA(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferJSMA, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferA1, True)
    ArraySetAsSeries(BufferA2, True)
    ArraySetAsSeries(BufferA3, True)
    ArraySetAsSeries(BufferA4, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferJSMA, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferA1, 0)
        ArrayInitialize(BufferA2, 0)
        ArrayInitialize(BufferA3, 0)
        ArrayInitialize(BufferA4, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferA1[i] = ((1 - alpha) * BufferMA[i]) + (alpha * BufferA1[i + 1])
        BufferA2[i] = ((1 - alpha) * (BufferMA[i] - BufferA1[i])) + (alpha * BufferA2[i + 1])
        BufferA3[i] = BufferA1[i] + BufferA2[i]
        BufferA4[i] = ((BufferA3[i] - BufferJSMA[i + 1]) * alpha12) + (alpha2 * BufferA4[i + 1])
        BufferJSMA[i] = BufferJSMA[i + 1] + BufferA4[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JSmoothMA(_MQL5Indicator):
    name = 'JSmooth_MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

