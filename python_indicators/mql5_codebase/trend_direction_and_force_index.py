"""Trend Direction And Force Index — converted from MQL5: MQL5 Indicators/Trend Direction And Force Index Alert/Trend Direction And Force Index.mq5

Copyright: Copyright 2022, aligroup inc.; Link: https://www.aligroup.org; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, aligroup inc.', 'link': 'https://www.aligroup.org', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 10, 2: 5, 3: 5, 4: 5}, 'colors': {1: [12632256, 8421376, 16436871, 2763429, 13353215], 2: [65280], 3: [255], 4: [12632256]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'TDFI', 2: 'BUY', 3: 'SELL', 4: 'FLAT'}, 'levels': [], 'description': [], 'name': 'Trend Direction And Force Index', 'source': 'MQL5 Indicators/Trend Direction And Force Index Alert/Trend Direction And Force Index.mq5', 'folder': 'Trend Direction And Force Index Alert', 'inputs': [{'mql': 'inpTrendPeriod', 'py': 'inpTrendPeriod', 'param': 'inpTrendPeriod', 'type': 'int', 'default': 14, 'label': 'Trend period', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'double', 'default': 3.0, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpTriggerUp', 'py': 'inpTriggerUp', 'param': 'inpTriggerUp', 'type': 'double', 'default': 0.05, 'label': 'Trigger up level', 'sinput': False}, {'mql': 'inpTriggerDown', 'py': 'inpTriggerDown', 'param': 'inpTriggerDown', 'type': 'double', 'default': -0.05, 'label': 'Trigger down level', 'sinput': False}, {'mql': 'AlertOn', 'py': 'AlertOn', 'param': 'AlertOn', 'type': 'bool', 'default': True, 'label': 'Alerts On', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Show Alert Message', 'sinput': False}, {'mql': 'EmailON', 'py': 'EmailON', 'param': 'EmailON', 'type': 'bool', 'default': False, 'label': 'Send Email Alerts', 'sinput': False}, {'mql': 'PushNotificationON', 'py': 'PushNotificationON', 'param': 'PushNotificationON', 'type': 'bool', 'default': False, 'label': 'Send Push Notifications', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpTrendPeriod = _input('inpTrendPeriod', 14)  # Trend period
inpSmooth = _input('inpSmooth', 3.0)  # Smoothing period
inpTriggerUp = _input('inpTriggerUp', 0.05)  # Trigger up level
inpTriggerDown = _input('inpTriggerDown', -0.05)  # Trigger down level
AlertOn = _input('AlertOn', True)  # Alerts On
SoundON = _input('SoundON', True)  # Show Alert Message
EmailON = _input('EmailON', False)  # Send Email Alerts
PushNotificationON = _input('PushNotificationON', False)  # Send Push Notifications
prog_name = 'TDFi'
_maxPeriod = 3 * inpTrendPeriod
Trend = Arr(0, 0.0)
Colors = Arr(0, 0.0)
mma = Arr(0, 0.0)
smma = Arr(0, 0.0)
tdfa = Arr(0, 0.0)
Buy = Arr(0, 0.0)
Sell = Arr(0, 0.0)
Flat = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, Trend, INDICATOR_DATA)
    SetIndexBuffer(1, Colors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, Buy, INDICATOR_DATA)
    SetIndexBuffer(3, Sell, INDICATOR_DATA)
    SetIndexBuffer(4, Flat, INDICATOR_DATA)
    SetIndexBuffer(5, mma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, smma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, tdfa, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'TDFI(' + _str(inpTrendPeriod) + ',' + _str(MathMax(inpSmooth, 1)) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastBarTime
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        Colors[i] = 0.0
        Flat[i] = EMPTY_VALUE
        Sell[i] = Flat[i]
        Buy[i] = Sell[i]
        Trend[i] = Buy[i]
        mma[i] = ((mma[i - 1] + (_alpha * (close[i] - mma[i - 1]))) if (i > 0) else close[i])
        smma[i] = ((smma[i - 1] + (_alpha * (mma[i] - smma[i - 1]))) if (i > 0) else mma[i])
        impetmma = mma[i] - mma[i - 1]
        impetsmma = smma[i] - smma[i - 1]
        divma = MathAbs(mma[i] - smma[i])
        averimpet = (impetmma + impetsmma) / 2.0
        tdf = divma * averimpet * averimpet * averimpet
        tdfa[i] = MathAbs(tdf)
        _start = MathMax(i - _maxPeriod + 1, 0)
        _absValue = tdfa[ArrayMaximum(tdfa, _start, _maxPeriod)]
        _val1 = (_fdiv(tdf, _absValue) if (_absValue > 0) else 0)
        Trend[i] = Trend[i - 1] + (_alpha2 * (_val1 - Trend[i - 1]))
        if Trend[i] > inpTriggerUp:
            Colors[i] = (1 if (Trend[i] > Trend[i - 1]) else 2)
            if Trend[i - 1] < inpTriggerUp:
                Buy[i] = 0.0
        if Trend[i] < inpTriggerDown:
            Colors[i] = (3 if (Trend[i] < Trend[i - 1]) else 4)
            if Trend[i - 1] > inpTriggerDown:
                Sell[i] = 0.0
        if (Trend[i] < inpTriggerUp and Trend[i - 1] > inpTriggerUp) or (Trend[i] > inpTriggerDown and Trend[i - 1] < inpTriggerDown):
            Flat[i] = 0.0
    if AlertOn:
        isNewBar = False
        CurrentBarTime = iTime(Symbol(), PERIOD_CURRENT, 0)
        _s_OnCalculate_LastBarTime = (CurrentBarTime if (isNewBar := CurrentBarTime > _s_OnCalculate_LastBarTime) else _s_OnCalculate_LastBarTime)
        if isNewBar:
            bar = rates_total - 2
            message = ('BUY' if (Buy[bar] == 0.0) else 'SELL' if (Sell[bar] == 0.0) else '')
            if StringLen(message) > 0:
                message = TimeToString(time[bar], TIME_MINUTES) + ' ' + Symbol() + ' ' + prog_name + ' ' + GetTimeFrame(PERIOD_CURRENT) + ' ' + message
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

# ---- global variables initialised from expressions
_alpha = _fdiv(2.0, 1.0 + inpTrendPeriod)
_alpha2 = _fdiv(2.0, 1.0 + MathSqrt(MathMax(inpSmooth, 1)))

# ---- static local variables
_s_OnCalculate_LastBarTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendDirectionAndForceIndex(_MQL5Indicator):
    name = 'Trend Direction And Force Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTrendPeriod': 14,  # Trend period
        'inpSmooth': 3.0,  # Smoothing period
        'inpTriggerUp': 0.05,  # Trigger up level
        'inpTriggerDown': -0.05,  # Trigger down level
        'AlertOn': True,  # Alerts On
        'SoundON': True,  # Show Alert Message
        'EmailON': False,  # Send Email Alerts
        'PushNotificationON': False,  # Send Push Notifications
    }

