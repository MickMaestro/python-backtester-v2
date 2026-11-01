"""TMACD — converted from MQL5: MQL5 Indicators/TMACD/TMACD.mq5

Triangular Moving Average Convergence/Divergence oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [32768, 255, 11119017], 2: [16711680]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'TMACD', 2: 'Signal'}, 'levels': [], 'description': ['Triangular Moving Average Convergence/Divergence oscillator'], 'name': 'TMACD', 'source': 'MQL5 Indicators/TMACD/TMACD.mq5', 'folder': 'TMACD', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 7, 'label': 'Fast TriMA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 14, 'label': 'Slow TriMA period', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 5, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 7)  # Fast TriMA period
InpPeriodSlow = _input('InpPeriodSlow', 14)  # Slow TriMA period
InpPeriodSig = _input('InpPeriodSig', 5)  # Signal period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferTMACD = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
period_fma = 0
period_sma = 0
period_sig = 0
period_f = 0
period_s = 0
period_max = 0
handle_fma = 0
handle_sma = 0

def OnInit():
    global handle_fma, handle_sma, period_f, period_fma, period_max, period_s, period_sig, period_sma
    period_fma = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_sma = ((period_fma + 1) if (InpPeriodSlow == period_fma) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_sig = (1 if (InpPeriodSig < 1) else InpPeriodSig)
    period_f = _int(floor(_idiv(period_fma, 2))) + 1
    period_s = _int(floor(_idiv(period_sma, 2))) + 1
    period_max = fmax(period_f, period_s)
    SetIndexBuffer(0, BufferTMACD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(3, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TMACD (' + _str(period_fma) + ',' + _str(period_sma) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTMACD, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_f, 0, MODE_SMA, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(period_f), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_s, 0, MODE_SMA, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(period_s), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferTMACD, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferTMACD[i] = GetSMA(rates_total, i, period_f, BufferFMA) - GetSMA(rates_total, i, period_s, BufferSMA)
        BufferSignal[i] = GetSMA(rates_total, i, period_sig, BufferTMACD)
        BufferColors[i] = (0 if (BufferTMACD[i] > BufferTMACD[i + 1]) else 1 if (BufferTMACD[i] < BufferTMACD[i + 1]) else 2)
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TMACD(_MQL5Indicator):
    name = 'TMACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 7,  # Fast TriMA period
        'InpPeriodSlow': 14,  # Slow TriMA period
        'InpPeriodSig': 5,  # Signal period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

