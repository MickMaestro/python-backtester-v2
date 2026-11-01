"""Range_Volume_Ratio_S — converted from MQL5: MQL5 Indicators/Range_Volume_Ratio_S/Range_Volume_Ratio_S.mq5

Smoothed Range Volume Ratio oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [10526303, 2263842, 7504122], 2: [16711680]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'RV Ratio', 2: 'Signal'}, 'levels': [], 'description': ['Smoothed Range Volume Ratio oscillator'], 'name': 'Range_Volume_Ratio_S', 'source': 'MQL5 Indicators/Range_Volume_Ratio_S/Range_Volume_Ratio_S.mq5', 'folder': 'Range_Volume_Ratio_S', 'inputs': [{'mql': 'InpType', 'py': 'InpType', 'param': 'InpType', 'type': 'int', 'default': 0, 'label': 'Calculation type', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 15, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'MA Method', 'sinput': False}, {'mql': 'InpPrevBars', 'py': 'InpPrevBars', 'param': 'InpPrevBars', 'type': 'int', 'default': 1, 'label': 'Colors setting', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_TYPE_CALC
TYPE_OC = 0
TYPE_HL = 1
_enum('ENUM_TYPE_CALC', {0: 'TYPE_OC', 1: 'TYPE_HL'})

# enum ENUM_COLOR_SET
COLORS_PREV = 1
COLORS_ONE = 0
_enum('ENUM_COLOR_SET', {1: 'COLORS_PREV', 0: 'COLORS_ONE'})

# ---- inputs and global variables
InpType = _input('InpType', TYPE_OC)  # Calculation type
InpPeriod = _input('InpPeriod', 15)  # Period
InpMethod = _input('InpMethod', MODE_EMA)  # MA Method
InpPrevBars = _input('InpPrevBars', COLORS_PREV)  # Colors setting
BufferRVR = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
period_ind = 0
weight_sum = 0

def OnInit():
    global period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferRVR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSignal, INDICATOR_DATA)
    descr = ('High/Low' if (InpType == TYPE_HL) else 'Open/Close')
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoothed Range Volume Ratio ' + descr + ' (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    PlotIndexSetString(0, PLOT_LABEL, 'RVR ' + descr)
    PlotIndexSetString(1, PLOT_LABEL, 'Signal' + ' (' + _str(period_ind) + ')')
    ArraySetAsSeries(BufferRVR, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSignal, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferRVR, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, 0)
    for i in range(limit, 0 - 1, -1):
        BufferRVR[i] = (_fdiv((fabs(open[i] - close[i]) if (InpType == TYPE_OC) else (high[i] - low[i])), tick_volume[i] * Point()) if (tick_volume[i] != 0) else 0)
        BufferColors[i] = 0.0
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_ind, period_ind, BufferRVR, BufferSignal)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_ind, period_ind, BufferRVR, BufferSignal)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ind, period_ind, BufferRVR, BufferSignal, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_ind, period_ind, BufferRVR, BufferSignal)
    if InpPrevBars:
        for i in range(limit, 0 - 1, -1):
            BufferColors[i] = (1 if (BufferRVR[i + 1] > BufferSignal[i + 1]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RangeVolumeRatioS(_MQL5Indicator):
    name = 'Range_Volume_Ratio_S'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpType': _Choice({0: 'Open/Close', 1: 'High/Low'}, default=0),  # Calculation type
        'InpPeriod': 15,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA Method
        'InpPrevBars': _Choice({1: 'By previous bar position', 0: 'One color'}, default=1),  # Colors setting
    }

