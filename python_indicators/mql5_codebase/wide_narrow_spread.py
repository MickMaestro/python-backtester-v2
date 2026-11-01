"""Wide_Narrow_Spread — converted from MQL5: MQL5 Indicators/Wide_Narrow_Spread/Wide_Narrow_Spread.mq5

Wide/Narrow Spread bar indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 17}, 'colors': {1: [8421504], 2: [8421504], 3: [16711680, 255, 11119017]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Wide bar', 2: 'Narrow bar', 3: 'Open;High;Low;Close'}, 'levels': [], 'description': ['Wide/Narrow Spread bar indicator'], 'name': 'Wide_Narrow_Spread', 'source': 'MQL5 Indicators/Wide_Narrow_Spread/Wide_Narrow_Spread.mq5', 'folder': 'Wide_Narrow_Spread', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 4, 'label': 'Range', 'sinput': False}, {'mql': 'InpShowWideBar', 'py': 'InpShowWideBar', 'param': 'InpShowWideBar', 'type': 'int', 'default': 1, 'label': 'Show wide spread bar', 'sinput': False}, {'mql': 'InpShowNarrowBar', 'py': 'InpShowNarrowBar', 'param': 'InpShowNarrowBar', 'type': 'int', 'default': 1, 'label': 'Show narrow spread bar', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 4)  # Range
InpShowWideBar = _input('InpShowWideBar', INPUT_YES)  # Show wide spread bar
InpShowNarrowBar = _input('InpShowNarrowBar', INPUT_YES)  # Show narrow spread bar
BufferWS = Arr(0, 0.0)
BufferNS = Arr(0, 0.0)
BufferOpen = Arr(0, 0.0)
BufferHigh = Arr(0, 0.0)
BufferLow = Arr(0, 0.0)
BufferClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferHL = Arr(0, 0.0)
point = 0.0
period = 0

def OnInit():
    global period, point
    period = (1 if (InpPeriod < 1) else InpPeriod)
    point = Point()
    SetIndexBuffer(0, BufferWS, INDICATOR_DATA)
    SetIndexBuffer(1, BufferNS, INDICATOR_DATA)
    SetIndexBuffer(2, BufferOpen, INDICATOR_DATA)
    SetIndexBuffer(3, BufferHigh, INDICATOR_DATA)
    SetIndexBuffer(4, BufferLow, INDICATOR_DATA)
    SetIndexBuffer(5, BufferClose, INDICATOR_DATA)
    SetIndexBuffer(6, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, BufferHL, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 32)
    PlotIndexSetInteger(1, PLOT_ARROW, 32)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Wide/Narrow Spread bar(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferWS, True)
    ArraySetAsSeries(BufferNS, True)
    ArraySetAsSeries(BufferOpen, True)
    ArraySetAsSeries(BufferHigh, True)
    ArraySetAsSeries(BufferLow, True)
    ArraySetAsSeries(BufferClose, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferHL, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < period or point == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferWS, EMPTY_VALUE)
        ArrayInitialize(BufferNS, EMPTY_VALUE)
        ArrayInitialize(BufferOpen, EMPTY_VALUE)
        ArrayInitialize(BufferHigh, EMPTY_VALUE)
        ArrayInitialize(BufferLow, EMPTY_VALUE)
        ArrayInitialize(BufferClose, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferHL, 0)
    for i in range(limit, 0 - 1, -1):
        BufferClose[i] = EMPTY_VALUE
        BufferLow[i] = BufferClose[i]
        BufferHigh[i] = BufferLow[i]
        BufferOpen[i] = BufferHigh[i]
        BufferColors[i] = 2.0
        BufferHL[i] = high[i] - low[i]
        min_idx = ArrayMinimum(BufferHL, i, period)
        max_idx = ArrayMaximum(BufferHL, i, period)
        if min_idx == WRONG_VALUE or max_idx == WRONG_VALUE:
            continue
        min_ = BufferHL[min_idx]
        max_ = BufferHL[max_idx]
        if InpShowWideBar:
            if max_ == BufferHL[i]:
                BufferWS[i] = _fdiv(max_, point)
                BufferOpen[i] = open[i]
                BufferHigh[i] = high[i]
                BufferLow[i] = low[i]
                BufferClose[i] = close[i]
                BufferColors[i] = 0.0
            else:
                BufferWS[i] = EMPTY_VALUE
        if InpShowNarrowBar:
            if min_ == BufferHL[i]:
                BufferNS[i] = _fdiv(min_, point)
                BufferOpen[i] = open[i]
                BufferHigh[i] = high[i]
                BufferLow[i] = low[i]
                BufferClose[i] = close[i]
                BufferColors[i] = 1.0
            else:
                BufferNS[i] = EMPTY_VALUE
    return rates_total

# ---- static local variables
_s_OnCalculate_last_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WideNarrowSpread(_MQL5Indicator):
    name = 'Wide_Narrow_Spread'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 4,  # Range
        'InpShowWideBar': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show wide spread bar
        'InpShowNarrowBar': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show narrow spread bar
    }

