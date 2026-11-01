"""VA — converted from MQL5: MQL5 Indicators/VA/VA.mq5

Velocity/Acceleration
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Velocity', 2: 'Acceleration'}, 'levels': [], 'description': ['Velocity/Acceleration'], 'name': 'VA', 'source': 'MQL5 Indicators/VA/VA.mq5', 'folder': 'VA', 'inputs': [{'mql': 'InpPeriodV', 'py': 'InpPeriodV', 'param': 'InpPeriodV', 'type': 'uint', 'default': 14, 'label': 'Velocity period', 'sinput': False}, {'mql': 'InpPeriodA', 'py': 'InpPeriodA', 'param': 'InpPeriodA', 'type': 'uint', 'default': 10, 'label': 'Acceleration period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodV = _input('InpPeriodV', 14)  # Velocity period
InpPeriodA = _input('InpPeriodA', 10)  # Acceleration period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferV = Arr(0, 0.0)
BufferA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_v = 0
period_a = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_a, period_v
    period_v = (1 if (InpPeriodV < 1) else InpPeriodV)
    period_a = (1 if (InpPeriodA < 1) else InpPeriodA)
    SetIndexBuffer(0, BufferV, INDICATOR_DATA)
    SetIndexBuffer(1, BufferA, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VA(' + _str(period_v) + ',' + _str(period_a) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferV, True)
    ArraySetAsSeries(BufferA, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = fmax(period_a, period_v)
    if rates_total < max_:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - max_ - 1
        ArrayInitialize(BufferV, EMPTY_VALUE)
        ArrayInitialize(BufferA, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        v = BufferMA[i + period_v]
        a = BufferV[i + period_a]
        BufferV[i] = _fdiv(100 * BufferMA[i], (v if (v != 0) else DBL_MIN))
        BufferA[i] = _fdiv(100 * BufferV[i], (a if (a != 0) else DBL_MIN))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VA(_MQL5Indicator):
    name = 'VA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodV': 14,  # Velocity period
        'InpPeriodA': 10,  # Acceleration period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

