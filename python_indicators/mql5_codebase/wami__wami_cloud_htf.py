"""WAMI — converted from MQL5: MQL5 Indicators/WAMI_Cloud_HTF/WAMI.mq5

Momentum Indicator by Anthony W.Warren
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'WAMI', 2: 'Signal'}, 'levels': [], 'description': ['Momentum Indicator by Anthony W.Warren'], 'name': 'WAMI', 'source': 'MQL5 Indicators/WAMI_Cloud_HTF/WAMI.mq5', 'folder': 'WAMI_Cloud_HTF', 'inputs': [{'mql': 'InpPeriodMA1', 'py': 'InpPeriodMA1', 'param': 'InpPeriodMA1', 'type': 'uint', 'default': 4, 'label': 'First MA period', 'sinput': False}, {'mql': 'InpMethodMA1', 'py': 'InpMethodMA1', 'param': 'InpMethodMA1', 'type': 'int', 'default': 0, 'label': 'First MA method', 'sinput': False}, {'mql': 'InpPeriodMA2', 'py': 'InpPeriodMA2', 'param': 'InpPeriodMA2', 'type': 'uint', 'default': 13, 'label': 'Second MA period', 'sinput': False}, {'mql': 'InpMethodMA2', 'py': 'InpMethodMA2', 'param': 'InpMethodMA2', 'type': 'int', 'default': 0, 'label': 'Second MA method', 'sinput': False}, {'mql': 'InpPeriodMA3', 'py': 'InpPeriodMA3', 'param': 'InpPeriodMA3', 'type': 'uint', 'default': 13, 'label': 'Third MA period', 'sinput': False}, {'mql': 'InpMethodMA3', 'py': 'InpMethodMA3', 'param': 'InpMethodMA3', 'type': 'int', 'default': 0, 'label': 'Third MA method', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 4, 'label': 'Signal MA period', 'sinput': False}, {'mql': 'InpMethodSig', 'py': 'InpMethodSig', 'param': 'InpMethodSig', 'type': 'int', 'default': 0, 'label': 'Signal MA method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodMA1 = _input('InpPeriodMA1', 4)  # First MA period
InpMethodMA1 = _input('InpMethodMA1', MODE_SMA)  # First MA method
InpPeriodMA2 = _input('InpPeriodMA2', 13)  # Second MA period
InpMethodMA2 = _input('InpMethodMA2', MODE_SMA)  # Second MA method
InpPeriodMA3 = _input('InpPeriodMA3', 13)  # Third MA period
InpMethodMA3 = _input('InpMethodMA3', MODE_SMA)  # Third MA method
InpPeriodSig = _input('InpPeriodSig', 4)  # Signal MA period
InpMethodSig = _input('InpMethodSig', MODE_SMA)  # Signal MA method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferWAMI = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferDiff = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferMA3 = Arr(0, 0.0)
BufferSigMA = Arr(0, 0.0)
period_ma1 = 0
period_ma2 = 0
period_ma3 = 0
period_sig = 0
period_max = 0
weight_sum = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ma1, period_ma2, period_ma3, period_max, period_sig
    period_ma1 = (2 if (InpPeriodMA1 < 2) else InpPeriodMA1)
    period_ma2 = (2 if (InpPeriodMA2 < 2) else InpPeriodMA2)
    period_ma3 = (2 if (InpPeriodMA3 < 2) else InpPeriodMA3)
    period_sig = (2 if (InpPeriodSig < 2) else InpPeriodSig)
    period_max = fmax(period_ma1, fmax(period_ma2, fmax(period_ma3, period_sig)))
    SetIndexBuffer(0, BufferWAMI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferDiff, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferMA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferSigMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Warren Momentum (' + _str(period_ma1) + ',' + _str(period_ma2) + ',' + _str(period_ma3) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferWAMI, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferDiff, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferMA3, True)
    ArraySetAsSeries(BufferSigMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_max or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferWAMI, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferDiff, 0)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
        ArrayInitialize(BufferMA3, 0)
        ArrayInitialize(BufferSigMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferDiff[i] = BufferMA[i] - BufferMA[i + 1]
    _sw1 = InpMethodMA1
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma1, BufferDiff, BufferMA1)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ma1, BufferDiff, BufferMA1)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ma1, BufferDiff, BufferMA1, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ma1, BufferDiff, BufferMA1)
    _sw2 = InpMethodMA2
    if _sw2 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_ma1, period_ma2, BufferMA1, BufferMA2)
    elif _sw2 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_ma1, period_ma2, BufferMA1, BufferMA2)
    elif _sw2 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ma1, period_ma2, BufferMA1, BufferMA2, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_ma1, period_ma2, BufferMA1, BufferMA2)
    _sw3 = InpMethodMA3
    if _sw3 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_ma2, period_ma3, BufferMA2, BufferMA3)
    elif _sw3 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_ma2, period_ma3, BufferMA2, BufferMA3)
    elif _sw3 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ma2, period_ma3, BufferMA2, BufferMA3, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_ma2, period_ma3, BufferMA2, BufferMA3)
    _sw4 = InpMethodSig
    if _sw4 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_ma3, period_sig, BufferMA3, BufferSigMA)
    elif _sw4 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_ma3, period_sig, BufferMA3, BufferSigMA)
    elif _sw4 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ma3, period_sig, BufferMA3, BufferSigMA, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_ma3, period_sig, BufferMA3, BufferSigMA)
    for i in range(limit, 0 - 1, -1):
        BufferWAMI[i] = _fdiv(BufferMA3[i], Point())
        BufferSignal[i] = _fdiv(BufferSigMA[i], Point())
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WAMI(_MQL5Indicator):
    name = 'WAMI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA1': 4,  # First MA period
        'InpMethodMA1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # First MA method
        'InpPeriodMA2': 13,  # Second MA period
        'InpMethodMA2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Second MA method
        'InpPeriodMA3': 13,  # Third MA period
        'InpMethodMA3': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Third MA method
        'InpPeriodSig': 4,  # Signal MA period
        'InpMethodSig': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Signal MA method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

