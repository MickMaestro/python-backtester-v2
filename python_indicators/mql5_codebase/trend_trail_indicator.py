"""Trend_Trail_Indicator — converted from MQL5: MQL5 Indicators/Trend_Trail_Indicator/Trend_Trail_Indicator.mq5

Trend Trail indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Stop line'}, 'levels': [], 'description': ['Trend Trail indicator'], 'name': 'Trend_Trail_Indicator', 'source': 'MQL5 Indicators/Trend_Trail_Indicator/Trend_Trail_Indicator.mq5', 'folder': 'Trend_Trail_Indicator', 'inputs': [{'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 10, 'label': 'ATR period', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 2.8, 'label': 'Multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodATR = _input('InpPeriodATR', 10)  # ATR period
InpMultiplier = _input('InpMultiplier', 2.8)  # Multiplier
BufferTrend = Arr(0, 0.0)
BufferHL = Arr(0, 0.0)
BufferDiff = Arr(0, 0.0)
BufferSupport = Arr(0, 0.0)
BufferWMA = Arr(0, 0.0)
period_atr = 0
multiplier = 0.0
k = 0.0

def OnInit():
    global k, multiplier, period_atr
    period_atr = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    multiplier = InpMultiplier
    k = _fdiv(1.0, period_atr)
    SetIndexBuffer(0, BufferTrend, INDICATOR_DATA)
    SetIndexBuffer(1, BufferHL, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDiff, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSupport, INDICATOR_DATA)
    SetIndexBuffer(4, BufferWMA, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend Trail (' + _str(period_atr) + ',' + DoubleToString(multiplier, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTrend, True)
    ArraySetAsSeries(BufferHL, True)
    ArraySetAsSeries(BufferDiff, True)
    ArraySetAsSeries(BufferSupport, True)
    ArraySetAsSeries(BufferWMA, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_atr, 5):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 5
        ArrayInitialize(BufferTrend, EMPTY_VALUE)
        ArrayInitialize(BufferHL, 0)
        ArrayInitialize(BufferDiff, 0)
        ArrayInitialize(BufferSupport, 0)
        ArrayInitialize(BufferWMA, 0)
    for i in range(limit, 0 - 1, -1):
        BufferHL[i] = high[i] - low[i]
        Avg_HL = GetSMA(rates_total, i, period_atr, BufferHL)
        HiLo = fmin(BufferHL[i], 1.5 * Avg_HL)
        Href = ((high[i] - close[i + 1] - ((low[i] - high[i + 1]) / 2.0)) if (low[i] > high[i + 1]) else (high[i] - close[i + 1]))
        Lref = ((close[i + 1] - low[i] - ((low[i + 1] - high[i]) / 2.0)) if (high[i] < low[i + 1]) else (close[i + 1] - low[i]))
        diff1 = fmax(HiLo, Href)
        BufferDiff[i] = fmax(diff1, Lref)
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - 2):
            BufferWMA[i] = GetSMA(rates_total, i, period_atr, BufferDiff)
            BufferSupport[i] = close[i]
            BufferTrend[i] = close[i]
            continue
        BufferWMA[i] = ((BufferDiff[i] - BufferWMA[i + 1]) * k) + BufferWMA[i + 1]
        loss = multiplier * BufferWMA[i]
        resistance = close[i] + loss
        BufferSupport[i] = (low[i + 2] if (((low[i] >= low[i + 2] and low[i + 1] >= low[i + 2]) and low[i + 3] >= low[i + 2]) and low[i + 4] >= low[i + 2]) else (high[i + 1] * 0.9945) if (low[i] > (high[i + 1] * 1.0013)) else (BufferSupport[i + 1] * 1.05) if (low[i] > (BufferSupport[i + 1] * 1.1)) else BufferSupport[i + 1])
        BufferTrend[i] = (fmax(BufferTrend[i + 1], BufferSupport[i]) if (high[i] > BufferTrend[i + 1] and high[i + 1] > BufferTrend[i + 1]) else fmin(BufferTrend[i + 1], resistance) if (high[i] < BufferTrend[i + 1] and high[i + 1] < BufferTrend[i + 1]) else BufferSupport[i] if (high[i] > BufferTrend[i + 1]) else resistance)
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


class TrendTrailIndicator(_MQL5Indicator):
    name = 'Trend_Trail_Indicator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodATR': 10,  # ATR period
        'InpMultiplier': 2.8,  # Multiplier
    }

