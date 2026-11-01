"""SO — converted from MQL5: MQL5 Indicators/SpeeD Oscillator v2.3/SO.mq5

Copyright: Copyright 2021, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 2.30

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '2.30', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 3, 2: 1}, 'colors': {1: [16748574], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 2}, 'labels': {}, 'levels': [], 'description': [], 'name': 'SO', 'source': 'MQL5 Indicators/SpeeD Oscillator v2.3/SO.mq5', 'folder': 'SpeeD Oscillator v2.3', 'inputs': [{'mql': 'InpMAperiod', 'py': 'InpMAperiod', 'param': 'InpMAperiod', 'type': 'int', 'default': 100, 'label': 'Moving average period', 'sinput': False}, {'mql': 'InpMAmethod', 'py': 'InpMAmethod', 'param': 'InpMAmethod', 'type': 'int', 'default': 0, 'label': 'Moving average mode', 'sinput': False}, {'mql': 'InpSPeriod', 'py': 'InpSPeriod', 'param': 'InpSPeriod', 'type': 'int', 'default': 400, 'label': 'Backward-sampling period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMAperiod = _input('InpMAperiod', 100)  # Moving average period
InpMAmethod = _input('InpMAmethod', MODE_SMA)  # Moving average mode
InpSPeriod = _input('InpSPeriod', 400)  # Backward-sampling period
AvgPosBuffer = Arr(0, 0.0)
AvgNegBuffer = Arr(0, 0.0)
SO = Arr(0, 0.0)
ExtMABuffer = Arr(0, 0.0)
Distance = Arr(0, 0.0)
ExtMAHandle = 0

def OnInit():
    global ExtMAHandle
    SetIndexBuffer(0, SO, INDICATOR_DATA)
    SetIndexBuffer(1, Distance, INDICATOR_DATA)
    SetIndexBuffer(2, AvgPosBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, AvgNegBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtMABuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpSPeriod)
    ExtMAHandle = iMA(None, 0, InpMAperiod, 0, InpMAmethod, PRICE_CLOSE)
    PlotIndexSetString(0, PLOT_LABEL, 'Speed(' + _str(InpMAperiod) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'Distance(%)')
    IndicatorSetString(INDICATOR_SHORTNAME, 'SO(' + _str(InpMAperiod) + ')')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if CopyBuffer(ExtMAHandle, 0, 0, rates_total - 1, ExtMABuffer) <= 0:
        Print('not all MA copied. Will try on next tick Error =', GetLastError())
        return 0
    if prev_calculated == 0:
        ArrayInitialize(AvgPosBuffer, 0)
        ArrayInitialize(AvgNegBuffer, 0)
        ArrayInitialize(SO, 0)
    i = 0
    pos_count = 0
    neg_count = 0
    pos_sum = 0.0
    neg_sum = 0.0
    j = 1
    if prev_calculated == 0:
        i = InpSPeriod + 1
        for i in range(i, rates_total):
            pos_count = 0
            neg_count = 0
            pos_sum = 0.0
            neg_sum = 0.0
            j = i
            while (pos_count < InpSPeriod or neg_count < InpSPeriod) and j > 1:
                j -= 1
                diff = ExtMABuffer[j] - ExtMABuffer[j - 1]
                if diff > 0 and pos_count < InpSPeriod:
                    pos_count += 1
                    pos_sum += diff
                if diff < 0 and neg_count < InpSPeriod:
                    neg_count += 1
                    neg_sum += diff
            AvgPosBuffer[i] = pos_sum / InpSPeriod
            AvgNegBuffer[i] = neg_sum / InpSPeriod
            if (ExtMABuffer[i] - ExtMABuffer[i - 1]) > 0:
                SO[i] = _fdiv(ExtMABuffer[i] - ExtMABuffer[i - 1], AvgPosBuffer[i])
            elif (ExtMABuffer[i] - ExtMABuffer[i - 1]) < 0:
                SO[i] = -_fdiv(ExtMABuffer[i] - ExtMABuffer[i - 1], AvgNegBuffer[i])
            else:
                SO[i] = 0.0
            Distance[i] = _fdiv(close[i] - ExtMABuffer[i], close[i]) * 100
        else:
            i = _range_end(i, rates_total, 1)
    else:
        i = rates_total - 1
        for i in range(i, rates_total):
            pos_count = 0
            neg_count = 0
            pos_sum = 0.0
            neg_sum = 0.0
            j = i
            while (pos_count < InpSPeriod or neg_count < InpSPeriod) and j > 1:
                j -= 1
                diff = ExtMABuffer[j] - ExtMABuffer[j - 1]
                if diff > 0 and pos_count < InpSPeriod:
                    pos_count += 1
                    pos_sum += diff
                if diff < 0 and neg_count < InpSPeriod:
                    neg_count += 1
                    neg_sum += diff
            AvgPosBuffer[i] = pos_sum / InpSPeriod
            AvgNegBuffer[i] = neg_sum / InpSPeriod
            if (ExtMABuffer[i] - ExtMABuffer[i - 1]) > 0:
                SO[i] = _fdiv(ExtMABuffer[i] - ExtMABuffer[i - 1], AvgPosBuffer[i])
            elif (ExtMABuffer[i] - ExtMABuffer[i - 1]) < 0:
                SO[i] = -_fdiv(ExtMABuffer[i] - ExtMABuffer[i - 1], AvgNegBuffer[i])
            else:
                SO[i] = 0.0
        else:
            i = _range_end(i, rates_total, 1)
    Distance[rates_total - 1] = _fdiv(close[rates_total - 1] - ExtMABuffer[rates_total - 1], close[rates_total - 1]) * 100
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SOIndicator(_MQL5Indicator):
    name = 'SO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMAperiod': 100,  # Moving average period
        'InpMAmethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Moving average mode
        'InpSPeriod': 400,  # Backward-sampling period
    }

