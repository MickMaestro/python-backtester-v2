"""LR_MACD — converted from MQL5: MQL5 Indicators/LR_MACD/LR_MACD.mq5

Linear regression MACD
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [255], 2: [16711680], 3: [3329330, 255]}, 'widths': {1: 1, 2: 1, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'MACD', 2: 'SIG', 3: 'HIST'}, 'levels': [], 'description': ['Linear regression MACD'], 'name': 'LR_MACD', 'source': 'MQL5 Indicators/LR_MACD/LR_MACD.mq5', 'folder': 'LR_MACD', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 12, 'label': 'Fast LSMA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 26, 'label': 'Slow LSMA period', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpMethodSig', 'py': 'InpMethodSig', 'param': 'InpMethodSig', 'type': 'int', 'default': 1, 'label': 'Signal method', 'sinput': False}, {'mql': 'InpPriceSig', 'py': 'InpPriceSig', 'param': 'InpPriceSig', 'type': 'int', 'default': 1, 'label': 'Signal applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 12)  # Fast LSMA period
InpPeriodSlow = _input('InpPeriodSlow', 26)  # Slow LSMA period
InpPeriodSig = _input('InpPeriodSig', 9)  # Signal period
InpMethodSig = _input('InpMethodSig', MODE_EMA)  # Signal method
InpPriceSig = _input('InpPriceSig', PRICE_CLOSE)  # Signal applied price
BufferMACD = Arr(0, 0.0)
BufferSIG = Arr(0, 0.0)
BufferHIST = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMAF = Arr(0, 0.0)
BufferMAS = Arr(0, 0.0)
period_fast = 0
period_slow = 0
period_sig = 0
handle_maf = 0
handle_mas = 0

def OnInit():
    global handle_maf, handle_mas, period_fast, period_sig, period_slow
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = (1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_sig = (1 if (InpPeriodSig < 1) else InpPeriodSig)
    SetIndexBuffer(0, BufferMACD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSIG, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHIST, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferMAF, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMAS, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'LRMACD(' + _str(period_fast) + ',' + _str(period_slow) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferSIG, True)
    ArraySetAsSeries(BufferHIST, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMAF, True)
    ArraySetAsSeries(BufferMAS, True)
    ResetLastError()
    handle_maf = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_CLOSE)
    if handle_maf == INVALID_HANDLE:
        Print('The Fast iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_mas = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_CLOSE)
    if handle_mas == INVALID_HANDLE:
        Print('The Slow iMA(1) by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = fmax(period_fast, period_slow)
    if rates_total < max_:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - max_ - 2
        ArrayInitialize(BufferMACD, EMPTY_VALUE)
        ArrayInitialize(BufferSIG, EMPTY_VALUE)
        ArrayInitialize(BufferHIST, EMPTY_VALUE)
        ArrayInitialize(BufferMAF, EMPTY_VALUE)
        ArrayInitialize(BufferMAS, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_maf, 0, 0, count, BufferMAF)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mas, 0, 0, count, BufferMAS)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        xF = 0.0
        x2F = 0.0
        xS = 0.0
        x2S = 0.0
        yF = 0.0
        xyF = 0.0
        yS = 0.0
        xyS = 0.0
        for jf in range(0, period_fast):
            yF += BufferMAF[i + jf]
            xyF += BufferMAF[i + jf] * jf
            xF += jf
            x2F += jf * jf
        for js in range(0, period_slow):
            yS += BufferMAS[i + js]
            xyS += BufferMAS[i + js] * js
            xS += js
            x2S += js * js
        tempF = (period_fast * x2F) - (xF * xF)
        mF = _fdiv((period_fast * xyF) - (xF * yF), (tempF if (tempF != 0) else DBL_MIN))
        yintF = _fdiv(yF + (mF * xF), period_fast)
        tempS = (period_slow * x2S) - (xS * xS)
        mS = _fdiv((period_slow * xyS) - (xS * yS), (tempS if (tempS != 0) else DBL_MIN))
        yintS = _fdiv(yS + (mS * xS), period_slow)
        BufferMAF[i] = yintF - (mF * period_fast)
        BufferMAS[i] = yintS - (mS * period_slow)
        BufferMACD[i] = BufferMAF[i] - BufferMAS[i]
    for i in range(limit, 0 - 1, -1):
        BufferSIG[i] = MAOnArray(BufferMACD, 0, period_sig, 0, InpMethodSig, i)
        BufferHIST[i] = BufferMACD[i] - BufferSIG[i]
        BufferColors[i] = (0 if (BufferHIST[i] > BufferHIST[i + 1]) else 1)
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


class LRMACD(_MQL5Indicator):
    name = 'LR_MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 12,  # Fast LSMA period
        'InpPeriodSlow': 26,  # Slow LSMA period
        'InpPeriodSig': 9,  # Signal period
        'InpMethodSig': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Signal method
        'InpPriceSig': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Signal applied price
    }

