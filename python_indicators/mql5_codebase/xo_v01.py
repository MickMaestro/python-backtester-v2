"""xo_v01 — converted from MQL5: MQL5 Indicators/Point and Figure/xo_v01.mq5

Copyright: Copyright © 2006-2012, FINEXWARE Technologies GmbH; Link: www.FINEXWARE.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006-2012, FINEXWARE Technologies GmbH', 'link': 'www.FINEXWARE.com', 'version': '1.0', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {}, 'colors': {1: [255, 3329330]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'xo_v01', 'source': 'MQL5 Indicators/Point and Figure/xo_v01.mq5', 'folder': 'Point and Figure', 'inputs': [{'mql': 'StepBox', 'py': 'StepBox', 'param': 'StepBox', 'type': 'int', 'default': 50, 'label': 'Price step', 'sinput': False}, {'mql': 'Treshold', 'py': 'Treshold', 'param': 'Treshold', 'type': 'double', 'default': 2.0, 'label': 'Threshold for the change of direction', 'sinput': False}, {'mql': 'MaxBar', 'py': 'MaxBar', 'param': 'MaxBar', 'type': 'int', 'default': 1000, 'label': 'Number of verifiable bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
StepBox = _input('StepBox', 50)  # Price step
Treshold = _input('Treshold', 2.0)  # Threshold for the change of direction
MaxBar = _input('MaxBar', 1000)  # Number of verifiable bars
Up = Arr(0, 0.0)
Hi = Arr(0, 0.0)
Lo = Arr(0, 0.0)
Dn = Arr(0, 0.0)
Clr = Arr(0, 0.0)

def OnInit():
    if StepBox <= 0 or Treshold <= 0:
        Alert('Error: StepBox<=0 || Treshold<=0')
        return -1
    i = -1
    i += 1
    SetIndexBuffer(i, Up, INDICATOR_DATA)
    i += 1
    SetIndexBuffer(i, Hi, INDICATOR_DATA)
    i += 1
    SetIndexBuffer(i, Lo, INDICATOR_DATA)
    i += 1
    SetIndexBuffer(i, Dn, INDICATOR_DATA)
    i += 1
    SetIndexBuffer(i, Clr, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_COLOR_CANDLES)
    ArraySetAsSeries(Hi, True)
    ArraySetAsSeries(Lo, True)
    ArraySetAsSeries(Up, True)
    ArraySetAsSeries(Dn, True)
    ArraySetAsSeries(Clr, True)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArrayInitialize(Hi, EMPTY_VALUE)
    ArrayInitialize(Lo, EMPTY_VALUE)
    ArrayInitialize(Up, EMPTY_VALUE)
    ArrayInitialize(Dn, EMPTY_VALUE)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    limit = 0
    if MaxBar <= 0:
        limit = rates_total - 1
    else:
        limit = MaxBar
    nBar = 0
    dir = 0
    Lvl = 0.0
    for i in range(limit, 0 - 1, -1):
        if (high[i] >= (Lvl + Box__v) and dir == 1) or (high[i] >= (Lvl + (Treshold * Box__v)) and dir == 0):
            Lvl += Box__v * MathFloor(_fdiv(high[i] - Lvl, Box__v))
            if dir == 0:
                nBar += 1
            dir = 1
        elif (low[i] <= (Lvl - Box__v) and dir == 0) or (low[i] <= (Lvl - (Treshold * Box__v)) and dir == 1):
            Lvl -= Box__v * MathFloor(_fdiv(Lvl - low[i], Box__v))
            if dir == 1:
                nBar += 1
            dir = 0
    Lvl = 0.0
    dir = 0
    b = nBar
    for i in range(limit, 0 - 1, -1):
        if (high[i] >= (Lvl + Box__v) and dir == 1) or (high[i] >= (Lvl + (Treshold * Box__v)) and dir == 0):
            if dir == 0:
                b -= 1
                Dn[b] = Lvl + Box__v
            Lvl += Box__v * MathFloor(_fdiv(high[i] - Lvl, Box__v))
            Up[b] = Lvl
            dir = 1
            Clr[b] = 1.0
        elif (low[i] <= (Lvl - Box__v) and dir == 0) or (low[i] <= (Lvl - (Treshold * Box__v)) and dir == 1):
            if dir == 1:
                b -= 1
                Dn[b] = Lvl - Box__v
            Lvl -= Box__v * MathFloor(_fdiv(Lvl - low[i], Box__v))
            Up[b] = Lvl
            dir = 0
            Clr[b] = 0.0
        if Hi[b] == EMPTY_VALUE or Hi[b] < Up[b]:
            Hi[b] = Up[b]
        if Hi[b] == EMPTY_VALUE or Hi[b] < high[i]:
            Hi[b] = high[i]
        if Lo[b] == EMPTY_VALUE or Lo[b] > Dn[b]:
            Lo[b] = Dn[b]
        if Lo[b] == EMPTY_VALUE or Lo[b] > low[i]:
            Lo[b] = low[i]
    Hi[nBar - 1] = EMPTY_VALUE
    Lo[nBar - 1] = EMPTY_VALUE
    Up[nBar - 1] = EMPTY_VALUE
    Dn[nBar - 1] = EMPTY_VALUE
    return rates_total

# ---- global variables initialised from expressions
Box__v = StepBox * Point()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XoV01(_MQL5Indicator):
    name = 'xo_v01'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'StepBox': 50,  # Price step
        'Treshold': 2.0,  # Threshold for the change of direction
        'MaxBar': 1000,  # Number of verifiable bars
    }

