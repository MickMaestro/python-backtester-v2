"""Internal_Strength — converted from MQL5: MQL5 Indicators/Internal_Strength/Internal_Strength.mq5

Internal Strength oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [5737262]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Internal Strength'}, 'levels': [], 'description': ['Internal Strength oscillator'], 'name': 'Internal_Strength', 'source': 'MQL5 Indicators/Internal_Strength/Internal_Strength.mq5', 'folder': 'Internal_Strength', 'inputs': [{'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 1, 'label': 'Calculating mode', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 55.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 45.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CALC_MODE
MODE_HLC = 0
MODE_RSI = 1
_enum('ENUM_CALC_MODE', {0: 'MODE_HLC', 1: 'MODE_RSI'})

# ---- inputs and global variables
InpMode = _input('InpMode', MODE_RSI)  # Calculating mode
InpPeriod = _input('InpPeriod', 14)  # RSI period
InpOverbought = _input('InpOverbought', 55.0)  # Overbought
InpOversold = _input('InpOversold', 45.0)  # Oversold
BufferData = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
BufferPos = Arr(0, 0.0)
BufferNeg = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
center = 0.0
period_rsi = 0

def OnInit():
    global center, overbought, oversold, period_rsi
    period_rsi = (1 if (InpPeriod < 1) else InpPeriod)
    overbought = (50.1 if (InpOverbought <= 50.0) else InpOverbought)
    oversold = ((overbought - 0.1) if (InpOversold >= overbought) else 49.9 if (InpOversold >= 50.0) else InpOversold)
    center = 50.0
    if InpMode == MODE_HLC:
        overbought = overbought / 100.0
        oversold = oversold / 100.0
        center = center / 100.0
    SetIndexBuffer(0, BufferData, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferPos, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferNeg, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Internal Strength (' + _str(period_rsi) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, center)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Oversold')
    ArraySetAsSeries(BufferData, True)
    ArraySetAsSeries(BufferRAW, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_rsi, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferData, EMPTY_VALUE)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferPos, 0)
        ArrayInitialize(BufferNeg, 0)
    for i in range(limit, 0 - 1, -1):
        hl = high[i] - low[i]
        BufferRAW[i] = (_fdiv(close[i] - low[i], hl) if (hl != 0) else 0)
        if InpMode == MODE_HLC:
            BufferData[i] = BufferRAW[i]
    if InpMode == MODE_RSI:
        return RSIOnArray(rates_total, prev_calculated, 0, period_rsi, BufferRAW, BufferPos, BufferNeg, BufferData)
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


class InternalStrength(_MQL5Indicator):
    name = 'Internal_Strength'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMode': _Choice({0: 'HLC', 1: 'RSI'}, default=1),  # Calculating mode
        'InpPeriod': 14,  # RSI period
        'InpOverbought': 55.0,  # Overbought
        'InpOversold': 45.0,  # Oversold
    }

