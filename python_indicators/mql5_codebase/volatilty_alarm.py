"""Volatilty Alarm — converted from MQL5: MQL5 Indicators/Pips Volatility Alarm/Volatilty Alarm.mq5

Copyright: Copyright © 2022; Link: drdz9876@gmail.com; Version: 1.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022', 'link': 'drdz9876@gmail.com', 'version': '1.1', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Volatilty Alarm', 'source': 'MQL5 Indicators/Pips Volatility Alarm/Volatilty Alarm.mq5', 'folder': 'Pips Volatility Alarm', 'inputs': [{'mql': 'CandleTF', 'py': 'CandleTF', 'param': 'CandleTF', 'type': 'int', 'default': 1, 'label': 'Candle Timeframe', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 0, 'label': 'Mode', 'sinput': False}, {'mql': 'PipAlarm', 'py': 'PipAlarm', 'param': 'PipAlarm', 'type': 'double', 'default': 5.0, 'label': 'Pips to Alarm', 'sinput': False}, {'mql': 'CandleColor', 'py': 'CandleColor', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Text Color', 'sinput': False}, {'mql': 'CandleAlarm', 'py': 'CandleAlarm', 'param': None, 'type': 'color', 'default': 65535, 'label': 'Text Color when Alarm', 'sinput': False}, {'mql': 'EnableAlert', 'py': 'EnableAlert', 'param': 'EnableAlert', 'type': 'bool', 'default': False, 'label': 'Enable Alert', 'sinput': False}, {'mql': 'EnableNotif', 'py': 'EnableNotif', 'param': 'EnableNotif', 'type': 'bool', 'default': False, 'label': 'Enable Notification', 'sinput': False}, {'mql': 'EnableSound', 'py': 'EnableSound', 'param': 'EnableSound', 'type': 'bool', 'default': False, 'label': 'Enable Sound', 'sinput': False}, {'mql': 'SoundsFile', 'py': 'SoundsFile', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Sounds File', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum CandleMode
HiLo = 0
Body = 1
_enum('CandleMode', {0: 'HiLo', 1: 'Body'})

# ---- inputs and global variables
CandleTF = _input('CandleTF', PERIOD_M1)  # Candle Timeframe
Mode = _input('Mode', HiLo)  # Mode
PipAlarm = _input('PipAlarm', 5.0)  # Pips to Alarm
CandleColor = _input('CandleColor', clrGreen)  # Text Color
CandleAlarm = _input('CandleAlarm', clrYellow)  # Text Color when Alarm
EnableAlert = _input('EnableAlert', False)  # Enable Alert
EnableNotif = _input('EnableNotif', False)  # Enable Notification
EnableSound = _input('EnableSound', False)  # Enable Sound
SoundsFile = _input('SoundsFile', 'alert.wav')  # Sounds File
chartID = 0
DigitMultiplier = 0.0
Range = Arr(0, 0.0)
HIGH = Arr(0, 0.0)
LOW = Arr(0, 0.0)
CLOSE = Arr(0, 0.0)
OPEN = Arr(0, 0.0)

def OnInit():
    global DigitMultiplier
    SetIndexBuffer(0, Range)
    SetIndexBuffer(1, HIGH)
    SetIndexBuffer(2, LOW)
    SetIndexBuffer(3, CLOSE)
    SetIndexBuffer(4, OPEN)
    if Digits() == 3 or Digits() == 5:
        DigitMultiplier = 0.1
    else:
        DigitMultiplier = 1.0
    createObject('vol', ' ', 15, 20, 16, CandleColor)
    createObject('spreadS', ' ', 15, 50, 16, clrRed)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility Scalper')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(chartID, 'vol')
    ObjectDelete(chartID, 'spreadS')
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(Range, True)
    ArrayInitialize(Range, 0.0)
    ArraySetAsSeries(HIGH, True)
    ArraySetAsSeries(LOW, True)
    ArraySetAsSeries(CLOSE, True)
    ArraySetAsSeries(OPEN, True)
    if CopyHigh(Symbol(), CandleTF, 0, Bars(Symbol(), CandleTF), HIGH) < 0:
        return 0
    if CopyLow(Symbol(), CandleTF, 0, Bars(Symbol(), CandleTF), LOW) < 0:
        return 0
    if CopyClose(Symbol(), CandleTF, 0, Bars(Symbol(), CandleTF), CLOSE) < 0:
        return 0
    if CopyOpen(Symbol(), CandleTF, 0, Bars(Symbol(), CandleTF), OPEN) < 0:
        return 0
    i = 0
    limit = 0
    limit = rates_total - prev_calculated
    if prev_calculated > 0:
        limit += 1
    i = 0
    for i in range(i, limit):
        if Mode == HiLo:
            Range[i] = _fdiv(MathAbs(HIGH[i] - LOW[i]), Point()) * DigitMultiplier
        elif Mode == Body:
            Range[i] = _fdiv(MathAbs(CLOSE[i] - OPEN[i]), Point()) * DigitMultiplier
    else:
        i = _range_end(i, limit, 1)
    if Range[0] >= PipAlarm:
        doAlert('Volatility is : ' + DoubleToString(Range[0], 1))
        ObjectSetInteger(chartID, 'vol', OBJPROP_COLOR, CandleAlarm)
    ObjectSetString(chartID, 'vol', OBJPROP_TEXT, 'Volatility: ' + DoubleToString(Range[0], 1))
    ObjectSetString(chartID, 'spreadS', OBJPROP_TEXT, 'Spread: ' + IntegerToString(SymbolInfoInteger(Symbol(), SYMBOL_SPREAD)))
    ResetLastError()
    ChartRedraw(chartID)
    return rates_total

def doAlert(doWhat):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    message = ""
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != iTime(None, 0, 0):
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = iTime(None, 0, 0)
        message = doWhat
        if EnableAlert:
            Alert(message)
        if EnableNotif:
            SendNotification(message)
        if EnableSound:
            PlaySound(SoundsFile)

def createObject(name, text, x, y, size, clr):
    ObjectCreate(chartID, name, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(chartID, name, OBJPROP_CORNER, CORNER_LEFT_UPPER)
    ObjectSetInteger(chartID, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(chartID, name, OBJPROP_YDISTANCE, y)
    ObjectSetString(chartID, name, OBJPROP_TEXT, text)
    ObjectSetString(chartID, name, OBJPROP_FONT, 'Arial')
    ObjectSetInteger(chartID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chartID, name, OBJPROP_FONTSIZE, 16)
    return True

# ---- static local variables
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatiltyAlarm(_MQL5Indicator):
    name = 'Volatilty Alarm'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CandleTF': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=1),  # Candle Timeframe
        'Mode': _Choice({0: 'High to Low', 1: 'Body'}, default=0),  # Mode
        'PipAlarm': 5.0,  # Pips to Alarm
        'EnableAlert': False,  # Enable Alert
        'EnableNotif': False,  # Enable Notification
        'EnableSound': False,  # Enable Sound
    }

