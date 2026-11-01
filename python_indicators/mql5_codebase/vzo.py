"""VZO — converted from MQL5: MQL5 Indicators/VZO/VZO.mq5

Volume Zone Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [10526303]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'VZO'}, 'levels': [], 'description': ['Volume Zone Oscillator'], 'name': 'VZO', 'source': 'MQL5 Indicators/VZO/VZO.mq5', 'folder': 'VZO', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 6, 'label': 'Period', 'sinput': False}, {'mql': 'InpUpper', 'py': 'InpUpper', 'param': 'InpUpper', 'type': 'double', 'default': 60.0, 'label': 'Extreme overbought', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 40.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -40.0, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpLower', 'py': 'InpLower', 'param': 'InpLower', 'type': 'double', 'default': -60.0, 'label': 'Extreme oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 6)  # Period
InpUpper = _input('InpUpper', 60.0)  # Extreme overbought
InpOverbought = _input('InpOverbought', 40.0)  # Overbought
InpOversold = _input('InpOversold', -40.0)  # Oversold
InpLower = _input('InpLower', -60.0)  # Extreme oversold
BufferVZO = Arr(0, 0.0)
BufferAvgVP = Arr(0, 0.0)
BufferAvgVol = Arr(0, 0.0)
BufferVP = Arr(0, 0.0)
BufferVOL = Arr(0, 0.0)
upper = 0.0
overbought = 0.0
oversold = 0.0
lower = 0.0
period_vzo = 0

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

def ExponentialMA_1(position, period, prev_value, price):
    result = 0.0
    if period > 0:
        pr = _fdiv(2.0, period + 1.0)
        result = (price[position] * pr) + (prev_value * (1 - pr))
    return result

def ExponentialMA_2(rates_total, period, index, price):
    global _s_ExponentialMA_prev_value
    result = 0.0
    if period < 1 or index > (rates_total - period - 1):
        return 0.0
    pr = _fdiv(2.0, period + 1.0)
    if index == (rates_total - period - 1) or _s_ExponentialMA_prev_value == 0:
        result = SimpleMA_2(rates_total, period, index, price)
        _s_ExponentialMA_prev_value = result
    else:
        result = _s_ExponentialMA_prev_value + (pr * (price[index] - _s_ExponentialMA_prev_value))
        if index != 0:
            _s_ExponentialMA_prev_value = result
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

def OnInit():
    global lower, overbought, oversold, period_vzo, upper
    period_vzo = (1 if (InpPeriod < 1) else InpPeriod)
    overbought = (0.1 if (fabs(InpOverbought) < 0.1) else 99.9 if (InpOverbought > 99.9) else fabs(InpOverbought))
    oversold = (-0.1 if ((-fabs(InpOversold)) > -0.1) else -99.9 if ((-fabs(InpOversold)) < -99.9) else (-fabs(InpOversold)))
    upper = ((overbought + 0.1) if (fabs(InpUpper) <= overbought) else 100.0 if (InpUpper > 100.0) else fabs(InpUpper))
    lower = ((oversold - 0.1) if ((-fabs(InpLower)) >= oversold) else -100.0 if ((-fabs(InpLower)) < -100.0) else (-fabs(InpLower)))
    SetIndexBuffer(0, BufferVZO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferAvgVP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferAvgVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferVP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferVOL, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VZO (' + _str(period_vzo) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, upper)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, lower)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Extreme overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Oversold')
    IndicatorSetString(INDICATOR_LEVELTEXT, 3, 'Extreme oversold')
    ArraySetAsSeries(BufferVZO, True)
    ArraySetAsSeries(BufferAvgVP, True)
    ArraySetAsSeries(BufferAvgVol, True)
    ArraySetAsSeries(BufferVP, True)
    ArraySetAsSeries(BufferVOL, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_vzo, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferVZO, EMPTY_VALUE)
        ArrayInitialize(BufferAvgVP, 0)
        ArrayInitialize(BufferAvgVol, 0)
        ArrayInitialize(BufferVP, 0)
        ArrayInitialize(BufferVOL, 0)
    for i in range(limit, 0 - 1, -1):
        BufferVOL[i] = float(tick_volume[i])
        BufferVP[i] = float((tick_volume[i] if (close[i] > close[i + 1]) else (-tick_volume[i])))
        BufferAvgVP[i] = ExponentialMA_2(rates_total, period_vzo, i, BufferVP)
    for i in range(limit, 0 - 1, -1):
        BufferAvgVol[i] = ExponentialMA_2(rates_total, period_vzo, i, BufferVOL)
        BufferVZO[i] = ((_fdiv(BufferAvgVP[i], BufferAvgVol[i]) * 100.0) if (BufferAvgVol[i] != 0) else 0)
    return rates_total

# ---- static local variables
_s_ExponentialMA_prev_value = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VZO(_MQL5Indicator):
    name = 'VZO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 6,  # Period
        'InpUpper': 60.0,  # Extreme overbought
        'InpOverbought': 40.0,  # Overbought
        'InpOversold': -40.0,  # Oversold
        'InpLower': -60.0,  # Extreme oversold
    }

