"""MACD Candles — converted from MQL5: MQL5 Indicators/MACD Candles Alert/MACD Candles.mq5

Moving Average Convergence/Divergence
Copyright: A.L.I™; Link: https://www.aligroup.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'A.L.I™', 'link': 'https://www.aligroup.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [3329330, 32768, 255, 2237106, 6908265]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Macd Candles'}, 'levels': [], 'description': ['Moving Average Convergence/Divergence'], 'name': 'MACD Candles', 'source': 'MQL5 Indicators/MACD Candles Alert/MACD Candles.mq5', 'folder': 'MACD Candles Alert', 'inputs': [{'mql': 'InpFastEMA', 'py': 'InpFastEMA', 'param': 'InpFastEMA', 'type': 'int', 'default': 12, 'label': 'Macd fast period', 'sinput': False}, {'mql': 'InpSlowEMA', 'py': 'InpSlowEMA', 'param': 'InpSlowEMA', 'type': 'int', 'default': 26, 'label': 'Macd slow period', 'sinput': False}, {'mql': 'InpSignalEMA', 'py': 'InpSignalEMA', 'param': 'InpSignalEMA', 'type': 'int', 'default': 9, 'label': 'Macd Signal period', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied Price', 'sinput': False}, {'mql': 'AlertOn', 'py': 'AlertOn', 'param': 'AlertOn', 'type': 'bool', 'default': True, 'label': 'Alerts On', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Show Alert Message', 'sinput': False}, {'mql': 'EmailON', 'py': 'EmailON', 'param': 'EmailON', 'type': 'bool', 'default': False, 'label': 'Send Email Alerts', 'sinput': False}, {'mql': 'PushNotificationON', 'py': 'PushNotificationON', 'param': 'PushNotificationON', 'type': 'bool', 'default': False, 'label': 'Send Push Notifications', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFastEMA = _input('InpFastEMA', 12)  # Macd fast period
InpSlowEMA = _input('InpSlowEMA', 26)  # Macd slow period
InpSignalEMA = _input('InpSignalEMA', 9)  # Macd Signal period
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)  # Applied Price
AlertOn = _input('AlertOn', True)  # Alerts On
SoundON = _input('SoundON', True)  # Show Alert Message
EmailON = _input('EmailON', False)  # Send Email Alerts
PushNotificationON = _input('PushNotificationON', False)  # Send Push Notifications
iMACD_Handle = 0
prog_name = 'MACD'
candleH = Arr(0, 0.0)
candleL = Arr(0, 0.0)
candleO = Arr(0, 0.0)
candleC = Arr(0, 0.0)
Colors = Arr(0, 0.0)

def OnInit():
    global iMACD_Handle
    SetIndexBuffer(0, candleO, INDICATOR_DATA)
    SetIndexBuffer(1, candleH, INDICATOR_DATA)
    SetIndexBuffer(2, candleL, INDICATOR_DATA)
    SetIndexBuffer(3, candleC, INDICATOR_DATA)
    SetIndexBuffer(4, Colors, INDICATOR_COLOR_INDEX)
    if (iMACD_Handle := iMACD(Symbol(), PERIOD_CURRENT, InpFastEMA, InpSlowEMA, InpSignalEMA, AppliedPrice)) == INVALID_HANDLE:
        Print('Failed to initialize ', Symbol(), ' MACD indicator handle')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastBarTime
    MacdMainBuffer = Arr(0, 0.0)
    MacdSignalBuffer = Arr(0, 0.0)
    if BarsCalculated(iMACD_Handle) < rates_total or CopyBuffer(iMACD_Handle, MAIN_LINE, 0, rates_total, MacdMainBuffer) < rates_total:
        Print('Unable to get macd indicator values, Error Code: ', GetLastError())
        return 0
    if BarsCalculated(iMACD_Handle) < rates_total or CopyBuffer(iMACD_Handle, SIGNAL_LINE, 0, rates_total, MacdSignalBuffer) < rates_total:
        Print('Unable to get macd indicator values, Error Code: ', GetLastError())
        return 0
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        if MacdMainBuffer[i] > 0:
            if MacdMainBuffer[i] > MacdSignalBuffer[i]:
                Colors[i] = 0.0
            if MacdMainBuffer[i] < MacdSignalBuffer[i]:
                Colors[i] = 1.0
        if MacdMainBuffer[i] < 0:
            if MacdMainBuffer[i] < MacdSignalBuffer[i]:
                Colors[i] = 2.0
            if MacdMainBuffer[i] > MacdSignalBuffer[i]:
                Colors[i] = 3.0
        candleO[i] = open[i]
        candleH[i] = high[i]
        candleL[i] = low[i]
        candleC[i] = close[i]
    if AlertOn:
        isNewBar = False
        CurrentBarTime = iTime(Symbol(), PERIOD_CURRENT, 0)
        _s_OnCalculate_LastBarTime = (CurrentBarTime if (isNewBar := CurrentBarTime > _s_OnCalculate_LastBarTime) else _s_OnCalculate_LastBarTime)
        if isNewBar:
            message = ""
            ArraySetAsSeries(MacdMainBuffer, True)
            if (MacdMainBuffer[0] > 0 and MacdMainBuffer[1] > 0) and MacdMainBuffer[2] < 0:
                message = 'BUY'
            if (MacdMainBuffer[0] < 0 and MacdMainBuffer[1] < 0) and MacdMainBuffer[2] > 0:
                message = 'SELL'
            if message != "":
                message = TimeToString(TimeCurrent(), TIME_MINUTES) + ' ' + Symbol() + ' ' + GetTimeFrame(PERIOD_CURRENT) + ' ' + prog_name + ' ' + message
                if SoundON:
                    Alert(message)
                if PushNotificationON:
                    SendNotification(message)
                if EmailON:
                    SendMail(prog_name, message)
    return rates_total

def GetTimeFrame(timeframe):
    timeframe = (Period() if (timeframe == PERIOD_CURRENT) else timeframe)
    period_xxx = EnumToString(timeframe, 'ENUM_TIMEFRAMES')
    return StringSubstr(period_xxx, 7)

# ---- static local variables
_s_OnCalculate_LastBarTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDCandles(_MQL5Indicator):
    name = 'MACD Candles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastEMA': 12,  # Macd fast period
        'InpSlowEMA': 26,  # Macd slow period
        'InpSignalEMA': 9,  # Macd Signal period
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied Price
        'AlertOn': True,  # Alerts On
        'SoundON': True,  # Show Alert Message
        'EmailON': False,  # Send Email Alerts
        'PushNotificationON': False,  # Send Push Notifications
    }

