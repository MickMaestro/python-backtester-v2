"""All_MA — converted from MQL5: MQL5 Indicators/Moving Averages-14 different types/All_MA.mq5

Copyright: Copyright 2022, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'MA'}, 'levels': [], 'description': [], 'name': 'All_MA', 'source': 'MQL5 Indicators/Moving Averages-14 different types/All_MA.mq5', 'folder': 'Moving Averages-14 different types', 'inputs': [{'mql': '_type', 'py': '_type', 'param': '_type', 'type': 'int', 'default': 12, 'label': 'MA Type:', 'sinput': False}, {'mql': '_length', 'py': '_length', 'param': '_length', 'type': 'int', 'default': 8, 'label': 'MA Period', 'sinput': False}, {'mql': '_offset', 'py': '_offset', 'param': '_offset', 'type': 'double', 'default': 0.85, 'label': 'Offset for ALMA', 'sinput': False}, {'mql': '_sigma', 'py': '_sigma', 'param': '_sigma', 'type': 'int', 'default': 6, 'label': 'Offset for LSMA / Sigma for ALMA', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum MA_TYPE
SMA = 0
EMA = 1
WMA = 2
VWMA = 3
RMA = 4
DEMA = 5
TEMA = 6
ZLEMA = 7
HMA = 8
ALMA = 9
LSMA = 10
SWMA = 11
SMMA = 12
DONCHIAN = 13
_enum('MA_TYPE', {0: 'SMA', 1: 'EMA', 2: 'WMA', 3: 'VWMA', 4: 'RMA', 5: 'DEMA', 6: 'TEMA', 7: 'ZLEMA', 8: 'HMA', 9: 'ALMA', 10: 'LSMA', 11: 'SWMA', 12: 'SMMA', 13: 'DONCHIAN'})

# ---- inputs and global variables
_type = _input('_type', SMMA)  # MA Type:
_length = _input('_length', 8)  # MA Period
_offset = _input('_offset', 0.85)  # Offset for ALMA
_sigma = _input('_sigma', 6)  # Offset for LSMA / Sigma for ALMA
EMABuffer = Arr(0, 0.0)
EMA2Buffer = Arr(0, 0.0)
EMA3Buffer = Arr(0, 0.0)
RMABuffer = Arr(0, 0.0)
DEMABuffer = Arr(0, 0.0)
TEMABuffer = Arr(0, 0.0)
zlematmpBuffer = Arr(0, 0.0)
ZLEMABuffer = Arr(0, 0.0)
MABuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, MABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, EMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, EMA2Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, EMA3Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, RMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, DEMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, TEMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, zlematmpBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, ZLEMABuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(EMABuffer, True)
    ArraySetAsSeries(EMA2Buffer, True)
    ArraySetAsSeries(EMA3Buffer, True)
    ArraySetAsSeries(RMABuffer, True)
    ArraySetAsSeries(DEMABuffer, True)
    ArraySetAsSeries(TEMABuffer, True)
    ArraySetAsSeries(zlematmpBuffer, True)
    ArraySetAsSeries(ZLEMABuffer, True)
    ArraySetAsSeries(MABuffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    for i in range(MathMax(rates_total - _length - prev_calculated, 1), 0 - 1, -1):
        MABuffer[i] = anyma(close, _length, _type, _offset, _sigma, i)
    return rates_total

def anyma(src, length, type_=EMA, offset=0.85, sigma=6, index=0):
    _sw1 = type_
    if _sw1 == SMA:
        return pine_sma(src, length, index)
    elif _sw1 == EMA:
        return pine_ema(src, length, index)
    elif _sw1 == WMA:
        return pine_wma(src, length, index)
    elif _sw1 == VWMA:
        return pine_vwma(src, length, index)
    elif _sw1 == RMA:
        return pine_rma(src, length, index)
    elif _sw1 == DEMA:
        return pine_dema(src, length, index)
    elif _sw1 == TEMA:
        return pine_tema(src, length, index)
    elif _sw1 == ZLEMA:
        return pine_zlema(src, length, index)
    elif _sw1 == HMA:
        return pine_hma(src, length, index)
    elif _sw1 == ALMA:
        return pine_alma(src, length, offset, sigma, index)
    elif _sw1 == LSMA:
        return pine_linreg(src, length, sigma, index)
    elif _sw1 == SWMA:
        return pine_swma(src, index)
    elif _sw1 == SMMA:
        return pine_rma(src, length, index)
    elif _sw1 == DONCHIAN:
        return pine_donchian(src, length, index)
    else:
        return EMPTY_VALUE

def pine_sma(src, length, index):
    sum_ = 0.0
    for i in range(index, index + length):
        sum_ = sum_ + _fdiv(src[i], length)
    return sum_

def pine_ema(src, length, index):
    alpha = _fdiv(2.0, 1 + length)
    EMABuffer[index] = (EMABuffer[index + 1] * (1 - alpha)) + (src[index] * alpha)
    return EMABuffer[index]

def pine_rma(src, length, index):
    alpha = _fdiv(1.0, length)
    RMABuffer[index] = (RMABuffer[index + 1] * (1 - alpha)) + (src[index] * alpha)
    return RMABuffer[index]

def pine_wma(src, length, index):
    norm = 0.0
    sum_ = 0.0
    for i in range(index, index + length):
        weight = (length - i + index) * length
        norm = norm + weight
        sum_ = sum_ + (src[i] * weight)
    return _fdiv(sum_, norm)

def pine_vwma(src, length, index):
    s1 = 0.0
    for i in range(index, index + length):
        s1 += _fdiv(src[i] * float(iVolume(Symbol(), PERIOD_CURRENT, i)), float(length))
    s2 = 0.0
    for i in range(index, index + length):
        s2 += _fdiv(float(iVolume(Symbol(), PERIOD_CURRENT, i)), length)
    return _fdiv(s1, s2)

def pine_dema(src, length, index):
    alpha = _fdiv(2.0, 1 + length)
    EMABuffer[index] = (EMABuffer[index + 1] * (1 - alpha)) + (src[index] * alpha)
    EMA2Buffer[index] = (EMA2Buffer[index + 1] * (1 - alpha)) + (EMABuffer[index] * alpha)
    DEMABuffer[index] = (2 * EMABuffer[index]) - EMA2Buffer[index]
    return DEMABuffer[index]

def pine_tema(src, length, index):
    alpha = _fdiv(2.0, 1 + length)
    EMABuffer[index] = (EMABuffer[index + 1] * (1 - alpha)) + (src[index] * alpha)
    EMA2Buffer[index] = (EMA2Buffer[index + 1] * (1 - alpha)) + (EMABuffer[index] * alpha)
    EMA3Buffer[index] = (EMA3Buffer[index + 1] * (1 - alpha)) + (EMA2Buffer[index] * alpha)
    TEMABuffer[index] = (3 * (EMABuffer[index] - EMA2Buffer[index])) + EMA3Buffer[index]
    return TEMABuffer[index]

def pine_zlema(src, length, index):
    zlematmpBuffer[index] = src[index] + (src[index] - src[index + _idiv(length, 2)])
    alpha = _fdiv(2.0, 1 + length)
    ZLEMABuffer[index] = (ZLEMABuffer[index + 1] * (1 - alpha)) + (zlematmpBuffer[index] * alpha)
    return ZLEMABuffer[index]

def pine_hma(src, length, index):
    norm = 0.0
    sum_ = 0.0
    i = index
    while i < (index + MathRound(MathSqrt(length))):
        weight = (MathRound(MathSqrt(length)) - (i - index)) * MathRound(MathSqrt(length))
        norm = norm + weight
        sum_ = sum_ + (((2 * pine_wma(src, _idiv(length, 2), index)) - pine_wma(src, length, index)) * weight)
        i += 1
    return _fdiv(sum_, norm)

def pine_alma(src, length, offset, sigma, index):
    m = MathFloor(offset * float(length - 1))
    s = _fdiv(float(length), sigma)
    norm = 0.0
    sum_ = 0.0
    for i in range(index, index + length):
        weight = MathExp(_fdiv(-1 * MathPow(i - index - m, 2), 2 * MathPow(s, 2)))
        norm = norm + weight
        sum_ = sum_ + (src[(2 * index) + length - i - 1] * weight)
    return _fdiv(sum_, norm)

def pine_linreg(input_src, _len, offset, index):
    sum_y = 0.0
    sum_x = 0.0
    sum_y2 = 0.0
    sum_x2 = 0.0
    sum_xy = 0.0
    for i in range(index, index + _len):
        sum_y += input_src[i]
        sum_x += i
        sum_y2 += input_src[i] * input_src[i]
        sum_x2 += i * i
        sum_xy += i * input_src[i]
    a = _fdiv((sum_y * sum_x2) - (sum_x * sum_xy), (_len * sum_x2) - (sum_x * sum_x))
    b = _fdiv((_len * sum_xy) - (sum_x * sum_y), (_len * sum_x2) - (sum_x * sum_x))
    return a + (b * (index + offset))

def pine_swma(src, index):
    return ((src[index + 3] * 1) / 6) + ((src[index + 2] * 2) / 6) + ((src[index + 1] * 2) / 6) + ((src[index + 0] * 1) / 6)

def pine_donchian(src, length, index):
    lowest = DBL_MAX
    for i in range(index, index + length):
        lowest = MathMin(src[i], lowest)
    highest = -DBL_MAX
    for i in range(index, index + length):
        highest = MathMax(src[i], highest)
    return (highest + lowest) / 2


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AllMA(_MQL5Indicator):
    name = 'All_MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        '_type': _Choice({0: 'SMA', 1: 'EMA', 2: 'WMA', 3: 'VWMA', 4: 'RMA', 5: 'DEMA', 6: 'TEMA', 7: 'ZLEMA', 8: 'HMA', 9: 'ALMA', 10: 'LSMA', 11: 'SWMA', 12: 'SMMA', 13: 'DONCHIAN'}, default=12),  # MA Type:
        '_length': 8,  # MA Period
        '_offset': 0.85,  # Offset for ALMA
        '_sigma': 6,  # Offset for LSMA / Sigma for ALMA
    }

