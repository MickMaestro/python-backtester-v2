"""Trend Rider — converted from MQL5: MQL5 Indicators/Trend Rider Alert/Trend Rider.mq5

Copyright: A.L.I™; Link: https://www.aligroup.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'A.L.I™', 'link': 'https://www.aligroup.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 2}, 'types': {1: 17, 2: 8}, 'colors': {1: [6908265, 32768, 255], 2: [16760576, 9662683]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 2}, 'labels': {1: 'Bars', 2: 'TrendLine'}, 'levels': [], 'description': [], 'name': 'Trend Rider', 'source': 'MQL5 Indicators/Trend Rider Alert/Trend Rider.mq5', 'folder': 'Trend Rider Alert', 'inputs': [{'mql': 'AtrLength', 'py': 'AtrLength', 'param': 'AtrLength', 'type': 'int', 'default': 10, 'label': 'ATR calculaion period', 'sinput': False}, {'mql': 'AtrMultiplier', 'py': 'AtrMultiplier', 'param': 'AtrMultiplier', 'type': 'double', 'default': 3.0, 'label': 'ATR multiplier', 'sinput': False}, {'mql': 'AtrAppliedPrice', 'py': 'AtrAppliedPrice', 'param': 'AtrAppliedPrice', 'type': 'int', 'default': 1, 'label': 'AtrAppliedPrice to use', 'sinput': False}, {'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'int', 'default': 14, 'label': 'Rsi Period', 'sinput': False}, {'mql': 'RsiAppliedPrice', 'py': 'RsiAppliedPrice', 'param': 'RsiAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Rsi Applied AtrAppliedPrice', 'sinput': False}, {'mql': 'InpFastEMA', 'py': 'InpFastEMA', 'param': 'InpFastEMA', 'type': 'int', 'default': 12, 'label': 'Macd fast period', 'sinput': False}, {'mql': 'InpSlowEMA', 'py': 'InpSlowEMA', 'param': 'InpSlowEMA', 'type': 'int', 'default': 26, 'label': 'Macd slow period', 'sinput': False}, {'mql': 'InpSignalEMA', 'py': 'InpSignalEMA', 'param': 'InpSignalEMA', 'type': 'int', 'default': 9, 'label': 'Macd Signal period', 'sinput': False}, {'mql': 'MacdAppliedPrice', 'py': 'MacdAppliedPrice', 'param': 'MacdAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied AtrAppliedPrice', 'sinput': False}, {'mql': 'AlertOn', 'py': 'AlertOn', 'param': 'AlertOn', 'type': 'bool', 'default': True, 'label': 'Alerts On', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Show Alert Message', 'sinput': False}, {'mql': 'EmailON', 'py': 'EmailON', 'param': 'EmailON', 'type': 'bool', 'default': False, 'label': 'Send Email Alerts', 'sinput': False}, {'mql': 'PushNotificationON', 'py': 'PushNotificationON', 'param': 'PushNotificationON', 'type': 'bool', 'default': False, 'label': 'Send Push Notifications', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AtrLength = _input('AtrLength', 10)  # ATR calculaion period
AtrMultiplier = _input('AtrMultiplier', 3.0)  # ATR multiplier
AtrAppliedPrice = _input('AtrAppliedPrice', PRICE_CLOSE)  # AtrAppliedPrice to use
RsiPeriod = _input('RsiPeriod', 14)  # Rsi Period
RsiAppliedPrice = _input('RsiAppliedPrice', PRICE_CLOSE)  # Rsi Applied AtrAppliedPrice
InpFastEMA = _input('InpFastEMA', 12)  # Macd fast period
InpSlowEMA = _input('InpSlowEMA', 26)  # Macd slow period
InpSignalEMA = _input('InpSignalEMA', 9)  # Macd Signal period
MacdAppliedPrice = _input('MacdAppliedPrice', PRICE_CLOSE)  # Applied AtrAppliedPrice
AlertOn = _input('AlertOn', True)  # Alerts On
SoundON = _input('SoundON', True)  # Show Alert Message
EmailON = _input('EmailON', False)  # Send Email Alerts
PushNotificationON = _input('PushNotificationON', False)  # Send Push Notifications
prog_name = 'Trend Rider'
iATR_Handle = 0
iRSI_Handle = 0
iMACD_Handle = 0
Up = Arr(0, 0.0)
Dn = Arr(0, 0.0)
Di = Arr(0, 0.0)
SuperTrend = Arr(0, 0.0)
STColors = Arr(0, 0.0)
candleH = Arr(0, 0.0)
candleL = Arr(0, 0.0)
candleO = Arr(0, 0.0)
candleC = Arr(0, 0.0)
Ccolors = Arr(0, 0.0)

def OnInit():
    global iATR_Handle, iMACD_Handle, iRSI_Handle
    SetIndexBuffer(0, candleO, INDICATOR_DATA)
    SetIndexBuffer(1, candleH, INDICATOR_DATA)
    SetIndexBuffer(2, candleL, INDICATOR_DATA)
    SetIndexBuffer(3, candleC, INDICATOR_DATA)
    SetIndexBuffer(4, Ccolors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, SuperTrend, INDICATOR_DATA)
    SetIndexBuffer(6, STColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, Up, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, Dn, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, Di, INDICATOR_CALCULATIONS)
    if (iMACD_Handle := iMACD(Symbol(), PERIOD_CURRENT, InpFastEMA, InpSlowEMA, InpSignalEMA, MacdAppliedPrice)) == INVALID_HANDLE:
        Print('Failed to initialize ', Symbol(), ' MACD indicator handle')
        return INIT_FAILED
    if (iRSI_Handle := iRSI(Symbol(), PERIOD_CURRENT, RsiPeriod, RsiAppliedPrice)) == INVALID_HANDLE:
        Print('Failed to initialize ', Symbol(), ' RSI indicator handle')
        return INIT_FAILED
    if (iATR_Handle := iATR(Symbol(), PERIOD_CURRENT, AtrLength)) == INVALID_HANDLE:
        Print('Failed to initialize ', Symbol(), ' ATR indicator handle')
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, prog_name + ' (' + _str(AtrLength) + ',' + _str(AtrMultiplier) + ') ' + GetTimeFrame(PERIOD_CURRENT))
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastBarTime
    atr = Arr(0, 0.0)
    rsi = Arr(0, 0.0)
    macd = Arr(0, 0.0)
    if BarsCalculated(iMACD_Handle) < rates_total or CopyBuffer(iMACD_Handle, MAIN_LINE, 0, rates_total, macd) < rates_total:
        Print('Unable to get all ', Symbol(), ' MACD indicator values, Error Code: ', GetLastError())
        return 0
    if BarsCalculated(iRSI_Handle) < rates_total or CopyBuffer(iRSI_Handle, 0, 0, rates_total, rsi) < rates_total:
        Print('Unable to get all ', Symbol(), ' RSI indicator values, Error Code: ', GetLastError())
        return 0
    if BarsCalculated(iATR_Handle) < rates_total or CopyBuffer(iATR_Handle, 0, 0, rates_total, atr) < rates_total:
        Print('Unable to get all ', Symbol(), ' ATR indicator values, Error Code: ', GetLastError())
        return 0
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        mprice = (high[i] + low[i]) / 2
        Up[i] = mprice + (AtrMultiplier * atr[i])
        Dn[i] = mprice - (AtrMultiplier * atr[i])
        cprice = getPrice(AtrAppliedPrice, open, close, high, low, i)
        Di[i] = (1 if (cprice > Up[i - 1]) else -1 if (cprice < Dn[i - 1]) else Di[i - 1])
        if Di[i] > 0:
            STColors[i] = 0.0
            Ccolors[i] = (1 if (rsi[i] > 50 and macd[i] > 0) else 0)
            Dn[i] = MathMax(Dn[i], Dn[i - 1])
            SuperTrend[i] = Dn[i]
        if Di[i] < 0:
            STColors[i] = 1.0
            Ccolors[i] = (2 if (rsi[i] < 50 and macd[i] < 0) else 0)
            Up[i] = MathMin(Up[i], Up[i - 1])
            SuperTrend[i] = Up[i]
        candleO[i] = open[i]
        candleH[i] = high[i]
        candleL[i] = low[i]
        candleC[i] = close[i]
    if AlertOn:
        isNewBar = False
        bars = rates_total - 1
        CurrentBarTime = iTime(Symbol(), PERIOD_CURRENT, 0)
        _s_OnCalculate_LastBarTime = (CurrentBarTime if (isNewBar := CurrentBarTime > _s_OnCalculate_LastBarTime) else _s_OnCalculate_LastBarTime)
        if isNewBar and Ccolors[bars - 1] != Ccolors[bars - 2]:
            prevTrend = ('BUY' if (Ccolors[bars - 2] == 1) else 'SELL' if (Ccolors[bars - 2] == 2) else '')
            direction = (('EXIT ' + prevTrend) if (Ccolors[bars - 1] == 0) else 'BUY' if (Ccolors[bars - 1] == 1) else 'SELL' if (Ccolors[bars - 1] == 2) else None)
            if direction != "":
                message = TimeToString(time[bars], TIME_MINUTES) + ' ' + Symbol() + ' ' + GetTimeFrame(PERIOD_CURRENT) + ' ' + prog_name + ' ' + direction
                if SoundON:
                    Alert(message)
                if PushNotificationON:
                    SendNotification(message)
                if EmailON:
                    SendMail(prog_name, message)
    return rates_total

def getPrice(price, open, close, high, low, i):
    _sw1 = price
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    else:
        return close[i]

def GetTimeFrame(timeframe):
    timeframe = (Period() if (timeframe == PERIOD_CURRENT) else timeframe)
    period_xxx = EnumToString(timeframe, 'ENUM_TIMEFRAMES')
    return StringSubstr(period_xxx, 7)

# ---- static local variables
_s_OnCalculate_LastBarTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendRider(_MQL5Indicator):
    name = 'Trend Rider'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AtrLength': 10,  # ATR calculaion period
        'AtrMultiplier': 3.0,  # ATR multiplier
        'AtrAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # AtrAppliedPrice to use
        'RsiPeriod': 14,  # Rsi Period
        'RsiAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Rsi Applied AtrAppliedPrice
        'InpFastEMA': 12,  # Macd fast period
        'InpSlowEMA': 26,  # Macd slow period
        'InpSignalEMA': 9,  # Macd Signal period
        'MacdAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied AtrAppliedPrice
        'AlertOn': True,  # Alerts On
        'SoundON': True,  # Show Alert Message
        'EmailON': False,  # Send Email Alerts
        'PushNotificationON': False,  # Send Push Notifications
    }

