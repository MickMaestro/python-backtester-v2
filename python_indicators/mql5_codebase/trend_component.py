"""Trend_Component — converted from MQL5: MQL5 Indicators/Trend_Component/Trend_Component.mq5

The Trend Component indicator of John Ehlers
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2237106]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TC'}, 'levels': [], 'description': ['The Trend Component indicator of John Ehlers'], 'name': 'Trend_Component', 'source': 'MQL5 Indicators/Trend_Component/Trend_Component.mq5', 'folder': 'Trend_Component', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 11, 'label': 'Period', 'sinput': False}, {'mql': 'InpDelta', 'py': 'InpDelta', 'param': 'InpDelta', 'type': 'double', 'default': 0.05, 'label': 'Delta', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 11)  # Period
InpDelta = _input('InpDelta', 0.05)  # Delta
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferTC = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferBP = Arr(0, 0.0)
period_ma = 0
handle_ma = 0
delta = 0.0
alpha = 0.0
beta = 0.0
gamma = 0.0

def OnInit():
    global alpha, beta, delta, gamma, handle_ma, period_ma
    period_ma = (2 if (InpPeriod < 2) else InpPeriod)
    delta = InpDelta
    beta = cos(_fdiv(2.0 * M_PI, period_ma))
    gamma = _fdiv(1.0, cos(_fdiv(4.0 * M_PI * delta, period_ma)))
    alpha = gamma * sqrt((gamma * gamma) - 1.0)
    SetIndexBuffer(0, BufferTC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferBP, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend Component (' + _str(period_ma) + ',' + DoubleToString(delta, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTC, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferBP, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= (period_ma * 2):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 3
        ArrayInitialize(BufferTC, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferBP, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferBP[i] = (0.5 * (1.0 - alpha) * (BufferMA[i] - BufferMA[i + 2])) + (beta * (1.0 + alpha) * BufferBP[i + 1]) - (alpha * BufferBP[i + 2])
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, (2 * period_ma) + 1, BufferBP, BufferTC)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendComponent(_MQL5Indicator):
    name = 'Trend_Component'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 11,  # Period
        'InpDelta': 0.05,  # Delta
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

