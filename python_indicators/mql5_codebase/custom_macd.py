"""Custom MACD — converted from MQL5: MQL5 Indicators/Custom MACD_ Elevate Your Trading with Real-Time Signal Alerts to Your Phone/Custom MACD.mq5

Copyright: Copyright 2025, Your Name; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, Your Name', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 3}, 'colors': {1: [16748574], 2: [42495], 3: [3329330]}, 'widths': {1: 2, 2: 1, 3: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MACD', 2: 'Signal', 3: 'Histogram'}, 'levels': [], 'description': [], 'name': 'Custom MACD', 'source': 'MQL5 Indicators/Custom MACD_ Elevate Your Trading with Real-Time Signal Alerts to Your Phone/Custom MACD.mq5', 'folder': 'Custom MACD_ Elevate Your Trading with Real-Time Signal Alerts to Your Phone', 'inputs': [{'mql': 'InpFastEMA', 'py': 'InpFastEMA', 'param': 'InpFastEMA', 'type': 'int', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpSlowEMA', 'py': 'InpSlowEMA', 'param': 'InpSlowEMA', 'type': 'int', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpSignalSMA', 'py': 'InpSignalSMA', 'param': 'InpSignalSMA', 'type': 'int', 'default': 9, 'label': 'Signal SMA period', 'sinput': False}, {'mql': 'ShowAlerts', 'py': 'ShowAlerts', 'param': 'ShowAlerts', 'type': 'bool', 'default': True, 'label': 'Show alerts for signals', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFastEMA = _input('InpFastEMA', 12)  # Fast EMA period
InpSlowEMA = _input('InpSlowEMA', 26)  # Slow EMA period
InpSignalSMA = _input('InpSignalSMA', 9)  # Signal SMA period
ShowAlerts = _input('ShowAlerts', True)  # Show alerts for signals
MACDBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
HistogramBuffer = Arr(0, 0.0)
FastEMABuffer = Arr(0, 0.0)
SlowEMABuffer = Arr(0, 0.0)
fast_ema_handle = 0
slow_ema_handle = 0

def OnInit():
    global fast_ema_handle, slow_ema_handle
    SetIndexBuffer(0, MACDBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, HistogramBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, FastEMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, SlowEMABuffer, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Custom MACD (' + IntegerToString(InpFastEMA) + ',' + IntegerToString(InpSlowEMA) + ',' + IntegerToString(InpSignalSMA) + ')')
    fast_ema_handle = iMA(None, 0, InpFastEMA, 0, MODE_EMA, PRICE_CLOSE)
    slow_ema_handle = iMA(None, 0, InpSlowEMA, 0, MODE_EMA, PRICE_CLOSE)
    if fast_ema_handle == INVALID_HANDLE or slow_ema_handle == INVALID_HANDLE:
        Print('Failed to create EMA handles')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if fast_ema_handle != INVALID_HANDLE:
        IndicatorRelease(fast_ema_handle)
    if slow_ema_handle != INVALID_HANDLE:
        IndicatorRelease(slow_ema_handle)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (InpSlowEMA + InpSignalSMA):
        return 0
    if CopyBuffer(fast_ema_handle, 0, 0, rates_total, FastEMABuffer) <= 0 or CopyBuffer(slow_ema_handle, 0, 0, rates_total, SlowEMABuffer) <= 0:
        Print('Failed to copy EMA data')
        return 0
    for i in range(0, rates_total):
        MACDBuffer[i] = FastEMABuffer[i] - SlowEMABuffer[i]
    for i in range(InpSignalSMA - 1, rates_total):
        sum_ = 0.0
        for j in range(0, InpSignalSMA):
            sum_ += MACDBuffer[i - j]
        SignalBuffer[i] = sum_ / InpSignalSMA
    for i in range(0, rates_total):
        HistogramBuffer[i] = MACDBuffer[i] - SignalBuffer[i]
    if (ShowAlerts and prev_calculated > 0) and rates_total > InpSignalSMA:
        for i in range(prev_calculated - 1, rates_total - 1):
            if MACDBuffer[i] > SignalBuffer[i] and MACDBuffer[i - 1] <= SignalBuffer[i - 1]:
                Alert('MACD Bullish Crossover at bar ', i, ': Buy Signal')
            if MACDBuffer[i] < SignalBuffer[i] and MACDBuffer[i - 1] >= SignalBuffer[i - 1]:
                Alert('MACD Bearish Crossover at bar ', i, ': Sell Signal')
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CustomMACD(_MQL5Indicator):
    name = 'Custom MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastEMA': 12,  # Fast EMA period
        'InpSlowEMA': 26,  # Slow EMA period
        'InpSignalSMA': 9,  # Signal SMA period
        'ShowAlerts': True,  # Show alerts for signals
    }

