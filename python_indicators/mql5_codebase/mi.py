"""MI — converted from MQL5: MQL5 Indicators/MI/MI.mq5

Mass Index (MI)
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13434880]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Mass IDX'}, 'levels': [], 'description': ['Mass Index (MI)'], 'name': 'MI', 'source': 'MQL5 Indicators/MI/MI.mq5', 'folder': 'MI', 'inputs': [{'mql': 'InpPeriodMA1', 'py': 'InpPeriodMA1', 'param': 'InpPeriodMA1', 'type': 'uint', 'default': 9, 'label': 'First smoothing period', 'sinput': False}, {'mql': 'InpPeriodMA2', 'py': 'InpPeriodMA2', 'param': 'InpPeriodMA2', 'type': 'uint', 'default': 9, 'label': 'Second smoothing period', 'sinput': False}, {'mql': 'InpPeriodSum', 'py': 'InpPeriodSum', 'param': 'InpPeriodSum', 'type': 'uint', 'default': 25, 'label': 'Resulting smoothing period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodMA1 = _input('InpPeriodMA1', 9)  # First smoothing period
InpPeriodMA2 = _input('InpPeriodMA2', 9)  # Second smoothing period
InpPeriodSum = _input('InpPeriodSum', 25)  # Resulting smoothing period
InpMethod = _input('InpMethod', MODE_EMA)  # Method
BufferMI = Arr(0, 0.0)
BufferRes = Arr(0, 0.0)
BufferHL = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferMA3 = Arr(0, 0.0)
period_ma1 = 0
period_ma2 = 0
period_sum = 0
weight_sum = 0

def OnInit():
    global period_ma1, period_ma2, period_sum
    period_ma1 = (2 if (InpPeriodMA1 < 2) else InpPeriodMA1)
    period_ma2 = (2 if (InpPeriodMA2 < 2) else InpPeriodMA2)
    period_sum = (2 if (InpPeriodSum < 2) else InpPeriodSum)
    SetIndexBuffer(0, BufferMI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferHL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferRes, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MI(' + _str(period_ma1) + ',' + _str(period_ma2) + ',' + _str(period_sum) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMI, True)
    ArraySetAsSeries(BufferHL, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferMA3, True)
    ArraySetAsSeries(BufferRes, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4 or Point() == 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferMI, EMPTY_VALUE)
        ArrayInitialize(BufferHL, 0)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
        ArrayInitialize(BufferMA3, 0)
        ArrayInitialize(BufferRes, 0)
    for i in range(limit, 0 - 1, -1):
        BufferHL[i] = high[i] - low[i]
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma1, BufferHL, BufferMA1)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ma1, BufferHL, BufferMA1)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ma1, BufferHL, BufferMA1, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ma1, BufferHL, BufferMA1)
    _sw2 = InpMethod
    if _sw2 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma2, BufferMA1, BufferMA2)
    elif _sw2 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ma2, BufferMA1, BufferMA2)
    elif _sw2 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ma2, BufferMA1, BufferMA2, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ma2, BufferMA1, BufferMA2)
    for i in range(limit, 0 - 1, -1):
        BufferRes[i] = _fdiv(BufferMA1[i], (BufferMA2[i] if (BufferMA2[i] != 0) else 1.0))
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sum, BufferRes, BufferMA3)
    for i in range(limit, 0 - 1, -1):
        BufferMI[i] = (BufferMA3[i] * period_sum) - 25.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MI(_MQL5Indicator):
    name = 'MI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA1': 9,  # First smoothing period
        'InpPeriodMA2': 9,  # Second smoothing period
        'InpPeriodSum': 25,  # Resulting smoothing period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Method
    }

