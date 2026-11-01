"""qqe_mtf — converted from MQL5: MQL5 Indicators/QQE [v02] and QQE multi-timeframe [v02]/qqe_mtf.mq5

QQE - Qualitative Quantitative Estimation, Multi-timeframe
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

MQL5_META = {'props': {'copyright': '2010, traderak20@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [65535]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 2}, 'labels': {}, 'levels': [50.0], 'description': ['QQE - Qualitative Quantitative Estimation, Multi-timeframe', 'Calculated as two indicators:', '1) MA on RSI', '2) Difference of MA on RSI and MA of MA of ATR of MA of RSI', 'The signal for buy is when blue line crosses level 50 from below', 'after crossing the yellow line from below.', 'The signal for sell is when blue line crosses level 50 from above', 'after crossing the yellow line from above.'], 'name': 'qqe_mtf', 'source': 'MQL5 Indicators/QQE [v02] and QQE multi-timeframe [v02]/qqe_mtf.mq5', 'folder': 'QQE [v02] and QQE multi-timeframe [v02]', 'inputs': [{'mql': 'InpTimeFrame_2', 'py': 'InpTimeFrame_2', 'param': 'InpTimeFrame_2', 'type': 'int', 'default': 16385, 'label': 'Timeframe 2 (TF2) period', 'sinput': False}, {'mql': 'InpIndicator_TF1', 'py': 'InpIndicator_TF1', 'param': None, 'type': 'string', 'default': 'qqe', 'label': 'Location of single timeframe indicator', 'sinput': False}, {'mql': 'InpSF', 'py': 'InpSF', 'param': 'InpSF', 'type': 'int', 'default': 5, 'label': 'Smoothing Factor', 'sinput': False}, {'mql': 'InpAlertLevel', 'py': 'InpAlertLevel', 'param': 'InpAlertLevel', 'type': 'int', 'default': 50, 'label': 'Alert level', 'sinput': False}, {'mql': 'InpMsgAlerts', 'py': 'InpMsgAlerts', 'param': 'InpMsgAlerts', 'type': 'bool', 'default': False, 'label': 'Use alert message', 'sinput': False}, {'mql': 'InpEmailAlerts', 'py': 'InpEmailAlerts', 'param': 'InpEmailAlerts', 'type': 'bool', 'default': False, 'label': 'Send email alert', 'sinput': False}, {'mql': 'InpSoundAlerts', 'py': 'InpSoundAlerts', 'param': 'InpSoundAlerts', 'type': 'bool', 'default': False, 'label': 'Play sound alert', 'sinput': False}, {'mql': 'InpSoundAlertFile', 'py': 'InpSoundAlertFile', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Sound alert', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpTimeFrame_2 = _input('InpTimeFrame_2', PERIOD_H1)  # Timeframe 2 (TF2) period
InpIndicator_TF1 = _input('InpIndicator_TF1', 'qqe')  # Location of single timeframe indicator
InpSF = _input('InpSF', 5)  # Smoothing Factor
InpAlertLevel = _input('InpAlertLevel', 50)  # Alert level
InpMsgAlerts = _input('InpMsgAlerts', False)  # Use alert message
InpEmailAlerts = _input('InpEmailAlerts', False)  # Send email alert
InpSoundAlerts = _input('InpSoundAlerts', False)  # Play sound alert
InpSoundAlertFile = _input('InpSoundAlertFile', 'alert.wav')  # Sound alert
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
ExtRsiMaBuffer_TF2 = Arr(0, 0.0)
ExtTrLevelSlowBuffer_TF2 = Arr(0, 0.0)
ExtRsiMaArray_TF2 = Arr(0, 0.0)  # intermediate array to hold TF2 Fast RSI MA buffer values
ExtTrLevelSlowArray_TF2 = Arr(0, 0.0)  # intermediate array to hold TF2 Slow RSI MA buffer values
PeriodRatio = 1  # ratio between timeframe 1 (TF1) and timeframe 2 (TF2)
PeriodSeconds_TF1 = 0  # TF1 period in seconds
PeriodSeconds_TF2 = 0  # TF2 period in seconds
RSI_Period = 14
Wilders_Period = 0
SmoothingFactor = 0
ExtQqeHandle_TF2 = 0  # QQE handle TF2
ShowErrorMessages = True  # turn on/off error messages for debugging

def OnInit():
    global ExtQqeHandle_TF2, PeriodRatio, PeriodSeconds_TF1, PeriodSeconds_TF2, SmoothingFactor, Wilders_Period
    Wilders_Period = (RSI_Period * 2) - 1
    SmoothingFactor = InpSF
    if SmoothingFactor <= 0:
        SmoothingFactor = 5
    SetIndexBuffer(0, ExtRsiMaBuffer_TF2, INDICATOR_DATA)
    SetIndexBuffer(1, ExtTrLevelSlowBuffer_TF2, INDICATOR_DATA)
    ArraySetAsSeries(ExtRsiMaBuffer_TF2, True)
    ArraySetAsSeries(ExtTrLevelSlowBuffer_TF2, True)
    ArraySetAsSeries(ExtRsiMaArray_TF2, True)
    ArraySetAsSeries(ExtTrLevelSlowArray_TF2, True)
    PlotIndexSetString(0, PLOT_LABEL, 'Fast RSI MA_TF2')
    PlotIndexSetString(1, PLOT_LABEL, 'Slow RSI MA_TF2')
    PeriodSeconds_TF1 = PeriodSeconds()
    PeriodSeconds_TF2 = PeriodSeconds(InpTimeFrame_2)
    if PeriodSeconds_TF1 < PeriodSeconds_TF2:
        PeriodRatio = _idiv(PeriodSeconds_TF2, PeriodSeconds_TF1)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    IndicatorSetDouble(INDICATOR_MINIMUM, -5)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 105)
    IndicatorSetString(INDICATOR_SHORTNAME, 'QQE(' + IntegerToString(SmoothingFactor) + ')')
    ExtQqeHandle_TF2 = iCustom(None, InpTimeFrame_2, InpIndicator_TF1, InpSF, InpAlertLevel, InpMsgAlerts, InpEmailAlerts, InpSoundAlerts, InpSoundAlertFile, InpAppliedPrice)
    if ExtQqeHandle_TF2 == INVALID_HANDLE:
        return -1
    return 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    ArraySetAsSeries(Time, True)
    bars_TF2 = Bars(None, InpTimeFrame_2)
    if bars_TF2 < (RSI_Period + SmoothingFactor + 1 + Wilders_Period + Wilders_Period):
        return 0
    calculated_TF2 = 0
    calculated_TF2 = BarsCalculated(ExtQqeHandle_TF2)
    if calculated_TF2 < bars_TF2:
        if ShowErrorMessages:
            Print('Not all data of ExtQqeHandle_TF2 has been calculated (', calculated_TF2, ' bars). Error', GetLastError())
        return 0
    limit = 0
    if (prev_calculated == 0 or prev_calculated < 0) or prev_calculated > rates_total:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    convertedTime = 0
    for i in range(limit, 0 - 1, -1):
        if InpAppliedPrice != PRICE_OPEN:
            convertedTime = Time[i] + PeriodSeconds_TF1 - PeriodSeconds_TF2
        if InpAppliedPrice == PRICE_OPEN:
            convertedTime = Time[i]
        tempTimeArray_TF2 = Arr(0, 0)
        CopyTime(None, InpTimeFrame_2, calculated_TF2 - 1, 1, tempTimeArray_TF2)
        if convertedTime < tempTimeArray_TF2[0]:
            ExtRsiMaBuffer_TF2[i] = EMPTY_VALUE
            ExtTrLevelSlowBuffer_TF2[i] = EMPTY_VALUE
            continue
        if CopyBuffer(ExtQqeHandle_TF2, 0, _DT(convertedTime), 1, ExtRsiMaArray_TF2) <= 0:
            if ShowErrorMessages:
                Print('Getting ICycle Arrow TF2 failed! Error', GetLastError())
            return 0
        else:
            ExtRsiMaBuffer_TF2[i] = ExtRsiMaArray_TF2[0]
        if CopyBuffer(ExtQqeHandle_TF2, 1, _DT(convertedTime), 1, ExtTrLevelSlowArray_TF2) <= 0:
            if ShowErrorMessages:
                Print('Getting ICycle Arrow color TF2 failed! Error', GetLastError())
            return 0
        else:
            ExtTrLevelSlowBuffer_TF2[i] = ExtTrLevelSlowArray_TF2[0]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class QqeMtf(_MQL5Indicator):
    name = 'qqe_mtf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTimeFrame_2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Timeframe 2 (TF2) period
        'InpSF': 5,  # Smoothing Factor
        'InpAlertLevel': 50,  # Alert level
        'InpMsgAlerts': False,  # Use alert message
        'InpEmailAlerts': False,  # Send email alert
        'InpSoundAlerts': False,  # Play sound alert
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

