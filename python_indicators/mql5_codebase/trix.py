"""Trix — converted from MQL5: MQL5 Indicators/TRiX/Trix.mq5

Trix oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [255], 2: [32768], 3: [32768, 255, 11119017]}, 'widths': {1: 1, 2: 1, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Trix', 2: 'Signal', 3: 'Histogram'}, 'levels': [], 'description': ['Trix oscillator'], 'name': 'Trix', 'source': 'MQL5 Indicators/TRiX/Trix.mq5', 'folder': 'TRiX', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod1', 'py': 'InpMethod1', 'param': 'InpMethod1', 'type': 'int', 'default': 0, 'label': 'First MA method', 'sinput': False}, {'mql': 'InpMethod2', 'py': 'InpMethod2', 'param': 'InpMethod2', 'type': 'int', 'default': 0, 'label': 'Second MA method', 'sinput': False}, {'mql': 'InpMethod3', 'py': 'InpMethod3', 'param': 'InpMethod3', 'type': 'int', 'default': 0, 'label': 'Third MA method', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpMethodSig', 'py': 'InpMethodSig', 'param': 'InpMethodSig', 'type': 'int', 'default': 0, 'label': 'Signal method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod1 = _input('InpMethod1', MODE_SMA)  # First MA method
InpMethod2 = _input('InpMethod2', MODE_SMA)  # Second MA method
InpMethod3 = _input('InpMethod3', MODE_SMA)  # Third MA method
InpPeriodSig = _input('InpPeriodSig', 9)  # Signal period
InpMethodSig = _input('InpMethodSig', MODE_SMA)  # Signal method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferTrix = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferHist = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferMA3 = Arr(0, 0.0)
period_ma = 0
period_sig = 0
handle_ma = 0
weight_sum2 = 0
weight_sum3 = 0
weight_sumS = 0

def OnInit():
    global handle_ma, period_ma, period_sig
    period_ma = (2 if (InpPeriod < 2) else InpPeriod)
    period_sig = (2 if (InpPeriodSig < 2) else InpPeriodSig)
    SetIndexBuffer(0, BufferTrix, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHist, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferMA3, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trix (' + MethodToString(InpMethod1) + '(' + _str(period_ma) + '),' + MethodToString(InpMethod2) + '(' + _str(period_ma) + '),' + MethodToString(InpMethod3) + '(' + _str(period_ma) + '))')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTrix, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferHist, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferMA3, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethod1, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ma, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferTrix, 0)
        ArrayInitialize(BufferSignal, 0)
        ArrayInitialize(BufferHist, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
        ArrayInitialize(BufferMA3, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    _sw1 = InpMethod2
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_ma, period_ma, BufferMA1, BufferMA2) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_ma, period_ma, BufferMA1, BufferMA2) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ma, period_ma, BufferMA1, BufferMA2, _GlobRef(globals(), 'weight_sum2')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_ma, period_ma, BufferMA1, BufferMA2) == 0:
            return 0
    _sw2 = InpMethod3
    if _sw2 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_ma, period_ma, BufferMA2, BufferMA3) == 0:
            return 0
    elif _sw2 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_ma, period_ma, BufferMA2, BufferMA3) == 0:
            return 0
    elif _sw2 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ma, period_ma, BufferMA2, BufferMA3, _GlobRef(globals(), 'weight_sum3')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_ma, period_ma, BufferMA2, BufferMA3) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        MA3_0 = BufferMA3[i]
        MA3_1 = BufferMA3[i + 1]
        BufferTrix[i] = (_fdiv(_fdiv(MA3_0 - MA3_1, MA3_1), Point()) if (MA3_1 != 0) else 0)
    _sw3 = InpMethodSig
    if _sw3 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_ma, period_sig, BufferTrix, BufferSignal) == 0:
            return 0
    elif _sw3 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_ma, period_sig, BufferTrix, BufferSignal) == 0:
            return 0
    elif _sw3 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ma, period_sig, BufferTrix, BufferSignal, _GlobRef(globals(), 'weight_sumS')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_ma, period_sig, BufferTrix, BufferSignal) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferHist[i] = BufferTrix[i] - BufferSignal[i]
        BufferColors[i] = (0 if (BufferHist[i] > BufferHist[i + 1]) else 1 if (BufferHist[i] < BufferHist[i + 1]) else 2)
    return rates_total

def MethodToString(method):
    return StringSubstr(EnumToString(method, 'ENUM_MA_METHOD'), 5)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trix(_MQL5Indicator):
    name = 'Trix'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMethod1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # First MA method
        'InpMethod2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Second MA method
        'InpMethod3': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Third MA method
        'InpPeriodSig': 9,  # Signal period
        'InpMethodSig': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Signal method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

