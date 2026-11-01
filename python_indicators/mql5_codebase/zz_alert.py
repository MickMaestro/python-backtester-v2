"""ZZ_Alert — converted from MQL5: MQL5 Indicators/ZigZag NK Sound Alerts on Bar Change/ZZ_Alert.mq5

Copyright: Copyright 2021, Dark Ryd3r; Link: https://t.me/DarkRyd3r; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, Dark Ryd3r', 'link': 'https://t.me/DarkRyd3r', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 13}, 'colors': {1: [16711935, 16775408]}, 'widths': {1: 1}, 'styles': {1: 1}, 'labels': {1: 'ZigZag_NK'}, 'levels': [], 'description': [], 'name': 'ZZ_Alert', 'source': 'MQL5 Indicators/ZigZag NK Sound Alerts on Bar Change/ZZ_Alert.mq5', 'folder': 'ZigZag NK Sound Alerts on Bar Change', 'inputs': [{'mql': 'sound', 'py': 'sound', 'param': 'sound', 'type': 'int', 'default': 1, 'label': 'Choose Sound', 'sinput': False}, {'mql': '_sound', 'py': '_sound', 'param': '_sound', 'type': 'bool', 'default': True, 'label': 'Play Sound?', 'sinput': False}, {'mql': '_alert', 'py': '_alert', 'param': '_alert', 'type': 'bool', 'default': True, 'label': 'Show Alerts?', 'sinput': False}, {'mql': 'notification', 'py': 'notification', 'param': 'notification', 'type': 'bool', 'default': False, 'label': 'Send Push Notificatoin?', 'sinput': False}, {'mql': 'InpText', 'py': 'InpText', 'param': None, 'type': 'string', 'default': 'ZZ Bar Changed ', 'label': 'Enter Alert Text', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_SOUNDS
alert = 0
alert2 = 1
connect = 2
disconnect = 3
email = 4
expert = 5
news = 6
ok = 7
request = 8
stops = 9
tick = 10
timeout = 11
wait = 12
_enum('ENUM_SOUNDS', {0: 'alert', 1: 'alert2', 2: 'connect', 3: 'disconnect', 4: 'email', 5: 'expert', 6: 'news', 7: 'ok', 8: 'request', 9: 'stops', 10: 'tick', 11: 'timeout', 12: 'wait'})

# ---- inputs and global variables
sound = _input('sound', alert2)  # Choose Sound
_sound = _input('_sound', True)  # Play Sound?
_alert = _input('_alert', True)  # Show Alerts?
notification = _input('notification', False)  # Send Push Notificatoin?
filename = ''
InpText = _input('InpText', 'ZZ Bar Changed ')  # Enter Alert Text
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
bar1 = 0
bar2 = 0
sign = 0
price1 = 0.0
price2 = 0.0
HighestBuffer = Arr(0, 0.0)
LowestBuffer = Arr(0, 0.0)
LASTlowpos = 0
LASThighpos = 0
LASTlow0 = 0.0
LASTlow1 = 0.0
LASThigh0 = 0.0
LASThigh1 = 0.0
StartBars = 0

def OnInit():
    global StartBars, filename
    _sw1 = sound
    if _sw1 == 0:
        filename = 'alert.wav'
    elif _sw1 == 1:
        filename = 'alert2.wav'
    elif _sw1 == 2:
        filename = 'connect .wav'
    elif _sw1 == 3:
        filename = 'disconnect.wav'
    elif _sw1 == 4:
        filename = 'email.wav'
    elif _sw1 == 5:
        filename = 'expert.wav'
    elif _sw1 == 6:
        filename = 'news.wav'
    elif _sw1 == 7:
        filename = 'ok.wav'
    elif _sw1 == 8:
        filename = 'request.wav'
    elif _sw1 == 9:
        filename = 'stops.wav'
    elif _sw1 == 10:
        filename = 'tick.wav'
    elif _sw1 == 11:
        filename = 'timeout.wav'
    elif _sw1 == 12:
        filename = 'wait.wav'
    StartBars = ExtDepth + ExtBackstep
    SetIndexBuffer(0, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighestBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetString(0, PLOT_LABEL, 'ZigZag Lowest')
    PlotIndexSetString(1, PLOT_LABEL, 'ZigZag Highest')
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'ZZ_Alert (ExtDepth=', ExtDepth, 'ExtDeviation = ', ExtDeviation, 'ExtBackstep = ', ExtBackstep, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LASThigh0, LASThigh1, LASThighpos, LASTlow0, LASTlow1, LASTlowpos, _s_OnCalculate__price2, bar1, bar2
    if rates_total < StartBars:
        return 0
    limit = 0
    bar = 0
    back = 0
    lasthighpos = 0
    lastlowpos = 0
    curlow = 0.0
    curhigh = 0.0
    lasthigh0 = 0.0
    lastlow0 = 0.0
    lasthigh1 = 0.0
    lastlow1 = 0.0
    val = 0.0
    res = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars
        lastlow1 = -1.0
        lasthigh1 = -1.0
        lastlowpos = -1
        lasthighpos = -1
    else:
        limit = rates_total - prev_calculated
        lastlow0 = LASTlow0
        lasthigh0 = LASThigh0
        lastlow1 = LASTlow1
        lasthigh1 = LASThigh1
        lastlowpos = LASTlowpos + limit
        lasthighpos = LASThighpos + limit
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            LASTlow0 = lastlow0
            LASThigh0 = lasthigh0
        val = low[ArrayMinimum(low, bar, ExtDepth)]
        if val == lastlow0:
            val = 0.0
        else:
            lastlow0 = val
            if (low[bar] - val) > (ExtDeviation * Point()):
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = LowestBuffer[bar + back]
                    if res != 0 and res > val:
                        LowestBuffer[bar + back] = 0.0
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        LowestBuffer[bar] = val
        val = high[ArrayMaximum(high, bar, ExtDepth)]
        if val == lasthigh0:
            val = 0.0
        else:
            lasthigh0 = val
            if (val - high[bar]) > (ExtDeviation * Point()):
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = HighestBuffer[bar + back]
                    if res != 0 and res < val:
                        HighestBuffer[bar + back] = 0.0
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        HighestBuffer[bar] = val
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            LASTlow1 = lastlow1
            LASThigh1 = lasthigh1
            LASTlowpos = lastlowpos
            LASThighpos = lasthighpos
        curlow = LowestBuffer[bar]
        curhigh = HighestBuffer[bar]
        if curlow == 0 and curhigh == 0:
            continue
        if curhigh != 0:
            if lasthigh1 > 0:
                if lasthigh1 < curhigh:
                    HighestBuffer[lasthighpos] = 0.0
                else:
                    HighestBuffer[bar] = 0.0
            if lasthigh1 < curhigh or lasthigh1 < 0:
                lasthigh1 = curhigh
                lasthighpos = bar
            lastlow1 = -1.0
        if curlow != 0:
            if lastlow1 > 0:
                if lastlow1 > curlow:
                    LowestBuffer[lastlowpos] = 0.0
                else:
                    LowestBuffer[bar] = 0.0
            if curlow < lastlow1 or lastlow1 < 0:
                lastlow1 = curlow
                lastlowpos = bar
            lasthigh1 = -1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar1 = FindFirstExtremum(0, rates_total, HighestBuffer, LowestBuffer, _GlobRef(globals(), 'sign'), _GlobRef(globals(), 'price1'))
    bar2 = FindSecondExtremum(sign, bar1, rates_total, HighestBuffer, LowestBuffer, _GlobRef(globals(), 'sign'), _GlobRef(globals(), 'price2'))
    now = TimeToString(TimeLocal(), TIME_SECONDS)
    if _s_OnCalculate__price2 is _UNSET:
        _s_OnCalculate__price2 = price2
    if price2 != _s_OnCalculate__price2:
        if _sound:
            PlaySound(filename)
        if _alert:
            Alert(InpText)
        if notification:
            text = Symbol() + ': ' + InpText + ' at ' + now
            SendNotification(text)
        _s_OnCalculate__price2 = price2
    return rates_total

def FindFirstExtremum(StartPos, Rates_total, UpArray, DnArray, Sign, Extremum):
    if StartPos >= Rates_total:
        StartPos = Rates_total - 1
    for bar in range(StartPos, Rates_total):
        if UpArray[bar] != 0.0 and UpArray[bar] != EMPTY_VALUE:
            Sign.v = 1
            Extremum.v = UpArray[bar]
            return bar
            break
        if DnArray[bar] != 0.0 and DnArray[bar] != EMPTY_VALUE:
            Sign.v = -1
            Extremum.v = DnArray[bar]
            return bar
            break
    return -1

def FindSecondExtremum(Direct, StartPos, Rates_total, UpArray, DnArray, Sign, Extremum):
    if StartPos >= Rates_total:
        StartPos = Rates_total - 1
    if Direct == -1:
        for bar in range(StartPos, Rates_total):
            if UpArray[bar] != 0.0 and UpArray[bar] != EMPTY_VALUE:
                Sign.v = 1
                Extremum.v = UpArray[bar]
                return bar
                break
    if Direct == 1:
        for bar in range(StartPos, Rates_total):
            if DnArray[bar] != 0.0 and DnArray[bar] != EMPTY_VALUE:
                Sign.v = -1
                Extremum.v = DnArray[bar]
                return bar
                break
    return -1

# ---- static local variables
_s_OnCalculate__price2 = _UNSET


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZZAlert(_MQL5Indicator):
    name = 'ZZ_Alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'sound': _Choice({0: 'alert', 1: 'alert2', 2: 'connect', 3: 'disconnect', 4: 'email', 5: 'expert', 6: 'news', 7: 'ok', 8: 'request', 9: 'stops', 10: 'tick', 11: 'timeout', 12: 'wait'}, default=1),  # Choose Sound
        '_sound': True,  # Play Sound?
        '_alert': True,  # Show Alerts?
        'notification': False,  # Send Push Notificatoin?
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
    }

