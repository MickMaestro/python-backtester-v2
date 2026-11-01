"""BB-Percentage-Decimal — converted from MQL5: MQL5 Indicators/BB-Percentage-Decimal/BB-Percentage-Decimal.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3329330]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'BB'}, 'levels': [], 'description': [], 'name': 'BB-Percentage-Decimal', 'source': 'MQL5 Indicators/BB-Percentage-Decimal/BB-Percentage-Decimal.mq5', 'folder': 'BB-Percentage-Decimal', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 2.0, 'label': 'Bands Deviation', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpDeviation = _input('InpDeviation', 2.0)  # Bands Deviation
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferBB = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
period = 0
handle_ma = 0
handle_ma1 = 0
handle_dev = 0
deviation = 0.0

def OnInit():
    global deviation, handle_dev, handle_ma, handle_ma1, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    deviation = (0.1 if (InpDeviation < 0.1) else InpDeviation)
    SetIndexBuffer(0, BufferBB, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferDev, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'BB-Percentage-Decimal')
    ArraySetAsSeries(BufferBB, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferDev, True)
    ResetLastError()
    handle_ma = iMA(Symbol(), PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_ma1 = iMA(Symbol(), PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_dev = iStdDev(Symbol(), PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_dev == INVALID_HANDLE:
        Print('The iStdDev(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 2:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferBB, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, EMPTY_VALUE)
        ArrayInitialize(BufferDev, EMPTY_VALUE)
    copied = 0
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_dev, 0, 0, count, BufferDev)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if BufferDev[i] == 0:
            continue
        BufferBB[i] = _fdiv(BufferMA1[i] - BufferMA[i] + (deviation * BufferDev[i]), 2.0 * deviation * BufferDev[i]) * 100.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBPercentageDecimal(_MQL5Indicator):
    name = 'BB-Percentage-Decimal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpDeviation': 2.0,  # Bands Deviation
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

