"""SineWMA — converted from MQL5: MQL5 Indicators/SineWMA/SineWMA.mq5

Sine Weighted Moving Average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14772545]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SineWMA'}, 'levels': [], 'description': ['Sine Weighted Moving Average'], 'name': 'SineWMA', 'source': 'MQL5 Indicators/SineWMA/SineWMA.mq5', 'folder': 'SineWMA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferSineWMA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
SinCoeff = Arr(0, 0.0)
coeff_sum = 0.0
period_ma = 0
handle_ma = 0

def OnInit():
    global coeff_sum, handle_ma, period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    ArrayResize(SinCoeff, period_ma)
    coeff_sum = 0.0
    for i in range(0, period_ma):
        SinCoeff[i] = sin(_fdiv(M_PI * (1.0 + i), 1.0 + period_ma))
        coeff_sum += SinCoeff[i]
    SetIndexBuffer(0, BufferSineWMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Sine WMA (' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferSineWMA, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ma - 1
        ArrayInitialize(BufferSineWMA, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        sum_ = 0.0
        for j in range(0, period_ma):
            sum_ += SinCoeff[j] * BufferMA[i + j]
        BufferSineWMA[i] = _fdiv(sum_, coeff_sum)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SineWMA(_MQL5Indicator):
    name = 'SineWMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

