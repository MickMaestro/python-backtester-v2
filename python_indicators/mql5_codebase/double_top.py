"""Double_Top — converted from MQL5: MQL5 Indicators/Double_Top/Double_Top.mq5

Double top indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [3329330], 2: [32768], 3: [17919], 4: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Double Top', 2: 'Top', 3: 'Double Bottom', 4: 'Bottom'}, 'levels': [], 'description': ['Double top indicator'], 'name': 'Double_Top', 'source': 'MQL5 Indicators/Double_Top/Double_Top.mq5', 'folder': 'Double_Top', 'inputs': [{'mql': 'InpMinHeight', 'py': 'InpMinHeight', 'param': 'InpMinHeight', 'type': 'uint', 'default': 10, 'label': 'Minumum Height/Depth', 'sinput': False}, {'mql': 'InpMaxDist', 'py': 'InpMaxDist', 'param': 'InpMaxDist', 'type': 'uint', 'default': 20, 'label': 'Maximum distance between the twin tops/bottoms', 'sinput': False}, {'mql': 'InpMinBars', 'py': 'InpMinBars', 'param': 'InpMinBars', 'type': 'uint', 'default': 3, 'label': 'Maximum number of bars after the top/bottom', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMinHeight = _input('InpMinHeight', 10)  # Minumum Height/Depth
InpMaxDist = _input('InpMaxDist', 20)  # Maximum distance between the twin tops/bottoms
InpMinBars = _input('InpMinBars', 3)  # Maximum number of bars after the top/bottom
BufferTop = Arr(0, 0.0)
BufferTopDBL = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferBottomDBL = Arr(0, 0.0)
min_height = 0.0
min_hgt = 0
min_bars = 0
max_dist = 0

def OnInit():
    global max_dist, min_bars, min_height, min_hgt
    min_hgt = (1 if (InpMinHeight < 1) else InpMinHeight)
    min_height = min_hgt * Point()
    min_bars = (1 if (InpMinBars < 1) else InpMinBars)
    max_dist = (1 if (InpMaxDist < 1) else InpMaxDist)
    SetIndexBuffer(0, BufferTopDBL, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottomDBL, INDICATOR_DATA)
    SetIndexBuffer(3, BufferBottom, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 82)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_ARROW, 82)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Double top (Min height: ' + _str(min_hgt) + ', max distance: ' + _str(max_dist) + ', min bars: ' + _str(min_bars) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferTopDBL, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferBottomDBL, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(min_bars, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - min_bars - 1
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferTopDBL, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferBottomDBL, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferTopDBL[i] = EMPTY_VALUE
        BufferTop[i] = BufferTopDBL[i]
        BufferBottomDBL[i] = BufferTop[i]
        BufferBottom[i] = BufferBottomDBL[i]
        BufferTop[i + min_bars] = (high[i + min_bars] if IsTop(rates_total, i + min_bars, high, low) else EMPTY_VALUE)
        BufferBottom[i + min_bars] = (low[i + min_bars] if IsBottom(rates_total, i + min_bars, high, low) else EMPTY_VALUE)
        if BufferTop[i + min_bars] == high[i + min_bars]:
            if FindPrevTop(rates_total, i + min_bars, high):
                BufferTopDBL[i + min_bars] = high[i + min_bars]
            else:
                BufferTopDBL[i + min_bars] = EMPTY_VALUE
        if BufferBottom[i + min_bars] == low[i + min_bars]:
            if FindPrevBottom(rates_total, i + min_bars, low):
                BufferBottomDBL[i + min_bars] = low[i + min_bars]
            else:
                BufferBottomDBL[i + min_bars] = EMPTY_VALUE
    return rates_total

def IsTop(rates_total, index, high, low):
    fl = True
    for i in range(1, min_bars + 1):
        if high[index - i] >= high[index]:
            fl = False
    if fl:
        i = index + 1
        while i < rates_total:
            if high[i] >= high[index]:
                return False
            if (high[index] - low[i]) >= min_height:
                return True
            i += 1
    return False

def IsBottom(rates_total, index, high, low):
    fl = True
    for i in range(1, min_bars + 1):
        if low[index - i] <= low[index]:
            fl = False
    if fl:
        i = index + 1
        while i < rates_total:
            if low[i] <= low[index]:
                return False
            if (high[i] - low[index]) >= min_height:
                return True
            i += 1
    return False

def FindPrevTop(rates_total, index, high):
    i = index + 1
    while i < rates_total and i <= (index + max_dist):
        if BufferTop[i] == high[i]:
            return True
        i += 1
    return False

def FindPrevBottom(rates_total, index, low):
    i = index + 1
    while i < rates_total and i <= (index + max_dist):
        if BufferBottom[i] == low[i]:
            return True
        i += 1
    return False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DoubleTop(_MQL5Indicator):
    name = 'Double_Top'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpMinHeight': 10,  # Minumum Height/Depth
        'InpMaxDist': 20,  # Maximum distance between the twin tops/bottoms
        'InpMinBars': 3,  # Maximum number of bars after the top/bottom
    }

