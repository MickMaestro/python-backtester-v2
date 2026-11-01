"""TIA — converted from MQL5: MQL5 Indicators/TIA/TIA.mq5

Trend Interruption Average oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [32768], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'TIA Up', 2: 'TIA Down', 3: 'TIA Difference'}, 'levels': [], 'description': ['Trend Interruption Average oscillator'], 'name': 'TIA', 'source': 'MQL5 Indicators/TIA/TIA.mq5', 'folder': 'TIA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferDiff = Arr(0, 0.0)
BufferTmpUP = Arr(0, 0.0)
BufferTmpDN = Arr(0, 0.0)
period_sm = 0
weight_sum1 = 0
weight_sum2 = 0

def OnInit():
    global period_sm
    period_sm = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDiff, INDICATOR_DATA)
    SetIndexBuffer(3, BufferTmpUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferTmpDN, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TIA Oscillator (' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferDiff, True)
    ArraySetAsSeries(BufferTmpUP, True)
    ArraySetAsSeries(BufferTmpDN, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_sm, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_sm - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferDiff, EMPTY_VALUE)
        ArrayInitialize(BufferTmpUP, 0)
        ArrayInitialize(BufferTmpDN, 0)
    for i in range(limit, 0 - 1, -1):
        BufferTmpDN[i] = 0.0
        BufferTmpUP[i] = BufferTmpDN[i]
        if close[i] > close[i + 1]:
            BufferTmpUP[i] = BufferTmpUP[i + 1] + 1
            BufferTmpDN[i] = 0.0
        if close[i] < close[i + 1]:
            BufferTmpDN[i] = BufferTmpDN[i + 1] + 1
            BufferTmpUP[i] = 0.0
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferTmpUP, BufferUP) == 0:
            return 0
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferTmpDN, BufferDN) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferTmpUP, BufferUP) == 0:
            return 0
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferTmpDN, BufferDN) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm, BufferTmpUP, BufferUP, _GlobRef(globals(), 'weight_sum1')) == 0:
            return 0
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm, BufferTmpDN, BufferDN, _GlobRef(globals(), 'weight_sum2')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferTmpUP, BufferUP) == 0:
            return 0
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferTmpDN, BufferDN) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferDiff[i] = BufferUP[i] - BufferDN[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TIA(_MQL5Indicator):
    name = 'TIA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
    }

