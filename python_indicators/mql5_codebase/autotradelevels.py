"""AutoTradeLevels — converted from MQL5: MQL5 Indicators/AutoTradeLevels/AutoTradeLevels.mq5

Индикатор производит подмену всех значков совершённых сделок покупки и продажи
Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Индикатор производит подмену всех значков совершённых сделок покупки и продажи'], 'name': 'AutoTradeLevels', 'source': 'MQL5 Indicators/AutoTradeLevels/AutoTradeLevels.mq5', 'folder': 'AutoTradeLevels', 'inputs': [{'mql': 'Sirname', 'py': 'Sirname', 'param': None, 'type': 'string', 'default': 'AutoTradeLevels', 'label': 'Название для меток индикатора', 'sinput': False}, {'mql': 'Len', 'py': 'Len', 'param': 'Len', 'type': 'uint', 'default': 3, 'label': 'Длина ценовых уровней в количестве свечей', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Sirname = _input('Sirname', 'AutoTradeLevels')  # Название для меток индикатора
Len = _input('Len', 3)  # Длина ценовых уровней в количестве свечей

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'AutoTradeLevels')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'AutoTradeLevels', -1, -1)
    ChartRedraw(None)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 1:
        return 0
    total = ObjectsTotal(0, 0, OBJ_ARROW_BUY)
    for kkk in range(total - 1, 0 - 1, -1):
        name = ObjectName(0, kkk, 0, OBJ_ARROW_BUY)
        if StringSubstr(name, 0, 9) == 'autotrade':
            Time = ObjectGetInteger(0, name, OBJPROP_TIME, 0)
            Price = ObjectGetDouble(0, name, OBJPROP_PRICE, 0)
            Color = _uint(ObjectGetInteger(0, name, OBJPROP_COLOR))
            SetTline(0, 'AutoTradeLevels' + name, 0, Time, Price, Time + (MathMax(1, Len) * PeriodSeconds()), Price, Color, 0, 2, name)
    total = ObjectsTotal(0, 0, OBJ_ARROW_SELL)
    for kkk in range(total - 1, 0 - 1, -1):
        name = ObjectName(0, kkk, 0, OBJ_ARROW_SELL)
        if StringSubstr(name, 0, 9) == 'autotrade':
            Time = ObjectGetInteger(0, name, OBJPROP_TIME, 0)
            Price = ObjectGetDouble(0, name, OBJPROP_PRICE, 0)
            Color = _uint(ObjectGetInteger(0, name, OBJPROP_COLOR))
            SetTline(0, 'AutoTradeLevels' + name, 0, Time, Price, Time + (MathMax(1, Len) * PeriodSeconds()), Price, Color, 0, 2, name)
    ChartRedraw(0)
    return rates_total

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, False)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AutoTradeLevels(_MQL5Indicator):
    name = 'AutoTradeLevels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Len': 3,  # Длина ценовых уровней в количестве свечей
    }

