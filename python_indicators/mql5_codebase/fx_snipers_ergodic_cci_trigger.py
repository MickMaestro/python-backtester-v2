"""Fx_Snipers_Ergodic_CCI_Trigger — converted from MQL5: MQL5 Indicators/Fx_Snipers_Ergodic_CCI_Trigger/Fx_Snipers_Ergodic_CCI_Trigger.mq5

Fx Sniper's Ergodic CCI Trigger oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65280], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'ECCI', 2: 'Trigger'}, 'levels': [], 'description': ["Fx Sniper's Ergodic CCI Trigger oscillator"], 'name': 'Fx_Snipers_Ergodic_CCI_Trigger', 'source': 'MQL5 Indicators/Fx_Snipers_Ergodic_CCI_Trigger/Fx_Snipers_Ergodic_CCI_Trigger.mq5', 'folder': 'Fx_Snipers_Ergodic_CCI_Trigger', 'inputs': [{'mql': 'InpPeriodQ', 'py': 'InpPeriodQ', 'param': 'InpPeriodQ', 'type': 'uint', 'default': 4, 'label': 'Period Q', 'sinput': False}, {'mql': 'InpPeriodR', 'py': 'InpPeriodR', 'param': 'InpPeriodR', 'type': 'uint', 'default': 8, 'label': 'Period R', 'sinput': False}, {'mql': 'InpPeriodS', 'py': 'InpPeriodS', 'param': 'InpPeriodS', 'type': 'uint', 'default': 5, 'label': 'Period S', 'sinput': False}, {'mql': 'InpTrigger', 'py': 'InpTrigger', 'param': 'InpTrigger', 'type': 'uint', 'default': 4, 'label': 'Trigger', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 150.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -150.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodQ = _input('InpPeriodQ', 4)  # Period Q
InpPeriodR = _input('InpPeriodR', 8)  # Period R
InpPeriodS = _input('InpPeriodS', 5)  # Period S
InpTrigger = _input('InpTrigger', 4)  # Trigger
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpOverbought = _input('InpOverbought', 150.0)  # Overbought
InpOversold = _input('InpOversold', -150.0)  # Oversold
BufferECCI = Arr(0, 0.0)
BufferTrigger = Arr(0, 0.0)
BufferMOM = Arr(0, 0.0)
BufferAbsMOM = Arr(0, 0.0)
BufferVar1 = Arr(0, 0.0)
BufferVar2 = Arr(0, 0.0)
BufferVar2a = Arr(0, 0.0)
BufferVar2b = Arr(0, 0.0)
BufferVar2c = Arr(0, 0.0)
BufferVar3 = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_q = 0
period_r = 0
period_s = 0
trigger = 0
period_max = 0
weight_sum1 = 0
weight_sum2 = 0
weight_sum3 = 0
weight_sum4 = 0
weight_sum5 = 0
weight_sum6 = 0
weight_sum7 = 0

def OnInit():
    global overbought, oversold, period_max, period_q, period_r, period_s, trigger
    period_q = (2 if (InpPeriodQ < 2) else InpPeriodQ)
    period_r = (2 if (InpPeriodR < 2) else InpPeriodR)
    period_s = (2 if (InpPeriodS < 2) else InpPeriodS)
    trigger = (2 if (InpTrigger < 2) else InpTrigger)
    period_max = fmax(trigger, fmax(period_q, fmax(period_r, period_s)))
    overbought = (0.001 if (fabs(InpOverbought) < 0.001) else fabs(InpOverbought))
    oversold = (-0.001 if ((-fabs(InpOversold)) > -0.001) else (-fabs(InpOversold)))
    SetIndexBuffer(0, BufferECCI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTrigger, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMOM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferAbsMOM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferVar1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferVar2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferVar2a, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferVar2b, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferVar2c, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferVar3, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, "Fx Sniper's Ergodic CCI Trigger (" + _str(period_q) + ',' + _str(period_r) + ',' + _str(period_s) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    ArraySetAsSeries(BufferECCI, True)
    ArraySetAsSeries(BufferTrigger, True)
    ArraySetAsSeries(BufferMOM, True)
    ArraySetAsSeries(BufferAbsMOM, True)
    ArraySetAsSeries(BufferVar1, True)
    ArraySetAsSeries(BufferVar2, True)
    ArraySetAsSeries(BufferVar2a, True)
    ArraySetAsSeries(BufferVar2b, True)
    ArraySetAsSeries(BufferVar2c, True)
    ArraySetAsSeries(BufferVar3, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferECCI, 0)
        ArrayInitialize(BufferTrigger, 0)
        ArrayInitialize(BufferMOM, 0)
        ArrayInitialize(BufferAbsMOM, 0)
        ArrayInitialize(BufferVar1, 0)
        ArrayInitialize(BufferVar2, 0)
        ArrayInitialize(BufferVar2a, 0)
        ArrayInitialize(BufferVar2b, 0)
        ArrayInitialize(BufferVar2c, 0)
        ArrayInitialize(BufferVar3, 0)
    for i in range(limit, 0 - 1, -1):
        BufferMOM[i] = close[i] - close[i + 1]
        BufferAbsMOM[i] = fabs(BufferMOM[i])
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_q, BufferMOM, BufferVar1) == 0:
            return 0
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_q, period_r, BufferVar1, BufferVar2) == 0:
            return 0
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_r, period_s, BufferVar2, BufferVar2c) == 0:
            return 0
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_q, BufferAbsMOM, BufferVar2a) == 0:
            return 0
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_q, period_r, BufferVar2a, BufferVar2b) == 0:
            return 0
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_r, period_s, BufferVar2b, BufferVar3) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_q, BufferMOM, BufferVar1) == 0:
            return 0
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_q, period_r, BufferVar1, BufferVar2) == 0:
            return 0
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_r, period_s, BufferVar2, BufferVar2c) == 0:
            return 0
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_q, BufferAbsMOM, BufferVar2a) == 0:
            return 0
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_q, period_r, BufferVar2a, BufferVar2b) == 0:
            return 0
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_r, period_s, BufferVar2b, BufferVar3) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_q, BufferMOM, BufferVar1, _GlobRef(globals(), 'weight_sum1')) == 0:
            return 0
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_q, period_r, BufferVar1, BufferVar2, _GlobRef(globals(), 'weight_sum2')) == 0:
            return 0
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_r, period_s, BufferVar2, BufferVar2c, _GlobRef(globals(), 'weight_sum3')) == 0:
            return 0
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_q, BufferAbsMOM, BufferVar2a, _GlobRef(globals(), 'weight_sum4')) == 0:
            return 0
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_q, period_r, BufferVar2a, BufferVar2b, _GlobRef(globals(), 'weight_sum5')) == 0:
            return 0
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_r, period_s, BufferVar2b, BufferVar3, _GlobRef(globals(), 'weight_sum6')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_q, BufferMOM, BufferVar1) == 0:
            return 0
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_q, period_r, BufferVar1, BufferVar2) == 0:
            return 0
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_r, period_s, BufferVar2, BufferVar2c) == 0:
            return 0
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_q, BufferAbsMOM, BufferVar2a) == 0:
            return 0
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_q, period_r, BufferVar2a, BufferVar2b) == 0:
            return 0
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_r, period_s, BufferVar2b, BufferVar3) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferECCI[i] = (_fdiv(500.0 * BufferVar2c[i], BufferVar3[i]) if (BufferVar3[i] != 0) else 0)
    _sw2 = InpMethod
    if _sw2 == MODE_EMA:
        return ExponentialMAOnBuffer(rates_total, prev_calculated, period_s, trigger, BufferECCI, BufferTrigger)
    elif _sw2 == MODE_SMMA:
        return SmoothedMAOnBuffer(rates_total, prev_calculated, period_s, trigger, BufferECCI, BufferTrigger)
    elif _sw2 == MODE_LWMA:
        return LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_s, trigger, BufferECCI, BufferTrigger, _GlobRef(globals(), 'weight_sum7'))
    else:
        return SimpleMAOnBuffer(rates_total, prev_calculated, period_s, trigger, BufferECCI, BufferTrigger)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FxSnipersErgodicCCITrigger(_MQL5Indicator):
    name = 'Fx_Snipers_Ergodic_CCI_Trigger'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodQ': 4,  # Period Q
        'InpPeriodR': 8,  # Period R
        'InpPeriodS': 5,  # Period S
        'InpTrigger': 4,  # Trigger
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpOverbought': 150.0,  # Overbought
        'InpOversold': -150.0,  # Oversold
    }

