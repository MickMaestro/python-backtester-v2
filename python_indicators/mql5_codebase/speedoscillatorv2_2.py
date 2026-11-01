"""SpeedOscillatorv2.2 — converted from MQL5: MQL5 Indicators/Speed Oscillator/SpeedOscillatorv2.2.mq5

Copyright: Copyright 2021, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SO'}, 'levels': [], 'description': [], 'name': 'SpeedOscillatorv2.2', 'source': 'MQL5 Indicators/Speed Oscillator/SpeedOscillatorv2.2.mq5', 'folder': 'Speed Oscillator', 'inputs': [{'mql': 'InpMAperiod', 'py': 'InpMAperiod', 'param': 'InpMAperiod', 'type': 'int', 'default': 24, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMAmethod', 'py': 'InpMAmethod', 'param': 'InpMAmethod', 'type': 'int', 'default': 0, 'label': 'MA mode', 'sinput': False}, {'mql': 'InpSPeriod', 'py': 'InpSPeriod', 'param': 'InpSPeriod', 'type': 'int', 'default': 170, 'label': 'Speed averaging-period (positive and negative)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMAperiod = _input('InpMAperiod', 24)  # MA period
InpMAmethod = _input('InpMAmethod', MODE_SMA)  # MA mode
InpSPeriod = _input('InpSPeriod', 170)  # Speed averaging-period (positive and negative)
AvgPosBuffer = Arr(0, 0.0)
AvgNegBuffer = Arr(0, 0.0)
SO = Arr(0, 0.0)
ExtMABuffer = Arr(0, 0.0)
ExtMAHandle = 0

def OnInit():
    global ExtMAHandle
    SetIndexBuffer(0, SO, INDICATOR_DATA)
    SetIndexBuffer(1, AvgPosBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, AvgNegBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtMABuffer, INDICATOR_CALCULATIONS)
    ExtMAHandle = iMA(None, 0, InpMAperiod, 0, InpMAmethod, PRICE_CLOSE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < InpSPeriod:
        return 0
    if False:
        return 0
    if CopyBuffer(ExtMAHandle, 0, 0, rates_total, ExtMABuffer) <= 0:
        Print('getting ExtMAHandle is failed! Error ', GetLastError())
        return 0
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
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SpeedOscillatorv22(_MQL5Indicator):
    name = 'SpeedOscillatorv2.2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMAperiod': 24,  # MA period
        'InpMAmethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA mode
        'InpSPeriod': 170,  # Speed averaging-period (positive and negative)
    }

