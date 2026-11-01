"""StochasticMomentum — converted from MQL5: MQL5 Indicators/StochasticMomentum/StochasticMomentum.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Main', 2: 'Signal'}, 'levels': [], 'description': [], 'name': 'StochasticMomentum', 'source': 'MQL5 Indicators/StochasticMomentum/StochasticMomentum.mq5', 'folder': 'StochasticMomentum', 'inputs': [{'mql': 'InpPeriodSTO', 'py': 'InpPeriodSTO', 'param': 'InpPeriodSTO', 'type': 'uint', 'default': 13, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodSIG', 'py': 'InpPeriodSIG', 'param': 'InpPeriodSIG', 'type': 'uint', 'default': 3, 'label': 'Signal', 'sinput': False}, {'mql': 'InpMethodSIG', 'py': 'InpMethodSIG', 'param': 'InpMethodSIG', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpSmooth', 'py': 'InpSmooth', 'param': 'InpSmooth', 'type': 'int', 'default': 1, 'label': 'Smooth', 'sinput': False}, {'mql': 'InpPeriodFirst', 'py': 'InpPeriodFirst', 'param': 'InpPeriodFirst', 'type': 'uint', 'default': 10, 'label': 'First MA period', 'sinput': False}, {'mql': 'InpMethodFirst', 'py': 'InpMethodFirst', 'param': 'InpMethodFirst', 'type': 'int', 'default': 0, 'label': 'First MA method', 'sinput': False}, {'mql': 'InpPeriodSecond', 'py': 'InpPeriodSecond', 'param': 'InpPeriodSecond', 'type': 'uint', 'default': 20, 'label': 'Second MA period', 'sinput': False}, {'mql': 'InpMethodSecond', 'py': 'InpMethodSecond', 'param': 'InpMethodSecond', 'type': 'int', 'default': 0, 'label': 'Second MA method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodSTO = _input('InpPeriodSTO', 13)  # Period
InpPeriodSIG = _input('InpPeriodSIG', 3)  # Signal
InpMethodSIG = _input('InpMethodSIG', MODE_SMA)  # Method
InpSmooth = _input('InpSmooth', INPUT_YES)  # Smooth
InpPeriodFirst = _input('InpPeriodFirst', 10)  # First MA period
InpMethodFirst = _input('InpMethodFirst', MODE_SMA)  # First MA method
InpPeriodSecond = _input('InpPeriodSecond', 20)  # Second MA period
InpMethodSecond = _input('InpMethodSecond', MODE_SMA)  # Second MA method
BufferSTO = Arr(0, 0.0)
BufferSIG = Arr(0, 0.0)
BufferRaw = Arr(0, 0.0)
BufferFirst = Arr(0, 0.0)
BufferSecond = Arr(0, 0.0)
period_sto = 0
period_sig = 0
period_1 = 0
period_2 = 0

def OnInit():
    global period_1, period_2, period_sig, period_sto
    period_sto = (1 if (InpPeriodSTO < 1) else InpPeriodSTO)
    period_sig = (1 if (InpPeriodSIG < 1) else InpPeriodSIG)
    period_1 = (1 if (InpPeriodFirst < 1) else InpPeriodFirst)
    period_2 = (1 if (InpPeriodSecond < 1) else InpPeriodSecond)
    SetIndexBuffer(0, BufferSTO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSIG, INDICATOR_DATA)
    SetIndexBuffer(2, BufferRaw, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferFirst, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSecond, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, ('A' if InpSmooth else '') + 'SM(' + _str(period_sto) + ',' + _str(period_sig) + ',' + _str(period_1) + ',' + _str(period_2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferSTO, True)
    ArraySetAsSeries(BufferSIG, True)
    ArraySetAsSeries(BufferRaw, True)
    ArraySetAsSeries(BufferFirst, True)
    ArraySetAsSeries(BufferSecond, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_sto:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    limit1 = limit
    limit2 = limit
    limit3 = limit
    limit4 = limit
    if limit > 1:
        limit = rates_total - 1
        limit1 = limit - period_sto
        limit2 = limit1 - period_1
        limit3 = limit2 - period_2
        limit4 = limit3 - period_sig
        ArrayInitialize(BufferSTO, 0)
        ArrayInitialize(BufferSIG, 0)
        ArrayInitialize(BufferRaw, 0)
        ArrayInitialize(BufferFirst, 0)
        ArrayInitialize(BufferSecond, 0)
    for i in range(limit1, 0 - 1, -1):
        h = Highest(period_sto, i)
        l = Lowest(period_sto, i)
        if h == WRONG_VALUE or l == WRONG_VALUE:
            return 0
        BufferRaw[i] = close[i] - (0.5 * (low[l] + high[h]))
    if InpSmooth:
        for i in range(limit2, 0 - 1, -1):
            BufferFirst[i] = MAOnArray(BufferRaw, 0, period_1, 0, InpMethodFirst, i)
        for i in range(limit3, 0 - 1, -1):
            BufferSecond[i] = MAOnArray(BufferFirst, 0, period_2, 0, InpMethodSecond, i)
            BufferSTO[i] = BufferSecond[i]
    else:
        for i in range(limit1, 0 - 1, -1):
            BufferSTO[i] = BufferRaw[i]
    for i in range(limit4, 0 - 1, -1):
        BufferSIG[i] = MAOnArray(BufferSTO, 0, period_sig, 0, InpMethodSIG, i)
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMinimum(array) + start
    return WRONG_VALUE

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


class StochasticMomentum(_MQL5Indicator):
    name = 'StochasticMomentum'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodSTO': 13,  # Period
        'InpPeriodSIG': 3,  # Signal
        'InpMethodSIG': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpSmooth': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Smooth
        'InpPeriodFirst': 10,  # First MA period
        'InpMethodFirst': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # First MA method
        'InpPeriodSecond': 20,  # Second MA period
        'InpMethodSecond': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Second MA method
    }

