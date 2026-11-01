"""ATR_MAs — converted from MQL5: MQL5 Indicators/ATR Weighted Moving Averages/ATR_MAs.mq5

Copyright: Copyright 2022, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'MA'}, 'levels': [], 'description': [], 'name': 'ATR_MAs', 'source': 'MQL5 Indicators/ATR Weighted Moving Averages/ATR_MAs.mq5', 'folder': 'ATR Weighted Moving Averages', 'inputs': [{'mql': '_length', 'py': '_length', 'param': '_length', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': '_type', 'py': '_type', 'param': '_type', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': '_atr_length', 'py': '_atr_length', 'param': '_atr_length', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': '_stdev_length', 'py': '_stdev_length', 'param': '_stdev_length', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}, {'mql': '_stdev_mult', 'py': '_stdev_mult', 'param': '_stdev_mult', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum MA_TYPE
ATRWSMA = 0
ATRWEMA = 1
ATRWRMA = 2
ATRWWMA = 3
_enum('MA_TYPE', {0: 'ATRWSMA', 1: 'ATRWEMA', 2: 'ATRWRMA', 3: 'ATRWWMA'})

# enum MA_TYPE2
SMA = 0
EMA = 1
RMA = 2
WMA = 3
_enum('MA_TYPE2', {0: 'SMA', 1: 'EMA', 2: 'RMA', 3: 'WMA'})

# ---- inputs and global variables
_length = _input('_length', 8)
_type = _input('_type', ATRWEMA)
_atr_length = _input('_atr_length', 14)
_stdev_length = _input('_stdev_length', 100)
_stdev_mult = _input('_stdev_mult', 1.0)
MABuffer = Arr(0, 0.0)
EMA1Buffer = Arr(0, 0.0)
EMA2Buffer = Arr(0, 0.0)
RMA1Buffer = Arr(0, 0.0)
RMA2Buffer = Arr(0, 0.0)
RMA3Buffer = Arr(0, 0.0)
atrwoBuffer = Arr(0, 0.0)
trwoBuffer = Arr(0, 0.0)
ta_trBuffer = Arr(0, 0.0)
atrwotmpBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, MABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, EMA1Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, EMA2Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, RMA1Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, RMA2Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, RMA3Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, atrwoBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, trwoBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, ta_trBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, atrwotmpBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(MABuffer, True)
    ArraySetAsSeries(EMA1Buffer, True)
    ArraySetAsSeries(EMA2Buffer, True)
    ArraySetAsSeries(RMA1Buffer, True)
    ArraySetAsSeries(RMA2Buffer, True)
    ArraySetAsSeries(RMA3Buffer, True)
    ArraySetAsSeries(atrwoBuffer, True)
    ArraySetAsSeries(trwoBuffer, True)
    ArraySetAsSeries(ta_trBuffer, True)
    ArraySetAsSeries(atrwotmpBuffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    for i in range(MathMax(rates_total - _length - _atr_length - _stdev_length - prev_calculated, 1), 0 - 1, -1):
        MABuffer[i] = anyma(open, close, high, low, close, _length, _type, _atr_length, _stdev_length, _stdev_mult, i)
    return rates_total

def anyma(open, close, high, low, src, length, type_, atr_length=14, stdev_length=100, stdev_mult=1.0, index=0):
    _sw1 = type_
    if _sw1 == ATRWSMA:
        return atrwma(open, close, high, low, src, length, SMA, atr_length, stdev_length, stdev_mult, index)
    elif _sw1 == ATRWEMA:
        return atrwma(open, close, high, low, src, length, EMA, atr_length, stdev_length, stdev_mult, index)
    elif _sw1 == ATRWRMA:
        return atrwma(open, close, high, low, src, length, RMA, atr_length, stdev_length, stdev_mult, index)
    elif _sw1 == ATRWWMA:
        return atrwma(open, close, high, low, src, length, WMA, atr_length, stdev_length, stdev_mult, index)
    else:
        return EMPTY_VALUE

def atrwma(open, close, high, low, src, length, type_, atr_length, stdev_length, stdev_mult, index):
    atrwo(open, close, high, low, length, stdev_length, stdev_mult, index)
    atrwotmpBuffer[index] = src[index] * atrwoBuffer[index]
    _sw2 = type_
    if _sw2 == SMA:
        return _fdiv(pine_sma(atrwotmpBuffer, length, index), pine_sma(atrwoBuffer, length, index))
    elif _sw2 == EMA:
        return _fdiv(pine_ema(atrwotmpBuffer, EMA1Buffer, length, index), pine_ema(atrwoBuffer, EMA2Buffer, length, index))
    elif _sw2 == RMA:
        return _fdiv(pine_rma(atrwotmpBuffer, RMA1Buffer, length, index), pine_rma(atrwoBuffer, RMA2Buffer, length, index))
    elif _sw2 == WMA:
        return _fdiv(pine_wma(atrwotmpBuffer, length, index), pine_wma(atrwoBuffer, length, index))
    return EMPTY_VALUE

def atrwo(open, close, high, low, length=14, stdev_length=100, stdev_mult=1.0, index=0):
    atrwoBuffer[index] = 0.0
    trwoBuffer[index] = 0.0
    ta_trBuffer[index] = MathMax(high[index] - low[index], MathAbs(high[index] - close[index + 1]))
    ta_trBuffer[index] = MathMax(ta_trBuffer[index], MathAbs(low[index] - close[index + 1]))
    max_tr = atrwoBuffer[index + 1] + (stdev_mult * pine_stdev(ta_trBuffer, stdev_length, index))
    trwoBuffer[index] = (trwoBuffer[index + 1] if (ta_trBuffer[index] > max_tr) else ta_trBuffer[index])
    atrwoBuffer[index] = pine_rma(trwoBuffer, RMA3Buffer, length, index)

def pine_stdev(src, length, index):
    avg = pine_sma(src, length, index)
    sumOfSquareDeviations = 0.0
    for i in range(index, index + length):
        sum_ = src[i] - avg
        sumOfSquareDeviations = sumOfSquareDeviations + (sum_ * sum_)
    return MathSqrt(_fdiv(sumOfSquareDeviations, length))

def pine_sma(src, length, index):
    sum_ = 0.0
    for i in range(index, index + length):
        sum_ = sum_ + _fdiv(src[i], length)
    return sum_

def pine_ema(src, out, length, index):
    alpha = _fdiv(2.0, 1 + length)
    out[index] = (out[index + 1] * (1 - alpha)) + (src[index] * alpha)
    return out[index]

def pine_rma(src, out, length, index):
    alpha = _fdiv(1.0, length)
    out[index] = (out[index + 1] * (1 - alpha)) + (src[index] * alpha)
    return out[index]

def pine_wma(src, length, index):
    norm = 0.0
    sum_ = 0.0
    for i in range(index, index + length):
        weight = (length - i + index) * length
        norm = norm + weight
        sum_ = sum_ + (src[i] * weight)
    return _fdiv(sum_, norm)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRMAs(_MQL5Indicator):
    name = 'ATR_MAs'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        '_length': 8,
        '_type': _Choice({0: 'ATRWSMA', 1: 'ATRWEMA', 2: 'ATRWRMA', 3: 'ATRWWMA'}, default=1),
        '_atr_length': 14,
        '_stdev_length': 100,
        '_stdev_mult': 1.0,
    }

