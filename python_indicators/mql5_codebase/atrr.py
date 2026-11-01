"""ATRR — converted from MQL5: MQL5 Indicators/ATRR/ATRR.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [32768]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ATRR'}, 'levels': [], 'description': [], 'name': 'ATRR', 'source': 'MQL5 Indicators/ATRR/ATRR.mq5', 'folder': 'ATRR', 'inputs': [{'mql': 'InpPeriodATR1', 'py': 'InpPeriodATR1', 'param': 'InpPeriodATR1', 'type': 'uint', 'default': 10, 'label': 'ATR1 Period', 'sinput': False}, {'mql': 'InpPeriodATR2', 'py': 'InpPeriodATR2', 'param': 'InpPeriodATR2', 'type': 'uint', 'default': 20, 'label': 'ATR2 Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodATR1 = _input('InpPeriodATR1', 10)  # ATR1 Period
InpPeriodATR2 = _input('InpPeriodATR2', 20)  # ATR2 Period
BufferATRR = Arr(0, 0.0)
BufferATR1 = Arr(0, 0.0)
BufferATR2 = Arr(0, 0.0)
period_atr1 = 0
period_atr2 = 0
handle_atr1 = 0
handle_atr2 = 0

def OnInit():
    global handle_atr1, handle_atr2, period_atr1, period_atr2
    period_atr1 = (1 if (InpPeriodATR1 < 1) else InpPeriodATR1)
    period_atr2 = (1 if (InpPeriodATR2 < 1) else InpPeriodATR2)
    SetIndexBuffer(0, BufferATRR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferATR1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferATR2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATRR(' + _str(period_atr1) + ',' + _str(period_atr2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferATR1, True)
    ArraySetAsSeries(BufferATR2, True)
    ArraySetAsSeries(BufferATRR, True)
    ResetLastError()
    handle_atr1 = iATR(None, PERIOD_CURRENT, period_atr1)
    if handle_atr1 == INVALID_HANDLE:
        Print('The first iATR(', _str(period_atr1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_atr2 = iATR(None, PERIOD_CURRENT, period_atr2)
    if handle_atr2 == INVALID_HANDLE:
        Print('The second iATR(', _str(period_atr2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 2:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferATR1, EMPTY_VALUE)
        ArrayInitialize(BufferATR2, EMPTY_VALUE)
        ArrayInitialize(BufferATRR, EMPTY_VALUE)
    copied = 0
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_atr1, 0, 0, count, BufferATR1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr2, 0, 0, count, BufferATR2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        one = BufferATR1[i]
        two = BufferATR2[i]
        BufferATRR[i] = _fdiv(one, (two if (two > 0) else DBL_MIN)) * 100.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRR(_MQL5Indicator):
    name = 'ATRR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodATR1': 10,  # ATR1 Period
        'InpPeriodATR2': 20,  # ATR2 Period
    }

