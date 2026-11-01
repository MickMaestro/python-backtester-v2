"""WVF_Stochastic — converted from MQL5: MQL5 Indicators/WVF_Stochastic/WVF_Stochastic.mq5

William’s VIX Fix Stochastic
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'K', 2: 'D'}, 'levels': [], 'description': ['William’s VIX Fix Stochastic'], 'name': 'WVF_Stochastic', 'source': 'MQL5 Indicators/WVF_Stochastic/WVF_Stochastic.mq5', 'folder': 'WVF_Stochastic', 'inputs': [{'mql': 'InpPeriodWVF', 'py': 'InpPeriodWVF', 'param': 'InpPeriodWVF', 'type': 'uint', 'default': 14, 'label': 'WVF period', 'sinput': False}, {'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 5, 'label': '%K period', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 3, 'label': '%D period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodWVF = _input('InpPeriodWVF', 14)  # WVF period
InpPeriodK = _input('InpPeriodK', 5)  # %K period
InpPeriodD = _input('InpPeriodD', 3)  # %D period
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferK = Arr(0, 0.0)
BufferD = Arr(0, 0.0)
BufferWVF = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_wvf = 0
period_k = 0
period_d = 0
period_max = 0

def OnInit():
    global overbought, oversold, period_d, period_k, period_max, period_wvf
    period_wvf = (1 if (InpPeriodWVF < 1) else InpPeriodWVF)
    period_k = (1 if (InpPeriodK < 1) else InpPeriodK)
    period_d = (1 if (InpPeriodD < 1) else InpPeriodD)
    period_max = fmax(period_wvf, fmax(period_k, period_d))
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferK, INDICATOR_DATA)
    SetIndexBuffer(1, BufferD, INDICATOR_DATA)
    SetIndexBuffer(2, BufferWVF, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'WVF Stochastic (' + _str(period_wvf) + ',' + _str(period_k) + ',' + _str(period_d) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    ArraySetAsSeries(BufferK, True)
    ArraySetAsSeries(BufferD, True)
    ArraySetAsSeries(BufferWVF, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 1
        ArrayInitialize(BufferK, EMPTY_VALUE)
        ArrayInitialize(BufferD, EMPTY_VALUE)
        ArrayInitialize(BufferWVF, 0)
    for i in range(limit, 0 - 1, -1):
        bh = HighestClose(period_wvf, i)
        if bh == WRONG_VALUE:
            continue
        max_ = close[bh]
        BufferWVF[i] = (_fdiv(100 * (max_ - low[i]), max_) if (max_ > 0) else 0)
    for i in range(limit, 0 - 1, -1):
        bl = ArrayMinimum(BufferWVF, i, period_k)
        bh = ArrayMaximum(BufferWVF, i, period_k)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        minLow = BufferWVF[bl]
        maxHigh = BufferWVF[bh]
        mins = BufferWVF[i] - minLow
        maxes = maxHigh - minLow
        BufferK[i] = (_fdiv(100.0 * mins, maxes) if (maxes > 0) else 50.0)
        BufferD[i] = GetSMA(rates_total, i, period_d, BufferK)
    return rates_total

def HighestClose(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMaximum(array) + start) if (CopyClose(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

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


class WVFStochastic(_MQL5Indicator):
    name = 'WVF_Stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodWVF': 14,  # WVF period
        'InpPeriodK': 5,  # %K period
        'InpPeriodD': 3,  # %D period
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
    }

