"""Smoothed Smart Money Pressure Osc — converted from MQL5: MQL5 Indicators/Smoothed_Smart_Money_Pressure_Oscillator/Smoothed Smart Money Pressure Osc.mq5

Smoothed Smart Money Pressure Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [10526303], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'SSMP Osc', 2: 'Signal'}, 'levels': [], 'description': ['Smoothed Smart Money Pressure Oscillator'], 'name': 'Smoothed Smart Money Pressure Osc', 'source': 'MQL5 Indicators/Smoothed_Smart_Money_Pressure_Oscillator/Smoothed Smart Money Pressure Osc.mq5', 'folder': 'Smoothed_Smart_Money_Pressure_Oscillator', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'SM Period', 'sinput': False}, {'mql': 'InpPeriodSM', 'py': 'InpPeriodSM', 'param': 'InpPeriodSM', 'type': 'uint', 'default': 5, 'label': 'SM Smoothing period', 'sinput': False}, {'mql': 'InpMethodSM', 'py': 'InpMethodSM', 'param': 'InpMethodSM', 'type': 'int', 'default': 1, 'label': 'SM Smoothing method', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 20, 'label': 'Signal line Smoothing period', 'sinput': False}, {'mql': 'InpMethodSig', 'py': 'InpMethodSig', 'param': 'InpMethodSig', 'type': 'int', 'default': 1, 'label': 'Signal line Smoothing method', 'sinput': False}, {'mql': 'InpInverse', 'py': 'InpInverse', 'param': 'InpInverse', 'type': 'int', 'default': 1, 'label': 'Graph inverse', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # SM Period
InpPeriodSM = _input('InpPeriodSM', 5)  # SM Smoothing period
InpMethodSM = _input('InpMethodSM', MODE_EMA)  # SM Smoothing method
InpPeriodSig = _input('InpPeriodSig', 20)  # Signal line Smoothing period
InpMethodSig = _input('InpMethodSig', MODE_EMA)  # Signal line Smoothing method
InpInverse = _input('InpInverse', INPUT_YES)  # Graph inverse
BufferAVG = Arr(0, 0.0)
BufferSig = Arr(0, 0.0)
BufferSMP = Arr(0, 0.0)
BufferSM = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
BufferVolMA = Arr(0, 0.0)
period_ind = 0
period_sm = 0
period_sig = 0
weight_sum = 0
inv = 0

def OnInit():
    global inv, period_ind, period_sig, period_sm
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    period_sm = (2 if (InpPeriodSM < 2) else InpPeriodSM)
    period_sig = (2 if (InpPeriodSig < 2) else InpPeriodSig)
    inv = (-1 if InpInverse else 1)
    SetIndexBuffer(0, BufferAVG, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSig, INDICATOR_DATA)
    SetIndexBuffer(2, BufferSMP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferSM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferVolMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoothed Smart Money Pressure Osc (' + _str(period_ind) + ',' + _str(period_sm) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferAVG, True)
    ArraySetAsSeries(BufferSig, True)
    ArraySetAsSeries(BufferSMP, True)
    ArraySetAsSeries(BufferSM, True)
    ArraySetAsSeries(BufferVol, True)
    ArraySetAsSeries(BufferVolMA, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    first = rates_total - 2
    if limit > 1:
        limit = first
        ArrayInitialize(BufferAVG, EMPTY_VALUE)
        ArrayInitialize(BufferSig, EMPTY_VALUE)
        ArrayInitialize(BufferSMP, 0)
        ArrayInitialize(BufferSM, 0)
        ArrayInitialize(BufferVol, 0)
        ArrayInitialize(BufferVolMA, 0)
    for i in range(limit, 0 - 1, -1):
        BufferVol[i] = float(tick_volume[i])
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVol, BufferVolMA)
    for i in range(limit, 0 - 1, -1):
        if i == first:
            BufferSM[i] = close[i]
        else:
            VolMA = BufferVolMA[i]
            Change = close[i] - close[i + 1]
            BufferSM[i] = ((BufferSM[i + 1] + Change) if (BufferVol[i] > VolMA) else BufferSM[i + 1])
            BufferSMP[i] = _fdiv(close[period_ind] - BufferSM[i], Point()) * inv
    _sw1 = InpMethodSM
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_ind, period_sm, BufferSMP, BufferAVG)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_ind, period_sm, BufferSMP, BufferAVG)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ind, period_sm, BufferSMP, BufferAVG, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_ind, period_sm, BufferSMP, BufferAVG)
    _sw2 = InpMethodSig
    if _sw2 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_sm, period_sig, BufferAVG, BufferSig)
    elif _sw2 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_sm, period_sig, BufferAVG, BufferSig)
    elif _sw2 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_sm, period_sig, BufferAVG, BufferSig, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_sm, period_sig, BufferAVG, BufferSig)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmoothedSmartMoneyPressureOsc(_MQL5Indicator):
    name = 'Smoothed Smart Money Pressure Osc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriod': 14,  # SM Period
        'InpPeriodSM': 5,  # SM Smoothing period
        'InpMethodSM': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # SM Smoothing method
        'InpPeriodSig': 20,  # Signal line Smoothing period
        'InpMethodSig': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Signal line Smoothing method
        'InpInverse': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Graph inverse
    }

