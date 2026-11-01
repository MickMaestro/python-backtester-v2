"""RoundLevels — converted from MQL5: MQL5 Indicators/Round Levels MT5/RoundLevels.mq5

Generates round level zone background shading on chart.
Copyright: https://t.me/ForexEaPremium; Link: https://t.me/ForexEaPremium; Version: 1.03

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://t.me/ForexEaPremium', 'link': 'https://t.me/ForexEaPremium', 'version': '1.03', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Generates round level zone background shading on chart.'], 'name': 'RoundLevels', 'source': 'MQL5 Indicators/Round Levels MT5/RoundLevels.mq5', 'folder': 'Round Levels MT5', 'inputs': [{'mql': 'Levels', 'py': 'Levels', 'param': 'Levels', 'type': 'int', 'default': 5, 'label': 'Levels - number of level zones in each direction.', 'sinput': False}, {'mql': 'Interval', 'py': 'Interval', 'param': 'Interval', 'type': 'int', 'default': 50, 'label': 'Interval between zones in points.', 'sinput': False}, {'mql': 'ZoneWidth', 'py': 'ZoneWidth', 'param': 'ZoneWidth', 'type': 'int', 'default': 10, 'label': 'Zone width in points.', 'sinput': False}, {'mql': 'ColorUp', 'py': 'ColorUp', 'param': None, 'type': 'color', 'default': 2237106, 'label': '', 'sinput': False}, {'mql': 'ColorDn', 'py': 'ColorDn', 'param': None, 'type': 'color', 'default': 25600, 'label': '', 'sinput': False}, {'mql': 'InvertZones', 'py': 'InvertZones', 'param': 'InvertZones', 'type': 'bool', 'default': False, 'label': 'Invert zones to shade the areas between round numbers.', 'sinput': False}, {'mql': 'ZonesAsBackground', 'py': 'ZonesAsBackground', 'param': 'ZonesAsBackground', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'DrawLines', 'py': 'DrawLines', 'param': 'DrawLines', 'type': 'bool', 'default': False, 'label': 'Draw lines on levels.', 'sinput': False}, {'mql': 'LineColor', 'py': 'LineColor', 'param': None, 'type': 'color', 'default': 11119017, 'label': '', 'sinput': False}, {'mql': 'LineWidth', 'py': 'LineWidth', 'param': 'LineWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'LineStyle', 'py': 'LineStyle', 'param': 'LineStyle', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'LinesAsBackground', 'py': 'LinesAsBackground', 'param': 'LinesAsBackground', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'ShowLineLabels', 'py': 'ShowLineLabels', 'param': 'ShowLineLabels', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'LineLabelColor', 'py': 'LineLabelColor', 'param': None, 'type': 'color', 'default': 16777215, 'label': '', 'sinput': False}, {'mql': 'ObjectPrefix', 'py': 'ObjectPrefix', 'param': None, 'type': 'string', 'default': 'RoundLevels', 'label': '', 'sinput': False}, {'mql': 'Comment_1', 'py': 'Comment_1', 'param': None, 'type': 'string', 'default': '=======================', 'label': 'Notification Options', 'sinput': False}, {'mql': 'EnableNotify', 'py': 'EnableNotify', 'param': 'EnableNotify', 'type': 'bool', 'default': False, 'label': 'Enable Notifications Feature', 'sinput': False}, {'mql': 'SendAlert', 'py': 'SendAlert', 'param': 'SendAlert', 'type': 'bool', 'default': True, 'label': 'Send Alert Notification', 'sinput': False}, {'mql': 'SendApp', 'py': 'SendApp', 'param': 'SendApp', 'type': 'bool', 'default': False, 'label': 'Send Notification to Mobile', 'sinput': False}, {'mql': 'SendEmail', 'py': 'SendEmail', 'param': 'SendEmail', 'type': 'bool', 'default': False, 'label': 'Send Notification via Email', 'sinput': False}, {'mql': 'AlertDelay', 'py': 'AlertDelay', 'param': 'AlertDelay', 'type': 'int', 'default': 5, 'label': 'Alert Delay, seconds', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum direction
Up = 0
Down = 1
_enum('direction', {0: 'Up', 1: 'Down'})

# ---- inputs and global variables
Levels = _input('Levels', 5)  # Levels - number of level zones in each direction.
Interval = _input('Interval', 50)  # Interval between zones in points.
ZoneWidth = _input('ZoneWidth', 10)  # Zone width in points.
ColorUp = _input('ColorUp', clrFireBrick)
ColorDn = _input('ColorDn', clrDarkGreen)
InvertZones = _input('InvertZones', False)  # Invert zones to shade the areas between round numbers.
ZonesAsBackground = _input('ZonesAsBackground', True)
DrawLines = _input('DrawLines', False)  # Draw lines on levels.
LineColor = _input('LineColor', clrDarkGray)
LineWidth = _input('LineWidth', 1)
LineStyle = _input('LineStyle', STYLE_DASHDOT)
LinesAsBackground = _input('LinesAsBackground', False)
ShowLineLabels = _input('ShowLineLabels', False)
LineLabelColor = _input('LineLabelColor', clrWhite)
ObjectPrefix = _input('ObjectPrefix', 'RoundLevels')
Comment_1 = _input('Comment_1', '=======================')  # Notification Options
EnableNotify = _input('EnableNotify', False)  # Enable Notifications Feature
SendAlert = _input('SendAlert', True)  # Send Alert Notification
SendApp = _input('SendApp', False)  # Send Notification to Mobile
SendEmail = _input('SendEmail', False)  # Send Notification via Email
AlertDelay = _input('AlertDelay', 5)  # Alert Delay, seconds
LastNotificationTime = 0

def OnInit():
    global LastNotificationTime
    LastNotificationTime = TimeCurrent()

def OnDeinit(reason):
    ObjectsDeleteAll(0, ObjectPrefix)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    starting_price = NormalizeDouble(SymbolInfoDouble(Symbol(), SYMBOL_BID), Digits())
    for i in range(0, Levels):
        lvl_down = FindNextLevel(NormalizeDouble(starting_price - (i * Interval * Point()), Digits()), Down)
        lvl_up = FindNextLevel(NormalizeDouble(starting_price + (i * Interval * Point()), Digits()), Up)
        name = ObjectPrefix + 'D' + IntegerToString(i)
        price1 = 0.0
        price2 = 0.0
        if InvertZones:
            price1 = lvl_down - (_idiv(ZoneWidth, 2) * Point())
            price2 = lvl_down - ((Interval - _idiv(ZoneWidth, 2)) * Point())
        else:
            price1 = lvl_down + (_idiv(ZoneWidth, 2) * Point())
            price2 = lvl_down - (_idiv(ZoneWidth, 2) * Point())
        DrawRectangle(name, price1, price2, ColorDn)
        name = ObjectPrefix + 'LD' + IntegerToString(i)
        if DrawLines:
            DrawLine(name, lvl_down)
        Notify(price1, price2)
        name = ObjectPrefix + 'U' + IntegerToString(i)
        if InvertZones:
            price1 = lvl_up + ((Interval - _idiv(ZoneWidth, 2)) * Point())
            price2 = lvl_up + (_idiv(ZoneWidth, 2) * Point())
        else:
            price1 = lvl_up + (_idiv(ZoneWidth, 2) * Point())
            price2 = lvl_up - (_idiv(ZoneWidth, 2) * Point())
        DrawRectangle(name, price1, price2, ColorUp)
        name = ObjectPrefix + 'LU' + IntegerToString(i)
        if DrawLines:
            DrawLine(name, lvl_up)
        Notify(price1, price2)
    if InvertZones:
        lvl_down = FindNextLevel(NormalizeDouble(starting_price, Digits()), Down)
        lvl_up = FindNextLevel(NormalizeDouble(starting_price, Digits()), Up)
        name = ObjectPrefix + 'C'
        price1 = lvl_up - (_idiv(ZoneWidth, 2) * Point())
        price2 = lvl_down + (_idiv(ZoneWidth, 2) * Point())
        DrawRectangle(name, price1, price2, _idiv(ColorDn + ColorUp, 2))
        Notify(price1, price2)
    return 0

def FindNextLevel(sp, dir):
    multiplier = MathPow(10, Digits())
    integer_price = _int(MathRound(sp * MathPow(10, Digits())))
    distance = _imod(integer_price, Interval)
    if dir == Down:
        return NormalizeDouble(_fdiv(MathRound(integer_price - distance), multiplier), Digits())
    elif dir == Up:
        return NormalizeDouble(_fdiv(integer_price + (Interval - distance), multiplier), Digits())
    return EMPTY_VALUE

def DrawRectangle(name, price1, price2, colour):
    if ObjectFind(0, name) < 0:
        ObjectCreate(0, name, OBJ_RECTANGLE, 0, 0, 0)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price1)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price2)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_TIME, 1, 32535129600)
    ObjectSetInteger(0, name, OBJPROP_COLOR, colour)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_BACK, ZonesAsBackground)
    ObjectSetInteger(0, name, OBJPROP_FILL, True)
    if (not DrawLines) and ShowLineLabels:
        DrawLineLabel(name + '_LL', (price1 + price2) / 2)

def DrawLine(name, price):
    if ObjectFind(0, name) < 0:
        ObjectCreate(0, name, OBJ_HLINE, 0, 0, 0)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price)
    ObjectSetInteger(0, name, OBJPROP_COLOR, LineColor)
    ObjectSetInteger(0, name, OBJPROP_STYLE, LineStyle)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, LineWidth)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_BACK, LinesAsBackground)
    if ShowLineLabels:
        DrawLineLabel(name + '_LL', price)

def DrawLineLabel(name, price):
    if ObjectFind(0, name) < 0:
        ObjectCreate(0, name, OBJ_ARROW_RIGHT_PRICE, 0, 0, 0)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, iTime(Symbol(), Period(), 0))
    ObjectSetInteger(0, name, OBJPROP_COLOR, LineLabelColor)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, LineWidth)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_BACK, False)

def Notify(price1, price2):
    global LastNotificationTime
    if (not EnableNotify) or (((not SendAlert) and (not SendApp)) and (not SendEmail)):
        return
    if (TimeCurrent() - LastNotificationTime) < AlertDelay:
        return
    if SymbolInfoDouble(Symbol(), SYMBOL_BID) > MathMax(price2, price1) or SymbolInfoDouble(Symbol(), SYMBOL_BID) < MathMin(price2, price1):
        return
    EmailSubject = 'RoundLevels ' + Symbol() + ' Notification'
    EmailBody = AccountInfoString(ACCOUNT_COMPANY) + ' - ' + AccountInfoString(ACCOUNT_NAME) + ' - ' + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) + '\r\nRoundLevels Notification for ' + Symbol() + ' @ ' + EnumToString(Period(), 'ENUM_TIMEFRAMES') + '\r\n'
    AlertText = ''
    AppText = AccountInfoString(ACCOUNT_COMPANY) + ' - ' + AccountInfoString(ACCOUNT_NAME) + ' - ' + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) + ' - RoundLevels - ' + Symbol() + ' @ ' + EnumToString(Period(), 'ENUM_TIMEFRAMES') + ' - '
    Text = 'Bid Price (' + DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_BID), Digits()) + ') inside a Zone (' + DoubleToString(price2, Digits()) + '-' + DoubleToString(price1, Digits()) + ')'
    EmailBody += Text
    AlertText += Text
    AppText += Text
    if SendAlert:
        Alert(AlertText)
    if SendEmail:
        if not SendMail(EmailSubject, EmailBody):
            Print('Error sending email ' + IntegerToString(GetLastError()))
    if SendApp:
        if not SendNotification(AppText):
            Print('Error sending notification ' + IntegerToString(GetLastError()))
    LastNotificationTime = TimeCurrent()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RoundLevels(_MQL5Indicator):
    name = 'RoundLevels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Levels': 5,  # Levels - number of level zones in each direction.
        'Interval': 50,  # Interval between zones in points.
        'ZoneWidth': 10,  # Zone width in points.
        'InvertZones': False,  # Invert zones to shade the areas between round numbers.
        'ZonesAsBackground': True,
        'DrawLines': False,  # Draw lines on levels.
        'LineWidth': 1,
        'LineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=3),
        'LinesAsBackground': False,
        'ShowLineLabels': False,
        'EnableNotify': False,  # Enable Notifications Feature
        'SendAlert': True,  # Send Alert Notification
        'SendApp': False,  # Send Notification to Mobile
        'SendEmail': False,  # Send Notification via Email
        'AlertDelay': 5,  # Alert Delay, seconds
    }

