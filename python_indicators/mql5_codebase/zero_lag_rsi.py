"""Zero_Lag_RSI — converted from MQL5: MQL5 Indicators/Zero_Lag_RSI/Zero_Lag_RSI.mq5

Zero Lag RSI
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 11193702, 255, 8036607, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Zero Lag RSI'}, 'levels': [], 'description': ['Zero Lag RSI'], 'name': 'Zero_Lag_RSI', 'source': 'MQL5 Indicators/Zero_Lag_RSI/Zero_Lag_RSI.mq5', 'folder': 'Zero_Lag_RSI', 'inputs': [{'mql': 'InpSmoothing1', 'py': 'InpSmoothing1', 'param': 'InpSmoothing1', 'type': 'uint', 'default': 15, 'label': 'First smoothing period', 'sinput': False}, {'mql': 'InpSmoothing2', 'py': 'InpSmoothing2', 'param': 'InpSmoothing2', 'type': 'uint', 'default': 7, 'label': 'Second smoothing period', 'sinput': False}, {'mql': 'InpFactor1', 'py': 'InpFactor1', 'param': 'InpFactor1', 'type': 'double', 'default': 0.05, 'label': 'First RSI factor', 'sinput': False}, {'mql': 'InpPeriodRSI1', 'py': 'InpPeriodRSI1', 'param': 'InpPeriodRSI1', 'type': 'uint', 'default': 8, 'label': 'First RSI period', 'sinput': False}, {'mql': 'InpFactor2', 'py': 'InpFactor2', 'param': 'InpFactor2', 'type': 'double', 'default': 0.1, 'label': 'Second RSI factor', 'sinput': False}, {'mql': 'InpPeriodRSI2', 'py': 'InpPeriodRSI2', 'param': 'InpPeriodRSI2', 'type': 'uint', 'default': 21, 'label': 'Second RSI period', 'sinput': False}, {'mql': 'InpFactor3', 'py': 'InpFactor3', 'param': 'InpFactor3', 'type': 'double', 'default': 0.16, 'label': 'Third RSI factor', 'sinput': False}, {'mql': 'InpPeriodRSI3', 'py': 'InpPeriodRSI3', 'param': 'InpPeriodRSI3', 'type': 'uint', 'default': 34, 'label': 'Third RSI period', 'sinput': False}, {'mql': 'InpFactor4', 'py': 'InpFactor4', 'param': 'InpFactor4', 'type': 'double', 'default': 0.26, 'label': 'Fourth RSI factor', 'sinput': False}, {'mql': 'InpPeriodRSI4', 'py': 'InpPeriodRSI4', 'param': 'InpPeriodRSI4', 'type': 'uint', 'default': 55, 'label': 'Fourth RSI period', 'sinput': False}, {'mql': 'InpFactor5', 'py': 'InpFactor5', 'param': 'InpFactor5', 'type': 'double', 'default': 0.43, 'label': 'Fifth RSI factor', 'sinput': False}, {'mql': 'InpPeriodRSI5', 'py': 'InpPeriodRSI5', 'param': 'InpPeriodRSI5', 'type': 'uint', 'default': 89, 'label': 'Fifth RSI period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpSmoothing1 = _input('InpSmoothing1', 15)  # First smoothing period
InpSmoothing2 = _input('InpSmoothing2', 7)  # Second smoothing period
InpFactor1 = _input('InpFactor1', 0.05)  # First RSI factor
InpPeriodRSI1 = _input('InpPeriodRSI1', 8)  # First RSI period
InpFactor2 = _input('InpFactor2', 0.1)  # Second RSI factor
InpPeriodRSI2 = _input('InpPeriodRSI2', 21)  # Second RSI period
InpFactor3 = _input('InpFactor3', 0.16)  # Third RSI factor
InpPeriodRSI3 = _input('InpPeriodRSI3', 34)  # Third RSI period
InpFactor4 = _input('InpFactor4', 0.26)  # Fourth RSI factor
InpPeriodRSI4 = _input('InpPeriodRSI4', 55)  # Fourth RSI period
InpFactor5 = _input('InpFactor5', 0.43)  # Fifth RSI factor
InpPeriodRSI5 = _input('InpPeriodRSI5', 89)  # Fifth RSI period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferRSIZL = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferFastTrend = Arr(0, 0.0)
BufferSlowTrend = Arr(0, 0.0)
BufferRSI1 = Arr(0, 0.0)
BufferRSI2 = Arr(0, 0.0)
BufferRSI3 = Arr(0, 0.0)
BufferRSI4 = Arr(0, 0.0)
BufferRSI5 = Arr(0, 0.0)
smoothing1 = 0.0
smoothing2 = 0.0
sm_const1 = 0.0
sm_const2 = 0.0
factor1 = 0.0
factor2 = 0.0
factor3 = 0.0
factor4 = 0.0
factor5 = 0.0
period1 = 0
period2 = 0
period3 = 0
period4 = 0
period5 = 0
period_max = 0
handle_rsi1 = 0
handle_rsi2 = 0
handle_rsi3 = 0
handle_rsi4 = 0
handle_rsi5 = 0

def OnInit():
    global factor1, factor2, factor3, factor4, factor5, handle_rsi1, handle_rsi2, handle_rsi3, handle_rsi4, handle_rsi5, period1, period2, period3, period4, period5, period_max, sm_const1, sm_const2, smoothing1, smoothing2
    period1 = (1 if (InpPeriodRSI1 < 1) else InpPeriodRSI1)
    period2 = (1 if (InpPeriodRSI2 < 1) else InpPeriodRSI2)
    period3 = (1 if (InpPeriodRSI3 < 1) else InpPeriodRSI3)
    period4 = (1 if (InpPeriodRSI4 < 1) else InpPeriodRSI4)
    period5 = (1 if (InpPeriodRSI5 < 1) else InpPeriodRSI5)
    period_max = fmax(period1, fmax(period2, fmax(period3, fmax(period4, period5))))
    smoothing1 = (2.0 if (InpSmoothing1 < 2) else InpSmoothing1)
    smoothing2 = (2.0 if (InpSmoothing2 < 2) else InpSmoothing2)
    sm_const1 = _fdiv(smoothing1 - 1.0, smoothing1)
    sm_const2 = _fdiv(smoothing2 - 1.0, smoothing2)
    factor1 = InpFactor1
    factor2 = InpFactor2
    factor3 = InpFactor3
    factor4 = InpFactor4
    factor5 = InpFactor5
    SetIndexBuffer(0, BufferRSIZL, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferFastTrend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferSlowTrend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferRSI1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferRSI2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferRSI3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferRSI4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferRSI5, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Zero Lag RSI')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    ArraySetAsSeries(BufferRSIZL, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferFastTrend, True)
    ArraySetAsSeries(BufferSlowTrend, True)
    ArraySetAsSeries(BufferRSI1, True)
    ArraySetAsSeries(BufferRSI2, True)
    ArraySetAsSeries(BufferRSI3, True)
    ArraySetAsSeries(BufferRSI4, True)
    ArraySetAsSeries(BufferRSI5, True)
    ResetLastError()
    handle_rsi1 = iRSI(None, PERIOD_CURRENT, period1, InpAppliedPrice)
    if handle_rsi1 == INVALID_HANDLE:
        Print('The iRSI(', _str(period1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_rsi2 = iRSI(None, PERIOD_CURRENT, period2, InpAppliedPrice)
    if handle_rsi2 == INVALID_HANDLE:
        Print('The iRSI(', _str(period2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_rsi3 = iRSI(None, PERIOD_CURRENT, period3, InpAppliedPrice)
    if handle_rsi3 == INVALID_HANDLE:
        Print('The iRSI(', _str(period3), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_rsi4 = iRSI(None, PERIOD_CURRENT, period4, InpAppliedPrice)
    if handle_rsi4 == INVALID_HANDLE:
        Print('The iRSI(', _str(period4), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_rsi5 = iRSI(None, PERIOD_CURRENT, period5, InpAppliedPrice)
    if handle_rsi5 == INVALID_HANDLE:
        Print('The iRSI(', _str(period5), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferRSIZL, 0)
        ArrayInitialize(BufferColors, 4)
        ArrayInitialize(BufferFastTrend, 0)
        ArrayInitialize(BufferSlowTrend, 0)
        ArrayInitialize(BufferRSI1, 0)
        ArrayInitialize(BufferRSI2, 0)
        ArrayInitialize(BufferRSI3, 0)
        ArrayInitialize(BufferRSI4, 0)
        ArrayInitialize(BufferRSI5, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_rsi1, 0, 0, count, BufferRSI1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_rsi2, 0, 0, count, BufferRSI2)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_rsi3, 0, 0, count, BufferRSI3)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_rsi4, 0, 0, count, BufferRSI4)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_rsi5, 0, 0, count, BufferRSI5)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        RSI1 = BufferRSI1[i]
        RSI2 = BufferRSI2[i]
        RSI3 = BufferRSI3[i]
        RSI4 = BufferRSI4[i]
        RSI5 = BufferRSI5[i]
        Osc1 = factor1 * RSI1
        Osc2 = factor2 * RSI2
        Osc3 = factor3 * RSI3
        Osc4 = factor4 * RSI4
        Osc5 = factor5 * RSI5
        BufferFastTrend[i] = Osc1 + Osc2 + Osc3 + Osc4 + Osc5
        BufferSlowTrend[i] = _fdiv(BufferFastTrend[i], smoothing1) + (BufferSlowTrend[i + 1] * sm_const1)
        BufferRSIZL[i] = _fdiv(BufferFastTrend[i] - BufferSlowTrend[i], smoothing2 * Point()) + (BufferRSIZL[i + 1] * sm_const2)
        if BufferRSIZL[i] > 0:
            BufferColors[i] = (0 if (BufferRSIZL[i] > BufferRSIZL[i + 1]) else 1 if (BufferRSIZL[i] < BufferRSIZL[i + 1]) else 4)
        else:
            BufferColors[i] = (2 if (BufferRSIZL[i] < BufferRSIZL[i + 1]) else 3 if (BufferRSIZL[i] > BufferRSIZL[i + 1]) else 4)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZeroLagRSI(_MQL5Indicator):
    name = 'Zero_Lag_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpSmoothing1': 15,  # First smoothing period
        'InpSmoothing2': 7,  # Second smoothing period
        'InpFactor1': 0.05,  # First RSI factor
        'InpPeriodRSI1': 8,  # First RSI period
        'InpFactor2': 0.1,  # Second RSI factor
        'InpPeriodRSI2': 21,  # Second RSI period
        'InpFactor3': 0.16,  # Third RSI factor
        'InpPeriodRSI3': 34,  # Third RSI period
        'InpFactor4': 0.26,  # Fourth RSI factor
        'InpPeriodRSI4': 55,  # Fourth RSI period
        'InpFactor5': 0.43,  # Fifth RSI factor
        'InpPeriodRSI5': 89,  # Fifth RSI period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

