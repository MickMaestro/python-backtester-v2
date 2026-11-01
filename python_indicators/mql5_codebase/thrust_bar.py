"""Thrust_Bar — converted from MQL5: MQL5 Indicators/Thrust_Bar/Thrust_Bar.mq5

Thrust Bar indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 17}, 'colors': {1: [32768], 2: [255], 3: [2263842, 255, 13882323]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Bullish', 2: 'Bearish', 3: 'Open;High;Low;Close'}, 'levels': [], 'description': ['Thrust Bar indicator'], 'name': 'Thrust_Bar', 'source': 'MQL5 Indicators/Thrust_Bar/Thrust_Bar.mq5', 'folder': 'Thrust_Bar', 'inputs': [{'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Indicator mode', 'sinput': False}, {'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 14, 'label': 'ATR period', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 2.0, 'label': 'ATR multiplier/Size candle in points', 'sinput': False}, {'mql': 'InpUseLong', 'py': 'InpUseLong', 'param': 'InpUseLong', 'type': 'int', 'default': 1, 'label': 'Use long side', 'sinput': False}, {'mql': 'InpUseShort', 'py': 'InpUseShort', 'param': 'InpUseShort', 'type': 'int', 'default': 1, 'label': 'Use short side', 'sinput': False}, {'mql': 'InpUseAlerts', 'py': 'InpUseAlerts', 'param': 'InpUseAlerts', 'type': 'int', 'default': 1, 'label': 'Use alerts', 'sinput': False}, {'mql': 'InpSendMail', 'py': 'InpSendMail', 'param': 'InpSendMail', 'type': 'int', 'default': 0, 'label': 'Send mail', 'sinput': False}, {'mql': 'InpSendPush', 'py': 'InpSendPush', 'param': 'InpSendPush', 'type': 'int', 'default': 1, 'label': 'Send push-notifications', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# enum ENUM_IND_METHOD
IND_METHOD_ATR = 0
IND_METHOD_PT = 1
_enum('ENUM_IND_METHOD', {0: 'IND_METHOD_ATR', 1: 'IND_METHOD_PT'})

# ---- inputs and global variables
InpMethod = _input('InpMethod', IND_METHOD_ATR)  # Indicator mode
InpPeriodATR = _input('InpPeriodATR', 14)  # ATR period
InpMultiplier = _input('InpMultiplier', 2.0)  # ATR multiplier/Size candle in points
InpUseLong = _input('InpUseLong', INPUT_YES)  # Use long side
InpUseShort = _input('InpUseShort', INPUT_YES)  # Use short side
InpUseAlerts = _input('InpUseAlerts', INPUT_YES)  # Use alerts
InpSendMail = _input('InpSendMail', INPUT_NO)  # Send mail
InpSendPush = _input('InpSendPush', INPUT_YES)  # Send push-notifications
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
BufferCandleOpen = Arr(0, 0.0)
BufferCandleHigh = Arr(0, 0.0)
BufferCandleLow = Arr(0, 0.0)
BufferCandleClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
multiplier = 0.0
period_atr = 0
period_max = 0
handle_atr = 0

def OnInit():
    global handle_atr, multiplier, period_atr, period_max
    period_atr = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    multiplier = InpMultiplier
    period_max = (period_atr if (InpMethod == IND_METHOD_ATR) else 4)
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCandleOpen, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCandleHigh, INDICATOR_DATA)
    SetIndexBuffer(4, BufferCandleLow, INDICATOR_DATA)
    SetIndexBuffer(5, BufferCandleClose, INDICATOR_DATA)
    SetIndexBuffer(6, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, BufferATR, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    data = (('(ATR period ' + _str(period_atr) + ',' + DoubleToString(multiplier, 1) + ')') if (InpMethod == IND_METHOD_ATR) else ('(' + DoubleToString(multiplier, 0) + ' Points)'))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Thrust Bar ' + data)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferCandleOpen, True)
    ArraySetAsSeries(BufferCandleHigh, True)
    ArraySetAsSeries(BufferCandleLow, True)
    ArraySetAsSeries(BufferCandleClose, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_time
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if rates_total < period_max:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferCandleOpen, EMPTY_VALUE)
        ArrayInitialize(BufferCandleHigh, EMPTY_VALUE)
        ArrayInitialize(BufferCandleLow, EMPTY_VALUE)
        ArrayInitialize(BufferCandleClose, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferATR, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_atr, MAIN_LINE, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferCandleClose[i] = EMPTY_VALUE
        BufferCandleLow[i] = BufferCandleClose[i]
        BufferCandleHigh[i] = BufferCandleLow[i]
        BufferCandleOpen[i] = BufferCandleHigh[i]
        BufferColors[i] = 2.0
        x = (_fdiv(multiplier * BufferATR[i], Point()) if (InpMethod == IND_METHOD_ATR) else multiplier)
        y = _fdiv(close[i] - open[i], Point())
        if y > x and InpUseLong:
            BufferUP[i] = low[i]
            BufferCandleOpen[i] = open[i]
            BufferCandleHigh[i] = high[i]
            BufferCandleLow[i] = low[i]
            BufferCandleClose[i] = close[i]
            BufferColors[i] = 0.0
            if i == 0 and _s_OnCalculate_last_time != time[0]:
                message = Symbol() + ', ' + TimeframeToString(Period()) + ': Thrust Bullish Bar at ' + TimeToString(TimeCurrent())
                if InpUseAlerts:
                    Alert(message)
                if InpSendMail and TerminalInfoInteger(TERMINAL_EMAIL_ENABLED):
                    SendMail('Thrust Bar Signal', message)
                if InpSendPush and TerminalInfoInteger(TERMINAL_NOTIFICATIONS_ENABLED):
                    SendNotification(message)
                _s_OnCalculate_last_time = time[0]
        if y < (-x) and InpUseShort:
            BufferDN[i] = high[i]
            BufferCandleOpen[i] = open[i]
            BufferCandleHigh[i] = high[i]
            BufferCandleLow[i] = low[i]
            BufferCandleClose[i] = close[i]
            BufferColors[i] = 1.0
            if i == 0 and _s_OnCalculate_last_time != time[0]:
                message = Symbol() + ', ' + TimeframeToString(Period()) + ': Thrust Bearish Bar at ' + TimeToString(TimeCurrent())
                if InpUseAlerts:
                    Alert(message)
                if InpSendMail and TerminalInfoInteger(TERMINAL_EMAIL_ENABLED):
                    SendMail('Thrust Bar Signal', message)
                if InpSendPush and TerminalInfoInteger(TERMINAL_NOTIFICATIONS_ENABLED):
                    SendNotification(message)
                _s_OnCalculate_last_time = time[0]
    return rates_total

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

# ---- static local variables
_s_OnCalculate_last_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ThrustBar(_MQL5Indicator):
    name = 'Thrust_Bar'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMethod': _Choice({0: 'ATR', 1: 'Points'}, default=0),  # Indicator mode
        'InpPeriodATR': 14,  # ATR period
        'InpMultiplier': 2.0,  # ATR multiplier/Size candle in points
        'InpUseLong': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use long side
        'InpUseShort': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use short side
        'InpUseAlerts': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use alerts
        'InpSendMail': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Send mail
        'InpSendPush': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Send push-notifications
    }

