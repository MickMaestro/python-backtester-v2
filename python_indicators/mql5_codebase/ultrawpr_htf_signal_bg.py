"""ultrawpr_htf_signal_bg — converted from MQL5: MQL5 Indicators/UltraWPR_HTF_Signal_BG/ultrawpr_htf_signal_bg.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ultrawpr_htf_signal_bg', 'source': 'MQL5 Indicators/UltraWPR_HTF_Signal_BG/ultrawpr_htf_signal_bg.mq5', 'folder': 'UltraWPR_HTF_Signal_BG', 'inputs': [{'mql': 'SessionDrawOff', 'py': 'SessionDrawOff', 'param': 'SessionDrawOff', 'type': 'bool', 'default': False, 'label': 'Show session in a non-session period', 'sinput': False}, {'mql': 'SessionSirName', 'py': 'SessionSirName', 'param': None, 'type': 'string', 'default': 'Asian', 'label': 'Session name', 'sinput': False}, {'mql': 'StartHour', 'py': 'StartHour', 'param': 'StartHour', 'type': 'int', 'default': 0, 'label': 'Session start hour', 'sinput': False}, {'mql': 'StartMinute', 'py': 'StartMinute', 'param': 'StartMinute', 'type': 'int', 'default': 0, 'label': 'Session start minute', 'sinput': False}, {'mql': 'SessionTime', 'py': 'SessionTime', 'param': 'SessionTime', 'type': 'uint', 'default': 480, 'label': 'Session duration in minutes', 'sinput': False}, {'mql': 'Up_Color', 'py': 'Up_Color', 'param': None, 'type': 'color', 'default': 15453831, 'label': 'Color of growth', 'sinput': False}, {'mql': 'Buy_Color', 'py': 'Buy_Color', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'Color of Buy', 'sinput': False}, {'mql': 'Sell_Color', 'py': 'Sell_Color', 'param': None, 'type': 'color', 'default': 14524637, 'label': 'Color of fall', 'sinput': False}, {'mql': 'Dn_Color', 'py': 'Dn_Color', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Color of Sell', 'sinput': False}, {'mql': 'Symbol_', 'py': 'Symbol_', 'param': None, 'type': 'string', 'default': '', 'label': 'Financial asset', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16390, 'label': 'Indicator timeframe for the indicator calculation', 'sinput': False}, {'mql': 'WPR_Period', 'py': 'WPR_Period', 'param': 'WPR_Period', 'type': 'int', 'default': 13, 'label': 'WPR indicator period', 'sinput': False}, {'mql': 'W_Method', 'py': 'W_Method', 'param': 'W_Method', 'type': 'int', 'default': 4, 'label': 'Method of averaging', 'sinput': False}, {'mql': 'StartLength', 'py': 'StartLength', 'param': 'StartLength', 'type': 'int', 'default': 3, 'label': 'Initial averaging period', 'sinput': False}, {'mql': 'WPhase', 'py': 'WPhase', 'param': 'WPhase', 'type': 'int', 'default': 100, 'label': 'Averaging parameter (-100..+100)', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'uint', 'default': 5, 'label': 'Period change step', 'sinput': False}, {'mql': 'StepsTotal', 'py': 'StepsTotal', 'param': 'StepsTotal', 'type': 'uint', 'default': 10, 'label': 'Number of period changes', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 4, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'SmoothLength', 'py': 'SmoothLength', 'param': 'SmoothLength', 'type': 'int', 'default': 3, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'SmoothPhase', 'py': 'SmoothPhase', 'param': 'SmoothPhase', 'type': 'int', 'default': 100, 'label': 'Soothing parameter (-100..+100)', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 0, 'label': 'Signal bar index, 0 is a current bar', 'sinput': False}, {'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'UltraWPR_Label_', 'label': 'Indicator labels name', 'sinput': False}, {'mql': 'IndName_Color', 'py': 'IndName_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Indicator name color', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'uint', 'default': 10, 'label': 'Indicator name font size', 'sinput': False}, {'mql': 'X_1', 'py': 'X_1', 'param': 'X_1', 'type': 'int', 'default': 5, 'label': 'Horizontal shift of the name', 'sinput': False}, {'mql': 'Y_1', 'py': 'Y_1', 'param': 'Y_1', 'type': 'int', 'default': -15, 'label': 'Vertical shift of the name', 'sinput': False}, {'mql': 'ShowIndName', 'py': 'ShowIndName', 'param': 'ShowIndName', 'type': 'bool', 'default': True, 'label': 'Indicator name display', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 3, 'label': 'Location corner', 'sinput': False}, {'mql': 'alert_mode', 'py': 'alert_mode', 'param': 'alert_mode', 'type': 'int', 'default': 0, 'label': 'Triggering indication option', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'Number of produced alerts', 'sinput': False}, {'mql': 'Push', 'py': 'Push', 'param': 'Push', 'type': 'bool', 'default': True, 'label': 'Allow push notifications', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

DarkOrchid = 0xCC3299  # MQL4 colour name

# enum Hour
H00 = 0
H01 = 1
H02 = 2
H03 = 3
H04 = 4
H05 = 5
H06 = 6
H07 = 7
H08 = 8
H09 = 9
H10 = 10
H11 = 11
H12 = 12
H13 = 13
H14 = 14
H15 = 15
H16 = 16
H17 = 17
H18 = 18
H19 = 19
H20 = 20
H21 = 21
H22 = 22
H23 = 23
_enum('Hour', {0: 'H00', 1: 'H01', 2: 'H02', 3: 'H03', 4: 'H04', 5: 'H05', 6: 'H06', 7: 'H07', 8: 'H08', 9: 'H09', 10: 'H10', 11: 'H11', 12: 'H12', 13: 'H13', 14: 'H14', 15: 'H15', 16: 'H16', 17: 'H17', 18: 'H18', 19: 'H19', 20: 'H20', 21: 'H21', 22: 'H22', 23: 'H23'})

# enum Min
M00 = 0
M01 = 1
M02 = 2
M03 = 3
M04 = 4
M05 = 5
M06 = 6
M07 = 7
M08 = 8
M09 = 9
M10 = 10
M11 = 11
M12 = 12
M13 = 13
M14 = 14
M15 = 15
M16 = 16
M17 = 17
M18 = 18
M19 = 19
M20 = 20
M21 = 21
M22 = 22
M23 = 23
M24 = 24
M25 = 25
M26 = 26
M27 = 27
M28 = 28
M29 = 29
M30 = 30
M31 = 31
M32 = 32
M33 = 33
M34 = 34
M35 = 35
M36 = 36
M37 = 37
M38 = 38
M39 = 39
M40 = 40
M41 = 41
M42 = 42
M43 = 43
M44 = 44
M45 = 45
M46 = 46
M47 = 47
M48 = 48
M49 = 49
M50 = 50
M51 = 51
M52 = 52
M53 = 53
M54 = 54
M55 = 55
M56 = 56
M57 = 57
M58 = 58
M59 = 59
_enum('Min', {0: 'M00', 1: 'M01', 2: 'M02', 3: 'M03', 4: 'M04', 5: 'M05', 6: 'M06', 7: 'M07', 8: 'M08', 9: 'M09', 10: 'M10', 11: 'M11', 12: 'M12', 13: 'M13', 14: 'M14', 15: 'M15', 16: 'M16', 17: 'M17', 18: 'M18', 19: 'M19', 20: 'M20', 21: 'M21', 22: 'M22', 23: 'M23', 24: 'M24', 25: 'M25', 26: 'M26', 27: 'M27', 28: 'M28', 29: 'M29', 30: 'M30', 31: 'M31', 32: 'M32', 33: 'M33', 34: 'M34', 35: 'M35', 36: 'M36', 37: 'M37', 38: 'M38', 39: 'M39', 40: 'M40', 41: 'M41', 42: 'M42', 43: 'M43', 44: 'M44', 45: 'M45', 46: 'M46', 47: 'M47', 48: 'M48', 49: 'M49', 50: 'M50', 51: 'M51', 52: 'M52', 53: 'M53', 54: 'M54', 55: 'M55', 56: 'M56', 57: 'M57', 58: 'M58', 59: 'M59'})

# enum ENUM_ALERT_MODE
OnlySound = 0
OnlyAlert = 1
_enum('ENUM_ALERT_MODE', {0: 'OnlySound', 1: 'OnlyAlert'})

# ---- inputs and global variables
SessionDrawOff = _input('SessionDrawOff', False)  # Show session in a non-session period
SessionSirName = _input('SessionSirName', 'Asian')  # Session name
StartHour = _input('StartHour', H00)  # Session start hour
StartMinute = _input('StartMinute', M00)  # Session start minute
SessionTime = _input('SessionTime', 480)  # Session duration in minutes
Up_Color = _input('Up_Color', clrSkyBlue)  # Color of growth
Buy_Color = _input('Buy_Color', clrDodgerBlue)  # Color of Buy
Sell_Color = _input('Sell_Color', clrPlum)  # Color of fall
Dn_Color = _input('Dn_Color', clrMagenta)  # Color of Sell
Symbol_ = _input('Symbol_', '')  # Financial asset
Timeframe = _input('Timeframe', PERIOD_H6)  # Indicator timeframe for the indicator calculation
WPR_Period = _input('WPR_Period', 13)  # WPR indicator period
W_Method = _input('W_Method', MODE_JJMA)  # Method of averaging
StartLength = _input('StartLength', 3)  # Initial averaging period
WPhase = _input('WPhase', 100)  # Averaging parameter (-100..+100)
Step = _input('Step', 5)  # Period change step
StepsTotal = _input('StepsTotal', 10)  # Number of period changes
SmoothMethod = _input('SmoothMethod', MODE_JJMA)  # Smoothing method
SmoothLength = _input('SmoothLength', 3)  # Smoothing depth
SmoothPhase = _input('SmoothPhase', 100)  # Soothing parameter (-100..+100)
SignalBar = _input('SignalBar', 0)  # Signal bar index, 0 is a current bar
Symbols_Sirname = _input('Symbols_Sirname', 'UltraWPR_Label_')  # Indicator labels name
Font_Size = _input('Font_Size', 10)  # Indicator name font size
X_1 = _input('X_1', 5)  # Horizontal shift of the name
Y_1 = _input('Y_1', -15)  # Vertical shift of the name
ShowIndName = _input('ShowIndName', True)  # Indicator name display
WhatCorner = _input('WhatCorner', CORNER_RIGHT_UPPER)  # Location corner
alert_mode = _input('alert_mode', OnlySound)  # Triggering indication option
AlertCount = _input('AlertCount', 0)  # Number of produced alerts
Push = _input('Push', True)  # Allow push notifications
UltraWPR_Handle = 0
min_rates_total = 0
X_1_ = 0
Y_1_ = 0
name1 = ""
IndName = ""
Symb = ""
BuySignal = ""
SellSignal = ""
ObjName = ""
StartHourSec = 0
StartMinuteSec = 0
SessionTimeSec = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def CreateChannel(chart_id, name, nwin, time1, price1, time2, price2, time3, price3, Color, background, text):
    ObjectCreate(chart_id, name, OBJ_CHANNEL, nwin, time1, price1, time2, price2, time3, price3)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_FILL, True)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, background)
    ObjectSetString(chart_id, name, OBJPROP_TOOLTIP, '\n')
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_LEFT, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)

def SetChannel(chart_id, name, nwin, time1, price1, time2, price2, time3, price3, Color, background, text):
    if ObjectFind(chart_id, name) == -1:
        CreateChannel(chart_id, name, nwin, time1, price1, time2, price2, time3, price3, Color, background, text)
    else:
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectMove(chart_id, name, 2, time3, price3)

def CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, textTT, Color, Font, Size):
    ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(chart_id, name, OBJPROP_CORNER, corner)
    ObjectSetInteger(chart_id, name, OBJPROP_ANCHOR, point)
    ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
    ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)
    ObjectSetString(chart_id, name, OBJPROP_TOOLTIP, textTT)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetTLabel(chart_id, name, nwin, corner, point, X, Y, text, textTT, Color, Font, Size):
    if ObjectFind(chart_id, name) == -1:
        CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, textTT, Color, Font, Size)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
        ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
        ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)
        ObjectSetString(chart_id, name, OBJPROP_FONT, Font)

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

def OnInit():
    global BuySignal, ObjName, SellSignal, SessionTimeSec, StartHourSec, StartMinuteSec, Symb, UltraWPR_Handle, X_1_, Y_1_, min_rates_total, name1
    min_rates_total = WPR_Period
    min_rates_total += GetStartBars(W_Method, StartLength + (Step * StepsTotal), WPhase) + 1
    min_rates_total += GetStartBars(SmoothMethod, SmoothLength, SmoothPhase)
    min_rates_total += _int(SignalBar) + 1 + 3
    ObjName = SessionSirName + ' Session'
    StartHourSec = StartHour * 60 * 60
    StartMinuteSec = StartMinute * 60
    SessionTimeSec = _int(SessionTime) * 60
    if Symbol_ != '':
        Symb = Symbol_
    else:
        Symb = Symbol()
    X_0 = 5
    Yn = 30
    if ShowIndName:
        Y_1_ = Yn + Y_1
        X_1_ = X_0 + X_1
        name1 = Symbols_Sirname + '1'
        StringConcatenate(_GlobRef(globals(), 'IndName'), 'UltraWPR', '(', Symb, ' ', GetStringTimeframe(Timeframe), ')')
    UltraWPR_Handle = iCustom(Symb, Timeframe, 'UltraWPR', WPR_Period, W_Method, StartLength, WPhase, Step, StepsTotal, SmoothMethod, SmoothLength, SmoothPhase, 0, 0, clrRed, clrRed, 0, 0)
    if UltraWPR_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the UltraWPR indicator')
        return INIT_FAILED
    BuySignal = IndName + ': ' + 'Buy signal'
    SellSignal = IndName + ': ' + 'Sell signal'
    shortname = name1
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def Deinit():
    if ObjectFind(0, ObjName) != -1:
        ObjectDelete(0, ObjName)

def OnDeinit(reason):
    Deinit()
    if ObjectFind(0, name1) != -1:
        ObjectDelete(0, name1)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_RePush, _s_OnCalculate_buycount, _s_OnCalculate_sellcount
    if BarsCalculated(UltraWPR_Handle) < min_rates_total:
        return 0
    if BarsCalculated(UltraWPR_Handle) < Bars(Symbol(), Timeframe):
        return prev_calculated
    iTime_ = Arr(1, 0, dyn=False)
    if CopyTime(Symbol(), PERIOD_D1, _DT(time[rates_total - 1]), 1, iTime_) <= 0:
        return 0
    StartTime = iTime_[0] + StartHourSec + StartMinuteSec
    EndTime = StartTime + SessionTimeSec
    if StartTime > TimeCurrent() or ((not SessionDrawOff) and TimeCurrent() > EndTime):
        Deinit()
        return 0
    ArraySetAsSeries(close, True)
    StartBar = iBarShift_u("", PERIOD_CURRENT, StartTime)
    EndBar = MathMax(iBarShift_u("", PERIOD_CURRENT, EndTime), 0)
    trend = 0
    UpMov = Arr(2, 0.0, dyn=False)
    DnMov = Arr(2, 0.0, dyn=False)
    Color0 = clrNONE
    signal = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        _s_OnCalculate_buycount = 0
        _s_OnCalculate_sellcount = 0
    else:
        if (prev_calculated == rates_total and SignalBar) and ((not _s_OnCalculate_buycount) or (not _s_OnCalculate_sellcount)):
            return rates_total
    if CopyBuffer(UltraWPR_Handle, 0, SignalBar, 2, UpMov) <= 0:
        return prev_calculated
    if CopyBuffer(UltraWPR_Handle, 1, SignalBar, 2, DnMov) <= 0:
        return prev_calculated
    if UpMov[1] > DnMov[1]:
        trend = 1
        if UpMov[0] <= DnMov[0]:
            signal = True
    if UpMov[1] < DnMov[1]:
        trend = -1
        if UpMov[0] >= DnMov[0]:
            signal = True
    if (prev_calculated != rates_total and AlertCount) and signal:
        _s_OnCalculate_buycount = AlertCount
        _s_OnCalculate_sellcount = AlertCount
    if trend > 0:
        if signal:
            Color0 = Buy_Color
            if (Push and SignalBar) and prev_calculated != rates_total:
                _s_OnCalculate_RePush = True
            if _s_OnCalculate_RePush:
                if SendNotification(BuySignal):
                    _s_OnCalculate_RePush = False
            if _s_OnCalculate_buycount and SignalBar:
                _sw1 = alert_mode
                if _sw1 == OnlyAlert:
                    Alert(BuySignal)
                elif _sw1 == OnlySound:
                    PlaySound('alert.wav')
                _s_OnCalculate_buycount -= 1
        else:
            Color0 = Up_Color
    if trend < 0:
        if signal:
            Color0 = Sell_Color
            if (Push and SignalBar) and prev_calculated != rates_total:
                _s_OnCalculate_RePush = True
            if _s_OnCalculate_RePush:
                if SendNotification(SellSignal):
                    _s_OnCalculate_RePush = False
            if _s_OnCalculate_sellcount and SignalBar:
                _sw2 = alert_mode
                if _sw2 == OnlyAlert:
                    Alert(SellSignal)
                elif _sw2 == OnlySound:
                    PlaySound('alert.wav')
                _s_OnCalculate_sellcount -= 1
        else:
            Color0 = Dn_Color
    SetChannel(0, ObjName, 0, StartTime, close[StartBar], StartTime, 0.0, EndTime, 0.0, Color0, True, ObjName)
    if ShowIndName:
        SetTLabel(0, name1, 0, WhatCorner, 2 * WhatCorner, X_1_, Y_1_, IndName, IndName, IndName_Color, 'Georgia', Font_Size)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
IndName_Color = _input('IndName_Color', _uint(DarkOrchid))  # Indicator name color

# ---- static local variables
_s_OnCalculate_buycount = 0
_s_OnCalculate_sellcount = 0
_s_OnCalculate_RePush = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UltrawprHtfSignalBg(_MQL5Indicator):
    name = 'ultrawpr_htf_signal_bg'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SessionDrawOff': False,  # Show session in a non-session period
        'StartHour': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=0),  # Session start hour
        'StartMinute': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=0),  # Session start minute
        'SessionTime': 480,  # Session duration in minutes
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Indicator timeframe for the indicator calculation
        'WPR_Period': 13,  # WPR indicator period
        'W_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Method of averaging
        'StartLength': 3,  # Initial averaging period
        'WPhase': 100,  # Averaging parameter (-100..+100)
        'Step': 5,  # Period change step
        'StepsTotal': 10,  # Number of period changes
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Smoothing method
        'SmoothLength': 3,  # Smoothing depth
        'SmoothPhase': 100,  # Soothing parameter (-100..+100)
        'SignalBar': 0,  # Signal bar index, 0 is a current bar
        'Font_Size': 10,  # Indicator name font size
        'X_1': 5,  # Horizontal shift of the name
        'Y_1': -15,  # Vertical shift of the name
        'ShowIndName': True,  # Indicator name display
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Location corner
        'alert_mode': _Choice({0: 'only sound', 1: 'only alert'}, default=0),  # Triggering indication option
        'AlertCount': 0,  # Number of produced alerts
        'Push': True,  # Allow push notifications
    }

