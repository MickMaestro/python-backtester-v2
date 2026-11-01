"""price — converted from MQL5: MQL5 Indicators/Price/price.mq5

Ценовая метка
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Ценовая метка'], 'name': 'price', 'source': 'MQL5 Indicators/Price/price.mq5', 'folder': 'Price', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'Price', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Способ определения цены', 'sinput': False}, {'mql': 'Digits_', 'py': 'Digits_', 'param': 'Digits_', 'type': 'uint', 'default': 0, 'label': 'Разряд округления', 'sinput': False}, {'mql': 'Color_', 'py': 'Color_', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Цвет цены', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'uint', 'default': 2, 'label': 'Размер ценовых меток', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 10, 'label': 'Сдвиг ценовых меток по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum PriceMode
BID = 0
ASK = 1
_enum('PriceMode', {0: 'BID', 1: 'ASK'})

# ---- inputs and global variables
SirName = _input('SirName', 'Price')  # Первая часть имени графических объектов
Price = _input('Price', BID)  # Способ определения цены
Digits_ = _input('Digits_', 0)  # Разряд округления
Color_ = _input('Color_', clrMagenta)  # Цвет цены
FontSize = _input('FontSize', 2)  # Размер ценовых меток
Shift = _input('Shift', 10)  # Сдвиг ценовых меток по горизонтали в барах
clr = 0
Normalize = 0
ObjectNames = ""
PointPow10 = 0.0

def OnInit():
    global Normalize, ObjectNames, PointPow10
    ObjectNames = SirName + ' PriceLable'
    PointPow10 = Point() * MathPow(10, Digits_)
    Normalize = _int(Digits() - Digits_)

def OnDeinit(reason):
    ObjectDelete(0, ObjectNames)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, False)
    ArraySetAsSeries(time, False)
    price = 0.0
    if Price == BID:
        price = close[rates_total - 1]
    else:
        ArraySetAsSeries(spread, False)
        price = close[rates_total - 1] + (Point() * spread[rates_total - 1])
    res = NormalizeDouble(PointPow10 * MathCeil(_fdiv(price, PointPow10)), Normalize)
    time0 = time[rates_total - 1] + (PeriodSeconds() * Shift)
    info = ObjectNames + ' ' + DoubleToString(res, Normalize)
    SetRightPrice(0, ObjectNames, 0, time0, res, Color_, FontSize, info)
    ChartRedraw(0)
    return rates_total

def CreateRightPrice(chart_id, name, nwin, time, price, Color, fontsize, text):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, fontsize)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, False)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, False)

def SetRightPrice(chart_id, name, nwin, time, price, Color, fontsize, text):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color, fontsize, text)
    else:
        ObjectMove(chart_id, name, 0, time, price)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceIndicator(_MQL5Indicator):
    name = 'price'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Price': _Choice({0: 'биды', 1: 'аски'}, default=0),  # Способ определения цены
        'Digits_': 0,  # Разряд округления
        'FontSize': 2,  # Размер ценовых меток
        'Shift': 10,  # Сдвиг ценовых меток по горизонтали в барах
    }

