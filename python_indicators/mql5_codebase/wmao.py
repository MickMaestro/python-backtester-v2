"""WMAO — converted from MQL5: MQL5 Indicators/WMAO/WMAO.mq5

Wilders Moving Average Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'WMAO'}, 'levels': [], 'description': ['Wilders Moving Average Oscillator'], 'name': 'WMAO', 'source': 'MQL5 Indicators/WMAO/WMAO.mq5', 'folder': 'WMAO', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 5, 'label': 'Fast WMA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 20, 'label': 'Slow WMA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'WMA applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 5)  # Fast WMA period
InpPeriodSlow = _input('InpPeriodSlow', 20)  # Slow WMA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # WMA applied price
BufferWMAO = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferWMAFast = Arr(0, 0.0)
BufferWMASlow = Arr(0, 0.0)
kf = 0.0
ks = 0.0
period_fast = 0
period_slow = 0
period_max = 0
handle_ma1 = 0
handle_fma = 0
handle_sma = 0

def OnInit():
    global handle_fma, handle_ma1, handle_sma, kf, ks, period_fast, period_max, period_slow
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = ((period_fast + 1) if (InpPeriodSlow == period_fast) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_max = fmax(period_fast, period_slow)
    kf = _fdiv(1.0, float(period_fast))
    ks = _fdiv(1.0, float(period_slow))
    SetIndexBuffer(0, BufferWMAO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferWMAFast, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferWMASlow, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Wilders OsWMA (' + _str(period_fast) + ',' + _str(period_slow) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferWMAO, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ArraySetAsSeries(BufferWMAFast, True)
    ArraySetAsSeries(BufferWMASlow, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_fma = iMA(None, PERIOD_CURRENT, period_fast, 0, MODE_SMA, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(period_fast), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_slow, 0, MODE_SMA, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(period_slow), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferWMAO, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
        ArrayInitialize(BufferWMAFast, 0)
        ArrayInitialize(BufferWMASlow, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - period_max - 2):
            BufferWMAFast[i] = BufferFMA[i]
            BufferWMASlow[i] = BufferSMA[i]
        else:
            BufferWMAFast[i] = ((BufferMA1[i] - BufferWMAFast[i + 1]) * kf) + BufferWMAFast[i + 1]
            BufferWMASlow[i] = ((BufferMA1[i] - BufferWMASlow[i + 1]) * ks) + BufferWMASlow[i + 1]
        BufferWMAO[i] = BufferWMAFast[i] - BufferWMASlow[i]
        BufferColors[i] = (0 if (BufferWMAO[i] > BufferWMAO[i + 1]) else 1 if (BufferWMAO[i] < BufferWMAO[i + 1]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WMAO(_MQL5Indicator):
    name = 'WMAO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 5,  # Fast WMA period
        'InpPeriodSlow': 20,  # Slow WMA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # WMA applied price
    }

