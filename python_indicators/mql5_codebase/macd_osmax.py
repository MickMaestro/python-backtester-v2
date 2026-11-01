"""MACD_Osmax — converted from MQL5: MQL5 Indicators/MACD_Osmax/MACD_Osmax.mq5

MACD OsmaX oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [16711680], 2: [255], 3: [16711680, 255, 8421504]}, 'widths': {1: 1, 2: 1, 3: 8}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'MACD', 2: 'Signal', 3: 'OsMA'}, 'levels': [], 'description': ['MACD OsmaX oscillator'], 'name': 'MACD_Osmax', 'source': 'MQL5 Indicators/MACD_Osmax/MACD_Osmax.mq5', 'folder': 'MACD_Osmax', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpOsmaX', 'py': 'InpOsmaX', 'param': 'InpOsmaX', 'type': 'uint', 'default': 2, 'label': 'OsmaX', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 12)  # Fast EMA period
InpPeriodSlow = _input('InpPeriodSlow', 26)  # Slow EMA period
InpPeriodSig = _input('InpPeriodSig', 9)  # Signal period
InpOsmaX = _input('InpOsmaX', 2)  # OsmaX
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferMACD = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferOsMA = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
period_fast = 0
period_slow = 0
period_sig = 0
osma = 0
handle_fma = 0
handle_sma = 0

def OnInit():
    global handle_fma, handle_sma, osma, period_fast, period_sig, period_slow
    period_fast = (3 if (InpPeriodFast < 3) else InpPeriodFast)
    period_slow = ((period_fast + 1) if (InpPeriodSlow == period_fast) else 3 if (InpPeriodSlow < 3) else InpPeriodSlow)
    period_sig = (2 if (InpPeriodSig < 2) else InpPeriodSig)
    osma = (1 if (InpOsmaX < 1) else InpOsmaX)
    SetIndexBuffer(0, BufferMACD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferOsMA, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD OsmaX (' + _str(period_fast) + ',' + _str(period_slow) + ',' + _str(period_sig) + ',' + _str(osma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferOsMA, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fast, 0, MODE_EMA, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA (', _str(period_fast), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_slow, 0, MODE_EMA, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA (', _str(period_slow), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_sig, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_sig - 2
        ArrayInitialize(BufferMACD, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferOsMA, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
    count = (rates_total if (limit > 0) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferMACD[i] = BufferFMA[i] - BufferSMA[i]
        BufferSignal[i] = EMA(rates_total, BufferMACD[i], BufferSignal[i + 1], period_sig, i)
        BufferOsMA[i] = (BufferMACD[i] - BufferSignal[i]) * osma
        BufferColors[i] = ((0 if (BufferOsMA[i] > BufferOsMA[i + 1]) else 2) if (BufferMACD[i] > BufferMACD[i + 1]) else (1 if (BufferOsMA[i] < BufferOsMA[i + 1]) else 2) if (BufferMACD[i] < BufferMACD[i + 1]) else 2)
    return rates_total

def EMA(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + (_fdiv(2.0, 1 + period) * (price - prev))))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDOsmax(_MQL5Indicator):
    name = 'MACD_Osmax'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 12,  # Fast EMA period
        'InpPeriodSlow': 26,  # Slow EMA period
        'InpPeriodSig': 9,  # Signal period
        'InpOsmaX': 2,  # OsmaX
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

