"""FanCCI2 — converted from MQL5: MQL5 Indicators/FanCCI2/FanCCI2.mq5

Fan CCI with Average line indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [32768, 255, 11119017], 2: [16711680]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'FanCCI Hist', 2: 'FanCCI Avg'}, 'levels': [], 'description': ['Fan CCI with Average line indicator'], 'name': 'FanCCI2', 'source': 'MQL5 Indicators/FanCCI2/FanCCI2.mq5', 'folder': 'FanCCI2', 'inputs': [{'mql': 'InpPeriodFirst', 'py': 'InpPeriodFirst', 'param': 'InpPeriodFirst', 'type': 'uint', 'default': 5, 'label': 'First CCI period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 6, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpCountCCI', 'py': 'InpCountCCI', 'param': 'InpCountCCI', 'type': 'uint', 'default': 10, 'label': 'CCI count', 'sinput': False}, {'mql': 'InpModeInc', 'py': 'InpModeInc', 'param': 'InpModeInc', 'type': 'int', 'default': 0, 'label': 'Incremental method', 'sinput': False}, {'mql': 'InpCoeff', 'py': 'InpCoeff', 'param': 'InpCoeff', 'type': 'uint', 'default': 2, 'label': 'Coefficient of increment', 'sinput': False}, {'mql': 'InpPeriodAvg', 'py': 'InpPeriodAvg', 'param': 'InpPeriodAvg', 'type': 'uint', 'default': 10, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpMethodAvg', 'py': 'InpMethodAvg', 'param': 'InpMethodAvg', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MODE_INC
MODE_ADD = 0
MODE_MLT = 1
_enum('ENUM_MODE_INC', {0: 'MODE_ADD', 1: 'MODE_MLT'})

# ---- inputs and global variables
InpPeriodFirst = _input('InpPeriodFirst', 5)  # First CCI period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_TYPICAL)  # Applied price
InpCountCCI = _input('InpCountCCI', 10)  # CCI count
InpModeInc = _input('InpModeInc', MODE_ADD)  # Incremental method
InpCoeff = _input('InpCoeff', 2)  # Coefficient of increment
InpPeriodAvg = _input('InpPeriodAvg', 10)  # Smoothing period
InpMethodAvg = _input('InpMethodAvg', MODE_SMA)  # Smoothing method
BufferHist = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferAvg = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
period_first = 0
period_sm = 0
cnt = 0
coeff = 0
handle_ma = 0
weight_sum = 0

def SimpleMA_1(position, period, price):
    result = 0.0
    if period > 0 and period <= (position + 1):
        for i in range(0, period):
            result += price[position - i]
        result = _fdiv(result, period)
    return result

def SimpleMA_2(rates_total, period, index, price):
    result = 0.0
    if period < 1 or index > (rates_total - period - 1):
        return 0.0
    for i in range(0, period):
        result = result + price[index + i]
    result = _fdiv(result, period)
    return result

def ExponentialMA(position, period, prev_value, price):
    result = 0.0
    if period > 0:
        pr = _fdiv(2.0, period + 1.0)
        result = (price[position] * pr) + (prev_value * (1 - pr))
    return result

def SmoothedMA(position, period, prev_value, price):
    result = 0.0
    if period > 0 and period <= (position + 1):
        if position == (period - 1):
            for i in range(0, period):
                result += price[position - i]
            result = _fdiv(result, period)
        result = _fdiv((prev_value * (period - 1)) + price[position], period)
    return result

def LinearWeightedMA(position, period, price):
    result = 0.0
    if period > 0 and period <= (position + 1):
        sum_ = 0.0
        wsum = 0
        for i in range(period, 0, -1):
            wsum += i
            sum_ += price[position - i + 1] * (period - i + 1)
        result = _fdiv(sum_, wsum)
    return result

def SimpleMAOnBuffer(rates_total, prev_calculated, begin, period, price, buffer):
    if period <= 1 or period > (rates_total - begin):
        return 0
    as_series_price = ArrayGetAsSeries(price)
    as_series_buffer = ArrayGetAsSeries(buffer)
    ArraySetAsSeries(price, False)
    ArraySetAsSeries(buffer, False)
    start_position = 0
    if prev_calculated == 0:
        start_position = period + begin
        for i in range(0, start_position - 1):
            buffer[i] = 0.0
        first_value = 0.0
        for i in range(begin, start_position):
            first_value += price[i]
        buffer[start_position - 1] = _fdiv(first_value, period)
    else:
        start_position = prev_calculated - 1
    for i in range(start_position, rates_total):
        buffer[i] = buffer[i - 1] + _fdiv(price[i] - price[i - period], period)
    ArraySetAsSeries(price, as_series_price)
    ArraySetAsSeries(buffer, as_series_buffer)
    return rates_total

def ExponentialMAOnBuffer(rates_total, prev_calculated, begin, period, price, buffer):
    if period <= 1 or period > (rates_total - begin):
        return 0
    as_series_price = ArrayGetAsSeries(price)
    as_series_buffer = ArrayGetAsSeries(buffer)
    ArraySetAsSeries(price, False)
    ArraySetAsSeries(buffer, False)
    start_position = 0
    smooth_factor = _fdiv(2.0, 1.0 + period)
    if prev_calculated == 0:
        for i in range(0, begin):
            buffer[i] = 0.0
        start_position = period + begin
        buffer[begin] = price[begin]
        for i in range(begin + 1, start_position):
            buffer[i] = (price[i] * smooth_factor) + (buffer[i - 1] * (1.0 - smooth_factor))
    else:
        start_position = prev_calculated - 1
    for i in range(start_position, rates_total):
        buffer[i] = (price[i] * smooth_factor) + (buffer[i - 1] * (1.0 - smooth_factor))
    ArraySetAsSeries(price, as_series_price)
    ArraySetAsSeries(buffer, as_series_buffer)
    return rates_total

def LinearWeightedMAOnBuffer_1(rates_total, prev_calculated, begin, period, price, buffer):
    if period <= 1 or period > (rates_total - begin):
        return 0
    as_series_price = ArrayGetAsSeries(price)
    as_series_buffer = ArrayGetAsSeries(buffer)
    ArraySetAsSeries(price, False)
    ArraySetAsSeries(buffer, False)
    i = 0
    start_position = 0
    if prev_calculated <= (period + begin + 2):
        start_position = period + begin
        i = 0
        for i in range(i, start_position):
            buffer[i] = 0.0
        else:
            i = _range_end(i, start_position, 1)
    else:
        start_position = prev_calculated - 2
    sum_ = 0.0
    lsum = 0.0
    l = 0
    weight = 0
    i = start_position - period
    l = 1
    while i < start_position:
        sum_ += price[i] * l
        lsum += price[i]
        weight += l
        i += 1
        l += 1
    buffer[start_position - 1] = _fdiv(sum_, weight)
    i = start_position
    for i in range(i, rates_total):
        sum_ = sum_ - lsum + (price[i] * period)
        lsum = lsum - price[i - period] + price[i]
        buffer[i] = _fdiv(sum_, weight)
    else:
        i = _range_end(i, rates_total, 1)
    ArraySetAsSeries(price, as_series_price)
    ArraySetAsSeries(buffer, as_series_buffer)
    return rates_total

def LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, begin, period, price, buffer, weight_sum_):
    if period <= 1 or period > (rates_total - begin):
        return 0
    as_series_price = ArrayGetAsSeries(price)
    as_series_buffer = ArrayGetAsSeries(buffer)
    ArraySetAsSeries(price, False)
    ArraySetAsSeries(buffer, False)
    start_position = 0
    if prev_calculated == 0:
        start_position = period + begin
        for i in range(0, start_position):
            buffer[i] = 0.0
        first_value = 0.0
        wsum = 0
        i = begin
        k = 1
        while i < start_position:
            first_value += k * price[i]
            wsum += k
            i += 1
            k += 1
        buffer[start_position - 1] = _fdiv(first_value, wsum)
        weight_sum_.v = wsum
    else:
        start_position = prev_calculated - 1
    for i in range(start_position, rates_total):
        sum_ = 0.0
        for j in range(0, period):
            sum_ += (period - j) * price[i - j]
        buffer[i] = _fdiv(sum_, weight_sum_.v)
    ArraySetAsSeries(price, as_series_price)
    ArraySetAsSeries(buffer, as_series_buffer)
    return rates_total

def SmoothedMAOnBuffer(rates_total, prev_calculated, begin, period, price, buffer):
    if period <= 1 or period > (rates_total - begin):
        return 0
    as_series_price = ArrayGetAsSeries(price)
    as_series_buffer = ArrayGetAsSeries(buffer)
    ArraySetAsSeries(price, False)
    ArraySetAsSeries(buffer, False)
    start_position = 0
    if prev_calculated == 0:
        start_position = period + begin
        for i in range(0, start_position - 1):
            buffer[i] = 0.0
        first_value = 0.0
        for i in range(begin, start_position):
            first_value += price[i]
        buffer[start_position - 1] = _fdiv(first_value, period)
    else:
        start_position = prev_calculated - 1
    for i in range(start_position, rates_total):
        buffer[i] = _fdiv((buffer[i - 1] * (period - 1)) + price[i], period)
    ArraySetAsSeries(price, as_series_price)
    ArraySetAsSeries(buffer, as_series_buffer)
    return rates_total

def OnInit():
    global cnt, coeff, handle_ma, period_first, period_sm
    period_first = (1 if (InpPeriodFirst < 1) else InpPeriodFirst)
    period_sm = (2 if (InpPeriodAvg < 2) else InpPeriodAvg)
    cnt = (1 if (_int(InpCountCCI) < 1) else InpCountCCI)
    k = (1 if (InpModeInc == MODE_ADD) else 2)
    coeff = (k if (InpCoeff < k) else InpCoeff)
    SetIndexBuffer(0, BufferHist, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferAvg, INDICATOR_DATA)
    SetIndexBuffer(3, BufferPrice, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FanCCI (Periods from ' + _str(period_first) + ', step ' + _str(coeff) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    ArraySetAsSeries(BufferHist, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferAvg, True)
    ArraySetAsSeries(BufferPrice, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferHist, 0)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferAvg, 0)
        ArrayInitialize(BufferPrice, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferPrice)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        s = 0.0
        length = period_first
        j = 0
        while j < cnt:
            cci0 = GetCCI(rates_total, length, i, BufferPrice)
            cci1 = GetCCI(rates_total, length, i + 1, BufferPrice)
            if cci0 == 0 or cci1 == 0:
                j += 1
                continue
            s += (1 if (cci0 > cci1) else -1)
            if InpModeInc == MODE_ADD:
                length += coeff
            else:
                length *= coeff
            j += 1
        BufferHist[i] = _fdiv(s, cnt)
        BufferColors[i] = (0 if (s > 0) else 1 if (s < 0) else 2)
    _sw1 = InpMethodAvg
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferHist, BufferAvg) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferHist, BufferAvg) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm, BufferHist, BufferAvg, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferHist, BufferAvg) == 0:
            return 0
    return rates_total

def GetCCI(rates_total, period, index, price):
    sum_ = 0.0
    if period < 1 or index > (rates_total - period - 1):
        return 0.0
    dev = SimpleMA_2(rates_total, period, index, price)
    for j in range(0, period):
        sum_ += fabs(price[index + j] - dev)
    meandev = _fdiv(sum_, period)
    return (_fdiv(price[index] - dev, meandev * 0.015) if (meandev != 0) else 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FanCCI2(_MQL5Indicator):
    name = 'FanCCI2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFirst': 5,  # First CCI period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Applied price
        'InpCountCCI': 10,  # CCI count
        'InpModeInc': _Choice({0: 'Addition', 1: 'Multiplication'}, default=0),  # Incremental method
        'InpCoeff': 2,  # Coefficient of increment
        'InpPeriodAvg': 10,  # Smoothing period
        'InpMethodAvg': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
    }

