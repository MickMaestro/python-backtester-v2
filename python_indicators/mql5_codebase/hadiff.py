"""haDiff — converted from MQL5: MQL5 Indicators/haDifference/haDiff.mq5

Heikin-Ashi Difference indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'HA Difference', 2: 'HA Signal'}, 'levels': [], 'description': ['Heikin-Ashi Difference indicator'], 'name': 'haDiff', 'source': 'MQL5 Indicators/haDifference/haDiff.mq5', 'folder': 'haDifference', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 3, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Signal Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 3)  # Signal period
InpMethod = _input('InpMethod', MODE_SMA)  # Signal Method
BufferDifference = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferOpen = Arr(0, 0.0)
BufferClose = Arr(0, 0.0)
period_ind = 0
weight_sum = 0

def OnInit():
    global period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferDifference, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferOpen, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferClose, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Heikin-Ashi Difference (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDifference, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferOpen, True)
    ArraySetAsSeries(BufferClose, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferDifference, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferOpen, 0)
        ArrayInitialize(BufferClose, 0)
    for i in range(limit, 0 - 1, -1):
        BufferOpen[i] = (BufferOpen[i + 1] + BufferClose[i + 1]) / 2.0
        BufferClose[i] = (open[i] + high[i] + low[i] + close[i]) / 4.0
        BufferDifference[i] = _fdiv(BufferClose[i] - BufferOpen[i], Point())
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_ind, period_ind, BufferDifference, BufferSignal)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_ind, period_ind, BufferDifference, BufferSignal)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ind, period_ind, BufferDifference, BufferSignal, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_ind, period_ind, BufferDifference, BufferSignal)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HaDiff(_MQL5Indicator):
    name = 'haDiff'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 3,  # Signal period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Signal Method
    }

