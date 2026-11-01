"""Volatility_Ratio2 — converted from MQL5: MQL5 Indicators/Volatility_Ratio2/Volatility_Ratio2.mq5

Volatility Ratio2 oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [9639167]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'VR2'}, 'levels': [], 'description': ['Volatility Ratio2 oscillator'], 'name': 'Volatility_Ratio2', 'source': 'MQL5 Indicators/Volatility_Ratio2/Volatility_Ratio2.mq5', 'folder': 'Volatility_Ratio2', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpThreshold', 'py': 'InpThreshold', 'param': 'InpThreshold', 'type': 'double', 'default': 2.0, 'label': 'Threshold', 'sinput': False}, {'mql': 'InpUseAlert', 'py': 'InpUseAlert', 'param': 'InpUseAlert', 'type': 'int', 'default': 1, 'label': 'Show alerts', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpThreshold = _input('InpThreshold', 2.0)  # Threshold
InpUseAlert = _input('InpUseAlert', INPUT_YES)  # Show alerts
BufferVR = Arr(0, 0.0)
BufferTR = Arr(0, 0.0)
BufferEMATR = Arr(0, 0.0)
threshold = 0.0
period_vr = 0

def OnInit():
    global period_vr, threshold
    period_vr = (1 if (InpPeriod < 1) else InpPeriod)
    threshold = InpThreshold
    SetIndexBuffer(0, BufferVR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferEMATR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility Ratio2 (' + _str(period_vr) + ',' + _str(threshold) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, threshold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Threshold')
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    ArraySetAsSeries(BufferVR, True)
    ArraySetAsSeries(BufferTR, True)
    ArraySetAsSeries(BufferEMATR, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_alert
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if rates_total < 2:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferVR, EMPTY_VALUE)
        ArrayInitialize(BufferTR, 0)
        ArrayInitialize(BufferEMATR, 0)
    for i in range(limit, 0 - 1, -1):
        BufferTR[i] = fmax(fmax(high[i] - low[i], fabs(high[i] - close[i + 1])), fabs(close[i + 1] - low[i]))
        BufferEMATR[i] = EMA(rates_total, BufferTR[i], BufferEMATR[i + 1], period_vr, i)
        BufferVR[i] = (_fdiv(BufferTR[i], BufferEMATR[i]) if (BufferEMATR[i] != 0) else 0)
        if ((InpUseAlert and i == 0) and time[0] > _s_OnCalculate_last_alert) and BufferVR[0] > threshold:
            Alert(Symbol() + ',' + TimeframeToString(Period()) + ': Volatility Ratio > ' + _str(threshold) + ')')
            _s_OnCalculate_last_alert = TimeCurrent()
    return rates_total

def EMA(rates_total, price, prev_value, period, shift):
    return ((prev_value + (_fdiv(2.0, 1 + period) * (price - prev_value))) if (shift < (rates_total - 2)) else price)

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

# ---- static local variables
_s_OnCalculate_last_alert = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityRatio2(_MQL5Indicator):
    name = 'Volatility_Ratio2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpThreshold': 2.0,  # Threshold
        'InpUseAlert': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show alerts
    }

