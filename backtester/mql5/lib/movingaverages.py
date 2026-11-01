"""MovingAverages.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


def SimpleMA(position, period, price):
    result = 0.0
    if period > 0 and period <= (position + 1):
        for i in range(0, period):
            result += price[position - i]
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

def LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, begin, period, price, buffer, weight_sum):
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
        weight_sum.v = wsum
    else:
        start_position = prev_calculated - 1
    for i in range(start_position, rates_total):
        sum_ = 0.0
        for j in range(0, period):
            sum_ += (period - j) * price[i - j]
        buffer[i] = _fdiv(sum_, weight_sum.v)
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

__all__ = ['SimpleMA', 'ExponentialMA', 'SmoothedMA', 'LinearWeightedMA', 'SimpleMAOnBuffer', 'ExponentialMAOnBuffer', 'LinearWeightedMAOnBuffer_1', 'LinearWeightedMAOnBuffer_2', 'SmoothedMAOnBuffer']
