"""cm_ind_level_cndl — converted from MQL5: MQL5 Indicators/cm_ind_level_cndl/cm_ind_level_cndl.mq5

Индикатор показывает точку разворота цены
Copyright: Copyright © 2014, cmillion@narod.ru; Link: http://cmillion.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, cmillion@narod.ru', 'link': 'http://cmillion.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Индикатор показывает точку разворота цены'], 'name': 'cm_ind_level_cndl', 'source': 'MQL5 Indicators/cm_ind_level_cndl/cm_ind_level_cndl.mq5', 'folder': 'cm_ind_level_cndl', 'inputs': [{'mql': 'level_name', 'py': 'level_name', 'param': None, 'type': 'string', 'default': 'cm_ind_level_cndl', 'label': 'первая часть имени графических объектов', 'sinput': False}, {'mql': 'Candles', 'py': 'Candles', 'param': 'Candles', 'type': 'uint', 'default': 5, 'label': 'сколько свечей зацепила цена', 'sinput': False}, {'mql': 'History', 'py': 'History', 'param': 'History', 'type': 'uint', 'default': 50, 'label': 'на каком промежутке ищем', 'sinput': False}, {'mql': 'buy_level_color', 'py': 'buy_level_color', 'param': None, 'type': 'color', 'default': 65280, 'label': 'цвет покупок', 'sinput': False}, {'mql': 'sell_level_color', 'py': 'sell_level_color', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет продаж', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
level_name = _input('level_name', 'cm_ind_level_cndl')  # первая часть имени графических объектов
Candles = _input('Candles', 5)  # сколько свечей зацепила цена
History = _input('History', 50)  # на каком промежутке ищем
buy_level_color = _input('buy_level_color', clrLime)  # цвет покупок
sell_level_color = _input('sell_level_color', clrMagenta)  # цвет продаж
UP = ""
DN = ""
UP1 = ""
DN1 = ""
min_rates_total = 0

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

def OnInit():
    global DN, DN1, UP, UP1, min_rates_total
    DN1 = level_name
    UP1 = DN1
    DN = UP1
    UP = DN
    UP += 'UP'
    DN += 'DN'
    UP1 += 'UP1'
    DN1 += 'DN1'
    min_rates_total = _int(History)

def OnDeinit(reason):
    ObjectsDeleteAll(None, level_name, -1, OBJ_TREND)
    ChartRedraw(None)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    kkk = 0
    iii = _int(History) - 1
    while iii >= 0:
        H = high[iii]
        L = MathMax(open[iii], close[iii])
        YES = True
        kkk = iii
        for kkk in range(kkk, iii + _int(Candles)):
            if high[kkk] < L or MathMax(open[kkk], close[kkk]) > H:
                YES = False
                break
            if H > high[kkk]:
                H = high[kkk]
            if L < MathMax(open[kkk], close[kkk]):
                L = MathMax(open[kkk], close[kkk])
        else:
            kkk = _range_end(kkk, iii + _int(Candles), 1)
        if YES:
            SetTline(0, UP, 0, time[kkk], H, time[iii], H, buy_level_color, STYLE_SOLID, 5, 'buy_level')
            SetTline(0, UP1, 0, time[kkk], H, time[0], H, buy_level_color, STYLE_SOLID, 1, 'buy_level')
        H = MathMin(open[iii], close[iii])
        L = low[iii]
        YES = True
        kkk = iii
        for kkk in range(kkk, iii + _int(Candles)):
            if MathMin(open[kkk], close[kkk]) < L or low[kkk] > H:
                YES = False
                break
            if H > MathMin(open[kkk], close[kkk]):
                H = MathMin(open[kkk], close[kkk])
            if L < low[kkk]:
                L = low[kkk]
        else:
            kkk = _range_end(kkk, iii + _int(Candles), 1)
        if YES:
            SetTline(0, DN, 0, time[kkk], L, time[iii], L, sell_level_color, STYLE_SOLID, 5, 'sell_level')
            SetTline(0, DN1, 0, time[kkk], L, time[0], L, sell_level_color, STYLE_SOLID, 1, 'sell_level')
        iii -= 1
    ChartRedraw(None)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CmIndLevelCndl(_MQL5Indicator):
    name = 'cm_ind_level_cndl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Candles': 5,  # сколько свечей зацепила цена
        'History': 50,  # на каком промежутке ищем
    }

