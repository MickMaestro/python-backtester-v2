"""TrendEQ — converted from MQL5: MQL5 Indicators/Trend Equilibrium Indicator TrendEQ/TrendEQ.mq5

Copyright: Copyright 2025, Simon Draxler; Link: drxtrading.com; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, Simon Draxler', 'link': 'drxtrading.com', 'version': '2.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [255], 3: [32768]}, 'widths': {1: 2, 2: 1, 3: 1}, 'styles': {1: 0, 2: 2, 3: 2}, 'labels': {1: 'TrendEquilibriumIndicator', 2: 'Overbought', 3: 'Oversold'}, 'levels': [], 'description': [], 'name': 'TrendEQ', 'source': 'MQL5 Indicators/Trend Equilibrium Indicator TrendEQ/TrendEQ.mq5', 'folder': 'Trend Equilibrium Indicator TrendEQ', 'inputs': [{'mql': 'momentum_period', 'py': 'momentum_period', 'param': 'momentum_period', 'type': 'int', 'default': 14, 'label': 'Number of candles to calculate momentum', 'sinput': False}, {'mql': 'volatility_period', 'py': 'volatility_period', 'param': 'volatility_period', 'type': 'int', 'default': 14, 'label': 'Number of candles to calculate volatility', 'sinput': False}, {'mql': 'scaling_factor', 'py': 'scaling_factor', 'param': 'scaling_factor', 'type': 'double', 'default': 100000.0, 'label': "Adjusts the indicator's readability", 'sinput': False}, {'mql': 'overbought_level', 'py': 'overbought_level', 'param': 'overbought_level', 'type': 'double', 'default': 100.0, 'label': 'Threshold above which market is overbought', 'sinput': False}, {'mql': 'oversold_level', 'py': 'oversold_level', 'param': 'oversold_level', 'type': 'double', 'default': -100.0, 'label': 'Threshold below which market is oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
momentum_period = _input('momentum_period', 14)  # Number of candles to calculate momentum
volatility_period = _input('volatility_period', 14)  # Number of candles to calculate volatility
scaling_factor = _input('scaling_factor', 100000.0)  # Adjusts the indicator's readability
overbought_level = _input('overbought_level', 100.0)  # Threshold above which market is overbought
oversold_level = _input('oversold_level', -100.0)  # Threshold below which market is oversold
trendEQ_buffer = Arr(0, 0.0)  # Stores calculated TrendEQ values
overbought_buffer = Arr(0, 0.0)  # Stores overbought level
oversold_buffer = Arr(0, 0.0)  # Stores oversold level

def OnInit():
    SetIndexBuffer(0, trendEQ_buffer, INDICATOR_DATA)
    SetIndexBuffer(1, overbought_buffer, INDICATOR_DATA)
    SetIndexBuffer(2, oversold_buffer, INDICATOR_DATA)
    shortName = 'TrendEQ(' + IntegerToString(momentum_period) + ',' + IntegerToString(volatility_period) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, shortName)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    required_bars = MathMax(momentum_period, volatility_period) + 1
    if rates_total < required_bars:
        return 0
    start = ((prev_calculated - 1) if (prev_calculated > 0) else required_bars)
    for i in range(start, rates_total):
        if i < momentum_period:
            trendEQ_buffer[i] = 0.0
            overbought_buffer[i] = overbought_level
            oversold_buffer[i] = oversold_level
            continue
        momentum = close[i] - close[i - momentum_period]
        volatility = 0.0
        for j in range(i - volatility_period + 1, i + 1):
            volatility += close[j]
        volatility = volatility / volatility_period
        if volatility > 0:
            trendEQ_buffer[i] = _fdiv(momentum, volatility * MathSqrt(momentum_period)) * scaling_factor
        else:
            trendEQ_buffer[i] = 0.0
        overbought_buffer[i] = overbought_level
        oversold_buffer[i] = oversold_level
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendEQ(_MQL5Indicator):
    name = 'TrendEQ'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'momentum_period': 14,  # Number of candles to calculate momentum
        'volatility_period': 14,  # Number of candles to calculate volatility
        'scaling_factor': 100000.0,  # Adjusts the indicator's readability
        'overbought_level': 100.0,  # Threshold above which market is overbought
        'oversold_level': -100.0,  # Threshold below which market is oversold
    }

