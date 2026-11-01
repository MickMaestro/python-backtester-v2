"""T3_MA — converted from MQL5: MQL5 Indicators/T3_MA/T3_MA.mq5

Tim Tillson's T3 MA
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [5737262]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'T3MA'}, 'levels': [], 'description': ["Tim Tillson's T3 MA"], 'name': 'T3_MA', 'source': 'MQL5 Indicators/T3_MA/T3_MA.mq5', 'folder': 'T3_MA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpCoeffB', 'py': 'InpCoeffB', 'param': 'InpCoeffB', 'type': 'double', 'default': 0.88, 'label': 'Coefficient', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpCoeffB = _input('InpCoeffB', 0.88)  # Coefficient
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferT3MA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferE1 = Arr(0, 0.0)
BufferE2 = Arr(0, 0.0)
BufferE3 = Arr(0, 0.0)
BufferE4 = Arr(0, 0.0)
BufferE5 = Arr(0, 0.0)
BufferE6 = Arr(0, 0.0)
period = 0
handle_ma = 0
c1 = 0.0
c2 = 0.0
c3 = 0.0
c4 = 0.0
w1 = 0.0
w2 = 0.0

def OnInit():
    global c1, c2, c3, c4, handle_ma, period, w1, w2
    period = (1 if (InpPeriod < 1) else InpPeriod)
    b2 = 0.0
    b3 = 0.0
    b2 = InpCoeffB * InpCoeffB
    b3 = b2 * InpCoeffB
    w1 = _fdiv(4.0, 3.0 + period)
    w2 = 1.0 - w1
    c1 = -b3
    c2 = 3 * (b2 + b3)
    c3 = -3 * ((2 * b2) + InpCoeffB + b3)
    c4 = 1 + (3 * InpCoeffB) + b3 + (3 * b2)
    SetIndexBuffer(0, BufferT3MA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferE1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferE2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferE3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferE4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferE5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferE6, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'T3MA(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferT3MA, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferE1, True)
    ArraySetAsSeries(BufferE2, True)
    ArraySetAsSeries(BufferE3, True)
    ArraySetAsSeries(BufferE4, True)
    ArraySetAsSeries(BufferE5, True)
    ArraySetAsSeries(BufferE6, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferT3MA, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferE1, 0)
        ArrayInitialize(BufferE2, 0)
        ArrayInitialize(BufferE3, 0)
        ArrayInitialize(BufferE4, 0)
        ArrayInitialize(BufferE5, 0)
        ArrayInitialize(BufferE6, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferE1[i] = (w1 * BufferMA[i]) + (w2 * BufferE1[i + 1])
        BufferE2[i] = (w1 * BufferE1[i]) + (w2 * BufferE2[i + 1])
        BufferE3[i] = (w1 * BufferE2[i]) + (w2 * BufferE3[i + 1])
        BufferE4[i] = (w1 * BufferE3[i]) + (w2 * BufferE4[i + 1])
        BufferE5[i] = (w1 * BufferE4[i]) + (w2 * BufferE5[i + 1])
        BufferE6[i] = (w1 * BufferE5[i]) + (w2 * BufferE6[i + 1])
        BufferT3MA[i] = (c1 * BufferE6[i]) + (c2 * BufferE5[i]) + (c3 * BufferE4[i]) + (c4 * BufferE3[i])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3MA(_MQL5Indicator):
    name = 'T3_MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpCoeffB': 0.88,  # Coefficient
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

