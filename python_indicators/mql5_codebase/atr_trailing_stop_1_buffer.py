"""ATR_Trailing_Stop_1_Buffer — converted from MQL5: MQL5 Indicators/ATR Trailing Stop with 1 Buffer only/ATR_Trailing_Stop_1_Buffer.mq5

Modified ATR Trailing Stop indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Level up'}, 'levels': [], 'description': ['Modified ATR Trailing Stop indicator'], 'name': 'ATR_Trailing_Stop_1_Buffer', 'source': 'MQL5 Indicators/ATR Trailing Stop with 1 Buffer only/ATR_Trailing_Stop_1_Buffer.mq5', 'folder': 'ATR Trailing Stop with 1 Buffer only', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 7, 'label': 'Period', 'sinput': False}, {'mql': 'InpCoeff', 'py': 'InpCoeff', 'param': 'InpCoeff', 'type': 'double', 'default': 2.0, 'label': 'Coefficient', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 7)  # Period
InpCoeff = _input('InpCoeff', 2.0)  # Coefficient
BufferMain = Arr(0, 0.0)
BufferHL = Arr(0, 0.0)
BufferDiff = Arr(0, 0.0)
BufferWMA = Arr(0, 0.0)
BufferTMP = Arr(0, 0.0)
period_ma = 0
K = 0.0

def OnInit():
    global K, period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    n1 = 2.0 * float(period_ma - 1)
    K = _fdiv(2.0, n1 + 1)
    SetIndexBuffer(0, BufferMain, INDICATOR_DATA)
    SetIndexBuffer(1, BufferHL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferDiff, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferWMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferTMP, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ModATRTS(' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMain, True)
    ArraySetAsSeries(BufferHL, True)
    ArraySetAsSeries(BufferDiff, True)
    ArraySetAsSeries(BufferWMA, True)
    ArraySetAsSeries(BufferTMP, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ma:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferMain, EMPTY_VALUE)
        ArrayInitialize(BufferHL, 0)
        ArrayInitialize(BufferDiff, 0)
        ArrayInitialize(BufferWMA, 0)
        ArrayInitialize(BufferTMP, 0)
    for i in range(limit, 0 - 1, -1):
        BufferHL[i] = high[i] - low[i]
        Href = 0.0
        Lref = 0.0
        SMA = MAOnArray(BufferHL, 0, period_ma, 0, MODE_SMA, i)
        HiLo = fmin(BufferHL[i], SMA)
        Href = ((high[i] - close[i + 1]) if (low[i] <= high[i + 1]) else ((BufferHL[i] - close[i + 1] + high[i + 1]) / 2))
        Lref = ((close[i + 1] - low[i]) if (high[i] >= low[i + 1]) else ((close[i + 1] - low[i + 1] + BufferHL[i]) / 2))
        BufferDiff[i] = fmax(HiLo, fmax(Href, Lref))
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - 2):
            BufferWMA[i] = MAOnArray(BufferDiff, 0, period_ma, 0, MODE_EMA, i)
        else:
            BufferWMA[i] = ((BufferDiff[i] - BufferWMA[i + 1]) * K) + BufferWMA[i + 1]
    for i in range(limit, 0 - 1, -1):
        loss = BufferWMA[i] * InpCoeff
        if close[i] > BufferTMP[i + 1] and close[i + 1] > BufferTMP[i + 1]:
            BufferTMP[i] = fmax(BufferTMP[i + 1], close[i] - loss)
            BufferMain[i] = BufferTMP[i]
        else:
            if close[i] < BufferTMP[i + 1] and close[i + 1] < BufferTMP[i + 1]:
                BufferTMP[i] = fmin(BufferTMP[i + 1], close[i] + loss)
                BufferMain[i] = BufferTMP[i]
            else:
                if close[i] > BufferTMP[i + 1]:
                    BufferTMP[i] = close[i] - loss
                    BufferMain[i] = BufferTMP[i]
                else:
                    BufferTMP[i] = close[i] + loss
                    BufferMain[i] = BufferTMP[i]
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


class ATRTrailingStop1Buffer(_MQL5Indicator):
    name = 'ATR_Trailing_Stop_1_Buffer'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 7,  # Period
        'InpCoeff': 2.0,  # Coefficient
    }

