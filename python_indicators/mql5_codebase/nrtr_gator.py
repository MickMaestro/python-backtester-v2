"""NRTR_GATOR — converted from MQL5: MQL5 Indicators/NRTR GATOR/NRTR_GATOR.mq5

Copyright: Rosh; Link: http://forexsystems.ru/phpBB/index.php

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rosh', 'link': 'http://forexsystems.ru/phpBB/index.php', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 11}, 'colors': {1: [4678655], 2: [16760576], 3: [16760576], 4: [4678655], 5: [3329434, 255]}, 'widths': {5: 3}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'NRTR_GATOR', 'source': 'MQL5 Indicators/NRTR GATOR/NRTR_GATOR.mq5', 'folder': 'NRTR GATOR', 'inputs': [{'mql': 'PerATR', 'py': 'PerATR', 'param': 'PerATR', 'type': 'int', 'default': 40, 'label': '', 'sinput': False}, {'mql': 'kATR', 'py': 'kATR', 'param': 'kATR', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'useSendMail', 'py': 'useSendMail', 'param': 'useSendMail', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PerATR = _input('PerATR', 40)
kATR = _input('kATR', 2.0)
useSendMail = _input('useSendMail', False)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
Ceil = Arr(0, 0.0)
Floor = Arr(0, 0.0)
UpBar = Arr(0, 0.0)
DownBar = Arr(0, 0.0)
ColorHistogram_2Colors = Arr(0, 0.0)
Trend = Arr(0, 0.0)
GatorTrend = Arr(0, 0.0)
handle_iATR = 0  # variable for storing the handle of the iATR indicator
handle_iAlligator = 0  # variable for storing the handle of the iAlligator indicator

def OnInit():
    global handle_iATR, handle_iAlligator
    PlotIndexSetInteger(0, PLOT_ARROW, 251)
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetString(0, PLOT_LABEL, 'Линия продажи')
    PlotIndexSetInteger(1, PLOT_ARROW, 251)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetString(1, PLOT_LABEL, 'Линия покупки')
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    SetIndexBuffer(2, Ceil, INDICATOR_DATA)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetString(2, PLOT_LABEL, 'Потолок')
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    SetIndexBuffer(3, Floor, INDICATOR_DATA)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetString(3, PLOT_LABEL, 'Пол')
    SetIndexBuffer(4, UpBar, INDICATOR_DATA)
    SetIndexBuffer(5, DownBar, INDICATOR_DATA)
    SetIndexBuffer(6, ColorHistogram_2Colors, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 2)
    SetIndexBuffer(7, Trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, GatorTrend, INDICATOR_CALCULATIONS)
    handle_iATR = iATR(Symbol(), Period(), PerATR)
    if handle_iATR == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iATR indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    handle_iAlligator = iAlligator(Symbol(), Period(), 13, 8, 8, 5, 5, 3, MODE_SMMA, PRICE_MEDIAN)
    if handle_iAlligator == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iAlligator indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    ArraySetAsSeries(SellBuffer, True)
    ArraySetAsSeries(BuyBuffer, True)
    ArraySetAsSeries(Ceil, True)
    ArraySetAsSeries(Floor, True)
    ArraySetAsSeries(UpBar, True)
    ArraySetAsSeries(DownBar, True)
    ArraySetAsSeries(ColorHistogram_2Colors, True)
    ArraySetAsSeries(Trend, True)
    ArraySetAsSeries(GatorTrend, True)
    return INIT_SUCCEEDED

def BreakDown(shift, close_value):
    result = False
    if close_value > SellBuffer[shift + 1]:
        result = True
    return result

def BreakUp(shift, close_value):
    result = False
    if close_value < BuyBuffer[shift + 1]:
        result = True
    return result

def BreakFloor(shift, high_value):
    result = False
    if high_value < Floor[shift + 1]:
        result = True
    return result

def BreakCeil(shift, low_value):
    result = False
    if low_value > Ceil[shift + 1]:
        result = True
    return result

def Uptrend(shift):
    result = False
    if Trend[shift + 1] == 1.0:
        result = True
    if Trend[shift + 1] == -1.0:
        result = False
    if Trend[shift + 1] != 1.0 and Trend[shift + 1] != -1:
        Print('Внимание! Тренд не определен, такого быть не может. Бар # ', shift)
    return result

def NewCeil(shift, close_value):
    Ceil[shift] = close_value
    Floor[shift] = 0.0

def NewFloor(shift, close_value):
    Floor[shift] = close_value
    Ceil[shift] = 0.0

def SetBuyBuffer(shift, close_value):
    BuyBuffer[shift] = close_value - (kATR * iATRGet(shift))
    SellBuffer[shift] = 0.0

def SetSellBuffer(shift, close_value):
    SellBuffer[shift] = close_value + (kATR * iATRGet(shift))
    BuyBuffer[shift] = 0.0

def NewTrend(shift, close_value):
    if Trend[shift + 1] == 1.0:
        Trend[shift] = -1.0
        NewFloor(shift, close_value)
        SetSellBuffer(shift, close_value)
    else:
        Trend[shift] = 1.0
        NewCeil(shift, close_value)
        SetBuyBuffer(shift, close_value)
    if Trend[shift + 1] != 1 and Trend[shift + 1] != -1:
        Print('Внимание! Тренд не определен, такого быть не может')

def CopyLastValues(shift):
    SellBuffer[shift] = SellBuffer[shift + 1]
    BuyBuffer[shift] = BuyBuffer[shift + 1]
    Ceil[shift] = Ceil[shift + 1]
    Floor[shift] = Floor[shift + 1]
    Trend[shift] = Trend[shift + 1]

def deinit():
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = 0
    if prev_calculated > 0:
        limit = rates_total - prev_calculated + 1
    if prev_calculated == 0:
        ArrayInitialize(SellBuffer, 0.0)
        ArrayInitialize(BuyBuffer, 0.0)
        ArrayInitialize(Ceil, 0.0)
        ArrayInitialize(Floor, 0.0)
        ArrayInitialize(UpBar, 0.0)
        ArrayInitialize(DownBar, 0.0)
        ArrayInitialize(ColorHistogram_2Colors, 2)
        ArrayInitialize(Trend, 0.0)
        ArrayInitialize(GatorTrend, 0.0)
        limit = rates_total - PerATR - 1
        if close[limit + 1] > open[limit + 1]:
            Trend[limit + 1] = 1.0
            Ceil[limit + 1] = close[limit + 1]
            BuyBuffer[limit + 1] = close[limit + 1] - (kATR * iATRGet(limit + 1))
        if close[limit + 1] < open[limit + 1]:
            Trend[limit + 1] = -1.0
            Floor[limit + 1] = close[limit + 1]
            SellBuffer[limit + 1] = close[limit + 1] + (kATR * iATRGet(limit + 1))
        if close[limit + 1] == open[limit + 1]:
            Trend[limit + 1] = 1.0
            Ceil[limit + 1] = close[limit + 1]
            BuyBuffer[limit + 1] = close[limit + 1] - (kATR * iATRGet(limit + 1))
    for cnt in range(limit, 0 - 1, -1):
        if iAlligatorGet(GATORJAW_LINE, cnt) < iAlligatorGet(GATORTEETH_LINE, cnt) and iAlligatorGet(GATORTEETH_LINE, cnt) < iAlligatorGet(GATORLIPS_LINE, cnt):
            GatorTrend[cnt] = 1.0
        if iAlligatorGet(GATORJAW_LINE, cnt) > iAlligatorGet(GATORTEETH_LINE, cnt) and iAlligatorGet(GATORTEETH_LINE, cnt) > iAlligatorGet(GATORLIPS_LINE, cnt):
            GatorTrend[cnt] = -1.0
        if GatorTrend[cnt] == 1.0:
            UpBar[cnt] = high[cnt]
            DownBar[cnt] = low[cnt]
        if GatorTrend[cnt] == -1.0:
            UpBar[cnt] = low[cnt]
            DownBar[cnt] = high[cnt]
        if UpBar[cnt] > DownBar[cnt]:
            ColorHistogram_2Colors[cnt] = 0.0
        else:
            ColorHistogram_2Colors[cnt] = 1.0
        if Uptrend(cnt):
            if BreakCeil(cnt, low[cnt]):
                NewCeil(cnt, close[cnt])
                SetBuyBuffer(cnt, close[cnt])
                Trend[cnt] = 1.0
                continue
            if BreakUp(cnt, close[cnt]):
                NewTrend(cnt, close[cnt])
                continue
            CopyLastValues(cnt)
        else:
            if BreakFloor(cnt, high[cnt]):
                NewFloor(cnt, close[cnt])
                SetSellBuffer(cnt, close[cnt])
                Trend[cnt] = -1.0
                continue
            if BreakDown(cnt, close[cnt]):
                NewTrend(cnt, close[cnt])
                continue
            CopyLastValues(cnt)
    return rates_total

def iATRGet(index):
    ATR = Arr(1, 0.0, dyn=False)
    ResetLastError()
    if CopyBuffer(handle_iATR, 0, index, 1, ATR) < 0:
        PrintFormat('Failed to copy data from the iATR indicator, error code %d', GetLastError())
        return 0.0
    return ATR[0]

def iAlligatorGet(buffer, index):
    Alligator = Arr(1, 0.0, dyn=False)
    ResetLastError()
    if CopyBuffer(handle_iAlligator, buffer, index, 1, Alligator) < 0:
        PrintFormat('Failed to copy data from the iAlligator indicator, error code %d, buffer %d , index %d ', GetLastError(), buffer, index)
        return 0.0
    return Alligator[0]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NRTRGATOR(_MQL5Indicator):
    name = 'NRTR_GATOR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PerATR': 40,
        'kATR': 2.0,
        'useSendMail': False,
    }

