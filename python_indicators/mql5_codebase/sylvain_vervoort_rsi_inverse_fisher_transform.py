"""Sylvain_Vervoort_RSI_inverse_fisher_transform — converted from MQL5: MQL5 Indicators/Sylvain_Vervoort_RSI_inverse_fisher_transform/Sylvain_Vervoort_RSI_inverse_fisher_transform.mq5

Sylvain Vervoort RSI inverse fisher transform oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 18, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13458026]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SVRSI InvFT'}, 'levels': [], 'description': ['Sylvain Vervoort RSI inverse fisher transform oscillator'], 'name': 'Sylvain_Vervoort_RSI_inverse_fisher_transform', 'source': 'MQL5 Indicators/Sylvain_Vervoort_RSI_inverse_fisher_transform/Sylvain_Vervoort_RSI_inverse_fisher_transform.mq5', 'folder': 'Sylvain_Vervoort_RSI_inverse_fisher_transform', 'inputs': [{'mql': 'InpPeriodSVRMA', 'py': 'InpPeriodSVRMA', 'param': 'InpPeriodSVRMA', 'type': 'uint', 'default': 2, 'label': 'SVRMA period', 'sinput': False}, {'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 4, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 4, 'label': 'MA period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 88.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 12.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodSVRMA = _input('InpPeriodSVRMA', 2)  # SVRMA period
InpPeriodRSI = _input('InpPeriodRSI', 4)  # RSI period
InpPeriodMA = _input('InpPeriodMA', 4)  # MA period
InpOverbought = _input('InpOverbought', 88.0)  # Overbought
InpOversold = _input('InpOversold', 12.0)  # Oversold
BufferSVRSI = Arr(0, 0.0)
BufferLWMA1 = Arr(0, 0.0)
BufferLWMA2 = Arr(0, 0.0)
BufferLWMA3 = Arr(0, 0.0)
BufferLWMA4 = Arr(0, 0.0)
BufferLWMA5 = Arr(0, 0.0)
BufferLWMA6 = Arr(0, 0.0)
BufferLWMA7 = Arr(0, 0.0)
BufferLWMA8 = Arr(0, 0.0)
BufferLWMA9 = Arr(0, 0.0)
BufferLWMA10 = Arr(0, 0.0)
BufferRMA = Arr(0, 0.0)
BufferSmMA1 = Arr(0, 0.0)
BufferSmMA2 = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
BufferTmpRSI = Arr(0, 0.0)
BufferPosRSI = Arr(0, 0.0)
BufferNegRSI = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_svrma = 0
period_rsi = 0
period_ma = 0
period_max = 0
handle_ma = 0

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

def LinearWeightedMA_1(position, period, price):
    result = 0.0
    if period > 0 and period <= (position + 1):
        sum_ = 0.0
        wsum = 0
        for i in range(period, 0, -1):
            wsum += i
            sum_ += price[position - i + 1] * (period - i + 1)
        result = _fdiv(sum_, wsum)
    return result

def LinearWeightedMA_2(rates_total, period, index, price):
    result = 0.0
    count = 0.0
    total = 0.0
    k = 0.0
    wsum = 0
    if period < 1 or index > (rates_total - period - 1):
        return 0.0
    for j in range(index + period - 1, index - 1, -1):
        count += 1
        k += count
        total += price[j] * count
    result = _fdiv(total, k)
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
    global handle_ma, overbought, oversold, period_ma, period_max, period_rsi, period_svrma
    period_svrma = (1 if (InpPeriodSVRMA < 1) else InpPeriodSVRMA)
    period_rsi = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    period_ma = (2 if (InpPeriodMA < 2) else InpPeriodMA)
    period_max = period_svrma + (period_svrma * 9)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferSVRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferLWMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferLWMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferLWMA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferLWMA4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferLWMA5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferLWMA6, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferLWMA7, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferLWMA8, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferLWMA9, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferLWMA10, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferRMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferSmMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, BufferSmMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, BufferRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, BufferTmpRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, BufferPosRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(17, BufferNegRSI, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Sylvain Vervoort RSI inverse fisher transform (' + _str(period_svrma) + ',' + _str(period_rsi) + ',' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    ArraySetAsSeries(BufferSVRSI, True)
    ArraySetAsSeries(BufferLWMA1, True)
    ArraySetAsSeries(BufferLWMA2, True)
    ArraySetAsSeries(BufferLWMA3, True)
    ArraySetAsSeries(BufferLWMA4, True)
    ArraySetAsSeries(BufferLWMA5, True)
    ArraySetAsSeries(BufferLWMA6, True)
    ArraySetAsSeries(BufferLWMA7, True)
    ArraySetAsSeries(BufferLWMA8, True)
    ArraySetAsSeries(BufferLWMA9, True)
    ArraySetAsSeries(BufferLWMA10, True)
    ArraySetAsSeries(BufferRMA, True)
    ArraySetAsSeries(BufferSmMA1, True)
    ArraySetAsSeries(BufferSmMA2, True)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferTmpRSI, True)
    ArraySetAsSeries(BufferPosRSI, True)
    ArraySetAsSeries(BufferNegRSI, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_svrma, 0, MODE_SMA, PRICE_CLOSE)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_svrma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferSVRSI, EMPTY_VALUE)
        ArrayInitialize(BufferLWMA1, 0)
        ArrayInitialize(BufferLWMA2, 0)
        ArrayInitialize(BufferLWMA3, 0)
        ArrayInitialize(BufferLWMA4, 0)
        ArrayInitialize(BufferLWMA5, 0)
        ArrayInitialize(BufferLWMA6, 0)
        ArrayInitialize(BufferLWMA7, 0)
        ArrayInitialize(BufferLWMA8, 0)
        ArrayInitialize(BufferLWMA9, 0)
        ArrayInitialize(BufferLWMA10, 0)
        ArrayInitialize(BufferRMA, 0)
        ArrayInitialize(BufferSmMA1, 0)
        ArrayInitialize(BufferSmMA2, 0)
        ArrayInitialize(BufferRSI, 0)
        ArrayInitialize(BufferTmpRSI, 0)
        ArrayInitialize(BufferPosRSI, 0)
        ArrayInitialize(BufferNegRSI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferLWMA1)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferLWMA2[i] = LinearWeightedMA_2(rates_total, period_svrma, i, BufferLWMA1)
        BufferLWMA3[i] = LinearWeightedMA_2(rates_total, period_svrma, i, BufferLWMA2)
        BufferLWMA4[i] = LinearWeightedMA_2(rates_total, period_svrma, i, BufferLWMA3)
        BufferLWMA5[i] = LinearWeightedMA_2(rates_total, period_svrma, i, BufferLWMA4)
        BufferLWMA6[i] = LinearWeightedMA_2(rates_total, period_svrma, i, BufferLWMA5)
        BufferLWMA7[i] = LinearWeightedMA_2(rates_total, period_svrma, i, BufferLWMA6)
        BufferLWMA8[i] = LinearWeightedMA_2(rates_total, period_svrma, i, BufferLWMA7)
        BufferLWMA9[i] = LinearWeightedMA_2(rates_total, period_svrma, i, BufferLWMA8)
        BufferLWMA10[i] = LinearWeightedMA_2(rates_total, period_svrma, i, BufferLWMA9)
        value = 0.0
        value += 5 * BufferLWMA1[i]
        value += 4 * BufferLWMA2[i]
        value += 3 * BufferLWMA3[i]
        value += 2 * BufferLWMA4[i]
        value += BufferLWMA5[i]
        value += BufferLWMA6[i]
        value += BufferLWMA7[i]
        value += BufferLWMA8[i]
        value += BufferLWMA9[i]
        value += BufferLWMA10[i]
        BufferRMA[i] = value / 20.0
    if RSIOnArray(rates_total, prev_calculated, period_max, period_rsi, BufferRMA, BufferPosRSI, BufferNegRSI, BufferTmpRSI) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferRSI[i] = 0.1 * (BufferTmpRSI[i] - 50.0)
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferRSI, BufferSmMA1) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferSmMA1, BufferSmMA2) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        zl_ema = BufferSmMA1[i] + (BufferSmMA1[i] - BufferSmMA2[i])
        BufferSVRSI[i] = (_fdiv(pow(2.71828183, 2 * zl_ema) - 1.0, pow(2.71828183, 2 * zl_ema) + 1.0) + 1.0) * 50.0
    return rates_total

def RSIOnArray(rates_total, prev_calculated, begin, period, price, buffer_pos, buffer_neg, buffer_rsi):
    i = 0
    diff = 0
    if period < 1 or (rates_total - begin) < period:
        return 0
    as_series_price = ArrayGetAsSeries(price)
    as_series_rsi = ArrayGetAsSeries(buffer_rsi)
    if as_series_price:
        ArraySetAsSeries(price, False)
    if as_series_rsi:
        ArraySetAsSeries(buffer_rsi, False)
        ArraySetAsSeries(buffer_pos, False)
        ArraySetAsSeries(buffer_neg, False)
    pos = prev_calculated - 1
    if pos <= period:
        buffer_rsi[0] = 0.0
        buffer_pos[0] = 0.0
        buffer_neg[0] = 0.0
        SumP = 0.0
        SumN = 0.0
        i = 1
        for i in range(i, period + 1):
            buffer_rsi[i] = 0.0
            buffer_pos[i] = 0.0
            buffer_neg[i] = 0.0
            diff = price[i] - price[i - 1]
            SumP += (diff if (diff > 0) else 0)
            SumN += ((-diff) if (diff < 0) else 0)
        else:
            i = _range_end(i, period + 1, 1)
        buffer_pos[period] = _fdiv(SumP, period)
        buffer_neg[period] = _fdiv(SumN, period)
        buffer_rsi[period] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(buffer_pos[period], (buffer_neg[period] if (buffer_neg[period] > 0) else DBL_MIN)))
        pos = period + 1
    i = pos
    for i in range(i, rates_total):
        diff = price[i] - price[i - 1]
        buffer_pos[i] = _fdiv((buffer_pos[i - 1] * (period - 1)) + (diff if (diff > 0.0) else 0.0), period)
        buffer_neg[i] = _fdiv((buffer_neg[i - 1] * (period - 1)) + ((-diff) if (diff < 0.0) else 0.0), period)
        buffer_rsi[i] = 100.0 - _fdiv(100.0, 1 + _fdiv(buffer_pos[i], (buffer_neg[i] if (buffer_neg[i] > 0) else DBL_MIN)))
    else:
        i = _range_end(i, rates_total, 1)
    if as_series_price:
        ArraySetAsSeries(price, True)
    if as_series_rsi:
        ArraySetAsSeries(buffer_rsi, True)
        ArraySetAsSeries(buffer_pos, True)
        ArraySetAsSeries(buffer_neg, True)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SylvainVervoortRSIInverseFisherTransform(_MQL5Indicator):
    name = 'Sylvain_Vervoort_RSI_inverse_fisher_transform'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodSVRMA': 2,  # SVRMA period
        'InpPeriodRSI': 4,  # RSI period
        'InpPeriodMA': 4,  # MA period
        'InpOverbought': 88.0,  # Overbought
        'InpOversold': 12.0,  # Oversold
    }

