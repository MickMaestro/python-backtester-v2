"""SSS — converted from MQL5: MQL5 Indicators/SSS/SSS.mq5

Special Slow Stochastic
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [11186720], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Main', 2: 'Signal', 3: 'SSS'}, 'levels': [], 'description': ['Special Slow Stochastic'], 'name': 'SSS', 'source': 'MQL5 Indicators/SSS/SSS.mq5', 'folder': 'SSS', 'inputs': [{'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 5, 'label': '%K period', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 3, 'label': '%D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'InpPeriodDS', 'py': 'InpPeriodDS', 'param': 'InpPeriodDS', 'type': 'uint', 'default': 3, 'label': 'Period Special Slow', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodK = _input('InpPeriodK', 5)  # %K period
InpPeriodD = _input('InpPeriodD', 3)  # %D period
InpSlowing = _input('InpSlowing', 3)  # Slowing
InpPeriodDS = _input('InpPeriodDS', 3)  # Period Special Slow
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferMAIN = Arr(0, 0.0)
BufferSIG = Arr(0, 0.0)
BufferDS = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_k = 0
slowing = 0
period_d = 0
period_ds = 0
handle_sto = 0

def OnInit():
    global handle_sto, overbought, oversold, period_d, period_ds, period_k, slowing
    period_k = (1 if (InpPeriodK < 1) else InpPeriodK)
    slowing = (1 if (InpSlowing < 1) else InpSlowing)
    period_d = (1 if (InpPeriodD < 1) else InpPeriodD)
    period_ds = (1 if (InpPeriodDS < 1) else InpPeriodDS)
    oversold = (0 if (InpOversold < 0) else 99.9 if (InpOversold > 99.9) else InpOversold)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferMAIN, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSIG, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDS, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Sto(' + _str(period_k) + ',' + _str(slowing) + ',' + _str(period_d) + ',' + _str(period_ds) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    ArraySetAsSeries(BufferMAIN, True)
    ArraySetAsSeries(BufferSIG, True)
    ArraySetAsSeries(BufferDS, True)
    ResetLastError()
    handle_sto = iStochastic(None, PERIOD_CURRENT, period_k, period_d, slowing, MODE_SMA, STO_LOWHIGH)
    if handle_sto == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k), ',', _str(period_d), ',', _str(slowing), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ds:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferMAIN, EMPTY_VALUE)
        ArrayInitialize(BufferSIG, EMPTY_VALUE)
        ArrayInitialize(BufferDS, EMPTY_VALUE)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_sto, MAIN_LINE, 0, count, BufferMAIN)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto, SIGNAL_LINE, 0, count, BufferSIG)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferDS[i] = MAOnArray(BufferSIG, 0, period_ds, 0, MODE_SMA, i)
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


class SSS(_MQL5Indicator):
    name = 'SSS'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodK': 5,  # %K period
        'InpPeriodD': 3,  # %D period
        'InpSlowing': 3,  # Slowing
        'InpPeriodDS': 3,  # Period Special Slow
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
    }

