"""Wilder_ATR — converted from MQL5: MQL5 Indicators/Wilder_ATR/Wilder_ATR.mq5

Wilder ATR indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Wilder ATR'}, 'levels': [], 'description': ['Wilder ATR indicator'], 'name': 'Wilder_ATR', 'source': 'MQL5 Indicators/Wilder_ATR/Wilder_ATR.mq5', 'folder': 'Wilder_ATR', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
BufferWATR = Arr(0, 0.0)
BufferTR = Arr(0, 0.0)
period_sm = 0
weight_sum = 0

def OnInit():
    global period_sm
    period_sm = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferWATR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Wilder ATR (' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferWATR, True)
    ArraySetAsSeries(BufferTR, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_sm, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferWATR, EMPTY_VALUE)
        ArrayInitialize(BufferTR, 0)
    for i in range(limit, 0 - 1, -1):
        hl = high[i] - low[i]
        hc = fabs(high[i] - close[i + 1])
        lc = fabs(low[i] - close[i + 1])
        BufferTR[i] = fmax(hl, fmax(hc, lc))
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        return ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferTR, BufferWATR)
    elif _sw1 == MODE_SMMA:
        return SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferTR, BufferWATR)
    elif _sw1 == MODE_LWMA:
        return LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm, BufferTR, BufferWATR, _GlobRef(globals(), 'weight_sum'))
    else:
        return SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferTR, BufferWATR)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WilderATR(_MQL5Indicator):
    name = 'Wilder_ATR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
    }

