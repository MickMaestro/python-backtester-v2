"""Simple_Support_Resistance — converted from MQL5: MQL5 Indicators/Simple_Support_Resistance/Simple_Support_Resistance.mq5

Simple Support/Resistance indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Resistance', 2: 'Support'}, 'levels': [], 'description': ['Simple Support/Resistance indicator'], 'name': 'Simple_Support_Resistance', 'source': 'MQL5 Indicators/Simple_Support_Resistance/Simple_Support_Resistance.mq5', 'folder': 'Simple_Support_Resistance', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 15, 'label': 'Period', 'sinput': False}, {'mql': 'InpBarsBefore', 'py': 'InpBarsBefore', 'param': 'InpBarsBefore', 'type': 'uint', 'default': 50, 'label': 'Lines length', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 15)  # Period
InpBarsBefore = _input('InpBarsBefore', 50)  # Lines length
BufferRes = Arr(0, 0.0)
BufferSup = Arr(0, 0.0)
period = 0
bars_before = 0

def OnInit():
    global bars_before, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    bars_before = (2 if (InpBarsBefore < 2) else InpBarsBefore)
    SetIndexBuffer(0, BufferRes, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSup, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Support/Resistance(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferRes, True)
    ArraySetAsSeries(BufferSup, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period or rates_total < bars_before:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferRes, EMPTY_VALUE)
        ArrayInitialize(BufferSup, EMPTY_VALUE)
    bl = Lowest(period, 1)
    bh = Highest(period, 1)
    if bl == WRONG_VALUE or bh == WRONG_VALUE:
        return 0
    min_ = low[bl]
    max_ = high[bh]
    Sup = (2 * min_) - max_
    Res = (2 * max_) - min_
    for i in range(0, bars_before):
        BufferRes[i] = Res
        BufferSup[i] = Sup
    BufferRes[bars_before] = EMPTY_VALUE
    BufferSup[bars_before] = EMPTY_VALUE
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMinimum(array) + start
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SimpleSupportResistance(_MQL5Indicator):
    name = 'Simple_Support_Resistance'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriod': 15,  # Period
        'InpBarsBefore': 50,  # Lines length
    }

