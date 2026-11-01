"""Wildhog — converted from MQL5: MQL5 Indicators/Wildhog/Wildhog.mq5

Wildhog oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2263842]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Wildhog'}, 'levels': [], 'description': ['Wildhog oscillator'], 'name': 'Wildhog', 'source': 'MQL5 Indicators/Wildhog/Wildhog.mq5', 'folder': 'Wildhog', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 8, 'label': 'Period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 70.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 30.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 8)  # Period
InpOverbought = _input('InpOverbought', 70.0)  # Overbought
InpOversold = _input('InpOversold', 30.0)  # Oversold
BufferWildhog = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period = 0

def OnInit():
    global overbought, oversold, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferWildhog, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Wildhog')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferWildhog, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferWildhog, 0)
    for i in range(limit, 0 - 1, -1):
        bl = Lowest(period, i)
        bh = Highest(period, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = low[bl]
        max_ = high[bh]
        if max_ != min_:
            BufferWildhog[i] = _fdiv(100.0 * (close[i] - min_), 3.0 * (max_ - min_)) + (BufferWildhog[i + 1] / 1.5)
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wildhog(_MQL5Indicator):
    name = 'Wildhog'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 8,  # Period
        'InpOverbought': 70.0,  # Overbought
        'InpOversold': 30.0,  # Oversold
    }

