"""Track_Cyclical — converted from MQL5: MQL5 Indicators/Track_Cyclical/Track_Cyclical.mq5

Track Cyclical oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11186720]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Track Cyclical'}, 'levels': [], 'description': ['Track Cyclical oscillator'], 'name': 'Track_Cyclical', 'source': 'MQL5 Indicators/Track_Cyclical/Track_Cyclical.mq5', 'folder': 'Track_Cyclical', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 25, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverboughtExept', 'py': 'InpOverboughtExept', 'param': 'InpOverboughtExept', 'type': 'double', 'default': 0.7, 'label': 'Exceptional overbought', 'sinput': False}, {'mql': 'InpOverboughtAbnormal', 'py': 'InpOverboughtAbnormal', 'param': 'InpOverboughtAbnormal', 'type': 'double', 'default': 0.5, 'label': 'Abnormal overbought', 'sinput': False}, {'mql': 'InpOverboughtNormal', 'py': 'InpOverboughtNormal', 'param': 'InpOverboughtNormal', 'type': 'double', 'default': 0.3, 'label': 'Normal overbought', 'sinput': False}, {'mql': 'InpOversoldNormal', 'py': 'InpOversoldNormal', 'param': 'InpOversoldNormal', 'type': 'double', 'default': -0.3, 'label': 'Normal oversold', 'sinput': False}, {'mql': 'InpOversoldAbnormal', 'py': 'InpOversoldAbnormal', 'param': 'InpOversoldAbnormal', 'type': 'double', 'default': -0.5, 'label': 'Abnormal oversold', 'sinput': False}, {'mql': 'InpOversoldExept', 'py': 'InpOversoldExept', 'param': 'InpOversoldExept', 'type': 'double', 'default': -0.7, 'label': 'Exceptional oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 25)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverboughtExept = _input('InpOverboughtExept', 0.7)  # Exceptional overbought
InpOverboughtAbnormal = _input('InpOverboughtAbnormal', 0.5)  # Abnormal overbought
InpOverboughtNormal = _input('InpOverboughtNormal', 0.3)  # Normal overbought
InpOversoldNormal = _input('InpOversoldNormal', -0.3)  # Normal oversold
InpOversoldAbnormal = _input('InpOversoldAbnormal', -0.5)  # Abnormal oversold
InpOversoldExept = _input('InpOversoldExept', -0.7)  # Exceptional oversold
BufferTC = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
overbought_e = 0.0
overbought_a = 0.0
overbought_n = 0.0
oversold_n = 0.0
oversold_a = 0.0
oversold_e = 0.0
period = 0
handle_ma1 = 0
handle_maP = 0

def OnInit():
    global handle_ma1, handle_maP, overbought_a, overbought_e, overbought_n, oversold_a, oversold_e, oversold_n, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    overbought_n = (0.001 if (fabs(InpOverboughtNormal) < 0.001) else fabs(InpOverboughtNormal))
    overbought_a = ((overbought_n + 0.001) if (fabs(InpOverboughtAbnormal) <= overbought_n) else fabs(InpOverboughtAbnormal))
    overbought_e = ((overbought_a + 0.001) if (fabs(InpOverboughtExept) <= overbought_a) else fabs(InpOverboughtExept))
    oversold_n = (-0.001 if ((-fabs(InpOversoldNormal)) > -0.001) else (-fabs(InpOversoldNormal)))
    oversold_a = ((oversold_n - 0.001) if ((-fabs(InpOversoldAbnormal)) >= oversold_n) else (-fabs(InpOversoldAbnormal)))
    oversold_e = ((oversold_a - 0.001) if ((-fabs(InpOversoldExept)) >= oversold_a) else (-fabs(InpOversoldExept)))
    SetIndexBuffer(0, BufferTC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMAP, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Track Cyclical (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 6)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought_e)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, overbought_a)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, overbought_n)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, oversold_n)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, oversold_a)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 5, oversold_e)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Exceptional overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Abnormal overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Normal overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 3, 'Normal oversold')
    IndicatorSetString(INDICATOR_LEVELTEXT, 4, 'Abnormal oversold')
    IndicatorSetString(INDICATOR_LEVELTEXT, 5, 'Exceptional oversold')
    ArraySetAsSeries(BufferTC, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMAP, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maP = iMA(None, PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferTC, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMAP, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMAP)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferTC[i] = (_fdiv(100.0 * (BufferMA1[i] - BufferMAP[i]), BufferMAP[i]) if (BufferMAP[i] != 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrackCyclical(_MQL5Indicator):
    name = 'Track_Cyclical'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 25,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverboughtExept': 0.7,  # Exceptional overbought
        'InpOverboughtAbnormal': 0.5,  # Abnormal overbought
        'InpOverboughtNormal': 0.3,  # Normal overbought
        'InpOversoldNormal': -0.3,  # Normal oversold
        'InpOversoldAbnormal': -0.5,  # Abnormal oversold
        'InpOversoldExept': -0.7,  # Exceptional oversold
    }

