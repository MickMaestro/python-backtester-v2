"""Daily Change Text Alert — converted from MQL5: MQL5 Indicators/Daily Change Text Alert/Daily Change Text Alert.mq5

 
'Daily Change' on last 'Number of bars' candles
Alert if 'Daily Change' limit reached
Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [' ', "'Daily Change' on last 'Number of bars' candles", "Alert if 'Daily Change' limit reached"], 'name': 'Daily Change Text Alert', 'source': 'MQL5 Indicators/Daily Change Text Alert/Daily Change Text Alert.mq5', 'folder': 'Daily Change Text Alert', 'inputs': [{'mql': 'InpCorner', 'py': 'InpCorner', 'param': 'InpCorner', 'type': 'int', 'default': 2, 'label': 'Chart corner for anchoring', 'sinput': False}, {'mql': 'InpFont', 'py': 'InpFont', 'param': None, 'type': 'string', 'default': 'Lucida Console', 'label': 'Font', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'int', 'default': 12, 'label': 'Font size', 'sinput': False}, {'mql': 'InpAnchor', 'py': 'InpAnchor', 'param': 'InpAnchor', 'type': 'int', 'default': 4, 'label': 'Anchor type', 'sinput': False}, {'mql': 'InpNumberOfBars', 'py': 'InpNumberOfBars', 'param': 'InpNumberOfBars', 'type': 'uchar', 'default': 3, 'label': 'Number of bars (do not use "0")', 'sinput': False}, {'mql': 'InpColorBullish', 'py': 'InpColorBullish', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'The color of bullish bars', 'sinput': False}, {'mql': 'InpColorBearish', 'py': 'InpColorBearish', 'param': None, 'type': 'color', 'default': 255, 'label': 'The color of bearish bars', 'sinput': False}, {'mql': 'InpIndent', 'py': 'InpIndent', 'param': 'InpIndent', 'type': 'bool', 'default': True, 'label': 'Indent', 'sinput': False}, {'mql': 'InpDailyLimit', 'py': 'InpDailyLimit', 'param': 'InpDailyLimit', 'type': 'double', 'default': 1.0, 'label': 'Daily Limit Alert', 'sinput': False}, {'mql': 'InpSoundName', 'py': 'InpSoundName', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Sound Name', 'sinput': False}, {'mql': 'InpSoundRepetitions', 'py': 'InpSoundRepetitions', 'param': 'InpSoundRepetitions', 'type': 'uchar', 'default': 3, 'label': 'Repetitions', 'sinput': False}, {'mql': 'InpSoundPause', 'py': 'InpSoundPause', 'param': 'InpSoundPause', 'type': 'uchar', 'default': 3, 'label': 'Pause, in seconds', 'sinput': False}, {'mql': 'InpUseSound', 'py': 'InpUseSound', 'param': 'InpUseSound', 'type': 'bool', 'default': False, 'label': 'Use Sound', 'sinput': False}, {'mql': 'InpAlert', 'py': 'InpAlert', 'param': 'InpAlert', 'type': 'bool', 'default': True, 'label': 'Alert', 'sinput': False}, {'mql': 'InpMail', 'py': 'InpMail', 'param': 'InpMail', 'type': 'bool', 'default': True, 'label': 'Send mail', 'sinput': False}, {'mql': 'InpNotification', 'py': 'InpNotification', 'param': 'InpNotification', 'type': 'bool', 'default': True, 'label': 'Send notification', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpCorner = _input('InpCorner', CORNER_RIGHT_LOWER)  # Chart corner for anchoring
InpFont = _input('InpFont', 'Lucida Console')  # Font
InpFontSize = _input('InpFontSize', 12)  # Font size
InpAnchor = _input('InpAnchor', ANCHOR_RIGHT_LOWER)  # Anchor type
InpNumberOfBars = _input('InpNumberOfBars', 3)  # Number of bars (do not use "0")
InpColorBullish = _input('InpColorBullish', clrBlue)  # The color of bullish bars
InpColorBearish = _input('InpColorBearish', clrRed)  # The color of bearish bars
InpIndent = _input('InpIndent', True)  # Indent
InpDailyLimit = _input('InpDailyLimit', 1.0)  # Daily Limit Alert
InpSoundName = _input('InpSoundName', 'alert.wav')  # Sound Name
InpSoundRepetitions = _input('InpSoundRepetitions', 3)  # Repetitions
InpSoundPause = _input('InpSoundPause', 3)  # Pause, in seconds
InpUseSound = _input('InpUseSound', False)  # Use Sound
InpAlert = _input('InpAlert', True)  # Alert
InpMail = _input('InpMail', True)  # Send mail
InpNotification = _input('InpNotification', True)  # Send notification
m_prefix = 'Daily_Change_Text_'  # prefix for object
m_adjusted_point = 0.0  # point value adjusted for 3 or 5 points
m_arr_names = Arr(0, "")  # array of names of objects OBJ_TEXT
m_last_sound = 0  # "0" -> D'1970.01.01 00:00';
m_repetitions = 0
m_text = ''
m_prev_bars = 0  # "0" -> D'1970.01.01 00:00';
m_init_error = False  # error on InInit

def OnInit():
    global m_adjusted_point, m_init_error, m_prefix
    if InpNumberOfBars == 0:
        Print('"Number of bars"==0. Do not use "0"')
        m_init_error = True
        return INIT_SUCCEEDED
    if Period() != PERIOD_D1:
        Print("Chart timeframe must be 'D1'!")
        m_init_error = True
        return INIT_SUCCEEDED
    m_prefix += EnumToString(Period(), '') + '_'
    digits_adjust = 1
    if Digits() == 3 or Digits() == 5:
        digits_adjust = 10
    m_adjusted_point = Point() * digits_adjust
    ObjectsDeleteAll(0, m_prefix, 0, OBJ_TEXT)
    ResetLastError()
    if ArrayResize(m_arr_names, InpNumberOfBars) == -1:
        Print('OnInit', ' ArrayResize error')
        return INIT_SUCCEEDED
    ArraySetAsSeries(m_arr_names, True)
    for i in range(0, InpNumberOfBars):
        m_arr_names[i] = m_prefix + '_' + IntegerToString(i)
        if not TextCreate(0, m_arr_names[i], 0, 0, 0.0, m_arr_names[i], 90.0, InpFont, InpFontSize, InpColorBearish, ANCHOR_RIGHT):
            ObjectsDeleteAll(0, m_prefix, 0, OBJ_TEXT)
            return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, m_prefix, 0, OBJ_TEXT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global m_last_sound, m_prev_bars, m_repetitions, m_text
    if m_init_error:
        return 0
    if rates_total <= InpNumberOfBars:
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if prev_calculated == 0 or prev_calculated != rates_total:
        limit = ArraySize(m_arr_names) - 1
        for i in range(limit, 0 - 1, -1):
            dc = _fdiv((close[i] - close[i + 1]) * 100.0, close[i + 1])
            text = DoubleToString(dc, 2) + '%'
            if dc > 0:
                if InpIndent:
                    text = ' ' + text
                if not TextMove(0, m_arr_names[i], time[i], high[i]):
                    return 0
                if not TextChange(0, m_arr_names[i], text, ANCHOR_LEFT, InpColorBullish):
                    return 0
            else:
                if InpIndent:
                    text = text + ' '
                if not TextMove(0, m_arr_names[i], time[i], low[i]):
                    return 0
                if not TextChange(0, m_arr_names[i], text, ANCHOR_RIGHT, InpColorBearish):
                    return 0
        return rates_total
    i = 0
    dc = _fdiv((close[i] - close[i + 1]) * 100.0, close[i + 1])
    text = DoubleToString(dc, 2) + '%'
    if dc > 0:
        if InpIndent:
            text = ' ' + text
        if not TextMove(0, m_arr_names[i], time[i], high[i]):
            return 0
        if not TextChange(0, m_arr_names[i], text, ANCHOR_LEFT, InpColorBullish):
            return 0
    else:
        if InpIndent:
            text = text + ' '
        if not TextMove(0, m_arr_names[i], time[i], low[i]):
            return 0
        if not TextChange(0, m_arr_names[i], text, ANCHOR_RIGHT, InpColorBearish):
            return 0
    if time[rates_total - 1] > m_prev_bars:
        m_last_sound = 0
        m_prev_bars = time[rates_total - 1]
        m_repetitions = 0
    if m_repetitions >= InpSoundRepetitions:
        return rates_total
    time_current = TimeCurrent()
    if (time_current - m_last_sound) > InpSoundPause:
        if dc > 0.0 or dc >= InpDailyLimit:
            if InpUseSound:
                PlaySound(InpSoundName)
            m_text = Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' Daily Change UP, ' + TimeToString(time[i])
            if InpAlert:
                Alert(m_text)
            m_last_sound = time_current
            m_repetitions += 1
            if InpMail:
                SendMail(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1), m_text)
            if InpNotification:
                SendNotification(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' ' + m_text)
        elif dc < 0.0 or dc <= (-InpDailyLimit):
            if InpUseSound:
                PlaySound(InpSoundName)
            m_text = Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' Daily Change DOWN, ' + TimeToString(time[i])
            if InpAlert:
                Alert(m_text)
            m_last_sound = time_current
            m_repetitions += 1
            if InpMail:
                SendMail(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1), m_text)
            if InpNotification:
                SendNotification(Symbol() + ',' + StringSubstr(EnumToString(Period(), ''), 7, -1) + ' ' + m_text)
    return rates_total

def TextCreate(chart_ID=0, name='Text', sub_window=0, time=0, price=0.0, text='Text', angle=90.0, font='Lucida Console', font_size=10, clr=clrBlue, anchor=ANCHOR_LEFT, back=False, selection=False, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_TEXT, sub_window, time, price):
        Print('TextCreate', ': failed to create "Text" object! Error code = ', GetLastError())
        return False
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
    ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
    ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
    ObjectSetDouble(chart_ID, name, OBJPROP_ANGLE, angle)
    ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def TextMove(chart_ID=0, name='Text', time=0, price=0.0):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, 0, time, price):
        Print('TextMove', ': failed to move the anchor point! Error code = ', GetLastError())
        return False
    return True

def TextChange(chart_ID=0, name='Text', text='Text', anchor=ANCHOR_LEFT, clr=clrBlue):
    ResetLastError()
    if not ObjectSetString(chart_ID, name, OBJPROP_TEXT, text):
        Print('TextChange', ': failed to change the text! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailyChangeTextAlert(_MQL5Indicator):
    name = 'Daily Change Text Alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=2),  # Chart corner for anchoring
        'InpFontSize': 12,  # Font size
        'InpAnchor': _Choice({0: 'ANCHOR_LEFT_UPPER', 1: 'ANCHOR_LEFT', 2: 'ANCHOR_LEFT_LOWER', 3: 'ANCHOR_LOWER', 4: 'ANCHOR_RIGHT_LOWER', 5: 'ANCHOR_RIGHT', 6: 'ANCHOR_RIGHT_UPPER', 7: 'ANCHOR_UPPER', 8: 'ANCHOR_CENTER'}, default=4),  # Anchor type
        'InpNumberOfBars': 3,  # Number of bars (do not use "0")
        'InpIndent': True,  # Indent
        'InpDailyLimit': 1.0,  # Daily Limit Alert
        'InpSoundRepetitions': 3,  # Repetitions
        'InpSoundPause': 3,  # Pause, in seconds
        'InpUseSound': False,  # Use Sound
        'InpAlert': True,  # Alert
        'InpMail': True,  # Send mail
        'InpNotification': True,  # Send notification
    }

