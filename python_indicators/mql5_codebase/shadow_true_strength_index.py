"""Shadow_True_Strength_Index — converted from MQL5: MQL5 Indicators/Shadow_True_Strength_Index/Shadow_True_Strength_Index.mq5

Shadow True Strength Index oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [3329330], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'TSI', 2: 'Shadow one', 3: 'Shadow two'}, 'levels': [], 'description': ['Shadow True Strength Index oscillator'], 'name': 'Shadow_True_Strength_Index', 'source': 'MQL5 Indicators/Shadow_True_Strength_Index/Shadow_True_Strength_Index.mq5', 'folder': 'Shadow_True_Strength_Index', 'inputs': [{'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Price source', 'sinput': False}, {'mql': 'InpPeriodSRC', 'py': 'InpPeriodSRC', 'param': 'InpPeriodSRC', 'type': 'uint', 'default': 1, 'label': 'Price source period', 'sinput': False}, {'mql': 'InpPeriodSm1', 'py': 'InpPeriodSm1', 'param': 'InpPeriodSm1', 'type': 'uint', 'default': 7, 'label': 'First smoothing period', 'sinput': False}, {'mql': 'InpPeriodSm2', 'py': 'InpPeriodSm2', 'param': 'InpPeriodSm2', 'type': 'uint', 'default': 14, 'label': 'Second smoothing period', 'sinput': False}, {'mql': 'InpPeriodSh1', 'py': 'InpPeriodSh1', 'param': 'InpPeriodSh1', 'type': 'uint', 'default': 14, 'label': 'First shadow period', 'sinput': False}, {'mql': 'InpMethodSh1', 'py': 'InpMethodSh1', 'param': 'InpMethodSh1', 'type': 'int', 'default': 0, 'label': 'First shadow method', 'sinput': False}, {'mql': 'InpPeriodSh2', 'py': 'InpPeriodSh2', 'param': 'InpPeriodSh2', 'type': 'uint', 'default': 14, 'label': 'Second shadow period', 'sinput': False}, {'mql': 'InpMethodSh2', 'py': 'InpMethodSh2', 'param': 'InpMethodSh2', 'type': 'int', 'default': 0, 'label': 'Second shadow method', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 25.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -25.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Price source
InpPeriodSRC = _input('InpPeriodSRC', 1)  # Price source period
InpPeriodSm1 = _input('InpPeriodSm1', 7)  # First smoothing period
InpPeriodSm2 = _input('InpPeriodSm2', 14)  # Second smoothing period
InpPeriodSh1 = _input('InpPeriodSh1', 14)  # First shadow period
InpMethodSh1 = _input('InpMethodSh1', MODE_SMA)  # First shadow method
InpPeriodSh2 = _input('InpPeriodSh2', 14)  # Second shadow period
InpMethodSh2 = _input('InpMethodSh2', MODE_SMA)  # Second shadow method
InpOverbought = _input('InpOverbought', 25.0)  # Overbought
InpOversold = _input('InpOversold', -25.0)  # Oversold
BufferTSI = Arr(0, 0.0)
BufferSH1 = Arr(0, 0.0)
BufferSH2 = Arr(0, 0.0)
BufferUDM = Arr(0, 0.0)
BufferADM = Arr(0, 0.0)
BufferUDM1 = Arr(0, 0.0)
BufferUDM2 = Arr(0, 0.0)
BufferADM1 = Arr(0, 0.0)
BufferADM2 = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_src = 0
period_sm1 = 0
period_sm2 = 0
period_sh1 = 0
period_sh2 = 0
weight_sum1 = 0
weight_sum2 = 0
handle_ma = 0

def OnInit():
    global handle_ma, overbought, oversold, period_sh1, period_sh2, period_sm1, period_sm2, period_src
    period_src = (1 if (InpPeriodSRC < 1) else InpPeriodSRC)
    period_sm1 = (2 if (InpPeriodSm1 < 2) else InpPeriodSm1)
    period_sm2 = (2 if (InpPeriodSm2 < 2) else InpPeriodSm2)
    period_sh1 = (2 if (InpPeriodSh1 < 2) else InpPeriodSh1)
    period_sh2 = (2 if (InpPeriodSh2 < 2) else InpPeriodSh2)
    overbought = (0.1 if (fabs(InpOverbought) < 0.1) else 100.0 if (InpOverbought > 100.0) else fabs(InpOverbought))
    oversold = (-0.1 if ((-fabs(InpOversold)) > -0.1) else -100.0 if ((-fabs(InpOversold)) < -100.0) else (-fabs(InpOversold)))
    SetIndexBuffer(0, BufferTSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSH1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferSH2, INDICATOR_DATA)
    SetIndexBuffer(3, BufferUDM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferUDM1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferUDM2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferADM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferADM1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferADM2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Shadow TSI (' + _str(period_src) + ',' + _str(period_sm1) + ',' + _str(period_sm2) + ',' + _str(period_sh1) + ',' + _str(period_sh2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    ArraySetAsSeries(BufferTSI, True)
    ArraySetAsSeries(BufferSH1, True)
    ArraySetAsSeries(BufferSH2, True)
    ArraySetAsSeries(BufferUDM, True)
    ArraySetAsSeries(BufferUDM1, True)
    ArraySetAsSeries(BufferUDM2, True)
    ArraySetAsSeries(BufferADM, True)
    ArraySetAsSeries(BufferADM1, True)
    ArraySetAsSeries(BufferADM2, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_src, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_src), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 2:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_src - 2
        ArrayInitialize(BufferTSI, 0)
        ArrayInitialize(BufferSH1, EMPTY_VALUE)
        ArrayInitialize(BufferSH2, EMPTY_VALUE)
        ArrayInitialize(BufferUDM, 0)
        ArrayInitialize(BufferUDM1, 0)
        ArrayInitialize(BufferUDM2, 0)
        ArrayInitialize(BufferADM, 0)
        ArrayInitialize(BufferADM1, 0)
        ArrayInitialize(BufferADM2, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferUDM[i] = BufferMA[i] - BufferMA[i + 1]
        BufferADM[i] = fabs(BufferUDM[i])
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period_src, period_sm1, BufferUDM, BufferUDM1) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period_src, period_sm1, BufferADM, BufferADM1) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period_sm1, period_sm2, BufferUDM1, BufferUDM2) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period_sm1, period_sm2, BufferADM1, BufferADM2) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferTSI[i] = (_fdiv(100.0 * BufferUDM2[i], BufferADM2[i]) if (BufferADM2[i] != 0) else 0)
    _sw1 = InpMethodSh1
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sh1, BufferTSI, BufferSH1) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sh1, BufferTSI, BufferSH1) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sh1, BufferTSI, BufferSH1, _GlobRef(globals(), 'weight_sum1')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sh1, BufferTSI, BufferSH1) == 0:
            return 0
    _sw2 = InpMethodSh2
    if _sw2 == MODE_EMA:
        return ExponentialMAOnBuffer(rates_total, prev_calculated, period_sh1, period_sh2, BufferSH1, BufferSH2)
    elif _sw2 == MODE_SMMA:
        return SmoothedMAOnBuffer(rates_total, prev_calculated, period_sh1, period_sh2, BufferSH1, BufferSH2)
    elif _sw2 == MODE_LWMA:
        return LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_sh1, period_sh2, BufferSH1, BufferSH2, _GlobRef(globals(), 'weight_sum2'))
    else:
        return SimpleMAOnBuffer(rates_total, prev_calculated, period_sh1, period_sh2, BufferSH1, BufferSH2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ShadowTrueStrengthIndex(_MQL5Indicator):
    name = 'Shadow_True_Strength_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price source
        'InpPeriodSRC': 1,  # Price source period
        'InpPeriodSm1': 7,  # First smoothing period
        'InpPeriodSm2': 14,  # Second smoothing period
        'InpPeriodSh1': 14,  # First shadow period
        'InpMethodSh1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # First shadow method
        'InpPeriodSh2': 14,  # Second shadow period
        'InpMethodSh2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Second shadow method
        'InpOverbought': 25.0,  # Overbought
        'InpOversold': -25.0,  # Oversold
    }

