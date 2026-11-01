"""MPO — converted from MQL5: MQL5 Indicators/MPO/MPO.mq5

Midpoint Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Midpoint', 2: 'Signal'}, 'levels': [], 'description': ['Midpoint Oscillator'], 'name': 'MPO', 'source': 'MQL5 Indicators/MPO/MPO.mq5', 'folder': 'MPO', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 26, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 9, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 26)  # Period
InpPeriodSm = _input('InpPeriodSm', 9)  # Smoothing period
InpMethod = _input('InpMethod', MODE_SMA)  # Smoothing method
BufferMP = Arr(0, 0.0)
BufferSM = Arr(0, 0.0)
period_mp = 0
period_sm = 0
weight_sum = 0

def OnInit():
    global period_mp, period_sm
    period_mp = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm = (2 if (InpPeriodSm < 2) else InpPeriodSm)
    SetIndexBuffer(0, BufferMP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSM, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MPO (' + _str(period_mp) + ',' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMP, True)
    ArraySetAsSeries(BufferSM, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferMP, EMPTY_VALUE)
        ArrayInitialize(BufferSM, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        bl = Lowest(period_mp, i)
        bh = Highest(period_mp, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = low[bl]
        max_ = high[bh]
        BufferMP[i] = (_fdiv(100.0 * ((2.0 * close[i]) - max_ - min_), max_ - min_) if (max_ != min_) else 0)
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_mp, period_sm, BufferMP, BufferSM)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_mp, period_sm, BufferMP, BufferSM)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_mp, period_sm, BufferMP, BufferSM, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_mp, period_sm, BufferMP, BufferSM)
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MPO(_MQL5Indicator):
    name = 'MPO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 26,  # Period
        'InpPeriodSm': 9,  # Smoothing period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
    }

