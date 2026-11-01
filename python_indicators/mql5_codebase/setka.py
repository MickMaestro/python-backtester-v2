"""setka — converted from MQL5: MQL5 Indicators/Setka (grid)/setka.mq5

Copyright: Privalov S.V.; Link: https://login.mql5.com/en/users/Prival; Version: 3.08

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Privalov S.V.', 'link': 'https://login.mql5.com/en/users/Prival', 'version': '3.08', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'setka', 'source': 'MQL5 Indicators/Setka (grid)/setka.mq5', 'folder': 'Setka (grid)', 'inputs': [{'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'int', 'default': 250, 'label': 'vertical grid step in points', 'sinput': False}, {'mql': 'Figure', 'py': 'Figure', 'param': 'Figure', 'type': 'int', 'default': 1000, 'label': 'figure step', 'sinput': False}, {'mql': 'MaxBars', 'py': 'MaxBars', 'param': 'MaxBars', 'type': 'int', 'default': 0, 'label': 'bars in history (0 - all history)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
DeepPink = 0x9314FF  # MQL4 colour name
DimGray = 0x696969  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
RoyalBlue = 0xE16941  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name

# ---- inputs and global variables
Step = _input('Step', 250)  # vertical grid step in points
Figure = _input('Figure', 1000)  # figure step
MaxBars = _input('MaxBars', 0)  # bars in history (0 - all history)
old_Times = Arr.of([0], fill=0, dyn=False, size=21)  # array for old times

def CheckOtherTimeFrames(symbol):
    ctm = Arr(1, 0, dyn=False)
    checktime = TimeCurrent() - (86400 * 60)
    res = True
    if CopyTime(symbol, PERIOD_H1, _DT(checktime), 1, ctm) != 1:
        res = False
    if CopyTime(symbol, PERIOD_D1, _DT(checktime), 1, ctm) != 1:
        res = False
    if CopyTime(symbol, PERIOD_W1, _DT(checktime), 1, ctm) != 1:
        res = False
    if CopyTime(symbol, PERIOD_MN1, _DT(checktime), 1, ctm) != 1:
        res = False
    return res

def OnInit():
    CheckOtherTimeFrames(Symbol())
    EventSetTimer(25)
    return 0

def OnDeinit(reason):
    ObjectsDeleteAll(0, 0, OBJ_HLINE)
    ObjectsDeleteAll(0, 0, OBJ_VLINE)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    str_ = MqlDateTime()
    line_name = Box('')
    line_counter = 0
    start_pos = 0
    start_time = GetTickCount()
    if rates_total < 0:
        return 0
    if not CheckOtherTimeFrames(Symbol()):
        Print('Other timeframes are not ready...')
        return prev_calculated
    if prev_calculated == 0:
        start_time = GetTickCount()
        ObjectsDeleteAll(0, 0, OBJ_VLINE)
        ObjectsDeleteAll(0, 0, OBJ_HLINE)
        Ris_H_Line()
        ArrayInitialize(old_Times, 0)
        if MaxBars != 0:
            if MaxBars < rates_total:
                start_pos = rates_total - MaxBars
    else:
        start_pos = prev_calculated - 1
    for i in range(start_pos, rates_total):
        line_color = 0
        if Period() < PERIOD_H1:
            if isNewBar_i(time[i], PERIOD_H1) and Period() < PERIOD_M30:
                line_color = new_hour
        if Period() < PERIOD_D1:
            if isNewBar_i(time[i], PERIOD_D1) and Period() < PERIOD_H4:
                line_color = new_day
        if Period() < PERIOD_W1:
            if isNewBar_i(time[i], PERIOD_W1) and Period() < PERIOD_D1:
                line_color = new_week
        if Period() < PERIOD_MN1:
            if isNewBar_i(time[i], PERIOD_MN1) and Period() < PERIOD_MN1:
                line_color = new_mon
        if line_color != 0:
            line_counter += 1
            TimeToStruct(time[i], str_)
            StringConcatenate(line_name, IntegerToString(str_.hour, 2, 48), ':', IntegerToString(str_.min, 2, 48), '_N', line_counter)
            SetVLine(line_name.v, time[i], line_color)
    if Period() < PERIOD_M30:
        if ObjectFind(0, 'VLine_0') >= 0:
            ObjectDelete(0, 'VLine_0')
        TimeToStruct(time[rates_total - 1], str_)
        SetVLine('VLine_0', time[rates_total - 1] + (60 * (60 - str_.min)), new_hour)
    if prev_calculated == 0:
        Print('Failure or first call Time=', DoubleToString((GetTickCount() - start_time) / 1000.0, 1), 'sec for ', rates_total, ' bars  ObjectsTotal=', ObjectsTotal(0, 0, -1), ' MaxBars=', MaxBars)
    return rates_total

def SetVLine(nm, t1, cl=_uint(Red)):
    if t1 <= 0:
        return
    if ObjectFind(0, nm) < 0:
        ObjectCreate(0, nm, OBJ_VLINE, 0, t1, 2)
    ObjectSetInteger(0, nm, OBJPROP_COLOR, cl)
    ObjectSetInteger(0, nm, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, nm, OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, nm, OBJPROP_BACK, True)
    ObjectSetInteger(0, nm, OBJPROP_SELECTABLE, False)

def SetHLine(nm, p1, cl=_uint(Red)):
    if ObjectFind(0, nm) < 0:
        ObjectCreate(0, nm, OBJ_HLINE, 0, 0, p1)
    ObjectSetInteger(0, nm, OBJPROP_COLOR, cl)
    ObjectSetInteger(0, nm, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, nm, OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, nm, OBJPROP_SELECTABLE, False)

def Ris_H_Line():
    Uroven = 0.0
    rez = 0
    line_counter = 0
    i = 0
    mass = Arr(0, 0.0)
    max_ = 10.0
    min_ = 0.0
    index = 0
    ArraySetAsSeries(mass, True)
    if CopyHigh(Symbol(), PERIOD_MN1, 0, Bars(Symbol(), PERIOD_MN1), mass) > 2:
        index = ArrayMaximum(mass, 0, WHOLE_ARRAY)
        CopyHigh(Symbol(), PERIOD_MN1, index, 1, mass)
        max_ = mass[0]
    if CopyLow(Symbol(), PERIOD_MN1, 0, Bars(Symbol(), PERIOD_MN1), mass) > 2:
        index = ArrayMinimum(mass, 0, WHOLE_ARRAY)
        CopyLow(Symbol(), PERIOD_MN1, index, 1, mass)
        min_ = mass[0]
    while Uroven <= max_:
        i += 1
        Uroven = i * Step * Point()
        if Uroven >= min_:
            line_counter += 1
            rez = _int(MathMod(Uroven * MathPow(10, Digits()), Figure))
            if rez == 0:
                if Period() < PERIOD_W1:
                    SetHLine('HLine_' + _str(line_counter), Uroven, new_Hfigure)
            elif Period() < PERIOD_M30:
                SetHLine('HLine_' + _str(line_counter), Uroven, new_Hline)
    ChartRedraw()

def isNewBar_i(date, timeFrame):
    res = False
    pos = 0
    new_Time = Arr(1, 0, dyn=False)
    _sw1 = timeFrame
    if _sw1 == PERIOD_M1:
        pos = 0
    elif _sw1 == PERIOD_M2:
        pos = 1
    elif _sw1 == PERIOD_M3:
        pos = 2
    elif _sw1 == PERIOD_M4:
        pos = 3
    elif _sw1 == PERIOD_M5:
        pos = 4
    elif _sw1 == PERIOD_M6:
        pos = 5
    elif _sw1 == PERIOD_M10:
        pos = 6
    elif _sw1 == PERIOD_M12:
        pos = 7
    elif _sw1 == PERIOD_M15:
        pos = 8
    elif _sw1 == PERIOD_M20:
        pos = 9
    elif _sw1 == PERIOD_M30:
        pos = 10
    elif _sw1 == PERIOD_H1:
        pos = 11
    elif _sw1 == PERIOD_H2:
        pos = 12
    elif _sw1 == PERIOD_H3:
        pos = 13
    elif _sw1 == PERIOD_H4:
        pos = 14
    elif _sw1 == PERIOD_H6:
        pos = 15
    elif _sw1 == PERIOD_H8:
        pos = 16
    elif _sw1 == PERIOD_H12:
        pos = 17
    elif _sw1 == PERIOD_D1:
        pos = 18
    elif _sw1 == PERIOD_W1:
        pos = 19
    elif _sw1 == PERIOD_MN1:
        pos = 20
    if CopyTime(Symbol(), timeFrame, _DT(date), 1, new_Time) == 1:
        if old_Times[pos] != new_Time[0]:
            if old_Times[pos] != 0:
                res = True
            old_Times[pos] = new_Time[0]
    else:
        Print('Timeframe ', fTimeFrameName(timeFrame), ' is not ready')
    return res

def fTimeFrameName(arg):
    v = 0
    if arg == 0:
        v = Period()
    else:
        v = arg
    _sw2 = v
    if _sw2 == PERIOD_M1:
        return 'M1'
    elif _sw2 == PERIOD_M2:
        return 'M2'
    elif _sw2 == PERIOD_M3:
        return 'M3'
    elif _sw2 == PERIOD_M4:
        return 'M4'
    elif _sw2 == PERIOD_M5:
        return 'М5'
    elif _sw2 == PERIOD_M6:
        return 'М6'
    elif _sw2 == PERIOD_M10:
        return 'M10'
    elif _sw2 == PERIOD_M12:
        return 'M12'
    elif _sw2 == PERIOD_M15:
        return 'M15'
    elif _sw2 == PERIOD_M20:
        return 'M20'
    elif _sw2 == PERIOD_M30:
        return 'M30'
    elif _sw2 == PERIOD_H1:
        return 'H1'
    elif _sw2 == PERIOD_H2:
        return 'H2'
    elif _sw2 == PERIOD_H3:
        return 'H3'
    elif _sw2 == PERIOD_H4:
        return 'H4'
    elif _sw2 == PERIOD_H6:
        return 'H6'
    elif _sw2 == PERIOD_H8:
        return 'H8'
    elif _sw2 == PERIOD_H12:
        return 'H12'
    elif _sw2 == PERIOD_D1:
        return 'D1'
    elif _sw2 == PERIOD_W1:
        return 'W1'
    elif _sw2 == PERIOD_MN1:
        return 'MN1'
    else:
        return '?'

# ---- global variables initialised from expressions
new_hour = _uint(DimGray)  # new hour
new_day = _uint(Blue)  # new day
new_week = _uint(DeepPink)  # new week
new_mon = _uint(Yellow)  # new month
new_Hfigure = _uint(RoyalBlue)  # new figure
new_Hline = _uint(DimGray)  # new line


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Setka(_MQL5Indicator):
    name = 'setka'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Step': 250,  # vertical grid step in points
        'Figure': 1000,  # figure step
        'MaxBars': 0,  # bars in history (0 - all history)
    }

