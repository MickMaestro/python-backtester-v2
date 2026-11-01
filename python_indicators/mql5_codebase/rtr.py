"""RTR — converted from MQL5: MQL5 Indicators/RTR/RTR.mq5

Range To Range indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'RTR'}, 'levels': [], 'description': ['Range To Range indicator'], 'name': 'RTR', 'source': 'MQL5 Indicators/RTR/RTR.mq5', 'folder': 'RTR', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 2, 'label': 'Fast ATR Period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 7, 'label': 'Slow ATR Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 2)  # Fast ATR Period
InpPeriodSlow = _input('InpPeriodSlow', 7)  # Slow ATR Period
BufferRTR = Arr(0, 0.0)
BufferFATR = Arr(0, 0.0)
BufferSATR = Arr(0, 0.0)
period_fast = 0
period_slow = 0
handle_fatr = 0
handle_satr = 0

def OnInit():
    global handle_fatr, handle_satr, period_fast, period_slow
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = ((period_fast + 1) if (InpPeriodSlow == period_fast) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    SetIndexBuffer(0, BufferRTR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferFATR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferSATR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Range To Range (' + _str(period_fast) + ',' + _str(period_slow) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferRTR, True)
    ArraySetAsSeries(BufferFATR, True)
    ArraySetAsSeries(BufferSATR, True)
    ResetLastError()
    handle_fatr = iATR(None, PERIOD_CURRENT, period_fast)
    if handle_fatr == INVALID_HANDLE:
        Print('The iATR(', _str(period_fast), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_satr = iATR(None, PERIOD_CURRENT, period_slow)
    if handle_satr == INVALID_HANDLE:
        Print('The iATR(', _str(period_slow), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferRTR, EMPTY_VALUE)
        ArrayInitialize(BufferFATR, 0)
        ArrayInitialize(BufferSATR, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fatr, 0, 0, count, BufferFATR)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_satr, 0, 0, count, BufferSATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferRTR[i] = _fdiv(100.0 * BufferFATR[i], (BufferSATR[i] if (BufferSATR[i] != 0) else 1.0))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RTR(_MQL5Indicator):
    name = 'RTR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 2,  # Fast ATR Period
        'InpPeriodSlow': 7,  # Slow ATR Period
    }

