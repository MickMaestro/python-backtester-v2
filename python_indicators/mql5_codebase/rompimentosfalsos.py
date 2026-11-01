"""RompimentosFalsos — converted from MQL5: MQL5 Indicators/False Breakups/RompimentosFalsos.mq5

Copyright: Copyright 2025, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 1, 4: 1, 5: 5, 6: 5}, 'colors': {1: [16711680], 2: [255], 3: [16711680], 4: [255], 5: [255], 6: [16711680]}, 'widths': {1: 5, 2: 5}, 'styles': {}, 'labels': {1: 'Buy', 2: 'Sell', 3: 'Support', 4: 'Resitance', 5: 'Bottom', 6: 'Top'}, 'levels': [], 'description': [], 'name': 'RompimentosFalsos', 'source': 'MQL5 Indicators/False Breakups/RompimentosFalsos.mq5', 'folder': 'False Breakups', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtResistancesBuffer = Arr(0, 0.0)
ExtSupportsBuffer = Arr(0, 0.0)
ExtTopsBuffer = Arr(0, 0.0)
ExtBottomsBuffer = Arr(0, 0.0)
ExtSellBuffer = Arr(0, 0.0)
ExtBuyBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtBuyBuffer)
    SetIndexBuffer(1, ExtSellBuffer)
    SetIndexBuffer(2, ExtSupportsBuffer)
    SetIndexBuffer(3, ExtResistancesBuffer)
    SetIndexBuffer(4, ExtBottomsBuffer)
    SetIndexBuffer(5, ExtTopsBuffer)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, 10)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -10)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_lastBottom, _s_OnCalculate_lastTop
    if prev_calculated == rates_total:
        return rates_total
    if prev_calculated == 0:
        ArrayInitialize(ExtResistancesBuffer, 0)
        ArrayInitialize(ExtSupportsBuffer, 0)
        ArrayInitialize(ExtTopsBuffer, 0)
        ArrayInitialize(ExtBottomsBuffer, 0)
        ArrayInitialize(ExtSellBuffer, 0)
        ArrayInitialize(ExtBuyBuffer, 0)
    if prev_calculated == (rates_total - 1):
        currentIndex = rates_total - 1
        ExtResistancesBuffer[currentIndex] = 0.0
        ExtSupportsBuffer[currentIndex] = 0.0
        ExtTopsBuffer[currentIndex] = 0.0
        ExtBottomsBuffer[currentIndex] = 0.0
        ExtSellBuffer[currentIndex] = 0.0
        ExtBuyBuffer[currentIndex] = 0.0
    limit = prev_calculated - 1
    if limit < 2:
        limit = 2
    i0 = 0
    i1 = 0
    i2 = 0
    for i in range(limit, rates_total - 1):
        i0 = i
        i1 = i - 1
        i2 = i - 2
        ExtTopsBuffer[i1] = 0.0
        ExtBottomsBuffer[i1] = 0.0
        ExtTopsBuffer[i0] = 0.0
        ExtBottomsBuffer[i0] = 0.0
        if high[i2] < high[i1] and high[i1] > high[i0]:
            _s_OnCalculate_lastTop = high[i1]
            ExtTopsBuffer[i1] = _s_OnCalculate_lastTop
            ExtResistancesBuffer[i1] = _s_OnCalculate_lastTop
        if low[i2] > low[i1] and low[i1] < low[i0]:
            _s_OnCalculate_lastBottom = low[i1]
            ExtBottomsBuffer[i1] = _s_OnCalculate_lastBottom
            ExtSupportsBuffer[i1] = _s_OnCalculate_lastBottom
        ExtResistancesBuffer[i0] = _s_OnCalculate_lastTop
        ExtSupportsBuffer[i0] = _s_OnCalculate_lastBottom
        if IsSell(ExtTopsBuffer, close, i0, rates_total):
            ExtSellBuffer[i0] = high[i0]
        if IsBuy(ExtBottomsBuffer, close, i0, rates_total):
            ExtBuyBuffer[i0] = low[i0]
    currentIndex = rates_total - 1
    ExtResistancesBuffer[currentIndex] = _s_OnCalculate_lastTop
    ExtSupportsBuffer[currentIndex] = _s_OnCalculate_lastBottom
    return rates_total

def IndexNextPoint(buffer, initial_index, rates_total):
    for i in range(initial_index - 1, 0 - 1, -1):
        if buffer[i] != 0:
            return i
    return 0

def IsBuy(points, close, i, rates_total):
    if i < 2:
        return False
    iPoint = 0
    iPoint = IndexNextPoint(points, i, rates_total)
    if iPoint == 0:
        return False
    point = points[iPoint]
    step = 0
    for x in range(i, iPoint, -1):
        c = close[x]
        if x == i:
            if c > point:
                step = 1
                continue
            else:
                return False
        if step == 1:
            if c < point:
                step = 2
                continue
            elif c > point:
                return False
        if step == 2 and c > point:
            return True
    return False

def IsSell(points, close, i, rates_total):
    if i < 2:
        return False
    iPoint = 0
    iPoint = IndexNextPoint(points, i, rates_total)
    if iPoint == 0:
        return False
    point = points[iPoint]
    step = 0
    for x in range(i, iPoint, -1):
        c = close[x]
        if x == i:
            if c < point:
                step = 1
                continue
            else:
                return False
        if step == 1:
            if c > point:
                step = 2
                continue
            elif c < point:
                return False
        if step == 2 and c < point:
            return True
    return False

# ---- static local variables
_s_OnCalculate_lastTop = 0.0
_s_OnCalculate_lastBottom = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RompimentosFalsos(_MQL5Indicator):
    name = 'RompimentosFalsos'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

