"""t3_double_bands — converted from MQL5: MQL5 Indicators/T3_Double Bands/t3_double_bands.mq5

Copyright: mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 8, 4: 8, 5: 8}, 'colors': {1: [15130800, 14804223], 2: [15130800, 14804223], 3: [11829830, 9662683], 4: [11829830, 9662683], 5: [11829830, 9662683]}, 'widths': {3: 2, 4: 2, 5: 2}, 'styles': {3: 0, 4: 0, 5: 0}, 'labels': {1: 'Upper bands', 2: 'Lower bands', 3: 'High band', 4: 'Middle band', 5: 'Low band'}, 'levels': [], 'description': [], 'name': 't3_double_bands', 'source': 'MQL5 Indicators/T3_Double Bands/t3_double_bands.mq5', 'folder': 'T3_Double Bands', 'inputs': [{'mql': 'T3Period', 'py': 'T3Period', 'param': 'T3Period', 'type': 'int', 'default': 30, 'label': 'Calculation period', 'sinput': False}, {'mql': 'T3Hot', 'py': 'T3Hot', 'param': 'T3Hot', 'type': 'double', 'default': 0.7, 'label': 'T3 hot value', 'sinput': False}, {'mql': 'T3Original', 'py': 'T3Original', 'param': 'T3Original', 'type': 'bool', 'default': False, 'label': 'T3 original Tillson calculation?', 'sinput': False}, {'mql': 'ShowLines', 'py': 'ShowLines', 'param': 'ShowLines', 'type': 'bool', 'default': True, 'label': 'Draw T3 lines?', 'sinput': False}, {'mql': 'MultiColorLines', 'py': 'MultiColorLines', 'param': 'MultiColorLines', 'type': 'bool', 'default': True, 'label': 'Multi color mode for lines?', 'sinput': False}, {'mql': 'MultiColorBand', 'py': 'MultiColorBand', 'param': 'MultiColorBand', 'type': 'bool', 'default': True, 'label': 'Multi color mode for bands?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
T3Period = _input('T3Period', 30)  # Calculation period
T3Hot = _input('T3Hot', 0.7)  # T3 hot value
T3Original = _input('T3Original', False)  # T3 original Tillson calculation?
ShowLines = _input('ShowLines', True)  # Draw T3 lines?
MultiColorLines = _input('MultiColorLines', True)  # Multi color mode for lines?
MultiColorBand = _input('MultiColorBand', True)  # Multi color mode for bands?
UpFaBuffer = Arr(0, 0.0)
UpFbBuffer = Arr(0, 0.0)
DnFaBuffer = Arr(0, 0.0)
DnFbBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
UpColorBuffer = Arr(0, 0.0)
MiBuffer = Arr(0, 0.0)
MiColorBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
DnColorBuffer = Arr(0, 0.0)
trends = Arr(0, 0.0, dims=(5,))
c1 = 0.0
c2 = 0.0
c3 = 0.0
c4 = 0.0
t3Alpha = 0.0
t3Values = Arr(0, 0.0, dims=(18,))

def OnInit():
    global c1, c2, c3, c4, t3Alpha
    SetIndexBuffer(0, UpFaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, UpFbBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, DnFaBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, DnFbBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, UpColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, MiBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, MiColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(9, DnColorBuffer, INDICATOR_COLOR_INDEX)
    if ShowLines:
        for i in range(2, 5):
            PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_COLOR_LINE)
    else:
        for i in range(2, 5):
            PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_NONE)
    a = MathMax(MathMin(T3Hot, 1), 0.0001)
    c1 = (-a) * a * a
    c2 = 3 * ((a * a) + (a * a * a))
    c3 = -3 * ((2 * a * a) + a + (a * a * a))
    c4 = 1 + (3 * a) + (a * a * a) + (3 * a * a)
    t3period = T3Period
    if not T3Original:
        t3period = 1.0 + ((t3period - 1.0) / 2.0)
    t3Alpha = _fdiv(2.0, 1.0 + t3period)
    return 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if ArrayRange(trends, 0) != rates_total:
        ArrayResize(trends, rates_total)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        UpBuffer[i] = calcT3(0, High[i], i, rates_total)
        MiBuffer[i] = calcT3(6, Close[i], i, rates_total)
        DnBuffer[i] = calcT3(12, Low[i], i, rates_total)
        UpFaBuffer[i] = EMPTY_VALUE
        UpFbBuffer[i] = EMPTY_VALUE
        DnFaBuffer[i] = EMPTY_VALUE
        DnFbBuffer[i] = EMPTY_VALUE
        if i > 0:
            for k in range(0, 5):
                trends[i][k] = trends[i - 1][k]
            if UpBuffer[i] > UpBuffer[i - 1]:
                trends[i][0] = 1.0
            if UpBuffer[i] < UpBuffer[i - 1]:
                trends[i][0] = -1.0
            if MiBuffer[i] > MiBuffer[i - 1]:
                trends[i][1] = 1.0
            if MiBuffer[i] < MiBuffer[i - 1]:
                trends[i][1] = -1.0
            if DnBuffer[i] > DnBuffer[i - 1]:
                trends[i][2] = 1.0
            if DnBuffer[i] < DnBuffer[i - 1]:
                trends[i][2] = -1.0
            if trends[i][0] == 1 and trends[i][1] == 1:
                trends[i][3] = 1.0
            if trends[i][0] == -1 and trends[i][1] == -1:
                trends[i][3] = -1.0
            if trends[i][2] == 1 and trends[i][1] == 1:
                trends[i][4] = 1.0
            if trends[i][2] == -1 and trends[i][1] == -1:
                trends[i][4] = -1.0
        else:
            for k in range(0, 5):
                trends[i][k] = 0.0
        UpColorBuffer[i] = (1 if (MultiColorLines and trends[i][0] == -1) else 0)
        MiColorBuffer[i] = (1 if (MultiColorLines and trends[i][1] == -1) else 0)
        DnColorBuffer[i] = (1 if (MultiColorLines and trends[i][2] == -1) else 0)
        if MultiColorBand:
            if trends[i][3] == -1:
                UpFaBuffer[i] = MiBuffer[i]
                UpFbBuffer[i] = UpBuffer[i]
            else:
                UpFbBuffer[i] = MiBuffer[i]
                UpFaBuffer[i] = UpBuffer[i]
            if trends[i][4] == -1:
                DnFaBuffer[i] = DnBuffer[i]
                DnFbBuffer[i] = MiBuffer[i]
            else:
                DnFbBuffer[i] = DnBuffer[i]
                DnFaBuffer[i] = MiBuffer[i]
    return rates_total

def calcT3(s, price, r, bars):
    if ArrayRange(t3Values, 0) != bars:
        ArrayResize(t3Values, bars)
    if r < 2:
        t3Values[r][s + 0] = price
        t3Values[r][s + 1] = price
        t3Values[r][s + 2] = price
        t3Values[r][s + 3] = price
        t3Values[r][s + 4] = price
        t3Values[r][s + 5] = price
    else:
        t3Values[r][s + 0] = t3Values[r - 1][s + 0] + (t3Alpha * (price - t3Values[r - 1][s + 0]))
        t3Values[r][s + 1] = t3Values[r - 1][s + 1] + (t3Alpha * (t3Values[r][s + 0] - t3Values[r - 1][s + 1]))
        t3Values[r][s + 2] = t3Values[r - 1][s + 2] + (t3Alpha * (t3Values[r][s + 1] - t3Values[r - 1][s + 2]))
        t3Values[r][s + 3] = t3Values[r - 1][s + 3] + (t3Alpha * (t3Values[r][s + 2] - t3Values[r - 1][s + 3]))
        t3Values[r][s + 4] = t3Values[r - 1][s + 4] + (t3Alpha * (t3Values[r][s + 3] - t3Values[r - 1][s + 4]))
        t3Values[r][s + 5] = t3Values[r - 1][s + 5] + (t3Alpha * (t3Values[r][s + 4] - t3Values[r - 1][s + 5]))
    return (c1 * t3Values[r][s + 5]) + (c2 * t3Values[r][s + 4]) + (c3 * t3Values[r][s + 3]) + (c4 * t3Values[r][s + 2])


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3DoubleBands(_MQL5Indicator):
    name = 't3_double_bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'T3Period': 30,  # Calculation period
        'T3Hot': 0.7,  # T3 hot value
        'T3Original': False,  # T3 original Tillson calculation?
        'ShowLines': True,  # Draw T3 lines?
        'MultiColorLines': True,  # Multi color mode for lines?
        'MultiColorBand': True,  # Multi color mode for bands?
    }

