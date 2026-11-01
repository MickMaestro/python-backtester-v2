"""Kalman bands — converted from MQL5: MQL5 Indicators/Kalman bands/Kalman bands.mq5

Copyright: mladenfx@gmail.com; Link: mladen

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'link': 'mladen', 'copyright': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 8, 4: 8, 5: 1}, 'colors': {1: [13628367], 2: [13492732], 3: [3329330, 6333684], 4: [3329330, 6333684], 5: [11119017]}, 'widths': {}, 'styles': {}, 'labels': {1: 'upper filling', 2: 'lower filling', 3: 'Upper band', 4: 'Lower band', 5: 'Middle value'}, 'levels': [], 'description': [], 'name': 'Kalman bands', 'source': 'MQL5 Indicators/Kalman bands/Kalman bands.mq5', 'folder': 'Kalman bands', 'inputs': [{'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'Order', 'py': 'Order', 'param': 'Order', 'type': 'int', 'default': 2, 'label': 'Filter Order', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 14, 'label': 'Fast Filter Period', 'sinput': False}, {'mql': 'PreSmooth', 'py': 'PreSmooth', 'param': 'PreSmooth', 'type': 'int', 'default': 3, 'label': 'Pre-smoothing period', 'sinput': False}, {'mql': 'PreSmoothMode', 'py': 'PreSmoothMode', 'param': 'PreSmoothMode', 'type': 'int', 'default': 3, 'label': 'Pre-smoothing MA Mode', 'sinput': False}, {'mql': 'K_Sigma', 'py': 'K_Sigma', 'param': 'K_Sigma', 'type': 'double', 'default': 2.0, 'label': 'Multiplier of Sigma(Standard Deviation)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enOrder
ord_1 = 0
ord_2 = 1
ord_3 = 2
_enum('enOrder', {0: 'ord_1', 1: 'ord_2', 2: 'ord_3'})

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
Price = _input('Price', PRICE_CLOSE)  # Price
Order = _input('Order', ord_3)  # Filter Order
Length = _input('Length', 14)  # Fast Filter Period
PreSmooth = _input('PreSmooth', 3)  # Pre-smoothing period
PreSmoothMode = _input('PreSmoothMode', ma_lwma)  # Pre-smoothing MA Mode
K_Sigma = _input('K_Sigma', 2.0)  # Multiplier of Sigma(Standard Deviation)
bufferUp = Arr(0, 0.0)
bufferUpc = Arr(0, 0.0)
bufferDn = Arr(0, 0.0)
bufferDnc = Arr(0, 0.0)
bufferMe = Arr(0, 0.0)
fupu = Arr(0, 0.0)
fupd = Arr(0, 0.0)
fdnd = Arr(0, 0.0)
fdnu = Arr(0, 0.0)
lowpass = Arr(0, 0.0)
delta = Arr(0, 0.0)
smoother = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, fupu, INDICATOR_DATA)
    SetIndexBuffer(1, fupd, INDICATOR_DATA)
    SetIndexBuffer(2, fdnu, INDICATOR_DATA)
    SetIndexBuffer(3, fdnd, INDICATOR_DATA)
    SetIndexBuffer(4, bufferUp, INDICATOR_DATA)
    SetIndexBuffer(5, bufferUpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, bufferDn, INDICATOR_DATA)
    SetIndexBuffer(7, bufferDnc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, bufferMe, INDICATOR_DATA)
    SetIndexBuffer(9, lowpass, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, delta, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, smoother, INDICATOR_CALCULATIONS)
    return 0

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    a = 0.0
    b = 0.0
    c = 0.0
    _sw1 = Order
    if _sw1 == ord_1:
        a = 2.0 / (1 + Length)
    elif _sw1 == ord_2:
        a = MathExp(((-MathSqrt(2)) * M_PI) / Length)
        b = 2 * a * MathCos((MathSqrt(2) * M_PI) / Length)
    else:
        a = MathExp((-M_PI) / Length)
        b = 2 * a * MathCos((MathSqrt(3) * M_PI) / Length)
        c = MathExp((-2 * M_PI) / Length)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _price = getPrice(Price, open, close, high, low, i, rates_total)
        detrend = 0.0
        smoother[i] = iCustomMa(PreSmoothMode, _price, PreSmooth, i, rates_total, 0)
        _sw2 = Order
        if _sw2 == ord_1:
            lowpass[i] = ((((1 - a) * lowpass[i - 1]) + (a * smoother[i])) if (i > 0) else smoother[i])
            detrend = smoother[i] - lowpass[i]
            delta[i] = ((((1 - a) * delta[i - 1]) + (a * detrend)) if (i > 0) else 0)
        elif _sw2 == ord_2:
            lowpass[i] = (((b * lowpass[i - 1]) - (a * a * lowpass[i - 2]) + ((1 - b + (a * a)) * smoother[i])) if (i > 1) else smoother[i])
            detrend = smoother[i] - lowpass[i]
            delta[i] = (((b * delta[i - 1]) - (a * a * delta[i - 2]) + ((1 - b + (a * a)) * detrend)) if (i > 1) else 0)
        else:
            lowpass[i] = ((((b + c) * lowpass[i - 1]) - ((c + (b * c)) * lowpass[i - 2]) + (c * c * lowpass[i - 3]) + ((1 - b + c) * (1 - c) * smoother[i])) if (i > 2) else smoother[i])
            detrend = smoother[i] - lowpass[i]
            delta[i] = ((((b + c) * delta[i - 1]) - ((c + (b * c)) * delta[i - 2]) + (c * c * delta[i - 3]) + ((1 - b + c) * (1 - c) * detrend)) if (i > 2) else 0)
        bufferMe[i] = lowpass[i] + delta[i]
        Sum = 0.0
        j = 0
        while j < Length and (i - j) >= 0:
            del_ = smoother[i - j] - bufferMe[i - j]
            Sum += del_ * del_
            j += 1
        _dev = MathSqrt(Sum / Length)
        bufferUp[i] = bufferMe[i] + (K_Sigma * _dev)
        bufferDn[i] = bufferMe[i] - (K_Sigma * _dev)
        fupd[i] = bufferMe[i]
        fupu[i] = bufferUp[i]
        fdnu[i] = bufferMe[i]
        fdnd[i] = bufferDn[i]
        if i > 0:
            bufferUpc[i] = bufferUpc[i - 1]
            bufferDnc[i] = bufferDnc[i - 1]
            if bufferUp[i] > bufferUp[i - 1]:
                bufferUpc[i] = 0.0
            if bufferUp[i] < bufferUp[i - 1]:
                bufferUpc[i] = 1.0
            if bufferDn[i] > bufferDn[i - 1]:
                bufferDnc[i] = 0.0
            if bufferDn[i] < bufferDn[i - 1]:
                bufferDnc[i] = 1.0
        i += 1
    return i

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw3 = mode
    if _sw3 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw3 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw3 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw3 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    workSmma[r][instanceNo] = price
    if r > 1 and period > 1:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    if period < 1:
        return price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)

def getPrice(tprice, open, close, high, low, i, _bars):
    _sw4 = tprice
    if _sw4 == PRICE_CLOSE:
        return close[i]
    elif _sw4 == PRICE_OPEN:
        return open[i]
    elif _sw4 == PRICE_HIGH:
        return high[i]
    elif _sw4 == PRICE_LOW:
        return low[i]
    elif _sw4 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw4 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw4 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KalmanBands(_MQL5Indicator):
    name = 'Kalman bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'Order': _Choice({0: 'First order (EMA)', 1: 'Second order', 2: 'Third order'}, default=2),  # Filter Order
        'Length': 14,  # Fast Filter Period
        'PreSmooth': 3,  # Pre-smoothing period
        'PreSmoothMode': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=3),  # Pre-smoothing MA Mode
        'K_Sigma': 2.0,  # Multiplier of Sigma(Standard Deviation)
    }

