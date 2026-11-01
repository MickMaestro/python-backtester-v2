"""Stats on Amplitude, Spread and Clock — converted from MQL5: MQL5 Indicators/Simple label indicator that shows Amplitude, Spread and Clock (time)/Stats on Amplitude, Spread and Clock.mq5

This simple indicator is just a statistical label showing Last and Current Candle Amplitude (MinMax), Last and Current Day Amplitude, Current Tick Amplitude and Time Remaining for next Candle.\\n
It also shows Server Time (Market Watch) and Local PC Time so you can focus more on the graph and adapt to market hours.\\n
You can get the source code at \\n\\thttps://github.com/BRMateus2/Simple-MQL5-Amplitude-Spread-and-Clock-Labels/
Copyright: 2021, Mateus Matucuma Teixeira; Link: https://github.com/BRMateus2/Simple-MQL5-Amplitude-Spread-and-Clock-Labels/; Version: 1.07

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2021, Mateus Matucuma Teixeira', 'link': 'https://github.com/BRMateus2/Simple-MQL5-Amplitude-Spread-and-Clock-Labels/', 'version': '1.07', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['This simple indicator is just a statistical label showing Last and Current Candle Amplitude (MinMax), Last and Current Day Amplitude, Current Tick Amplitude and Time Remaining for next Candle.\\n', 'It also shows Server Time (Market Watch) and Local PC Time so you can focus more on the graph and adapt to market hours.\\n', 'You can get the source code at \\n\\thttps://github.com/BRMateus2/Simple-MQL5-Amplitude-Spread-and-Clock-Labels/'], 'name': 'Stats on Amplitude, Spread and Clock', 'source': 'MQL5 Indicators/Simple label indicator that shows Amplitude, Spread and Clock (time)/Stats on Amplitude, Spread and Clock.mq5', 'folder': 'Simple label indicator that shows Amplitude, Spread and Clock (time)', 'inputs': [{'mql': 'lColor', 'py': 'lColor', 'param': None, 'type': 'color', 'default': 65535, 'label': 'Text Color', 'sinput': False}, {'mql': 'lCorner', 'py': 'lCorner', 'param': 'lCorner', 'type': 'int', 'default': 3, 'label': 'Text Corner', 'sinput': False}, {'mql': 'lFontSize', 'py': 'lFontSize', 'param': 'lFontSize', 'type': 'long', 'default': 12, 'label': 'Font Size', 'sinput': False}, {'mql': 'lFontName', 'py': 'lFontName', 'param': None, 'type': 'string', 'default': 'DejaVu Sans Mono', 'label': 'Font Name (system naming)', 'sinput': False}, {'mql': 'oDistX', 'py': 'oDistX', 'param': 'oDistX', 'type': 'long', 'default': 0, 'label': 'X Distance or Horizontal Position Offset', 'sinput': False}, {'mql': 'oDistY', 'py': 'oDistY', 'param': 'oDistY', 'type': 'long', 'default': 0, 'label': 'Y Distance or Vertical Position Offset', 'sinput': False}, {'mql': 'oSpacingY', 'py': 'oSpacingY', 'param': 'oSpacingY', 'type': 'long', 'default': 3, 'label': 'Vertical gap between objects', 'sinput': False}, {'mql': 'oStatsShow', 'py': 'oStatsShow', 'param': 'oStatsShow', 'type': 'bool', 'default': True, 'label': 'Show Statistics line?', 'sinput': False}, {'mql': 'weekRange', 'py': 'weekRange', 'param': 'weekRange', 'type': 'int', 'default': 52, 'label': 'How many weeks should the range contain? Normally 52 weeks', 'sinput': False}, {'mql': 'sFormat', 'py': 'sFormat', 'param': 'sFormat', 'type': 'int', 'default': 1, 'label': 'Amplitude and Spread Stats Format', 'sinput': False}, {'mql': 'oStatsShowMktClosed', 'py': 'oStatsShowMktClosed', 'param': 'oStatsShowMktClosed', 'type': 'bool', 'default': True, 'label': 'If there is no new ticks for 5m, show "Closed"/"Disconnected"?', 'sinput': False}, {'mql': 'dFormat', 'py': 'dFormat', 'param': 'dFormat', 'type': 'int', 'default': 2, 'label': 'Date Format', 'sinput': False}, {'mql': 'dShowOffset', 'py': 'dShowOffset', 'param': 'dShowOffset', 'type': 'bool', 'default': True, 'label': 'Show UTC Timezone Offset?', 'sinput': False}, {'mql': 'dShowSameLine', 'py': 'dShowSameLine', 'param': 'dShowSameLine', 'type': 'bool', 'default': True, 'label': 'Show both dates on the same line?', 'sinput': False}, {'mql': 'dUseServer', 'py': 'dUseServer', 'param': 'dUseServer', 'type': 'bool', 'default': True, 'label': 'Use Server Date instead of Local/UTC Date?', 'sinput': False}, {'mql': 'dServerOffset', 'py': 'dServerOffset', 'param': 'dServerOffset', 'type': 'int', 'default': 0, 'label': 'Offset in seconds', 'sinput': False}, {'mql': 'oCSLatencyAppend', 'py': 'oCSLatencyAppend', 'param': 'oCSLatencyAppend', 'type': 'bool', 'default': False, 'label': 'DEBUG: append latency of the last 20 calls to Server Label', 'sinput': False}, {'mql': 'oCSLatencyHP', 'py': 'oCSLatencyHP', 'param': 'oCSLatencyHP', 'type': 'bool', 'default': False, 'label': 'DEBUG: use 1ms OnTimer() instead of power-saving 1000ms', 'sinput': False}, {'mql': 'dShowLocal', 'py': 'dShowLocal', 'param': 'dShowLocal', 'type': 'bool', 'default': True, 'label': 'Show Local Time Label?', 'sinput': False}, {'mql': 'dShowLocalAsUTC', 'py': 'dShowLocalAsUTC', 'param': 'dShowLocalAsUTC', 'type': 'bool', 'default': False, 'label': 'Use UTC+0 / GMT Time instead of Local Timezone?', 'sinput': False}, {'mql': 'dLocalOffset', 'py': 'dLocalOffset', 'param': 'dLocalOffset', 'type': 'int', 'default': 0, 'label': 'Offset in seconds', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

TERMINAL_RETRANSMISSION = 0  # MQL5 constant unknown to the converter

# enum SFormat
kSFormatFirst = 0
kSFormatSecond = 1
_enum('SFormat', {0: 'kSFormatFirst', 1: 'kSFormatSecond'})

# enum DateFormat
kTimeSeconds = 0
kTimeMinutes = 1
kTimeDateSeconds = 2
kTimeDateMinutes = 3
_enum('DateFormat', {0: 'kTimeSeconds', 1: 'kTimeMinutes', 2: 'kTimeDateSeconds', 3: 'kTimeDateMinutes'})

# ---- inputs and global variables
iName = 'StatsAndClock'
lColor = _input('lColor', clrYellow)  # Text Color
lCorner = _input('lCorner', CORNER_RIGHT_UPPER)  # Text Corner
lFontSize = _input('lFontSize', 12)  # Font Size
lFontName = _input('lFontName', 'DejaVu Sans Mono')  # Font Name (system naming)
oDistX = _input('oDistX', 0)  # X Distance or Horizontal Position Offset
oDistY = _input('oDistY', 0)  # Y Distance or Vertical Position Offset
oSpacingY = _input('oSpacingY', 3)  # Vertical gap between objects
oStatsShow = _input('oStatsShow', True)  # Show Statistics line?
weekRange = _input('weekRange', 52)  # How many weeks should the range contain? Normally 52 weeks
sFormat = _input('sFormat', kSFormatSecond)  # Amplitude and Spread Stats Format
oStatsShowMktClosed = _input('oStatsShowMktClosed', True)  # If there is no new ticks for 5m, show "Closed"/"Disconnected"?
oStatsShowMktClosedTimer = 60  # Inactivity timer, which if there are no new quotes, will show as "Mkt Closed"
dFormat = _input('dFormat', kTimeDateSeconds)  # Date Format
dShowOffset = _input('dShowOffset', True)  # Show UTC Timezone Offset?
dShowSameLine = _input('dShowSameLine', True)  # Show both dates on the same line?
dUseServer = _input('dUseServer', True)  # Use Server Date instead of Local/UTC Date?
dServerOffset = _input('dServerOffset', 0)  # Offset in seconds
oCSLatencyAppend = _input('oCSLatencyAppend', False)  # DEBUG: append latency of the last 20 calls to Server Label
oCSLatencyHP = _input('oCSLatencyHP', False)  # DEBUG: use 1ms OnTimer() instead of power-saving 1000ms
dShowLocal = _input('dShowLocal', True)  # Show Local Time Label?
dShowLocalAsUTC = _input('dShowLocalAsUTC', False)  # Use UTC+0 / GMT Time instead of Local Timezone?
dLocalOffset = _input('dLocalOffset', 0)  # Offset in seconds
oStats = 'AmplitudeAndSpread'  # Object Stats, used for naming
oCS = 'ClockServer'  # Object Clock Server, used for naming
oCL = 'ClockLocal'  # Object Clock Local, used for naming
last = 0
getMicrosecondCountBuf = Arr.of([], fill=0, dyn=False, size=20)
getMicrosecondCountLast = 0
getMicrosecondCountI = 0
getMicrosecondCountJ = 0
getMicrosecondCountMean = 0

def OnInit():
    global getMicrosecondCountLast, last
    last = TimeGMT()
    getMicrosecondCountLast = GetMicrosecondCount()
    IndicatorSetString(INDICATOR_SHORTNAME, iName)
    ObjectDelete(ChartID(), oStats)
    ObjectDelete(ChartID(), oCS)
    ObjectDelete(ChartID(), oCL)
    if oStatsShow:
        if not ObjectCreate(ChartID(), oStats, OBJ_LABEL, ChartWindowFind(ChartID(), iName), 0, 0.0):
            Print('ERROR: ' + 'Object creation with ChartID() ' + IntegerToString(ChartID()) + ' at window ' + IntegerToString(ChartWindowFind(ChartID(), iName)) + ' at "' + 'OnInit' + ':' + IntegerToString(120) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Stats on Amplitude, Spread and Clock.mq5' + ')')
            ResetLastError()
            DebugBreak()
        ObjectSetInteger(ChartID(), oStats, OBJPROP_CORNER, lCorner)
        ObjectSetInteger(ChartID(), oStats, OBJPROP_XDISTANCE, oDistX)
        ObjectSetInteger(ChartID(), oStats, OBJPROP_YDISTANCE, oDistY)
        ObjectSetInteger(ChartID(), oStats, OBJPROP_FONTSIZE, lFontSize)
        ObjectSetInteger(ChartID(), oStats, OBJPROP_COLOR, lColor)
        ObjectSetString(ChartID(), oStats, OBJPROP_FONT, lFontName)
        ObjectSetString(ChartID(), oStats, OBJPROP_TEXT, oStats)
    ObjectCreate(ChartID(), oCS, OBJ_LABEL, ChartWindowFind(ChartID(), iName), 0, 0.0)
    ObjectSetInteger(ChartID(), oCS, OBJPROP_CORNER, lCorner)
    ObjectSetInteger(ChartID(), oCS, OBJPROP_XDISTANCE, oDistX)
    ObjectSetInteger(ChartID(), oCS, OBJPROP_YDISTANCE, ((lFontSize + oSpacingY + oDistY) if oStatsShow else oDistY))
    ObjectSetInteger(ChartID(), oCS, OBJPROP_FONTSIZE, lFontSize)
    ObjectSetInteger(ChartID(), oCS, OBJPROP_COLOR, lColor)
    ObjectSetString(ChartID(), oCS, OBJPROP_FONT, lFontName)
    ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, oCS)
    if dShowLocal and (not dShowSameLine):
        ObjectCreate(ChartID(), oCL, OBJ_LABEL, ChartWindowFind(ChartID(), iName), 0, 0.0)
        ObjectSetInteger(ChartID(), oCL, OBJPROP_CORNER, lCorner)
        ObjectSetInteger(ChartID(), oCL, OBJPROP_XDISTANCE, oDistX)
        ObjectSetInteger(ChartID(), oCL, OBJPROP_YDISTANCE, (((2 * (lFontSize + oSpacingY)) + oDistY) if oStatsShow else (lFontSize + oSpacingY + oDistY)))
        ObjectSetInteger(ChartID(), oCL, OBJPROP_FONTSIZE, lFontSize)
        ObjectSetInteger(ChartID(), oCL, OBJPROP_COLOR, lColor)
        ObjectSetString(ChartID(), oCL, OBJPROP_FONT, lFontName)
        ObjectSetString(ChartID(), oCL, OBJPROP_TEXT, oCL)
    anchor = ANCHOR_LEFT_UPPER
    _sw1 = lCorner
    if _sw1 == CORNER_LEFT_UPPER:
        anchor = ANCHOR_LEFT_UPPER
    elif _sw1 == CORNER_RIGHT_UPPER:
        anchor = ANCHOR_RIGHT_UPPER
    elif _sw1 == CORNER_LEFT_LOWER:
        anchor = ANCHOR_LEFT_LOWER
    elif _sw1 == CORNER_RIGHT_LOWER:
        anchor = ANCHOR_RIGHT_LOWER
    if oStatsShow:
        ObjectSetInteger(ChartID(), oStats, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(ChartID(), oCS, OBJPROP_ANCHOR, anchor)
    if dShowLocal and (not dShowSameLine):
        ObjectSetInteger(ChartID(), oCL, OBJPROP_ANCHOR, anchor)
    if oCSLatencyHP:
        if not EventSetMillisecondTimer(1):
            Print('ERROR: ' + '!EventSetMillisecondTimer(1) failure at subscribing to event timer' + ' at "' + 'OnInit' + ':' + IntegerToString(176) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Stats on Amplitude, Spread and Clock.mq5' + ')')
            ResetLastError()
            DebugBreak()
            return INIT_FAILED
    elif not EventSetTimer(1):
        Print('ERROR: ' + '!EventSetTimer(1) failure at subscribing to event timer' + ' at "' + 'OnInit' + ':' + IntegerToString(180) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Stats on Amplitude, Spread and Clock.mq5' + ')')
        ResetLastError()
        DebugBreak()
        return INIT_FAILED
    OnTimer()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(ChartID(), oStats)
    ObjectDelete(ChartID(), oCS)
    ObjectDelete(ChartID(), oCL)
    EventKillTimer()
    return

def OnTimer():
    global getMicrosecondCountI, getMicrosecondCountJ, getMicrosecondCountLast, getMicrosecondCountMean
    if False:
        return
    if (not dShowLocal) and (not dShowOffset):
        ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)))
    elif (not dShowLocal) and dShowOffset:
        ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)) + ' ' + TimeGMTOffset_u(TimeTradeServer() + dServerOffset))
    elif (dShowLocal and dShowSameLine) and (dFormat == kTimeSeconds or dFormat == kTimeDateSeconds):
        if ((not dShowLocalAsUTC) and dUseServer) and (not dShowOffset):
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)) + ' ' + TimeToString(TimeLocal() + dLocalOffset, TIME_SECONDS))
        elif (dShowLocalAsUTC and dUseServer) and (not dShowOffset):
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)) + ' ' + TimeToString(TimeGMT() + dLocalOffset, TIME_SECONDS))
        elif ((not dShowLocalAsUTC) and (not dUseServer)) and (not dShowOffset):
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, TIME_SECONDS) + ' ' + TimeToString(TimeLocal() + dLocalOffset, EnumToInt(dFormat)))
        elif (dShowLocalAsUTC and (not dUseServer)) and (not dShowOffset):
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, TIME_SECONDS) + ' ' + TimeToString(TimeGMT() + dLocalOffset, EnumToInt(dFormat)))
        elif ((not dShowLocalAsUTC) and dUseServer) and dShowOffset:
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)) + ' ' + TimeGMTOffset_u(TimeTradeServer() + dServerOffset) + ' ' + TimeToString(TimeLocal() + dLocalOffset, TIME_SECONDS) + ' ' + TimeGMTOffset_u(TimeLocal() + dLocalOffset))
        elif (dShowLocalAsUTC and dUseServer) and dShowOffset:
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)) + ' ' + TimeGMTOffset_u(TimeTradeServer() + dServerOffset) + ' ' + TimeToString(TimeGMT() + dLocalOffset, TIME_SECONDS) + ' ' + TimeGMTOffset_u(TimeGMT() + dLocalOffset))
        elif ((not dShowLocalAsUTC) and (not dUseServer)) and dShowOffset:
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, TIME_SECONDS) + ' ' + TimeGMTOffset_u(TimeTradeServer() + dServerOffset) + ' ' + TimeToString(TimeLocal() + dLocalOffset, EnumToInt(dFormat)) + ' ' + TimeGMTOffset_u(TimeLocal() + dLocalOffset))
        elif (dShowLocalAsUTC and (not dUseServer)) and dShowOffset:
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, TIME_SECONDS) + ' ' + TimeGMTOffset_u(TimeTradeServer() + dServerOffset) + ' ' + TimeToString(TimeGMT() + dLocalOffset, EnumToInt(dFormat)) + ' ' + TimeGMTOffset_u(TimeGMT() + dLocalOffset))
        else:
            Print('ERROR: ' + 'untreated condition with dShowLocal: "' + _str(dShowLocal) + '" ' + 'dShowOffset: "' + _str(dShowOffset) + '" ' + 'dShowSameLine: "' + _str(dShowSameLine) + '" ' + 'dFormat: "' + EnumToString(dFormat, 'DateFormat') + '" ' + 'dShowLocalAsUTC: "' + _str(dShowLocalAsUTC) + '" ' + 'dUseServer: "' + _str(dUseServer) + '" ' + '"' + ' at "' + 'OnTimer' + ':' + IntegerToString(231) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Stats on Amplitude, Spread and Clock.mq5' + ')')
            ResetLastError()
            DebugBreak()
    elif (dShowLocal and dShowSameLine) and (dFormat == kTimeMinutes or dFormat == kTimeDateMinutes):
        if ((not dShowLocalAsUTC) and dUseServer) and (not dShowOffset):
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)) + ' ' + TimeToString(TimeLocal() + dLocalOffset, TIME_MINUTES))
        elif (dShowLocalAsUTC and dUseServer) and (not dShowOffset):
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)) + ' ' + TimeToString(TimeGMT() + dLocalOffset, TIME_MINUTES))
        elif ((not dShowLocalAsUTC) and (not dUseServer)) and (not dShowOffset):
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, TIME_MINUTES) + ' ' + TimeToString(TimeLocal() + dLocalOffset, EnumToInt(dFormat)))
        elif (dShowLocalAsUTC and (not dUseServer)) and (not dShowOffset):
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, TIME_MINUTES) + ' ' + TimeToString(TimeGMT() + dLocalOffset, EnumToInt(dFormat)))
        elif ((not dShowLocalAsUTC) and dUseServer) and dShowOffset:
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)) + ' ' + TimeGMTOffset_u(TimeTradeServer() + dServerOffset) + ' ' + TimeToString(TimeLocal() + dLocalOffset, TIME_MINUTES) + ' ' + TimeGMTOffset_u(TimeLocal() + dLocalOffset))
        elif (dShowLocalAsUTC and dUseServer) and dShowOffset:
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)) + ' ' + TimeGMTOffset_u(TimeTradeServer() + dServerOffset) + ' ' + TimeToString(TimeGMT() + dLocalOffset, TIME_MINUTES) + ' ' + TimeGMTOffset_u(TimeGMT() + dLocalOffset))
        elif ((not dShowLocalAsUTC) and (not dUseServer)) and dShowOffset:
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, TIME_MINUTES) + ' ' + TimeGMTOffset_u(TimeTradeServer() + dServerOffset) + ' ' + TimeToString(TimeLocal() + dLocalOffset, EnumToInt(dFormat)) + ' ' + TimeGMTOffset_u(TimeLocal() + dLocalOffset))
        elif (dShowLocalAsUTC and (not dUseServer)) and dShowOffset:
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, TIME_MINUTES) + ' ' + TimeGMTOffset_u(TimeTradeServer() + dServerOffset) + ' ' + TimeToString(TimeGMT() + dLocalOffset, EnumToInt(dFormat)) + ' ' + TimeGMTOffset_u(TimeGMT() + dLocalOffset))
        else:
            Print('ERROR: ' + 'untreated condition with dShowLocal: "' + _str(dShowLocal) + '" ' + 'dShowOffset: "' + _str(dShowOffset) + '" ' + 'dShowSameLine: "' + _str(dShowSameLine) + '" ' + 'dFormat: "' + EnumToString(dFormat, 'DateFormat') + '" ' + 'dShowLocalAsUTC: "' + _str(dShowLocalAsUTC) + '" ' + 'dUseServer: "' + _str(dUseServer) + '" ' + '"' + ' at "' + 'OnTimer' + ':' + IntegerToString(251) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Stats on Amplitude, Spread and Clock.mq5' + ')')
            ResetLastError()
            DebugBreak()
    elif dShowLocal and (not dShowSameLine):
        if (not dShowLocalAsUTC) and (not dShowOffset):
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)))
            ObjectSetString(ChartID(), oCL, OBJPROP_TEXT, TimeToString(TimeLocal() + dLocalOffset, EnumToInt(dFormat)))
        elif (not dShowLocalAsUTC) and dShowOffset:
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)) + ' ' + TimeGMTOffset_u(TimeTradeServer() + dServerOffset))
            ObjectSetString(ChartID(), oCL, OBJPROP_TEXT, TimeToString(TimeLocal() + dLocalOffset, EnumToInt(dFormat)) + ' ' + TimeGMTOffset_u(TimeLocal() + dLocalOffset))
        elif dShowLocalAsUTC and (not dShowOffset):
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)))
            ObjectSetString(ChartID(), oCL, OBJPROP_TEXT, TimeToString(TimeGMT() + dLocalOffset, EnumToInt(dFormat)))
        elif dShowLocalAsUTC and dShowOffset:
            ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, TimeToString(TimeTradeServer() + dServerOffset, EnumToInt(dFormat)) + ' ' + TimeGMTOffset_u(TimeTradeServer() + dServerOffset))
            ObjectSetString(ChartID(), oCL, OBJPROP_TEXT, TimeToString(TimeGMT() + dLocalOffset, EnumToInt(dFormat)) + ' ' + TimeGMTOffset_u(TimeGMT() + dLocalOffset))
        else:
            Print('ERROR: ' + 'untreated condition with dShowLocal: "' + _str(dShowLocal) + '" ' + 'dShowOffset: "' + _str(dShowOffset) + '" ' + 'dShowSameLine: "' + _str(dShowSameLine) + '" ' + 'dFormat: "' + EnumToString(dFormat, 'DateFormat') + '" ' + 'dShowLocalAsUTC: "' + _str(dShowLocalAsUTC) + '" ' + 'dUseServer: "' + _str(dUseServer) + '" ' + '"' + ' at "' + 'OnTimer' + ':' + IntegerToString(267) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Stats on Amplitude, Spread and Clock.mq5' + ')')
            ResetLastError()
            DebugBreak()
    else:
        Print('ERROR: ' + 'untreated condition with dShowLocal: "' + _str(dShowLocal) + '" ' + 'dShowOffset: "' + _str(dShowOffset) + '" ' + 'dShowSameLine: "' + _str(dShowSameLine) + '" ' + 'dFormat: "' + EnumToString(dFormat, 'DateFormat') + '" ' + 'dShowLocalAsUTC: "' + _str(dShowLocalAsUTC) + '" ' + 'dUseServer: "' + _str(dUseServer) + '" ' + '"' + ' at "' + 'OnTimer' + ':' + IntegerToString(270) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Stats on Amplitude, Spread and Clock.mq5' + ')')
        ResetLastError()
        DebugBreak()
    if last < TimeGMT() and oStatsShow:
        statsUpdate()
    if oCSLatencyAppend:
        getMicrosecondCountBuf[((getMicrosecondCountI := getMicrosecondCountI + 1) - 1)] = GetMicrosecondCount() - getMicrosecondCountLast
        if getMicrosecondCountI > 19:
            getMicrosecondCountI = 0
        getMicrosecondCountJ = 0
        getMicrosecondCountMean = 0
        while getMicrosecondCountJ < 20 and getMicrosecondCountBuf[getMicrosecondCountJ] > 0:
            getMicrosecondCountMean = getMicrosecondCountMean + getMicrosecondCountBuf[getMicrosecondCountJ]
            getMicrosecondCountJ += 1
        getMicrosecondCountMean = _idiv(getMicrosecondCountMean, getMicrosecondCountJ * 1000)
        ObjectSetString(ChartID(), oCS, OBJPROP_TOOLTIP, 'Last 20 calls latency of OnTimer(): ' + IntegerToString(getMicrosecondCountMean) + 'ms')
        ObjectSetString(ChartID(), oCS, OBJPROP_TEXT, ObjectGetString(ChartID(), oCS, OBJPROP_TEXT) + ' ' + IntegerToString(getMicrosecondCountMean) + 'ms')
        getMicrosecondCountLast = GetMicrosecondCount()
        if oStatsShow:
            ObjectSetString(ChartID(), oStats, OBJPROP_TOOLTIP, 'Server Latency: ' + IntegerToString(TerminalInfoInteger(TERMINAL_PING_LAST)) + 'us' + '/Packet Retransmissions: ' + DoubleToString(TerminalInfoDouble(TERMINAL_RETRANSMISSION), 2) + '%')
    ChartRedraw()
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (not oStatsShow) or rates_total <= 2:
        return 0
    statsUpdate()
    return rates_total

def statsUpdate():
    global last
    last = TimeGMT()
    m = _ulong((0 if ((iTime(Symbol(), PERIOD_CURRENT, 0) + PeriodSeconds(PERIOD_CURRENT) - TimeCurrent()) < 0) else (iTime(Symbol(), PERIOD_CURRENT, 0) + PeriodSeconds(PERIOD_CURRENT) - TimeCurrent())))
    s = _imod(m, 60)
    m = _idiv(m - s, 60)
    if sFormat == kSFormatFirst:
        ObjectSetString(ChartID(), oStats, OBJPROP_TEXT, 'Ampl(' + DoubleToString(iHigh(Symbol(), PERIOD_CURRENT, 1) - iLow(Symbol(), PERIOD_CURRENT, 1), Digits()) + '/' + DoubleToString(iHigh(Symbol(), PERIOD_CURRENT, 0) - iLow(Symbol(), PERIOD_CURRENT, 0), Digits()) + ')/D1(' + DoubleToString(iHigh(Symbol(), PERIOD_D1, 1) - iLow(Symbol(), PERIOD_D1, 1), Digits()) + '/' + DoubleToString(iHigh(Symbol(), PERIOD_D1, 0) - iLow(Symbol(), PERIOD_D1, 0), Digits()) + ') Spr(' + IntegerToString(SymbolInfoInteger(Symbol(), SYMBOL_SPREAD)) + ('...' if (SymbolInfoInteger(Symbol(), SYMBOL_SPREAD) < 10) else '..' if (SymbolInfoInteger(Symbol(), SYMBOL_SPREAD) < 100) else '.' if (SymbolInfoInteger(Symbol(), SYMBOL_SPREAD) < 1000) else '') + ') ' + ('Mkt Closed' if ((SymbolInfoInteger(Symbol(), SYMBOL_TIME) < (TimeCurrent() - oStatsShowMktClosedTimer) and oStatsShowMktClosed) and TerminalInfoInteger(TERMINAL_CONNECTED)) else 'Disconnected' if (oStatsShowMktClosed and (not TerminalInfoInteger(TERMINAL_CONNECTED))) else (('0' if (m < 10) else '') + IntegerToString((0 if (m < 0) else m)) + ':' + ('0' if (s < 10) else '') + IntegerToString((0 if (s < 0) else s)))))
    elif sFormat == kSFormatSecond:
        ObjectSetString(ChartID(), oStats, OBJPROP_TEXT, 'Chg(' + DoubleToString(((_fdiv(iClose(Symbol(), PERIOD_D1, 1) * 100.0, iClose(Symbol(), PERIOD_D1, 2)) - 100.0) if iClose(Symbol(), PERIOD_D1, 2) else 0.0), 2) + '%/' + DoubleToString(((_fdiv(iClose(Symbol(), PERIOD_D1, 0) * 100.0, iClose(Symbol(), PERIOD_D1, 1)) - 100.0) if iClose(Symbol(), PERIOD_D1, 1) else 0.0), 2) + '%) W' + IntegerToString(weekRange) + '[' + DoubleToString(iLow(Symbol(), PERIOD_W1, iLowest(Symbol(), PERIOD_W1, MODE_LOW, weekRange, 0)), Digits()) + ', ' + DoubleToString(iHigh(Symbol(), PERIOD_W1, iHighest(Symbol(), PERIOD_W1, MODE_HIGH, weekRange, 0)), Digits()) + '] Spr(' + IntegerToString(SymbolInfoInteger(Symbol(), SYMBOL_SPREAD)) + ('...' if (SymbolInfoInteger(Symbol(), SYMBOL_SPREAD) < 10) else '..' if (SymbolInfoInteger(Symbol(), SYMBOL_SPREAD) < 100) else '.' if (SymbolInfoInteger(Symbol(), SYMBOL_SPREAD) < 1000) else '') + ') ' + ('Mkt Closed' if ((SymbolInfoInteger(Symbol(), SYMBOL_TIME) < (TimeCurrent() - oStatsShowMktClosedTimer) and oStatsShowMktClosed) and TerminalInfoInteger(TERMINAL_CONNECTED)) else 'Disconnected' if (oStatsShowMktClosed and (not TerminalInfoInteger(TERMINAL_CONNECTED))) else (('0' if (m < 10) else '') + IntegerToString((0 if (m < 0) else m)) + ':' + ('0' if (s < 10) else '') + IntegerToString((0 if (s < 0) else s)))))
    else:
        Print('ERROR: ' + 'not implemented' + ' at "' + 'statsUpdate' + ':' + IntegerToString(376) + '", last internal error: ' + IntegerToString(GetLastError()) + ' (' + 'Stats on Amplitude, Spread and Clock.mq5' + ')')
        ResetLastError()
        DebugBreak()
    return

def TimeGMTOffset_u(t=0):
    s = ""
    t = t - TimeGMT()
    if t < 0:
        s = '-' + IntegerToString(_long(MathFloor(MathAbs(t) / 3600.0)), 2, _char(48)) + ':' + IntegerToString(_idiv(_imod(MathAbs(t), 3600), 60), 2, _char(48))
    else:
        s = '+' + IntegerToString(_long(MathFloor(t / 3600.0)), 2, _char(48)) + ':' + IntegerToString(_idiv(_imod(MathAbs(t), 3600), 60), 2, _char(48))
    return s

def EnumToInt(e):
    if e == kTimeSeconds:
        return TIME_SECONDS
    elif e == kTimeMinutes:
        return TIME_MINUTES
    elif e == kTimeDateSeconds:
        return TIME_DATE | TIME_SECONDS
    elif e == kTimeDateMinutes:
        return TIME_DATE | TIME_MINUTES
    return -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StatsOnAmplitudeSpreadAndClock(_MQL5Indicator):
    name = 'Stats on Amplitude, Spread and Clock'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'lCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Text Corner
        'lFontSize': 12,  # Font Size
        'oDistX': 0,  # X Distance or Horizontal Position Offset
        'oDistY': 0,  # Y Distance or Vertical Position Offset
        'oSpacingY': 3,  # Vertical gap between objects
        'oStatsShow': True,  # Show Statistics line?
        'weekRange': 52,  # How many weeks should the range contain? Normally 52 weeks
        'sFormat': _Choice({0: 'Format Ampl(xA/xB)/(yA/yB) Spr(z) mm:ss - Amplitude/Spread', 1: 'Format Chg(dA/dB) W([m,M]) Spr(z) mm:ss - Chg/WeekRange/Spread'}, default=1),  # Amplitude and Spread Stats Format
        'oStatsShowMktClosed': True,  # If there is no new ticks for 5m, show "Closed"/"Disconnected"?
        'dFormat': _Choice({0: 'Format hh:mm:ss', 1: 'Format hh:mm', 2: 'Format YYYY.MM.DD hh:mm:ss', 3: 'Format YYYY.MM.DD hh:mm'}, default=2),  # Date Format
        'dShowOffset': True,  # Show UTC Timezone Offset?
        'dShowSameLine': True,  # Show both dates on the same line?
        'dUseServer': True,  # Use Server Date instead of Local/UTC Date?
        'dServerOffset': 0,  # Offset in seconds
        'oCSLatencyAppend': False,  # DEBUG: append latency of the last 20 calls to Server Label
        'oCSLatencyHP': False,  # DEBUG: use 1ms OnTimer() instead of power-saving 1000ms
        'dShowLocal': True,  # Show Local Time Label?
        'dShowLocalAsUTC': False,  # Use UTC+0 / GMT Time instead of Local Timezone?
        'dLocalOffset': 0,  # Offset in seconds
    }

