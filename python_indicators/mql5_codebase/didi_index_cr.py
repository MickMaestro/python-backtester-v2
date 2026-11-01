"""Didi_Index_CR — converted from MQL5: MQL5 Indicators/Didi Index (Cleaned_Reversed)/Didi_Index_CR.mq5

Copyright: Copyright 2021, Manuel Alejandro Cercós Pérez; Link: https://www.mql5.com/en/users/alexcercos; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, Manuel Alejandro Cercós Pérez', 'link': 'https://www.mql5.com/en/users/alexcercos', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [10526303]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Didi Index'}, 'levels': [1.0], 'description': [], 'name': 'Didi_Index_CR', 'source': 'MQL5 Indicators/Didi Index (Cleaned_Reversed)/Didi_Index_CR.mq5', 'folder': 'Didi Index (Cleaned_Reversed)', 'inputs': [{'mql': 'Method', 'py': 'Method', 'param': 'Method', 'type': 'int', 'default': 0, 'label': 'Smoothing Method', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Price Values', 'sinput': False}, {'mql': 'MeanPeriod', 'py': 'MeanPeriod', 'param': 'MeanPeriod', 'type': 'int', 'default': 8, 'label': 'Mean MA Period', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'int', 'default': 20, 'label': 'Slow MA Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Method = _input('Method', MODE_SMA)  # Smoothing Method
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)  # Price Values
MeanPeriod = _input('MeanPeriod', 8)  # Mean MA Period
SlowPeriod = _input('SlowPeriod', 20)  # Slow MA Period
FinalBuffer = Arr(0, 0.0)
MeanBuffer = Arr(0, 0.0)
SlowBuffer = Arr(0, 0.0)
average_handle = 0
long_handle = 0
max_period = 0

def OnInit():
    global average_handle, long_handle, max_period
    SetIndexBuffer(0, FinalBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MeanBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, SlowBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(FinalBuffer, True)
    ArraySetAsSeries(MeanBuffer, True)
    ArraySetAsSeries(SlowBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    ArrayInitialize(SlowBuffer, EMPTY_VALUE)
    max_period = MathMax(MeanPeriod, SlowPeriod)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, max_period)
    average_handle = iMA(Symbol(), PERIOD_CURRENT, MeanPeriod, 0, Method, AppliedPrice)
    long_handle = iMA(Symbol(), PERIOD_CURRENT, SlowPeriod, 0, Method, AppliedPrice)
    if average_handle == INVALID_HANDLE or long_handle == INVALID_HANDLE:
        Print('Error starting handles!')
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'DidiIndex(' + IntegerToString(MeanPeriod) + ', ' + IntegerToString(SlowPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    IndicatorRelease(average_handle)
    IndicatorRelease(long_handle)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = MathMin(rates_total - prev_calculated, rates_total - max_period)
    if CopyBuffer(average_handle, 0, 0, limit + 1, MeanBuffer) <= 0:
        return prev_calculated
    if CopyBuffer(long_handle, 0, 0, limit + 1, SlowBuffer) <= 0:
        return prev_calculated
    for i in range(limit, 0 - 1, -1):
        FinalBuffer[i] = 2.0 - _fdiv(SlowBuffer[i], MeanBuffer[i])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DidiIndexCR(_MQL5Indicator):
    name = 'Didi_Index_CR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing Method
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price Values
        'MeanPeriod': 8,  # Mean MA Period
        'SlowPeriod': 20,  # Slow MA Period
    }

