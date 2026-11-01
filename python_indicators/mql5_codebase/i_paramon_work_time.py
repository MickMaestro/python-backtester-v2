"""i-Paramon_Work_Time — converted from MQL5: MQL5 Indicators/i-Paramon work time/i-Paramon_Work_Time.mq5

The iParamon WorkTime indicator originally made by Kim Igor V
This version made by Mladen
Copyright: Copyright © 2006, Kim Igor V. aka KimIV; Link: http://www.kimiv.ru

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Kim Igor V. aka KimIV', 'link': 'http://www.kimiv.ru', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['The iParamon WorkTime indicator originally made by Kim Igor V', 'This version made by Mladen'], 'name': 'i-Paramon_Work_Time', 'source': 'MQL5 Indicators/i-Paramon work time/i-Paramon_Work_Time.mq5', 'folder': 'i-Paramon work time', 'inputs': [{'mql': 'NumberOfDays', 'py': 'NumberOfDays', 'param': 'NumberOfDays', 'type': 'int', 'default': 10, 'label': 'Number of days', 'sinput': False}, {'mql': 'Begin_1', 'py': 'Begin_1', 'param': None, 'type': 'string', 'default': '07:00', 'label': 'Start of first session', 'sinput': False}, {'mql': 'End_1', 'py': 'End_1', 'param': None, 'type': 'string', 'default': '11:00', 'label': 'End of first session', 'sinput': False}, {'mql': 'Color_1', 'py': 'Color_1', 'param': None, 'type': 'color', 'default': 12903679, 'label': 'Color of first session', 'sinput': False}, {'mql': 'Begin_2', 'py': 'Begin_2', 'param': None, 'type': 'string', 'default': '13:00', 'label': 'Start of second session', 'sinput': False}, {'mql': 'End_2', 'py': 'End_2', 'param': None, 'type': 'string', 'default': '17:00', 'label': 'End of second session', 'sinput': False}, {'mql': 'Color_2', 'py': 'Color_2', 'param': None, 'type': 'color', 'default': 15658671, 'label': 'Color of second session', 'sinput': False}, {'mql': 'Begin_3', 'py': 'Begin_3', 'param': None, 'type': 'string', 'default': '19:00', 'label': 'Start of third session', 'sinput': False}, {'mql': 'End_3', 'py': 'End_3', 'param': None, 'type': 'string', 'default': '23:00', 'label': 'End of third session', 'sinput': False}, {'mql': 'Color_3', 'py': 'Color_3', 'param': None, 'type': 'color', 'default': 14804223, 'label': 'Color of third session', 'sinput': False}, {'mql': 'UniqueID', 'py': 'UniqueID', 'param': None, 'type': 'string', 'default': 'workTimes1', 'label': 'Unique ID for objects', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
NumberOfDays = _input('NumberOfDays', 10)  # Number of days
Begin_1 = _input('Begin_1', '07:00')  # Start of first session
End_1 = _input('End_1', '11:00')  # End of first session
Color_1 = _input('Color_1', clrBisque)  # Color of first session
Begin_2 = _input('Begin_2', '13:00')  # Start of second session
End_2 = _input('End_2', '17:00')  # End of second session
Color_2 = _input('Color_2', clrPaleTurquoise)  # Color of second session
Begin_3 = _input('Begin_3', '19:00')  # Start of third session
End_3 = _input('End_3', '23:00')  # End of third session
Color_3 = _input('Color_3', clrMistyRose)  # Color of third session
UniqueID = _input('UniqueID', 'workTimes1')  # Unique ID for objects

def OnInit():
    pass

def OnDeinit(reason):
    for i in range(ObjectsTotal(0, -1, OBJ_RECTANGLE) - 1, 0 - 1, -1):
        name = ObjectName(0, i, -1, OBJ_RECTANGLE)
        if StringFind(name, UniqueID + ':') == 0:
            ObjectDelete(0, name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_lastTime
    if Period() >= PERIOD_D1 or Bars(Symbol(), Period()) < rates_total:
        return 0
    noOfDays = NumberOfDays
    if _s_OnCalculate_lastTime == time[rates_total - 1]:
        noOfDays = MathMin(NumberOfDays, 1)
    dtime = Arr(0, 0)
    copied = CopyTime(Symbol(), PERIOD_D1, 0, noOfDays, dtime)
    if copied <= 0:
        return 0
    for i in range(0, copied):
        if Begin_1 != '':
            CreateSession(dtime[copied - i - 1], Begin_1, End_1, Color_1, ':PWT1:' + _str(i))
        if Begin_2 != '':
            CreateSession(dtime[copied - i - 1], Begin_2, End_2, Color_2, ':PWT2:' + _str(i))
        if Begin_3 != '':
            CreateSession(dtime[copied - i - 1], Begin_3, End_3, Color_3, ':PWT3:' + _str(i))
    _s_OnCalculate_lastTime = time[rates_total - 1]
    return rates_total

def CreateSession(btime, begin, end, dcolor, id_):
    stime = StringToTime(TimeToString(btime, TIME_DATE) + ' ' + begin)
    etime = StringToTime(TimeToString(btime, TIME_DATE) + ' ' + end)
    if etime < stime:
        etime += 24 * 3600
    ah = Arr(0, 0.0)
    al = Arr(0, 0.0)
    size = CopyHigh(Symbol(), Period(), _DT(stime), etime - 1, ah)
    if size <= 0:
        return
    size = CopyLow(Symbol(), Period(), _DT(stime), etime - 1, al)
    if size <= 0:
        return
    whigh = ah[ArrayMaximum(ah)]
    wlow = al[ArrayMinimum(al)]
    name = UniqueID + id_
    ObjectCreate(0, name, OBJ_RECTANGLE, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_COLOR, dcolor)
    ObjectSetInteger(0, name, OBJPROP_BACK, True)
    ObjectSetInteger(0, name, OBJPROP_FILL, True)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, stime)
    ObjectSetInteger(0, name, OBJPROP_TIME, 1, etime)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, whigh)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, wlow)

# ---- static local variables
_s_OnCalculate_lastTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IParamonWorkTime(_MQL5Indicator):
    name = 'i-Paramon_Work_Time'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'NumberOfDays': 10,  # Number of days
    }

