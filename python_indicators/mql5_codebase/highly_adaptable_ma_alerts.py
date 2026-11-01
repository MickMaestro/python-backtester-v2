"""Highly_Adaptable_MA_Alerts — converted from MQL5: MQL5 Indicators/Highly_Adaptable_MA_Alerts/Highly_Adaptable_MA_Alerts.mq5

Highly Adaptable Moving Average Alert indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 5, 5: 5, 6: 5}, 'colors': {1: [16748574], 2: [255], 3: [3329330], 4: [32768], 5: [255], 6: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 2, 3: 2, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'MA', 2: 'Top band', 3: 'Bottom band', 4: 'Mean crossing', 5: 'Top crossing', 6: 'Bottom crossing'}, 'levels': [], 'description': ['Highly Adaptable Moving Average Alert indicator'], 'name': 'Highly_Adaptable_MA_Alerts', 'source': 'MQL5 Indicators/Highly_Adaptable_MA_Alerts/Highly_Adaptable_MA_Alerts.mq5', 'folder': 'Highly_Adaptable_MA_Alerts', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 50, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'MA method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'MA applied price', 'sinput': False}, {'mql': 'InpPercentBand', 'py': 'InpPercentBand', 'param': 'InpPercentBand', 'type': 'double', 'default': 0.618, 'label': 'Bands percent', 'sinput': False}, {'mql': 'InpReasonAlert', 'py': 'InpReasonAlert', 'param': 'InpReasonAlert', 'type': 'int', 'default': 0, 'label': 'Show alerts for', 'sinput': False}, {'mql': 'InpUseAlert', 'py': 'InpUseAlert', 'param': 'InpUseAlert', 'type': 'int', 'default': 1, 'label': 'Use alert', 'sinput': False}, {'mql': 'InpSendMail', 'py': 'InpSendMail', 'param': 'InpSendMail', 'type': 'int', 'default': 0, 'label': 'Send mail', 'sinput': False}, {'mql': 'InpSendPush', 'py': 'InpSendPush', 'param': 'InpSendPush', 'type': 'int', 'default': 1, 'label': 'Send push', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum ENUM_ALERT_REASON
REASON_ALERT_ALL = 0
REASON_ALERT_MEAN = 1
REASON_ALERT_TOP = 2
REASON_ALERT_BOTTOM = 3
_enum('ENUM_ALERT_REASON', {0: 'REASON_ALERT_ALL', 1: 'REASON_ALERT_MEAN', 2: 'REASON_ALERT_TOP', 3: 'REASON_ALERT_BOTTOM'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 50)  # MA period
InpMethod = _input('InpMethod', METHOD_EMA)  # MA method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # MA applied price
InpPercentBand = _input('InpPercentBand', 0.618)  # Bands percent
InpReasonAlert = _input('InpReasonAlert', REASON_ALERT_ALL)  # Show alerts for
InpUseAlert = _input('InpUseAlert', INPUT_YES)  # Use alert
InpSendMail = _input('InpSendMail', INPUT_NO)  # Send mail
InpSendPush = _input('InpSendPush', INPUT_YES)  # Send push
BufferMA = Arr(0, 0.0)
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferSigMean = Arr(0, 0.0)
BufferSigTop = Arr(0, 0.0)
BufferSigBottom = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
percent_band = 0.0
point = 0.0
period_ma = 0
handle_ma = 0

def OnInit():
    global handle_ma, percent_band, period_ma, point
    point = Point()
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    percent_band = InpPercentBand
    SetIndexBuffer(0, BufferMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSigMean, INDICATOR_DATA)
    SetIndexBuffer(4, BufferSigTop, INDICATOR_DATA)
    SetIndexBuffer(5, BufferSigBottom, INDICATOR_DATA)
    SetIndexBuffer(6, BufferPrice, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetInteger(4, PLOT_ARROW, 234)
    PlotIndexSetInteger(5, PLOT_ARROW, 233)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Highly Adaptable ' + MethodToString(InpMethod) + ' (' + _str(period_ma) + ',' + _str(percent_band) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferSigMean, True)
    ArraySetAsSeries(BufferSigTop, True)
    ArraySetAsSeries(BufferSigBottom, True)
    ArraySetAsSeries(BufferPrice, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_time
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ma - 1
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferSigMean, EMPTY_VALUE)
        ArrayInitialize(BufferSigTop, EMPTY_VALUE)
        ArrayInitialize(BufferSigBottom, EMPTY_VALUE)
        ArrayInitialize(BufferPrice, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferPrice)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        _sw1 = InpMethod
        if _sw1 == METHOD_EMA:
            BufferMA[i] = EMA(rates_total, BufferPrice[i], BufferMA[i + 1], period_ma, i)
        elif _sw1 == METHOD_SMMA:
            BufferMA[i] = SMMA(rates_total, BufferPrice, BufferMA[i + 1], period_ma, i)
        elif _sw1 == METHOD_LWMA:
            BufferMA[i] = LWMA(rates_total, BufferPrice, period_ma, i)
        elif _sw1 == METHOD_WILDER_EMA:
            BufferMA[i] = Wilder(rates_total, BufferPrice[i], BufferMA[i + 1], period_ma, i)
        elif _sw1 == METHOD_SINE_WMA:
            BufferMA[i] = SineWMA(rates_total, BufferPrice, period_ma, i)
        elif _sw1 == METHOD_TRI_MA:
            BufferMA[i] = TriMA(rates_total, BufferPrice, period_ma, i)
        elif _sw1 == METHOD_LSMA:
            BufferMA[i] = LSMA(rates_total, BufferPrice, period_ma, i)
        elif _sw1 == METHOD_HMA:
            BufferMA[i] = HMA(rates_total, BufferPrice, period_ma, i)
        elif _sw1 == METHOD_ZL_EMA:
            BufferMA[i] = ZeroLagEMA(rates_total, BufferPrice, BufferMA[i + 1], period_ma, i)
        elif _sw1 == METHOD_ITREND_MA:
            BufferMA[i] = ITrend(rates_total, BufferPrice, BufferMA, period_ma, i)
        elif _sw1 == METHOD_MOVING_MEDIAN:
            BufferMA[i] = Median(rates_total, BufferPrice, period_ma, i)
        elif _sw1 == METHOD_GEO_MEAN:
            BufferMA[i] = GeoMean(rates_total, BufferPrice, period_ma, i)
        elif _sw1 == METHOD_REMA:
            BufferMA[i] = REMA(rates_total, BufferPrice[i], BufferMA, period_ma, 0.5, i)
        elif _sw1 == METHOD_ILRS:
            BufferMA[i] = ILRS(rates_total, BufferPrice, period_ma, i)
        elif _sw1 == METHOD_IE_2:
            BufferMA[i] = IE2(rates_total, BufferPrice, period_ma, i)
        elif _sw1 == METHOD_TRI_MA_GEN:
            BufferMA[i] = TriMAgen(rates_total, BufferPrice, period_ma, i)
        elif _sw1 == METHOD_VWMA:
            BufferMA[i] = VWMA(rates_total, BufferPrice, tick_volume, period_ma, i)
        else:
            BufferMA[i] = SMA(rates_total, BufferPrice, period_ma, i)
        BufferTop[i] = BufferMA[i] * (1 + (percent_band / 100.0))
        BufferBottom[i] = BufferMA[i] * (1 - (percent_band / 100.0))
        if (InpReasonAlert == REASON_ALERT_ALL or InpReasonAlert == REASON_ALERT_MEAN) and ((close[i + 1] < BufferMA[i + 1] and close[i] >= BufferMA[i]) or (close[i + 1] > BufferMA[i + 1] and close[i] <= BufferMA[i])):
            BufferSigMean[i] = BufferMA[i]
            if i == 0 and time[0] > _s_OnCalculate_last_time:
                message = Symbol() + ',' + TimeframeToString(Period()) + ': Price just crossed the Moving Average Center Line.'
                if InpUseAlert:
                    Alert(message)
                if InpSendMail and TerminalInfoInteger(TERMINAL_EMAIL_ENABLED):
                    SendMail('Moving Average Cross Signal', message)
                if InpSendPush and TerminalInfoInteger(TERMINAL_NOTIFICATIONS_ENABLED):
                    SendNotification(message)
                _s_OnCalculate_last_time = TimeCurrent()
        if ((InpReasonAlert == REASON_ALERT_ALL or InpReasonAlert == REASON_ALERT_TOP) and close[i + 1] < BufferTop[i + 1]) and close[i] >= BufferTop[i]:
            BufferSigTop[i] = high[i] + (20 * point)
            if i == 0 and time[0] > _s_OnCalculate_last_time:
                message = Symbol() + ',' + TimeframeToString(Period()) + ': Price just crossed the Moving Average Top Band.'
                if InpUseAlert:
                    Alert(message)
                if InpSendMail and TerminalInfoInteger(TERMINAL_EMAIL_ENABLED):
                    SendMail('Moving Average Cross Signal', message)
                if InpSendPush and TerminalInfoInteger(TERMINAL_NOTIFICATIONS_ENABLED):
                    SendNotification(message)
                _s_OnCalculate_last_time = TimeCurrent()
        if ((InpReasonAlert == REASON_ALERT_ALL or InpReasonAlert == REASON_ALERT_BOTTOM) and close[i + 1] > BufferBottom[i + 1]) and close[i] <= BufferBottom[i]:
            BufferSigBottom[i] = low[i] - (20 * point)
            if i == 0 and time[0] > _s_OnCalculate_last_time:
                message = Symbol() + ',' + TimeframeToString(Period()) + ': Price just crossed the Moving Average Bottom Band.'
                if InpUseAlert:
                    Alert(message)
                if InpSendMail and TerminalInfoInteger(TERMINAL_EMAIL_ENABLED):
                    SendMail('Moving Average Cross Signal', message)
                if InpSendPush and TerminalInfoInteger(TERMINAL_NOTIFICATIONS_ENABLED):
                    SendNotification(message)
                _s_OnCalculate_last_time = TimeCurrent()
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

def MethodToString(method):
    return StringSubstr(EnumToString(method, 'ENUM_MA_MODE'), 7)

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

# ---- static local variables
_s_OnCalculate_last_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HighlyAdaptableMAAlerts(_MQL5Indicator):
    name = 'Highly_Adaptable_MA_Alerts'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 50,  # MA period
        'InpMethod': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'Linear-Weighted', 4: 'Wilder Exponential', 5: 'Sine-Weighted', 6: 'Triangular', 7: 'Least Square', 8: 'Hull MA by Alan Hull', 9: 'Zero-Lag Exponential', 10: 'Instantaneous Trendline by J.Ehlers', 11: 'Moving Median', 12: 'Geometric Mean', 13: 'Regularized EMA by Chris Satchwell', 14: 'Integral of Linear Regression Slope', 15: 'Combination of LSMA and ILRS', 16: 'Triangular MA generalized by J.Ehlers', 17: 'Volume-Weighted'}, default=1),  # MA method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA applied price
        'InpPercentBand': 0.618,  # Bands percent
        'InpReasonAlert': _Choice({0: 'All', 1: 'Mean', 2: 'Top', 3: 'Bottom'}, default=0),  # Show alerts for
        'InpUseAlert': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use alert
        'InpSendMail': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Send mail
        'InpSendPush': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Send push
    }

