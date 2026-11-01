"""supertrend — converted from MQL5: MQL5 Indicators/Supertrend/supertrend.mq5

Copyright: Copyright 2011, FxGeek; Link:  http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, FxGeek', 'link': ' http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [12903679, 10025880], 2: [32768, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Filling', 2: 'SuperTrend'}, 'levels': [], 'description': [], 'name': 'supertrend', 'source': 'MQL5 Indicators/Supertrend/supertrend.mq5', 'folder': 'Supertrend', 'inputs': [{'mql': 'Periode', 'py': 'Periode', 'param': 'Periode', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Multiplier', 'py': 'Multiplier', 'param': 'Multiplier', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'Show_Filling', 'py': 'Show_Filling', 'param': 'Show_Filling', 'type': 'bool', 'default': True, 'label': 'Show as DRAW_FILLING', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Periode = _input('Periode', 10)
Multiplier = _input('Multiplier', 3.0)
Show_Filling = _input('Show_Filling', True)  # Show as DRAW_FILLING
Filled_a = Arr(0, 0.0)
Filled_b = Arr(0, 0.0)
SuperTrend = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
Atr = Arr(0, 0.0)
Up = Arr(0, 0.0)
Down = Arr(0, 0.0)
Middle = Arr(0, 0.0)
trend = Arr(0, 0.0)
atrHandle = 0
changeOfTrend = 0
flag = 0
flagh = 0

def OnInit():
    global atrHandle
    SetIndexBuffer(0, Filled_a, INDICATOR_DATA)
    SetIndexBuffer(1, Filled_b, INDICATOR_DATA)
    SetIndexBuffer(2, SuperTrend, INDICATOR_DATA)
    SetIndexBuffer(3, ColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, Atr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, Up, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, Down, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, Middle, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, trend, INDICATOR_CALCULATIONS)
    atrHandle = iATR(Symbol(), Period(), Periode)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global changeOfTrend, flag, flagh
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(atrHandle, 0, 0, to_copy, Atr) <= 0:
        Print('Getting Atr is failed! Error', GetLastError())
        return 0
    first = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = Periode
    else:
        first = prev_calculated - 1
    for i in range(first, rates_total):
        Middle[i] = (high[i] + low[i]) / 2
        Up[i] = Middle[i] + (Multiplier * Atr[i])
        Down[i] = Middle[i] - (Multiplier * Atr[i])
        if close[i] > Up[i - 1]:
            trend[i] = 1.0
            if trend[i - 1] == -1:
                changeOfTrend = 1
        elif close[i] < Down[i - 1]:
            trend[i] = -1.0
            if trend[i - 1] == 1:
                changeOfTrend = 1
        elif trend[i - 1] == 1:
            trend[i] = 1.0
            changeOfTrend = 0
        elif trend[i - 1] == -1:
            trend[i] = -1.0
            changeOfTrend = 0
        if trend[i] < 0 and trend[i - 1] > 0:
            flag = 1
        else:
            flag = 0
        if trend[i] > 0 and trend[i - 1] < 0:
            flagh = 1
        else:
            flagh = 0
        if trend[i] > 0 and Down[i] < Down[i - 1]:
            Down[i] = Down[i - 1]
        if trend[i] < 0 and Up[i] > Up[i - 1]:
            Up[i] = Up[i - 1]
        if flag == 1:
            Up[i] = Middle[i] + (Multiplier * Atr[i])
        if flagh == 1:
            Down[i] = Middle[i] - (Multiplier * Atr[i])
        if trend[i] == 1:
            SuperTrend[i] = Down[i]
            if changeOfTrend == 1:
                SuperTrend[i - 1] = SuperTrend[i - 2]
                changeOfTrend = 0
            ColorBuffer[i] = 0.0
        elif trend[i] == -1:
            SuperTrend[i] = Up[i]
            if changeOfTrend == 1:
                SuperTrend[i - 1] = SuperTrend[i - 2]
                changeOfTrend = 0
            ColorBuffer[i] = 1.0
        if Show_Filling:
            Filled_a[i] = SuperTrend[i]
            Filled_b[i] = close[i]
        else:
            Filled_a[i] = EMPTY_VALUE
            Filled_b[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Supertrend(_MQL5Indicator):
    name = 'supertrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Periode': 10,
        'Multiplier': 3.0,
        'Show_Filling': True,  # Show as DRAW_FILLING
    }

