"""MA_Difference — converted from MQL5: MQL5 Indicators/MA_Difference/MA_Difference.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16760576], 2: [2330219], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Difference', 2: 'MA1', 3: 'MA2'}, 'levels': [], 'description': [], 'name': 'MA_Difference', 'source': 'MQL5 Indicators/MA_Difference/MA_Difference.mq5', 'folder': 'MA_Difference', 'inputs': [{'mql': 'InpPeriodMA1', 'py': 'InpPeriodMA1', 'param': 'InpPeriodMA1', 'type': 'uint', 'default': 14, 'label': 'MA1 period', 'sinput': False}, {'mql': 'InpMethodMA1', 'py': 'InpMethodMA1', 'param': 'InpMethodMA1', 'type': 'int', 'default': 0, 'label': 'MA1 method', 'sinput': False}, {'mql': 'InpPeriodMA2', 'py': 'InpPeriodMA2', 'param': 'InpPeriodMA2', 'type': 'uint', 'default': 14, 'label': 'MA2 period', 'sinput': False}, {'mql': 'InpMethodMA2', 'py': 'InpMethodMA2', 'param': 'InpMethodMA2', 'type': 'int', 'default': 1, 'label': 'MA2 method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpAbsolute', 'py': 'InpAbsolute', 'param': 'InpAbsolute', 'type': 'int', 'default': 1, 'label': 'Absolute difference', 'sinput': False}, {'mql': 'InpShowDiff', 'py': 'InpShowDiff', 'param': 'InpShowDiff', 'type': 'int', 'default': 1, 'label': 'Show difference MA1/MA2', 'sinput': False}, {'mql': 'InpShowMA1', 'py': 'InpShowMA1', 'param': 'InpShowMA1', 'type': 'int', 'default': 1, 'label': 'Show MA1', 'sinput': False}, {'mql': 'InpShowMA2', 'py': 'InpShowMA2', 'param': 'InpShowMA2', 'type': 'int', 'default': 1, 'label': 'Show MA2', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodMA1 = _input('InpPeriodMA1', 14)  # MA1 period
InpMethodMA1 = _input('InpMethodMA1', MODE_SMA)  # MA1 method
InpPeriodMA2 = _input('InpPeriodMA2', 14)  # MA2 period
InpMethodMA2 = _input('InpMethodMA2', MODE_EMA)  # MA2 method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpAbsolute = _input('InpAbsolute', INPUT_YES)  # Absolute difference
InpShowDiff = _input('InpShowDiff', INPUT_YES)  # Show difference MA1/MA2
InpShowMA1 = _input('InpShowMA1', INPUT_YES)  # Show MA1
InpShowMA2 = _input('InpShowMA2', INPUT_YES)  # Show MA2
BufferDiff = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferTmpMA = Arr(0, 0.0)
BufferTmpMA1 = Arr(0, 0.0)
BufferTmpMA2 = Arr(0, 0.0)
period_ma1 = 0
period_ma2 = 0
handle_ma = 0
handle_ma1 = 0
handle_ma2 = 0

def OnInit():
    global handle_ma, handle_ma1, handle_ma2, period_ma1, period_ma2
    period_ma1 = (1 if (InpPeriodMA1 < 1) else InpPeriodMA1)
    period_ma2 = (1 if (InpPeriodMA2 < 1) else InpPeriodMA2)
    SetIndexBuffer(0, BufferDiff, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA2, INDICATOR_DATA)
    SetIndexBuffer(3, BufferTmpMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferTmpMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferTmpMA2, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'MA difference(' + _str(period_ma1) + ',' + _str(period_ma2) + ')')
    ArraySetAsSeries(BufferDiff, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferTmpMA, True)
    ArraySetAsSeries(BufferTmpMA1, True)
    ArraySetAsSeries(BufferTmpMA2, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, period_ma1, 0, InpMethodMA1, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_ma2 = iMA(None, PERIOD_CURRENT, period_ma2, 0, InpMethodMA2, InpAppliedPrice)
    if handle_ma2 == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferDiff, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, EMPTY_VALUE)
        ArrayInitialize(BufferMA2, EMPTY_VALUE)
        ArrayInitialize(BufferTmpMA, EMPTY_VALUE)
        ArrayInitialize(BufferTmpMA1, EMPTY_VALUE)
        ArrayInitialize(BufferTmpMA2, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferTmpMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferTmpMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma2, 0, 0, count, BufferTmpMA2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        Pr = BufferTmpMA[i]
        MA1 = BufferTmpMA1[i]
        MA2 = BufferTmpMA2[i]
        BufferMA1[i] = ((_fdiv(fabs(MA1 - Pr), Point()) if InpAbsolute else _fdiv(MA1 - Pr, Point())) if InpShowMA1 else EMPTY_VALUE)
        BufferMA2[i] = ((_fdiv(fabs(MA2 - Pr), Point()) if InpAbsolute else _fdiv(MA2 - Pr, Point())) if InpShowMA2 else EMPTY_VALUE)
        BufferDiff[i] = ((_fdiv(fabs(MA1 - MA2), Point()) if InpAbsolute else _fdiv(MA1 - MA2, Point())) if InpShowDiff else EMPTY_VALUE)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MADifference(_MQL5Indicator):
    name = 'MA_Difference'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA1': 14,  # MA1 period
        'InpMethodMA1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA1 method
        'InpPeriodMA2': 14,  # MA2 period
        'InpMethodMA2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA2 method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpAbsolute': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Absolute difference
        'InpShowDiff': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show difference MA1/MA2
        'InpShowMA1': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show MA1
        'InpShowMA2': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show MA2
    }

