"""StochasticEx — converted from MQL5: MQL5 Indicators/StochasticEx/StochasticEx.mq5

Stochastic expansion indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'K', 2: 'Signal'}, 'levels': [], 'description': ['Stochastic expansion indicator'], 'name': 'StochasticEx', 'source': 'MQL5 Indicators/StochasticEx/StochasticEx.mq5', 'folder': 'StochasticEx', 'inputs': [{'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 13, 'label': '%K period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 6, 'label': 'Slowing', 'sinput': False}, {'mql': 'InpNoiseFilter', 'py': 'InpNoiseFilter', 'param': 'InpNoiseFilter', 'type': 'uint', 'default': 6, 'label': 'Noise filter period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodK = _input('InpPeriodK', 13)  # %K period
InpSlowing = _input('InpSlowing', 6)  # Slowing
InpNoiseFilter = _input('InpNoiseFilter', 6)  # Noise filter period
BufferK = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferHigh = Arr(0, 0.0)
BufferLow = Arr(0, 0.0)
period_k = 0
slowing = 0
noise = 0
period_max = 0

def OnInit():
    global noise, period_k, period_max, slowing
    period_k = (1 if (InpPeriodK < 1) else InpPeriodK)
    slowing = (1 if (InpSlowing < 1) else InpSlowing)
    noise = (2 if (InpNoiseFilter < 2) else InpNoiseFilter)
    period_max = fmax(noise, fmax(slowing, period_k))
    SetIndexBuffer(0, BufferK, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHigh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferLow, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic expansion (' + _str(period_k) + ',' + _str(slowing) + ',' + _str(noise) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferK, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferHigh, True)
    ArraySetAsSeries(BufferLow, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_k - 1
        ArrayInitialize(BufferK, 0)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferHigh, 0)
        ArrayInitialize(BufferLow, 0)
    for i in range(limit, 0 - 1, -1):
        bl = Lowest(period_k, i)
        bh = Highest(period_k, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = low[bl]
        max_ = high[bh]
        BufferLow[i] = close[i] - min_
        BufferHigh[i] = max_ - close[i]
        Avg_Low = GetSMA(rates_total, i, slowing, BufferLow)
        Avg_High = GetSMA(rates_total, i, slowing, BufferHigh)
        KB1 = (_fdiv(Avg_Low, Avg_High) if (Avg_High != 0) else 0)
        KB2 = (_fdiv(-Avg_High, Avg_Low) if (Avg_Low != 0) else 0)
        BufferK[i] = KB1 + KB2
        BufferSignal[i] = GetSMA(rates_total, i, noise, BufferK)
    return rates_total

def Highest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

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


class StochasticEx(_MQL5Indicator):
    name = 'StochasticEx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodK': 13,  # %K period
        'InpSlowing': 6,  # Slowing
        'InpNoiseFilter': 6,  # Noise filter period
    }

