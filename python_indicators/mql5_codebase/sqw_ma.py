"""SqW_MA — converted from MQL5: MQL5 Indicators/Square Weighted MA/SqW_MA.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SqWMA'}, 'levels': [], 'description': [], 'name': 'SqW_MA', 'source': 'MQL5 Indicators/Square Weighted MA/SqW_MA.mq5', 'folder': 'Square Weighted MA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 40, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 40)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferSqWMA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
summ_p = 0.0
summ_p2 = 0.0
period = 0
handle_ma = 0

def OnInit():
    global handle_ma, period, summ_p, summ_p2
    period = (2 if (InpPeriod < 2) else InpPeriod)
    summ_p = _idiv(period * (period - 1), 2)
    summ_p2 = _idiv(period * (period - 1) * ((2 * period) - 1), 6)
    SetIndexBuffer(0, BufferSqWMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(BufferSqWMA, True)
    ArraySetAsSeries(BufferMA, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Square weighted MA(' + _str(period) + ')')
    ResetLastError()
    handle_ma = iMA(Symbol(), PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1 - period
        ArrayInitialize(BufferSqWMA, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        summ = 0.0
        summ_w = 0.0
        for n in range(0, period):
            summ += BufferMA[i + n]
            summ_w += BufferMA[i + n] * n
        var3 = (summ_p2 * period) - (summ_p * summ_p)
        var2 = _fdiv((summ_w * period) - (summ_p * summ), var3)
        BufferSqWMA[i] = _fdiv(summ - (summ_p * var2), period)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SqWMA(_MQL5Indicator):
    name = 'SqW_MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 40,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

