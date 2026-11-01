"""TCI — converted from MQL5: MQL5 Indicators/TCI/TCI.mq5

Trading Channel Index indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2263842]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TChannel Idx'}, 'levels': [], 'description': ['Trading Channel Index indicator'], 'name': 'TCI', 'source': 'MQL5 Indicators/TCI/TCI.mq5', 'folder': 'TCI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodAVG', 'py': 'InpPeriodAVG', 'param': 'InpPeriodAVG', 'type': 'uint', 'default': 21, 'label': 'Average period', 'sinput': False}, {'mql': 'InpCoeff', 'py': 'InpCoeff', 'param': 'InpCoeff', 'type': 'double', 'default': 0.015, 'label': 'Coefficient', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpPeriodAVG = _input('InpPeriodAVG', 21)  # Average period
InpCoeff = _input('InpCoeff', 0.015)  # Coefficient
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferTCI = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
BufferRAW1 = Arr(0, 0.0)
BufferRAW2 = Arr(0, 0.0)
BufferAvgRAW = Arr(0, 0.0)
coeff = 0.0
period_tpi = 0
period_avg = 0
handle_ma1 = 0
handle_maP = 0

def OnInit():
    global coeff, handle_ma1, handle_maP, period_avg, period_tpi
    period_tpi = (2 if (InpPeriod < 2) else InpPeriod)
    period_avg = (2 if (InpPeriodAVG < 2) else InpPeriodAVG)
    coeff = (0.0001 if (InpCoeff == 0) else InpCoeff)
    SetIndexBuffer(0, BufferTCI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMAP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferRAW1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferRAW2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferAvgRAW, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trading Channel Index (' + _str(period_tpi) + ',' + _str(period_avg) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTCI, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMAP, True)
    ArraySetAsSeries(BufferRAW1, True)
    ArraySetAsSeries(BufferRAW2, True)
    ArraySetAsSeries(BufferAvgRAW, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maP = iMA(None, PERIOD_CURRENT, period_tpi, 0, MODE_EMA, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period_tpi), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferTCI, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMAP, 0)
        ArrayInitialize(BufferRAW1, 0)
        ArrayInitialize(BufferRAW2, 0)
        ArrayInitialize(BufferAvgRAW, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMAP)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferRAW1[i] = fabs(BufferMA1[i] - BufferMAP[i])
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_tpi, BufferRAW1, BufferAvgRAW) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferRAW2[i] = (_fdiv(BufferMA1[i] - BufferMAP[i], coeff * BufferAvgRAW[i]) if (BufferAvgRAW[i] != 0) else 0)
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_avg, BufferRAW2, BufferTCI) == 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TCI(_MQL5Indicator):
    name = 'TCI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpPeriodAVG': 21,  # Average period
        'InpCoeff': 0.015,  # Coefficient
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

