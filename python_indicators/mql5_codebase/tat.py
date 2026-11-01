"""TAT — converted from MQL5: MQL5 Indicators/TAT (Trend Analyzer Tool)/TAT.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 2}, 'types': {1: 3, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'TAT', 2: 'SIG'}, 'levels': [], 'description': [], 'name': 'TAT', 'source': 'MQL5 Indicators/TAT (Trend Analyzer Tool)/TAT.mq5', 'folder': 'TAT (Trend Analyzer Tool)', 'inputs': [{'mql': 'InpPeriodFastMACD', 'py': 'InpPeriodFastMACD', 'param': 'InpPeriodFastMACD', 'type': 'uint', 'default': 12, 'label': 'MACD Fast EMA period', 'sinput': False}, {'mql': 'InpPeriodSlowMACD', 'py': 'InpPeriodSlowMACD', 'param': 'InpPeriodSlowMACD', 'type': 'uint', 'default': 26, 'label': 'MACD Slow EMA period', 'sinput': False}, {'mql': 'InpPeriodSigMACD', 'py': 'InpPeriodSigMACD', 'param': 'InpPeriodSigMACD', 'type': 'uint', 'default': 9, 'label': 'MACD Signal MA period', 'sinput': False}, {'mql': 'InpStepSAR', 'py': 'InpStepSAR', 'param': 'InpStepSAR', 'type': 'double', 'default': 0.02, 'label': 'SAR step', 'sinput': False}, {'mql': 'InpMaxSAR', 'py': 'InpMaxSAR', 'param': 'InpMaxSAR', 'type': 'double', 'default': 0.2, 'label': 'SAR max', 'sinput': False}, {'mql': 'InpMultMACD', 'py': 'InpMultMACD', 'param': 'InpMultMACD', 'type': 'double', 'default': 66.67, 'label': 'MACD multiplier', 'sinput': False}, {'mql': 'InpMultSAR', 'py': 'InpMultSAR', 'param': 'InpMultSAR', 'type': 'double', 'default': 6.67, 'label': 'SAR multiplier', 'sinput': False}, {'mql': 'InpPeriodSigTAT', 'py': 'InpPeriodSigTAT', 'param': 'InpPeriodSigTAT', 'type': 'uint', 'default': 12, 'label': 'TAT Signal period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 10.0, 'label': 'TAT overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -10.0, 'label': 'TAT oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodFastMACD = _input('InpPeriodFastMACD', 12)  # MACD Fast EMA period
InpPeriodSlowMACD = _input('InpPeriodSlowMACD', 26)  # MACD Slow EMA period
InpPeriodSigMACD = _input('InpPeriodSigMACD', 9)  # MACD Signal MA period
InpStepSAR = _input('InpStepSAR', 0.02)  # SAR step
InpMaxSAR = _input('InpMaxSAR', 0.2)  # SAR max
InpMultMACD = _input('InpMultMACD', 66.67)  # MACD multiplier
InpMultSAR = _input('InpMultSAR', 6.67)  # SAR multiplier
InpPeriodSigTAT = _input('InpPeriodSigTAT', 12)  # TAT Signal period
InpOverbought = _input('InpOverbought', 10.0)  # TAT overbought
InpOversold = _input('InpOversold', -10.0)  # TAT oversold
BufferTAT = Arr(0, 0.0)
BufferSIG = Arr(0, 0.0)
BufferLong = Arr(0, 0.0)
BufferAF = Arr(0, 0.0)
BufferExtr = Arr(0, 0.0)
BufferSAR = Arr(0, 0.0)
BufferMACD = Arr(0, 0.0)
BufferSIG_MACD = Arr(0, 0.0)
period_sig_tat = 0
period_sig_macd = 0
period_fast = 0
period_slow = 0
handle_macd = 0
sar_step = 0.0
sar_max = 0.0
overbought = 0.0
oversold = 0.0

def OnInit():
    global handle_macd, overbought, oversold, period_fast, period_sig_macd, period_sig_tat, period_slow, sar_max, sar_step
    period_fast = (1 if (InpPeriodFastMACD < 1) else InpPeriodFastMACD)
    period_slow = (1 if (InpPeriodSlowMACD < 1) else InpPeriodSlowMACD)
    period_sig_macd = (1 if (InpPeriodSigMACD < 1) else InpPeriodSigMACD)
    period_sig_tat = (1 if (InpPeriodSigTAT < 1) else InpPeriodSigTAT)
    sar_step = InpStepSAR
    sar_max = InpMaxSAR
    overbought = (0.001 if (fabs(InpOverbought) < 0.001) else fabs(InpOverbought))
    oversold = (-0.001 if ((-fabs(InpOversold)) > -0.001) else (-fabs(InpOversold)))
    SetIndexBuffer(0, BufferTAT, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSIG, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLong, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferAF, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferExtr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSAR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferMACD, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferSIG_MACD, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TAT')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    ArraySetAsSeries(BufferTAT, True)
    ArraySetAsSeries(BufferSIG, True)
    ArraySetAsSeries(BufferLong, True)
    ArraySetAsSeries(BufferAF, True)
    ArraySetAsSeries(BufferExtr, True)
    ArraySetAsSeries(BufferSAR, True)
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferSIG_MACD, True)
    ResetLastError()
    handle_macd = iMACD(None, PERIOD_CURRENT, period_fast, period_slow, period_sig_macd, PRICE_CLOSE)
    if handle_macd == INVALID_HANDLE:
        Print('The iMACD(', _str(period_fast), ',', _str(period_slow), ',', _str(period_sig_macd), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = fmax(period_fast, fmax(period_slow, fmax(period_sig_tat, period_sig_macd)))
    if rates_total < (max_ + period_sig_macd + 2):
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    total = rates_total - period_sig_macd - max_ - 2
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = total
        ArrayInitialize(BufferTAT, 0)
        ArrayInitialize(BufferSIG, 0)
        ArrayInitialize(BufferLong, 0)
        ArrayInitialize(BufferAF, 0)
        ArrayInitialize(BufferExtr, 0)
        ArrayInitialize(BufferSAR, 0)
        ArrayInitialize(BufferMACD, 0)
        ArrayInitialize(BufferSIG_MACD, 0)
    copied = 0
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_macd, MAIN_LINE, 0, count, BufferMACD)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_macd, SIGNAL_LINE, 0, count, BufferSIG_MACD)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if i == total:
            BufferLong[i] = 1.0
            BufferAF[i] = sar_step
            BufferExtr[i] = high[i]
            BufferSAR[i] = low[i]
        else:
            BufferLong[i] = BufferLong[i + 1]
            BufferAF[i] = BufferAF[i + 1]
            BufferExtr[i] = BufferExtr[i + 1]
            BufferSAR[i] = BufferSAR[i + 1] + (BufferAF[i + 1] * (BufferExtr[i + 1] - BufferSAR[i + 1]))
            if BufferLong[i + 1] == 1:
                if low[i] < BufferSAR[i]:
                    BufferLong[i] = 0.0
                    BufferAF[i] = sar_step
                    BufferSAR[i] = BufferExtr[i + 1]
                    BufferExtr[i] = low[i]
                else:
                    if BufferExtr[i + 1] < high[i]:
                        BufferExtr[i] = high[i]
                        BufferAF[i] = BufferAF[i + 1] + sar_step
                        if BufferAF[i] > sar_max:
                            BufferAF[i] = sar_max
            else:
                if high[i] > BufferSAR[i]:
                    BufferLong[i] = 1.0
                    BufferAF[i] = sar_step
                    BufferSAR[i] = BufferExtr[i + 1]
                    BufferExtr[i] = high[i]
                else:
                    if BufferExtr[i + 1] > low[i]:
                        BufferExtr[i] = low[i]
                        BufferAF[i] = BufferAF[i + 1] + sar_step
                        if BufferAF[i] > sar_max:
                            BufferAF[i] = sar_max
    tat_sar = 0.0
    tat_macd = 0.0
    for i in range(limit, 0 - 1, -1):
        tat_sar = _fdiv(close[i] - BufferSAR[i], (BufferSAR[i] if (BufferSAR[i] > 0) else DBL_MIN))
        tat_macd = _fdiv(BufferMACD[i] - BufferSIG_MACD[i], close[i])
        BufferTAT[i] = 50 * ((tat_sar * InpMultSAR) + (tat_macd * InpMultMACD))
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sig_tat, BufferTAT, BufferSIG)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TAT(_MQL5Indicator):
    name = 'TAT'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastMACD': 12,  # MACD Fast EMA period
        'InpPeriodSlowMACD': 26,  # MACD Slow EMA period
        'InpPeriodSigMACD': 9,  # MACD Signal MA period
        'InpStepSAR': 0.02,  # SAR step
        'InpMaxSAR': 0.2,  # SAR max
        'InpMultMACD': 66.67,  # MACD multiplier
        'InpMultSAR': 6.67,  # SAR multiplier
        'InpPeriodSigTAT': 12,  # TAT Signal period
        'InpOverbought': 10.0,  # TAT overbought
        'InpOversold': -10.0,  # TAT oversold
    }

