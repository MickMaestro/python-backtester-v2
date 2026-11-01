"""DNC_Bandwidth — converted from MQL5: MQL5 Indicators/DNC_Bandwidth/DNC_Bandwidth.mq5

Donchian Channel Bandwidth indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [7451452]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'DNC Band Width'}, 'levels': [], 'description': ['Donchian Channel Bandwidth indicator'], 'name': 'DNC_Bandwidth', 'source': 'MQL5 Indicators/DNC_Bandwidth/DNC_Bandwidth.mq5', 'folder': 'DNC_Bandwidth', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpCurrentPeriod', 'py': 'InpCurrentPeriod', 'param': 'InpCurrentPeriod', 'type': 'int', 'default': 1, 'label': 'Analyze current bar', 'sinput': False}, {'mql': 'InpInPoints', 'py': 'InpInPoints', 'param': 'InpInPoints', 'type': 'int', 'default': 0, 'label': 'Data in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpCurrentPeriod = _input('InpCurrentPeriod', INPUT_YES)  # Analyze current bar
InpInPoints = _input('InpInPoints', INPUT_NO)  # Data in points
BufferWidth = Arr(0, 0.0)
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
size = 0.0
period = 0
shift = 0

def OnInit():
    global period, shift, size
    period = (1 if (InpPeriod < 1) else InpPeriod)
    shift = (0 if InpCurrentPeriod else 1)
    size = Point()
    SetIndexBuffer(0, BufferWidth, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTop, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferBottom, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Donchian Channel Bandwidth (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferWidth, True)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period, 4) or size == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferWidth, EMPTY_VALUE)
        ArrayInitialize(BufferTop, 0)
        ArrayInitialize(BufferBottom, 0)
    for i in range(limit, 0 - 1, -1):
        bh = Highest(period, i + shift)
        bl = Lowest(period, i + shift)
        if bh == WRONG_VALUE or bl == WRONG_VALUE:
            continue
        BufferTop[i] = high[bh]
        BufferBottom[i] = low[bl]
    for i in range(limit, 0 - 1, -1):
        BufferWidth[i] = (_fdiv(BufferTop[i] - BufferBottom[i], size) if InpInPoints else (BufferTop[i] - BufferBottom[i]))
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


class DNCBandwidth(_MQL5Indicator):
    name = 'DNC_Bandwidth'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpCurrentPeriod': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Analyze current bar
        'InpInPoints': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Data in points
    }

