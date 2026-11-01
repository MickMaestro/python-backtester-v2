"""FTNP — converted from MQL5: MQL5 Indicators/FTNP/FTNP.mq5

Fisher Transform of Normalized Prices indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [3329330], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Fisher', 2: 'Trigger'}, 'levels': [], 'description': ['Fisher Transform of Normalized Prices indicator'], 'name': 'FTNP', 'source': 'MQL5 Indicators/FTNP/FTNP.mq5', 'folder': 'FTNP', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferFisher = Arr(0, 0.0)
BufferTrigger = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferV = Arr(0, 0.0)
period = 0
handle_ma = 0

def OnInit():
    global handle_ma, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferFisher, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTrigger, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferV, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fisher Transform of Normalized Prices (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferFisher, True)
    ArraySetAsSeries(BufferTrigger, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferV, True)
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
        ArrayInitialize(BufferFisher, 0)
        ArrayInitialize(BufferTrigger, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferV, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        bl = ArrayMinimum(BufferMA, i, period)
        bh = ArrayMaximum(BufferMA, i, period)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        MinPr = BufferMA[bl]
        MaxPr = BufferMA[bh]
        if MaxPr != MinPr:
            BufferV[i] = 0.667 * (_fdiv(BufferMA[i] - MinPr, MaxPr - MinPr) - 0.5 + BufferV[i + 1])
            BufferV[i] = fmin(BufferV[i], 0.999)
            BufferV[i] = fmax(BufferV[i], -0.999)
            BufferFisher[i] = 0.5 * (log(_fdiv(1.0 + BufferV[i], 1.0 - BufferV[i])) + BufferFisher[i + 1])
            BufferTrigger[i] = BufferFisher[i + 1]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FTNP(_MQL5Indicator):
    name = 'FTNP'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

