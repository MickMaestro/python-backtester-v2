"""i-paramonworktime — converted from MQL5: MQL5 Indicators/i-ParamonWorkTime/i-paramonworktime.mq5

The iParamon WorkTime indicator
Copyright: Copyright © 2006, Kim Igor V. aka KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Kim Igor V. aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['The iParamon WorkTime indicator'], 'name': 'i-paramonworktime', 'source': 'MQL5 Indicators/i-ParamonWorkTime/i-paramonworktime.mq5', 'folder': 'i-ParamonWorkTime', 'inputs': [{'mql': 'NumberOfDays', 'py': 'NumberOfDays', 'param': 'NumberOfDays', 'type': 'int', 'default': 5, 'label': 'Number of days in history', 'sinput': False}, {'mql': 'Begin_1', 'py': 'Begin_1', 'param': None, 'type': 'string', 'default': '08:00', 'label': 'Start time 1', 'sinput': False}, {'mql': 'End_1', 'py': 'End_1', 'param': None, 'type': 'string', 'default': '11:00', 'label': 'End time 1', 'sinput': False}, {'mql': 'Color_1', 'py': 'Color_1', 'param': None, 'type': 'color', 'default': 9109504, 'label': 'Paramon color 1', 'sinput': False}, {'mql': 'Begin_2', 'py': 'Begin_2', 'param': None, 'type': 'string', 'default': '14:00', 'label': 'Start time 2', 'sinput': False}, {'mql': 'End_2', 'py': 'End_2', 'param': None, 'type': 'string', 'default': '17:00', 'label': 'End time 2', 'sinput': False}, {'mql': 'Color_2', 'py': 'Color_2', 'param': None, 'type': 'color', 'default': 8388736, 'label': 'Paramon color 2', 'sinput': False}, {'mql': 'HighRange', 'py': 'HighRange', 'param': 'HighRange', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
NumberOfDays = _input('NumberOfDays', 5)  # Number of days in history
Begin_1 = _input('Begin_1', '08:00')  # Start time 1
End_1 = _input('End_1', '11:00')  # End time 1
Color_1 = _input('Color_1', clrDarkBlue)  # Paramon color 1
Begin_2 = _input('Begin_2', '14:00')  # Start time 2
End_2 = _input('End_2', '17:00')  # End time 2
Color_2 = _input('Color_2', clrPurple)  # Paramon color 2
HighRange = _input('HighRange', False)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _idiv(NumberOfDays * PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT))
    IndicatorSetString(INDICATOR_SHORTNAME, 'i-ParamonWorkTime')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    for i in range(0, NumberOfDays):
        ObjectDelete(0, 'PWT1' + _str(i))
        ObjectDelete(0, 'PWT2' + _str(i))
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    dt = TimeCurrent()
    for i in range(0, NumberOfDays):
        DrawRectangle(dt, 'PWT1' + _str(i), Begin_1, End_1, Color_1, high, low)
        DrawRectangle(dt, 'PWT2' + _str(i), Begin_2, End_2, Color_2, high, low)
        dt = decDateTradeDay(dt)
        ttt = MqlDateTime()
        TimeToStruct(dt, ttt)
        while ttt.day_of_week > 5:
            dt = decDateTradeDay(dt)
            TimeToStruct(dt, ttt)
    ChartRedraw(0)
    return rates_total

def DrawRectangle(dt, no, tb, te, clr, High, Low):
    t1 = 0
    t2 = 0
    p1 = 0.0
    p2 = 0.0
    b1 = 0
    b2 = 0
    t1 = StringToTime(TimeToString(dt, TIME_DATE) + ' ' + tb)
    t2 = StringToTime(TimeToString(dt, TIME_DATE) + ' ' + te)
    b1 = iBarShift_u("", 0, t1)
    b2 = iBarShift_u("", 0, t2)
    res = b1 - b2
    extr = MathMax(0, ArrayMaximum(High, b2, res))
    p1 = High[extr]
    extr = MathMax(0, ArrayMinimum(Low, b2, res))
    p2 = Low[extr]
    if not HighRange:
        p1 = 0.0
        p2 = 2 * p2
    SetRectangle(0, no, 0, t1, p1, t2, p2, clr, False, no)

def decDateTradeDay(dt):
    ttt = MqlDateTime()
    TimeToStruct(dt, ttt)
    ty = ttt.year
    tm = ttt.mon
    td = ttt.day
    th = ttt.hour
    ti = ttt.min
    td -= 1
    if td == 0:
        tm -= 1
        if not tm:
            ty -= 1
            tm = 12
        if (((((tm == 1 or tm == 3) or tm == 5) or tm == 7) or tm == 8) or tm == 10) or tm == 12:
            td = 31
        if tm == 2:
            if not MathMod(ty, 4):
                td = 29
            else:
                td = 28
        if ((tm == 4 or tm == 6) or tm == 9) or tm == 11:
            td = 30
    text = Box("")
    StringConcatenate(text, ty, '.', tm, '.', td, ' ', th, ':', ti)
    return StringToTime(text.v)

def iBarShift_u(symbol, timeframe, time):
    if time < 0:
        return -1
    Arr_ = Arr(0, 0)
    time1 = 0
    time1 = SeriesInfoInteger(symbol, timeframe, SERIES_LASTBAR_DATE)
    if CopyTime(symbol, timeframe, _DT(time), _DT(time1), Arr_) > 0:
        size = ArraySize(Arr_)
        return size - 1
    else:
        return -1

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IParamonworktime(_MQL5Indicator):
    name = 'i-paramonworktime'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'NumberOfDays': 5,  # Number of days in history
        'HighRange': False,
    }

