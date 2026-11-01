"""Buying_Selling_Pressure — converted from MQL5: MQL5 Indicators/Buying_Selling_Pressure/Buying_Selling_Pressure.mq5

Buying/Selling Pressure indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [32768], 2: [255], 3: [16711680], 4: [8421504], 5: [65280], 6: [4678655]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'BP', 2: 'SP', 3: 'PT', 4: 'PS', 5: 'SBP', 6: 'SSP'}, 'levels': [], 'description': ['Buying/Selling Pressure indicator'], 'name': 'Buying_Selling_Pressure', 'source': 'MQL5 Indicators/Buying_Selling_Pressure/Buying_Selling_Pressure.mq5', 'folder': 'Buying_Selling_Pressure', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodSM', 'py': 'InpPeriodSM', 'param': 'InpPeriodSM', 'type': 'uint', 'default': 4, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpMethodSM', 'py': 'InpMethodSM', 'param': 'InpMethodSM', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'InpType1', 'py': 'InpType1', 'param': 'InpType1', 'type': 'int', 'default': 3, 'label': 'Pressure filter', 'sinput': False}, {'mql': 'InpType2', 'py': 'InpType2', 'param': 'InpType2', 'type': 'int', 'default': 2, 'label': 'Smoothing filter', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_FILTER_TYPE_1
FILTER1_BOTH = 0
FILTER1_BUYING = 1
FILTER1_SELLING = 2
FILTER1_PREVALVING = 3
_enum('ENUM_FILTER_TYPE_1', {0: 'FILTER1_BOTH', 1: 'FILTER1_BUYING', 2: 'FILTER1_SELLING', 3: 'FILTER1_PREVALVING'})

# enum ENUM_FILTER_TYPE_2
FILTER2_BOTH = 0
FILTER2_UNSMOOTHED = 1
FILTER2_SMOOTHED = 2
_enum('ENUM_FILTER_TYPE_2', {0: 'FILTER2_BOTH', 1: 'FILTER2_UNSMOOTHED', 2: 'FILTER2_SMOOTHED'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpPeriodSM = _input('InpPeriodSM', 4)  # Smoothing period
InpMethodSM = _input('InpMethodSM', 0)  # Smoothing method
InpType1 = _input('InpType1', 3)  # Pressure filter
InpType2 = _input('InpType2', 2)  # Smoothing filter
BufferBP = Arr(0, 0.0)
BufferSP = Arr(0, 0.0)
BufferPT = Arr(0, 0.0)
BufferPS = Arr(0, 0.0)
BufferSBP = Arr(0, 0.0)
BufferSSP = Arr(0, 0.0)
period_ma = 0
period_sm = 0
weight_sum_sbp = 0
weight_sum_ssp = 0

def OnInit():
    global period_ma, period_sm
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm = (2 if (InpPeriodSM < 2) else InpPeriodSM)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BSPressure (' + _str(period_ma) + ',' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    if InpType1 == FILTER1_BUYING or InpType1 == FILTER1_BOTH:
        if InpType2 == FILTER2_UNSMOOTHED or InpType2 == FILTER2_BOTH:
            SetIndexBuffer(0, BufferBP, INDICATOR_DATA)
            PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
            PlotIndexSetString(0, PLOT_LABEL, 'Buy Pressure')
        else:
            SetIndexBuffer(0, BufferBP, INDICATOR_DATA)
            PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
            PlotIndexSetString(0, PLOT_LABEL, 'Buy Pressure')
        if InpType2 == FILTER2_SMOOTHED or InpType2 == FILTER2_BOTH:
            SetIndexBuffer(4, BufferSBP, INDICATOR_DATA)
            PlotIndexSetInteger(4, PLOT_DRAW_TYPE, DRAW_LINE)
            PlotIndexSetString(4, PLOT_LABEL, 'Smooth BuyPrs')
        else:
            SetIndexBuffer(4, BufferSBP, INDICATOR_DATA)
            PlotIndexSetInteger(4, PLOT_DRAW_TYPE, DRAW_NONE)
            PlotIndexSetString(4, PLOT_LABEL, 'Smooth BuyPrs')
    else:
        SetIndexBuffer(0, BufferBP, INDICATOR_DATA)
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetString(0, PLOT_LABEL, 'Buy Pressure')
        SetIndexBuffer(4, BufferSBP, INDICATOR_DATA)
        PlotIndexSetInteger(4, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetString(4, PLOT_LABEL, 'Smooth BuyPrs')
    if InpType1 == FILTER1_SELLING or InpType1 == FILTER1_BOTH:
        if InpType2 == FILTER2_UNSMOOTHED or InpType2 == FILTER2_BOTH:
            SetIndexBuffer(1, BufferSP, INDICATOR_DATA)
            PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_LINE)
            PlotIndexSetString(1, PLOT_LABEL, 'Sell Pressure')
        else:
            SetIndexBuffer(1, BufferSP, INDICATOR_DATA)
            PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_NONE)
            PlotIndexSetString(1, PLOT_LABEL, 'Sell Pressure')
        if InpType2 == FILTER2_SMOOTHED or InpType2 == FILTER2_BOTH:
            SetIndexBuffer(5, BufferSSP, INDICATOR_DATA)
            PlotIndexSetInteger(5, PLOT_DRAW_TYPE, DRAW_LINE)
            PlotIndexSetString(5, PLOT_LABEL, 'Smooth SellPrs')
        else:
            SetIndexBuffer(5, BufferSSP, INDICATOR_DATA)
            PlotIndexSetInteger(5, PLOT_DRAW_TYPE, DRAW_NONE)
            PlotIndexSetString(5, PLOT_LABEL, 'Smooth SellPrs')
    else:
        SetIndexBuffer(1, BufferSP, INDICATOR_DATA)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetString(1, PLOT_LABEL, 'Sell Pressure')
        SetIndexBuffer(5, BufferSSP, INDICATOR_DATA)
        PlotIndexSetInteger(5, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetString(5, PLOT_LABEL, 'Smooth SellPrs')
    if InpType1 == FILTER1_PREVALVING or InpType1 == FILTER1_BOTH:
        if InpType2 == FILTER2_UNSMOOTHED or InpType2 == FILTER2_BOTH:
            SetIndexBuffer(2, BufferPT, INDICATOR_DATA)
            PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_LINE)
            PlotIndexSetString(2, PLOT_LABEL, 'Prevailing')
        else:
            SetIndexBuffer(2, BufferPT, INDICATOR_DATA)
            PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_NONE)
            PlotIndexSetString(2, PLOT_LABEL, 'Prevailing')
        if InpType2 == FILTER2_SMOOTHED or InpType2 == FILTER2_BOTH:
            SetIndexBuffer(3, BufferPS, INDICATOR_DATA)
            PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_LINE)
            PlotIndexSetString(3, PLOT_LABEL, 'Smooth Prv')
        else:
            SetIndexBuffer(3, BufferPS, INDICATOR_DATA)
            PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_NONE)
            PlotIndexSetString(3, PLOT_LABEL, 'Smooth Prv')
    else:
        SetIndexBuffer(2, BufferPT, INDICATOR_DATA)
        PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetString(2, PLOT_LABEL, 'Prevailing')
        SetIndexBuffer(3, BufferPS, INDICATOR_DATA)
        PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetString(3, PLOT_LABEL, 'Smooth Prv')
    ArraySetAsSeries(BufferBP, True)
    ArraySetAsSeries(BufferSP, True)
    ArraySetAsSeries(BufferPT, True)
    ArraySetAsSeries(BufferPS, True)
    ArraySetAsSeries(BufferSBP, True)
    ArraySetAsSeries(BufferSSP, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferBP, EMPTY_VALUE)
        ArrayInitialize(BufferSP, EMPTY_VALUE)
        ArrayInitialize(BufferPT, EMPTY_VALUE)
        ArrayInitialize(BufferPS, EMPTY_VALUE)
        ArrayInitialize(BufferSBP, EMPTY_VALUE)
        ArrayInitialize(BufferSSP, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferBP[i] = high[i] - open[i]
        BufferSP[i] = open[i] - low[i]
        BufferPT[i] = (BufferBP[i] if (BufferBP[i] > BufferSP[i]) else BufferSP[i])
    _sw1 = InpMethodSM
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferBP, BufferSBP) == 0:
            return 0
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferSP, BufferSSP) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferBP, BufferSBP) == 0:
            return 0
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferSP, BufferSSP) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm, BufferBP, BufferSBP, _GlobRef(globals(), 'weight_sum_sbp')) == 0:
            return 0
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm, BufferSP, BufferSSP, _GlobRef(globals(), 'weight_sum_ssp')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferBP, BufferSBP) == 0:
            return 0
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferSP, BufferSSP) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferPS[i] = (BufferSBP[i] if (BufferSBP[i] > BufferSSP[i]) else BufferSSP[i])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BuyingSellingPressure(_MQL5Indicator):
    name = 'Buying_Selling_Pressure'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpPeriodSM': 4,  # Smoothing period
        'InpMethodSM': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
        'InpType1': _Choice({0: 'Both pressures', 1: 'Buying pressure', 2: 'Selling pressure', 3: 'Prevailing pressure'}, default=3),  # Pressure filter
        'InpType2': _Choice({0: 'Both', 1: 'Only unsmoothed', 2: 'Only smoothed'}, default=2),  # Smoothing filter
    }

