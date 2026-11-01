"""True_Strength_Index — converted from MQL5: MQL5 Indicators/True_Strength_Index/True_Strength_Index.mq5

True Strength Index oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [6053069]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TSI'}, 'levels': [], 'description': ['True Strength Index oscillator'], 'name': 'True_Strength_Index', 'source': 'MQL5 Indicators/True_Strength_Index/True_Strength_Index.mq5', 'folder': 'True_Strength_Index', 'inputs': [{'mql': 'InpPeriodSm1', 'py': 'InpPeriodSm1', 'param': 'InpPeriodSm1', 'type': 'uint', 'default': 7, 'label': 'First smoothing period', 'sinput': False}, {'mql': 'InpPeriodSm2', 'py': 'InpPeriodSm2', 'param': 'InpPeriodSm2', 'type': 'uint', 'default': 14, 'label': 'Second smoothing period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 25.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -25.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodSm1 = _input('InpPeriodSm1', 7)  # First smoothing period
InpPeriodSm2 = _input('InpPeriodSm2', 14)  # Second smoothing period
InpOverbought = _input('InpOverbought', 25.0)  # Overbought
InpOversold = _input('InpOversold', -25.0)  # Oversold
BufferTSI = Arr(0, 0.0)
BufferUDM = Arr(0, 0.0)
BufferADM = Arr(0, 0.0)
BufferUDM1 = Arr(0, 0.0)
BufferUDM2 = Arr(0, 0.0)
BufferADM1 = Arr(0, 0.0)
BufferADM2 = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_sm1 = 0
period_sm2 = 0

def OnInit():
    global overbought, oversold, period_sm1, period_sm2
    period_sm1 = (2 if (InpPeriodSm1 < 2) else InpPeriodSm1)
    period_sm2 = (2 if (InpPeriodSm2 < 2) else InpPeriodSm2)
    overbought = (0.1 if (fabs(InpOverbought) < 0.1) else 100.0 if (InpOverbought > 100.0) else fabs(InpOverbought))
    oversold = (-0.1 if ((-fabs(InpOversold)) > -0.1) else -100.0 if ((-fabs(InpOversold)) < -100.0) else (-fabs(InpOversold)))
    SetIndexBuffer(0, BufferTSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUDM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferUDM1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferUDM2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferADM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferADM1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferADM2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'True Strength Index (' + _str(period_sm1) + ',' + _str(period_sm2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    ArraySetAsSeries(BufferTSI, True)
    ArraySetAsSeries(BufferUDM, True)
    ArraySetAsSeries(BufferUDM1, True)
    ArraySetAsSeries(BufferUDM2, True)
    ArraySetAsSeries(BufferADM, True)
    ArraySetAsSeries(BufferADM1, True)
    ArraySetAsSeries(BufferADM2, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < 2:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferTSI, EMPTY_VALUE)
        ArrayInitialize(BufferUDM, 0)
        ArrayInitialize(BufferUDM1, 0)
        ArrayInitialize(BufferUDM2, 0)
        ArrayInitialize(BufferADM, 0)
        ArrayInitialize(BufferADM1, 0)
        ArrayInitialize(BufferADM2, 0)
    for i in range(limit, 0 - 1, -1):
        BufferUDM[i] = close[i] - close[i + 1]
        BufferADM[i] = fabs(BufferUDM[i])
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferUDM, BufferUDM1) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferADM, BufferADM1) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period_sm1, period_sm2, BufferUDM1, BufferUDM2) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period_sm1, period_sm2, BufferADM1, BufferADM2) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferTSI[i] = (_fdiv(100.0 * BufferUDM2[i], BufferADM2[i]) if (BufferADM2[i] != 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrueStrengthIndex(_MQL5Indicator):
    name = 'True_Strength_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodSm1': 7,  # First smoothing period
        'InpPeriodSm2': 14,  # Second smoothing period
        'InpOverbought': 25.0,  # Overbought
        'InpOversold': -25.0,  # Oversold
    }

