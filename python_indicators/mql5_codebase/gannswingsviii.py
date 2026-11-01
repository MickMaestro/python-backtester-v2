"""gannswingsviii — converted from MQL5: MQL5 Indicators/GannSwingsVIII/gannswingsviii.mq5

Copyright: Copyright © 2005, Rosh; Link: http://www.metaquotes.net; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Rosh', 'link': 'http://www.metaquotes.net', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 2, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [55295], 2: [16711680], 3: [8721863], 4: [16760576], 5: [16711935]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 1, 5: 1}, 'styles': {1: 0, 2: 4, 3: 4}, 'labels': {1: 'BinaryWave', 2: 'Upper', 3: 'Lower', 4: 'Buy', 5: 'Sell'}, 'levels': [], 'description': [], 'name': 'gannswingsviii', 'source': 'MQL5 Indicators/GannSwingsVIII/gannswingsviii.mq5', 'folder': 'GannSwingsVIII', 'inputs': [{'mql': 'kind', 'py': 'kind', 'param': 'kind', 'type': 'int', 'default': 1, 'label': 'Тип тенденции', 'sinput': False}, {'mql': 'MoveLastSwing', 'py': 'MoveLastSwing', 'param': 'MoveLastSwing', 'type': 'bool', 'default': False, 'label': 'Сдвиг хвоста зигзага к нулевому бару для двух одинаковых баров по High или Low', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Type
LITTLE = 1
MIDLE = 2
MAIN = 3
_enum('Type', {1: 'LITTLE', 2: 'MIDLE', 3: 'MAIN'})

# ---- inputs and global variables
kind = _input('kind', LITTLE)  # Тип тенденции
MoveLastSwing = _input('MoveLastSwing', False)  # Сдвиг хвоста зигзага к нулевому бару для двух одинаковых баров по High или Low
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SwingsBuffer = Arr(0, 0.0)
HighsBuffer = Arr(0, 0.0)
LowsBuffer = Arr(0, 0.0)
TrendBuffer = Arr(0, 0.0)
UpCloseOutSideBuffers = Arr(0, 0.0)
DownCloseOutSideBuffers = Arr(0, 0.0)
SwingHigh = 0.0
SwingLow = 0.0
LastSwing = 0
lowCounter = 0
highCounter = 0
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, SwingsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SwingsBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, HighsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(HighsBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    SetIndexBuffer(2, LowsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(LowsBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    SetIndexBuffer(3, UpCloseOutSideBuffers, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpCloseOutSideBuffers, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    SetIndexBuffer(4, DownCloseOutSideBuffers, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DownCloseOutSideBuffers, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(4, PLOT_ARROW, 108)
    SetIndexBuffer(5, TrendBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(TrendBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'GannSwingsVIII')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global LastSwing, SwingHigh, SwingLow, highCounter, lowCounter
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    maxbar = 0
    nonOutSide = False
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    maxbar = rates_total - min_rates_total - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
        lowCounter = 0
        highCounter = 0
        LowsBuffer[limit] = Low[limit]
        SwingsBuffer[limit] = High[limit]
        SwingsBuffer[limit] = Low[limit]
        SwingHigh = High[limit]
        SwingLow = Low[limit]
        LastSwing = 0
        TrendBuffer[limit + 1] = -1.0
        TrendBuffer[limit] = -1.0
    else:
        limit = maxbar
        lowCounter = 0
        highCounter = 0
        LowsBuffer[limit] = Low[limit]
        SwingsBuffer[limit] = High[limit]
        SwingsBuffer[limit] = Low[limit]
        SwingHigh = High[limit]
        SwingLow = Low[limit]
        LastSwing = 0
        TrendBuffer[limit + 1] = -1.0
        TrendBuffer[limit] = -1.0
    LastSwing += limit
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if bar != maxbar:
            UpCloseOutSideBuffers[bar] = 0.0
            DownCloseOutSideBuffers[bar] = 0.0
            SwingsBuffer[bar] = 0.0
            HighsBuffer[bar] = 0.0
            LowsBuffer[bar] = 0.0
        nonOutSide = not (High[bar] > High[bar + 1] and Low[bar] < Low[bar + 1])
        if not nonOutSide:
            if Close[bar] > Open[bar]:
                UpCloseOutSideBuffers[bar] = (High[bar] + Low[bar]) / 2.0
            else:
                DownCloseOutSideBuffers[bar] = (High[bar] + Low[bar]) / 2.0
        if High[bar] > SwingHigh:
            highCounter += 1
            SwingHigh = High[bar]
            HighsBuffer[bar] = SwingHigh
        if Low[bar] < SwingLow:
            lowCounter += 1
            SwingLow = Low[bar]
            LowsBuffer[bar] = SwingLow
        TrendBuffer[bar] = TrendBuffer[bar + 1]
        if TrendBuffer[bar + 1] == -1.0 and lowCounter == 1:
            if LastSwing != maxbar:
                SwingsBuffer[LastSwing] = 0.0
            LastSwing = bar
            SwingHigh = High[bar]
            SwingLow = Low[bar]
            highCounter = 0
            lowCounter = 0
            SwingsBuffer[bar] = Low[bar]
            HighsBuffer[bar] = SwingHigh
        else:
            if TrendBuffer[bar + 1] == -1.0 and highCounter == kind:
                LastSwing = bar
                SwingHigh = High[bar]
                SwingLow = Low[bar]
                TrendBuffer[bar] = 1.0
                highCounter = 0
                lowCounter = 0
                SwingsBuffer[bar] = High[bar]
                LowsBuffer[bar] = SwingLow
            else:
                if (TrendBuffer[bar + 1] == -1.0 and Low[bar] == SwingLow) and MoveLastSwing:
                    SwingsBuffer[LastSwing] = 0.0
                    LastSwing = bar
                    SwingsBuffer[bar] = Low[bar]
        if TrendBuffer[bar + 1] == 1.0 and highCounter == 1:
            if LastSwing != maxbar:
                SwingsBuffer[LastSwing] = 0.0
            LastSwing = bar
            SwingHigh = High[bar]
            SwingLow = Low[bar]
            highCounter = 0
            lowCounter = 0
            SwingsBuffer[bar] = High[bar]
            LowsBuffer[bar] = SwingLow
        else:
            if TrendBuffer[bar + 1] == 1.0 and lowCounter == kind:
                LastSwing = bar
                SwingHigh = High[bar]
                SwingLow = Low[bar]
                TrendBuffer[bar] = -1.0
                highCounter = 0
                lowCounter = 0
                SwingsBuffer[bar] = Low[bar]
                HighsBuffer[bar] = SwingHigh
            else:
                if (TrendBuffer[bar + 1] == 1.0 and High[bar] == SwingHigh) and MoveLastSwing:
                    SwingsBuffer[LastSwing] = 0.0
                    LastSwing = bar
                    SwingsBuffer[bar] = High[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Gannswingsviii(_MQL5Indicator):
    name = 'gannswingsviii'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'kind': _Choice({1: 'малая', 2: 'промежуточная', 3: 'основная'}, default=1),  # Тип тенденции
        'MoveLastSwing': False,  # Сдвиг хвоста зигзага к нулевому бару для двух одинаковых баров по High или Low
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

