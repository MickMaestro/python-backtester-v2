"""ADX_Difference — converted from MQL5: MQL5 Indicators/ADX_Difference/ADX_Difference.mq5

ADX Difference indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Difference'}, 'levels': [], 'description': ['ADX Difference indicator'], 'name': 'ADX_Difference', 'source': 'MQL5 Indicators/ADX_Difference/ADX_Difference.mq5', 'folder': 'ADX_Difference', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'ADX Period', 'sinput': False}, {'mql': 'InpDifference', 'py': 'InpDifference', 'param': 'InpDifference', 'type': 'uint', 'default': 1, 'label': 'Difference', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # ADX Period
InpDifference = _input('InpDifference', 1)  # Difference
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferADXD = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferADX = Arr(0, 0.0)
period = 0
difference = 0
handle_adx = 0

def OnInit():
    global difference, handle_adx, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    difference = (1 if (InpDifference < 1) else InpDifference)
    SetIndexBuffer(0, BufferADXD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferADX, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ADX Difference (' + _str(period) + ',' + _str(difference) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferADXD, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferADX, True)
    ResetLastError()
    handle_adx = iADX(None, PERIOD_CURRENT, period)
    if handle_adx == INVALID_HANDLE:
        Print('The iADX(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - difference - 1
        ArrayInitialize(BufferADXD, EMPTY_VALUE)
        ArrayInitialize(BufferADX, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_adx, MAIN_LINE, 0, count, BufferADX)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferADXD[i] = BufferADX[i] - BufferADX[i + difference]
        BufferColors[i] = (1 if (BufferADXD[i] > BufferADXD[i + 1]) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ADXDifference(_MQL5Indicator):
    name = 'ADX_Difference'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # ADX Period
        'InpDifference': 1,  # Difference
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

