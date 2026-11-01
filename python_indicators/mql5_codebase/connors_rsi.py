"""Connors_RSI — converted from MQL5: MQL5 Indicators/Connors_RSI/Connors_RSI.mq5

Larry Connors RSI oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11829830]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'CRSI'}, 'levels': [], 'description': ['Larry Connors RSI oscillator'], 'name': 'Connors_RSI', 'source': 'MQL5 Indicators/Connors_RSI/Connors_RSI.mq5', 'folder': 'Connors_RSI', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 3, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpPeriodSM', 'py': 'InpPeriodSM', 'param': 'InpPeriodSM', 'type': 'uint', 'default': 2, 'label': 'Pulse RCI period', 'sinput': False}, {'mql': 'InpPeriodPercRank', 'py': 'InpPeriodPercRank', 'param': 'InpPeriodPercRank', 'type': 'uint', 'default': 100, 'label': 'Percent rank period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 3)  # RSI period
InpPeriodSM = _input('InpPeriodSM', 2)  # Pulse RCI period
InpPeriodPercRank = _input('InpPeriodPercRank', 100)  # Percent rank period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferCRSI = Arr(0, 0.0)
BufferUpDown = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
BufferRSI2 = Arr(0, 0.0)
BufferArrRSI = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferPosRSI = Arr(0, 0.0)
BufferNegRSI = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_rsi = 0
period_sm = 0
period_rnk = 0
period_max = 0
handle_rsi = 0
handle_rsi2 = 0
handle_ma = 0

def OnInit():
    global handle_ma, handle_rsi, handle_rsi2, overbought, oversold, period_max, period_rnk, period_rsi, period_sm
    period_rsi = (2 if (InpPeriodRSI < 2) else InpPeriodRSI)
    period_sm = (2 if (InpPeriodSM < 2) else InpPeriodSM)
    period_rnk = (1 if (InpPeriodPercRank < 1) else InpPeriodPercRank)
    period_max = fmax(period_sm, period_rnk)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferCRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUpDown, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferRSI2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferArrRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferPosRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferNegRSI, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Connors RSI (' + _str(period_rsi) + ',' + _str(period_sm) + ',' + _str(period_rnk) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    ArraySetAsSeries(BufferCRSI, True)
    ArraySetAsSeries(BufferUpDown, True)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferRSI2, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferArrRSI, True)
    ArraySetAsSeries(BufferPosRSI, True)
    ArraySetAsSeries(BufferNegRSI, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_rsi2 = iRSI(None, PERIOD_CURRENT, 2, InpAppliedPrice)
    if handle_rsi2 == INVALID_HANDLE:
        Print('The iRSI(2) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_rsi = iRSI(None, PERIOD_CURRENT, period_rsi, InpAppliedPrice)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI(', _str(period_rsi), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferCRSI, EMPTY_VALUE)
        ArrayInitialize(BufferUpDown, 0)
        ArrayInitialize(BufferRSI, 0)
        ArrayInitialize(BufferRSI2, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferArrRSI, 0)
        ArrayInitialize(BufferPosRSI, 0)
        ArrayInitialize(BufferNegRSI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_rsi2, 0, 0, count, BufferRSI2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferUpDown[i] = (((BufferUpDown[i + 1] + 1) if (BufferUpDown[i + 1] > 0) else 1) if (BufferMA[i] > BufferMA[i + 1]) else ((BufferUpDown[i + 1] - 1) if (BufferUpDown[i + 1] < 0) else -1) if (BufferMA[i] < BufferMA[i + 1]) else 0)
    if RSIOnArray(rates_total, prev_calculated, 0, period_sm, BufferUpDown, BufferPosRSI, BufferNegRSI, BufferArrRSI) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        RSI1 = BufferRSI[i]
        RSI2 = BufferArrRSI[i]
        RSI3 = PercentRank(i)
        BufferCRSI[i] = (RSI1 + RSI2 + RSI3) / 3.0
    return rates_total

def PercentRank(index):
    count = 0.0
    for i in range(1, period_rnk + 1):
        if BufferRSI2[index] > BufferRSI2[index + i]:
            count += 1
    return _fdiv(100.0 * count, float(period_rnk))

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


class ConnorsRSI(_MQL5Indicator):
    name = 'Connors_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 3,  # RSI period
        'InpPeriodSM': 2,  # Pulse RCI period
        'InpPeriodPercRank': 100,  # Percent rank period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
    }

