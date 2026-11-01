"""Nonlinear Kalman filter deviation — converted from MQL5: MQL5 Indicators/Nonlinear Kalman filter deviation/Nonlinear Kalman filter deviation.mq5

Deviation based on Ehlers nonlinear Kalman filter
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Deviation'}, 'levels': [], 'description': ['Deviation based on Ehlers nonlinear Kalman filter'], 'name': 'Nonlinear Kalman filter deviation', 'source': 'MQL5 Indicators/Nonlinear Kalman filter deviation/Nonlinear Kalman filter deviation.mq5', 'folder': 'Nonlinear Kalman filter deviation', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 14, 'label': 'Filter Period', 'sinput': False}, {'mql': 'Order', 'py': 'Order', 'param': 'Order', 'type': 'int', 'default': 2, 'label': 'Filter Order', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'PreSmooth', 'py': 'PreSmooth', 'param': 'PreSmooth', 'type': 'int', 'default': 3, 'label': 'Pre-smoothing period', 'sinput': False}, {'mql': 'PreSmoothMode', 'py': 'PreSmoothMode', 'param': 'PreSmoothMode', 'type': 'int', 'default': 3, 'label': 'Pre-smoothing MA method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enOrder
ord_1 = 0
ord_2 = 1
ord_3 = 2
_enum('enOrder', {0: 'ord_1', 1: 'ord_2', 2: 'ord_3'})

# ---- inputs and global variables
Length = _input('Length', 14)  # Filter Period
Order = _input('Order', ord_3)  # Filter Order
Price = _input('Price', PRICE_CLOSE)  # Price
PreSmooth = _input('PreSmooth', 3)  # Pre-smoothing period
PreSmoothMode = _input('PreSmoothMode', MODE_LWMA)  # Pre-smoothing MA method
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
lowpass = Arr(0, 0.0)
delta = Arr(0, 0.0)
flt = Arr(0, 0.0)
avg = Arr(0, 0.0)
dev_diff = Arr(0, 0.0)
dev_summ = Arr(0, 0.0)
ª_a = 0.0
ª_b = 0.0
ª_c = 0.0
ª_maHandle = 0

def OnInit():
    global ª_a, ª_b, ª_c, ª_maHandle
    ª_maHandle = iMA(Symbol(), 0, PreSmooth, 0, PreSmoothMode, Price)
    if not _checkHandle(ª_maHandle, 'average'):
        return INIT_FAILED
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, flt, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, avg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, delta, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, lowpass, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, dev_diff, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, dev_summ, INDICATOR_CALCULATIONS)
    _sw1 = Order
    if _sw1 == ord_1:
        ª_a = 2.0 / (1 + Length)
    elif _sw1 == ord_2:
        ª_a = MathExp(((-MathSqrt(2)) * M_PI) / Length)
        ª_b = 2 * ª_a * MathCos((MathSqrt(2) * M_PI) / Length)
    else:
        ª_a = MathExp((-M_PI) / Length)
        ª_b = 2 * ª_a * MathCos((MathSqrt(3) * M_PI) / Length)
        ª_c = MathExp((-2 * M_PI) / Length)
    IndicatorSetString(INDICATOR_SHORTNAME, 'NL Kalman filter deviation (' + _str(Length) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_maHandle, 0, 0, _copyCount, avg) != _copyCount:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _price = 0.0
        _sw2 = Price
        if _sw2 == PRICE_CLOSE:
            _price = close[i]
        elif _sw2 == PRICE_OPEN:
            _price = open[i]
        elif _sw2 == PRICE_HIGH:
            _price = high[i]
        elif _sw2 == PRICE_LOW:
            _price = low[i]
        elif _sw2 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw2 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw2 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        if avg[i] == EMPTY_VALUE:
            avg[i] = _price
        _sw3 = Order
        if _sw3 == ord_1:
            lowpass[i] = ((((1 - ª_a) * lowpass[i - 1]) + (ª_a * avg[i])) if (i > 0) else avg[i])
            delta[i] = ((((1 - ª_a) * delta[i - 1]) + (ª_a * (avg[i] - lowpass[i]))) if (i > 0) else 0)
        elif _sw3 == ord_2:
            lowpass[i] = (((ª_b * lowpass[i - 1]) - (ª_a * ª_a * lowpass[i - 2]) + ((1 - ª_b + (ª_a * ª_a)) * avg[i])) if (i > 1) else avg[i])
            delta[i] = (((ª_b * delta[i - 1]) - (ª_a * ª_a * delta[i - 2]) + ((1 - ª_b + (ª_a * ª_a)) * (avg[i] - lowpass[i]))) if (i > 1) else 0)
        else:
            lowpass[i] = ((((ª_b + ª_c) * lowpass[i - 1]) - ((ª_c + (ª_b * ª_c)) * lowpass[i - 2]) + (ª_c * ª_c * lowpass[i - 3]) + ((1 - ª_b + ª_c) * (1 - ª_c) * avg[i])) if (i > 2) else avg[i])
            delta[i] = ((((ª_b + ª_c) * delta[i - 1]) - ((ª_c + (ª_b * ª_c)) * delta[i - 2]) + (ª_c * ª_c * delta[i - 3]) + ((1 - ª_b + ª_c) * (1 - ª_c) * (avg[i] - lowpass[i]))) if (i > 2) else 0)
        flt[i] = lowpass[i] + delta[i]
        dev_diff[i] = (avg[i] - flt[i]) * (avg[i] - flt[i])
        if i > Length:
            dev_summ[i] = dev_summ[i - 1] + dev_diff[i] - dev_diff[i - Length]
        else:
            dev_summ[i] = dev_diff[i]
            k = 1
            while k < Length and i >= k:
                dev_summ[i] += dev_diff[i - k]
                k += 1
        val[i] = MathSqrt(dev_summ[i] / Length)
        valc[i] = ((0 if (val[i] > val[i - 1]) else 1) if (i > 0) else 0)
        i += 1
    return i

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__handles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__handles, _size + 1)
        _s__checkHandle__handles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__handles[i])
        ArrayResize(_s__checkHandle__handles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- static local variables
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NonlinearKalmanFilterDeviation(_MQL5Indicator):
    name = 'Nonlinear Kalman filter deviation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 14,  # Filter Period
        'Order': _Choice({0: 'First order (EMA)', 1: 'Second order', 2: 'Third order'}, default=2),  # Filter Order
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'PreSmooth': 3,  # Pre-smoothing period
        'PreSmoothMode': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Pre-smoothing MA method
    }

