"""VolatilityMA — converted from MQL5: MQL5 Indicators/VolatilityMA/VolatilityMA.mq5

Volatility moving average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11829830]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'VolMA'}, 'levels': [], 'description': ['Volatility moving average'], 'name': 'VolatilityMA', 'source': 'MQL5 Indicators/VolatilityMA/VolatilityMA.mq5', 'folder': 'VolatilityMA', 'inputs': [{'mql': 'InpLookBack', 'py': 'InpLookBack', 'param': 'InpLookBack', 'type': 'uint', 'default': 300, 'label': 'Period', 'sinput': False}, {'mql': 'InpBarrier', 'py': 'InpBarrier', 'param': 'InpBarrier', 'type': 'double', 'default': 2.0, 'label': 'Barrier', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpLookBack = _input('InpLookBack', 300)  # Period
InpBarrier = _input('InpBarrier', 2.0)  # Barrier
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferVolMA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
BufferRawAVG = Arr(0, 0.0)
BufferLength = Arr(0, 0.0)
barrier = 0.0
lookback = 0
handle_ma = 0

def OnInit():
    global barrier, handle_ma, lookback
    barrier = (0 if (InpBarrier < 0) else InpBarrier)
    lookback = (1 if (InpLookBack < 1) else InpLookBack)
    SetIndexBuffer(0, BufferVolMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferRawAVG, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferLength, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility moving average (' + _str(lookback) + ',' + DoubleToString(barrier, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferVolMA, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferRAW, True)
    ArraySetAsSeries(BufferRawAVG, True)
    ArraySetAsSeries(BufferLength, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < lookback:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - lookback - 2
        ArrayInitialize(BufferVolMA, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferRawAVG, 0)
        ArrayInitialize(BufferLength, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferRAW[i] = _fdiv(BufferMA[i] - BufferMA[i + 1], (BufferMA[i] if (BufferMA[i] != 0) else 1.0))
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, lookback, BufferRAW, BufferRawAVG)
    for i in range(limit, 0 - 1, -1):
        var = 0.0
        for j in range(0, lookback + 1):
            var += pow(BufferRAW[i + j] + BufferRawAVG[i], 2)
        sDev = sqrt(_fdiv(var, lookback))
        sDevNow = _fdiv(BufferRAW[i], BufferMA[i] * sDev)
        BufferLength[i] = (1 if (fabs(sDevNow) > barrier) else (BufferLength[i + 1] + 1))
        BufferVolMA[i] = SMAOnArray(BufferMA, 0, _int(BufferLength[i]), 0, i)
    return rates_total

def SMAOnArray(array, total, period, ma_shift, shift):
    buf = Arr(0, 0.0)
    arr = Arr(0, 0.0)
    if total == 0:
        total = ArraySize(array)
    if total > 0 and total <= period:
        return 0.0
    if shift > (total - period - ma_shift):
        return 0.0
    total = ArrayCopy(arr, array, 0, shift + ma_shift, period)
    if ArrayResize(buf, total) < 0:
        return 0.0
    sum_ = 0.0
    i = 0
    pos = total - 1
    i = 1
    while i < period:
        sum_ += arr[pos]
        i += 1
        pos -= 1
    while pos >= 0:
        sum_ += arr[pos]
        buf[pos] = _fdiv(sum_, period)
        sum_ -= arr[pos + period - 1]
        pos -= 1
    return buf[0]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityMA(_MQL5Indicator):
    name = 'VolatilityMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpLookBack': 300,  # Period
        'InpBarrier': 2.0,  # Barrier
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

