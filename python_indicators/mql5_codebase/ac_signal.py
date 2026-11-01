"""ac_signal — converted from MQL5: MQL5 Indicators/AC_Signal/ac_signal.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'AC Sell', 2: 'AC Buy'}, 'levels': [], 'description': [''], 'name': 'ac_signal', 'source': 'MQL5 Indicators/AC_Signal/ac_signal.mq5', 'folder': 'AC_Signal', 'inputs': [{'mql': 'InfoComment', 'py': 'InfoComment', 'param': None, 'type': 'string', 'default': 'AC_Signal ', 'label': 'the first part of the message comment', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 1, 'label': 'signal bar index, 0 is a current bar', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'number of alerts', 'sinput': False}, {'mql': 'push', 'py': 'push', 'param': 'push', 'type': 'bool', 'default': True, 'label': 'allow to send push-messages', 'sinput': False}, {'mql': 'email', 'py': 'email', 'param': 'email', 'type': 'bool', 'default': False, 'label': 'allow to send e-mail messages', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InfoComment = _input('InfoComment', 'AC_Signal ')  # the first part of the message comment
SignalBar = _input('SignalBar', 1)  # signal bar index, 0 is a current bar
AlertCount = _input('AlertCount', 0)  # number of alerts
push = _input('push', True)  # allow to send push-messages
email = _input('email', False)  # allow to send e-mail messages
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
AC_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global AC_Handle, ATR_Handle, min_rates_total
    min_rates_total = 33 + 3
    AC_Handle = iAC(Symbol(), PERIOD_CURRENT)
    if AC_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Accelerator Oscillator indicator')
    ATR_Handle = iATR(None, 0, 15)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'AC_Signal'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_DnCount, _s_OnCalculate_DnTime1, _s_OnCalculate_DnTime2, _s_OnCalculate_UpCount, _s_OnCalculate_UpTime1, _s_OnCalculate_UpTime2
    if (BarsCalculated(AC_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    AC = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(AC, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    if CopyBuffer(AC_Handle, 0, 0, limit + 3, AC) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, limit + 1, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if AC[bar + 2] > AC[bar + 1] and AC[bar + 1] < AC[bar]:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        else:
            BuyBuffer[bar] = 0.0
        if AC[bar + 2] < AC[bar + 1] and AC[bar + 1] > AC[bar]:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        else:
            SellBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if rates_total != prev_calculated:
        _s_OnCalculate_UpCount = 0
        _s_OnCalculate_DnCount = 0
    if _s_OnCalculate_UpCount < AlertCount and BuyBuffer[SignalBar]:
        _s_OnCalculate_UpCount += 1
        Alert(InfoComment + Symbol() + GetStringTimeframe(PERIOD_CURRENT) + ': Buy signal ' + Symbol())
    if _s_OnCalculate_DnCount < AlertCount and SellBuffer[SignalBar]:
        _s_OnCalculate_DnCount += 1
        Alert(InfoComment + Symbol() + GetStringTimeframe(PERIOD_CURRENT) + ': Sell signal ' + Symbol())
    if push:
        if BuyBuffer[SignalBar] and _s_OnCalculate_UpTime1 != time[SignalBar]:
            if SendNotification(InfoComment + Symbol() + GetStringTimeframe(PERIOD_CURRENT) + ': Buy signal ' + Symbol()):
                _s_OnCalculate_UpTime1 = time[SignalBar]
        if SellBuffer[SignalBar] and _s_OnCalculate_DnTime1 != time[SignalBar]:
            if SendNotification(InfoComment + Symbol() + GetStringTimeframe(PERIOD_CURRENT) + ': Sell signal ' + Symbol()):
                _s_OnCalculate_DnTime1 = time[SignalBar]
    if email:
        if BuyBuffer[SignalBar] and _s_OnCalculate_UpTime2 != time[SignalBar]:
            text = InfoComment + Symbol() + GetStringTimeframe(PERIOD_CURRENT) + ': Buy signal ' + Symbol()
            if SendMail(text, text):
                _s_OnCalculate_UpTime2 = time[SignalBar]
        if SellBuffer[SignalBar] and _s_OnCalculate_DnTime2 != time[SignalBar]:
            text = InfoComment + Symbol() + GetStringTimeframe(PERIOD_CURRENT) + ': Sell signal ' + Symbol()
            if SendMail(text, text):
                _s_OnCalculate_DnTime2 = time[SignalBar]
    return rates_total

# ---- static local variables
_s_OnCalculate_UpCount = 0
_s_OnCalculate_DnCount = 0
_s_OnCalculate_UpTime1 = 0
_s_OnCalculate_DnTime1 = 0
_s_OnCalculate_UpTime2 = 0
_s_OnCalculate_DnTime2 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AcSignal(_MQL5Indicator):
    name = 'ac_signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SignalBar': 1,  # signal bar index, 0 is a current bar
        'AlertCount': 0,  # number of alerts
        'push': True,  # allow to send push-messages
        'email': False,  # allow to send e-mail messages
    }

