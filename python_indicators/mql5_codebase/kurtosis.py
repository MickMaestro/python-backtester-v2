"""Kurtosis — converted from MQL5: MQL5 Indicators/Kurtosis/Kurtosis.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [255], 2: [255], 3: [255], 4: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Kurtosis', 2: 'Momentum', 3: 'RAW', 4: 'MA'}, 'levels': [], 'description': [], 'name': 'Kurtosis', 'source': 'MQL5 Indicators/Kurtosis/Kurtosis.mq5', 'folder': 'Kurtosis', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 4, 'label': 'Period of momentum', 'sinput': False}, {'mql': 'InpPeriodSmooth1', 'py': 'InpPeriodSmooth1', 'param': 'InpPeriodSmooth1', 'type': 'uint', 'default': 66, 'label': 'Primary smoothing period', 'sinput': False}, {'mql': 'InpPeriodSmooth2', 'py': 'InpPeriodSmooth2', 'param': 'InpPeriodSmooth2', 'type': 'uint', 'default': 3, 'label': 'Secondary smoothing period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 4)  # Period of momentum
InpPeriodSmooth1 = _input('InpPeriodSmooth1', 66)  # Primary smoothing period
InpPeriodSmooth2 = _input('InpPeriodSmooth2', 3)  # Secondary smoothing period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferKurtosis = Arr(0, 0.0)
BufferMomentum = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferSmooth = Arr(0, 0.0)
handle_ma = 0
period_momentum = 0
period_smooth1 = 0
period_smooth2 = 0

def OnInit():
    global handle_ma, period_momentum, period_smooth1, period_smooth2
    period_momentum = (1 if (InpPeriod < 1) else InpPeriod)
    period_smooth1 = (1 if (InpPeriodSmooth1 < 1) else InpPeriodSmooth1)
    period_smooth2 = (1 if (InpPeriodSmooth2 < 1) else InpPeriodSmooth2)
    SetIndexBuffer(0, BufferKurtosis, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMomentum, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSmooth, INDICATOR_CALCULATIONS)
    PlotIndexSetString(0, PLOT_LABEL, 'Kurtosis(' + _str(period_momentum) + ')')
    IndicatorSetString(INDICATOR_SHORTNAME, 'Kurtosis(' + _str(period_momentum) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferKurtosis, True)
    ArraySetAsSeries(BufferMomentum, True)
    ArraySetAsSeries(BufferRAW, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferSmooth, True)
    ResetLastError()
    handle_ma = iMA(Symbol(), PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_momentum or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_momentum - 1
        ArrayInitialize(BufferKurtosis, 0)
        ArrayInitialize(BufferMomentum, 0)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferSmooth, EMPTY_VALUE)
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferMomentum[i] = BufferMA[i] - BufferMA[i + period_momentum]
        BufferRAW[i] = _fdiv(BufferMomentum[i] - BufferMomentum[i + 1], Point())
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_smooth1, BufferRAW, BufferSmooth)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_smooth2, BufferSmooth, BufferKurtosis)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Kurtosis(_MQL5Indicator):
    name = 'Kurtosis'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 4,  # Period of momentum
        'InpPeriodSmooth1': 66,  # Primary smoothing period
        'InpPeriodSmooth2': 3,  # Secondary smoothing period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

