"""Angle&Speed — converted from MQL5: MQL5 Indicators/Angle and Speed/Angle&Speed.mq5

индикатор расчитывает угол между трендовой линией и горизонталью
или
индикатор расчитывает среднюю скорость изменения цены
пунктов в минуту
нарисовать трендовую линию, задать ей цвет как в настройках индикатора
Copyright: Copyright 2025, MetaQuotes Ltd.; Link: https://www.mql5.com/ru/users/s22aa; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, MetaQuotes Ltd.', 'link': 'https://www.mql5.com/ru/users/s22aa', 'version': '1.02', 'window': 'separate', 'indicator_plots': 1, 'indicator_buffers': 1, 'indicator_minimum': 0.0}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Angle&Speed'}, 'levels': [], 'description': ['индикатор расчитывает угол между трендовой линией и горизонталью', 'или', 'индикатор расчитывает среднюю скорость изменения цены', 'пунктов в минуту', 'нарисовать трендовую линию, задать ей цвет как в настройках индикатора'], 'name': 'Angle&Speed', 'source': 'MQL5 Indicators/Angle and Speed/Angle&Speed.mq5', 'folder': 'Angle and Speed', 'inputs': [{'mql': 'variant', 'py': 'variant', 'param': 'variant', 'type': 'int', 'default': 0, 'label': '', 'sinput': True}, {'mql': 'trendColor', 'py': 'trendColor', 'param': None, 'type': 'color', 'default': 16777215, 'label': 'цвет трендовой линии', 'sinput': True}, {'mql': 'bar', 'py': 'bar', 'param': 'bar', 'type': 'int', 'default': 30, 'label': 'period', 'sinput': True}, {'mql': 'basement', 'py': 'basement', 'param': 'basement', 'type': 'bool', 'default': True, 'label': 'показывать подвал', 'sinput': True}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum var
angle = 0
average_speed = 1
_enum('var', {0: 'angle', 1: 'average_speed'})

# ---- inputs and global variables
variant = _input('variant', angle)
trendColor = _input('trendColor', clrWhite)  # цвет трендовой линии
bar = _input('bar', 30)  # period
basement = _input('basement', True)  # показывать подвал
prefix = ''
perSec = 0
speed = Arr(0, 0.0)

def OnInit():
    global perSec, prefix
    SetIndexBuffer(0, speed, INDICATOR_DATA)
    if not basement:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
        ChartSetInteger(0, CHART_HEIGHT_IN_PIXELS, ChartWindowFind(), 0)
    else:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
        ChartSetInteger(0, CHART_HEIGHT_IN_PIXELS, ChartWindowFind(), -1)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    name = ('angle (' if (variant == angle) else 'speed (') + _str(bar) + ') '
    IndicatorSetString(INDICATOR_SHORTNAME, name)
    prefix = _str(trendColor)
    perSec = PeriodSeconds(PERIOD_CURRENT)
    ChartSetInteger(0, CHART_EVENT_OBJECT_DELETE, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if prev_calculated <= 0:
        ArrayInitialize(speed, 0)
        limit = bar
    for i in range(limit, rates_total):
        _sw1 = variant
        if _sw1 == angle:
            speed[i] = (atan(_fdiv(MathAbs(_fdiv(close[i] - close[i - bar], Point())), bar * _idiv(perSec, 60))) * 180) / M_PI
            if (close[i] - close[i - bar]) < 0:
                speed[i] = 360 - speed[i]
        else:
            speed[i] = _fdiv(MathAbs(_fdiv(close[i] - close[i - bar], Point())), bar * _idiv(perSec, 60))
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_OBJECT_DRAG or id_ == CHARTEVENT_OBJECT_CHANGE:
        if ObjectGetInteger(0, sparam, OBJPROP_TYPE) == OBJ_TREND:
            if ObjectGetInteger(0, sparam, OBJPROP_COLOR) == trendColor:
                ObjectsDeleteAll(0, prefix + sparam, 0, OBJ_TEXT)
                price1 = ObjectGetDouble(0, sparam, OBJPROP_PRICE, 0)
                price2 = ObjectGetDouble(0, sparam, OBJPROP_PRICE, 1)
                pips = _fdiv(price2 - price1, Point())
                time1 = ObjectGetInteger(0, sparam, OBJPROP_TIME, 0)
                time2 = ObjectGetInteger(0, sparam, OBJPROP_TIME, 1)
                minut = float(time2 - time1) / 60
                txt = '90'
                if minut != 0:
                    _sw2 = variant
                    if _sw2 == angle:
                        Angle = (atan(_fdiv(pips, minut)) * 180) / M_PI
                        Angle = ((Angle + 180) if (minut < 0) else (Angle + 360) if (pips < 0) else Angle)
                        txt = DoubleToString(Angle, 2) + '°'
                    else:
                        txt = DoubleToString(MathAbs(_fdiv(pips, minut)), 2)
                name = prefix + sparam + _str(time2)
                TextCreate(name, time2, price2, txt)
                ObjectSetInteger(0, sparam, OBJPROP_TIME, 0, time1)
                ObjectSetInteger(0, sparam, OBJPROP_TIME, 1, time2)
                ObjectSetInteger(0, sparam, OBJPROP_BACK, False)
                ChartRedraw()
            else:
                ObjectsDeleteAll(0, prefix + sparam, 0, OBJ_TEXT)
                ChartRedraw()
    if id_ == CHARTEVENT_OBJECT_DELETE and StringFind(sparam, prefix) < 0:
        ObjectsDeleteAll(0, prefix + sparam, 0, OBJ_TEXT)
        ChartRedraw()

def OnDeinit(reason):
    if reason != REASON_CHARTCHANGE:
        ObjectsDeleteAll(0, prefix, 0, OBJ_TEXT)

def TextCreate(name, time, price, txt):
    ObjectCreate(0, name, OBJ_TEXT, 0, time, price)
    ObjectSetString(0, name, OBJPROP_TEXT, txt)
    ObjectSetInteger(0, name, OBJPROP_COLOR, trendColor)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
    ObjectSetInteger(0, name, OBJPROP_BACK, False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AngleSpeed(_MQL5Indicator):
    name = 'Angle&Speed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'variant': _Choice({0: 'angle', 1: 'average_speed'}, default=0),
        'bar': 30,  # period
        'basement': True,  # показывать подвал
    }

