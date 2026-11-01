"""IDayIIndex — converted from MQL5: MQL5 Indicators/IDayIIndex/IDayIIndex.mq5

Intraday Intensity Index
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [32768]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'IDIndex'}, 'levels': [], 'description': ['Intraday Intensity Index'], 'name': 'IDayIIndex', 'source': 'MQL5 Indicators/IDayIIndex/IDayIIndex.mq5', 'folder': 'IDayIIndex', 'inputs': [{'mql': 'InpNormal', 'py': 'InpNormal', 'param': 'InpNormal', 'type': 'int', 'default': 1, 'label': 'Normalized', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 21, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpNormal = _input('InpNormal', INPUT_YES)  # Normalized
InpPeriod = _input('InpPeriod', 21)  # Period
BufferIDI = Arr(0, 0.0)
BufferRaw = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferIDI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRaw, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'IDayII(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferIDI, True)
    ArraySetAsSeries(BufferRaw, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    limit1 = limit
    if limit > 1:
        limit = rates_total - 1
        limit1 = limit - period
        ArrayInitialize(BufferIDI, EMPTY_VALUE)
        ArrayInitialize(BufferRaw, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        value = high[i] - low[i]
        BufferRaw[i] = ((_fdiv((2 * close[i]) - high[i] - low[i], value) * tick_volume[i]) if (value != 0) else 0)
    for i in range(limit1, 0 - 1, -1):
        summ_idi = ArraySum(BufferRaw, i)
        if InpNormal:
            BufferIDI[i] = summ_idi
        else:
            summ_vol = float(ArraySum(tick_volume, i))
            BufferIDI[i] = _fdiv(summ_idi, summ_vol) * 100
    return rates_total

def ArraySum(array, index):
    summation = 0
    for i in range(period, 0 - 1, -1):
        summation += array[i + index]
    return summation


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IDayIIndex(_MQL5Indicator):
    name = 'IDayIIndex'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpNormal': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Normalized
        'InpPeriod': 21,  # Period
    }

