"""ADMIR — converted from MQL5: MQL5 Indicators/ADMIR/ADMIR.mq5

Average Directional Movement Index Rating indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3329330]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ADMIR'}, 'levels': [], 'description': ['Average Directional Movement Index Rating indicator'], 'name': 'ADMIR', 'source': 'MQL5 Indicators/ADMIR/ADMIR.mq5', 'folder': 'ADMIR', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'ADX Period', 'sinput': False}, {'mql': 'InpDifference', 'py': 'InpDifference', 'param': 'InpDifference', 'type': 'uint', 'default': 14, 'label': 'Difference', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # ADX Period
InpDifference = _input('InpDifference', 14)  # Difference
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferADMIR = Arr(0, 0.0)
BufferADX1 = Arr(0, 0.0)
BufferADX2 = Arr(0, 0.0)
period = 0
difference = 0
handle_adx1 = 0
handle_adx2 = 0

def OnInit():
    global difference, handle_adx1, handle_adx2, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    difference = (1 if (InpDifference < 1) else InpDifference)
    SetIndexBuffer(0, BufferADMIR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferADX1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferADX2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ADM Index Rating (' + _str(period) + ',' + _str(difference) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferADMIR, True)
    ArraySetAsSeries(BufferADX1, True)
    ArraySetAsSeries(BufferADX2, True)
    ResetLastError()
    handle_adx1 = iADX(None, PERIOD_CURRENT, period)
    if handle_adx1 == INVALID_HANDLE:
        Print('The iADX(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_adx2 = iADX(None, PERIOD_CURRENT, period + difference)
    if handle_adx2 == INVALID_HANDLE:
        Print('The iADX(', _str(period + difference), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferADMIR, EMPTY_VALUE)
        ArrayInitialize(BufferADX1, 0)
        ArrayInitialize(BufferADX2, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_adx1, MAIN_LINE, 0, count, BufferADX1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx2, MAIN_LINE, 0, count, BufferADX2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferADMIR[i] = (BufferADX1[i] + BufferADX2[i]) / 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ADMIR(_MQL5Indicator):
    name = 'ADMIR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # ADX Period
        'InpDifference': 14,  # Difference
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

