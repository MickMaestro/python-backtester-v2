"""Repulse — converted from MQL5: MQL5 Indicators/Repulse/Repulse.mq5

Repulse oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Repulse', 2: 'Signal'}, 'levels': [], 'description': ['Repulse oscillator'], 'name': 'Repulse', 'source': 'MQL5 Indicators/Repulse/Repulse.mq5', 'folder': 'Repulse', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 5, 'label': 'Repulse period', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 15, 'label': 'Signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 5)  # Repulse period
InpPeriod2 = _input('InpPeriod2', 15)  # Signal period
BufferRP1 = Arr(0, 0.0)
BufferRP2 = Arr(0, 0.0)
BufferPos1 = Arr(0, 0.0)
BufferNeg1 = Arr(0, 0.0)
BufferPos2 = Arr(0, 0.0)
BufferNeg2 = Arr(0, 0.0)
BufferPos1tmp = Arr(0, 0.0)
BufferNeg1tmp = Arr(0, 0.0)
BufferPos2tmp = Arr(0, 0.0)
BufferNeg2tmp = Arr(0, 0.0)
period1 = 0
period2 = 0

def OnInit():
    global period1, period2
    period1 = (1 if (InpPeriod1 < 1) else InpPeriod1)
    period2 = (1 if (InpPeriod2 < 1) else InpPeriod2)
    SetIndexBuffer(0, BufferRP1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRP2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferPos1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferNeg1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferPos2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferNeg2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferPos1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferNeg1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferPos2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferNeg2tmp, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Repulse(' + _str(period1) + ',' + _str(period2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferRP1, True)
    ArraySetAsSeries(BufferRP2, True)
    ArraySetAsSeries(BufferPos1, True)
    ArraySetAsSeries(BufferNeg1, True)
    ArraySetAsSeries(BufferPos2, True)
    ArraySetAsSeries(BufferNeg2, True)
    ArraySetAsSeries(BufferPos1tmp, True)
    ArraySetAsSeries(BufferNeg1tmp, True)
    ArraySetAsSeries(BufferPos2tmp, True)
    ArraySetAsSeries(BufferNeg2tmp, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4 or Point() == 0:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    max_ = fmax(period1, period2)
    if limit > 1:
        limit = rates_total - max_ - 1
        ArrayInitialize(BufferRP1, EMPTY_VALUE)
        ArrayInitialize(BufferRP2, EMPTY_VALUE)
        ArrayInitialize(BufferPos1, 0)
        ArrayInitialize(BufferNeg1, 0)
        ArrayInitialize(BufferPos2, 0)
        ArrayInitialize(BufferNeg2, 0)
        ArrayInitialize(BufferPos1tmp, 0)
        ArrayInitialize(BufferNeg1tmp, 0)
        ArrayInitialize(BufferPos2tmp, 0)
        ArrayInitialize(BufferNeg2tmp, 0)
    MinPrice = 0.0
    MaxPrice = 0.0
    bl = WRONG_VALUE
    bh = WRONG_VALUE
    for i in range(limit, 0 - 1, -1):
        if close[i] == 0:
            continue
        bl = Lowest(period1, i)
        bh = Highest(period1, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        MinPrice = low[bl]
        MaxPrice = high[bh]
        BufferPos1tmp[i] = _fdiv(100.0 * ((3.0 * close[i]) - (2.0 * MinPrice) - open[i]), close[i])
        BufferNeg1tmp[i] = _fdiv(100.0 * (open[i] + (2.0 * MaxPrice) - (3.0 * close[i])), close[i])
        bl = Lowest(period2, i)
        bh = Highest(period2, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        MinPrice = low[bl]
        MaxPrice = high[bh]
        BufferPos2tmp[i] = _fdiv(100.0 * ((3.0 * close[i]) - (2.0 * MinPrice) - open[i + period2]), close[i])
        BufferNeg2tmp[i] = _fdiv(100.0 * (open[i + period2] + (2.0 * MaxPrice) - (3.0 * close[i])), close[i])
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, 5 * period1, BufferPos1tmp, BufferPos1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, 5 * period1, BufferNeg1tmp, BufferNeg1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, 5 * period2, BufferPos2tmp, BufferPos2)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, 5 * period2, BufferNeg2tmp, BufferNeg2)
    for i in range(limit, 0 - 1, -1):
        BufferRP1[i] = _fdiv(BufferPos1[i] - BufferNeg1[i], Point())
        BufferRP2[i] = _fdiv(BufferPos2[i] - BufferNeg2[i], Point())
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMinimum(array) + start
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Repulse(_MQL5Indicator):
    name = 'Repulse'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 5,  # Repulse period
        'InpPeriod2': 15,  # Signal period
    }

