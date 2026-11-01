"""Dynamic_Trend — converted from MQL5: MQL5 Indicators/Dynamic_Trend/Dynamic_Trend.mq5

Dynamic Trend indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 8, 2: 5, 3: 5}, 'colors': {1: [16711680, 255, 11119017], 2: [16711680], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Line', 2: 'UP', 3: 'DN'}, 'levels': [], 'description': ['Dynamic Trend indicator'], 'name': 'Dynamic_Trend', 'source': 'MQL5 Indicators/Dynamic_Trend/Dynamic_Trend.mq5', 'folder': 'Dynamic_Trend', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpPercent', 'py': 'InpPercent', 'param': 'InpPercent', 'type': 'uint', 'default': 10, 'label': 'Percent', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpPercent = _input('InpPercent', 10)  # Percent
BufferLine = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
percent = 0
period = 0

def OnInit():
    global percent, period
    percent = _int(InpPercent)
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferLine, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(3, BufferDN, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    PlotIndexSetInteger(2, PLOT_ARROW, 234)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dynamic Trend (' + _str(period) + ',' + _str(percent) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferLine, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 4
        ArrayInitialize(BufferLine, 0)
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        BufferLine[limit] = close[limit]
    for i in range(limit, 0 - 1, -1):
        bh = HighestClose(period, i + 1)
        bl = LowestClose(period, i + 1)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        BufferColors[i] = 2.0
        if close[i] < BufferLine[i + 1]:
            BufferLine[i] = close[bh] - (percent * Point())
            BufferColors[i] = 1.0
        else:
            BufferLine[i] = close[bl] + (percent * Point())
            BufferColors[i] = 0.0
        BufferDN[i] = EMPTY_VALUE
        BufferUP[i] = BufferDN[i]
        if close[i + 3] > BufferLine[i + 2] and close[i + 2] < BufferLine[i + 3]:
            BufferUP[i] = open[i]
        if close[i + 2] < BufferLine[i + 1] and close[i + 2] > BufferLine[i + 3]:
            BufferDN[i] = open[i]
    return rates_total

def HighestClose(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMaximum(array) + start) if (CopyClose(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def LowestClose(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMinimum(array) + start) if (CopyClose(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DynamicTrend(_MQL5Indicator):
    name = 'Dynamic_Trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpPercent': 10,  # Percent
    }

