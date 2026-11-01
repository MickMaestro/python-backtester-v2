"""tirone_levels_x5 — converted from MQL5: MQL5 Indicators/Five Tirone Levels/tirone_levels_x5.mq5

5 Tirone Levels
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'colors': {1: [32768], 2: [65280], 3: [55295], 4: [255], 5: [2763429]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 4, 2: 4, 3: 4, 4: 4, 5: 4}, 'labels': {1: 'Upper Tirone Level', 2: 'Upper/Middle Tirone Level', 3: 'Middle Tirone Level', 4: 'Lower/Middle Tirone Level', 5: 'Lower Tirone Level'}, 'levels': [], 'description': ['5 Tirone Levels'], 'name': 'tirone_levels_x5', 'source': 'MQL5 Indicators/Five Tirone Levels/tirone_levels_x5.mq5', 'folder': 'Five Tirone Levels', 'inputs': [{'mql': 'TirPeriod', 'py': 'TirPeriod', 'param': 'TirPeriod', 'type': 'int', 'default': 15, 'label': 'Period of the indicator', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TirPeriod = _input('TirPeriod', 15)  # Period of the indicator
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
quotient = 0.0
StartBars = 0

def OnInit():
    global StartBars
    StartBars = TirPeriod + 1
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer5, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'Upper Tirone Level')
    PlotIndexSetString(1, PLOT_LABEL, 'Upper/Middle Tirone Level')
    PlotIndexSetString(2, PLOT_LABEL, 'Middle Tirone Level')
    PlotIndexSetString(3, PLOT_LABEL, 'Lower/Middle Tirone Level')
    PlotIndexSetString(4, PLOT_LABEL, 'Lower Tirone Level')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, '5 Tirone Levels(', _str(TirPeriod), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    Hhigh = 0.0
    Llow = 0.0
    AdjMean = 0.0
    Upper = 0.0
    UpMiddle = 0.0
    LoMiddle = 0.0
    Lower = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = StartBars
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Hhigh = high[iHighest_u(high, TirPeriod, bar)]
        Llow = low[iLowest_u(low, TirPeriod, bar)]
        AdjMean = (Hhigh + Llow + close[bar]) / 3.0
        Upper = AdjMean + (Hhigh - Llow)
        UpMiddle = (2 * AdjMean) - Llow
        LoMiddle = (2 * AdjMean) - Hhigh
        Lower = AdjMean - (Hhigh - Llow)
        ExtLineBuffer1[bar] = Upper
        ExtLineBuffer2[bar] = UpMiddle
        ExtLineBuffer3[bar] = AdjMean
        ExtLineBuffer4[bar] = LoMiddle
        ExtLineBuffer5[bar] = Lower
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def iHighest_u(array, count, startPos):
    index = startPos
    if startPos < 0:
        Print('Bad value in the iHighest function, startPos = ', startPos)
        return 0
    if (startPos - count) < 0:
        count = startPos
    max_ = array[startPos]
    for i in range(startPos, startPos - count, -1):
        if array[i] > max_:
            index = i
            max_ = array[i]
    return index

def iLowest_u(array, count, startPos):
    index = startPos
    if startPos < 0:
        Print('Bad value in the iLowest function, startPos = ', startPos)
        return 0
    if (startPos - count) < 0:
        count = startPos
    min_ = array[startPos]
    for i in range(startPos, startPos - count, -1):
        if array[i] < min_:
            index = i
            min_ = array[i]
    return index


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TironeLevelsX5(_MQL5Indicator):
    name = 'tirone_levels_x5'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TirPeriod': 15,  # Period of the indicator
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

