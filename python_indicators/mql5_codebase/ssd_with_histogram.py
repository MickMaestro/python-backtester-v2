"""SSD_With_Histogram — converted from MQL5: MQL5 Indicators/SSD_With_Histogram/SSD_With_Histogram.mq5

SSD with histogram indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [11186720], 2: [1993170], 3: [32768, 255]}, 'widths': {1: 1, 2: 1, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Stoch', 2: 'Signal', 3: 'Histogram'}, 'levels': [], 'description': ['SSD with histogram indicator'], 'name': 'SSD_With_Histogram', 'source': 'MQL5 Indicators/SSD_With_Histogram/SSD_With_Histogram.mq5', 'folder': 'SSD_With_Histogram', 'inputs': [{'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 5, 'label': '%K period', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 3, 'label': '%D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpPriceField', 'py': 'InpPriceField', 'param': 'InpPriceField', 'type': 'int', 'default': 0, 'label': 'Price field', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodK = _input('InpPeriodK', 5)  # %K period
InpPeriodD = _input('InpPeriodD', 3)  # %D period
InpSlowing = _input('InpSlowing', 3)  # Slowing
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpPriceField = _input('InpPriceField', STO_LOWHIGH)  # Price field
BufferK = Arr(0, 0.0)
BufferD = Arr(0, 0.0)
BufferH = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSTO = Arr(0, 0.0)
period_k = 0
period_d = 0
slowing = 0
weight_sum = 0
handle_sto = 0

def OnInit():
    global handle_sto, period_d, period_k, slowing
    period_k = (1 if (InpPeriodK < 1) else InpPeriodK)
    period_d = (1 if (InpPeriodD < 1) else InpPeriodD)
    slowing = (2 if (InpSlowing < 2) else InpSlowing)
    SetIndexBuffer(0, BufferK, INDICATOR_DATA)
    SetIndexBuffer(1, BufferD, INDICATOR_DATA)
    SetIndexBuffer(2, BufferH, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferSTO, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SSDH (' + _str(period_k) + ',' + _str(period_d) + ',' + _str(slowing) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferK, True)
    ArraySetAsSeries(BufferD, True)
    ArraySetAsSeries(BufferH, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSTO, True)
    ResetLastError()
    handle_sto = iStochastic(None, PERIOD_CURRENT, period_k, period_d, slowing, InpMethod, InpPriceField)
    if handle_sto == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k), ',', _str(period_d), ',', _str(slowing), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferK, 0)
        ArrayInitialize(BufferD, 0)
        ArrayInitialize(BufferH, 0)
        ArrayInitialize(BufferSTO, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_sto, SIGNAL_LINE, 0, count, BufferSTO)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferK[i] = BufferSTO[i] - 50.0
    SimpleMAOnBuffer(rates_total, prev_calculated, period_k + slowing, period_d, BufferK, BufferD)
    for i in range(limit, 0 - 1, -1):
        BufferH[i] = BufferK[i] - BufferD[i]
        BufferColors[i] = (1 if (BufferH[i] < BufferH[i + 1]) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SSDWithHistogram(_MQL5Indicator):
    name = 'SSD_With_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodK': 5,  # %K period
        'InpPeriodD': 3,  # %D period
        'InpSlowing': 3,  # Slowing
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpPriceField': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Price field
    }

