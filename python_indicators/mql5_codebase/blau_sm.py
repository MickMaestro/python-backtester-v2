"""Blau_SM — converted from MQL5: MQL5 Indicators/Blau_SM/Blau_SM.mq5

William Blau Stochastic Momentum
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'BSMomentum'}, 'levels': [], 'description': ['William Blau Stochastic Momentum'], 'name': 'Blau_SM', 'source': 'MQL5 Indicators/Blau_SM/Blau_SM.mq5', 'folder': 'Blau_SM', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 2, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodSmooth1', 'py': 'InpPeriodSmooth1', 'param': 'InpPeriodSmooth1', 'type': 'uint', 'default': 20, 'label': 'First smoothing period', 'sinput': False}, {'mql': 'InpPeriodSmooth2', 'py': 'InpPeriodSmooth2', 'param': 'InpPeriodSmooth2', 'type': 'uint', 'default': 5, 'label': 'Second smoothing period', 'sinput': False}, {'mql': 'InpPeriodSmooth3', 'py': 'InpPeriodSmooth3', 'param': 'InpPeriodSmooth3', 'type': 'uint', 'default': 3, 'label': 'Third smoothing period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 2)  # Period
InpPeriodSmooth1 = _input('InpPeriodSmooth1', 20)  # First smoothing period
InpPeriodSmooth2 = _input('InpPeriodSmooth2', 5)  # Second smoothing period
InpPeriodSmooth3 = _input('InpPeriodSmooth3', 3)  # Third smoothing period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferBSM = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferHH = Arr(0, 0.0)
BufferEMA1 = Arr(0, 0.0)
BufferEMA2 = Arr(0, 0.0)
period_ind = 0
period_sm1 = 0
period_sm2 = 0
period_sm3 = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ind, period_sm1, period_sm2, period_sm3
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm1 = (2 if (InpPeriodSmooth1 < 2) else InpPeriodSmooth1)
    period_sm2 = (2 if (InpPeriodSmooth2 < 2) else InpPeriodSmooth2)
    period_sm3 = (2 if (InpPeriodSmooth3 < 2) else InpPeriodSmooth3)
    SetIndexBuffer(0, BufferBSM, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferHH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferEMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferEMA2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BSMomentum(' + _str(period_ind) + ',' + _str(period_sm1) + ',' + _str(period_sm2) + ',' + _str(period_sm3) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferBSM, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferHH, True)
    ArraySetAsSeries(BufferEMA1, True)
    ArraySetAsSeries(BufferEMA2, True)
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
        ArrayInitialize(BufferBSM, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferHH, 0)
        ArrayInitialize(BufferEMA1, 0)
        ArrayInitialize(BufferEMA2, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        bl = Lowest(period_ind, i)
        bh = Highest(period_ind, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = low[bl]
        max_ = high[bh]
        BufferHH[i] = BufferMA[i] - ((max_ + min_) / 2.0)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferHH, BufferEMA1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm2, BufferEMA1, BufferEMA2)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm3, BufferEMA2, BufferBSM)
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


class BlauSM(_MQL5Indicator):
    name = 'Blau_SM'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 2,  # Period
        'InpPeriodSmooth1': 20,  # First smoothing period
        'InpPeriodSmooth2': 5,  # Second smoothing period
        'InpPeriodSmooth3': 3,  # Third smoothing period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

