"""Murreys_Math_Oscillator — converted from MQL5: MQL5 Indicators/Murreys_Math_Oscillator/Murreys_Math_Oscillator.mq5

Murreys Math Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [65280, 8388352, 3329330, 32768, 1262987, 1993170, 9221330, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Murreys Math'}, 'levels': [], 'description': ['Murreys Math Oscillator'], 'name': 'Murreys_Math_Oscillator', 'source': 'MQL5 Indicators/Murreys_Math_Oscillator/Murreys_Math_Oscillator.mq5', 'folder': 'Murreys_Math_Oscillator', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 100, 'label': 'Period', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 0.125, 'label': 'Multiplier', 'sinput': False}, {'mql': 'InpShowLevels', 'py': 'InpShowLevels', 'param': 'InpShowLevels', 'type': 'int', 'default': 1, 'label': 'Show levels', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 100)  # Period
InpMultiplier = _input('InpMultiplier', 0.125)  # Multiplier
InpShowLevels = _input('InpShowLevels', INPUT_YES)  # Show levels
BufferMMO = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
multiplier = 0.0
level_2 = 0.0
level_4 = 0.0
level_6 = 0.0
level_8 = 0.0
period = 0

def OnInit():
    global level_2, level_4, level_6, level_8, multiplier, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    multiplier = (0 if (InpMultiplier < 0) else InpMultiplier)
    level_2 = 2 * multiplier
    level_4 = 4 * multiplier
    level_6 = 6 * multiplier
    level_8 = 8 * multiplier
    SetIndexBuffer(0, BufferMMO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Murreys Math oscillator (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, (8 if InpShowLevels else 0))
    if InpShowLevels:
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, level_8)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, level_6)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, level_4)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, level_2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, -level_2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 5, -level_4)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 6, -level_6)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 7, -level_8)
    ArraySetAsSeries(BufferMMO, True)
    ArraySetAsSeries(BufferColors, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferMMO, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        bl = Lowest(period, i)
        bh = Highest(period, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = low[bl]
        max_ = high[bh]
        range_ = max_ - min_
        mid = min_ + (multiplier * range_ * 4.0)
        BufferMMO[i] = (_fdiv(2.0 * (close[i] - mid), range_) if (range_ != 0) else 0)
        if BufferMMO[i] > 0:
            BufferColors[i] = 0.0
            if BufferMMO[i] >= level_6:
                BufferColors[i] = 3.0
            else:
                if BufferMMO[i] >= level_4:
                    BufferColors[i] = 2.0
                else:
                    if BufferMMO[i] >= level_2:
                        BufferColors[i] = 1.0
        else:
            BufferColors[i] = 4.0
            if BufferMMO[i] <= (-level_6):
                BufferColors[i] = 7.0
            else:
                if BufferMMO[i] <= (-level_4):
                    BufferColors[i] = 6.0
                else:
                    if BufferMMO[i] <= (-level_2):
                        BufferColors[i] = 5.0
    return rates_total

def Highest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MurreysMathOscillator(_MQL5Indicator):
    name = 'Murreys_Math_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 100,  # Period
        'InpMultiplier': 0.125,  # Multiplier
        'InpShowLevels': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show levels
    }

