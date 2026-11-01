"""Blau_TS_Stochastic — converted from MQL5: MQL5 Indicators/Blau_TS_Stochastic/Blau_TS_Stochastic.mq5

William Blau Stochastic oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 12, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [15130800, 12180223, 13882323], 2: [255]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'BStochOSC', 2: 'Signal'}, 'levels': [], 'description': ['William Blau Stochastic oscillator'], 'name': 'Blau_TS_Stochastic', 'source': 'MQL5 Indicators/Blau_TS_Stochastic/Blau_TS_Stochastic.mq5', 'folder': 'Blau_TS_Stochastic', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 5, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodSmooth1', 'py': 'InpPeriodSmooth1', 'param': 'InpPeriodSmooth1', 'type': 'uint', 'default': 20, 'label': 'First smooth period', 'sinput': False}, {'mql': 'InpPeriodSmooth2', 'py': 'InpPeriodSmooth2', 'param': 'InpPeriodSmooth2', 'type': 'uint', 'default': 5, 'label': 'Second smooth period', 'sinput': False}, {'mql': 'InpPeriodSmooth3', 'py': 'InpPeriodSmooth3', 'param': 'InpPeriodSmooth3', 'type': 'uint', 'default': 3, 'label': 'Third smooth period', 'sinput': False}, {'mql': 'InpPeriodSignal', 'py': 'InpPeriodSignal', 'param': 'InpPeriodSignal', 'type': 'uint', 'default': 3, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 5)  # Period
InpPeriodSmooth1 = _input('InpPeriodSmooth1', 20)  # First smooth period
InpPeriodSmooth2 = _input('InpPeriodSmooth2', 5)  # Second smooth period
InpPeriodSmooth3 = _input('InpPeriodSmooth3', 3)  # Third smooth period
InpPeriodSignal = _input('InpPeriodSignal', 3)  # Signal period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferBStoch = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferSto = Arr(0, 0.0)
BufferSto_EMA1 = Arr(0, 0.0)
BufferSto_EMA2 = Arr(0, 0.0)
BufferSto_EMA3 = Arr(0, 0.0)
BufferHH = Arr(0, 0.0)
BufferHH_EMA1 = Arr(0, 0.0)
BufferHH_EMA2 = Arr(0, 0.0)
BufferHH_EMA3 = Arr(0, 0.0)
period_ind = 0
period_sm1 = 0
period_sm2 = 0
period_sm3 = 0
period_sig = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ind, period_sig, period_sm1, period_sm2, period_sm3
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm1 = (2 if (InpPeriodSmooth1 < 2) else InpPeriodSmooth1)
    period_sm2 = (2 if (InpPeriodSmooth2 < 2) else InpPeriodSmooth2)
    period_sm3 = (2 if (InpPeriodSmooth3 < 2) else InpPeriodSmooth3)
    period_sig = (2 if (InpPeriodSignal < 2) else InpPeriodSignal)
    SetIndexBuffer(0, BufferBStoch, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSto, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSto_EMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferSto_EMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferSto_EMA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferHH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferHH_EMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferHH_EMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferHH_EMA3, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BStochOsc(' + _str(period_ind) + ',' + _str(period_sm1) + ',' + _str(period_sm2) + ',' + _str(period_sm3) + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferBStoch, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferSto, True)
    ArraySetAsSeries(BufferSto_EMA1, True)
    ArraySetAsSeries(BufferSto_EMA2, True)
    ArraySetAsSeries(BufferSto_EMA3, True)
    ArraySetAsSeries(BufferHH, True)
    ArraySetAsSeries(BufferHH_EMA1, True)
    ArraySetAsSeries(BufferHH_EMA2, True)
    ArraySetAsSeries(BufferHH_EMA3, True)
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
        limit = rates_total - 2
        ArrayInitialize(BufferBStoch, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferSto, 0)
        ArrayInitialize(BufferSto_EMA1, 0)
        ArrayInitialize(BufferSto_EMA2, 0)
        ArrayInitialize(BufferSto_EMA3, 0)
        ArrayInitialize(BufferHH, 0)
        ArrayInitialize(BufferHH_EMA1, 0)
        ArrayInitialize(BufferHH_EMA2, 0)
        ArrayInitialize(BufferHH_EMA3, 0)
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
        BufferHH[i] = max_ - min_
        BufferSto[i] = BufferMA[i] - min_
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferHH, BufferHH_EMA1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferSto, BufferSto_EMA1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm2, BufferHH_EMA1, BufferHH_EMA2)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm2, BufferSto_EMA1, BufferSto_EMA2)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm3, BufferHH_EMA2, BufferHH_EMA3)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm3, BufferSto_EMA2, BufferSto_EMA3)
    for i in range(limit, 0 - 1, -1):
        HH_EMA3 = BufferHH_EMA3[i]
        Stoch_EMA3 = BufferSto_EMA3[i]
        BufferBStoch[i] = (_fdiv(100.0 * Stoch_EMA3, HH_EMA3) if (HH_EMA3 > 0) else 0)
        BufferColors[i] = (0 if (BufferBStoch[i] > BufferBStoch[i + 1]) else 1 if (BufferBStoch[i] < BufferBStoch[i + 1]) else 2)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferBStoch, BufferSignal)
    for i in range(limit, 0 - 1, -1):
        BufferColors[i] = (0 if (BufferBStoch[i] > BufferSignal[i + 1]) else 1 if (BufferBStoch[i] < BufferSignal[i + 1]) else 2)
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


class BlauTSStochastic(_MQL5Indicator):
    name = 'Blau_TS_Stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 5,  # Period
        'InpPeriodSmooth1': 20,  # First smooth period
        'InpPeriodSmooth2': 5,  # Second smooth period
        'InpPeriodSmooth3': 3,  # Third smooth period
        'InpPeriodSignal': 3,  # Signal period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

