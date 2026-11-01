"""Breakout_RSI — converted from MQL5: MQL5 Indicators/Breakout_RSI/Breakout_RSI.mq5

Breakout RSI oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [10526303]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'BRSI'}, 'levels': [], 'description': ['Breakout RSI oscillator'], 'name': 'Breakout_RSI', 'source': 'MQL5 Indicators/Breakout_RSI/Breakout_RSI.mq5', 'folder': 'Breakout_RSI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferBRSI = Arr(0, 0.0)
BufferBPower = Arr(0, 0.0)
BufferN = Arr(0, 0.0)
BufferP = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_rsi = 0

def OnInit():
    global overbought, oversold, period_rsi
    period_rsi = (2 if (InpPeriod < 2) else InpPeriod)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferBRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBPower, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferN, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferP, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Breakout RSI (' + _str(period_rsi) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Oversold')
    ArraySetAsSeries(BufferBRSI, True)
    ArraySetAsSeries(BufferBPower, True)
    ArraySetAsSeries(BufferN, True)
    ArraySetAsSeries(BufferP, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_rsi, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferBRSI, EMPTY_VALUE)
        ArrayInitialize(BufferBPower, 0)
        ArrayInitialize(BufferN, 0)
        ArrayInitialize(BufferP, 0)
    for i in range(limit, 0 - 1, -1):
        min_ = fmin(low[i], low[i + 1])
        max_ = fmax(high[i], high[i + 1])
        BPrice = (open[i + 1] + max_ + min_ + close[i]) / 4.0
        BStrength = (_fdiv(close[i] - open[i + 1], max_ - min_) if ((max_ - min_) != 0) else 0)
        BVolume = float(tick_volume[i] + tick_volume[i + 1])
        BufferBPower[i] = BPrice * BStrength * BVolume * Point()
        if BufferBPower[i] > BufferBPower[i + 1]:
            BufferP[i] = fabs(BufferBPower[i])
            BufferN[i] = 0.0
        else:
            BufferN[i] = fabs(BufferBPower[i])
            BufferP[i] = 0.0
        avgN = GetSMA(rates_total, i, period_rsi, BufferN)
        avgP = GetSMA(rates_total, i, period_rsi, BufferP)
        BufferBRSI[i] = ((100.0 - _fdiv(100.0, 1.0 + _fdiv(avgP, avgN))) if (avgN != 0) else 0)
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BreakoutRSI(_MQL5Indicator):
    name = 'Breakout_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
    }

