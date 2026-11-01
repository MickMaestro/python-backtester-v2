"""FX_Trend — converted from MQL5: MQL5 Indicators/FX_Trend/FX_Trend.mq5

FX Trend oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [5737262]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'FX Trend'}, 'levels': [], 'description': ['FX Trend oscillator'], 'name': 'FX_Trend', 'source': 'MQL5 Indicators/FX_Trend/FX_Trend.mq5', 'folder': 'FX_Trend', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 7, 'label': 'Small range of bars', 'sinput': False}, {'mql': 'InpPeriodMiddle', 'py': 'InpPeriodMiddle', 'param': 'InpPeriodMiddle', 'type': 'uint', 'default': 14, 'label': 'Middle range of bars', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 28, 'label': 'Big range of bars', 'sinput': False}, {'mql': 'InpLevel', 'py': 'InpLevel', 'param': 'InpLevel', 'type': 'double', 'default': 50.0, 'label': 'Threshold level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 7)  # Small range of bars
InpPeriodMiddle = _input('InpPeriodMiddle', 14)  # Middle range of bars
InpPeriodSlow = _input('InpPeriodSlow', 28)  # Big range of bars
InpLevel = _input('InpLevel', 50.0)  # Threshold level
BufferFXT = Arr(0, 0.0)
level = 0.0
k = 0.0
period_fast = 0
period_middle = 0
period_slow = 0
period_max = 0

def OnInit():
    global k, level, period_fast, period_max, period_middle, period_slow
    period_fast = (2 if (InpPeriodFast < 2) else InpPeriodFast)
    period_middle = (2 if (InpPeriodMiddle < 2) else InpPeriodMiddle)
    period_slow = (2 if (InpPeriodSlow < 2) else InpPeriodSlow)
    period_max = fmax(period_fast, fmax(period_middle, period_slow))
    k = _fdiv(100.0, _fdiv(1.0, period_fast) + _fdiv(1.0, period_middle) + _fdiv(1.0, period_slow))
    level = (0 if (InpLevel < 0) else 100 if (InpLevel > 100) else InpLevel)
    SetIndexBuffer(0, BufferFXT, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FX Trend (' + _str(period_fast) + ',' + _str(period_middle) + ',' + _str(period_slow) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, level)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    ArraySetAsSeries(BufferFXT, True)
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
        ArrayInitialize(BufferFXT, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        blf = Lowest(period_fast, i)
        bhf = Highest(period_fast, i)
        blm = Lowest(period_middle, i)
        bhm = Highest(period_middle, i)
        bls = Lowest(period_slow, i)
        bhs = Highest(period_slow, i)
        if ((((blf == WRONG_VALUE or bhf == WRONG_VALUE) or blm == WRONG_VALUE) or bhm == WRONG_VALUE) or bls == WRONG_VALUE) or bhs == WRONG_VALUE:
            continue
        minf = low[blf]
        maxf = high[bhf]
        minm = low[blm]
        maxm = high[bhm]
        mins = low[bls]
        maxs = high[bhs]
        fdiff = maxf - minf
        mdiff = maxm - minm
        sdiff = maxs - mins
        v = k * (_fdiv(close[i] - minf, fdiff * period_fast) + _fdiv(close[i] - minm, mdiff * period_middle) + _fdiv(close[i] - mins, sdiff * period_slow))
        BufferFXT[i] = (v if (v != 0) else close[i])
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


class FXTrend(_MQL5Indicator):
    name = 'FX_Trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 7,  # Small range of bars
        'InpPeriodMiddle': 14,  # Middle range of bars
        'InpPeriodSlow': 28,  # Big range of bars
        'InpLevel': 50.0,  # Threshold level
    }

