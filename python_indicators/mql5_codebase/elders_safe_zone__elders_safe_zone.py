"""Elders_Safe_Zone — converted from MQL5: MQL5 Indicators/Elders_Safe_Zone/Elders_Safe_Zone.mq5

Elder's Safe Zone indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ESZ'}, 'levels': [], 'description': ["Elder's Safe Zone indicator"], 'name': 'Elders_Safe_Zone', 'source': 'MQL5 Indicators/Elders_Safe_Zone/Elders_Safe_Zone.mq5', 'folder': 'Elders_Safe_Zone', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'ESZ Period', 'sinput': False}, {'mql': 'InpStopFactor', 'py': 'InpStopFactor', 'param': 'InpStopFactor', 'type': 'uint', 'default': 3, 'label': 'Stop factor', 'sinput': False}, {'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'uint', 'default': 13, 'label': 'EMA period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # ESZ Period
InpStopFactor = _input('InpStopFactor', 3)  # Stop factor
InpPeriodEMA = _input('InpPeriodEMA', 13)  # EMA period
BufferESZ = Arr(0, 0.0)
BufferEMA = Arr(0, 0.0)
period_esz = 0
period_ema = 0
stop_factor = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ema, period_esz, stop_factor
    period_esz = (1 if (InpPeriod < 1) else InpPeriod)
    period_ema = (1 if (InpPeriodEMA < 1) else InpPeriodEMA)
    stop_factor = (1 if (InpStopFactor < 1) else InpStopFactor)
    SetIndexBuffer(0, BufferESZ, INDICATOR_DATA)
    SetIndexBuffer(1, BufferEMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, "Elder's Safe Zone (" + _str(period_esz) + ',' + _str(stop_factor) + ',' + _str(period_ema) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferESZ, True)
    ArraySetAsSeries(BufferEMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ema, 0, MODE_EMA, PRICE_CLOSE)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_esz, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_esz - 3
        ArrayInitialize(BufferESZ, EMPTY_VALUE)
        ArrayInitialize(BufferEMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferEMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        PreSafeStop = BufferESZ[i + 1]
        Pen = 0.0
        Counter = 0.0
        SafeStop = 0.0
        if BufferEMA[i] > BufferEMA[i + 1]:
            for j in range(0, period_esz):
                if low[i + j] < low[i + j + 1]:
                    Pen = low[i + j + 1] - low[i + j] + Pen
                    Counter += 1
            if Counter > 0:
                SafeStop = close[i] - (stop_factor * _fdiv(Pen, Counter))
            else:
                SafeStop = close[i] - (stop_factor * Pen)
            if SafeStop < PreSafeStop and BufferEMA[i + 1] > BufferEMA[i + 2]:
                SafeStop = PreSafeStop
        elif BufferEMA[i] < BufferEMA[i + 1]:
            for j in range(0, period_esz):
                if high[i + j] > high[i + j + 1]:
                    Pen = high[i + j] - high[i + j + 1] + Pen
                    Counter += 1
            if Counter > 0:
                SafeStop = close[i] + (stop_factor * _fdiv(Pen, Counter))
            else:
                SafeStop = close[i] + (stop_factor * Pen)
            if SafeStop > PreSafeStop and BufferEMA[i + 1] < BufferEMA[i + 2]:
                SafeStop = PreSafeStop
        PreSafeStop = SafeStop
        BufferESZ[i] = SafeStop
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EldersSafeZone(_MQL5Indicator):
    name = 'Elders_Safe_Zone'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # ESZ Period
        'InpStopFactor': 3,  # Stop factor
        'InpPeriodEMA': 13,  # EMA period
    }

