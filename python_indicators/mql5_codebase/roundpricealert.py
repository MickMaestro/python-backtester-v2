"""roundpricealert — converted from MQL5: MQL5 Indicators/RoundPriceAlert/roundpricealert.mq5

Sound signal of rounded price value
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Sound signal of rounded price value'], 'name': 'roundpricealert', 'source': 'MQL5 Indicators/RoundPriceAlert/roundpricealert.mq5', 'folder': 'RoundPriceAlert', 'inputs': [{'mql': 'On_Push', 'py': 'On_Push', 'param': 'On_Push', 'type': 'bool', 'default': False, 'label': 'allow to send push-messages', 'sinput': False}, {'mql': 'On_Email', 'py': 'On_Email', 'param': 'On_Email', 'type': 'bool', 'default': False, 'label': 'allow to send e-mail messages', 'sinput': False}, {'mql': 'On_Alert', 'py': 'On_Alert', 'param': 'On_Alert', 'type': 'bool', 'default': True, 'label': 'allow to put alert', 'sinput': False}, {'mql': 'On_Play_Sound', 'py': 'On_Play_Sound', 'param': 'On_Play_Sound', 'type': 'bool', 'default': False, 'label': 'allow to put sound signal', 'sinput': False}, {'mql': 'NameFileSound', 'py': 'NameFileSound', 'param': None, 'type': 'string', 'default': 'expert.wav', 'label': 'name of the file with sound', 'sinput': False}, {'mql': 'CommentSirName', 'py': 'CommentSirName', 'param': None, 'type': 'string', 'default': 'RoundPriceAlert: ', 'label': 'the first part of the allert comment', 'sinput': False}, {'mql': 'RoundDigits', 'py': 'RoundDigits', 'param': 'RoundDigits', 'type': 'uint', 'default': 3, 'label': 'nuber of zeros in the digits', 'sinput': False}, {'mql': 'SignalPause', 'py': 'SignalPause', 'param': 'SignalPause', 'type': 'uint', 'default': 5, 'label': 'pause between the signals in minutes', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
On_Push = _input('On_Push', False)  # allow to send push-messages
On_Email = _input('On_Email', False)  # allow to send e-mail messages
On_Alert = _input('On_Alert', True)  # allow to put alert
On_Play_Sound = _input('On_Play_Sound', False)  # allow to put sound signal
NameFileSound = _input('NameFileSound', 'expert.wav')  # name of the file with sound
CommentSirName = _input('CommentSirName', 'RoundPriceAlert: ')  # the first part of the allert comment
RoundDigits = _input('RoundDigits', 3)  # nuber of zeros in the digits
SignalPause = _input('SignalPause', 5)  # pause between the signals in minutes
min_rates_total = 0
ratio = 0.0
power = 0.0

def OnInit():
    global min_rates_total, power, ratio
    min_rates_total = 2
    power = MathPow(10, RoundDigits)
    ratio = Point() * power
    shortname = 'RoundPriceAlert'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    Comment(shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_LastRes, _s_OnCalculate_LastSignalTime
    if rates_total < min_rates_total:
        return 0
    SignalTime = TimeCurrent()
    Price = Close[rates_total - 1]
    Res = MathFloor(_fdiv(Price, ratio))
    if prev_calculated > rates_total or prev_calculated <= 0:
        _s_OnCalculate_LastRes = Res
        _s_OnCalculate_LastSignalTime = SignalTime
    dTime = _int(_idiv(SignalTime - _s_OnCalculate_LastSignalTime, 60))
    if _s_OnCalculate_LastRes != Res and dTime > _int(SignalPause):
        if On_Play_Sound:
            PlaySound(NameFileSound)
        comment = Box("")
        sTime = ' CurrTime=' + TimeToString(SignalTime, TIME_MINUTES)
        StringConcatenate(comment, CommentSirName, Symbol(), sTime, ' The price breakthrough the level ', DoubleToString(Res * ratio, Digits()), '!')
        if On_Alert:
            Alert(comment.v)
        if On_Push:
            SendNotification(comment.v)
        if On_Email:
            SendMail(CommentSirName + Symbol(), comment.v)
        _s_OnCalculate_LastSignalTime = SignalTime
        _s_OnCalculate_LastRes = Res
    return rates_total

# ---- static local variables
_s_OnCalculate_LastRes = 0.0
_s_OnCalculate_LastSignalTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Roundpricealert(_MQL5Indicator):
    name = 'roundpricealert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'On_Push': False,  # allow to send push-messages
        'On_Email': False,  # allow to send e-mail messages
        'On_Alert': True,  # allow to put alert
        'On_Play_Sound': False,  # allow to put sound signal
        'RoundDigits': 3,  # nuber of zeros in the digits
        'SignalPause': 5,  # pause between the signals in minutes
    }

