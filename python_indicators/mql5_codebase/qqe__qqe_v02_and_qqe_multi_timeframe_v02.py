"""qqe — converted from MQL5: MQL5 Indicators/QQE [v02] and QQE multi-timeframe [v02]/qqe.mq5

QQE - Qualitative Quantitative Estimation.
Calculated as two indicators:
1) MA on RSI
2) Difference of MA on RSI and MA of MA of ATR of MA of RSI
The signal for buy is when blue line crosses level 50 from below
after crossing the yellow line from below.
The signal for sell is when blue line crosses level 50 from above
after crossing the yellow line from above.
Copyright: 2010, traderak20@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2010, traderak20@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [65535]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 2}, 'labels': {}, 'levels': [50.0], 'description': ['QQE - Qualitative Quantitative Estimation.', 'Calculated as two indicators:', '1) MA on RSI', '2) Difference of MA on RSI and MA of MA of ATR of MA of RSI', 'The signal for buy is when blue line crosses level 50 from below', 'after crossing the yellow line from below.', 'The signal for sell is when blue line crosses level 50 from above', 'after crossing the yellow line from above.'], 'name': 'qqe', 'source': 'MQL5 Indicators/QQE [v02] and QQE multi-timeframe [v02]/qqe.mq5', 'folder': 'QQE [v02] and QQE multi-timeframe [v02]', 'inputs': [{'mql': 'InpSF', 'py': 'InpSF', 'param': 'InpSF', 'type': 'int', 'default': 5, 'label': 'Smoothing Factor', 'sinput': False}, {'mql': 'InpAlertLevel', 'py': 'InpAlertLevel', 'param': 'InpAlertLevel', 'type': 'int', 'default': 50, 'label': 'Alert level', 'sinput': False}, {'mql': 'InpMsgAlerts', 'py': 'InpMsgAlerts', 'param': 'InpMsgAlerts', 'type': 'bool', 'default': False, 'label': 'Use alert message', 'sinput': False}, {'mql': 'InpEmailAlerts', 'py': 'InpEmailAlerts', 'param': 'InpEmailAlerts', 'type': 'bool', 'default': False, 'label': 'Send email alert', 'sinput': False}, {'mql': 'InpSoundAlerts', 'py': 'InpSoundAlerts', 'param': 'InpSoundAlerts', 'type': 'bool', 'default': False, 'label': 'Play sound alert', 'sinput': False}, {'mql': 'InpSoundAlertFile', 'py': 'InpSoundAlertFile', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Sound alert', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpSF = _input('InpSF', 5)  # Smoothing Factor
InpAlertLevel = _input('InpAlertLevel', 50)  # Alert level
InpMsgAlerts = _input('InpMsgAlerts', False)  # Use alert message
InpEmailAlerts = _input('InpEmailAlerts', False)  # Send email alert
InpSoundAlerts = _input('InpSoundAlerts', False)  # Play sound alert
InpSoundAlertFile = _input('InpSoundAlertFile', 'alert.wav')  # Sound alert
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
ExtRsiMaBuffer = Arr(0, 0.0)  # moving average of RSI
ExtTrLevelSlowBuffer = Arr(0, 0.0)  # true range level
ExtRsiBuffer = Arr(0, 0.0)  # RSI
ExtAtrRsiBuffer = Arr(0, 0.0)  # average true range of RSI
ExtMaAtrRsiBuffer = Arr(0, 0.0)  # moving average of true range of RSI
ExtMaMaAtrRsiBuffer = Arr(0, 0.0)  # moving average of moving average of true range of RSI
RsiHandle = 0
RSI_Period = 14
Wilders_Period = 0
SmoothingFactor = 0
AlertLevel = 0
LastAlertBar = 0
ShowErrorMessages = True  # turn on/off error messages for debugging

def OnInit():
    global AlertLevel, RsiHandle, SmoothingFactor, Wilders_Period
    Wilders_Period = (RSI_Period * 2) - 1
    SmoothingFactor = InpSF
    if SmoothingFactor <= 0:
        SmoothingFactor = 5
    AlertLevel = InpAlertLevel
    if AlertLevel < 0 or AlertLevel > 100:
        AlertLevel = 50
    SetIndexBuffer(0, ExtRsiMaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtTrLevelSlowBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtRsiBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtAtrRsiBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtMaAtrRsiBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtMaMaAtrRsiBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtRsiMaBuffer, True)
    ArraySetAsSeries(ExtTrLevelSlowBuffer, True)
    ArraySetAsSeries(ExtRsiBuffer, True)
    ArraySetAsSeries(ExtAtrRsiBuffer, True)
    ArraySetAsSeries(ExtMaAtrRsiBuffer, True)
    ArraySetAsSeries(ExtMaMaAtrRsiBuffer, True)
    PlotIndexSetString(0, PLOT_LABEL, 'Fast RSI MA')
    PlotIndexSetString(1, PLOT_LABEL, 'Slow RSI MA')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, RSI_Period + SmoothingFactor)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, RSI_Period + SmoothingFactor + 1 + Wilders_Period + Wilders_Period)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    IndicatorSetDouble(INDICATOR_MINIMUM, -5)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 105)
    IndicatorSetString(INDICATOR_SHORTNAME, 'QQE(' + IntegerToString(SmoothingFactor) + ')')
    RsiHandle = iRSI(None, 0, RSI_Period, InpAppliedPrice)
    if RsiHandle == INVALID_HANDLE:
        return -1
    return 0

def TF2Str(period):
    _sw1 = period
    if _sw1 == PERIOD_M1:
        return 'M1'
    elif _sw1 == PERIOD_M2:
        return 'M2'
    elif _sw1 == PERIOD_M3:
        return 'M3'
    elif _sw1 == PERIOD_M4:
        return 'M4'
    elif _sw1 == PERIOD_M5:
        return 'M5'
    elif _sw1 == PERIOD_M6:
        return 'M6'
    elif _sw1 == PERIOD_M10:
        return 'M10'
    elif _sw1 == PERIOD_M12:
        return 'M12'
    elif _sw1 == PERIOD_M15:
        return 'M15'
    elif _sw1 == PERIOD_M20:
        return 'M20'
    elif _sw1 == PERIOD_M30:
        return 'M30'
    elif _sw1 == PERIOD_H1:
        return 'H1'
    elif _sw1 == PERIOD_H2:
        return 'H2'
    elif _sw1 == PERIOD_H3:
        return 'H3'
    elif _sw1 == PERIOD_H4:
        return 'H4'
    elif _sw1 == PERIOD_H6:
        return 'H6'
    elif _sw1 == PERIOD_H8:
        return 'H8'
    elif _sw1 == PERIOD_H12:
        return 'H12'
    elif _sw1 == PERIOD_D1:
        return 'D1'
    elif _sw1 == PERIOD_W1:
        return 'W1'
    elif _sw1 == PERIOD_MN1:
        return 'MN'
    return IntegerToString(Period())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LastAlertBar
    if rates_total <= MathMax(Wilders_Period, SmoothingFactor):
        return 0
    calculated = 0
    calculated = BarsCalculated(RsiHandle)
    if calculated < rates_total:
        if ShowErrorMessages:
            Print('Not all data of RsiHandle has been calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    limit = 0
    if (prev_calculated == 0 or prev_calculated < 0) or prev_calculated > rates_total:
        limit = rates_total - 1 - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if CopyBuffer(RsiHandle, 0, 0, to_copy, ExtRsiBuffer) <= 0:
        if ShowErrorMessages:
            Print('Getting RSI failed! Error', GetLastError())
        return 0
    ExponentialMAOnBuffer(rates_total, prev_calculated, RSI_Period, SmoothingFactor, ExtRsiBuffer, ExtRsiMaBuffer)
    for i in range(limit, 0 - 1, -1):
        ExtAtrRsiBuffer[i] = MathAbs(ExtRsiMaBuffer[i + 1] - ExtRsiMaBuffer[i])
    ExponentialMAOnBuffer(rates_total, prev_calculated, RSI_Period + SmoothingFactor + 1, Wilders_Period, ExtAtrRsiBuffer, ExtMaAtrRsiBuffer)
    ExponentialMAOnBuffer(rates_total, prev_calculated, RSI_Period + SmoothingFactor + 1 + Wilders_Period, Wilders_Period, ExtMaAtrRsiBuffer, ExtMaMaAtrRsiBuffer)
    rsi0 = 0.0
    rsi1 = 0.0
    dar = 0.0
    tr = 0.0
    dv = 0.0
    tr = ExtTrLevelSlowBuffer[limit + 1]
    rsi1 = ExtRsiMaBuffer[limit + 1]
    for i in range(limit + 1, 0 - 1, -1):
        rsi0 = ExtRsiMaBuffer[i]
        dar = ExtMaMaAtrRsiBuffer[i] * 4.236
        dv = tr
        if rsi0 < tr:
            tr = rsi0 + dar
            if rsi1 < dv and tr > dv:
                tr = dv
        elif rsi0 > tr:
            tr = rsi0 - dar
            if rsi1 > dv and tr < dv:
                tr = dv
        ExtTrLevelSlowBuffer[i] = tr
        rsi1 = rsi0
    if ((InpMsgAlerts or InpSoundAlerts) or InpEmailAlerts) and rates_total > LastAlertBar:
        AlertDirection = 0
        if ExtRsiMaBuffer[1] < AlertLevel and ExtRsiMaBuffer[0] >= AlertLevel:
            AlertDirection = 1
        if ExtRsiMaBuffer[1] > AlertLevel and ExtRsiMaBuffer[0] <= AlertLevel:
            AlertDirection = -1
        if AlertDirection == 1 or AlertDirection == -1:
            AlertSubj = Symbol() + ', TF: ' + TF2Str(Period()) + ', ' + IntegerToString(AlertLevel) + ' level Cross '
            if AlertDirection == 1:
                AlertSubj = AlertSubj + 'UP'
            if AlertDirection == -1:
                AlertSubj = AlertSubj + 'DOWN'
            AlertMsg = AlertSubj + ' @ ' + TimeToString(TimeLocal(), TIME_SECONDS)
            if InpMsgAlerts:
                Alert(AlertMsg)
            if InpEmailAlerts:
                mailsent = False
                mailsent = SendMail(AlertSubj, AlertMsg)
                if mailsent == False and ShowErrorMessages:
                    Print('Email alert was not sent! ', AlertMsg, ' --- Error', GetLastError())
            if InpSoundAlerts:
                playsoundfile = False
                playsoundfile = PlaySound(InpSoundAlertFile)
                if playsoundfile == False and ShowErrorMessages:
                    Print('Soundfile not found:"', InpSoundAlertFile, '" --- Error', GetLastError())
            LastAlertBar = rates_total
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Qqe(_MQL5Indicator):
    name = 'qqe'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpSF': 5,  # Smoothing Factor
        'InpAlertLevel': 50,  # Alert level
        'InpMsgAlerts': False,  # Use alert message
        'InpEmailAlerts': False,  # Send email alert
        'InpSoundAlerts': False,  # Play sound alert
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

