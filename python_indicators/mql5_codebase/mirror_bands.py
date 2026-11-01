"""Mirror_Bands — converted from MQL5: MQL5 Indicators/Mirror_Bands/Mirror_Bands.mq5

Mirror bands
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [14772545], 2: [14772545], 3: [32768], 4: [17919]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 2, 2: 2, 3: 0, 4: 0}, 'labels': {1: 'Top', 2: 'Bottom', 3: 'MA', 4: 'Mirror'}, 'levels': [], 'description': ['Mirror bands'], 'name': 'Mirror_Bands', 'source': 'MQL5 Indicators/Mirror_Bands/Mirror_Bands.mq5', 'folder': 'Mirror_Bands', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 9, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 2, 'label': 'MA period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 2.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 9)  # Period
InpPeriodMA = _input('InpPeriodMA', 2)  # MA period
InpDeviation = _input('InpDeviation', 2.0)  # Deviation
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferMirror = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMAInd = Arr(0, 0.0)
deviation = 0.0
period = 0
period_ma = 0
handle_ma = 0
handle_ma1 = 0
handle_ma_ind = 0

def OnInit():
    global deviation, handle_ma, handle_ma1, handle_ma_ind, period, period_ma
    period = (1 if (InpPeriod < 1) else InpPeriod)
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    deviation = InpDeviation
    SetIndexBuffer(0, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMirror, INDICATOR_DATA)
    SetIndexBuffer(4, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMAInd, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MBands(' + _str(period) + ',' + _str(period_ma) + ',' + DoubleToString(deviation, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferMirror, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMAInd, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_ma_ind = iMA(None, PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma_ind == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferMirror, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMAInd, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma_ind, 0, 0, count, BufferMAInd)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        Sum = 0.0
        for j in range(0, period):
            New = BufferMA1[i + j] - BufferMAInd[i]
            Sum = Sum + (New * New)
        Dev = deviation * sqrt(_fdiv(Sum, period))
        BufferTop[i] = BufferMAInd[i] + Dev
        BufferBottom[i] = BufferMAInd[i] - Dev
        BufferMirror[i] = (2 * BufferMAInd[i]) - BufferMA[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MirrorBands(_MQL5Indicator):
    name = 'Mirror_Bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 9,  # Period
        'InpPeriodMA': 2,  # MA period
        'InpDeviation': 2.0,  # Deviation
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

