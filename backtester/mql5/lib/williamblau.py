"""williamblau.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


def ExponentialMAOnBufferWB(rates_total, prev_calculated, begin, period, price, buffer):
    i = 0
    limit = 0
    if period < 1 or (rates_total - begin) < period:
        return 0
    dSmoothFactor = _fdiv(2.0, 1.0 + period)
    as_series_price = ArrayGetAsSeries(price)
    as_series_buffer = ArrayGetAsSeries(buffer)
    if as_series_price:
        ArraySetAsSeries(price, False)
    if as_series_buffer:
        ArraySetAsSeries(buffer, False)
    if prev_calculated == 0:
        limit = period + begin
        i = 0
        for i in range(i, begin):
            buffer[i] = 0.0
        else:
            i = _range_end(i, begin, 1)
        buffer[begin] = price[begin]
        i = begin + 1
        for i in range(i, limit):
            buffer[i] = (price[i] * dSmoothFactor) + (buffer[i - 1] * (1.0 - dSmoothFactor))
        else:
            i = _range_end(i, limit, 1)
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        buffer[i] = (price[i] * dSmoothFactor) + (buffer[i - 1] * (1.0 - dSmoothFactor))
    else:
        i = _range_end(i, rates_total, 1)
    if as_series_price:
        ArraySetAsSeries(price, True)
    if as_series_buffer:
        ArraySetAsSeries(buffer, True)
    return rates_total

def PriceName(applied_price):
    name = ""
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        name = 'close'
    elif _sw1 == PRICE_OPEN:
        name = 'open'
    elif _sw1 == PRICE_HIGH:
        name = 'high'
    elif _sw1 == PRICE_LOW:
        name = 'low'
    elif _sw1 == PRICE_MEDIAN:
        name = 'median'
    elif _sw1 == PRICE_TYPICAL:
        name = 'typical'
    elif _sw1 == PRICE_WEIGHTED:
        name = 'weighted'
    else:
        name = ''
    return name

def CalculatePriceBuffer(applied_price, rates_total, prev_calculated, Open, High, Low, Close, Price):
    i = 0
    pos = 0
    if prev_calculated == 0:
        pos = 0
    else:
        pos = prev_calculated - 1
    i = pos
    for i in range(i, rates_total):
        _sw2 = applied_price
        if _sw2 == PRICE_CLOSE:
            Price[i] = Close[i]
        elif _sw2 == PRICE_OPEN:
            Price[i] = Open[i]
        elif _sw2 == PRICE_HIGH:
            Price[i] = High[i]
        elif _sw2 == PRICE_LOW:
            Price[i] = Low[i]
        elif _sw2 == PRICE_MEDIAN:
            Price[i] = (High[i] + Low[i]) / 2.0
        elif _sw2 == PRICE_TYPICAL:
            Price[i] = (High[i] + Low[i] + Close[i]) / 3.0
        elif _sw2 == PRICE_WEIGHTED:
            Price[i] = (High[i] + Low[i] + Close[i] + Close[i]) / 4.0
        else:
            Price[i] = 0.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

__all__ = ['ExponentialMAOnBufferWB', 'PriceName', 'CalculatePriceBuffer']
