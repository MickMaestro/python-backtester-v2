"""Waddah_Attar_Pivot — converted from MQL5: MQL5 Indicators/Waddah_Attar_Pivot/Waddah_Attar_Pivot.mq5

Copyright: Copyright © 2007, waddahattar@hotmail.com; Link: waddahattar@hotmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, waddahattar@hotmail.com', 'link': 'waddahattar@hotmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [65280], 2: [255], 3: [16711680]}, 'widths': {1: 3, 2: 4, 3: 5}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Daily Pivot', 2: 'Weekly Pivot', 3: 'Monthly Pivot'}, 'levels': [], 'description': [], 'name': 'Waddah_Attar_Pivot', 'source': 'MQL5 Indicators/Waddah_Attar_Pivot/Waddah_Attar_Pivot.mq5', 'folder': 'Waddah_Attar_Pivot', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'Waddah_Attar_Pivot', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_color1 = 65280  # #property indicator_color1
indicator_color2 = 255  # #property indicator_color2
indicator_color3 = 16711680  # #property indicator_color3

# ---- inputs and global variables
SirName = _input('SirName', 'Waddah_Attar_Pivot')  # Первая часть имени графических объектов
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
min_rates_total = 0
daily_price_name = ""
weekly_price_name = ""
monthly_price_name = ""
daily_text_name = ""
weekly_text_name = ""
monthly_text_name = ""

def OnDeinit(reason):
    ObjectDelete(0, daily_price_name)
    ObjectDelete(0, weekly_price_name)
    ObjectDelete(0, monthly_price_name)
    ObjectDelete(0, daily_text_name)
    ObjectDelete(0, weekly_text_name)
    ObjectDelete(0, monthly_text_name)
    ChartRedraw(0)

def OnInit():
    global daily_price_name, daily_text_name, min_rates_total, monthly_price_name, monthly_text_name, weekly_price_name, weekly_text_name
    min_rates_total = 2
    daily_price_name = SirName + ' upper price lable'
    weekly_price_name = SirName + ' middle price lable'
    monthly_price_name = SirName + ' lower price lable'
    daily_text_name = SirName + ' upper text lable'
    weekly_text_name = SirName + ' middle text lable'
    monthly_text_name = SirName + ' lower text lable'
    SetIndexBuffer(0, IndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer1, True)
    SetIndexBuffer(1, IndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer2, True)
    SetIndexBuffer(2, IndBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer3, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Waddah_Attar_Pivot')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    PP = 0.0
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
        if not CopyClose(Symbol(), PERIOD_D1, _DT(time[bar]), 2, iClose_):
            return prev_calculated
        if not CopyLow(Symbol(), PERIOD_D1, _DT(time[bar]), 2, iLow_):
            return prev_calculated
        if not CopyHigh(Symbol(), PERIOD_D1, _DT(time[bar]), 2, iHigh_):
            return prev_calculated
        PP = (iHigh_[0] + iLow_[0] + iClose_[0]) / 3
        IndBuffer1[bar] = PP
        if not CopyClose(Symbol(), PERIOD_W1, _DT(time[bar]), 2, iClose_):
            return prev_calculated
        if not CopyLow(Symbol(), PERIOD_W1, _DT(time[bar]), 2, iLow_):
            return prev_calculated
        if not CopyHigh(Symbol(), PERIOD_W1, _DT(time[bar]), 2, iHigh_):
            return prev_calculated
        PP = (iHigh_[0] + iLow_[0] + iClose_[0]) / 3
        IndBuffer2[bar] = PP
        if not CopyClose(Symbol(), PERIOD_MN1, _DT(time[bar]), 2, iClose_):
            return prev_calculated
        if not CopyLow(Symbol(), PERIOD_MN1, _DT(time[bar]), 2, iLow_):
            return prev_calculated
        if not CopyHigh(Symbol(), PERIOD_MN1, _DT(time[bar]), 2, iHigh_):
            return prev_calculated
        PP = (iHigh_[0] + iLow_[0] + iClose_[0]) / 3
        IndBuffer3[bar] = PP
    else:
        bar = _range_end(bar, 0 - 1, -1)
    SetRightPrice(0, daily_price_name, 0, time[0], IndBuffer1[0], _uint(indicator_color1))
    SetRightPrice(0, weekly_price_name, 0, time[0], IndBuffer2[0], _uint(indicator_color2))
    SetRightPrice(0, monthly_price_name, 0, time[0], IndBuffer3[0], _uint(indicator_color3))
    SetText(0, daily_text_name, 0, 'Daily Pivot', time[10], IndBuffer1[0], _uint(indicator_color1))
    SetText(0, weekly_text_name, 0, 'Weekly Pivot', time[10], IndBuffer2[0], _uint(indicator_color2))
    SetText(0, monthly_text_name, 0, 'Monthly Pivot', time[10], IndBuffer3[0], _uint(indicator_color3))
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WaddahAttarPivot(_MQL5Indicator):
    name = 'Waddah_Attar_Pivot'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

