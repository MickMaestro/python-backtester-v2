"""Blau_Candlestick_Index — converted from MQL5: MQL5 Indicators/Blau_Candlestick_Index/Blau_Candlestick_Index.mq5

William Blau Candlestick Index
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 13, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [8721863]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'BCIndex'}, 'levels': [], 'description': ['William Blau Candlestick Index'], 'name': 'Blau_Candlestick_Index', 'source': 'MQL5 Indicators/Blau_Candlestick_Index/Blau_Candlestick_Index.mq5', 'folder': 'Blau_Candlestick_Index', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 1, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpPeriodSmooth1', 'py': 'InpPeriodSmooth1', 'param': 'InpPeriodSmooth1', 'type': 'uint', 'default': 20, 'label': 'First smoothing period', 'sinput': False}, {'mql': 'InpPeriodSmooth2', 'py': 'InpPeriodSmooth2', 'param': 'InpPeriodSmooth2', 'type': 'uint', 'default': 5, 'label': 'Second smoothing period', 'sinput': False}, {'mql': 'InpPeriodSmooth3', 'py': 'InpPeriodSmooth3', 'param': 'InpPeriodSmooth3', 'type': 'uint', 'default': 3, 'label': 'Third smoothing period', 'sinput': False}, {'mql': 'InpLevelUP', 'py': 'InpLevelUP', 'param': 'InpLevelUP', 'type': 'double', 'default': 25.0, 'label': 'Upper level', 'sinput': False}, {'mql': 'InpLevelDN', 'py': 'InpLevelDN', 'param': 'InpLevelDN', 'type': 'double', 'default': 25.0, 'label': 'Lower level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 1)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpPeriodSmooth1 = _input('InpPeriodSmooth1', 20)  # First smoothing period
InpPeriodSmooth2 = _input('InpPeriodSmooth2', 5)  # Second smoothing period
InpPeriodSmooth3 = _input('InpPeriodSmooth3', 3)  # Third smoothing period
InpLevelUP = _input('InpLevelUP', 25.0)  # Upper level
InpLevelDN = _input('InpLevelDN', 25.0)  # Lower level
BufferCI = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferMAA1 = Arr(0, 0.0)
BufferMAA2 = Arr(0, 0.0)
BufferMAA3 = Arr(0, 0.0)
BufferCM = Arr(0, 0.0)
BufferCMMA1 = Arr(0, 0.0)
BufferCMMA2 = Arr(0, 0.0)
BufferCMMA3 = Arr(0, 0.0)
BufferMinMax = Arr(0, 0.0)
BufferMinMaxMA1 = Arr(0, 0.0)
BufferMinMaxMA2 = Arr(0, 0.0)
BufferMinMaxMA3 = Arr(0, 0.0)
level_up = 0.0
level_dn = 0.0
period_ind = 0
period_sm1 = 0
period_sm2 = 0
period_sm3 = 0
handle_ma = 0

def OnInit():
    global handle_ma, level_dn, level_up, period_ind, period_sm1, period_sm2, period_sm3
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm1 = (2 if (InpPeriodSmooth1 < 2) else InpPeriodSmooth1)
    period_sm2 = (2 if (InpPeriodSmooth2 < 2) else InpPeriodSmooth2)
    period_sm3 = (2 if (InpPeriodSmooth3 < 2) else InpPeriodSmooth3)
    level_up = (0.1 if (InpLevelUP < 0.1) else InpLevelUP)
    level_dn = ((-InpLevelDN) if (InpLevelDN > 0) else -0.1 if (InpLevelDN > -0.1) else InpLevelDN)
    SetIndexBuffer(0, BufferCI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMAA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMAA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMAA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferCM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferCMMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferCMMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferCMMA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferMinMax, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferMinMaxMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferMinMaxMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferMinMaxMA3, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BCSI(' + _str(period_ind) + ',' + _str(period_sm1) + ',' + _str(period_sm2) + ',' + _str(period_sm3) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, level_up)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, level_dn)
    ArraySetAsSeries(BufferCI, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferMAA1, True)
    ArraySetAsSeries(BufferMAA2, True)
    ArraySetAsSeries(BufferMAA3, True)
    ArraySetAsSeries(BufferCM, True)
    ArraySetAsSeries(BufferCMMA1, True)
    ArraySetAsSeries(BufferCMMA2, True)
    ArraySetAsSeries(BufferCMMA3, True)
    ArraySetAsSeries(BufferMinMax, True)
    ArraySetAsSeries(BufferMinMaxMA1, True)
    ArraySetAsSeries(BufferMinMaxMA2, True)
    ArraySetAsSeries(BufferMinMaxMA3, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ind:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ind - 1
        ArrayInitialize(BufferCI, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferMAA1, 0)
        ArrayInitialize(BufferMAA2, 0)
        ArrayInitialize(BufferMAA3, 0)
        ArrayInitialize(BufferCM, 0)
        ArrayInitialize(BufferCMMA1, 0)
        ArrayInitialize(BufferCMMA2, 0)
        ArrayInitialize(BufferCMMA3, 0)
        ArrayInitialize(BufferMinMax, 0)
        ArrayInitialize(BufferMinMaxMA1, 0)
        ArrayInitialize(BufferMinMaxMA2, 0)
        ArrayInitialize(BufferMinMaxMA3, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferCM[i] = BufferMA[i] - BufferMA[i + period_ind]
        bl = Lowest(period_ind, i)
        bh = Highest(period_ind, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = low[bl]
        max_ = high[bh]
        BufferMinMax[i] = max_ - min_
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferCM, BufferCMMA1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferMinMax, BufferMinMaxMA1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm2, BufferCMMA1, BufferCMMA2)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm2, BufferMinMaxMA1, BufferMinMaxMA2)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm3, BufferCMMA2, BufferCMMA3)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm3, BufferMinMaxMA2, BufferMinMaxMA3)
    for i in range(limit, 0 - 1, -1):
        BufferCI[i] = _fdiv(100.0 * BufferCMMA3[i], (BufferMinMaxMA3[i] if (BufferMinMaxMA3[i] != 0) else DBL_MIN))
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


class BlauCandlestickIndex(_MQL5Indicator):
    name = 'Blau_Candlestick_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 1,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpPeriodSmooth1': 20,  # First smoothing period
        'InpPeriodSmooth2': 5,  # Second smoothing period
        'InpPeriodSmooth3': 3,  # Third smoothing period
        'InpLevelUP': 25.0,  # Upper level
        'InpLevelDN': 25.0,  # Lower level
    }

