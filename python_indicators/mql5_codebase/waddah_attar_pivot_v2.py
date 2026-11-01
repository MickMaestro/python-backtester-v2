"""Waddah_Attar_Pivot_V2 — converted from MQL5: MQL5 Indicators/Waddah_Attar_Pivot_V2/Waddah_Attar_Pivot_V2.mq5

Copyright: Copyright © 2007, waddahattar@hotmail.com; Link: waddahattar@hotmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, waddahattar@hotmail.com', 'link': 'waddahattar@hotmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711935], 2: [42495], 3: [16748574]}, 'widths': {1: 4, 2: 4, 3: 4}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Pivot 1', 2: 'Pivot 2', 3: 'Pivot 3'}, 'levels': [], 'description': [], 'name': 'Waddah_Attar_Pivot_V2', 'source': 'MQL5 Indicators/Waddah_Attar_Pivot_V2/Waddah_Attar_Pivot_V2.mq5', 'folder': 'Waddah_Attar_Pivot_V2', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'Waddah_Attar_Pivot_V2', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16408, 'label': 'Период графика индикатора (таймфрейм) 1', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм) 2', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16385, 'label': 'Период графика индикатора (таймфрейм) 3', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_color1 = 16711935  # #property indicator_color1
indicator_color2 = 42495  # #property indicator_color2
indicator_color3 = 16748574  # #property indicator_color3

# ---- inputs and global variables
SirName = _input('SirName', 'Waddah_Attar_Pivot_V2')  # Первая часть имени графических объектов
TimeFrame1 = _input('TimeFrame1', PERIOD_D1)  # Период графика индикатора (таймфрейм) 1
TimeFrame2 = _input('TimeFrame2', PERIOD_H4)  # Период графика индикатора (таймфрейм) 2
TimeFrame3 = _input('TimeFrame3', PERIOD_H1)  # Период графика индикатора (таймфрейм) 3
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
min_rates_total = 0
price_name1 = ""
price_name2 = ""
price_name3 = ""
text_name1 = ""
text_name2 = ""
text_name3 = ""
name1 = ""
name2 = ""
name3 = ""

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnDeinit(reason):
    ObjectDelete(0, price_name1)
    ObjectDelete(0, price_name2)
    ObjectDelete(0, price_name3)
    ObjectDelete(0, text_name1)
    ObjectDelete(0, text_name2)
    ObjectDelete(0, text_name3)
    ChartRedraw(0)

def OnInit():
    global min_rates_total, name1, name2, name3, price_name1, price_name2, price_name3, text_name1, text_name2, text_name3
    min_rates_total = 2
    price_name1 = SirName + ' upper price lable'
    price_name2 = SirName + ' middle price lable'
    price_name3 = SirName + ' lower price lable'
    text_name1 = SirName + ' upper text lable'
    text_name2 = SirName + ' middle text lable'
    text_name3 = SirName + ' lower text lable'
    name1 = 'Pivot ' + GetStringTimeframe(TimeFrame1)
    name2 = 'Pivot ' + GetStringTimeframe(TimeFrame2)
    name3 = 'Pivot ' + GetStringTimeframe(TimeFrame3)
    if not TimeFramesCheck(name1, TimeFrame1):
        return INIT_FAILED
    if not TimeFramesCheck(name2, TimeFrame2):
        return INIT_FAILED
    if not TimeFramesCheck(name3, TimeFrame3):
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(0, PLOT_LABEL, name1)
    ArraySetAsSeries(IndBuffer1, True)
    SetIndexBuffer(1, IndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(1, PLOT_LABEL, name2)
    ArraySetAsSeries(IndBuffer2, True)
    SetIndexBuffer(2, IndBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(2, PLOT_LABEL, name3)
    ArraySetAsSeries(IndBuffer3, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Waddah_Attar_Pivot_V2')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    iClose_ = Arr(2, 0.0, dyn=False)
    iHigh_ = Arr(2, 0.0, dyn=False)
    iLow_ = Arr(2, 0.0, dyn=False)
    limit = 0
    bar = 0
    ArraySetAsSeries(time, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if not CopyClose(Symbol(), TimeFrame1, _DT(time[bar]), 2, iClose_):
            return prev_calculated
        if not CopyLow(Symbol(), TimeFrame1, _DT(time[bar]), 2, iLow_):
            return prev_calculated
        if not CopyHigh(Symbol(), TimeFrame1, _DT(time[bar]), 2, iHigh_):
            return prev_calculated
        IndBuffer1[bar] = (iHigh_[0] + iLow_[0] + iClose_[0]) / 3
        if not CopyClose(Symbol(), TimeFrame2, _DT(time[bar]), 2, iClose_):
            return prev_calculated
        if not CopyLow(Symbol(), TimeFrame2, _DT(time[bar]), 2, iLow_):
            return prev_calculated
        if not CopyHigh(Symbol(), TimeFrame2, _DT(time[bar]), 2, iHigh_):
            return prev_calculated
        IndBuffer2[bar] = (iHigh_[0] + iLow_[0] + iClose_[0]) / 3
        if not CopyClose(Symbol(), TimeFrame3, _DT(time[bar]), 2, iClose_):
            return prev_calculated
        if not CopyLow(Symbol(), TimeFrame3, _DT(time[bar]), 2, iLow_):
            return prev_calculated
        if not CopyHigh(Symbol(), TimeFrame3, _DT(time[bar]), 2, iHigh_):
            return prev_calculated
        IndBuffer3[bar] = (iHigh_[0] + iLow_[0] + iClose_[0]) / 3
    else:
        bar = _range_end(bar, 0 - 1, -1)
    SetRightPrice(0, price_name1, 0, time[0], IndBuffer1[0], _uint(indicator_color1))
    SetRightPrice(0, price_name2, 0, time[0], IndBuffer2[0], _uint(indicator_color2))
    SetRightPrice(0, price_name3, 0, time[0], IndBuffer3[0], _uint(indicator_color3))
    SetText(0, text_name1, 0, name1, time[10], IndBuffer1[0], _uint(indicator_color1))
    SetText(0, text_name2, 0, name2, time[10], IndBuffer2[0], _uint(indicator_color2))
    SetText(0, text_name3, 0, name3, time[10], IndBuffer3[0], _uint(indicator_color3))
    ChartRedraw(0)
    return rates_total

def calc_atr(index, h, l, c):
    return MathMax(h[index], c[index - 1]) - MathMin(l[index], c[index - 1])

def CreateText(chart_id, name, nwin, txt, time, price, Color):
    ObjectCreate(chart_id, name, OBJ_TEXT, nwin, time, price)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, txt)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, 1)

def SetText(chart_id, name, nwin, txt, time, price, Color):
    if ObjectFind(chart_id, name) == -1:
        CreateText(chart_id, name, nwin, txt, time, price, Color)
    else:
        ObjectMove(chart_id, name, 0, time, price)
        ObjectSetString(chart_id, name, OBJPROP_TEXT, txt)

def CreateRightPrice(chart_id, name, nwin, time, price, Color):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, 2)

def SetRightPrice(chart_id, name, nwin, time, price, Color):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color)
    else:
        ObjectMove(chart_id, name, 0, time, price)

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WaddahAttarPivotV2(_MQL5Indicator):
    name = 'Waddah_Attar_Pivot_V2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Период графика индикатора (таймфрейм) 1
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм) 2
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Период графика индикатора (таймфрейм) 3
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

