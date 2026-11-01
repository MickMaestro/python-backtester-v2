"""i-morningrange — converted from MQL5: MQL5 Indicators/i-MorningRange/i-morningrange.mq5

the morning range indicator
Copyright: Copyright © 2006, Kim Igor V. aka KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Kim Igor V. aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [36095]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper Line', 2: 'Lower Line'}, 'levels': [], 'description': ['the morning range indicator'], 'name': 'i-morningrange', 'source': 'MQL5 Indicators/i-MorningRange/i-morningrange.mq5', 'folder': 'i-MorningRange', 'inputs': [{'mql': 'CheckTime', 'py': 'CheckTime', 'param': None, 'type': 'string', 'default': '08:00', 'label': 'Range check time', 'sinput': False}, {'mql': 'ShowHistory', 'py': 'ShowHistory', 'param': 'ShowHistory', 'type': 'bool', 'default': True, 'label': 'Show levels in history', 'sinput': False}, {'mql': 'NumberOfDays', 'py': 'NumberOfDays', 'param': 'NumberOfDays', 'type': 'int', 'default': 5, 'label': 'Number of days in history', 'sinput': False}, {'mql': 'ShowComment', 'py': 'ShowComment', 'param': 'ShowComment', 'type': 'bool', 'default': True, 'label': 'Show comments', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'Color1', 'py': 'Color1', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'resistance color', 'sinput': False}, {'mql': 'Color2', 'py': 'Color2', 'param': None, 'type': 'color', 'default': 36095, 'label': 'support color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CheckTime = _input('CheckTime', '08:00')  # Range check time
ShowHistory = _input('ShowHistory', True)  # Show levels in history
NumberOfDays = _input('NumberOfDays', 5)  # Number of days in history
ShowComment = _input('ShowComment', True)  # Show comments
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
Color1 = _input('Color1', clrBlue)  # resistance color
Color2 = _input('Color2', clrDarkOrange)  # support color
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _idiv(NumberOfDays * PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT))
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'i-MorningRange')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    Comment('')
    ObjectDelete(0, 'HLine' + _str(0))
    ObjectDelete(0, 'HLine' + _str(1))

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    for bar in range(limit, 0 - 1, -1):
        ExtLineBuffer1[bar] = 0.0
        ExtLineBuffer2[bar] = 0.0
    t1 = 0
    t2 = 0
    dt = 0
    p1 = 0.0
    p2 = 0.0
    b1 = 0
    b2 = 0
    sd = 0
    t1 = StringToTime(TimeToString(TimeCurrent(), TIME_DATE) + ' 00:00')
    t2 = StringToTime(TimeToString(TimeCurrent(), TIME_DATE) + ' ' + CheckTime)
    b1 = iBarShift_u("", 0, t1)
    b2 = iBarShift_u("", 0, t2)
    res = b1 - b2 + 1
    p1 = high[ArrayMaximum(high, b2, res)]
    p2 = low[ArrayMinimum(low, b2, res)]
    Width1 = PlotIndexGetInteger(PLOT_LINE_WIDTH, 0)
    Style1 = PlotIndexGetInteger(PLOT_LINE_STYLE, 0)
    SetHline(0, 'HLine' + _str(0), 0, p1, Color1, Style1, Width1, 'HLine' + _str(0))
    Width2 = PlotIndexGetInteger(PLOT_LINE_WIDTH, 1)
    Style2 = PlotIndexGetInteger(PLOT_LINE_STYLE, 1)
    SetHline(0, 'HLine' + _str(1), 0, p2, Color2, Style2, Width2, 'HLine' + _str(1))
    if ShowHistory:
        dt = decDateTradeDay(TimeCurrent())
        for i in range(0, NumberOfDays):
            DrawLines(dt, high, low)
            dt = decDateTradeDay(dt)
            tqq = MqlDateTime()
            TimeToStruct(dt, tqq)
            while tqq.day_of_week < 1 or tqq.day_of_week > 5:
                dt = decDateTradeDay(dt)
                TimeToStruct(dt, tqq)
    if ShowComment:
        Comment('CheckTime=' + CheckTime)
    return rates_total

def DrawLines(dt, High, Low):
    t1 = 0
    t2 = 0
    p1 = 0.0
    p2 = 0.0
    b1 = 0
    b2 = 0
    t1 = StringToTime(TimeToString(dt, TIME_DATE) + ' 00:00')
    t2 = StringToTime(TimeToString(dt, TIME_DATE) + ' ' + CheckTime)
    b1 = iBarShift_u("", 0, t1)
    b2 = iBarShift_u("", 0, t2)
    res = b1 - b2 + 1
    p1 = High[ArrayMaximum(High, b2, res)]
    p2 = Low[ArrayMinimum(Low, b2, res)]
    for rrr in range(b1, b2 - 1, -1):
        ExtLineBuffer1[rrr] = p1
        ExtLineBuffer2[rrr] = p2

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

def CreateHline(chart_id, name, nwin, price, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_HLINE, 0, 0, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetHline(chart_id, name, nwin, price, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateHline(chart_id, name, nwin, price, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, 0, price)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IMorningrange(_MQL5Indicator):
    name = 'i-morningrange'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ShowHistory': True,  # Show levels in history
        'NumberOfDays': 5,  # Number of days in history
        'ShowComment': True,  # Show comments
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

