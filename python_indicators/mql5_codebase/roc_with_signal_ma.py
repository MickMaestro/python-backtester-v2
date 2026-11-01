"""ROC_with_Signal_MA — converted from MQL5: MQL5 Indicators/ROC_with_Signal_MA/ROC_with_Signal_MA.mq5

Rate of Change with signal Moving Average indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [5737262], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Rate of Change', 2: 'Signal'}, 'levels': [], 'description': ['Rate of Change with signal Moving Average indicator'], 'name': 'ROC_with_Signal_MA', 'source': 'MQL5 Indicators/ROC_with_Signal_MA/ROC_with_Signal_MA.mq5', 'folder': 'ROC_with_Signal_MA', 'inputs': [{'mql': 'InpPeriodROC', 'py': 'InpPeriodROC', 'param': 'InpPeriodROC', 'type': 'uint', 'default': 8, 'label': 'ROC period', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 8, 'label': 'Signal MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'Signal MA method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodROC = _input('InpPeriodROC', 8)  # ROC period
InpPeriodSig = _input('InpPeriodSig', 8)  # Signal MA period
InpMethod = _input('InpMethod', MODE_EMA)  # Signal MA method
BufferROC = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
period_roc = 0
period_sig = 0
period_max = 0
weight_sum = 0

def OnInit():
    global period_max, period_roc, period_sig
    period_roc = (1 if (InpPeriodROC < 1) else InpPeriodROC)
    period_sig = (2 if (InpPeriodSig < 2) else InpPeriodSig)
    period_max = fmax(period_roc, period_sig)
    SetIndexBuffer(0, BufferROC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ROC with signal (' + _str(period_roc) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferROC, True)
    ArraySetAsSeries(BufferSignal, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_roc - 1
        ArrayInitialize(BufferROC, 0)
        ArrayInitialize(BufferSignal, 0)
    for i in range(limit, 0 - 1, -1):
        BufferROC[i] = (_fdiv(100.0 * (close[i] - close[i + period_roc]), close[i + period_roc]) if (close[i + period_roc] != 0) else 0)
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        return ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferROC, BufferSignal)
    elif _sw1 == MODE_SMMA:
        return SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferROC, BufferSignal)
    elif _sw1 == MODE_LWMA:
        return LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sig, BufferROC, BufferSignal, _GlobRef(globals(), 'weight_sum'))
    else:
        return SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferROC, BufferSignal)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ROCWithSignalMA(_MQL5Indicator):
    name = 'ROC_with_Signal_MA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodROC': 8,  # ROC period
        'InpPeriodSig': 8,  # Signal MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Signal MA method
    }

