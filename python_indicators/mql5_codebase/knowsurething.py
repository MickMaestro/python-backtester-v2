"""KnowSureThing — converted from MQL5: MQL5 Indicators/Know Sure Thing/KnowSureThing.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [8951296], 2: [3556340]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'KST', 2: 'Signal'}, 'levels': [], 'description': [], 'name': 'KnowSureThing', 'source': 'MQL5 Indicators/Know Sure Thing/KnowSureThing.mq5', 'folder': 'Know Sure Thing', 'inputs': [{'mql': 'InpPeriodROC1', 'py': 'InpPeriodROC1', 'param': 'InpPeriodROC1', 'type': 'uint', 'default': 10, 'label': 'ROC Length #1', 'sinput': False}, {'mql': 'InpPeriodROC2', 'py': 'InpPeriodROC2', 'param': 'InpPeriodROC2', 'type': 'uint', 'default': 15, 'label': 'ROC Length #2', 'sinput': False}, {'mql': 'InpPeriodROC3', 'py': 'InpPeriodROC3', 'param': 'InpPeriodROC3', 'type': 'uint', 'default': 20, 'label': 'ROC Length #3', 'sinput': False}, {'mql': 'InpPeriodROC4', 'py': 'InpPeriodROC4', 'param': 'InpPeriodROC4', 'type': 'uint', 'default': 30, 'label': 'ROC Length #4', 'sinput': False}, {'mql': 'InpPeriodSMA1', 'py': 'InpPeriodSMA1', 'param': 'InpPeriodSMA1', 'type': 'uint', 'default': 10, 'label': 'SMA Length #1', 'sinput': False}, {'mql': 'InpPeriodSMA2', 'py': 'InpPeriodSMA2', 'param': 'InpPeriodSMA2', 'type': 'uint', 'default': 10, 'label': 'SMA Length #2', 'sinput': False}, {'mql': 'InpPeriodSMA3', 'py': 'InpPeriodSMA3', 'param': 'InpPeriodSMA3', 'type': 'uint', 'default': 10, 'label': 'SMA Length #3', 'sinput': False}, {'mql': 'InpPeriodSMA4', 'py': 'InpPeriodSMA4', 'param': 'InpPeriodSMA4', 'type': 'uint', 'default': 15, 'label': 'SMA Length #4', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 9, 'label': 'Signal Line Length', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodROC1 = _input('InpPeriodROC1', 10)  # ROC Length #1
InpPeriodROC2 = _input('InpPeriodROC2', 15)  # ROC Length #2
InpPeriodROC3 = _input('InpPeriodROC3', 20)  # ROC Length #3
InpPeriodROC4 = _input('InpPeriodROC4', 30)  # ROC Length #4
InpPeriodSMA1 = _input('InpPeriodSMA1', 10)  # SMA Length #1
InpPeriodSMA2 = _input('InpPeriodSMA2', 10)  # SMA Length #2
InpPeriodSMA3 = _input('InpPeriodSMA3', 10)  # SMA Length #3
InpPeriodSMA4 = _input('InpPeriodSMA4', 15)  # SMA Length #4
InpPeriodSig = _input('InpPeriodSig', 9)  # Signal Line Length
ExtBufferKST = Arr(0, 0.0)
ExtBufferSignal = Arr(0, 0.0)
ExtBufferROC1 = Arr(0, 0.0)
ExtBufferROC2 = Arr(0, 0.0)
ExtBufferROC3 = Arr(0, 0.0)
ExtBufferROC4 = Arr(0, 0.0)
ExtBufferSMA1 = Arr(0, 0.0)
ExtBufferSMA2 = Arr(0, 0.0)
ExtBufferSMA3 = Arr(0, 0.0)
ExtBufferSMA4 = Arr(0, 0.0)
ExtPeriodROC1 = 0
ExtPeriodROC2 = 0
ExtPeriodROC3 = 0
ExtPeriodROC4 = 0
ExtPeriodSMA1 = 0
ExtPeriodSMA2 = 0
ExtPeriodSMA3 = 0
ExtPeriodSMA4 = 0
ExtPeriodSig = 0

def OnInit():
    global ExtPeriodROC1, ExtPeriodROC2, ExtPeriodROC3, ExtPeriodROC4, ExtPeriodSMA1, ExtPeriodSMA2, ExtPeriodSMA3, ExtPeriodSMA4, ExtPeriodSig
    SetIndexBuffer(0, ExtBufferKST, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, ExtBufferROC1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtBufferROC2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtBufferROC3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtBufferROC4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ExtBufferSMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, ExtBufferSMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, ExtBufferSMA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, ExtBufferSMA4, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtBufferKST, True)
    ArraySetAsSeries(ExtBufferSignal, True)
    ArraySetAsSeries(ExtBufferROC1, True)
    ArraySetAsSeries(ExtBufferROC2, True)
    ArraySetAsSeries(ExtBufferROC3, True)
    ArraySetAsSeries(ExtBufferROC4, True)
    ArraySetAsSeries(ExtBufferSMA1, True)
    ArraySetAsSeries(ExtBufferSMA2, True)
    ArraySetAsSeries(ExtBufferSMA3, True)
    ArraySetAsSeries(ExtBufferSMA4, True)
    ExtPeriodROC1 = (1 if (InpPeriodROC1 < 1) else InpPeriodROC1)
    ExtPeriodROC2 = (1 if (InpPeriodROC2 < 1) else InpPeriodROC2)
    ExtPeriodROC3 = (1 if (InpPeriodROC3 < 1) else InpPeriodROC3)
    ExtPeriodROC4 = (1 if (InpPeriodROC4 < 1) else InpPeriodROC4)
    ExtPeriodSMA1 = (2 if (InpPeriodSMA1 < 2) else InpPeriodSMA1)
    ExtPeriodSMA2 = (2 if (InpPeriodSMA2 < 2) else InpPeriodSMA2)
    ExtPeriodSMA3 = (2 if (InpPeriodSMA3 < 2) else InpPeriodSMA3)
    ExtPeriodSMA4 = (2 if (InpPeriodSMA4 < 2) else InpPeriodSMA4)
    ExtPeriodSig = (2 if (InpPeriodSig < 2) else InpPeriodSig)
    param = StringFormat('KST (%lu, %lu, %lu, %lu, %lu, %lu, %lu, %lu, %lu)', ExtPeriodROC1, ExtPeriodROC2, ExtPeriodROC3, ExtPeriodROC4, ExtPeriodSMA1, ExtPeriodSMA2, ExtPeriodSMA3, ExtPeriodSMA4, ExtPeriodSig)
    IndicatorSetString(INDICATOR_SHORTNAME, param)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    roc_max = fmax(ExtPeriodROC1, fmax(ExtPeriodROC2, fmax(ExtPeriodROC3, ExtPeriodROC4)))
    sma_max = fmax(ExtPeriodSMA1, fmax(ExtPeriodSMA2, fmax(ExtPeriodSMA3, ExtPeriodSMA4)))
    max_ = fmax(roc_max, sma_max)
    if rates_total < roc_max:
        return 0
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1 - max_
        ArrayInitialize(ExtBufferKST, EMPTY_VALUE)
        ArrayInitialize(ExtBufferSignal, EMPTY_VALUE)
        ArrayInitialize(ExtBufferROC1, 0)
        ArrayInitialize(ExtBufferROC2, 0)
        ArrayInitialize(ExtBufferROC3, 0)
        ArrayInitialize(ExtBufferROC4, 0)
        ArrayInitialize(ExtBufferSMA1, 0)
        ArrayInitialize(ExtBufferSMA2, 0)
        ArrayInitialize(ExtBufferSMA3, 0)
        ArrayInitialize(ExtBufferSMA4, 0)
    for i in range(limit, 0 - 1, -1):
        ExtBufferROC1[i] = GetROC(i, ExtPeriodROC1, close)
        ExtBufferROC2[i] = GetROC(i, ExtPeriodROC2, close)
        ExtBufferROC3[i] = GetROC(i, ExtPeriodROC3, close)
        ExtBufferROC4[i] = GetROC(i, ExtPeriodROC4, close)
    if SimpleMAOnBuffer(rates_total, prev_calculated, 0, ExtPeriodSMA1, ExtBufferROC1, ExtBufferSMA1) == 0:
        return 0
    if SimpleMAOnBuffer(rates_total, prev_calculated, 0, ExtPeriodSMA2, ExtBufferROC2, ExtBufferSMA2) == 0:
        return 0
    if SimpleMAOnBuffer(rates_total, prev_calculated, 0, ExtPeriodSMA3, ExtBufferROC3, ExtBufferSMA3) == 0:
        return 0
    if SimpleMAOnBuffer(rates_total, prev_calculated, 0, ExtPeriodSMA4, ExtBufferROC4, ExtBufferSMA4) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        ExtBufferKST[i] = ExtBufferSMA1[i] + (2 * ExtBufferSMA2[i]) + (3 * ExtBufferSMA3[i]) + (4 * ExtBufferSMA4[i])
    return SimpleMAOnBuffer(rates_total, prev_calculated, max_, ExtPeriodSig, ExtBufferKST, ExtBufferSignal)

def GetROC(index, period, price):
    return ((_fdiv(price[index] - price[index + period], price[index]) * 100.0) if (price[index] != 0) else 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KnowSureThing(_MQL5Indicator):
    name = 'KnowSureThing'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodROC1': 10,  # ROC Length #1
        'InpPeriodROC2': 15,  # ROC Length #2
        'InpPeriodROC3': 20,  # ROC Length #3
        'InpPeriodROC4': 30,  # ROC Length #4
        'InpPeriodSMA1': 10,  # SMA Length #1
        'InpPeriodSMA2': 10,  # SMA Length #2
        'InpPeriodSMA3': 10,  # SMA Length #3
        'InpPeriodSMA4': 15,  # SMA Length #4
        'InpPeriodSig': 9,  # Signal Line Length
    }

