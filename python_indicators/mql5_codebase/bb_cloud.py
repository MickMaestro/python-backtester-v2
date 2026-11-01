"""BB_Cloud — converted from MQL5: MQL5 Indicators/BB_Cloud/BB_Cloud.mq5

Double-deviation Bollinger Band with cloud indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 7, 3: 7}, 'colors': {1: [14599344], 2: [11920639, 11920639], 3: [16443110, 16443110]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Middle', 2: 'Top Cloud H;Top Cloud L', 3: 'Bottom Cloud H;Bottom Cloud L'}, 'levels': [], 'description': ['Double-deviation Bollinger Band with cloud indicator'], 'name': 'BB_Cloud', 'source': 'MQL5 Indicators/BB_Cloud/BB_Cloud.mq5', 'folder': 'BB_Cloud', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpDeviation1', 'py': 'InpDeviation1', 'param': 'InpDeviation1', 'type': 'double', 'default': 2.0, 'label': 'First deviation', 'sinput': False}, {'mql': 'InpDeviation2', 'py': 'InpDeviation2', 'param': 'InpDeviation2', 'type': 'double', 'default': 3.0, 'label': 'Second deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpDeviation1 = _input('InpDeviation1', 2.0)  # First deviation
InpDeviation2 = _input('InpDeviation2', 3.0)  # Second deviation
BufferMiddle = Arr(0, 0.0)
BufferTopCloud1 = Arr(0, 0.0)
BufferTopCloud2 = Arr(0, 0.0)
BufferBottomCloud1 = Arr(0, 0.0)
BufferBottomCloud2 = Arr(0, 0.0)
deviation1 = 0.0
deviation2 = 0.0
period = 0
handle_bb1 = 0
handle_bb2 = 0

def OnInit():
    global deviation1, deviation2, handle_bb1, handle_bb2, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    deviation1 = InpDeviation1
    deviation2 = InpDeviation2
    SetIndexBuffer(0, BufferMiddle, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTopCloud1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferTopCloud2, INDICATOR_DATA)
    SetIndexBuffer(3, BufferBottomCloud1, INDICATOR_DATA)
    SetIndexBuffer(4, BufferBottomCloud2, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Double Bollinger Band (' + _str(period) + ',' + DoubleToString(deviation1, 1) + ',' + DoubleToString(deviation2, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMiddle, True)
    ArraySetAsSeries(BufferTopCloud1, True)
    ArraySetAsSeries(BufferTopCloud2, True)
    ArraySetAsSeries(BufferBottomCloud1, True)
    ArraySetAsSeries(BufferBottomCloud2, True)
    ResetLastError()
    handle_bb1 = iBands(None, PERIOD_CURRENT, period, 0, deviation1, PRICE_CLOSE)
    if handle_bb1 == INVALID_HANDLE:
        Print('The iBands(', _str(period), ',', DoubleToString(deviation1, 1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_bb2 = iBands(None, PERIOD_CURRENT, period, 0, deviation2, PRICE_CLOSE)
    if handle_bb2 == INVALID_HANDLE:
        Print('The iBands(', _str(period), ',', DoubleToString(deviation2, 1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferMiddle, EMPTY_VALUE)
        ArrayInitialize(BufferTopCloud1, EMPTY_VALUE)
        ArrayInitialize(BufferTopCloud2, EMPTY_VALUE)
        ArrayInitialize(BufferBottomCloud1, EMPTY_VALUE)
        ArrayInitialize(BufferBottomCloud2, EMPTY_VALUE)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_bb2, UPPER_BAND, 0, count, BufferTopCloud1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb1, UPPER_BAND, 0, count, BufferTopCloud2)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb1, LOWER_BAND, 0, count, BufferBottomCloud1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb2, LOWER_BAND, 0, count, BufferBottomCloud2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferMiddle[i] = (BufferTopCloud1[i] + BufferBottomCloud1[i]) / 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBCloud(_MQL5Indicator):
    name = 'BB_Cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpDeviation1': 2.0,  # First deviation
        'InpDeviation2': 3.0,  # Second deviation
    }

