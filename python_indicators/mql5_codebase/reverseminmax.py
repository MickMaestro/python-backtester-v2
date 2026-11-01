"""ReverseMinMax — converted from MQL5: MQL5 Indicators/ReverseMinMax/ReverseMinMax.mq5

Reverse Min Max indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [255], 2: [32768], 3: [16711680], 4: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Reverse Min', 2: 'Reverse Max', 3: 'Min', 4: 'Max'}, 'levels': [], 'description': ['Reverse Min Max indicator'], 'name': 'ReverseMinMax', 'source': 'MQL5 Indicators/ReverseMinMax/ReverseMinMax.mq5', 'folder': 'ReverseMinMax', 'inputs': [{'mql': 'InpPeriodRev', 'py': 'InpPeriodRev', 'param': 'InpPeriodRev', 'type': 'uint', 'default': 5, 'label': 'Reverse period', 'sinput': False}, {'mql': 'InpShowMinMax', 'py': 'InpShowMinMax', 'param': 'InpShowMinMax', 'type': 'int', 'default': 0, 'label': 'Show Min/Max lines', 'sinput': False}, {'mql': 'InpPeriodMM', 'py': 'InpPeriodMM', 'param': 'InpPeriodMM', 'type': 'uint', 'default': 20, 'label': 'Min/Max period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodRev = _input('InpPeriodRev', 5)  # Reverse period
InpShowMinMax = _input('InpShowMinMax', INPUT_NO)  # Show Min/Max lines
InpPeriodMM = _input('InpPeriodMM', 20)  # Min/Max period
BufferRevMin = Arr(0, 0.0)
BufferRevMax = Arr(0, 0.0)
BufferMin = Arr(0, 0.0)
BufferMax = Arr(0, 0.0)
period_mm = 0
period_rev = 0

def OnInit():
    global period_mm, period_rev
    period_rev = (2 if (InpPeriodRev < 2) else InpPeriodRev)
    period_mm = (2 if (InpPeriodMM < 2) else InpPeriodMM)
    SetIndexBuffer(0, BufferRevMin, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRevMax, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMin, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMax, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Reverse Min Max (' + _str(period_rev) + ',' + _str(period_mm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferRevMin, True)
    ArraySetAsSeries(BufferRevMax, True)
    ArraySetAsSeries(BufferMin, True)
    ArraySetAsSeries(BufferMax, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferRevMin, EMPTY_VALUE)
        ArrayInitialize(BufferRevMax, EMPTY_VALUE)
        ArrayInitialize(BufferMin, EMPTY_VALUE)
        ArrayInitialize(BufferMax, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        highest_low = HighestLow(period_rev - 1, i + 1)
        lowest_high = LowestHigh(period_rev - 1, i + 1)
        if highest_low == WRONG_VALUE or lowest_high == WRONG_VALUE:
            continue
        BufferRevMax[i] = high[lowest_high]
        BufferRevMin[i] = low[highest_low]
        if InpShowMinMax:
            highest_high = HighestHigh(period_mm - 1, i + 1)
            lowest_low = LowestLow(period_mm - 1, i + 1)
            if highest_high == WRONG_VALUE or lowest_low == WRONG_VALUE:
                continue
            BufferMax[i] = high[highest_high]
            BufferMin[i] = low[lowest_low]
        else:
            BufferMax[i] = EMPTY_VALUE
            BufferMin[i] = EMPTY_VALUE
    return rates_total

def HighestHigh(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE

def HighestLow(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE

def LowestHigh(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMinimum(array) + start
    return WRONG_VALUE

def LowestLow(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMinimum(array) + start
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ReverseMinMax(_MQL5Indicator):
    name = 'ReverseMinMax'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRev': 5,  # Reverse period
        'InpShowMinMax': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show Min/Max lines
        'InpPeriodMM': 20,  # Min/Max period
    }

