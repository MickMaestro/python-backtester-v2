"""DEROSC — converted from MQL5: MQL5 Indicators/DEROSC/DEROSC.mq5

Derivative Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 3329434, 255, 42495, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Derivative'}, 'levels': [], 'description': ['Derivative Oscillator'], 'name': 'DEROSC', 'source': 'MQL5 Indicators/DEROSC/DEROSC.mq5', 'folder': 'DEROSC', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpPeriodEMA1', 'py': 'InpPeriodEMA1', 'param': 'InpPeriodEMA1', 'type': 'uint', 'default': 5, 'label': 'First EMA period', 'sinput': False}, {'mql': 'InpPeriodEMA2', 'py': 'InpPeriodEMA2', 'param': 'InpPeriodEMA2', 'type': 'uint', 'default': 3, 'label': 'Second EMA period', 'sinput': False}, {'mql': 'InpPeriodSMA', 'py': 'InpPeriodSMA', 'param': 'InpPeriodSMA', 'type': 'uint', 'default': 9, 'label': 'SMA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 14)  # RSI period
InpPeriodEMA1 = _input('InpPeriodEMA1', 5)  # First EMA period
InpPeriodEMA2 = _input('InpPeriodEMA2', 3)  # Second EMA period
InpPeriodSMA = _input('InpPeriodSMA', 9)  # SMA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferDEROSC = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferEMA1 = Arr(0, 0.0)
BufferEMA2 = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
period_rsi = 0
period_ema1 = 0
period_ema2 = 0
period_sma = 0
handle_rsi = 0

def OnInit():
    global handle_rsi, period_ema1, period_ema2, period_rsi, period_sma
    period_rsi = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    period_ema1 = (2 if (InpPeriodEMA1 < 2) else InpPeriodEMA1)
    period_ema2 = (2 if (InpPeriodEMA2 < 2) else InpPeriodEMA2)
    period_sma = (2 if (InpPeriodSMA < 2) else InpPeriodSMA)
    SetIndexBuffer(0, BufferDEROSC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferEMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferEMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferRSI, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Derivative Oscillator (' + _str(period_rsi) + ',' + _str(period_ema1) + ',' + _str(period_ema2) + ',' + _str(period_sma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDEROSC, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferEMA1, True)
    ArraySetAsSeries(BufferEMA2, True)
    ArraySetAsSeries(BufferSMA, True)
    ArraySetAsSeries(BufferRSI, True)
    ResetLastError()
    handle_rsi = iRSI(None, PERIOD_CURRENT, period_rsi, InpAppliedPrice)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI(', _str(period_rsi), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_sma, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferDEROSC, EMPTY_VALUE)
        ArrayInitialize(BufferEMA1, 0)
        ArrayInitialize(BufferEMA2, 0)
        ArrayInitialize(BufferSMA, 0)
        ArrayInitialize(BufferRSI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
    if copied != count:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period_rsi, period_ema1, BufferRSI, BufferEMA1) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period_ema1, period_ema2, BufferEMA1, BufferEMA2) == 0:
        return 0
    if SimpleMAOnBuffer(rates_total, prev_calculated, period_ema2, period_sma, BufferEMA2, BufferSMA) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferDEROSC[i] = _fdiv(BufferEMA2[i] - BufferSMA[i], Point())
        BufferColors[i] = ((0 if (BufferDEROSC[i] > BufferDEROSC[i + 1]) else 1) if (BufferDEROSC[i] > 0) else (2 if (BufferDEROSC[i] < BufferDEROSC[i + 1]) else 3) if (BufferDEROSC[i] < 0) else 4)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DEROSC(_MQL5Indicator):
    name = 'DEROSC'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 14,  # RSI period
        'InpPeriodEMA1': 5,  # First EMA period
        'InpPeriodEMA2': 3,  # Second EMA period
        'InpPeriodSMA': 9,  # SMA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

