"""Market_Sessions — converted from MQL5: MQL5 Indicators/Market_Sessions/Market_Sessions.mq5

Market Sessions indicator
Highlights the Forex Market Sessions
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 7, 2: 7, 3: 7, 4: 7}, 'colors': {1: [42495, 42495], 2: [17919, 17919], 3: [7451452, 7451452], 4: [15453831, 15453831]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Sidney', 2: 'Tokio', 3: 'London', 4: 'NewYork'}, 'levels': [], 'description': ['Market Sessions indicator', 'Highlights the Forex Market Sessions'], 'name': 'Market_Sessions', 'source': 'MQL5 Indicators/Market_Sessions/Market_Sessions.mq5', 'folder': 'Market_Sessions', 'inputs': [{'mql': 'InpStartSidney', 'py': 'InpStartSidney', 'param': 'InpStartSidney', 'type': 'uint', 'default': 0, 'label': 'Sidney session begin', 'sinput': False}, {'mql': 'InpEndSidney', 'py': 'InpEndSidney', 'param': 'InpEndSidney', 'type': 'uint', 'default': 9, 'label': 'Sidney session end', 'sinput': False}, {'mql': 'InpColorSidney', 'py': 'InpColorSidney', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Sidney session color', 'sinput': False}, {'mql': 'InpStartTokio', 'py': 'InpStartTokio', 'param': 'InpStartTokio', 'type': 'uint', 'default': 2, 'label': 'Tokio session begin', 'sinput': False}, {'mql': 'InpEndTokio', 'py': 'InpEndTokio', 'param': 'InpEndTokio', 'type': 'uint', 'default': 11, 'label': 'Tokio session end', 'sinput': False}, {'mql': 'InpColorTokio', 'py': 'InpColorTokio', 'param': None, 'type': 'color', 'default': 17919, 'label': 'Tokio session color', 'sinput': False}, {'mql': 'InpStartLondon', 'py': 'InpStartLondon', 'param': 'InpStartLondon', 'type': 'uint', 'default': 10, 'label': 'London session begin', 'sinput': False}, {'mql': 'InpEndLondon', 'py': 'InpEndLondon', 'param': 'InpEndLondon', 'type': 'uint', 'default': 19, 'label': 'London session end', 'sinput': False}, {'mql': 'InpColorLondon', 'py': 'InpColorLondon', 'param': None, 'type': 'color', 'default': 7451452, 'label': 'London session color', 'sinput': False}, {'mql': 'InpStartNewYork', 'py': 'InpStartNewYork', 'param': 'InpStartNewYork', 'type': 'uint', 'default': 15, 'label': 'NewYork session begin', 'sinput': False}, {'mql': 'InpEndNewYork', 'py': 'InpEndNewYork', 'param': 'InpEndNewYork', 'type': 'uint', 'default': 0, 'label': 'NewYork session end', 'sinput': False}, {'mql': 'InpColorNewYork', 'py': 'InpColorNewYork', 'param': None, 'type': 'color', 'default': 15453831, 'label': 'NewYork session color', 'sinput': False}, {'mql': 'InpWidth', 'py': 'InpWidth', 'param': 'InpWidth', 'type': 'uchar', 'default': 60, 'label': 'Session field height', 'sinput': False}, {'mql': 'InpShowLabels', 'py': 'InpShowLabels', 'param': 'InpShowLabels', 'type': 'int', 'default': 1, 'label': 'Show session labels', 'sinput': False}, {'mql': 'InpFontName', 'py': 'InpFontName', 'param': None, 'type': 'string', 'default': 'Calibri', 'label': 'Font name', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'uchar', 'default': 8, 'label': 'Font size', 'sinput': False}, {'mql': 'InpFontColor', 'py': 'InpFontColor', 'param': None, 'type': 'color', 'default': 8388608, 'label': 'Font color', 'sinput': False}, {'mql': 'InpShowVLines', 'py': 'InpShowVLines', 'param': 'InpShowVLines', 'type': 'int', 'default': 1, 'label': 'Show start-session lines', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# enum ENUM_SESSIONS
SESSION_SIDNEY = 0
SESSION_TOKIO = 1
SESSION_LONDON = 2
SESSION_NEW_YORK = 3
_enum('ENUM_SESSIONS', {0: 'SESSION_SIDNEY', 1: 'SESSION_TOKIO', 2: 'SESSION_LONDON', 3: 'SESSION_NEW_YORK'})

# ---- inputs and global variables
InpStartSidney = _input('InpStartSidney', 0)  # Sidney session begin
InpEndSidney = _input('InpEndSidney', 9)  # Sidney session end
InpColorSidney = _input('InpColorSidney', clrOrange)  # Sidney session color
InpStartTokio = _input('InpStartTokio', 2)  # Tokio session begin
InpEndTokio = _input('InpEndTokio', 11)  # Tokio session end
InpColorTokio = _input('InpColorTokio', clrOrangeRed)  # Tokio session color
InpStartLondon = _input('InpStartLondon', 10)  # London session begin
InpEndLondon = _input('InpEndLondon', 19)  # London session end
InpColorLondon = _input('InpColorLondon', clrMediumSeaGreen)  # London session color
InpStartNewYork = _input('InpStartNewYork', 15)  # NewYork session begin
InpEndNewYork = _input('InpEndNewYork', 0)  # NewYork session end
InpColorNewYork = _input('InpColorNewYork', clrSkyBlue)  # NewYork session color
InpWidth = _input('InpWidth', 60)  # Session field height
InpShowLabels = _input('InpShowLabels', INPUT_YES)  # Show session labels
InpFontName = _input('InpFontName', 'Calibri')  # Font name
InpFontSize = _input('InpFontSize', 8)  # Font size
InpFontColor = _input('InpFontColor', clrNavy)  # Font color
InpShowVLines = _input('InpShowVLines', INPUT_YES)  # Show start-session lines
BufferSidney1 = Arr(0, 0.0)
BufferSidney2 = Arr(0, 0.0)
BufferTokio1 = Arr(0, 0.0)
BufferTokio2 = Arr(0, 0.0)
BufferLondon1 = Arr(0, 0.0)
BufferLondon2 = Arr(0, 0.0)
BufferNewYork1 = Arr(0, 0.0)
BufferNewYork2 = Arr(0, 0.0)
prefix = ""
start_sidney = 0
end_sidney = 0
start_tokio = 0
end_tokio = 0
start_london = 0
end_london = 0
start_new_york = 0
end_new_york = 0
width = 0
font_size = 0
prev_fgnd = False

def OnInit():
    global end_london, end_new_york, end_sidney, end_tokio, font_size, prefix, prev_fgnd, start_london, start_new_york, start_sidney, start_tokio, width
    EventSetTimer(90)
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    start_sidney = (0 if (InpStartSidney >= 24) else InpStartSidney)
    end_sidney = (0 if (InpEndSidney >= 24) else InpEndSidney)
    start_tokio = (0 if (InpStartTokio >= 24) else InpStartTokio)
    end_tokio = (0 if (InpEndTokio >= 24) else InpEndTokio)
    start_london = (0 if (InpStartLondon >= 24) else InpStartLondon)
    end_london = (0 if (InpEndLondon >= 24) else InpEndLondon)
    start_new_york = (0 if (InpStartNewYork >= 24) else InpStartNewYork)
    end_new_york = (0 if (InpEndNewYork >= 24) else InpEndNewYork)
    width = (1 if (InpWidth < 1) else InpWidth)
    font_size = (5 if (InpFontSize < 5) else InpFontSize)
    if Period() > PERIOD_H1:
        Alert('This indicator works only on H1 charts and lower')
        ChartSetSymbolPeriod(0, None, PERIOD_H1)
    prev_fgnd = (ChartGetInteger(0, CHART_FOREGROUND) != 0)
    ChartSetInteger(0, CHART_FOREGROUND, False)
    ChartRedraw()
    SetIndexBuffer(0, BufferSidney1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSidney2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferTokio1, INDICATOR_DATA)
    SetIndexBuffer(3, BufferTokio2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferLondon1, INDICATOR_DATA)
    SetIndexBuffer(5, BufferLondon2, INDICATOR_DATA)
    SetIndexBuffer(6, BufferNewYork1, INDICATOR_DATA)
    SetIndexBuffer(7, BufferNewYork2, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Market Sessions')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, 'Sidney session;  from ' + _str(start_sidney) + ' to ' + _str(end_sidney))
    PlotIndexSetString(1, PLOT_LABEL, 'Tokio session;  from ' + _str(start_tokio) + ' to ' + _str(end_tokio))
    PlotIndexSetString(2, PLOT_LABEL, 'London session;  from ' + _str(start_london) + ' to ' + _str(end_london))
    PlotIndexSetString(3, PLOT_LABEL, 'NewYork session;  from ' + _str(start_new_york) + ' to ' + _str(end_new_york))
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, InpColorSidney)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, InpColorSidney)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 0, InpColorTokio)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 1, InpColorTokio)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, 0, InpColorLondon)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, 1, InpColorLondon)
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, 0, InpColorNewYork)
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, 1, InpColorNewYork)
    ArraySetAsSeries(BufferSidney1, True)
    ArraySetAsSeries(BufferSidney2, True)
    ArraySetAsSeries(BufferTokio1, True)
    ArraySetAsSeries(BufferTokio2, True)
    ArraySetAsSeries(BufferLondon1, True)
    ArraySetAsSeries(BufferLondon2, True)
    ArraySetAsSeries(BufferNewYork1, True)
    ArraySetAsSeries(BufferNewYork2, True)
    Time("", PERIOD_D1, 1)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ChartSetInteger(0, CHART_FOREGROUND, prev_fgnd)
    ObjectsDeleteAll(0, prefix)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if rates_total < 24:
        return 0
    if Time("", PERIOD_D1, 1) == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferSidney1, 0)
        ArrayInitialize(BufferSidney2, 0)
        ArrayInitialize(BufferTokio1, 0)
        ArrayInitialize(BufferTokio2, 0)
        ArrayInitialize(BufferLondon1, 0)
        ArrayInitialize(BufferLondon2, 0)
        ArrayInitialize(BufferNewYork1, 0)
        ArrayInitialize(BufferNewYork2, 0)
    for i in range(limit, 0 - 1, -1):
        Initialize(i)
        if IsTradeTime(time[i], start_sidney, 0, end_sidney, 0):
            Calculations(i, time, start_sidney, BufferSidney1, BufferSidney2, SESSION_SIDNEY)
        if IsTradeTime(time[i], start_tokio, 0, end_tokio, 0):
            Calculations(i, time, start_tokio, BufferTokio1, BufferTokio2, SESSION_TOKIO)
        if IsTradeTime(time[i], start_london, 0, end_london, 0):
            Calculations(i, time, start_london, BufferLondon1, BufferLondon2, SESSION_LONDON)
        if IsTradeTime(time[i], start_new_york, 0, end_new_york, 0):
            Calculations(i, time, start_new_york, BufferNewYork1, BufferNewYork2, SESSION_NEW_YORK)
    return rates_total

def OnTimer():
    Time("", PERIOD_D1, 1)

def Initialize(shift):
    BufferTokio2[shift] = 0.0
    BufferTokio1[shift] = BufferTokio2[shift]
    BufferSidney2[shift] = BufferTokio1[shift]
    BufferSidney1[shift] = BufferSidney2[shift]
    BufferNewYork2[shift] = BufferSidney1[shift]
    BufferNewYork1[shift] = BufferNewYork2[shift]
    BufferLondon2[shift] = BufferNewYork1[shift]
    BufferLondon1[shift] = BufferLondon2[shift]

def Calculations(shift, time, hour_start, buffer1, buffer2, session):
    bar = BarShift("", PERIOD_D1, time[shift])
    if bar == WRONG_VALUE:
        return
    p1 = High("", PERIOD_D1, bar)
    if p1 == 0:
        return
    buffer1[shift] = p1 - ((width + 4) * session * Point())
    buffer2[shift] = buffer1[shift] - (width * Point())
    if TimeHour_u(time[shift]) == hour_start and TimeMinute_u(time[shift]) == 0:
        if InpShowLabels:
            text = ' NewYork'
            end = 'NY'
            tooltip = 'NewYork session time:\nfrom ' + IntegerToString(start_new_york, 2, 48) + ':00 to ' + IntegerToString(end_new_york, 2, 48) + ':00'
            if session == SESSION_SIDNEY:
                text = ' Sidney'
                end = 'SD'
                tooltip = 'Sidney session time:\nfrom ' + IntegerToString(start_sidney, 2, 48) + ':00 to ' + IntegerToString(end_sidney, 2, 48) + ':00'
            elif session == SESSION_TOKIO:
                text = ' Tokio'
                end = 'TK'
                tooltip = 'Tokio session time:\nfrom ' + IntegerToString(start_tokio, 2, 48) + ':00 to ' + IntegerToString(end_tokio, 2, 48) + ':00'
            elif session == SESSION_LONDON:
                text = ' London'
                end = 'LD'
                tooltip = 'London session time:\nfrom ' + IntegerToString(start_london, 2, 48) + ':00 to ' + IntegerToString(end_london, 2, 48) + ':00'
            name = prefix + TimeToString(time[shift]) + end
            DrawLabel(name, text, tooltip, time[shift], buffer1[shift], InpFontColor)
        if InpShowVLines:
            clr = InpColorNewYork
            text = ' NewYork'
            end = 'NY_VL'
            tooltip = ' NewYork session time from ' + IntegerToString(start_new_york, 2, 48) + ':00 to ' + IntegerToString(end_new_york, 2, 48) + ':00'
            if session == SESSION_SIDNEY:
                clr = InpColorSidney
                text = ' Sidney'
                end = 'SD_VL'
                tooltip = ' Sidney session time from ' + IntegerToString(start_sidney, 2, 48) + ':00 to ' + IntegerToString(end_sidney, 2, 48) + ':00'
            elif session == SESSION_TOKIO:
                clr = InpColorTokio
                text = ' Tokio'
                end = 'TK_VL'
                tooltip = ' Tokio session time from ' + IntegerToString(start_tokio, 2, 48) + ':00 to ' + IntegerToString(end_tokio, 2, 48) + ':00'
            elif session == SESSION_LONDON:
                clr = InpColorLondon
                text = ' London'
                end = 'LD_VL'
                tooltip = ' London session time from ' + IntegerToString(start_london, 2, 48) + ':00 to ' + IntegerToString(end_london, 2, 48) + ':00'
            name = prefix + TimeToString(time[shift]) + end
            DrawLine(name, text, tooltip, time[shift], clr)

def IsTradeTime(time_current, hour_begin=0, minutes_begin=0, hour_end=0, minutes_end=0):
    tmb = MqlDateTime()
    tme = MqlDateTime()
    tradetime_begin = 0
    tradetime_end = 0
    current_serv_hour = 0
    TimeToStruct(time_current, tmb)
    current_serv_hour = tmb.hour
    TimeToStruct(time_current, tme)
    tmb.hour = hour_begin
    tmb.min = minutes_begin
    tme.hour = hour_end
    tme.min = minutes_end
    tradetime_begin = StructToTime(tmb)
    tradetime_end = StructToTime(tme)
    if tradetime_begin >= tradetime_end:
        if current_serv_hour >= hour_end:
            tradetime_end += 24 * PeriodSeconds(PERIOD_H1)
        else:
            tradetime_begin -= 24 * PeriodSeconds(PERIOD_H1)
    return time_current >= tradetime_begin and time_current <= tradetime_end

def BarShift(symbol_name, timeframe, time, exact=False):
    res = Bars(symbol_name, timeframe, time + 1, UINT_MAX)
    if exact:
        if (timeframe != PERIOD_MN1 or time > TimeCurrent()) and res == Bars(symbol_name, timeframe, time - PeriodSeconds(timeframe) + 1, UINT_MAX):
            return WRONG_VALUE
    return res

def High(symbol_name, timeframe, shift):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyHigh(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def Time(symbol_name, timeframe, shift):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyTime(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def TimeHour_u(time):
    tm = MqlDateTime()
    if not TimeToStruct(time, tm):
        return WRONG_VALUE
    return tm.hour

def TimeMinute_u(time):
    tm = MqlDateTime()
    if not TimeToStruct(time, tm):
        return WRONG_VALUE
    return tm.min

def DrawLabel(name, text, tooltip, time, price, text_color):
    if ObjectFind(0, name) < 0:
        ObjectCreate(0, name, OBJ_TEXT, 0, 0, 0)
        ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
        ObjectSetInteger(0, name, OBJPROP_COLOR, text_color)
        ObjectSetInteger(0, name, OBJPROP_FONTSIZE, InpFontSize)
        ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_LEFT)
        ObjectSetString(0, name, OBJPROP_FONT, InpFontName)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, time)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price - (_idiv(width, 2) * Point()))
    ObjectSetString(0, name, OBJPROP_TEXT, text)
    ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip)

def DrawLine(name, text, tooltip, time, line_color):
    if ObjectFind(0, name) < 0:
        ObjectCreate(0, name, OBJ_VLINE, 0, 0, 0)
        ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
        ObjectSetInteger(0, name, OBJPROP_COLOR, line_color)
        ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_DOT)
        ObjectSetInteger(0, name, OBJPROP_RAY, False)
    ObjectSetInteger(0, name, OBJPROP_TIME, time)
    ObjectSetString(0, name, OBJPROP_TEXT, text)
    ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MarketSessions(_MQL5Indicator):
    name = 'Market_Sessions'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpStartSidney': 0,  # Sidney session begin
        'InpEndSidney': 9,  # Sidney session end
        'InpStartTokio': 2,  # Tokio session begin
        'InpEndTokio': 11,  # Tokio session end
        'InpStartLondon': 10,  # London session begin
        'InpEndLondon': 19,  # London session end
        'InpStartNewYork': 15,  # NewYork session begin
        'InpEndNewYork': 0,  # NewYork session end
        'InpWidth': 60,  # Session field height
        'InpShowLabels': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show session labels
        'InpFontSize': 8,  # Font size
        'InpShowVLines': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show start-session lines
    }

