"""Blau_Stochastic_Index — converted from MQL5: MQL5 Indicators/Blau_Stochastic_Index/Blau_Stochastic_Index.mq5

Blau Stochastic Index oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711680, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'BStoIndexOsc'}, 'levels': [], 'description': ['Blau Stochastic Index oscillator'], 'name': 'Blau_Stochastic_Index', 'source': 'MQL5 Indicators/Blau_Stochastic_Index/Blau_Stochastic_Index.mq5', 'folder': 'Blau_Stochastic_Index', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodSmooth1', 'py': 'InpPeriodSmooth1', 'param': 'InpPeriodSmooth1', 'type': 'uint', 'default': 5, 'label': 'First smooth period', 'sinput': False}, {'mql': 'InpPeriodSmooth2', 'py': 'InpPeriodSmooth2', 'param': 'InpPeriodSmooth2', 'type': 'uint', 'default': 15, 'label': 'Second smooth period', 'sinput': False}, {'mql': 'InpPeriodSignal', 'py': 'InpPeriodSignal', 'param': 'InpPeriodSignal', 'type': 'uint', 'default': 10, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpPeriodSmooth1 = _input('InpPeriodSmooth1', 5)  # First smooth period
InpPeriodSmooth2 = _input('InpPeriodSmooth2', 15)  # Second smooth period
InpPeriodSignal = _input('InpPeriodSignal', 10)  # Signal period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
BufferHist = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferDiff = Arr(0, 0.0)
BufferDiff_MA1 = Arr(0, 0.0)
BufferDiff_MA2 = Arr(0, 0.0)
BufferDiff_MA3 = Arr(0, 0.0)
BufferRange = Arr(0, 0.0)
BufferRange_MA1 = Arr(0, 0.0)
BufferRange_MA2 = Arr(0, 0.0)
BufferRange_MA3 = Arr(0, 0.0)
period_ind = 0
period_sm1 = 0
period_sm2 = 0
period_sig = 0
weight_summ = 0

def OnInit():
    global period_ind, period_sig, period_sm1, period_sm2
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm1 = (2 if (InpPeriodSmooth1 < 2) else InpPeriodSmooth1)
    period_sm2 = (2 if (InpPeriodSmooth2 < 2) else InpPeriodSmooth2)
    period_sig = (2 if (InpPeriodSignal < 2) else InpPeriodSignal)
    SetIndexBuffer(0, BufferHist, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferDiff, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferDiff_MA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDiff_MA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferDiff_MA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferRange, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferRange_MA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferRange_MA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferRange_MA3, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BStoIndexOsc(' + _str(period_ind) + ',' + _str(period_sm1) + ',' + _str(period_sm2) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferHist, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferDiff, True)
    ArraySetAsSeries(BufferDiff_MA1, True)
    ArraySetAsSeries(BufferDiff_MA2, True)
    ArraySetAsSeries(BufferDiff_MA3, True)
    ArraySetAsSeries(BufferRange, True)
    ArraySetAsSeries(BufferRange_MA1, True)
    ArraySetAsSeries(BufferRange_MA2, True)
    ArraySetAsSeries(BufferRange_MA3, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ind:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferHist, EMPTY_VALUE)
        ArrayInitialize(BufferDiff, 0)
        ArrayInitialize(BufferDiff_MA1, 0)
        ArrayInitialize(BufferDiff_MA2, 0)
        ArrayInitialize(BufferDiff_MA3, 0)
        ArrayInitialize(BufferRange, 0)
        ArrayInitialize(BufferRange_MA1, 0)
        ArrayInitialize(BufferRange_MA2, 0)
        ArrayInitialize(BufferRange_MA3, 0)
    for i in range(limit, 0 - 1, -1):
        bl = Lowest(period_ind, i)
        bh = Highest(period_ind, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = low[bl]
        max_ = high[bh]
        BufferDiff[i] = close[i] - min_
        BufferRange[i] = max_ - min_
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferDiff, BufferDiff_MA1)
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferRange, BufferRange_MA1)
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm2, BufferDiff_MA1, BufferDiff_MA2)
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm2, BufferRange_MA1, BufferRange_MA2)
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferDiff_MA2, BufferDiff_MA3)
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferRange_MA2, BufferRange_MA3)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferDiff, BufferDiff_MA1)
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferRange, BufferRange_MA1)
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm2, BufferDiff_MA1, BufferDiff_MA2)
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm2, BufferRange_MA1, BufferRange_MA2)
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferDiff_MA2, BufferDiff_MA3)
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferRange_MA2, BufferRange_MA3)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm1, BufferDiff, BufferDiff_MA1, _GlobRef(globals(), 'weight_summ'))
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm1, BufferRange, BufferRange_MA1, _GlobRef(globals(), 'weight_summ'))
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm2, BufferDiff_MA1, BufferDiff_MA2, _GlobRef(globals(), 'weight_summ'))
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm2, BufferRange_MA1, BufferRange_MA2, _GlobRef(globals(), 'weight_summ'))
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sig, BufferDiff_MA2, BufferDiff_MA3, _GlobRef(globals(), 'weight_summ'))
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sig, BufferRange_MA2, BufferRange_MA3, _GlobRef(globals(), 'weight_summ'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferDiff, BufferDiff_MA1)
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferRange, BufferRange_MA1)
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm2, BufferDiff_MA1, BufferDiff_MA2)
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm2, BufferRange_MA1, BufferRange_MA2)
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferDiff_MA2, BufferDiff_MA3)
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferRange_MA2, BufferRange_MA3)
    for i in range(limit, 0 - 1, -1):
        BufferHist[i] = ((_fdiv(100.0 * BufferDiff_MA3[i], BufferRange_MA3[i]) - 50.0) if (BufferRange_MA3[i] != 0) else 0)
        BufferColors[i] = (1 if (BufferHist[i] < BufferHist[i + 1]) else 0)
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


class BlauStochasticIndex(_MQL5Indicator):
    name = 'Blau_Stochastic_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpPeriodSmooth1': 5,  # First smooth period
        'InpPeriodSmooth2': 15,  # Second smooth period
        'InpPeriodSignal': 10,  # Signal period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
    }

