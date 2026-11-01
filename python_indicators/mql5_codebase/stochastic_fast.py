"""Stochastic_Fast — converted from MQL5: MQL5 Indicators/Stochastic_Fast/Stochastic_Fast.mq5

Stochastic Fast
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'FSK', 2: 'FSD'}, 'levels': [], 'description': ['Stochastic Fast'], 'name': 'Stochastic_Fast', 'source': 'MQL5 Indicators/Stochastic_Fast/Stochastic_Fast.mq5', 'folder': 'Stochastic_Fast', 'inputs': [{'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 5, 'label': 'Period K', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 5, 'label': 'Period D', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodK = _input('InpPeriodK', 5)  # Period K
InpPeriodD = _input('InpPeriodD', 5)  # Period D
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferK = Arr(0, 0.0)
BufferD = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_k = 0
period_d = 0

def OnInit():
    global overbought, oversold, period_d, period_k
    period_k = (1 if (InpPeriodK < 1) else InpPeriodK)
    period_d = (2 if (InpPeriodD < 2) else InpPeriodD)
    oversold = (0 if (InpOversold < 0) else 99.9 if (InpOversold > 99.9) else InpOversold)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferK, INDICATOR_DATA)
    SetIndexBuffer(1, BufferD, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FStochastic(' + _str(period_k) + ',' + _str(period_d) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    ArraySetAsSeries(BufferK, True)
    ArraySetAsSeries(BufferD, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_k:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_k - 1
        ArrayInitialize(BufferK, 0)
        ArrayInitialize(BufferD, 0)
    for i in range(limit, 0 - 1, -1):
        bh = Highest(period_k, i)
        bl = Lowest(period_k, i)
        if bh == WRONG_VALUE or bl == WRONG_VALUE:
            continue
        min_ = close[i] - low[bl]
        max_ = high[bh] - low[bl]
        BufferK[i] = ((_fdiv(min_, max_) * 100.0) if (max_ > 0) else 50.0)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_d, BufferK, BufferD)
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMinimum(array) + start
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticFast(_MQL5Indicator):
    name = 'Stochastic_Fast'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodK': 5,  # Period K
        'InpPeriodD': 5,  # Period D
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
    }

