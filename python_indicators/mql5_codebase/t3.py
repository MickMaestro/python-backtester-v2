"""T3 — converted from MQL5: MQL5 Indicators/T3 Moving Average/T3.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 't3'}, 'levels': [], 'description': [], 'name': 'T3', 'source': 'MQL5 Indicators/T3 Moving Average/T3.mq5', 'folder': 'T3 Moving Average', 'inputs': [{'mql': 'T3_Length', 'py': 'T3_Length', 'param': 'T3_Length', 'type': 'int', 'default': 12, 'label': 'Period length for the T3 calculation (default: 12)', 'sinput': False}, {'mql': 'T3_Factor', 'py': 'T3_Factor', 'param': 'T3_Factor', 'type': 'double', 'default': 0.7, 'label': 'Volume factor for the T3 calculation (default: 0.7)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
T3_Length = _input('T3_Length', 12)  # Period length for the T3 calculation (default: 12)
T3_Factor = _input('T3_Factor', 0.7)  # Volume factor for the T3 calculation (default: 0.7)
T3Buffer = Arr(0, 0.0)
hEMA1 = 0
hEMA2 = 0
hEMA3 = 0
hEMA4 = 0
hEMA5 = 0
hEMA6 = 0

def OnInit():
    global hEMA1, hEMA2, hEMA3, hEMA4, hEMA5, hEMA6
    hEMA1 = iMA(Symbol(), PERIOD_CURRENT, T3_Length, 0, MODE_EMA, PRICE_CLOSE)
    hEMA2 = iMA(Symbol(), PERIOD_CURRENT, T3_Length, 0, MODE_EMA, hEMA1)
    hEMA3 = iMA(Symbol(), PERIOD_CURRENT, T3_Length, 0, MODE_EMA, hEMA2)
    hEMA4 = iMA(Symbol(), PERIOD_CURRENT, T3_Length, 0, MODE_EMA, hEMA3)
    hEMA5 = iMA(Symbol(), PERIOD_CURRENT, T3_Length, 0, MODE_EMA, hEMA4)
    hEMA6 = iMA(Symbol(), PERIOD_CURRENT, T3_Length, 0, MODE_EMA, hEMA5)
    SetIndexBuffer(0, T3Buffer)
    ArraySetAsSeries(T3Buffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'T3 Indicator')
    return INIT_SUCCEEDED

def T3(length, factor, shift):
    ema1 = Arr(0, 0.0)
    ema2 = Arr(0, 0.0)
    ema3 = Arr(0, 0.0)
    ema4 = Arr(0, 0.0)
    ema5 = Arr(0, 0.0)
    ema6 = Arr(0, 0.0)
    ArraySetAsSeries(ema1, True)
    ArraySetAsSeries(ema2, True)
    ArraySetAsSeries(ema3, True)
    ArraySetAsSeries(ema4, True)
    ArraySetAsSeries(ema5, True)
    ArraySetAsSeries(ema6, True)
    CopyBuffer(hEMA1, 0, shift, 1, ema1)
    CopyBuffer(hEMA2, 0, shift, 1, ema2)
    CopyBuffer(hEMA3, 0, shift, 1, ema3)
    CopyBuffer(hEMA4, 0, shift, 1, ema4)
    CopyBuffer(hEMA5, 0, shift, 1, ema5)
    CopyBuffer(hEMA6, 0, shift, 1, ema6)
    c1 = (-factor) * factor * factor
    c2 = (3 * factor * factor) + (3 * factor * factor * factor)
    c3 = (-6 * factor * factor) - (3 * factor) - (3 * factor * factor * factor)
    c4 = 1 + (3 * factor) + (factor * factor * factor) + (3 * factor * factor)
    return (c1 * ema6[0]) + (c2 * ema5[0]) + (c3 * ema4[0]) + (c4 * ema3[0])

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(0, rates_total - prev_calculated):
        T3Buffer[i] = T3(T3_Length, T3_Factor, i)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3Indicator(_MQL5Indicator):
    name = 'T3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'T3_Length': 12,  # Period length for the T3 calculation (default: 12)
        'T3_Factor': 0.7,  # Volume factor for the T3 calculation (default: 0.7)
    }

