"""TimeToClose-v1.01 — converted from MQL5: MQL5 Indicators/Time To Close v1.01 - MT5/TimeToClose-v1.01.mq5

Time to Current Candle Close
Copyright: Copyright 2025, Tautvydas Vaitkus; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, Tautvydas Vaitkus', 'version': '1.01', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Time to Current Candle Close'], 'name': 'TimeToClose-v1.01', 'source': 'MQL5 Indicators/Time To Close v1.01 - MT5/TimeToClose-v1.01.mq5', 'folder': 'Time To Close v1.01 - MT5', 'inputs': [{'mql': 'EnableTextInVisualBacktest', 'py': 'EnableTextInVisualBacktest', 'param': 'EnableTextInVisualBacktest', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'ColorText', 'py': 'ColorText', 'param': 'ColorText', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'ShowTimeDate', 'py': 'ShowTimeDate', 'param': 'ShowTimeDate', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'Font', 'py': 'Font', 'param': None, 'type': 'string', 'default': 'Arial Bold', 'label': 'Font (Arial, Arial Bold, ..)', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'TextAnchorPoint', 'py': 'TextAnchorPoint', 'param': 'TextAnchorPoint', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'TextFirstSeperator', 'py': 'TextFirstSeperator', 'param': None, 'type': 'string', 'default': '    ¬ ', 'label': 'Text Seperator Price+Time', 'sinput': False}, {'mql': 'TestSecondSeperator', 'py': 'TestSecondSeperator', 'param': None, 'type': 'string', 'default': '        ', 'label': 'Text Seperator Time+TimeDate', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_COLOR_TEXT
COLOR_CHART = 0
COLOR_CHART_CANDLE = 1
_enum('ENUM_COLOR_TEXT', {0: 'COLOR_CHART', 1: 'COLOR_CHART_CANDLE'})

# ---- inputs and global variables
objName = 'TimeToNextCandle'
isVisualMode = False
EnableTextInVisualBacktest = _input('EnableTextInVisualBacktest', False)
ColorText = _input('ColorText', COLOR_CHART)
ShowTimeDate = _input('ShowTimeDate', False)
Font = _input('Font', 'Arial Bold')  # Font (Arial, Arial Bold, ..)
FontSize = _input('FontSize', 12)
TextAnchorPoint = _input('TextAnchorPoint', ANCHOR_LEFT_UPPER)
TextFirstSeperator = _input('TextFirstSeperator', '    ¬ ')  # Text Seperator Price+Time
TestSecondSeperator = _input('TestSecondSeperator', '        ')  # Text Seperator Time+TimeDate

def OnInit():
    global isVisualMode
    isVisualMode = IsVisualMode()
    if isVisualMode:
        if not EventSetMillisecondTimer(1000):
            Print('Failed to set timer: ', GetLastError())
            return INIT_FAILED
    else:
        Print('TimeToClose-v1.01.mq5', ': Running in non-visual mode')
    return INIT_SUCCEEDED

def OnTimer():
    UpdateTimeToNextCandle()

def OnDeinit(reason):
    if (reason == REASON_REMOVE or reason == REASON_PROGRAM) or reason == REASON_PARAMETERS:
        ObjectDelete(0, objName)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_lastClose
    if not isVisualMode:
        return rates_total
    thisClose = close[rates_total - 1]
    if _s_OnCalculate_lastClose is _UNSET:
        _s_OnCalculate_lastClose = close[rates_total - 1]
    if _s_OnCalculate_lastClose != thisClose or rates_total != prev_calculated:
        CreateModifyTimeToNextCandlePos(open[rates_total - 1], thisClose)
    return rates_total

def CreateModifyTimeToNextCandlePos(open, close):
    if ObjectFind(0, objName) < 0:
        ObjectCreate(0, objName, OBJ_TEXT, 0, TimeCurrent(), close)
        ObjectSetInteger(0, objName, OBJPROP_FONTSIZE, FontSize)
        ObjectSetString(0, objName, OBJPROP_FONT, Font)
        ObjectSetInteger(0, objName, OBJPROP_ANCHOR, TextAnchorPoint)
        ObjectSetString(0, objName, OBJPROP_TEXT, 'loading..')
    ObjectMove(0, objName, 0, TimeCurrent(), close)
    if open < close:
        ObjectSetInteger(0, objName, OBJPROP_COLOR, ChartGetInteger(0, (CHART_COLOR_CHART_UP if (ColorText == COLOR_CHART) else CHART_COLOR_CANDLE_BULL)))
    elif open > close:
        ObjectSetInteger(0, objName, OBJPROP_COLOR, ChartGetInteger(0, (CHART_COLOR_CHART_DOWN if (ColorText == COLOR_CHART) else CHART_COLOR_CANDLE_BEAR)))
    else:
        ObjectSetInteger(0, objName, OBJPROP_COLOR, ChartGetInteger(0, CHART_COLOR_CHART_LINE))
    UpdateTimeToNextCandle()

def UpdateTimeToNextCandle():
    currentTime = TimeCurrent()
    currentBarTime = iTime(Symbol(), Period(), 0)
    secondsLeft = _int(PeriodSeconds(Period()) - (currentTime - currentBarTime))
    showDays = Period() == PERIOD_W1 or Period() == PERIOD_MN1
    showHours = Period() >= PERIOD_H4 or Period() == PERIOD_D1
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    remaining = secondsLeft
    if showDays:
        days = _idiv(remaining, 86400)
        remaining = _imod(remaining, 86400)
    if showHours:
        hours = _idiv(remaining, 3600)
        remaining = _imod(remaining, 3600)
    minutes = _idiv(remaining, 60)
    seconds = _imod(remaining, 60)
    txtTimeDate = ''
    if ShowTimeDate:
        txtTimeDate = TestSecondSeperator + '[' + TimeToString(TimeCurrent()) + ']'
    txt = TextFirstSeperator
    if showDays:
        txt += StringFormat('%dd ', days)
    if showHours:
        txt += StringFormat('%02d:', hours)
    txt += StringFormat('%02d:%02d', minutes, seconds)
    ObjectSetString(0, objName, OBJPROP_TEXT, txt + txtTimeDate)
    ChartRedraw(0)

def IsVisualMode():
    if not MQLInfoInteger(MQL_TESTER):
        return True
    return _bool(MQLInfoInteger(MQL_VISUAL_MODE)) and EnableTextInVisualBacktest

# ---- static local variables
_s_OnCalculate_lastClose = _UNSET


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TimeToCloseV101(_MQL5Indicator):
    name = 'TimeToClose-v1.01'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'EnableTextInVisualBacktest': False,
        'ColorText': _Choice({0: 'Candle Border', 1: 'Candle Body'}, default=0),
        'ShowTimeDate': False,
        'FontSize': 12,
        'TextAnchorPoint': _Choice({0: 'ANCHOR_LEFT_UPPER', 1: 'ANCHOR_LEFT', 2: 'ANCHOR_LEFT_LOWER', 3: 'ANCHOR_LOWER', 4: 'ANCHOR_RIGHT_LOWER', 5: 'ANCHOR_RIGHT', 6: 'ANCHOR_RIGHT_UPPER', 7: 'ANCHOR_UPPER', 8: 'ANCHOR_CENTER'}, default=0),
    }

