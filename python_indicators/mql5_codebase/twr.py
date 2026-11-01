"""TWR — converted from MQL5: MQL5 Indicators/TWR/TWR.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.Jianye; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.Jianye', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 11, 2: 11, 3: 1}, 'colors': {3: [16711680]}, 'widths': {1: 8, 2: 8, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'T1 Open;T1 Close', 2: 'T2 Open;T2 Close', 3: 'T Ema'}, 'levels': [], 'description': [], 'name': 'TWR', 'source': 'MQL5 Indicators/TWR/TWR.mq5', 'folder': 'TWR', 'inputs': [{'mql': 'EmaPeriod', 'py': 'EmaPeriod', 'param': 'EmaPeriod', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
EmaPeriod = _input('EmaPeriod', 12)
hema = 0
BarBuffer1 = Arr(0, 0.0)
BarBuffer2 = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
turn1 = Arr(0, 0.0)
turn2 = Arr(0, 0.0)
turn_color = Arr(0, 0.0)
EmaBuffer = Arr(0, 0.0)

def OnInit():
    global hema
    SetIndexBuffer(0, BarBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, BarBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, turn1, INDICATOR_DATA)
    SetIndexBuffer(4, turn2, INDICATOR_DATA)
    SetIndexBuffer(5, turn_color, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, EmaBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, SignalBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 2)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, clrRed)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, clrGreen)
    PlotIndexSetInteger(1, PLOT_COLOR_INDEXES, 2)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 0, clrRed)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 1, clrGreen)
    hema = iMA(Symbol(), 0, EmaPeriod, 0, MODE_EMA, PRICE_CLOSE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    CopyBuffer(hema, 0, 0, rates_total, EmaBuffer)
    start = 0
    start = prev_calculated
    if prev_calculated == 0:
        BarBuffer1[0] = open[0]
        BarBuffer2[0] = close[0]
        turn1[0] = BarBuffer1[0]
        turn2[0] = BarBuffer2[0]
        if close[0] >= open[0]:
            SignalBuffer[0] = 0.0
            ColorBuffer[0] = 0.0
            turn_color[0] = 0.0
        else:
            SignalBuffer[0] = 1.0
            ColorBuffer[0] = 1.0
            turn_color[0] = 1.0
        start = 1
    for i in range(start, rates_total):
        if SignalBuffer[i - 1] == 0:
            if BarBuffer1[i - 1] <= BarBuffer2[i - 1]:
                BarBuffer1[i] = BarBuffer2[i - 1]
                BarBuffer2[i] = close[i]
                turn1[i] = BarBuffer1[i]
                turn2[i] = BarBuffer2[i]
                if close[i] >= BarBuffer1[i - 1]:
                    SignalBuffer[i] = 0.0
                    ColorBuffer[i] = 0.0
                    turn_color[i] = 0.0
                if close[i] < BarBuffer1[i - 1]:
                    SignalBuffer[i] = 1.0
                    ColorBuffer[i] = 0.0
                    turn1[i] = BarBuffer1[i - 1]
                    turn_color[i] = 1.0
            if BarBuffer1[i - 1] > BarBuffer2[i - 1]:
                if close[i] >= BarBuffer1[i - 1]:
                    BarBuffer1[i] = BarBuffer2[i - 1]
                    BarBuffer2[i] = close[i]
                    turn1[i] = BarBuffer1[i]
                    turn2[i] = BarBuffer2[i]
                    SignalBuffer[i] = 0.0
                    ColorBuffer[i] = 0.0
                    turn_color[i] = 0.0
                if close[i] < BarBuffer1[i - 1] and close[i] >= BarBuffer2[i - 1]:
                    BarBuffer1[i] = BarBuffer1[i - 1]
                    BarBuffer2[i] = close[i]
                    turn1[i] = BarBuffer1[i]
                    turn2[i] = BarBuffer2[i]
                    SignalBuffer[i] = 0.0
                    ColorBuffer[i] = 0.0
                    turn_color[i] = 0.0
                if close[i] < BarBuffer2[i - 1]:
                    BarBuffer1[i] = BarBuffer1[i - 1]
                    BarBuffer2[i] = close[i]
                    turn1[i] = BarBuffer2[i - 1]
                    turn2[i] = BarBuffer2[i]
                    SignalBuffer[i] = 1.0
                    ColorBuffer[i] = 0.0
                    turn_color[i] = 1.0
        if SignalBuffer[i - 1] == 1:
            if BarBuffer1[i - 1] >= BarBuffer2[i - 1]:
                BarBuffer1[i] = BarBuffer2[i - 1]
                BarBuffer2[i] = close[i]
                turn1[i] = BarBuffer1[i]
                turn2[i] = BarBuffer2[i]
                if close[i] <= BarBuffer1[i - 1]:
                    SignalBuffer[i] = 1.0
                    ColorBuffer[i] = 1.0
                    turn_color[i] = 1.0
                if close[i] > BarBuffer1[i - 1]:
                    SignalBuffer[i] = 0.0
                    ColorBuffer[i] = 1.0
                    turn1[i] = BarBuffer1[i - 1]
                    turn_color[i] = 0.0
            if BarBuffer1[i - 1] < BarBuffer2[i - 1]:
                if close[i] <= BarBuffer1[i - 1]:
                    BarBuffer1[i] = BarBuffer2[i - 1]
                    BarBuffer2[i] = close[i]
                    turn1[i] = BarBuffer1[i]
                    turn2[i] = BarBuffer2[i]
                    SignalBuffer[i] = 1.0
                    ColorBuffer[i] = 1.0
                    turn_color[i] = 1.0
                if close[i] > BarBuffer1[i - 1] and close[i] <= BarBuffer2[i - 1]:
                    BarBuffer1[i] = BarBuffer1[i - 1]
                    BarBuffer2[i] = close[i]
                    turn1[i] = BarBuffer1[i]
                    turn2[i] = BarBuffer2[i]
                    SignalBuffer[i] = 1.0
                    ColorBuffer[i] = 1.0
                    turn_color[i] = 1.0
                if close[i] > BarBuffer2[i - 1]:
                    BarBuffer1[i] = BarBuffer1[i - 1]
                    BarBuffer2[i] = close[i]
                    turn1[i] = BarBuffer2[i - 1]
                    turn2[i] = BarBuffer2[i]
                    SignalBuffer[i] = 0.0
                    ColorBuffer[i] = 1.0
                    turn_color[i] = 0.0
    return rates_total - 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TWR(_MQL5Indicator):
    name = 'TWR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'EmaPeriod': 12,
    }

