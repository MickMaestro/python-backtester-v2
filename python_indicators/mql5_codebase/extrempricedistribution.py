"""ExtremPriceDistribution — converted from MQL5: MQL5 Indicators/ExtremPriceDistribution/ExtremPriceDistribution.mq5

Индикатор показывает гистограмму распределения экстемальных цен за период в барах от текущего
Copyright: Copyright © 2012, cmillion@narod.ru; Link: http://cmillion.narod.ru

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, cmillion@narod.ru', 'link': 'http://cmillion.narod.ru', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Индикатор показывает гистограмму распределения экстемальных цен за период в барах от текущего'], 'name': 'ExtremPriceDistribution', 'source': 'MQL5 Indicators/ExtremPriceDistribution/ExtremPriceDistribution.mq5', 'folder': 'ExtremPriceDistribution', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'ExtremPriceDistribution', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 3000, 'label': 'период расчёта', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': -300, 'label': 'сдвиг начального уровня отрисовки гистограммы', 'sinput': False}, {'mql': 'Dev', 'py': 'Dev', 'param': 'Dev', 'type': 'double', 'default': 30.0, 'label': 'масштаб отрисовки гистограммы', 'sinput': False}, {'mql': 'PrColor', 'py': 'PrColor', 'param': None, 'type': 'color', 'default': 65280, 'label': 'цвет количества цен', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SirName = _input('SirName', 'ExtremPriceDistribution')  # Первая часть имени графических объектов
iPeriod = _input('iPeriod', 3000)  # период расчёта
Shift = _input('Shift', -300)  # сдвиг начального уровня отрисовки гистограммы
Dev = _input('Dev', 30.0)  # масштаб отрисовки гистограммы
PrColor = _input('PrColor', clrLime)  # цвет количества цен
min_rates_total = 0
iperiod = 0
Ind_Handle = 0

def OnInit():
    global iperiod, min_rates_total
    min_rates_total = _int(iPeriod)
    iperiod = _int(iPeriod)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'ExtremPriceDistribution'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, SirName, -1, OBJ_TREND)
    Comment('')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global iperiod
    to_copy = 0
    Pr = 0
    limit = 0
    max_ = 0.0
    min_ = 0.0
    P = 0.0
    txt = Box("")
    name = Box("")
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    if not limit:
        return rates_total
    to_copy = limit + 1
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    TimeSt = time[0] + (PeriodSeconds() * Shift)
    max_ = high[ArrayMaximum(high, 0, iperiod)]
    min_ = low[ArrayMinimum(low, 0, iperiod)]
    iperiod = MathMin(iperiod, rates_total - 1)
    txt.v = ''
    StringConcatenate(txt, 'Баров в истории ', iperiod, ' с ', TimeToString(time[iperiod], TIME_DATE), '\nМаксимум ', DoubleToString(max_, Digits()), '\nМинимум ', DoubleToString(min_, Digits()))
    Comment(txt.v, '\n', 'Старт расчета ', TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS))
    Pr = _int(_fdiv(max_ - min_, Point()))
    Price = Arr(0, 0.0)
    ArrayResize(Price, Pr)
    ArrayInitialize(Price, 0)
    for bar in range(1, iperiod + 1):
        for kkk in range(0, Pr):
            P = NormalizeDouble(min_ + (kkk * Point()), Digits())
            if low[bar] == P or high[bar] == P:
                Price[kkk] += 1
    for rrr in range(0, Pr):
        P = NormalizeDouble(min_ + (rrr * Point()), Digits())
        name.v = ''
        StringConcatenate(name, SirName, ' ', P)
        SetTline(0, name.v, 0, TimeSt, P, _long(TimeSt + (Price[rrr] * Dev * PeriodSeconds())), P, PrColor, 0, 3)
    ChartRedraw(0)
    return rates_total

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, False)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, False)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width)
    else:
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
        ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
        ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ExtremPriceDistribution(_MQL5Indicator):
    name = 'ExtremPriceDistribution'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 3000,  # период расчёта
        'Shift': -300,  # сдвиг начального уровня отрисовки гистограммы
        'Dev': 30.0,  # масштаб отрисовки гистограммы
    }

