"""BezierMA — converted from MQL5: MQL5 Indicators/BezierMA/BezierMA.mq5

Bezier-weighting Moving Average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13458026]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Bezier MA'}, 'levels': [], 'description': ['Bezier-weighting Moving Average'], 'name': 'BezierMA', 'source': 'MQL5 Indicators/BezierMA/BezierMA.mq5', 'folder': 'BezierMA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 8, 'label': 'Period', 'sinput': False}, {'mql': 'InpSensitivity', 'py': 'InpSensitivity', 'param': 'InpSensitivity', 'type': 'double', 'default': 0.5, 'label': 'Sensitivity', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 8)  # Period
InpSensitivity = _input('InpSensitivity', 0.5)  # Sensitivity
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferBMA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
Fact = Arr(0, 0.0)
sensitivity = 0.0
period = 0
handle_ma = 0

def OnInit():
    global handle_ma, period, sensitivity
    period = (1 if (InpPeriod < 1) else InpPeriod)
    sensitivity = (0 if (InpSensitivity < 0) else InpSensitivity)
    ArrayResize(Fact, period + 1)
    Fact[0] = 1.0
    for i in range(1, period + 1):
        Fact[i] = Fact[i - 1] * i
    SetIndexBuffer(0, BufferBMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bezier MA (' + _str(period) + ',' + DoubleToString(sensitivity, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferBMA, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferBMA, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        sum_ = 0.0
        for j in range(period, 0 - 1, -1):
            sum_ = sum_ + (BufferMA[i + j] * _fdiv(Fact[period], Fact[j] * Fact[period - j]) * pow(sensitivity, j) * pow(1.0 - sensitivity, period - j))
        BufferBMA[i] = sum_
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BezierMA(_MQL5Indicator):
    name = 'BezierMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 8,  # Period
        'InpSensitivity': 0.5,  # Sensitivity
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

