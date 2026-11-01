"""RSS — converted from MQL5: MQL5 Indicators/RSS/RSS.mq5

Relative Spread Strength indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [10061943]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'RSS'}, 'levels': [], 'description': ['Relative Spread Strength indicator'], 'name': 'RSS', 'source': 'MQL5 Indicators/RSS/RSS.mq5', 'folder': 'RSS', 'inputs': [{'mql': 'InpPeriodFastMA', 'py': 'InpPeriodFastMA', 'param': 'InpPeriodFastMA', 'type': 'uint', 'default': 10, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpPeriodSlowMA', 'py': 'InpPeriodSlowMA', 'param': 'InpPeriodSlowMA', 'type': 'uint', 'default': 50, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 5, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 5, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 70.0, 'label': 'Overbought level', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 30.0, 'label': 'Oversold level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodFastMA = _input('InpPeriodFastMA', 10)  # Fast EMA period
InpPeriodSlowMA = _input('InpPeriodSlowMA', 50)  # Slow EMA period
InpPeriodRSI = _input('InpPeriodRSI', 5)  # RSI period
InpPeriodSm = _input('InpPeriodSm', 5)  # Smoothing period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverbought = _input('InpOverbought', 70.0)  # Overbought level
InpOversold = _input('InpOversold', 30.0)  # Oversold level
BufferRSS = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
BufferSpread = Arr(0, 0.0)
BufferPos = Arr(0, 0.0)
BufferNeg = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_fma = 0
period_sma = 0
period_rsi = 0
period_sm = 0
weight_sum = 0
handle_fma = 0
handle_sma = 0

def OnInit():
    global handle_fma, handle_sma, overbought, oversold, period_fma, period_rsi, period_sm, period_sma
    period_fma = (1 if (InpPeriodFastMA < 1) else InpPeriodFastMA)
    period_sma = ((period_fma + 1) if (InpPeriodSlowMA == period_fma) else 1 if (InpPeriodSlowMA < 1) else InpPeriodSlowMA)
    period_rsi = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    period_sm = (2 if (InpPeriodSm < 2) else InpPeriodSm)
    oversold = (0 if (InpOversold < 0) else 99.9 if (InpOversold > 99.9) else InpOversold)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferRSS, INDICATOR_DATA)
    SetIndexBuffer(1, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferSMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSpread, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferPos, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferNeg, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Relative Spread Strength (' + _str(period_fma) + ',' + _str(period_sma) + ',' + _str(period_rsi) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    ArraySetAsSeries(BufferRSS, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferSpread, True)
    ArraySetAsSeries(BufferPos, True)
    ArraySetAsSeries(BufferNeg, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fma, 0, MODE_EMA, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(period_fma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_sma, 0, MODE_EMA, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(period_sma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferRSS, EMPTY_VALUE)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
        ArrayInitialize(BufferRSI, 0)
        ArrayInitialize(BufferSpread, 0)
        ArrayInitialize(BufferPos, 0)
        ArrayInitialize(BufferNeg, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferSpread[i] = BufferFMA[i] - BufferSMA[i]
    RSIOnArray(rates_total, prev_calculated, 0, period_rsi, BufferSpread, BufferPos, BufferNeg, BufferRSI)
    if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferRSI, BufferRSS) == 0:
        return 0
    return rates_total

def RSIOnArray(rates_total, prev_calculated, begin, period, price, buffer_pos, buffer_neg, buffer_rsi):
    i = 0
    diff = 0
    if period < 1 or (rates_total - begin) < period:
        return 0
    as_series_price = ArrayGetAsSeries(price)
    as_series_rsi = ArrayGetAsSeries(buffer_rsi)
    if as_series_price:
        ArraySetAsSeries(price, False)
    if as_series_rsi:
        ArraySetAsSeries(buffer_rsi, False)
        ArraySetAsSeries(buffer_pos, False)
        ArraySetAsSeries(buffer_neg, False)
    pos = prev_calculated - 1
    if pos <= period:
        buffer_rsi[0] = 0.0
        buffer_pos[0] = 0.0
        buffer_neg[0] = 0.0
        SumP = 0.0
        SumN = 0.0
        i = 1
        for i in range(i, period + 1):
            buffer_rsi[i] = 0.0
            buffer_pos[i] = 0.0
            buffer_neg[i] = 0.0
            diff = price[i] - price[i - 1]
            SumP += (diff if (diff > 0) else 0)
            SumN += ((-diff) if (diff < 0) else 0)
        else:
            i = _range_end(i, period + 1, 1)
        buffer_pos[period] = _fdiv(SumP, period)
        buffer_neg[period] = _fdiv(SumN, period)
        buffer_rsi[period] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(buffer_pos[period], (buffer_neg[period] if (buffer_neg[period] > 0) else DBL_MIN)))
        pos = period + 1
    i = pos
    for i in range(i, rates_total):
        diff = price[i] - price[i - 1]
        buffer_pos[i] = _fdiv((buffer_pos[i - 1] * (period - 1)) + (diff if (diff > 0.0) else 0.0), period)
        buffer_neg[i] = _fdiv((buffer_neg[i - 1] * (period - 1)) + ((-diff) if (diff < 0.0) else 0.0), period)
        buffer_rsi[i] = 100.0 - _fdiv(100.0, 1 + _fdiv(buffer_pos[i], (buffer_neg[i] if (buffer_neg[i] > 0) else DBL_MIN)))
    else:
        i = _range_end(i, rates_total, 1)
    if as_series_price:
        ArraySetAsSeries(price, True)
    if as_series_rsi:
        ArraySetAsSeries(buffer_rsi, True)
        ArraySetAsSeries(buffer_pos, True)
        ArraySetAsSeries(buffer_neg, True)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSS(_MQL5Indicator):
    name = 'RSS'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastMA': 10,  # Fast EMA period
        'InpPeriodSlowMA': 50,  # Slow EMA period
        'InpPeriodRSI': 5,  # RSI period
        'InpPeriodSm': 5,  # Smoothing period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 70.0,  # Overbought level
        'InpOversold': 30.0,  # Oversold level
    }

