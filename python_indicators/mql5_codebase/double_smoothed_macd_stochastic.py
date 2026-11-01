"""Double_Smoothed_MACD_Stochastic — converted from MQL5: MQL5 Indicators/Double_Smoothed_MACD_Stochastic/Double_Smoothed_MACD_Stochastic.mq5

Double smoothed MACD Stochastic oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'DSS', 2: 'Signal'}, 'levels': [], 'description': ['Double smoothed MACD Stochastic oscillator'], 'name': 'Double_Smoothed_MACD_Stochastic', 'source': 'MQL5 Indicators/Double_Smoothed_MACD_Stochastic/Double_Smoothed_MACD_Stochastic.mq5', 'folder': 'Double_Smoothed_MACD_Stochastic', 'inputs': [{'mql': 'InpPeriodSto', 'py': 'InpPeriodSto', 'param': 'InpPeriodSto', 'type': 'uint', 'default': 32, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 9, 'label': 'Smoothing', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 5, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodSto = _input('InpPeriodSto', 32)  # Stochastic period
InpPeriodSm = _input('InpPeriodSm', 9)  # Smoothing
InpPeriodSig = _input('InpPeriodSig', 5)  # Signal period
InpPeriodFast = _input('InpPeriodFast', 12)  # Fast EMA period
InpPeriodSlow = _input('InpPeriodSlow', 26)  # Slow EMA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferDSS = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferDDS2 = Arr(0, 0.0)
BufferMACD = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
alpha = 0.0
beta = 0.0
period_sto = 0
period_sm = 0
period_sig = 0
period_fast = 0
period_slow = 0
handle_fma = 0
handle_sma = 0

def OnInit():
    global alpha, beta, handle_fma, handle_sma, overbought, oversold, period_fast, period_sig, period_slow, period_sm, period_sto
    period_sto = (2 if (InpPeriodSto < 2) else InpPeriodSto)
    period_sm = (1 if (InpPeriodSm < 1) else InpPeriodSm)
    period_sig = (1 if (InpPeriodSig < 1) else InpPeriodSig)
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = ((period_fast + 1) if (InpPeriodSlow == period_fast) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    alpha = _fdiv(2.0, 1.0 + period_sig)
    beta = _fdiv(2.0, 1.0 + period_sm)
    SetIndexBuffer(0, BufferDSS, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDDS2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMACD, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Double smoothed MACD Stochastic (' + _str(period_sto) + ',' + _str(period_sm) + ',' + _str(period_sig) + ',' + _str(period_fast) + ',' + _str(period_slow) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferDSS, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferDDS2, True)
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fast, 0, MODE_EMA, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(period_fast), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_slow, 0, MODE_EMA, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(period_slow), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_sto, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_sto - 2
        ArrayInitialize(BufferDSS, 0)
        ArrayInitialize(BufferSignal, 0)
        ArrayInitialize(BufferDDS2, 0)
        ArrayInitialize(BufferMACD, 0)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferMACD[i] = BufferFMA[i] - BufferSMA[i]
        bl = ArrayMinimum(BufferMACD, i, period_sto)
        bh = ArrayMaximum(BufferMACD, i, period_sto)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = BufferMACD[bl]
        max_ = BufferMACD[bh]
        DDS1 = (_fdiv(100.0 * (BufferMACD[i] - min_), max_ - min_) if (min_ != max_) else 0)
        BufferDDS2[i] = BufferDDS2[i + 1] + (beta * (DDS1 - BufferDDS2[i + 1]))
    for i in range(limit, 0 - 1, -1):
        bl = ArrayMinimum(BufferDDS2, i, period_sto)
        bh = ArrayMaximum(BufferDDS2, i, period_sto)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = BufferDDS2[bl]
        max_ = BufferDDS2[bh]
        DDS3 = (_fdiv(100.0 * (BufferDDS2[i] - min_), max_ - min_) if (min_ != max_) else 0)
        BufferDSS[i] = BufferDSS[i + 1] + (beta * (DDS3 - BufferDSS[i + 1]))
        BufferSignal[i] = BufferSignal[i + 1] + (alpha * (BufferDSS[i] - BufferSignal[i + 1]))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DoubleSmoothedMACDStochastic(_MQL5Indicator):
    name = 'Double_Smoothed_MACD_Stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodSto': 32,  # Stochastic period
        'InpPeriodSm': 9,  # Smoothing
        'InpPeriodSig': 5,  # Signal period
        'InpPeriodFast': 12,  # Fast EMA period
        'InpPeriodSlow': 26,  # Slow EMA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
    }

