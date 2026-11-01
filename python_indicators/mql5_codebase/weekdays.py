"""WeekDays — converted from MQL5: MQL5 Indicators/Day Of Week, Week Of Year and other marks in Data Window and on chart/WeekDays.mq5

Tracks current mouse position to show day of week, week number, day of year, or bar index under the cursor.
Two selected parameters are combined in a single value as a whole part and a fractional part in the Data Window.
Copyright: Copyright (c) 2009-2024, Marketeer; Link: https://www.mql5.com/en/users/marketeer; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.arrayutils import *  # #include ArrayUtils.mqh

MQL5_META = {'props': {'copyright': 'Copyright (c) 2009-2024, Marketeer', 'link': 'https://www.mql5.com/en/users/marketeer', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 0}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Tracks current mouse position to show day of week, week number, day of year, or bar index under the cursor.', 'Two selected parameters are combined in a single value as a whole part and a fractional part in the Data Window.'], 'name': 'WeekDays', 'source': 'MQL5 Indicators/Day Of Week, Week Of Year and other marks in Data Window and on chart/WeekDays.mq5', 'folder': 'Day Of Week, Week Of Year and other marks in Data Window and on chart', 'inputs': [{'mql': 'WholePart', 'py': 'WholePart', 'param': 'WholePart', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'FractionalPart', 'py': 'FractionalPart', 'param': 'FractionalPart', 'type': 'int', 'default': 1000, 'label': '', 'sinput': False}, {'mql': 'ShowLabels', 'py': 'ShowLabels', 'param': 'ShowLabels', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'FontName', 'py': 'FontName', 'param': None, 'type': 'string', 'default': 'Segoe UI', 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 25, 'label': '', 'sinput': False}, {'mql': 'FontColor', 'py': 'FontColor', 'param': None, 'type': 'color', 'default': 4294967295, 'label': '', 'sinput': False}, {'mql': 'Padding', 'py': 'Padding', 'param': 'Padding', 'type': 'int', 'default': 5, 'label': 'Padding (% of chart height, for top/bottom alignment)', 'sinput': False}, {'mql': 'AlignTo', 'py': 'AlignTo', 'param': 'AlignTo', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'RotationAngle', 'py': 'RotationAngle', 'param': 'RotationAngle', 'type': 'int', 'default': 0, 'label': 'RotationAngle (for middle alignment)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['ArrayUtils.mqh']}

# enum InfoType
None_ = 1
DoW = 10
Week = 100
DoY = 1000
Bar = 1000000000
_enum('InfoType', {1: 'None', 10: 'DoW', 100: 'Week', 1000: 'DoY', 1000000000: 'Bar'})

# enum Alignment
Top = 0
Middle = 1
Bottom = 2
_enum('Alignment', {0: 'Top', 1: 'Middle', 2: 'Bottom'})

# ---- inputs and global variables
WholePart = _input('WholePart', Week)
FractionalPart = _input('FractionalPart', DoY)
ShowLabels = _input('ShowLabels', False)
FontName = _input('FontName', 'Segoe UI')
FontSize = _input('FontSize', 25)
FontColor = _input('FontColor', clrNONE)
Padding = _input('Padding', 5)  # Padding (% of chart height, for top/bottom alignment)
AlignTo = _input('AlignTo', Top)
RotationAngle = _input('RotationAngle', 0)  # RotationAngle (for middle alignment)
Buffer1 = Arr(0, 0.0)
objCache = Arr(0, 0)

class DateTime(MqlObject):
    _q_fields = ('mdtstruct', 'origin')
    _DateTime = None
    def __init__(self):
        self.mdtstruct = MqlDateTime()
        self.origin = 0
        self.origin = 0
        TimeToStruct(0, self.mdtstruct)
    def convert(self, dt):
        if self.origin != dt:
            self.origin = dt
            TimeToStruct(dt, self.mdtstruct)
    @staticmethod
    def assign(dt):
        DateTime._DateTime.convert(dt)
        return DateTime._DateTime
    def timeDayOfWeek(self):
        return self.mdtstruct.day_of_week
    def timeDayOfYear(self):
        return self.mdtstruct.day_of_year
    def timeYear(self):
        return self.mdtstruct.year
    def timeMonth(self):
        return self.mdtstruct.mon
    def timeDay(self):
        return self.mdtstruct.day
    def timeHour(self):
        return self.mdtstruct.hour
    def timeMinute(self):
        return self.mdtstruct.min
    def timeSeconds(self):
        return self.mdtstruct.sec
DateTime._DateTime = DateTime()

def OnInit():
    if Period() > PERIOD_D1:
        return INIT_PARAMETERS_INCORRECT
    SetIndexBuffer(0, Buffer1, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, _int(MathLog10(FractionalPart)))
    ChartSetInteger(0, CHART_EVENT_MOUSE_MOVE, True)
    if WholePart == FractionalPart and WholePart != None_:
        Alert('The same info is selected to display as whole part and fractional part of indicator values!')
    if ShowLabels and Period() < PERIOD_D1:
        AdjustLabels()
    return INIT_SUCCEEDED

def OnDeinit(_p0):
    ObjectsDeleteAll(0, 'WDi_')
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = 0
    if prev_calculated <= 0:
        ArrayInitialize(Buffer1, EMPTY_VALUE)
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        if (WholePart * FractionalPart) > 1:
            d = DateTime.assign(time[i]).timeDayOfYear()
            Buffer1[i] = GetPart(WholePart, i) + (GetPart(FractionalPart, i) / float(FractionalPart))
        else:
            Buffer1[i] = DayOfWeek(time[i])
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global _s_OnChartEvent_day
    if id_ == CHARTEVENT_MOUSE_MOVE:
        window = Box(0)
        time = Box(0)
        price = Box(0.0)
        if ChartXYToTimePrice(0, _int(lparam), _int(dparam), window, time, price):
            b = iBarShift(Symbol(), Period(), time.v)
            if b > -1:
                time.v = iTime(Symbol(), Period(), b)
            else:
                time.v = _idiv(time.v + _idiv(PeriodSeconds(), 2), PeriodSeconds()) * PeriodSeconds()
            now = DayOfWeek(time.v)
            if now != _s_OnChartEvent_day:
                _s_OnChartEvent_day = now
                valid = (WholePart * FractionalPart) > 1
                legend = StringFormat('%s%s%s%s', (' | ' if valid else ''), (EnumToString(WholePart, 'InfoType') if (WholePart > 1) else ''), (('.' + EnumToString(FractionalPart, 'InfoType')) if (FractionalPart > 1) else ''), (': ->' if valid else ''))
                PlotIndexSetString(0, PLOT_LABEL, StringFormat('Day: %s%s', DayName(_s_OnChartEvent_day), legend))
                ChartRedraw(0)
    elif id_ == CHARTEVENT_CHART_CHANGE:
        if ShowLabels and Period() < PERIOD_D1:
            AdjustLabels()

def AdjustLabels():
    left = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR))
    width = _int(ChartGetInteger(0, CHART_VISIBLE_BARS))
    overnights = Arr(0, 0, dims=(2,))
    prevday = -1
    for i in range(0, width):
        if (left - i) < 0:
            continue
        day = DayOfWeek(iTime(Symbol(), Period(), left - i))
        if day != prevday or (left - i) == 0:
            range_ = Arr.of([[(iTime(Symbol(), Period(), left - i + 1) if ((left - i) > 0) else ((_idiv(iTime(Symbol(), Period(), 0), 60 * 60 * 24) * (60 * 60 * 24)) - PeriodSeconds())), (iTime(Symbol(), Period(), left - i) if ((left - i) > 0) else ((_idiv(iTime(Symbol(), Period(), 0), 60 * 60 * 24) * (60 * 60 * 24)) + (60 * 60 * 24)))]], fill=0, dyn=False, size=1, dims=(2,))
            ArrayInsert(overnights, range_, ArrayRange(overnights, 0))
            prevday = day
    add = (Padding / 100.0) * (ChartGetDouble(0, CHART_PRICE_MAX) - ChartGetDouble(0, CHART_PRICE_MIN))
    price = ((ChartGetDouble(0, CHART_PRICE_MAX) - add) if (AlignTo == Top) else (ChartGetDouble(0, CHART_PRICE_MIN) + add) if (AlignTo == Bottom) else ((ChartGetDouble(0, CHART_PRICE_MAX) + ChartGetDouble(0, CHART_PRICE_MIN)) / 2))
    realFontSize = _int(_idiv(FontSize, 6 - ChartGetInteger(0, CHART_SCALE)))
    i = 1
    while i < ArrayRange(overnights, 0):
        CreateLabel(overnights[i - 1][1], (overnights[i][1] if (overnights[i][1] > TimeCurrent()) else (overnights[i][0] + PeriodSeconds())), price, realFontSize)
        i += 1
    CleanUpLabels(iTime(Symbol(), Period(), left), iTime(Symbol(), Period(), left - width), price, realFontSize)
    ChartRedraw()

def CreateLabel(left, right, price, realFontSize):
    if (right - left) < _idiv(60 * 60 * 24, 2):
        return
    iClose(Symbol(), Period(), 0)
    d = DateTime.assign(left).timeDayOfYear()
    name = 'WDi_' + _str(d)
    ObjectCreate(0, name, OBJ_TEXT, 0, _idiv(left + right, 2), price)
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, (ANCHOR_UPPER if (AlignTo == Top) else ANCHOR_LOWER if (AlignTo == Bottom) else ANCHOR_CENTER))
    ObjectSetString(0, name, OBJPROP_TEXT, DayName(DayOfWeek(left)) + (('|' + _str(WeekNumber())) if (WholePart == Week or FractionalPart == Week) else '') + (('|' + _str(d)) if (WholePart == DoY or FractionalPart == DoY) else ''))
    ObjectSetString(0, name, OBJPROP_FONT, FontName)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, realFontSize)
    ObjectSetInteger(0, name, OBJPROP_COLOR, (FontColor if (FontColor != clrNONE) else (~ChartGetInteger(0, CHART_COLOR_BACKGROUND))))
    ObjectSetInteger(0, name, OBJPROP_BACK, True)
    if AlignTo == Middle:
        ObjectSetDouble(0, name, OBJPROP_ANGLE, RotationAngle)
    objCache[ArrayResize(objCache, ArrayRange(objCache, 0) + 1, ArrayRange(objCache, 0) * 2) - 1] = d

def CleanUpLabels(left, right, price, realFontSize):
    for i in range(0, ArraySize(objCache)):
        name = 'WDi_' + _str(objCache[i])
        t = ObjectGetInteger(0, name, OBJPROP_TIME, 0)
        if t != 0 and (t < left or t > (right if right else (TimeCurrent() + (60 * 60 * 24 * 7)))):
            ObjectDelete(0, name)
            objCache[i] = -1
        else:
            ObjectSetDouble(0, name, OBJPROP_PRICE, price)
            ObjectSetInteger(0, name, OBJPROP_FONTSIZE, realFontSize)
    ArrayPurge(objCache, -1)

def GetPart(part, i):
    _sw1 = part
    if _sw1 == DoW:
        return DateTime._DateTime.timeDayOfWeek()
    elif _sw1 == DoY:
        return DateTime._DateTime.timeDayOfYear()
    elif _sw1 == Week:
        return WeekNumber()
    elif _sw1 == Bar:
        return i
    return 0.0

def DayName(DayNo):
    return _s_DayName_Days[_imod(DayNo, 7)]

def DayOfWeek(time):
    return _imod(_int(_idiv(time, 86400) + 4), 7)

def WeekNumber():
    d1 = StringToTime(_str(DateTime._DateTime.timeYear()) + '.01.01 00:00')
    return _idiv(DateTime._DateTime.timeDayOfYear() + DayOfWeek(d1), 7) + 1

# ---- static local variables
_s_OnChartEvent_day = -1
_s_DayName_Days = Arr.of(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], fill="", dyn=False, size=7)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WeekDays(_MQL5Indicator):
    name = 'WeekDays'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WholePart': _Choice({1: 'None', 10: 'Day Of Week', 100: 'Week Of Year', 1000: 'Day Of Year', 1000000000: 'Bar Index'}, default=100),
        'FractionalPart': _Choice({1: 'None', 10: 'Day Of Week', 100: 'Week Of Year', 1000: 'Day Of Year', 1000000000: 'Bar Index'}, default=1000),
        'ShowLabels': False,
        'FontSize': 25,
        'Padding': 5,  # Padding (% of chart height, for top/bottom alignment)
        'AlignTo': _Choice({0: 'Top', 1: 'Middle', 2: 'Bottom'}, default=0),
        'RotationAngle': 0,  # RotationAngle (for middle alignment)
    }

