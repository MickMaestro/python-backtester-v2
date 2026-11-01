"""ant_gubreakout — converted from MQL5: MQL5 Indicators/ant-GUBreakout/ant_gubreakout.mq5

Copyright: avoitenko; Link: https://login.mql5.com/en/users/avoitenko; Version: 1.041

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'avoitenko', 'link': 'https://login.mql5.com/en/users/avoitenko', 'version': '1.041', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 7, 4: 1, 5: 1}, 'colors': {1: [16748574], 2: [16711680], 3: [16711680], 4: [16777215], 5: [16777215]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 2, 5: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Area', 2: 'Offset Upper', 3: 'Offset Lower', 4: 'Line Upper', 5: 'Line Lower'}, 'levels': [], 'description': [], 'name': 'ant_gubreakout', 'source': 'MQL5 Indicators/ant-GUBreakout/ant_gubreakout.mq5', 'folder': 'ant-GUBreakout', 'inputs': [{'mql': 'InpUniqueNumber', 'py': 'InpUniqueNumber', 'param': 'InpUniqueNumber', 'type': 'ushort', 'default': 0, 'label': 'Unique Number', 'sinput': False}, {'mql': 'time_options', 'py': 'time_options', 'param': None, 'type': 'string', 'default': '---- Time Setting ---', 'label': 'Time Setting', 'sinput': False}, {'mql': 'InpGMTShift', 'py': 'InpGMTShift', 'param': 'InpGMTShift', 'type': 'int', 'default': 0, 'label': 'GMT Shift (hours)', 'sinput': False}, {'mql': 'InpStartHour', 'py': 'InpStartHour', 'param': 'InpStartHour', 'type': 'ushort', 'default': 12, 'label': 'Time Start Hour (box)', 'sinput': False}, {'mql': 'InpStartMinute', 'py': 'InpStartMinute', 'param': 'InpStartMinute', 'type': 'ushort', 'default': 0, 'label': 'Time Start Minute (box)', 'sinput': False}, {'mql': 'InpStopHour', 'py': 'InpStopHour', 'param': 'InpStopHour', 'type': 'ushort', 'default': 16, 'label': 'Time Stop Hour (box)', 'sinput': False}, {'mql': 'InpStopMinute', 'py': 'InpStopMinute', 'param': 'InpStopMinute', 'type': 'ushort', 'default': 0, 'label': 'Time Stop Minute (box)', 'sinput': False}, {'mql': 'InpEndHour', 'py': 'InpEndHour', 'param': 'InpEndHour', 'type': 'ushort', 'default': 21, 'label': 'Time End Hour (line)', 'sinput': False}, {'mql': 'InpEndMinute', 'py': 'InpEndMinute', 'param': 'InpEndMinute', 'type': 'ushort', 'default': 0, 'label': 'Time End Minute (line)', 'sinput': False}, {'mql': 'display_options', 'py': 'display_options', 'param': None, 'type': 'string', 'default': '--- Display Setting ---', 'label': 'Display Setting', 'sinput': False}, {'mql': 'InpDays', 'py': 'InpDays', 'param': 'InpDays', 'type': 'ushort', 'default': 6, 'label': 'Days Number', 'sinput': False}, {'mql': 'InpOffsetPips', 'py': 'InpOffsetPips', 'param': 'InpOffsetPips', 'type': 'ushort', 'default': 5, 'label': 'Offset Pips', 'sinput': False}, {'mql': 'InpShowLabels', 'py': 'InpShowLabels', 'param': 'InpShowLabels', 'type': 'bool', 'default': True, 'label': 'Show Labels', 'sinput': False}, {'mql': 'InpFontName', 'py': 'InpFontName', 'param': None, 'type': 'string', 'default': 'Arial', 'label': 'Font Name', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'ushort', 'default': 8, 'label': 'Font Size', 'sinput': False}, {'mql': 'InpTextColor', 'py': 'InpTextColor', 'param': None, 'type': 'color', 'default': 16777215, 'label': 'Text Color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpUniqueNumber = _input('InpUniqueNumber', 0)  # Unique Number
time_options = _input('time_options', '---- Time Setting ---')  # Time Setting
InpGMTShift = _input('InpGMTShift', 0)  # GMT Shift (hours)
InpStartHour = _input('InpStartHour', 12)  # Time Start Hour (box)
InpStartMinute = _input('InpStartMinute', 0)  # Time Start Minute (box)
InpStopHour = _input('InpStopHour', 16)  # Time Stop Hour (box)
InpStopMinute = _input('InpStopMinute', 0)  # Time Stop Minute (box)
InpEndHour = _input('InpEndHour', 21)  # Time End Hour (line)
InpEndMinute = _input('InpEndMinute', 0)  # Time End Minute (line)
display_options = _input('display_options', '--- Display Setting ---')  # Display Setting
InpDays = _input('InpDays', 6)  # Days Number
InpOffsetPips = _input('InpOffsetPips', 5)  # Offset Pips
InpShowLabels = _input('InpShowLabels', True)  # Show Labels
InpFontName = _input('InpFontName', 'Arial')  # Font Name
InpFontSize = _input('InpFontSize', 8)  # Font Size
InpTextColor = _input('InpTextColor', clrWhite)  # Text Color
AreaUpperBuffer = Arr(0, 0.0)
AreaLowerBuffer = Arr(0, 0.0)
OffsetUpper1Buffer = Arr(0, 0.0)
OffsetUpper2Buffer = Arr(0, 0.0)
OffsetLower1Buffer = Arr(0, 0.0)
OffsetLower2Buffer = Arr(0, 0.0)
LineUpperBuffer = Arr(0, 0.0)
LineLowerBuffer = Arr(0, 0.0)
min_ = 0.0
max_ = 0.0
coef = 0
increment = False
prefix = ""
Days = Arr(0, 0)
days_count = 0
time_start = 0
time_stop = 0
time_end = 0
index_start = 0
index_stop = 0
index_end = 0

def OnInit():
    global coef, prefix
    coef = 1
    if Digits() == 3 or Digits() == 5:
        coef = 10
    prefix = 'Text_' + IntegerToString(InpUniqueNumber)
    ChartSetInteger(0, CHART_FOREGROUND, True)
    SetIndexBuffer(0, AreaUpperBuffer)
    SetIndexBuffer(1, AreaLowerBuffer)
    SetIndexBuffer(2, OffsetUpper1Buffer)
    SetIndexBuffer(3, OffsetUpper2Buffer)
    SetIndexBuffer(4, OffsetLower1Buffer)
    SetIndexBuffer(5, OffsetLower2Buffer)
    SetIndexBuffer(6, LineUpperBuffer)
    SetIndexBuffer(7, LineLowerBuffer)
    ArraySetAsSeries(AreaUpperBuffer, True)
    ArraySetAsSeries(AreaLowerBuffer, True)
    ArraySetAsSeries(OffsetUpper1Buffer, True)
    ArraySetAsSeries(OffsetUpper2Buffer, True)
    ArraySetAsSeries(OffsetLower1Buffer, True)
    ArraySetAsSeries(OffsetLower2Buffer, True)
    ArraySetAsSeries(LineUpperBuffer, True)
    ArraySetAsSeries(LineLowerBuffer, True)
    ArraySetAsSeries(Days, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ant_GUBreakout(' + IntegerToString(InpUniqueNumber) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnDeinit(reason):
    total = ObjectsTotal(0)
    for i in range(total - 1, 0 - 1, -1):
        obj_name = ObjectName(0, i)
        if StringFind(obj_name, prefix) == 0:
            ObjectDelete(0, obj_name)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global days_count, index_end, index_start, index_stop, max_, min_, time_end, time_start, time_stop
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = 0
    if rates_total < prev_calculated or prev_calculated <= 0:
        limit = rates_total - 1
        ArrayInitialize(AreaUpperBuffer, 0)
        ArrayInitialize(AreaLowerBuffer, 0)
        ArrayInitialize(OffsetUpper1Buffer, 0)
        ArrayInitialize(OffsetUpper2Buffer, 0)
        ArrayInitialize(OffsetLower1Buffer, 0)
        ArrayInitialize(OffsetLower2Buffer, 0)
        ArrayInitialize(LineUpperBuffer, EMPTY_VALUE)
        ArrayInitialize(LineLowerBuffer, EMPTY_VALUE)
        min_ = DBL_MAX
        max_ = 0.0
    else:
        limit = rates_total - prev_calculated
    if limit < 2:
        days_count = 1
    else:
        days_count = InpDays
    if CopyTime(Symbol(), PERIOD_D1, 0, days_count, Days) != days_count:
        return 0
    for day in range(days_count - 1, 0 - 1, -1):
        time_start = BuildTime(Days[day], InpStartHour, InpStartMinute, InpGMTShift)
        time_stop = BuildTime(Days[day], InpStopHour, InpStopMinute, InpGMTShift)
        time_end = BuildTime(Days[day], InpEndHour, InpEndMinute, InpGMTShift)
        if time_start > time_stop:
            time_stop += PeriodSeconds(PERIOD_D1)
            time_end += PeriodSeconds(PERIOD_D1)
        time_end = fmax(time_stop, time_end)
        if limit > 1 or (time[0] >= time_start and time[0] <= time_end):
            index_start = iBarShift_u(Symbol(), Period(), time_start)
            index_stop = iBarShift_u(Symbol(), Period(), time_stop)
            index_end = iBarShift_u(Symbol(), Period(), time_end)
            count = index_start - index_stop + 1
            if (index_start < 0 or index_stop < 0) or count < 1:
                return 0
            index_max = ArrayMaximum(high, index_stop, count)
            index_min = ArrayMinimum(low, index_stop, count)
            if index_max < 0 or index_min < 0:
                return 0
            max_ = high[index_max]
            min_ = low[index_min]
            for i in range(index_start, index_stop - 1, -1):
                if InpOffsetPips > 0:
                    if (max_ - min_) <= (InpOffsetPips * coef * Point() * 2):
                        AreaUpperBuffer[i] = 0.0
                        AreaLowerBuffer[i] = 0.0
                        OffsetUpper1Buffer[i] = max_
                        OffsetUpper2Buffer[i] = min_
                        OffsetLower1Buffer[i] = 0.0
                        OffsetLower2Buffer[i] = 0.0
                    else:
                        AreaUpperBuffer[i] = max_ - (InpOffsetPips * coef * Point())
                        AreaLowerBuffer[i] = min_ + (InpOffsetPips * coef * Point())
                        OffsetUpper1Buffer[i] = max_
                        OffsetUpper2Buffer[i] = max_ - (InpOffsetPips * coef * Point())
                        OffsetLower1Buffer[i] = min_ + (InpOffsetPips * coef * Point())
                        OffsetLower2Buffer[i] = min_
                else:
                    AreaUpperBuffer[i] = max_
                    AreaLowerBuffer[i] = min_
                    OffsetUpper1Buffer[i] = 0.0
                    OffsetUpper2Buffer[i] = 0.0
                    OffsetLower1Buffer[i] = 0.0
                    OffsetLower2Buffer[i] = 0.0
            for i in range(index_start, index_end - 1, -1):
                LineUpperBuffer[i] = max_
                LineLowerBuffer[i] = min_
            LineUpperBuffer[index_start + 1] = EMPTY_VALUE
            LineLowerBuffer[index_start + 1] = EMPTY_VALUE
            if InpShowLabels and count > 1:
                mask = StringFormat('H:[%%.%df]  L:[%%.%df]  R:[%%d]', Digits(), Digits())
                text = StringFormat(mask, max_, min_, _int(_fdiv(_fdiv(max_ - min_, Point()), coef)))
                SetText(IntegerToString(Days[day]), time[index_start], max_, text)
        else:
            AreaUpperBuffer[0] = 0.0
            AreaLowerBuffer[0] = 0.0
            OffsetUpper1Buffer[0] = 0.0
            OffsetUpper2Buffer[0] = 0.0
            OffsetLower1Buffer[0] = 0.0
            OffsetLower2Buffer[0] = 0.0
            LineUpperBuffer[0] = EMPTY_VALUE
            LineLowerBuffer[0] = EMPTY_VALUE
    return rates_total

def BuildTime(date, hour, minute, offset):
    new_time = 0
    dt = MqlDateTime()
    TimeToStruct(date, dt)
    dt.hour = hour
    dt.min = minute
    new_time = StructToTime(dt)
    new_time += PeriodSeconds(PERIOD_H1) * offset
    return new_time

def SetText(sufix, time, price, caption):
    name = prefix + sufix
    if ObjectFind(0, name) == 0 or ObjectCreate(0, name, OBJ_TEXT, 0, time, price):
        ObjectSetDouble(0, name, OBJPROP_PRICE, price)
        ObjectSetInteger(0, name, OBJPROP_TIME, time)
        ObjectSetString(0, name, OBJPROP_FONT, InpFontName)
        ObjectSetInteger(0, name, OBJPROP_FONTSIZE, InpFontSize)
        ObjectSetInteger(0, name, OBJPROP_COLOR, InpTextColor)
        ObjectSetString(0, name, OBJPROP_TEXT, caption)

def iBarShift_u(symbol, tf, time):
    if time < 0:
        return -1
    Arr_ = Arr(0, 0)
    CopyTime(symbol, tf, 0, 1, Arr_)
    time1 = Arr_[0]
    if CopyTime(symbol, tf, _DT(time), _DT(time1), Arr_) > 0:
        if ArraySize(Arr_) > 2:
            return ArraySize(Arr_) - 1
        if time < time1:
            return 1
        else:
            return 0
    else:
        return -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AntGubreakout(_MQL5Indicator):
    name = 'ant_gubreakout'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpUniqueNumber': 0,  # Unique Number
        'InpGMTShift': 0,  # GMT Shift (hours)
        'InpStartHour': 12,  # Time Start Hour (box)
        'InpStartMinute': 0,  # Time Start Minute (box)
        'InpStopHour': 16,  # Time Stop Hour (box)
        'InpStopMinute': 0,  # Time Stop Minute (box)
        'InpEndHour': 21,  # Time End Hour (line)
        'InpEndMinute': 0,  # Time End Minute (line)
        'InpDays': 6,  # Days Number
        'InpOffsetPips': 5,  # Offset Pips
        'InpShowLabels': True,  # Show Labels
        'InpFontSize': 8,  # Font Size
    }

