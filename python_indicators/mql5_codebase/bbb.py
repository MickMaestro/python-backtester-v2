"""BBB — converted from MQL5: MQL5 Indicators/BBB/BBB.mq5

Bull And Bear Balance indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [11186720, 9662683, 12632256]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'BB Balance'}, 'levels': [], 'description': ['Bull And Bear Balance indicator'], 'name': 'BBB', 'source': 'MQL5 Indicators/BBB/BBB.mq5', 'folder': 'BBB', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 30, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpMethodSm', 'py': 'InpMethodSm', 'param': 'InpMethodSm', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpPeriodSm = _input('InpPeriodSm', 30)  # Smoothing period
InpMethodSm = _input('InpMethodSm', MODE_SMA)  # Smoothing method
BufferBBB = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferBull = Arr(0, 0.0)
BufferBear = Arr(0, 0.0)
BufferMaBull = Arr(0, 0.0)
BufferMaBear = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
period_ind = 0
period_sm = 0
weight_sum = 0

def OnInit():
    global period_ind, period_sm
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm = (2 if (InpPeriodSm < 2) else InpPeriodSm)
    SetIndexBuffer(0, BufferBBB, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferBull, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferBear, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMaBull, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMaBear, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferRAW, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bull And Bear Balance (' + _str(period_ind) + ',' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferBBB, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferBull, True)
    ArraySetAsSeries(BufferBear, True)
    ArraySetAsSeries(BufferMaBull, True)
    ArraySetAsSeries(BufferMaBear, True)
    ArraySetAsSeries(BufferRAW, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 2:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferBBB, EMPTY_VALUE)
        ArrayInitialize(BufferBull, 0)
        ArrayInitialize(BufferBear, 0)
        ArrayInitialize(BufferMaBull, 0)
        ArrayInitialize(BufferMaBear, 0)
        ArrayInitialize(BufferRAW, 0)
    for i in range(limit, 0 - 1, -1):
        BufferBull[i] = BullPower(i, open, high, low, close)
        BufferBear[i] = BearPower(i, open, high, low, close)
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferBull, BufferMaBull)
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferBear, BufferMaBear)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferBull, BufferMaBull)
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferBear, BufferMaBear)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ind, BufferBull, BufferMaBull, _GlobRef(globals(), 'weight_sum'))
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ind, BufferBear, BufferMaBear, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferBull, BufferMaBull)
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferBear, BufferMaBear)
    for i in range(limit, 0 - 1, -1):
        BufferRAW[i] = BufferMaBull[i] - BufferMaBear[i]
    _sw2 = InpMethodSm
    if _sw2 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_ind, period_sm, BufferRAW, BufferBBB)
    elif _sw2 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_ind, period_sm, BufferRAW, BufferBBB)
    elif _sw2 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ind, period_sm, BufferRAW, BufferBBB, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_ind, period_sm, BufferRAW, BufferBBB)
    for i in range(limit, 0 - 1, -1):
        BufferColors[i] = (0 if (BufferBBB[i] > 0) else 1 if (BufferBBB[i] < 0) else 0)
    return rates_total

def BearPower(index, open, high, low, close):
    Value = 0.0
    if close[index] < open[index]:
        if close[index + 1] > open[index]:
            Value = MathMax(close[index + 1] - open[index], high[index] - low[index])
        else:
            Value = high[index] - low[index]
    else:
        if close[index] > open[index]:
            if close[index + 1] > open[index]:
                Value = MathMax(close[index + 1] - low[index], high[index] - close[index])
            else:
                Value = MathMax(open[index] - low[index], high[index] - close[index])
        else:
            if (high[index] - close[index]) > (close[index] - low[index]):
                if close[index + 1] > open[index]:
                    Value = MathMax(close[index + 1] - open[index], high[index] - low[index])
                else:
                    Value = high[index] - low[index]
            else:
                if (high[index] - close[index]) < (close[index] - low[index]):
                    if close[index + 1] > open[index]:
                        Value = MathMax(close[index + 1] - low[index], high[index] - close[index])
                    else:
                        Value = open[index] - low[index]
                else:
                    if close[index + 1] > open[index]:
                        Value = MathMax(close[index + 1] - open[index], high[index] - low[index])
                    else:
                        if close[index + 1] < open[index]:
                            Value = MathMax(open[index] - low[index], high[index] - close[index])
                        else:
                            Value = high[index] - low[index]
    return Value

def BullPower(index, open, high, low, close):
    Value = 0.0
    if close[index] < open[index]:
        if close[index + 1] < open[index]:
            Value = MathMax(high[index] - close[index + 1], close[index] - low[index])
        else:
            Value = MathMax(high[index] - open[index], close[index] - low[index])
    else:
        if close[index] > open[index]:
            if close[index + 1] > open[index]:
                Value = high[index] - low[index]
            else:
                Value = MathMax(open[index] - close[index + 1], high[index] - low[index])
        else:
            if (high[index] - close[index]) > (close[index] - low[index]):
                if close[index + 1] < open[index]:
                    Value = MathMax(high[index] - close[index + 1], close[index] - low[index])
                else:
                    Value = high[index] - open[index]
            else:
                if (high[index] - close[index]) < (close[index] - low[index]):
                    if close[index + 1] > open[index]:
                        Value = high[index] - low[index]
                    else:
                        Value = MathMax(open[index] - close[index + 1], high[index] - low[index])
                else:
                    if close[index + 1] > open[index]:
                        Value = MathMax(high[index] - open[index], close[index] - low[index])
                    else:
                        if close[index + 1] < open[index]:
                            Value = MathMax(open[index] - close[index + 1], high[index] - low[index])
                        else:
                            Value = high[index] - low[index]
    return Value


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBB(_MQL5Indicator):
    name = 'BBB'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpPeriodSm': 30,  # Smoothing period
        'InpMethodSm': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
    }

