"""Elders_Safe_Zone_Triple — converted from MQL5: MQL5 Indicators/Elders_Safe_Zone_Triple/Elders_Safe_Zone_Triple.mq5

Elder's Triple Safe Zone indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [32768], 2: [16748574], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'ESZ One', 2: 'ESZ Two', 3: 'ESZ Three'}, 'levels': [], 'description': ["Elder's Triple Safe Zone indicator"], 'name': 'Elders_Safe_Zone_Triple', 'source': 'MQL5 Indicators/Elders_Safe_Zone_Triple/Elders_Safe_Zone_Triple.mq5', 'folder': 'Elders_Safe_Zone_Triple', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 10, 'label': 'First ESZ Period', 'sinput': False}, {'mql': 'InpStopFactor1', 'py': 'InpStopFactor1', 'param': 'InpStopFactor1', 'type': 'uint', 'default': 3, 'label': 'First Stop factor', 'sinput': False}, {'mql': 'InpPeriodEMA1', 'py': 'InpPeriodEMA1', 'param': 'InpPeriodEMA1', 'type': 'uint', 'default': 13, 'label': 'First EMA period', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 20, 'label': 'Second ESZ Period', 'sinput': False}, {'mql': 'InpStopFactor2', 'py': 'InpStopFactor2', 'param': 'InpStopFactor2', 'type': 'uint', 'default': 6, 'label': 'Second Stop factor', 'sinput': False}, {'mql': 'InpPeriodEMA2', 'py': 'InpPeriodEMA2', 'param': 'InpPeriodEMA2', 'type': 'uint', 'default': 50, 'label': 'Second EMA period', 'sinput': False}, {'mql': 'InpPeriod3', 'py': 'InpPeriod3', 'param': 'InpPeriod3', 'type': 'uint', 'default': 30, 'label': 'Third ESZ Period', 'sinput': False}, {'mql': 'InpStopFactor3', 'py': 'InpStopFactor3', 'param': 'InpStopFactor3', 'type': 'uint', 'default': 10, 'label': 'Third Stop factor', 'sinput': False}, {'mql': 'InpPeriodEMA3', 'py': 'InpPeriodEMA3', 'param': 'InpPeriodEMA3', 'type': 'uint', 'default': 100, 'label': 'Third EMA period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 10)  # First ESZ Period
InpStopFactor1 = _input('InpStopFactor1', 3)  # First Stop factor
InpPeriodEMA1 = _input('InpPeriodEMA1', 13)  # First EMA period
InpPeriod2 = _input('InpPeriod2', 20)  # Second ESZ Period
InpStopFactor2 = _input('InpStopFactor2', 6)  # Second Stop factor
InpPeriodEMA2 = _input('InpPeriodEMA2', 50)  # Second EMA period
InpPeriod3 = _input('InpPeriod3', 30)  # Third ESZ Period
InpStopFactor3 = _input('InpStopFactor3', 10)  # Third Stop factor
InpPeriodEMA3 = _input('InpPeriodEMA3', 100)  # Third EMA period
BufferESZ1 = Arr(0, 0.0)
BufferESZ2 = Arr(0, 0.0)
BufferESZ3 = Arr(0, 0.0)
BufferEMA1 = Arr(0, 0.0)
BufferEMA2 = Arr(0, 0.0)
BufferEMA3 = Arr(0, 0.0)
period_esz1 = 0
period_esz2 = 0
period_esz3 = 0
period_ema1 = 0
period_ema2 = 0
period_ema3 = 0
stop_factor1 = 0
stop_factor2 = 0
stop_factor3 = 0
period_max = 0
handle_ma1 = 0
handle_ma2 = 0
handle_ma3 = 0

def OnInit():
    global handle_ma1, handle_ma2, handle_ma3, period_ema1, period_ema2, period_ema3, period_esz1, period_esz2, period_esz3, period_max, stop_factor1, stop_factor2, stop_factor3
    period_esz1 = (1 if (InpPeriod1 < 1) else InpPeriod1)
    period_esz2 = (1 if (InpPeriod2 < 1) else InpPeriod2)
    period_esz3 = (1 if (InpPeriod3 < 1) else InpPeriod3)
    period_ema1 = (1 if (InpPeriodEMA1 < 1) else InpPeriodEMA1)
    period_ema2 = (1 if (InpPeriodEMA2 < 1) else InpPeriodEMA2)
    period_ema3 = (1 if (InpPeriodEMA3 < 1) else InpPeriodEMA3)
    stop_factor1 = (1 if (InpStopFactor1 < 1) else InpStopFactor1)
    stop_factor2 = (1 if (InpStopFactor2 < 1) else InpStopFactor2)
    stop_factor3 = (1 if (InpStopFactor3 < 1) else InpStopFactor3)
    period_max = fmax(period_esz1, fmax(period_esz2, period_esz3))
    SetIndexBuffer(0, BufferESZ1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferESZ2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferESZ3, INDICATOR_DATA)
    SetIndexBuffer(3, BufferEMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferEMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferEMA3, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, "Elder's Triple Safe Zone")
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferESZ1, True)
    ArraySetAsSeries(BufferESZ2, True)
    ArraySetAsSeries(BufferESZ3, True)
    ArraySetAsSeries(BufferEMA1, True)
    ArraySetAsSeries(BufferEMA2, True)
    ArraySetAsSeries(BufferEMA3, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, period_ema1, 0, MODE_EMA, PRICE_CLOSE)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(', _str(period_ema1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(None, PERIOD_CURRENT, period_ema2, 0, MODE_EMA, PRICE_CLOSE)
    if handle_ma2 == INVALID_HANDLE:
        Print('The iMA(', _str(period_ema2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma3 = iMA(None, PERIOD_CURRENT, period_ema3, 0, MODE_EMA, PRICE_CLOSE)
    if handle_ma3 == INVALID_HANDLE:
        Print('The iMA(', _str(period_ema3), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 3
        ArrayInitialize(BufferESZ1, EMPTY_VALUE)
        ArrayInitialize(BufferESZ2, EMPTY_VALUE)
        ArrayInitialize(BufferESZ3, EMPTY_VALUE)
        ArrayInitialize(BufferEMA1, 0)
        ArrayInitialize(BufferEMA2, 0)
        ArrayInitialize(BufferEMA3, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferEMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma2, 0, 0, count, BufferEMA2)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma3, 0, 0, count, BufferEMA3)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        CalculateESZ(i, period_esz1, stop_factor1, BufferESZ1, BufferEMA1, high, low, close)
        CalculateESZ(i, period_esz2, stop_factor2, BufferESZ2, BufferEMA2, high, low, close)
        CalculateESZ(i, period_esz3, stop_factor3, BufferESZ3, BufferEMA3, high, low, close)
    return rates_total

def CalculateESZ(shift, period, factor, esz, ema, high, low, close):
    PreSafeStop = esz[shift + 1]
    Pen = 0.0
    Counter = 0.0
    SafeStop = 0.0
    if ema[shift] > ema[shift + 1]:
        for j in range(0, period):
            if low[shift + j] < low[shift + j + 1]:
                Pen = low[shift + j + 1] - low[shift + j] + Pen
                Counter += 1
        if Counter > 0:
            SafeStop = close[shift] - (factor * _fdiv(Pen, Counter))
        else:
            SafeStop = close[shift] - (factor * Pen)
        if SafeStop < PreSafeStop and ema[shift + 1] > ema[shift + 2]:
            SafeStop = PreSafeStop
    elif ema[shift] < ema[shift + 1]:
        for j in range(0, period):
            if high[shift + j] > high[shift + j + 1]:
                Pen = high[shift + j] - high[shift + j + 1] + Pen
                Counter += 1
        if Counter > 0:
            SafeStop = close[shift] + (factor * _fdiv(Pen, Counter))
        else:
            SafeStop = close[shift] + (factor * Pen)
        if SafeStop > PreSafeStop and ema[shift + 1] < ema[shift + 2]:
            SafeStop = PreSafeStop
    PreSafeStop = SafeStop
    esz[shift] = SafeStop


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EldersSafeZoneTriple(_MQL5Indicator):
    name = 'Elders_Safe_Zone_Triple'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 10,  # First ESZ Period
        'InpStopFactor1': 3,  # First Stop factor
        'InpPeriodEMA1': 13,  # First EMA period
        'InpPeriod2': 20,  # Second ESZ Period
        'InpStopFactor2': 6,  # Second Stop factor
        'InpPeriodEMA2': 50,  # Second EMA period
        'InpPeriod3': 30,  # Third ESZ Period
        'InpStopFactor3': 10,  # Third Stop factor
        'InpPeriodEMA3': 100,  # Third EMA period
    }

