"""speedometer — converted from MQL5: MQL5 Indicators/Speedometer/speedometer.mq5

Copyright: Copyright 2016, AM2; Link: http://www.forexsystems.biz; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, AM2', 'link': 'http://www.forexsystems.biz', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'speedometer', 'source': 'MQL5 Indicators/Speedometer/speedometer.mq5', 'folder': 'Speedometer', 'inputs': [{'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 12, 'label': 'Размер шрифта', 'sinput': False}, {'mql': 'FontName', 'py': 'FontName', 'param': None, 'type': 'string', 'default': 'Arial', 'label': 'Наименование шрифта', 'sinput': False}, {'mql': 'ClrWay', 'py': 'ClrWay', 'param': None, 'type': 'color', 'default': 0, 'label': 'Цвет метки - путь цены в пунктах', 'sinput': False}, {'mql': 'ClrSpeed', 'py': 'ClrSpeed', 'param': None, 'type': 'color', 'default': 0, 'label': 'Цвет метки - скорость пункты в секунду', 'sinput': False}, {'mql': 'ClrTime', 'py': 'ClrTime', 'param': None, 'type': 'color', 'default': 0, 'label': 'Цвет метки - изменение времени в микросекундах', 'sinput': False}, {'mql': 'SpeedSound', 'py': 'SpeedSound', 'param': 'SpeedSound', 'type': 'int', 'default': 20, 'label': 'Оповещение превышения скорости', 'sinput': False}, {'mql': 'Corner', 'py': 'Corner', 'param': 'Corner', 'type': 'int', 'default': 3, 'label': 'Угол для вывода информации', 'sinput': False}, {'mql': 'AlertOn', 'py': 'AlertOn', 'param': 'AlertOn', 'type': 'bool', 'default': True, 'label': 'Включение оповещения', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Red = 0x0000FF  # MQL4 colour name
White = 0xFFFFFF  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name

# ---- inputs and global variables
FontSize = _input('FontSize', 12)  # Размер шрифта
FontName = _input('FontName', 'Arial')  # Наименование шрифта
SpeedSound = _input('SpeedSound', 20)  # Оповещение превышения скорости
Corner = _input('Corner', CORNER_RIGHT_UPPER)  # Угол для вывода информации
AlertOn = _input('AlertOn', True)  # Включение оповещения
one = True
LastBid = 0.0
LastTime = 0
T_v = 0

def OnInit():
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    ObjectDelete(0, 'Label1')
    ObjectDelete(0, 'Label2')
    ObjectDelete(0, 'Label3')

def PutLabel(name, text, x, y, clr):
    ObjectDelete(0, name)
    ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(0, name, OBJPROP_CORNER, Corner)
    ObjectSetString(0, name, OBJPROP_TEXT, text)
    ObjectSetString(0, name, OBJPROP_FONT, FontName)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LastBid, LastTime, T_v, one
    speed = 0.0
    way = 0.0
    Bid = 0.0
    dt = 0
    T_v = GetMicrosecondCount()
    Bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    if LastBid != Bid:
        dt = T_v - LastTime
        way = _fdiv(Bid - LastBid, Point())
        speed = _fdiv(way, dt)
        if Corner == CORNER_RIGHT_UPPER or Corner == CORNER_RIGHT_LOWER:
            PutLabel('Label1', 'Way: ' + _str(NormalizeDouble(way, 2)), 150, 30, ClrWay)
            PutLabel('Label2', 'Time: ' + _str(NormalizeDouble(dt, 2)), 150, 55, ClrTime)
            PutLabel('Label3', 'Speed: ' + _str(NormalizeDouble(speed * 1000000, 2)), 150, 80, ClrSpeed)
        else:
            PutLabel('Label1', 'Way: ' + _str(NormalizeDouble(way, 2)), 20, 30, ClrWay)
            PutLabel('Label2', 'Time: ' + _str(NormalizeDouble(dt, 2)), 20, 55, ClrTime)
            PutLabel('Label3', 'Speed: ' + _str(NormalizeDouble(speed * 1000000, 2)), 20, 80, ClrSpeed)
    LastTime = T_v
    LastBid = Bid
    if MathAbs(speed * 1000000) < SpeedSound:
        one = True
    if (MathAbs(speed * 1000000) > SpeedSound and one) and AlertOn:
        Alert('Скорость выше ' + _str(SpeedSound) + ' пунктов в секунду!')
        SendNotification('Скорость выше: ' + _str(SpeedSound) + ' пунктов в секунду!')
        SendMail('Сигнал индикатора', 'Скорость выше: ' + _str(SpeedSound) + ' пунктов в секунду!')
        one = False
    return rates_total

# ---- global variables initialised from expressions
ClrWay = _input('ClrWay', _uint(Red))  # Цвет метки - путь цены в пунктах
ClrSpeed = _input('ClrSpeed', _uint(Yellow))  # Цвет метки - скорость пункты в секунду
ClrTime = _input('ClrTime', _uint(White))  # Цвет метки - изменение времени в микросекундах


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Speedometer(_MQL5Indicator):
    name = 'speedometer'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FontSize': 12,  # Размер шрифта
        'SpeedSound': 20,  # Оповещение превышения скорости
        'Corner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Угол для вывода информации
        'AlertOn': True,  # Включение оповещения
    }

