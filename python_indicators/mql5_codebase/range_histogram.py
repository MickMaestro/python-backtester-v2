"""Range_Histogram — converted from MQL5: MQL5 Indicators/Range_Histogram/Range_Histogram.mq5

Range Histogram indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Range'}, 'levels': [], 'description': ['Range Histogram indicator'], 'name': 'Range_Histogram', 'source': 'MQL5 Indicators/Range_Histogram/Range_Histogram.mq5', 'folder': 'Range_Histogram', 'inputs': [{'mql': 'InpType', 'py': 'InpType', 'param': 'InpType', 'type': 'int', 'default': 0, 'label': 'Calculation type', 'sinput': False}, {'mql': 'InpSmoothing', 'py': 'InpSmoothing', 'param': 'InpSmoothing', 'type': 'int', 'default': 0, 'label': 'Smoothing', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_TYPE_CALC
TYPE_OC = 0
TYPE_HL = 1
_enum('ENUM_TYPE_CALC', {0: 'TYPE_OC', 1: 'TYPE_HL'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpType = _input('InpType', TYPE_OC)  # Calculation type
InpSmoothing = _input('InpSmoothing', INPUT_NO)  # Smoothing
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
BufferRange = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
BufferAVG = Arr(0, 0.0)
period_ind = 0
weight_sum = 0

def OnInit():
    global period_ind
    min_ = (2 if InpSmoothing else 1)
    period_ind = _int((min_ if (InpPeriod < min_) else InpPeriod))
    SetIndexBuffer(0, BufferRange, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferAVG, INDICATOR_CALCULATIONS)
    descr = ('Range High/Low' if (InpType == TYPE_HL) else 'Range Open/Close')
    IndicatorSetString(INDICATOR_SHORTNAME, descr + ' Histogram (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    PlotIndexSetString(0, PLOT_LABEL, descr)
    ArraySetAsSeries(BufferRange, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferRAW, True)
    ArraySetAsSeries(BufferAVG, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < period_ind:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferRange, EMPTY_VALUE)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferAVG, 0)
    for i in range(limit, 0 - 1, -1):
        BufferRAW[i] = ((high[i] - low[i]) if (InpType == TYPE_HL) else fabs(open[i] - close[i]))
    if InpSmoothing:
        _sw1 = InpMethod
        if _sw1 == MODE_EMA:
            ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferRAW, BufferAVG)
        elif _sw1 == MODE_SMMA:
            SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferRAW, BufferAVG)
        elif _sw1 == MODE_LWMA:
            LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ind, BufferRAW, BufferAVG, _GlobRef(globals(), 'weight_sum'))
        else:
            SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferRAW, BufferAVG)
    for i in range(limit, 0 - 1, -1):
        BufferRange[i] = (BufferAVG[i] if InpSmoothing else BufferRAW[i])
        BufferColors[i] = (1 if (BufferRange[i] < BufferRange[i + 1]) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RangeHistogram(_MQL5Indicator):
    name = 'Range_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpType': _Choice({0: 'Open/Close', 1: 'High/Low'}, default=0),  # Calculation type
        'InpSmoothing': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Smoothing
        'InpPeriod': 14,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
    }

