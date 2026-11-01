"""ZScore — converted from MQL5: MQL5 Indicators/ZScore/ZScore.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ZScore'}, 'levels': [], 'description': [], 'name': 'ZScore', 'source': 'MQL5 Indicators/ZScore/ZScore.mq5', 'folder': 'ZScore', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period of calculation', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period of calculation
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferZScore = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
period = 0
handle_dev = 0
handle_ma1 = 0
handle_ma2 = 0

def OnInit():
    global handle_dev, handle_ma1, handle_ma2, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferZScore, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA2, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'ZScore(' + _str(period) + ')')
    ArraySetAsSeries(BufferZScore, True)
    ArraySetAsSeries(BufferDev, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    handle_dev = iStdDev(Symbol(), PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_dev == INVALID_HANDLE:
        Print("Error creating StdDev's handle: ", GetLastError())
        return INIT_FAILED
    handle_ma1 = iMA(Symbol(), PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print("Error creating MA(1)'s handle: ", GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(Symbol(), PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('Error creating MA(', _str(period), ")'s handle: ", GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferZScore, EMPTY_VALUE)
        ArrayInitialize(BufferDev, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, EMPTY_VALUE)
        ArrayInitialize(BufferMA2, EMPTY_VALUE)
    copied = (rates_total if (limit > 1) else 1)
    copied_dev = CopyBuffer(handle_dev, 0, 0, copied, BufferDev)
    if copied_dev != copied:
        return 0
    copied_ma1 = CopyBuffer(handle_ma1, 0, 0, copied, BufferMA1)
    if copied_ma1 != copied:
        return 0
    copied_ma2 = CopyBuffer(handle_ma2, 0, 0, copied, BufferMA2)
    if copied_ma2 != copied:
        return 0
    for i in range(limit, 0 - 1, -1):
        dev = BufferDev[i]
        BufferZScore[i] = _fdiv(BufferMA1[i] - BufferMA2[i], (dev if (dev > 0) else DBL_MIN))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZScore(_MQL5Indicator):
    name = 'ZScore'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period of calculation
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

