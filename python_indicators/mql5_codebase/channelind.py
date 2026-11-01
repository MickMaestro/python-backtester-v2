"""ChannelInd — converted from MQL5: MQL5 Indicators/ChannelInd/ChannelInd.mq5

 The indicator draws the High/Low channel for time range (start hour - end hour). 
 Near the lower boundary of the channel displays channel size in points. 
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [10025880, 12903679], 2: [16748574], 3: [17919]}, 'widths': {1: 1, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Channel', 2: 'Upper', 3: 'Lower'}, 'levels': [], 'description': [' The indicator draws the High/Low channel for time range (start hour - end hour). ', ' Near the lower boundary of the channel displays channel size in points. '], 'name': 'ChannelInd', 'source': 'MQL5 Indicators/ChannelInd/ChannelInd.mq5', 'folder': 'ChannelInd', 'inputs': [{'mql': 'InpHourBegin', 'py': 'InpHourBegin', 'param': 'InpHourBegin', 'type': 'uint', 'default': 1, 'label': 'Begin trade day hour', 'sinput': False}, {'mql': 'InpHourEnd', 'py': 'InpHourEnd', 'param': 'InpHourEnd', 'type': 'uint', 'default': 22, 'label': 'End trade day hour', 'sinput': False}, {'mql': 'InpShowSizes', 'py': 'InpShowSizes', 'param': 'InpShowSizes', 'type': 'int', 'default': 1, 'label': 'Draw channels size', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'uint', 'default': 8, 'label': 'Labels size', 'sinput': False}, {'mql': 'InpFontColor', 'py': 'InpFontColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Labels color', 'sinput': False}, {'mql': 'InpFontName', 'py': 'InpFontName', 'param': None, 'type': 'string', 'default': 'Calibri', 'label': 'Font name', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpHourBegin = _input('InpHourBegin', 1)  # Begin trade day hour
InpHourEnd = _input('InpHourEnd', 22)  # End trade day hour
InpShowSizes = _input('InpShowSizes', INPUT_YES)  # Draw channels size
InpFontSize = _input('InpFontSize', 8)  # Labels size
InpFontColor = _input('InpFontColor', clrGray)  # Labels color
InpFontName = _input('InpFontName', 'Calibri')  # Font name
BufferChannelUP = Arr(0, 0.0)
BufferChannelDN = Arr(0, 0.0)
BufferUpperLine = Arr(0, 0.0)
BufferLowerLine = Arr(0, 0.0)
hour_begin = 0
hour_end = 0
font_size = 0
prefix = ""

def OnInit():
    global font_size, hour_begin, hour_end, prefix
    short_name = 'Channel(' + IntegerToString(hour_begin, 2, 48) + ':00-' + IntegerToString(hour_end, 2, 48) + ':00)'
    hour_begin = (23 if (InpHourBegin > 23) else InpHourBegin)
    hour_end = ((hour_begin - 1) if (InpHourEnd == _uint(hour_begin)) else 23 if (InpHourEnd > 23) else InpHourEnd)
    font_size = (6 if (InpFontSize < 6) else InpFontSize)
    prefix = short_name + '_'
    SetIndexBuffer(0, BufferChannelUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferChannelDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferUpperLine, INDICATOR_DATA)
    SetIndexBuffer(3, BufferLowerLine, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUpperLine, True)
    ArraySetAsSeries(BufferLowerLine, True)
    ArraySetAsSeries(BufferChannelUP, True)
    ArraySetAsSeries(BufferChannelDN, True)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_size, _s_OnCalculate_size
    if rates_total < 4:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUpperLine, EMPTY_VALUE)
        ArrayInitialize(BufferLowerLine, EMPTY_VALUE)
        ArrayInitialize(BufferChannelUP, EMPTY_VALUE)
        ArrayInitialize(BufferChannelDN, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        end_time = EndTime(time[i])
        if time[i] >= end_time and time[i + 1] < end_time:
            max_price = high[i]
            min_price = low[i]
            begin_time = BeginTime(time[i])
            if hour_begin > hour_end:
                begin_time -= 86400
            pos = i
            while pos < rates_total and time[pos] >= begin_time:
                min_price = fmin(min_price, low[pos])
                max_price = fmax(max_price, high[pos])
                pos += 1
            _s_OnCalculate_size = _int(_fdiv(max_price - min_price, Point()))
            for n in range(pos - 1, i - 1, -1):
                BufferUpperLine[n] = max_price
                BufferLowerLine[n] = min_price
                BufferChannelUP[n] = (max_price if (_s_OnCalculate_size > _s_OnCalculate_prev_size) else min_price)
                BufferChannelDN[n] = (min_price if (_s_OnCalculate_size > _s_OnCalculate_prev_size) else max_price)
            if InpShowSizes and i != (pos - 1):
                name = prefix + TimeToString(time[i], TIME_DATE)
                text = _str(_s_OnCalculate_size)
                if ObjectFind(0, name) == WRONG_VALUE:
                    ObjectCreate(0, name, OBJ_TEXT, 0, 0, 0)
                    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
                    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
                    ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
                    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size)
                    ObjectSetInteger(0, name, OBJPROP_COLOR, InpFontColor)
                    ObjectSetInteger(0, name, OBJPROP_TIME, 0, time[i])
                    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, min_price)
                    ObjectSetString(0, name, OBJPROP_FONT, InpFontName)
                    ObjectSetString(0, name, OBJPROP_TEXT, text)
                else:
                    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, min_price)
            _s_OnCalculate_prev_size = _s_OnCalculate_size
        else:
            BufferUpperLine[i] = EMPTY_VALUE
            BufferLowerLine[i] = BufferUpperLine[i]
            BufferChannelUP[i] = 0.0
            BufferChannelDN[i] = BufferChannelUP[i]
    return rates_total

def BeginTime(time):
    tm = MqlDateTime()
    if TimeToStruct(time, tm):
        tm.hour = hour_begin
        tm.min = 0
        return StructToTime(tm)
    return 0

def EndTime(time):
    tm = MqlDateTime()
    if TimeToStruct(time, tm):
        tm.hour = hour_end
        tm.min = 0
        return StructToTime(tm)
    return 0

# ---- static local variables
_s_OnCalculate_prev_size = 0
_s_OnCalculate_size = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChannelInd(_MQL5Indicator):
    name = 'ChannelInd'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpHourBegin': 1,  # Begin trade day hour
        'InpHourEnd': 22,  # End trade day hour
        'InpShowSizes': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Draw channels size
        'InpFontSize': 8,  # Labels size
    }

