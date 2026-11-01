"""UDP — converted from MQL5: MQL5 Indicators/UDP/UDP.mq5

Up/Down Percentage indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Up', 2: 'Down'}, 'levels': [], 'description': ['Up/Down Percentage indicator'], 'name': 'UDP', 'source': 'MQL5 Indicators/UDP/UDP.mq5', 'folder': 'UDP', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferFUP = Arr(0, 0.0)
BufferFDN = Arr(0, 0.0)
period_ind = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ind
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferFUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferFDN, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Up/Down Percentage (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferFUP, True)
    ArraySetAsSeries(BufferFDN, True)
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
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferFUP, 0)
        ArrayInitialize(BufferFDN, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferFDN[i] = 0.0
        BufferFUP[i] = BufferFDN[i]
        if BufferMA[i] > BufferMA[i + 1]:
            BufferFUP[i] = 1.0
        elif BufferMA[i] < BufferMA[i + 1]:
            BufferFDN[i] = 1.0
    if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferFUP, BufferUP) == 0:
        return 0
    if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferFDN, BufferDN) == 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UDP(_MQL5Indicator):
    name = 'UDP'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

