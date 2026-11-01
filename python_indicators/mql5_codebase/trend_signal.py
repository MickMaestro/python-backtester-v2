"""Trend_Signal — converted from MQL5: MQL5 Indicators/Trend_Signal/Trend_Signal.mq5

Trend Signal indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 3, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bearish signal', 2: 'Bullish signal'}, 'levels': [], 'description': ['Trend Signal indicator'], 'name': 'Trend_Signal', 'source': 'MQL5 Indicators/Trend_Signal/Trend_Signal.mq5', 'folder': 'Trend_Signal', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 9, 'label': 'Period', 'sinput': False}, {'mql': 'InpRisk', 'py': 'InpRisk', 'param': 'InpRisk', 'type': 'uint', 'default': 30, 'label': 'Risk', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 9)  # Period
InpRisk = _input('InpRisk', 30)  # Risk
BufferUp = Arr(0, 0.0)
BufferDn = Arr(0, 0.0)
BufferTrend = Arr(0, 0.0)
period = 0
risk = 0

def OnInit():
    global period, risk
    period = (1 if (InpPeriod < 1) else InpPeriod)
    risk = (1 if (InpRisk < 1) else InpRisk)
    SetIndexBuffer(0, BufferDn, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUp, INDICATOR_DATA)
    SetIndexBuffer(2, BufferTrend, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend Signal (' + _str(period) + ',' + _str(risk) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    ArraySetAsSeries(BufferUp, True)
    ArraySetAsSeries(BufferDn, True)
    ArraySetAsSeries(BufferTrend, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 2
        ArrayInitialize(BufferUp, EMPTY_VALUE)
        ArrayInitialize(BufferDn, EMPTY_VALUE)
        ArrayInitialize(BufferTrend, 0)
    for i in range(limit, 0 - 1, -1):
        bh = Highest(period, i + 1)
        bl = Lowest(period, i + 1)
        if bh == WRONG_VALUE or bl == WRONG_VALUE:
            continue
        max_ = high[bh]
        min_ = low[bl]
        Max = max_ - (((max_ - min_) * risk) / 100.0)
        Min = min_ + (((max_ - min_) * risk) / 100.0)
        BufferUp[i] = EMPTY_VALUE
        BufferDn[i] = BufferUp[i]
        if (close[i + 1] < Max and close[i] > Max) and BufferTrend[i + 1] != 1.0:
            BufferTrend[i] = 1.0
            BufferUp[i] = open[i]
        else:
            if (close[i + 1] > Min and close[i] < Min) and BufferTrend[i + 1] != -1.0:
                BufferTrend[i] = -1.0
                BufferDn[i] = open[i]
            else:
                BufferTrend[i] = BufferTrend[i + 1]
    return rates_total

def Highest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendSignal(_MQL5Indicator):
    name = 'Trend_Signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 9,  # Period
        'InpRisk': 30,  # Risk
    }

