"""BB-Decimal — converted from MQL5: MQL5 Indicators/BB-Decimal/BB-Decimal.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [32768]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper', 2: 'Middle', 3: 'Lower'}, 'levels': [], 'description': [], 'name': 'BB-Decimal', 'source': 'MQL5 Indicators/BB-Decimal/BB-Decimal.mq5', 'folder': 'BB-Decimal', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 2.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpDeviation = _input('InpDeviation', 2.0)  # Deviation
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferUpper = Arr(0, 0.0)
BufferMiddle = Arr(0, 0.0)
BufferLower = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
period = 0
deviation = 0.0
handle_ma = 0
handle_dev = 0

def OnInit():
    global deviation, handle_dev, handle_ma, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    deviation = (0.01 if (InpDeviation < 0.01) else InpDeviation)
    SetIndexBuffer(0, BufferUpper, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMiddle, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLower, INDICATOR_DATA)
    SetIndexBuffer(3, BufferDev, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'BB-Decimal')
    ArraySetAsSeries(BufferUpper, True)
    ArraySetAsSeries(BufferMiddle, True)
    ArraySetAsSeries(BufferLower, True)
    ArraySetAsSeries(BufferDev, True)
    ResetLastError()
    handle_ma = iMA(Symbol(), PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_dev = iStdDev(Symbol(), PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_dev == INVALID_HANDLE:
        Print('The iStdDev(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferUpper, EMPTY_VALUE)
        ArrayInitialize(BufferMiddle, EMPTY_VALUE)
        ArrayInitialize(BufferLower, EMPTY_VALUE)
        ArrayInitialize(BufferDev, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMiddle)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_dev, 0, 0, count, BufferDev)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferUpper[i] = BufferMiddle[i] + (deviation * BufferDev[i])
        BufferLower[i] = BufferMiddle[i] - (deviation * BufferDev[i])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBDecimal(_MQL5Indicator):
    name = 'BB-Decimal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpDeviation': 2.0,  # Deviation
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

