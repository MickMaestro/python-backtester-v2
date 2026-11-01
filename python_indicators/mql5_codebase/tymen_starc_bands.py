"""Tymen_STARC_Bands — converted from MQL5: MQL5 Indicators/Tymen_STARC_Bands/Tymen_STARC_Bands.mq5

Tymen STARC Bands indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'colors': {1: [255], 2: [255], 3: [255], 4: [255], 5: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Highest', 2: 'Top', 3: 'Middle', 4: 'Bottom', 5: 'Lowest'}, 'levels': [], 'description': ['Tymen STARC Bands indicator'], 'name': 'Tymen_STARC_Bands', 'source': 'MQL5 Indicators/Tymen_STARC_Bands/Tymen_STARC_Bands.mq5', 'folder': 'Tymen_STARC_Bands', 'inputs': [{'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 15, 'label': 'ATR period', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 6, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpKATR', 'py': 'InpKATR', 'param': 'InpKATR', 'type': 'double', 'default': 1.0, 'label': 'ATR coefficient', 'sinput': False}, {'mql': 'InpMKATR', 'py': 'InpMKATR', 'param': 'InpMKATR', 'type': 'double', 'default': 0.7, 'label': 'ATR middle coefficient', 'sinput': False}, {'mql': 'InpShowMiddle', 'py': 'InpShowMiddle', 'param': 'InpShowMiddle', 'type': 'int', 'default': 1, 'label': 'Show middle lines', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MA_MODE
METHOD_SMA = 0
METHOD_EMA = 1
METHOD_SMMA = 2
METHOD_LWMA = 3
METHOD_WILDER_EMA = 4
METHOD_SINE_WMA = 5
METHOD_TRI_MA = 6
METHOD_LSMA = 7
METHOD_HMA = 8
METHOD_ZL_EMA = 9
METHOD_ITREND_MA = 10
METHOD_MOVING_MEDIAN = 11
METHOD_GEO_MEAN = 12
METHOD_REMA = 13
METHOD_ILRS = 14
METHOD_IE_2 = 15
METHOD_TRI_MA_GEN = 16
METHOD_VWMA = 17
_enum('ENUM_MA_MODE', {0: 'METHOD_SMA', 1: 'METHOD_EMA', 2: 'METHOD_SMMA', 3: 'METHOD_LWMA', 4: 'METHOD_WILDER_EMA', 5: 'METHOD_SINE_WMA', 6: 'METHOD_TRI_MA', 7: 'METHOD_LSMA', 8: 'METHOD_HMA', 9: 'METHOD_ZL_EMA', 10: 'METHOD_ITREND_MA', 11: 'METHOD_MOVING_MEDIAN', 12: 'METHOD_GEO_MEAN', 13: 'METHOD_REMA', 14: 'METHOD_ILRS', 15: 'METHOD_IE_2', 16: 'METHOD_TRI_MA_GEN', 17: 'METHOD_VWMA'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodATR = _input('InpPeriodATR', 15)  # ATR period
InpPeriodMA = _input('InpPeriodMA', 6)  # MA period
InpMethod = _input('InpMethod', METHOD_EMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpKATR = _input('InpKATR', 1.0)  # ATR coefficient
InpMKATR = _input('InpMKATR', 0.7)  # ATR middle coefficient
InpShowMiddle = _input('InpShowMiddle', INPUT_YES)  # Show middle lines
BufferTopExtr = Arr(0, 0.0)
BufferTop = Arr(0, 0.0)
BufferMiddle = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferBottomExtr = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
katr = 0.0
mkatr = 0.0
period_ma = 0
period_atr = 0
handle_ma = 0
handle_atr = 0

def OnInit():
    global handle_atr, handle_ma, katr, mkatr, period_atr, period_ma
    period_ma = (2 if (InpPeriodMA < 2) else InpPeriodMA)
    period_atr = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    katr = InpKATR
    mkatr = InpMKATR
    SetIndexBuffer(0, BufferTopExtr, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMiddle, INDICATOR_DATA)
    SetIndexBuffer(3, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(4, BufferBottomExtr, INDICATOR_DATA)
    SetIndexBuffer(5, BufferATR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferPrice, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Tymen STARC Bands (' + _str(period_atr) + ',' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, InpShowMiddle)
    ArraySetAsSeries(BufferTopExtr, True)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferMiddle, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferBottomExtr, True)
    ArraySetAsSeries(BufferATR, True)
    ArraySetAsSeries(BufferPrice, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 3
        ArrayInitialize(BufferTopExtr, EMPTY_VALUE)
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferMiddle, 0)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferBottomExtr, EMPTY_VALUE)
        ArrayInitialize(BufferATR, 0)
        ArrayInitialize(BufferPrice, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferPrice)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        GetMA(rates_total, InpMethod, period_ma, i, BufferPrice, BufferMiddle, tick_volume)
        BufferTopExtr[i] = BufferMiddle[i] + (BufferATR[i] * katr)
        BufferTop[i] = BufferMiddle[i] + (BufferATR[i] * mkatr)
        BufferBottom[i] = BufferMiddle[i] - (BufferATR[i] * mkatr)
        BufferBottomExtr[i] = BufferMiddle[i] - (BufferATR[i] * katr)
    return rates_total

def GetMA(rates_total, method, period, shift, price, ma, tick_volume):
    _sw1 = method
    if _sw1 == METHOD_EMA:
        ma[shift] = EMA(rates_total, price[shift], ma[shift + 1], period, shift)
    elif _sw1 == METHOD_SMMA:
        ma[shift] = SMMA(rates_total, price, ma[shift + 1], period, shift)
    elif _sw1 == METHOD_LWMA:
        ma[shift] = LWMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_WILDER_EMA:
        ma[shift] = Wilder(rates_total, price[shift], ma[shift + 1], period, shift)
    elif _sw1 == METHOD_SINE_WMA:
        ma[shift] = SineWMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_TRI_MA:
        ma[shift] = TriMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_LSMA:
        ma[shift] = LSMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_HMA:
        ma[shift] = HMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_ZL_EMA:
        ma[shift] = ZeroLagEMA(rates_total, price, ma[shift + 1], period, shift)
    elif _sw1 == METHOD_ITREND_MA:
        ma[shift] = ITrend(rates_total, price, ma, period, shift)
    elif _sw1 == METHOD_MOVING_MEDIAN:
        ma[shift] = Median(rates_total, price, period, shift)
    elif _sw1 == METHOD_GEO_MEAN:
        ma[shift] = GeoMean(rates_total, price, period, shift)
    elif _sw1 == METHOD_REMA:
        ma[shift] = REMA(rates_total, price[shift], ma, period, 0.5, shift)
    elif _sw1 == METHOD_ILRS:
        ma[shift] = ILRS(rates_total, price, period, shift)
    elif _sw1 == METHOD_IE_2:
        ma[shift] = IE2(rates_total, price, period, shift)
    elif _sw1 == METHOD_TRI_MA_GEN:
        ma[shift] = TriMAgen(rates_total, price, period, shift)
    elif _sw1 == METHOD_VWMA:
        ma[shift] = VWMA(rates_total, price, tick_volume, period, shift)
    else:
        ma[shift] = SMA(rates_total, price, period, shift)

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
    return _fdiv(sum_, len_)

def LSMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    for i in range(period, 1 - 1, -1):
        sum_ += (i - ((period + 1) / 3.0)) * array_src[shift + period - i]
    return _fdiv(sum_ * 6.0, period * (period + 1))

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


class TymenSTARCBands(_MQL5Indicator):
    name = 'Tymen_STARC_Bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodATR': 15,  # ATR period
        'InpPeriodMA': 6,  # MA period
        'InpMethod': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'Linear-Weighted', 4: 'Wilder Exponential', 5: 'Sine-Weighted', 6: 'Triangular', 7: 'Least Square', 8: 'Hull MA by Alan Hull', 9: 'Zero-Lag Exponential', 10: 'Instantaneous Trendline by J.Ehlers', 11: 'Moving Median', 12: 'Geometric Mean', 13: 'Regularized EMA by Chris Satchwell', 14: 'Integral of Linear Regression Slope', 15: 'Combination of LSMA and ILRS', 16: 'Triangular MA generalized by J.Ehlers', 17: 'Volume-Weighted'}, default=1),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpKATR': 1.0,  # ATR coefficient
        'InpMKATR': 0.7,  # ATR middle coefficient
        'InpShowMiddle': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show middle lines
    }

