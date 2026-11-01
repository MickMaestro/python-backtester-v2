"""Candle_Code — converted from MQL5: MQL5 Indicators/Candle_Code/Candle_Code.mq5

Candle Codes indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 11, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [32768], 2: [255], 3: [11119017]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'One smoothing', 2: 'Two smoothing', 3: 'Weights Data'}, 'levels': [], 'description': ['Candle Codes indicator'], 'name': 'Candle_Code', 'source': 'MQL5 Indicators/Candle_Code/Candle_Code.mq5', 'folder': 'Candle_Code', 'inputs': [{'mql': 'InpWeightBodySize', 'py': 'InpWeightBodySize', 'param': 'InpWeightBodySize', 'type': 'int', 'default': 32, 'label': 'Body size weight', 'sinput': False}, {'mql': 'InpWeightUpperShadow', 'py': 'InpWeightUpperShadow', 'param': 'InpWeightUpperShadow', 'type': 'int', 'default': 16, 'label': 'Upper shadow weight', 'sinput': False}, {'mql': 'InpWeightLowerShadow', 'py': 'InpWeightLowerShadow', 'param': 'InpWeightLowerShadow', 'type': 'int', 'default': 16, 'label': 'Lower shadow weight', 'sinput': False}, {'mql': 'InpWeightDirection', 'py': 'InpWeightDirection', 'param': 'InpWeightDirection', 'type': 'int', 'default': 32, 'label': 'Candle direction weight', 'sinput': False}, {'mql': 'InpWeightGap', 'py': 'InpWeightGap', 'param': 'InpWeightGap', 'type': 'int', 'default': 8, 'label': 'Gap weight', 'sinput': False}, {'mql': 'InpShowData', 'py': 'InpShowData', 'param': 'InpShowData', 'type': 'int', 'default': 0, 'label': 'Show data', 'sinput': False}, {'mql': 'InpPeriodMA1', 'py': 'InpPeriodMA1', 'param': 'InpPeriodMA1', 'type': 'uint', 'default': 21, 'label': 'First MA period', 'sinput': False}, {'mql': 'InpMethodMA1', 'py': 'InpMethodMA1', 'param': 'InpMethodMA1', 'type': 'int', 'default': 0, 'label': 'First MA method', 'sinput': False}, {'mql': 'InpPeriodMA2', 'py': 'InpPeriodMA2', 'param': 'InpPeriodMA2', 'type': 'uint', 'default': 3, 'label': 'Second MA period', 'sinput': False}, {'mql': 'InpMethodMA2', 'py': 'InpMethodMA2', 'param': 'InpMethodMA2', 'type': 'int', 'default': 0, 'label': 'Second MA method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_WEIGHTS
WEIGHT_0 = 0
WEIGHT_1 = 1
WEIGHT_2 = 2
WEIGHT_4 = 4
WEIGHT_8 = 8
WEIGHT_16 = 16
WEIGHT_32 = 32
WEIGHT_64 = 64
WEIGHT_128 = 128
WEIGHT_256 = 256
WEIGHT_512 = 512
_enum('ENUM_WEIGHTS', {0: 'WEIGHT_0', 1: 'WEIGHT_1', 2: 'WEIGHT_2', 4: 'WEIGHT_4', 8: 'WEIGHT_8', 16: 'WEIGHT_16', 32: 'WEIGHT_32', 64: 'WEIGHT_64', 128: 'WEIGHT_128', 256: 'WEIGHT_256', 512: 'WEIGHT_512'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpWeightBodySize = _input('InpWeightBodySize', WEIGHT_32)  # Body size weight
InpWeightUpperShadow = _input('InpWeightUpperShadow', WEIGHT_16)  # Upper shadow weight
InpWeightLowerShadow = _input('InpWeightLowerShadow', WEIGHT_16)  # Lower shadow weight
InpWeightDirection = _input('InpWeightDirection', WEIGHT_32)  # Candle direction weight
InpWeightGap = _input('InpWeightGap', WEIGHT_8)  # Gap weight
InpShowData = _input('InpShowData', INPUT_NO)  # Show data
InpPeriodMA1 = _input('InpPeriodMA1', 21)  # First MA period
InpMethodMA1 = _input('InpMethodMA1', MODE_SMA)  # First MA method
InpPeriodMA2 = _input('InpPeriodMA2', 3)  # Second MA period
InpMethodMA2 = _input('InpMethodMA2', MODE_SMA)  # Second MA method
BufferOne = Arr(0, 0.0)
BufferTwo = Arr(0, 0.0)
BufferRaw = Arr(0, 0.0)
BufferRawBody = Arr(0, 0.0)
BufferRawUpper = Arr(0, 0.0)
BufferRawLower = Arr(0, 0.0)
BufferRawGap = Arr(0, 0.0)
BufferOpen = Arr(0, 0.0)
BufferHigh = Arr(0, 0.0)
BufferLow = Arr(0, 0.0)
BufferClose = Arr(0, 0.0)
period_ma1 = 0
period_ma2 = 0
handle_open = 0
handle_high = 0
handle_low = 0
handle_close = 0
weight_sum = 0

def OnInit():
    global handle_close, handle_high, handle_low, handle_open, period_ma1, period_ma2
    period_ma1 = (2 if (InpPeriodMA1 < 2) else InpPeriodMA1)
    period_ma2 = (2 if (InpPeriodMA2 < 2) else InpPeriodMA2)
    SetIndexBuffer(0, BufferOne, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTwo, INDICATOR_DATA)
    SetIndexBuffer(2, BufferRaw, INDICATOR_DATA)
    SetIndexBuffer(3, BufferRawBody, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferRawUpper, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferRawLower, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferRawGap, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferOpen, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferHigh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferLow, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferClose, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, (DRAW_LINE if InpShowData else DRAW_NONE))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Candle Codes (weights: ' + _str(InpWeightBodySize) + ',' + _str(InpWeightUpperShadow) + ',' + _str(InpWeightLowerShadow) + ',' + _str(InpWeightDirection) + ',' + _str(InpWeightGap) + ', periods: ' + _str(period_ma1) + ',' + _str(period_ma2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferOne, True)
    ArraySetAsSeries(BufferTwo, True)
    ArraySetAsSeries(BufferRaw, True)
    ArraySetAsSeries(BufferRawBody, True)
    ArraySetAsSeries(BufferRawUpper, True)
    ArraySetAsSeries(BufferRawLower, True)
    ArraySetAsSeries(BufferRawGap, True)
    ArraySetAsSeries(BufferOpen, True)
    ArraySetAsSeries(BufferHigh, True)
    ArraySetAsSeries(BufferLow, True)
    ArraySetAsSeries(BufferClose, True)
    ResetLastError()
    handle_open = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_OPEN)
    if handle_open == INVALID_HANDLE:
        Print('The iMA(1) by PRICE_OPEN object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_high = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_HIGH)
    if handle_high == INVALID_HANDLE:
        Print('The iMA(1) by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_low = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_LOW)
    if handle_low == INVALID_HANDLE:
        Print('The iMA(1) by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_close = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_CLOSE)
    if handle_close == INVALID_HANDLE:
        Print('The iMA(1) by PRICE_CLOSE object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferOne, EMPTY_VALUE)
        ArrayInitialize(BufferTwo, EMPTY_VALUE)
        ArrayInitialize(BufferRaw, EMPTY_VALUE)
        ArrayInitialize(BufferRawBody, 0)
        ArrayInitialize(BufferRawUpper, 0)
        ArrayInitialize(BufferRawLower, 0)
        ArrayInitialize(BufferRawGap, 0)
        ArrayInitialize(BufferOpen, 0)
        ArrayInitialize(BufferHigh, 0)
        ArrayInitialize(BufferLow, 0)
        ArrayInitialize(BufferClose, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_open, 0, 0, count, BufferOpen)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_high, 0, 0, count, BufferHigh)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_low, 0, 0, count, BufferLow)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_close, 0, 0, count, BufferClose)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferRawBody[i] = fabs(BufferClose[i] - BufferOpen[i])
        BufferRawUpper[i] = BufferHigh[i] - fmax(BufferClose[i], BufferOpen[i])
        BufferRawLower[i] = fmin(BufferClose[i], BufferOpen[i]) - BufferLow[i]
        BufferRawGap[i] = BufferOpen[i] - BufferClose[i + 1]
    AvgShadow = (SMAOnArray(BufferRawLower, 0, rates_total - 2, 0, 0) + SMAOnArray(BufferRawUpper, 0, rates_total - 2, 0, 0)) / 2.0
    AvgBodySize = SMAOnArray(BufferRawBody, 0, rates_total - 2, 0, 0)
    AvgGap = SMAOnArray(BufferRawGap, 0, rates_total - 2, 0, 0)
    BodySize = 0.0
    UpperShadow = 0.0
    LowerShadow = 0.0
    Gap = 0.0
    Direction = 0.0
    for i in range(limit, 0 - 1, -1):
        BodySize = (InpWeightBodySize if (fabs(BufferClose[i] - BufferOpen[i]) >= (AvgBodySize * 2.0)) else _fdiv(InpWeightBodySize * fabs(BufferClose[i] - BufferOpen[i]), 2.0 * AvgBodySize))
        UpperShadow = (InpWeightUpperShadow if ((BufferHigh[i] - fmax(BufferClose[i], BufferOpen[i])) >= (AvgShadow * 2.0)) else _fdiv(InpWeightUpperShadow * (BufferHigh[i] - fmax(BufferClose[i], BufferOpen[i])), 2.0 * AvgShadow))
        LowerShadow = (InpWeightLowerShadow if ((fmin(BufferClose[i], BufferOpen[i]) - BufferLow[i]) >= (AvgShadow * 2.0)) else _fdiv(InpWeightLowerShadow * (fmin(BufferClose[i], BufferOpen[i]) - BufferLow[i]), 2.0 * AvgShadow))
        Gap = _fdiv(InpWeightGap * (BufferOpen[i] - BufferClose[i + 1]), AvgGap)
        Direction = (InpWeightDirection if (BufferClose[i] > BufferOpen[i]) else (-1.0 * InpWeightDirection) if (BufferClose[i] < BufferOpen[i]) else 0)
        BufferRaw[i] = Direction + BodySize + UpperShadow + LowerShadow + Gap
    _sw1 = InpMethodMA1
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_ma1, period_ma1, BufferRaw, BufferOne)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_ma1, period_ma1, BufferRaw, BufferOne)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ma1, period_ma1, BufferRaw, BufferOne, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ma1, BufferRaw, BufferOne)
    _sw2 = InpMethodMA2
    if _sw2 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_ma1, period_ma2, BufferOne, BufferTwo)
    elif _sw2 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_ma1, period_ma2, BufferOne, BufferTwo)
    elif _sw2 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ma1, period_ma2, BufferOne, BufferTwo, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_ma1, period_ma2, BufferOne, BufferTwo)
    return rates_total

def SMAOnArray(array, total, period, ma_shift, shift):
    buf = Arr(0, 0.0)
    arr = Arr(0, 0.0)
    if total == 0:
        total = ArraySize(array)
    if total > 0 and total <= period:
        return 0.0
    if shift > (total - period - ma_shift):
        return 0.0
    total = ArrayCopy(arr, array, 0, shift + ma_shift, period)
    if ArrayResize(buf, total) < 0:
        return 0.0
    sum_ = 0.0
    i = 0
    pos = total - 1
    i = 1
    while i < period:
        sum_ += arr[pos]
        i += 1
        pos -= 1
    while pos >= 0:
        sum_ += arr[pos]
        buf[pos] = _fdiv(sum_, period)
        sum_ -= arr[pos + period - 1]
        pos -= 1
    return buf[0]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleCode(_MQL5Indicator):
    name = 'Candle_Code'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpWeightBodySize': _Choice({0: '0', 1: '1', 2: '2', 4: '4', 8: '8', 16: '16', 32: '32', 64: '64', 128: '128', 256: '256', 512: '512'}, default=32),  # Body size weight
        'InpWeightUpperShadow': _Choice({0: '0', 1: '1', 2: '2', 4: '4', 8: '8', 16: '16', 32: '32', 64: '64', 128: '128', 256: '256', 512: '512'}, default=16),  # Upper shadow weight
        'InpWeightLowerShadow': _Choice({0: '0', 1: '1', 2: '2', 4: '4', 8: '8', 16: '16', 32: '32', 64: '64', 128: '128', 256: '256', 512: '512'}, default=16),  # Lower shadow weight
        'InpWeightDirection': _Choice({0: '0', 1: '1', 2: '2', 4: '4', 8: '8', 16: '16', 32: '32', 64: '64', 128: '128', 256: '256', 512: '512'}, default=32),  # Candle direction weight
        'InpWeightGap': _Choice({0: '0', 1: '1', 2: '2', 4: '4', 8: '8', 16: '16', 32: '32', 64: '64', 128: '128', 256: '256', 512: '512'}, default=8),  # Gap weight
        'InpShowData': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show data
        'InpPeriodMA1': 21,  # First MA period
        'InpMethodMA1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # First MA method
        'InpPeriodMA2': 3,  # Second MA period
        'InpMethodMA2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Second MA method
    }

