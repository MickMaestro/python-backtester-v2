"""Effort_Result — converted from MQL5: MQL5 Indicators/Effort_Result/Effort_Result.mq5

Effort Result indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'EResult'}, 'levels': [], 'description': ['Effort Result indicator'], 'name': 'Effort_Result', 'source': 'MQL5 Indicators/Effort_Result/Effort_Result.mq5', 'folder': 'Effort_Result', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
BufferER = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
period = 0
handle_ma = 0

def OnInit():
    global handle_ma, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferER, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferVol, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Effort Result (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferER, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferVol, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period, 0, MODE_SMA, PRICE_CLOSE)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferER, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferVol, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferVol[i] = float(tick_volume[i])
    for i in range(limit, 0 - 1, -1):
        Pr0 = BufferMA[i]
        Pr1 = BufferMA[i + period]
        roc = ((100.0 * (_fdiv(Pr0, Pr1) - 1.0)) if (Pr1 != 0) else 0)
        bh = ArrayMaximum(BufferVol, i, period)
        if bh == WRONG_VALUE:
            continue
        max_ = BufferVol[bh]
        BufferER[i] = (_fdiv(roc, max_ * Point() * Point()) if (max_ != 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EffortResult(_MQL5Indicator):
    name = 'Effort_Result'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
    }

