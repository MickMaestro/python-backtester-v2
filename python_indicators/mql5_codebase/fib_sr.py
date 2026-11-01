"""Fib_SR — converted from MQL5: MQL5 Indicators/Fib_SR/Fib_SR.mq5

Copyright: Copyright © 2006, Eli hayun; Link: http://www.elihayun.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Eli hayun', 'link': 'http://www.elihayun.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Fib_SR', 'source': 'MQL5 Indicators/Fib_SR/Fib_SR.mq5', 'folder': 'Fib_SR', 'inputs': [{'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16408, 'label': 'Таймфрейм индикатора для расчета индикатора', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для расчета индикатора', 'sinput': False}, {'mql': 'Ratio1', 'py': 'Ratio1', 'param': 'Ratio1', 'type': 'double', 'default': 0.618, 'label': 'первое соотношение', 'sinput': False}, {'mql': 'Ratio2', 'py': 'Ratio2', 'param': 'Ratio2', 'type': 'double', 'default': 1.382, 'label': 'второе соотношение', 'sinput': False}, {'mql': 'Color_Res2', 'py': 'Color_Res2', 'param': None, 'type': 'color', 'default': 65280, 'label': 'цвет второй зоны сопротивления', 'sinput': False}, {'mql': 'Color_Res1', 'py': 'Color_Res1', 'param': None, 'type': 'color', 'default': 32768, 'label': 'цвет первой зоны сопротивления', 'sinput': False}, {'mql': 'Color_Sup1', 'py': 'Color_Sup1', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет первой зоны поддержки', 'sinput': False}, {'mql': 'Color_Sup2', 'py': 'Color_Sup2', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет второй зоны поддержки', 'sinput': False}, {'mql': 'RightTail', 'py': 'RightTail', 'param': 'RightTail', 'type': 'uint', 'default': 60, 'label': 'выступ прямоугольников за нулевой бар вправо в минутах', 'sinput': False}, {'mql': 'LeftTail', 'py': 'LeftTail', 'param': 'LeftTail', 'type': 'uint', 'default': 60, 'label': 'выступ прямоугольников за стартовый бар влево в минутах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Timeframe = _input('Timeframe', PERIOD_D1)  # Таймфрейм индикатора для расчета индикатора
NumberofBar = _input('NumberofBar', 1)  # Номер бара для расчета индикатора
Ratio1 = _input('Ratio1', 0.618)  # первое соотношение
Ratio2 = _input('Ratio2', 1.382)  # второе соотношение
Color_Res2 = _input('Color_Res2', clrLime)  # цвет второй зоны сопротивления
Color_Res1 = _input('Color_Res1', clrGreen)  # цвет первой зоны сопротивления
Color_Sup1 = _input('Color_Sup1', clrRed)  # цвет первой зоны поддержки
Color_Sup2 = _input('Color_Sup2', clrMagenta)  # цвет второй зоны поддержки
RightTail = _input('RightTail', 60)  # выступ прямоугольников за нулевой бар вправо в минутах
LeftTail = _input('LeftTail', 60)  # выступ прямоугольников за стартовый бар влево в минутах
SecondRightTail = 0
SecondLeftTail = 0

def CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, background, text):
    ObjectCreate(chart_id, name, OBJ_RECTANGLE, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_FILL, True)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, background)
    ObjectSetString(chart_id, name, OBJPROP_TOOLTIP, '\n')
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, background, text):
    if ObjectFind(chart_id, name) == -1:
        CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, background, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)

def OnInit():
    global SecondLeftTail, SecondRightTail
    SecondRightTail = RightTail * 60
    SecondLeftTail = LeftTail * 60
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fib_SR')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, 'FIB_SUP_1')
    ObjectDelete(0, 'FIB_SUP_2')
    ObjectDelete(0, 'FIB_RES_1')
    ObjectDelete(0, 'FIB_RES_2')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if prev_calculated == rates_total and NumberofBar:
        return rates_total
    nClose = Arr(1, 0.0, dyn=False)
    nHigh = Arr(1, 0.0, dyn=False)
    nLow = Arr(1, 0.0, dyn=False)
    nTime = Arr(1, 0, dyn=False)
    to_copy = 0
    ArraySetAsSeries(time, True)
    to_copy = 1
    if CopyTime(None, Timeframe, 0, to_copy, nTime) < to_copy:
        return 0
    if CopyClose(None, Timeframe, NumberofBar, to_copy, nClose) < to_copy:
        return 0
    if CopyHigh(None, Timeframe, NumberofBar, to_copy, nHigh) < to_copy:
        return 0
    if CopyLow(None, Timeframe, NumberofBar, to_copy, nLow) < to_copy:
        return 0
    C = nClose[0]
    H = nHigh[0]
    L = nLow[0]
    R = H - L
    C = (H + L + C) / 3
    D = (R / 2) + C
    B = C - (R / 2)
    E = R + C
    A = C - R
    R1 = R * Ratio2
    R2 = R * Ratio1
    B1 = C - R2
    A1 = C - R1
    D1 = C + R2
    E1 = C + R1
    SetRectangle(0, 'FIB_RES_2', 0, nTime[0] - SecondLeftTail, E, time[0] + SecondRightTail, E1, Color_Res2, True, 'FIB_RES_2')
    SetRectangle(0, 'FIB_RES_1', 0, nTime[0] - SecondLeftTail, D, time[0] + SecondRightTail, D1, Color_Res1, True, 'FIB_RES_1')
    SetRectangle(0, 'FIB_SUP_1', 0, nTime[0] - SecondLeftTail, B, time[0] + SecondRightTail, B1, Color_Sup1, True, 'FIB_SUP_1')
    SetRectangle(0, 'FIB_SUP_2', 0, nTime[0] - SecondLeftTail, A, time[0] + SecondRightTail, A1, Color_Sup2, True, 'FIB_SUP_2')
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FibSR(_MQL5Indicator):
    name = 'Fib_SR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Таймфрейм индикатора для расчета индикатора
        'NumberofBar': 1,  # Номер бара для расчета индикатора
        'Ratio1': 0.618,  # первое соотношение
        'Ratio2': 1.382,  # второе соотношение
        'RightTail': 60,  # выступ прямоугольников за нулевой бар вправо в минутах
        'LeftTail': 60,  # выступ прямоугольников за стартовый бар влево в минутах
    }

