"""EMV — converted from MQL5: MQL5 Indicators/EMV/EMV.mq5

Arm's Ease of Movement Value
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'EMV', 2: 'Signal'}, 'levels': [], 'description': ["Arm's Ease of Movement Value"], 'name': 'EMV', 'source': 'MQL5 Indicators/EMV/EMV.mq5', 'folder': 'EMV', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
BufferEMV = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
period_ind = 0
weight_sum = 0

def OnInit():
    global period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferEMV, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'AEMV(' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferEMV, True)
    ArraySetAsSeries(BufferSignal, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4 or Point() == 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ind - 2
        ArrayInitialize(BufferEMV, 0)
        ArrayInitialize(BufferSignal, 0)
    for i in range(limit, 0 - 1, -1):
        V = float(tick_volume[i])
        HL0 = _fdiv(high[i] + low[i], 2.0 * Point())
        HL1 = _fdiv(high[i + 1] + low[i + 1], 2.0 * Point())
        BufferEMV[i] = (_fdiv(_fdiv((HL0 - HL1) * (high[i] - low[i]), V), Point()) if (V != 0) else 0)
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferEMV, BufferSignal)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferEMV, BufferSignal)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ind, BufferEMV, BufferSignal, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferEMV, BufferSignal)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EMV(_MQL5Indicator):
    name = 'EMV'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
    }

