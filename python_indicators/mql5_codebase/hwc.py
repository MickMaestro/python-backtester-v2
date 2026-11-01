"""HWC — converted from MQL5: MQL5 Indicators/HWC/HWC.mq5

Holt-Winter Channel indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [3329434], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'HVMA', 2: 'Top', 3: 'Bottom'}, 'levels': [], 'description': ['Holt-Winter Channel indicator'], 'name': 'HWC', 'source': 'MQL5 Indicators/HWC/HWC.mq5', 'folder': 'HWC', 'inputs': [{'mql': 'InpValueA', 'py': 'InpValueA', 'param': 'InpValueA', 'type': 'double', 'default': 0.2, 'label': 'nA (from 0 to 1)', 'sinput': False}, {'mql': 'InpValueB', 'py': 'InpValueB', 'param': 'InpValueB', 'type': 'double', 'default': 0.1, 'label': 'nB (from 0 to 1)', 'sinput': False}, {'mql': 'InpValueC', 'py': 'InpValueC', 'param': 'InpValueC', 'type': 'double', 'default': 0.1, 'label': 'nC (from 0 to 1)', 'sinput': False}, {'mql': 'InpValueD', 'py': 'InpValueD', 'param': 'InpValueD', 'type': 'double', 'default': 0.1, 'label': 'nD (from 0 to 1)', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 1.0, 'label': 'Multiplier', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpValueA = _input('InpValueA', 0.2)  # nA (from 0 to 1)
InpValueB = _input('InpValueB', 0.1)  # nB (from 0 to 1)
InpValueC = _input('InpValueC', 0.1)  # nC (from 0 to 1)
InpValueD = _input('InpValueD', 0.1)  # nD (from 0 to 1)
InpMultiplier = _input('InpMultiplier', 1.0)  # Multiplier
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferHVMA = Arr(0, 0.0)
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferF = Arr(0, 0.0)
BufferV = Arr(0, 0.0)
BufferA = Arr(0, 0.0)
BufferVar = Arr(0, 0.0)
a = 0.0
b = 0.0
c = 0.0
d = 0.0
multiplier = 0.0
handle_ma = 0

def OnInit():
    global a, b, c, d, handle_ma, multiplier
    a = (0 if (InpValueA < 0) else 1 if (InpValueA > 1) else InpValueA)
    b = (0 if (InpValueB < 0) else 1 if (InpValueB > 1) else InpValueB)
    c = (0 if (InpValueC < 0) else 1 if (InpValueC > 1) else InpValueC)
    d = (0 if (InpValueD < 0) else 1 if (InpValueD > 1) else InpValueD)
    multiplier = fabs(InpMultiplier)
    SetIndexBuffer(0, BufferHVMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferF, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferV, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferVar, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Holt-Winter Channel (' + DoubleToString(a, 2) + ',' + DoubleToString(b, 2) + ',' + DoubleToString(c, 2) + ',' + DoubleToString(d, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferHVMA, True)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferF, True)
    ArraySetAsSeries(BufferV, True)
    ArraySetAsSeries(BufferA, True)
    ArraySetAsSeries(BufferVar, True)
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
        ArrayInitialize(BufferHVMA, 0)
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferF, 0)
        ArrayInitialize(BufferV, 0)
        ArrayInitialize(BufferA, 0)
        ArrayInitialize(BufferVar, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferF[i] = ((1.0 - a) * (BufferF[i + 1] + BufferV[i + 1] + (0.5 * BufferA[i + 1]))) + (a * BufferMA[i])
        BufferV[i] = ((1.0 - b) * (BufferV[i + 1] + BufferA[i + 1])) + (b * (BufferF[i] - BufferF[i + 1]))
        BufferA[i] = ((1.0 - c) * BufferA[i + 1]) + (c * (BufferV[i] - BufferV[i + 1]))
        BufferHVMA[i] = BufferF[i] + BufferV[i] + (0.5 * BufferA[i])
        BufferVar[i] = ((1.0 - d) * BufferVar[i + 1]) + (d * (BufferMA[i + 1] - BufferHVMA[i + 1]) * (BufferMA[i + 1] - BufferHVMA[i + 1]))
        Stdt = sqrt(BufferVar[i + 1])
        BufferTop[i] = BufferHVMA[i] + (multiplier * Stdt)
        BufferBottom[i] = BufferHVMA[i] - (multiplier * Stdt)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HWC(_MQL5Indicator):
    name = 'HWC'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpValueA': 0.2,  # nA (from 0 to 1)
        'InpValueB': 0.1,  # nB (from 0 to 1)
        'InpValueC': 0.1,  # nC (from 0 to 1)
        'InpValueD': 0.1,  # nD (from 0 to 1)
        'InpMultiplier': 1.0,  # Multiplier
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

