"""Bands_Fill — converted from MQL5: MQL5 Indicators/Bands_Fill/Bands_Fill.mq5

Bands Fill indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 7}, 'colors': {1: [11186720], 2: [11186720], 3: [15130800, 12903679]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper BB', 2: 'Lower BB', 3: 'Cloud'}, 'levels': [], 'description': ['Bands Fill indicator'], 'name': 'Bands_Fill', 'source': 'MQL5 Indicators/Bands_Fill/Bands_Fill.mq5', 'folder': 'Bands_Fill', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 2.0, 'label': 'Deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpDeviation = _input('InpDeviation', 2.0)  # Deviation
BufferUpper = Arr(0, 0.0)
BufferLower = Arr(0, 0.0)
BufferCloud1 = Arr(0, 0.0)
BufferCloud2 = Arr(0, 0.0)
BufferBase = Arr(0, 0.0)
BufferTrigger = Arr(0, 0.0)
deviation = 0.0
period = 0
handle_bb = 0

def OnInit():
    global deviation, handle_bb, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    deviation = InpDeviation
    SetIndexBuffer(0, BufferUpper, INDICATOR_DATA)
    SetIndexBuffer(1, BufferLower, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCloud1, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCloud2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferBase, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferTrigger, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bands Fill (' + _str(period) + ',' + DoubleToString(deviation, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferUpper, True)
    ArraySetAsSeries(BufferLower, True)
    ArraySetAsSeries(BufferCloud1, True)
    ArraySetAsSeries(BufferCloud2, True)
    ArraySetAsSeries(BufferBase, True)
    ArraySetAsSeries(BufferTrigger, True)
    ResetLastError()
    handle_bb = iBands(None, PERIOD_CURRENT, period, 0, deviation, PRICE_CLOSE)
    if handle_bb == INVALID_HANDLE:
        Print('The iBands(', _str(period), ',', DoubleToString(deviation, 2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUpper, EMPTY_VALUE)
        ArrayInitialize(BufferLower, EMPTY_VALUE)
        ArrayInitialize(BufferCloud1, 0)
        ArrayInitialize(BufferCloud2, 0)
        ArrayInitialize(BufferBase, 0)
        ArrayInitialize(BufferTrigger, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_bb, UPPER_BAND, 0, count, BufferUpper)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb, LOWER_BAND, 0, count, BufferLower)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb, BASE_LINE, 0, count, BufferBase)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferTrigger[i] = BufferTrigger[i + 1]
        if BufferTrigger[i] == 1 and close[i] < BufferBase[i]:
            BufferTrigger[i] = 0.0
        if BufferTrigger[i] == -1 and close[i] > BufferBase[i]:
            BufferTrigger[i] = 0.0
        if close[i] >= BufferUpper[i]:
            BufferTrigger[i] = 1.0
        if close[i] <= BufferLower[i]:
            BufferTrigger[i] = -1.0
        if BufferTrigger[i] == 1:
            BufferCloud1[i] = BufferUpper[i]
            BufferCloud2[i] = BufferLower[i]
        elif BufferTrigger[i] == -1:
            BufferCloud1[i] = BufferLower[i]
            BufferCloud2[i] = BufferUpper[i]
        else:
            BufferCloud1[i] = 0.0
            BufferCloud2[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BandsFill(_MQL5Indicator):
    name = 'Bands_Fill'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpDeviation': 2.0,  # Deviation
    }

