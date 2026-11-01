"""18AvgMA — converted from MQL5: MQL5 Indicators/18AvgMA/18AvgMA.mq5

Average of 18 Moving Averages indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Avg of 18 MA'}, 'levels': [], 'description': ['Average of 18 Moving Averages indicator'], 'name': '18AvgMA', 'source': 'MQL5 Indicators/18AvgMA/18AvgMA.mq5', 'folder': '18AvgMA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 50, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 50)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferMA = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
BufferEMA = Arr(0, 0.0)
BufferWilder = Arr(0, 0.0)
BufferSMMA = Arr(0, 0.0)
BufferZeroLagEMA = Arr(0, 0.0)
BufferITrend = Arr(0, 0.0)
BufferREMA = Arr(0, 0.0)
period_ma = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferPrice, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferWilder, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSMMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferZeroLagEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferITrend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferREMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Average of 18 MA (' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferPrice, True)
    ArraySetAsSeries(BufferEMA, True)
    ArraySetAsSeries(BufferWilder, True)
    ArraySetAsSeries(BufferSMMA, True)
    ArraySetAsSeries(BufferZeroLagEMA, True)
    ArraySetAsSeries(BufferITrend, True)
    ArraySetAsSeries(BufferREMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ma - 1
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferPrice, 0)
        ArrayInitialize(BufferEMA, 0)
        ArrayInitialize(BufferWilder, 0)
        ArrayInitialize(BufferSMMA, 0)
        ArrayInitialize(BufferZeroLagEMA, 0)
        ArrayInitialize(BufferITrend, 0)
        ArrayInitialize(BufferREMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferPrice)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferEMA[i] = EMA(rates_total, BufferPrice[i], BufferEMA[i + 1], period_ma, i)
        BufferWilder[i] = Wilder(rates_total, BufferPrice[i], BufferWilder[i + 1], period_ma, i)
        BufferSMMA[i] = SMMA(rates_total, BufferPrice, BufferSMMA[i + 1], period_ma, i)
        BufferZeroLagEMA[i] = ZeroLagEMA(rates_total, BufferPrice, BufferZeroLagEMA[i + 1], period_ma, i)
        BufferITrend[i] = ITrend(rates_total, BufferPrice, BufferITrend, period_ma, i)
        BufferREMA[i] = REMA(rates_total, BufferPrice[i], BufferREMA, period_ma, 0.5, i)
    for i in range(limit, 0 - 1, -1):
        iSMA = SMA(rates_total, BufferPrice, period_ma, i)
        iLWMA = LWMA(rates_total, BufferPrice, period_ma, i)
        iSineWMA = SineWMA(rates_total, BufferPrice, period_ma, i)
        iTriMA = TriMA(rates_total, BufferPrice, period_ma, i)
        iLSMA = LSMA(rates_total, BufferPrice, period_ma, i)
        iHMA = HMA(rates_total, BufferPrice, period_ma, i)
        iMedian = Median(rates_total, BufferPrice, period_ma, i)
        iGeoMean = GeoMean(rates_total, BufferPrice, period_ma, i)
        iILRS = ILRS(rates_total, BufferPrice, period_ma, i)
        iIE2 = IE2(rates_total, BufferPrice, period_ma, i)
        iTriMA_gen = TriMAgen(rates_total, BufferPrice, period_ma, i)
        iVolWMA = VWMA(rates_total, BufferPrice, tick_volume, period_ma, i)
        BufferMA[i] = (iSMA + BufferEMA[i] + BufferWilder[i] + iLWMA + iSineWMA + iTriMA + iLSMA + BufferSMMA[i] + iHMA + BufferZeroLagEMA[i] + BufferITrend[i] + iMedian + iGeoMean + BufferREMA[i] + iILRS + iIE2 + iTriMA_gen + iVolWMA) / 18.0
    return rates_total

def SMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return array_src[shift]
    sum_ = 0.0
    for i in range(0, period):
        sum_ += array_src[shift + i]
    return _fdiv(sum_, period)

def EMA(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + (_fdiv(2.0, 1 + period) * (price - prev))))

def Wilder(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + _fdiv(price - prev, period)))

def LWMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += period - i
        sum_ += array_src[shift + i] * (period - i)
    return (_fdiv(sum_, weight) if (weight > 0) else 0)

def SineWMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += sin(_fdiv(M_PI * (i + 1), period + 1))
        sum_ += array_src[shift + i] * sin(_fdiv(M_PI * (i + 1), period + 1))
    return (_fdiv(sum_, weight) if (weight > 0) else 0)

def TriMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sma = 0.0
    len_ = _int(ceil((period + 1) * 0.5))
    sum_ = 0.0
    for i in range(0, len_):
        sma = SMA(rates_total, array_src, len_, shift + i)
        sum_ += sma
    trima = _fdiv(sum_, len_)
    return trima

def LSMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    for i in range(period, 1 - 1, -1):
        sum_ += (i - ((period + 1) / 3.0)) * array_src[shift + period - i]
    lsma = _fdiv(sum_ * 6.0, period * (period + 1))
    return lsma

def SMMA(rates_total, array_src, prev, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    smma = 0.0
    if shift == (rates_total - period - 1):
        smma = SMA(rates_total, array_src, period, shift)
    elif shift < (rates_total - period - 1):
        sum_ = 0.0
        for i in range(0, period):
            sum_ += array_src[shift + i + 1]
        smma = _fdiv(sum_ - prev + array_src[shift], period)
    return smma

def HMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    tmp1 = Arr(0, 0.0)
    hma = 0.0
    len_ = _int(sqrt(period))
    ArrayResize(tmp1, len_)
    if shift == (rates_total - period - 1):
        hma = array_src[shift]
    elif shift < (rates_total - period - 1):
        for i in range(0, len_):
            tmp1[i] = (2.0 * LWMA(rates_total, array_src, _idiv(period, 2), shift + i)) - LWMA(rates_total, array_src, period, shift + i)
        hma = LWMA(rates_total, tmp1, len_, 0)
    return hma

def ZeroLagEMA(rates_total, array_src, prev, period, shift):
    alfa = _fdiv(2.0, 1 + period)
    lag = _int(0.5 * (period - 1))
    return (array_src[shift] if (shift >= (rates_total - lag)) else ((alfa * ((2.0 * array_src[shift]) - array_src[shift + lag])) + ((1 - alfa) * prev)))

def ITrend(rates_total, array_src, array, period, shift):
    alfa = _fdiv(2.0, period + 1)
    return ((((alfa - (0.25 * alfa * alfa)) * array_src[shift]) + (0.5 * alfa * alfa * array_src[shift + 1]) - ((alfa - (0.75 * alfa * alfa)) * array_src[shift + 2]) + (2 * (1 - alfa) * array[shift + 1]) - ((1 - alfa) * (1 - alfa) * array[shift + 2])) if (shift < (rates_total - 7)) else ((array_src[shift] + (2 * array_src[shift + 1]) + array_src[shift + 2]) / 4.0))

def Median(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    array = Arr(0, 0.0)
    ArrayResize(array, period)
    for i in range(0, period):
        array[i] = array_src[shift + i]
    ArraySort(array)
    num = _int(round(_idiv(period - 1, 2)))
    return (array_src[num] if (fmod(period, 2) > 0) else (0.5 * (array_src[num] + array[num + 1])))

def GeoMean(rates_total, array_src, period, shift):
    gmean = 0.0
    if shift < (rates_total - period):
        gmean = pow(array_src[shift], _fdiv(1.0, period))
        for i in range(1, period):
            gmean *= pow(array_src[shift + i], _fdiv(1.0, period))
    return gmean

def REMA(rates_total, price, array, period, lambda_, shift):
    alpha = _fdiv(2.0, period + 1)
    return (price if (shift >= (rates_total - 3)) else _fdiv((array[shift + 1] * (1 + (2 * lambda_))) + (alpha * (price - array[shift + 1])) - (lambda_ * array[shift + 2]), 1 + lambda_))

def ILRS(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = period * (period - 1) * 0.5
    sum2 = ((period - 1) * period * ((2 * period) - 1)) / 6.0
    sum1 = 0.0
    sumy = 0.0
    for i in range(0, period):
        sum1 += i * array_src[shift + i]
        sumy += array_src[shift + i]
    num1 = (period * sum1) - (sum_ * sumy)
    num2 = (sum_ * sum_) - (period * sum2)
    slope = (_fdiv(num1, num2) if (num2 != 0) else 0)
    return slope + SMA(rates_total, array_src, period, shift)

def IE2(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    return 0.5 * (ILRS(rates_total, array_src, period, shift) + LSMA(rates_total, array_src, period, shift))

def TriMAgen(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    len1 = _int(floor((period + 1) * 0.5))
    len2 = _int(ceil((period + 1) * 0.5))
    sum_ = 0.0
    for i in range(0, len2):
        sum_ += SMA(rates_total, array_src, len1, shift + i)
    return _fdiv(sum_, len2)

def VWMA(rates_total, array_src, volume, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += float(volume[shift + i])
        sum_ += array_src[shift + i] * volume[shift + i]
    return (_fdiv(sum_, weight) if (weight > 0) else 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind18AvgMA(_MQL5Indicator):
    name = '18AvgMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriod': 50,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

