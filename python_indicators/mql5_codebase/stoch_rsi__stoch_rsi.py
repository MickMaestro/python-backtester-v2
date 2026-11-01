"""Stoch_RSI — converted from MQL5: MQL5 Indicators/Stoch_RSI/Stoch_RSI.mq5

Adaptable Stochastic RSI indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Slow %K', 2: 'Slow %D'}, 'levels': [], 'description': ['Adaptable Stochastic RSI indicator'], 'name': 'Stoch_RSI', 'source': 'MQL5 Indicators/Stoch_RSI/Stoch_RSI.mq5', 'folder': 'Stoch_RSI', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 14, 'label': 'RSI Period', 'sinput': False}, {'mql': 'InpPeriodStoK', 'py': 'InpPeriodStoK', 'param': 'InpPeriodStoK', 'type': 'uint', 'default': 14, 'label': 'Stoch Period', 'sinput': False}, {'mql': 'InpSlowingK', 'py': 'InpSlowingK', 'param': 'InpSlowingK', 'type': 'uint', 'default': 3, 'label': 'Stoch Slowing K', 'sinput': False}, {'mql': 'InpSlowingD', 'py': 'InpSlowingD', 'param': 'InpSlowingD', 'type': 'uint', 'default': 5, 'label': 'Stoch Slowing D', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 14)  # RSI Period
InpPeriodStoK = _input('InpPeriodStoK', 14)  # Stoch Period
InpSlowingK = _input('InpSlowingK', 3)  # Stoch Slowing K
InpSlowingD = _input('InpSlowingD', 5)  # Stoch Slowing D
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferK = Arr(0, 0.0)
BufferD = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
BufferSKI = Arr(0, 0.0)
period_rsi = 0
period_k = 0
period_sk = 0
period_sd = 0
handle_rsi = 0
weight_sum = 0
overbought = 0.0
oversold = 0.0

def OnInit():
    global handle_rsi, overbought, oversold, period_k, period_rsi, period_sd, period_sk
    period_rsi = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    period_k = (1 if (InpPeriodStoK < 1) else InpPeriodStoK)
    period_sk = (2 if (InpSlowingK < 2) else InpSlowingK)
    period_sd = (2 if (InpSlowingD < 2) else InpSlowingD)
    oversold = (0 if (InpOversold < 0) else 99.9 if (InpOversold > 99.9) else InpOversold)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferK, INDICATOR_DATA)
    SetIndexBuffer(1, BufferD, INDICATOR_DATA)
    SetIndexBuffer(2, BufferRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferSKI, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Adaptable Stochastic RSI (' + _str(period_rsi) + ',' + _str(period_k) + ',' + _str(period_sk) + ',' + _str(period_sd) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    ArraySetAsSeries(BufferK, True)
    ArraySetAsSeries(BufferD, True)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferSKI, True)
    ResetLastError()
    handle_rsi = iRSI(None, PERIOD_CURRENT, period_rsi, InpAppliedPrice)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI(', _str(period_rsi), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferK, EMPTY_VALUE)
        ArrayInitialize(BufferD, EMPTY_VALUE)
        ArrayInitialize(BufferRSI, 0)
        ArrayInitialize(BufferSKI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        bl = ArrayMinimum(BufferRSI, i, period_k)
        bh = ArrayMaximum(BufferRSI, i, period_k)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = BufferRSI[bl]
        max_ = BufferRSI[bh]
        BufferSKI[i] = (100.0 if (min_ == max_) else _fdiv(100.0 * (BufferRSI[i] - min_), max_ - min_))
    if SimpleMAOnBuffer(rates_total, prev_calculated, period_k, period_sk, BufferSKI, BufferK) == 0:
        return 0
    if SimpleMAOnBuffer(rates_total, prev_calculated, period_sk, period_sd, BufferK, BufferD) == 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochRSI(_MQL5Indicator):
    name = 'Stoch_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 14,  # RSI Period
        'InpPeriodStoK': 14,  # Stoch Period
        'InpSlowingK': 3,  # Stoch Slowing K
        'InpSlowingD': 5,  # Stoch Slowing D
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
    }

