"""Unsmoothed_RSI — converted from MQL5: MQL5 Indicators/Unsmoothed_RSI/Unsmoothed_RSI.mq5

Unsmoothed RSI
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'URSI'}, 'levels': [], 'description': ['Unsmoothed RSI'], 'name': 'Unsmoothed_RSI', 'source': 'MQL5 Indicators/Unsmoothed_RSI/Unsmoothed_RSI.mq5', 'folder': 'Unsmoothed_RSI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 70.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 30.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverbought = _input('InpOverbought', 70.0)  # Overbought
InpOversold = _input('InpOversold', 30.0)  # Oversold
BufferRSI = Arr(0, 0.0)
BufferPos = Arr(0, 0.0)
BufferNeg = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_ma = 0
handle_ma = 0
overbought = 0.0
oversold = 0.0

def OnInit():
    global handle_ma, overbought, oversold, period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    oversold = (0 if (InpOversold < 0) else 99 if (InpOversold > 99) else InpOversold)
    overbought = (100 if (InpOverbought > 100) else 1 if (InpOverbought < 1) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 1
    if oversold >= overbought:
        oversold = overbought - 1
    SetIndexBuffer(0, BufferRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferPos, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferNeg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'URSI(' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferPos, True)
    ArraySetAsSeries(BufferNeg, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ma:
        return 0
    limit = rates_total - prev_calculated
    limit1 = limit
    if limit > 1:
        limit = rates_total - 1
        limit1 = limit - 1
        ArrayInitialize(BufferRSI, EMPTY_VALUE)
        ArrayInitialize(BufferPos, 0)
        ArrayInitialize(BufferNeg, 0)
        ArrayInitialize(BufferMA, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit1, 0 - 1, -1):
        Diff = BufferMA[i] - BufferMA[i + 1]
        if Diff > 0:
            BufferPos[i] = Diff
            BufferNeg[i] = 0.0
        else:
            BufferPos[i] = 0.0
            BufferNeg[i] = -Diff
    for i in range(limit, 0 - 1, -1):
        P = MAOnArray(BufferPos, 0, period_ma, 0, MODE_SMA, i)
        N = MAOnArray(BufferNeg, 0, period_ma, 0, MODE_SMA, i)
        BufferRSI[i] = (0 if (N == 0) else (100 - _fdiv(100, 1 + _fdiv(P, N))))
    return rates_total

def MAOnArray(array, total, period, ma_shift, ma_method, shift):
    buf = Arr(0, 0.0)
    arr = Arr(0, 0.0)
    if total == 0:
        total = ArraySize(array)
    if total > 0 and total <= period:
        return 0.0
    if shift > (total - period - ma_shift):
        return 0.0
    _sw1 = ma_method
    if _sw1 == MODE_SMA:
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
    elif _sw1 == MODE_EMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        pr = _fdiv(2.0, period + 1)
        pos = total - 2
        while pos >= 0:
            if pos == (total - 2):
                buf[pos + 1] = array[pos + 1]
            buf[pos] = (array[pos] * pr) + (buf[pos + 1] * (1 - pr))
            pos -= 1
        return buf[shift + ma_shift]
    elif _sw1 == MODE_SMMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        i = 0
        k = 0
        pos = 0
        pos = total - period
        while pos >= 0:
            if pos == (total - period):
                i = 0
                k = pos
                while i < period:
                    sum_ += array[k]
                    buf[k] = 0.0
                    i += 1
                    k += 1
            else:
                sum_ = (buf[pos + 1] * (period - 1)) + array[pos]
            buf[pos] = _fdiv(sum_, period)
            pos -= 1
        return buf[shift + ma_shift]
    elif _sw1 == MODE_LWMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        lsum = 0.0
        price = 0.0
        i = 0
        weight = 0
        pos = total - 1
        i = 1
        while i <= period:
            price = array[pos]
            sum_ += price * i
            lsum += price
            weight += i
            i += 1
            pos -= 1
        pos += 1
        i = pos + period
        while pos >= 0:
            buf[pos] = _fdiv(sum_, weight)
            if pos == 0:
                break
            pos -= 1
            i -= 1
            price = array[pos]
            sum_ = sum_ - lsum + (price * period)
            lsum -= array[i]
            lsum += price
        return buf[shift + ma_shift]
    else:
        return 0.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UnsmoothedRSI(_MQL5Indicator):
    name = 'Unsmoothed_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 70.0,  # Overbought
        'InpOversold': 30.0,  # Oversold
    }

