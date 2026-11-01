"""Toby_Crabel_NR_Pattern — converted from MQL5: MQL5 Indicators/Toby_Crabel_NR_Pattern/Toby_Crabel_NR_Pattern.mq5

Toby Crabel NR Pattern indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Wide Range Bar', 2: 'Narrow Range Bar'}, 'levels': [], 'description': ['Toby Crabel NR Pattern indicator'], 'name': 'Toby_Crabel_NR_Pattern', 'source': 'MQL5 Indicators/Toby_Crabel_NR_Pattern/Toby_Crabel_NR_Pattern.mq5', 'folder': 'Toby_Crabel_NR_Pattern', 'inputs': [{'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'NR Method', 'sinput': False}, {'mql': 'InpSample', 'py': 'InpSample', 'param': 'InpSample', 'type': 'uint', 'default': 2, 'label': 'Sample (NR Custom)', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period (NR Custom)', 'sinput': False}, {'mql': 'InpShowWide', 'py': 'InpShowWide', 'param': 'InpShowWide', 'type': 'int', 'default': 1, 'label': 'Show wide range bar', 'sinput': False}, {'mql': 'InpShowNarrow', 'py': 'InpShowNarrow', 'param': 'InpShowNarrow', 'type': 'int', 'default': 1, 'label': 'Show narrow range bar', 'sinput': False}, {'mql': 'InpExludeCurr', 'py': 'InpExludeCurr', 'param': 'InpExludeCurr', 'type': 'int', 'default': 1, 'label': 'Exclude current bar', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_NR_METHOD
METHOD_2NR = 0
METHOD_3NR = 1
METHOD_4NR = 2
METHOD_8NR = 3
METHOD_CUSTOM = 4
_enum('ENUM_NR_METHOD', {0: 'METHOD_2NR', 1: 'METHOD_3NR', 2: 'METHOD_4NR', 3: 'METHOD_8NR', 4: 'METHOD_CUSTOM'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpMethod = _input('InpMethod', METHOD_2NR)  # NR Method
InpSample = _input('InpSample', 2)  # Sample (NR Custom)
InpPeriod = _input('InpPeriod', 20)  # Period (NR Custom)
InpShowWide = _input('InpShowWide', INPUT_YES)  # Show wide range bar
InpShowNarrow = _input('InpShowNarrow', INPUT_YES)  # Show narrow range bar
InpExludeCurr = _input('InpExludeCurr', INPUT_YES)  # Exclude current bar
BufferWS = Arr(0, 0.0)
BufferNS = Arr(0, 0.0)
BufferHL = Arr(0, 0.0)
sample = 0
period = 0
period_max = 0
shift = 0

def OnInit():
    global period_max, shift
    SetSP(InpMethod)
    period_max = fmax(sample, period)
    shift = (1 if InpExludeCurr else 0)
    SetIndexBuffer(0, BufferWS, INDICATOR_DATA)
    SetIndexBuffer(1, BufferNS, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHL, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Toby Crabel NR Pattern')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferWS, True)
    ArraySetAsSeries(BufferNS, True)
    ArraySetAsSeries(BufferHL, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 1 - shift
        ArrayInitialize(BufferWS, EMPTY_VALUE)
        ArrayInitialize(BufferNS, EMPTY_VALUE)
        ArrayInitialize(BufferHL, 0)
    for i in range(limit, 0 - 1, -1):
        bl = Lowest(sample, i + shift)
        bh = Highest(sample, i + shift)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            return 0
        min_ = low[bl]
        max_ = high[bh]
        BufferHL[i + shift] = max_ - min_
    for i in range(limit, 0 - 1, -1):
        BufferNS[i + shift] = EMPTY_VALUE
        BufferWS[i + shift] = BufferNS[i + shift]
        bl = Lowest(period, i + shift)
        bh = Highest(period, i + shift)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            return 0
        min_ = BufferHL[bl]
        max_ = BufferHL[bh]
        if InpShowWide:
            BufferWS[i + shift] = (high[i + shift] if (max_ == BufferHL[i + shift]) else EMPTY_VALUE)
        if InpShowNarrow:
            BufferNS[i + shift] = (high[i + shift] if (min_ == BufferHL[i + shift]) else EMPTY_VALUE)
    return rates_total

def Highest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def SetSP(method):
    global period, sample
    _sw1 = method
    if _sw1 == METHOD_2NR:
        sample = 2
        period = 20
    elif _sw1 == METHOD_3NR:
        sample = 3
        period = 20
    elif _sw1 == METHOD_4NR:
        sample = 4
        period = 40
    elif _sw1 == METHOD_8NR:
        sample = 8
        period = 40
    else:
        sample = _int(InpSample)
        period = _int(InpPeriod)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TobyCrabelNRPattern(_MQL5Indicator):
    name = 'Toby_Crabel_NR_Pattern'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMethod': _Choice({0: '2NR', 1: '3NR', 2: '4NR', 3: '8NR', 4: 'Custom'}, default=0),  # NR Method
        'InpSample': 2,  # Sample (NR Custom)
        'InpPeriod': 20,  # Period (NR Custom)
        'InpShowWide': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show wide range bar
        'InpShowNarrow': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show narrow range bar
        'InpExludeCurr': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Exclude current bar
    }

