"""i-sessions — converted from MQL5: MQL5 Indicators/i-Sessions/i-sessions.mq5

The trade sessions indicator
Copyright: Copyright © 2006, Kim Igor V. aka KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Kim Igor V. aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['The trade sessions indicator'], 'name': 'i-sessions', 'source': 'MQL5 Indicators/i-Sessions/i-sessions.mq5', 'folder': 'i-Sessions', 'inputs': [{'mql': 'NumberOfDays', 'py': 'NumberOfDays', 'param': 'NumberOfDays', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'S1Begin', 'py': 'S1Begin', 'param': None, 'type': 'string', 'default': '00:55', 'label': '', 'sinput': False}, {'mql': 'S1End', 'py': 'S1End', 'param': None, 'type': 'string', 'default': '03:55', 'label': '', 'sinput': False}, {'mql': 'S1Color', 'py': 'S1Color', 'param': None, 'type': 'color', 'default': 5197615, 'label': '', 'sinput': False}, {'mql': 'S2Begin', 'py': 'S2Begin', 'param': None, 'type': 'string', 'default': '03:55', 'label': '', 'sinput': False}, {'mql': 'S2End', 'py': 'S2End', 'param': None, 'type': 'string', 'default': '06:55', 'label': '', 'sinput': False}, {'mql': 'S2Color', 'py': 'S2Color', 'param': None, 'type': 'color', 'default': 5197615, 'label': '', 'sinput': False}, {'mql': 'S3Begin', 'py': 'S3Begin', 'param': None, 'type': 'string', 'default': '06:55', 'label': '', 'sinput': False}, {'mql': 'S3End', 'py': 'S3End', 'param': None, 'type': 'string', 'default': '09:55', 'label': '', 'sinput': False}, {'mql': 'S3Color', 'py': 'S3Color', 'param': None, 'type': 'color', 'default': 5197615, 'label': '', 'sinput': False}, {'mql': 'S4Begin', 'py': 'S4Begin', 'param': None, 'type': 'string', 'default': '09:55', 'label': '', 'sinput': False}, {'mql': 'S4End', 'py': 'S4End', 'param': None, 'type': 'string', 'default': '12:55', 'label': '', 'sinput': False}, {'mql': 'S4Color', 'py': 'S4Color', 'param': None, 'type': 'color', 'default': 5197615, 'label': '', 'sinput': False}, {'mql': 'S5Begin', 'py': 'S5Begin', 'param': None, 'type': 'string', 'default': '12:55', 'label': '', 'sinput': False}, {'mql': 'S5End', 'py': 'S5End', 'param': None, 'type': 'string', 'default': '15:55', 'label': '', 'sinput': False}, {'mql': 'S5Color', 'py': 'S5Color', 'param': None, 'type': 'color', 'default': 5197615, 'label': '', 'sinput': False}, {'mql': 'S6Begin', 'py': 'S6Begin', 'param': None, 'type': 'string', 'default': '15:55', 'label': '', 'sinput': False}, {'mql': 'S6End', 'py': 'S6End', 'param': None, 'type': 'string', 'default': '18:55', 'label': '', 'sinput': False}, {'mql': 'S6Color', 'py': 'S6Color', 'param': None, 'type': 'color', 'default': 5197615, 'label': '', 'sinput': False}, {'mql': 'S7Begin', 'py': 'S7Begin', 'param': None, 'type': 'string', 'default': '18:55', 'label': '', 'sinput': False}, {'mql': 'S7End', 'py': 'S7End', 'param': None, 'type': 'string', 'default': '21:55', 'label': '', 'sinput': False}, {'mql': 'S7Color', 'py': 'S7Color', 'param': None, 'type': 'color', 'default': 5197615, 'label': '', 'sinput': False}, {'mql': 'S8Begin', 'py': 'S8Begin', 'param': None, 'type': 'string', 'default': '21:55', 'label': '', 'sinput': False}, {'mql': 'S8End', 'py': 'S8End', 'param': None, 'type': 'string', 'default': '23:55', 'label': '', 'sinput': False}, {'mql': 'S8Color', 'py': 'S8Color', 'param': None, 'type': 'color', 'default': 5197615, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
NumberOfDays = _input('NumberOfDays', 50)
S1Begin = _input('S1Begin', '00:55')
S1End = _input('S1End', '03:55')
S1Color = _input('S1Color', clrDarkSlateGray)
S2Begin = _input('S2Begin', '03:55')
S2End = _input('S2End', '06:55')
S2Color = _input('S2Color', clrDarkSlateGray)
S3Begin = _input('S3Begin', '06:55')
S3End = _input('S3End', '09:55')
S3Color = _input('S3Color', clrDarkSlateGray)
S4Begin = _input('S4Begin', '09:55')
S4End = _input('S4End', '12:55')
S4Color = _input('S4Color', clrDarkSlateGray)
S5Begin = _input('S5Begin', '12:55')
S5End = _input('S5End', '15:55')
S5Color = _input('S5Color', clrDarkSlateGray)
S6Begin = _input('S6Begin', '15:55')
S6End = _input('S6End', '18:55')
S6Color = _input('S6Color', clrDarkSlateGray)
S7Begin = _input('S7Begin', '18:55')
S7End = _input('S7End', '21:55')
S7Color = _input('S7Color', clrDarkSlateGray)
S8Begin = _input('S8Begin', '21:55')
S8End = _input('S8End', '23:55')
S8Color = _input('S8Color', clrDarkSlateGray)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _idiv(NumberOfDays * PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT))
    IndicatorSetString(INDICATOR_SHORTNAME, 'i-Sessions')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    for i in range(0, NumberOfDays):
        ObjectDelete(0, 'S1' + _str(i))
        ObjectDelete(0, 'S2' + _str(i))
        ObjectDelete(0, 'S3' + _str(i))
        ObjectDelete(0, 'S4' + _str(i))
        ObjectDelete(0, 'S5' + _str(i))
        ObjectDelete(0, 'S6' + _str(i))
        ObjectDelete(0, 'S7' + _str(i))
        ObjectDelete(0, 'S8' + _str(i))
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    dt = TimeCurrent()
    for i in range(0, NumberOfDays):
        DrawRectangle(dt, 'S1' + _str(i), S1Begin, S1End, S1Color, high, low)
        DrawRectangle(dt, 'S2' + _str(i), S2Begin, S2End, S2Color, high, low)
        DrawRectangle(dt, 'S3' + _str(i), S3Begin, S3End, S3Color, high, low)
        DrawRectangle(dt, 'S4' + _str(i), S4Begin, S4End, S4Color, high, low)
        DrawRectangle(dt, 'S5' + _str(i), S5Begin, S5End, S5Color, high, low)
        DrawRectangle(dt, 'S6' + _str(i), S6Begin, S6End, S6Color, high, low)
        DrawRectangle(dt, 'S7' + _str(i), S7Begin, S7End, S7Color, high, low)
        DrawRectangle(dt, 'S8' + _str(i), S8Begin, S8End, S8Color, high, low)
        dt = decDateTradeDay(dt)
        ttt = MqlDateTime()
        TimeToStruct(dt, ttt)
        while ttt.day_of_week > 5:
            dt = decDateTradeDay(dt)
            TimeToStruct(dt, ttt)
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


class ISessions(_MQL5Indicator):
    name = 'i-sessions'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'NumberOfDays': 50,
    }

