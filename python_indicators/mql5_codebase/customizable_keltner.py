"""Customizable Keltner — converted from MQL5: MQL5 Indicators/Modified Keltner Channel/Customizable Keltner.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [32768]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper', 2: 'Middle', 3: 'Lower'}, 'levels': [], 'description': [], 'name': 'Customizable Keltner', 'source': 'MQL5 Indicators/Modified Keltner Channel/Customizable Keltner.mq5', 'folder': 'Modified Keltner Channel', 'inputs': [{'mql': 'InpSmoothCenter', 'py': 'InpSmoothCenter', 'param': 'InpSmoothCenter', 'type': 'int', 'default': 50, 'label': 'Number of the periods to smooth the center line', 'sinput': False}, {'mql': 'InpSmoothDeviation', 'py': 'InpSmoothDeviation', 'param': 'InpSmoothDeviation', 'type': 'int', 'default': 50, 'label': 'Number of periods to smooth deviation', 'sinput': False}, {'mql': 'InpF', 'py': 'InpF', 'param': 'InpF', 'type': 'double', 'default': 1.0, 'label': 'Factor which is used to apply the deviation', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'The center line applied price:', 'sinput': False}, {'mql': 'InpMethodSmoothing', 'py': 'InpMethodSmoothing', 'param': 'InpMethodSmoothing', 'type': 'int', 'default': 0, 'label': 'The center line smoothing method', 'sinput': False}, {'mql': 'InpMethodVariation', 'py': 'InpMethodVariation', 'param': 'InpMethodVariation', 'type': 'int', 'default': 0, 'label': 'Variation Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_METHOD_VARIATION
METHOD_HL = 0
METHOD_ATR = 1
_enum('ENUM_METHOD_VARIATION', {0: 'METHOD_HL', 1: 'METHOD_ATR'})

# ---- inputs and global variables
InpSmoothCenter = _input('InpSmoothCenter', 50)  # Number of the periods to smooth the center line
InpSmoothDeviation = _input('InpSmoothDeviation', 50)  # Number of periods to smooth deviation
InpF = _input('InpF', 1.0)  # Factor which is used to apply the deviation
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # The center line applied price:
InpMethodSmoothing = _input('InpMethodSmoothing', MODE_SMA)  # The center line smoothing method
InpMethodVariation = _input('InpMethodVariation', METHOD_HL)  # Variation Method
BufferUpper = Arr(0, 0.0)
BufferMiddle = Arr(0, 0.0)
BufferLower = Arr(0, 0.0)
BufferVariation = Arr(0, 0.0)
handle_ma = 0
handle_atr = 0
period_center = 0
period_dev = 0

def OnInit():
    global handle_atr, handle_ma, period_center, period_dev
    SetIndexBuffer(0, BufferUpper, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMiddle, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLower, INDICATOR_DATA)
    SetIndexBuffer(3, BufferVariation, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Keltner with color zones')
    period_center = (1 if (InpSmoothCenter < 1) else InpSmoothCenter)
    period_dev = (1 if (InpSmoothDeviation < 1) else InpSmoothDeviation)
    ResetLastError()
    handle_ma = iMA(Symbol(), PERIOD_CURRENT, period_center, 0, InpMethodSmoothing, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA object was not created: Error ', GetLastError())
        return INIT_FAILED
    if InpMethodVariation == METHOD_ATR:
        ResetLastError()
        handle_atr = iATR(Symbol(), PERIOD_CURRENT, period_dev)
        if handle_atr == INVALID_HANDLE:
            Print('The iATR object was not created: Error ', GetLastError())
            return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(BufferLower, True)
    ArraySetAsSeries(BufferMiddle, True)
    ArraySetAsSeries(BufferUpper, True)
    ArraySetAsSeries(BufferVariation, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    copied_ma = 0
    copied_atr = 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferLower, EMPTY_VALUE)
        ArrayInitialize(BufferMiddle, EMPTY_VALUE)
        ArrayInitialize(BufferUpper, EMPTY_VALUE)
        ArrayInitialize(BufferVariation, EMPTY_VALUE)
        copied_ma = CopyBuffer(handle_ma, 0, 0, rates_total, BufferMiddle)
        if copied_ma != rates_total:
            return 0
        if InpMethodVariation == METHOD_ATR:
            copied_atr = CopyBuffer(handle_atr, 0, 0, rates_total, BufferVariation)
            if copied_atr != rates_total:
                return 0
        else:
            for i in range(limit, 0 - 1, -1):
                BufferVariation[i] = high[i] - low[i]
    copied = (rates_total if (limit > 1) else 1)
    copied_ma = CopyBuffer(handle_ma, 0, 0, copied, BufferMiddle)
    if copied_ma != copied:
        return 0
    if InpMethodVariation == METHOD_ATR:
        copied_atr = CopyBuffer(handle_atr, 0, 0, copied, BufferVariation)
        if copied_atr != copied:
            return 0
    else:
        for i in range(limit, 0 - 1, -1):
            BufferVariation[i] = high[i] - low[i]
    v = 0.0
    for i in range(limit, 0 - 1, -1):
        v = (BufferVariation[i] if (InpMethodVariation == METHOD_ATR) else iMAOnArray_u(BufferVariation, 0, period_dev, 0, InpMethodVariation, i))
        BufferUpper[i] = BufferMiddle[i] + (v * InpF)
        BufferLower[i] = BufferMiddle[i] - (v * InpF)
    return rates_total

def iMAOnArray_u(array, total, period, ma_shift, ma_method, shift):
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


class CustomizableKeltner(_MQL5Indicator):
    name = 'Customizable Keltner'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpSmoothCenter': 50,  # Number of the periods to smooth the center line
        'InpSmoothDeviation': 50,  # Number of periods to smooth deviation
        'InpF': 1.0,  # Factor which is used to apply the deviation
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # The center line applied price:
        'InpMethodSmoothing': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # The center line smoothing method
        'InpMethodVariation': _Choice({0: 'Smoothed H-L', 1: 'ATR as source'}, default=0),  # Variation Method
    }

