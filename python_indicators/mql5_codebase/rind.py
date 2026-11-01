"""RIND — converted from MQL5: MQL5 Indicators/RIND/RIND.mq5

\\"RIND\\": Range Indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [10061943]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'RIND'}, 'levels': [], 'description': ['\\"RIND\\": Range Indicator'], 'name': 'RIND', 'source': 'MQL5 Indicators/RIND/RIND.mq5', 'folder': 'RIND', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 3, 'label': 'Period', 'sinput': False}, {'mql': 'InpSmoothing', 'py': 'InpSmoothing', 'param': 'InpSmoothing', 'type': 'uint', 'default': 10, 'label': 'Smoothing', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}, {'mql': 'InpLevel0', 'py': 'InpLevel0', 'param': 'InpLevel0', 'type': 'double', 'default': 20.0, 'label': 'Level 1', 'sinput': False}, {'mql': 'InpLevel1', 'py': 'InpLevel1', 'param': 'InpLevel1', 'type': 'double', 'default': 30.0, 'label': 'Level 2', 'sinput': False}, {'mql': 'InpLevel2', 'py': 'InpLevel2', 'param': 'InpLevel2', 'type': 'double', 'default': 40.0, 'label': 'Level 3', 'sinput': False}, {'mql': 'InpLevel3', 'py': 'InpLevel3', 'param': 'InpLevel3', 'type': 'double', 'default': 50.0, 'label': 'Level 4', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 3)  # Period
InpSmoothing = _input('InpSmoothing', 10)  # Smoothing
InpMethod = _input('InpMethod', MODE_EMA)  # Method
InpLevel0 = _input('InpLevel0', 20.0)  # Level 1
InpLevel1 = _input('InpLevel1', 30.0)  # Level 2
InpLevel2 = _input('InpLevel2', 40.0)  # Level 3
InpLevel3 = _input('InpLevel3', 50.0)  # Level 4
BufferRIND = Arr(0, 0.0)
BufferRange = Arr(0, 0.0)
BufferValue = Arr(0, 0.0)
period_ind = 0
period_sm = 0
weight_sum = 0

def OnInit():
    global period_ind, period_sm
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm = (2 if (InpSmoothing < 2) else InpSmoothing)
    SetIndexBuffer(0, BufferRIND, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRange, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferValue, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Range Indicator (' + _str(period_ind) + ',' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, InpLevel0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, InpLevel1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, InpLevel2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, InpLevel3)
    ArraySetAsSeries(BufferRIND, True)
    ArraySetAsSeries(BufferRange, True)
    ArraySetAsSeries(BufferValue, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferRIND, EMPTY_VALUE)
        ArrayInitialize(BufferRange, 0)
        ArrayInitialize(BufferValue, 0)
    for i in range(limit, 0 - 1, -1):
        trueRange = fmax(high[i], close[i + 1]) - fmin(low[i], close[i + 1])
        BufferValue[i] = (_fdiv(trueRange, close[i] - close[i + 1]) if (close[i] > close[i + 1]) else trueRange)
    for i in range(limit, 0 - 1, -1):
        bl = ArrayMinimum(BufferValue, i, period_ind)
        bh = ArrayMaximum(BufferValue, i, period_ind)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = BufferValue[bl]
        max_ = BufferValue[bh]
        BufferRange[i] = (_fdiv(100.0 * (BufferValue[i] - min_), max_ - min_) if ((max_ - min_) > 0) else (100.0 * (BufferValue[i] - min_)))
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferRange, BufferRIND)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferRange, BufferRIND)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm, BufferRange, BufferRIND, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferRange, BufferRIND)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RIND(_MQL5Indicator):
    name = 'RIND'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 3,  # Period
        'InpSmoothing': 10,  # Smoothing
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Method
        'InpLevel0': 20.0,  # Level 1
        'InpLevel1': 30.0,  # Level 2
        'InpLevel2': 40.0,  # Level 3
        'InpLevel3': 50.0,  # Level 4
    }

