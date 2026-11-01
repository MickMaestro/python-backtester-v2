"""WMA — converted from MQL5: MQL5 Indicators/WMA/WMA.mq5

Wilder's smoothing average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'WMA'}, 'levels': [], 'description': ["Wilder's smoothing average"], 'name': 'WMA', 'source': 'MQL5 Indicators/WMA/WMA.mq5', 'folder': 'WMA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferWMA = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
k = 0.0
period = 0
handle_ma1 = 0
handle_maP = 0

def OnInit():
    global handle_ma1, handle_maP, k, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    k = _fdiv(1.0, float(period))
    SetIndexBuffer(0, BufferWMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMAP, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Wilders smoothing average (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferWMA, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMAP, True)
    ResetLastError()
    handle_maP = iMA(None, PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 2
        ArrayInitialize(BufferWMA, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMAP, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMAP)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - period - 2):
            BufferWMA[i] = BufferMAP[i]
        else:
            BufferWMA[i] = ((BufferMA1[i] - BufferWMA[i + 1]) * k) + BufferWMA[i + 1]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WMA(_MQL5Indicator):
    name = 'WMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

