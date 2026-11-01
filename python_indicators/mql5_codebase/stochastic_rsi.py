"""Stochastic_RSI — converted from MQL5: MQL5 Indicators/Stochastic_RSI/Stochastic_RSI.mq5

Stochastic RSI oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'RSI Stoch %K', 2: 'RSI Stoch %D'}, 'levels': [], 'description': ['Stochastic RSI oscillator'], 'name': 'Stochastic_RSI', 'source': 'MQL5 Indicators/Stochastic_RSI/Stochastic_RSI.mq5', 'folder': 'Stochastic_RSI', 'inputs': [{'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 14, 'label': 'Stochastic %K period', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 3, 'label': 'Stochastic %D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 5, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodK = _input('InpPeriodK', 14)  # Stochastic %K period
InpPeriodD = _input('InpPeriodD', 3)  # Stochastic %D period
InpSlowing = _input('InpSlowing', 5)  # Stochastic slowing
InpPeriodRSI = _input('InpPeriodRSI', 14)  # RSI period
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferSK = Arr(0, 0.0)
BufferSD = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
BufferSKI = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
periodRSI = 0
periodK = 0
periodD = 0
slowing = 0
period_max = 0
handle_rsi = 0

def OnInit():
    global handle_rsi, overbought, oversold, periodD, periodK, periodRSI, period_max, slowing
    periodRSI = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    periodK = (1 if (InpPeriodK < 1) else InpPeriodK)
    periodD = (1 if (InpPeriodD < 1) else InpPeriodD)
    slowing = (1 if (InpSlowing < 1) else InpSlowing)
    period_max = fmax(periodD, fmax(periodK, slowing))
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferSK, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSD, INDICATOR_DATA)
    SetIndexBuffer(2, BufferRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferSKI, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic RSI(' + _str(periodK) + ',' + _str(periodD) + ',' + _str(slowing) + ',' + _str(periodRSI) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Oversold')
    ArraySetAsSeries(BufferSK, True)
    ArraySetAsSeries(BufferSD, True)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferSKI, True)
    ResetLastError()
    handle_rsi = iRSI(None, PERIOD_CURRENT, periodRSI, PRICE_CLOSE)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI(' + _str(periodRSI) + ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - periodK - 1
        ArrayInitialize(BufferSK, EMPTY_VALUE)
        ArrayInitialize(BufferSD, EMPTY_VALUE)
        ArrayInitialize(BufferRSI, 0)
        ArrayInitialize(BufferSKI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        min_ = DBL_MAX
        max_ = 0.0
        for j in range(i, i + periodK):
            if BufferRSI[j] > max_:
                max_ = BufferRSI[j]
            if BufferRSI[j] < min_:
                min_ = BufferRSI[j]
        BufferSKI[i] = ((_fdiv(BufferRSI[i] - min_, max_ - min_) * 100.0) if (min_ != max_) else 100.0)
    for i in range(limit, 0 - 1, -1):
        BufferSK[i] = SMA(rates_total, BufferSKI, slowing, i)
        BufferSD[i] = SMA(rates_total, BufferSK, periodD, i)
    for i in range(limit, 0 - 1, -1):
        pass
    return rates_total

def SMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return array_src[shift]
    sum_ = 0.0
    for i in range(0, period):
        sum_ += array_src[shift + i]
    return _fdiv(sum_, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticRSI(_MQL5Indicator):
    name = 'Stochastic_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodK': 14,  # Stochastic %K period
        'InpPeriodD': 3,  # Stochastic %D period
        'InpSlowing': 5,  # Stochastic slowing
        'InpPeriodRSI': 14,  # RSI period
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
    }

