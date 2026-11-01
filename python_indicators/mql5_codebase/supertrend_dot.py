"""SuperTrend_Dot — converted from MQL5: MQL5 Indicators/SuperTrend_Dot/SuperTrend_Dot.mq5

SuperTrend Dot indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Trend Up', 2: 'Trend Down'}, 'levels': [], 'description': ['SuperTrend Dot indicator'], 'name': 'SuperTrend_Dot', 'source': 'MQL5 Indicators/SuperTrend_Dot/SuperTrend_Dot.mq5', 'folder': 'SuperTrend_Dot', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 1.5, 'label': 'Multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpMultiplier = _input('InpMultiplier', 1.5)  # Multiplier
BufferTrUP = Arr(0, 0.0)
BufferTrDN = Arr(0, 0.0)
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferTR = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
multiplier = 0.0
period = 0
handle_atr = 0

def OnInit():
    global handle_atr, multiplier, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    multiplier = (0 if (InpMultiplier < 0) else InpMultiplier)
    SetIndexBuffer(0, BufferTrUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTrDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferDN, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferTR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferATR, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SuperTrend Dot (' + _str(period) + ',' + DoubleToString(multiplier, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTrUP, True)
    ArraySetAsSeries(BufferTrDN, True)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferTR, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferTrUP, EMPTY_VALUE)
        ArrayInitialize(BufferTrDN, EMPTY_VALUE)
        ArrayInitialize(BufferUP, 0)
        ArrayInitialize(BufferDN, 0)
        ArrayInitialize(BufferTR, 0)
        ArrayInitialize(BufferATR, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        ATR = BufferATR[i]
        median = (high[i] + low[i]) / 2.0
        BufferUP[i] = median + (ATR * multiplier)
        BufferDN[i] = median - (ATR * multiplier)
        BufferTR[i] = (1 if (close[i] > BufferUP[i + 1]) else -1 if (close[i] < BufferDN[i + 1]) else BufferTR[i + 1])
        flag = (True if (BufferTR[i] < 0 and BufferTR[i + 1] > 0) else False)
        flagh = (True if (BufferTR[i] > 0 and BufferTR[i + 1] < 0) else False)
        if BufferTR[i] > 0 and BufferDN[i] < BufferDN[i + 1]:
            BufferDN[i] = BufferDN[i + 1]
        if BufferTR[i] < 0 and BufferUP[i] > BufferUP[i + 1]:
            BufferUP[i] = BufferUP[i + 1]
        if flag:
            BufferUP[i] = median + (ATR * multiplier)
        if flagh:
            BufferDN[i] = median - (ATR * multiplier)
        if BufferTR[i] == 1:
            BufferTrUP[i] = BufferDN[i]
            BufferTrDN[i] = EMPTY_VALUE
        else:
            BufferTrDN[i] = BufferUP[i]
            BufferTrUP[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SuperTrendDot(_MQL5Indicator):
    name = 'SuperTrend_Dot'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpMultiplier': 1.5,  # Multiplier
    }

