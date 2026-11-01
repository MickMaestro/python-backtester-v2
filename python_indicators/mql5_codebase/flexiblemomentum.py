"""FlexibleMomentum — converted from MQL5: MQL5 Indicators/Flexible Momentum for MT5/FlexibleMomentum.mq5

Shows price momentum in percentage or points during the last N seconds.
Alerts on above/below a given threshold.
Find More on https://t.me/ForexEaPremium

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'indicator_plots': 0, 'indicator_buffers': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Shows price momentum in percentage or points during the last N seconds.', 'Alerts on above/below a given threshold.', '', 'Find More on https://t.me/ForexEaPremium'], 'name': 'FlexibleMomentum', 'source': 'MQL5 Indicators/Flexible Momentum for MT5/FlexibleMomentum.mq5', 'folder': 'Flexible Momentum for MT5', 'inputs': [{'mql': 'Seconds', 'py': 'Seconds', 'param': 'Seconds', 'type': 'int', 'default': 10, 'label': 'Number of seconds to calculate momentum', 'sinput': False}, {'mql': 'ThresholdPoints', 'py': 'ThresholdPoints', 'param': 'ThresholdPoints', 'type': 'int', 'default': 30, 'label': 'Threshold in points', 'sinput': False}, {'mql': 'ThresholdPercentage', 'py': 'ThresholdPercentage', 'param': 'ThresholdPercentage', 'type': 'double', 'default': 0.02, 'label': 'Threshold in percentage', 'sinput': False}, {'mql': 'DiscardIfOlder', 'py': 'DiscardIfOlder', 'param': 'DiscardIfOlder', 'type': 'int', 'default': 1, 'label': 'Discard calculations if ticks are older than N seconds', 'sinput': False}, {'mql': 'PriceToUse', 'py': 'PriceToUse', 'param': 'PriceToUse', 'type': 'int', 'default': 1, 'label': 'PriceToUse: Which price to use?', 'sinput': False}, {'mql': 'AlertBehaviror', 'py': 'AlertBehaviror', 'param': 'AlertBehaviror', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'AlertTimeLimitForRestricted', 'py': 'AlertTimeLimitForRestricted', 'param': 'AlertTimeLimitForRestricted', 'type': 'int', 'default': 5, 'label': 'Alert time limit till next alert in seconds', 'sinput': False}, {'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'Font_Size', 'py': 'Font_Size', 'param': 'Font_Size', 'type': 'int', 'default': 8, 'label': 'Font size', 'sinput': False}, {'mql': 'Up_Color', 'py': 'Up_Color', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Up color', 'sinput': False}, {'mql': 'Down_Color', 'py': 'Down_Color', 'param': None, 'type': 'color', 'default': 255, 'label': 'Down color', 'sinput': False}, {'mql': 'No_Mvt_Color', 'py': 'No_Mvt_Color', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'No change color', 'sinput': False}, {'mql': 'X_Position_Text', 'py': 'X_Position_Text', 'param': 'X_Position_Text', 'type': 'int', 'default': 21, 'label': 'X distance for text', 'sinput': False}, {'mql': 'Y_Position_Text', 'py': 'Y_Position_Text', 'param': 'Y_Position_Text', 'type': 'int', 'default': 20, 'label': 'Y distance for text', 'sinput': False}, {'mql': 'Corner_Position_Text', 'py': 'Corner_Position_Text', 'param': 'Corner_Position_Text', 'type': 'int', 'default': 1, 'label': 'Text corner', 'sinput': False}, {'mql': 'Text_Object', 'py': 'Text_Object', 'param': None, 'type': 'string', 'default': 'FM_Text', 'label': 'Text object name', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

COPY_TICKS_ALL = 0  # MQL5 constant unknown to the converter

# enum ENUM_ALERT_BEHAVIOR
ENUM_ALERT_BEHAVIOR_NONE = 0
ENUM_ALERT_BEHAVIOR_SINGLE = 1
ENUM_ALERT_BEHAVIOR_CONSTANT = 2
ENUM_ALERT_BEHAVIOR_RESTRICTED = 3
_enum('ENUM_ALERT_BEHAVIOR', {0: 'ENUM_ALERT_BEHAVIOR_NONE', 1: 'ENUM_ALERT_BEHAVIOR_SINGLE', 2: 'ENUM_ALERT_BEHAVIOR_CONSTANT', 3: 'ENUM_ALERT_BEHAVIOR_RESTRICTED'})

# enum ENUM_PRICE
ENUM_PRICE_ASK = 0
ENUM_PRICE_BID = 1
ENUM_PRICE_MIDPRICE = 2
_enum('ENUM_PRICE', {0: 'ENUM_PRICE_ASK', 1: 'ENUM_PRICE_BID', 2: 'ENUM_PRICE_MIDPRICE'})

# ---- inputs and global variables
Seconds = _input('Seconds', 10)  # Number of seconds to calculate momentum
ThresholdPoints = _input('ThresholdPoints', 30)  # Threshold in points
ThresholdPercentage = _input('ThresholdPercentage', 0.02)  # Threshold in percentage
DiscardIfOlder = _input('DiscardIfOlder', 1)  # Discard calculations if ticks are older than N seconds
PriceToUse = _input('PriceToUse', ENUM_PRICE_BID)  # PriceToUse: Which price to use?
AlertBehaviror = _input('AlertBehaviror', ENUM_ALERT_BEHAVIOR_NONE)
AlertTimeLimitForRestricted = _input('AlertTimeLimitForRestricted', 5)  # Alert time limit till next alert in seconds
EnableNativeAlerts = _input('EnableNativeAlerts', False)
EnableEmailAlerts = _input('EnableEmailAlerts', False)
EnablePushAlerts = _input('EnablePushAlerts', False)
Font_Size = _input('Font_Size', 8)  # Font size
Up_Color = _input('Up_Color', clrGreen)  # Up color
Down_Color = _input('Down_Color', clrRed)  # Down color
No_Mvt_Color = _input('No_Mvt_Color', clrBlue)  # No change color
X_Position_Text = _input('X_Position_Text', 21)  # X distance for text
Y_Position_Text = _input('Y_Position_Text', 20)  # Y distance for text
Corner_Position_Text = _input('Corner_Position_Text', CORNER_LEFT_LOWER)  # Text corner
Text_Object = _input('Text_Object', 'FM_Text')  # Text object name

def OnInit():
    if ((AlertBehaviror != ENUM_ALERT_BEHAVIOR_NONE and (not EnableNativeAlerts)) and (not EnableEmailAlerts)) and (not EnablePushAlerts):
        Print("AlertBehaviror is set to issue alerts, but no alret type is enabled. There won't be any alerts.")
    if AlertBehaviror == ENUM_ALERT_BEHAVIOR_NONE and ((EnableNativeAlerts or EnableEmailAlerts) or EnablePushAlerts):
        Print('One or more alert type is enabled, but AlertBehaviror is set to "No alerts". There won\'t be any alerts.')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(ChartID(), Text_Object)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, Time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_not_enough_chart_data, _s_OnCalculate_prev_need_percentage_alert, _s_OnCalculate_prev_need_points_alert, _s_OnCalculate_prev_percentage_alert, _s_OnCalculate_prev_points_alert, _s_OnCalculate_syncing, _s_OnCalculate_waiting_for_ticks
    if iBarShift(Symbol(), Period(), iTime(Symbol(), Period(), 0), True) < 0:
        Print('Syncing...')
        _s_OnCalculate_syncing = True
        return prev_calculated
    if _s_OnCalculate_syncing:
        Print('Synced.')
        _s_OnCalculate_syncing = False
    ticks_array = Arr(0, 0, factory=MqlTick)
    end_time_seconds = _int(TimeCurrent())
    begin_time_ms = _ulong(end_time_seconds - Seconds - DiscardIfOlder) * 1000
    if _idiv(begin_time_ms, 1000) < _ulong(Time[0]):
        Print('Not enough chart data...')
        _s_OnCalculate_not_enough_chart_data = True
        return prev_calculated
    if _s_OnCalculate_not_enough_chart_data:
        Print('Found enough chart data.')
        _s_OnCalculate_not_enough_chart_data = False
    n = _int(CopyTicksRange(Symbol(), ticks_array, COPY_TICKS_ALL, begin_time_ms, _ulong(end_time_seconds) * 1000))
    if n <= 0:
        Print('Waiting for ticks... ')
        _s_OnCalculate_waiting_for_ticks = True
        return prev_calculated
    if _s_OnCalculate_waiting_for_ticks == True:
        Print('Found enough ticks.')
        _s_OnCalculate_waiting_for_ticks = False
    found_i = -1
    for i in range(0, n):
        if ticks_array[i].time > (end_time_seconds - Seconds):
            if i == 0:
                found_i = -1
            elif i > 0:
                found_i = i - 1
            break
        elif ticks_array[i].time == (end_time_seconds - Seconds):
            found_i = i
            break
    text = '???'
    colour = No_Mvt_Color
    distance_points = 0
    distance_percentage = 0.0
    time_ms = 0
    if found_i >= 0:
        price_old = 0.0
        price_current = 0.0
        _sw1 = PriceToUse
        if _sw1 == ENUM_PRICE_BID:
            price_old = ticks_array[found_i].bid
            price_current = SymbolInfoDouble(Symbol(), SYMBOL_BID)
        elif _sw1 == ENUM_PRICE_ASK:
            price_old = ticks_array[found_i].ask
            price_current = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
        elif _sw1 == ENUM_PRICE_MIDPRICE:
            price_old = (ticks_array[found_i].bid + ticks_array[found_i].ask) / 2
            price_current = (SymbolInfoDouble(Symbol(), SYMBOL_BID) + SymbolInfoDouble(Symbol(), SYMBOL_ASK)) / 2
        else:
            price_old = ticks_array[found_i].bid
            price_current = SymbolInfoDouble(Symbol(), SYMBOL_BID)
        time_ms = ticks_array[found_i].time_msc
        distance_points = _int(MathRound(_fdiv(MathAbs(price_current - price_old), Point())))
        distance_percentage = 0.0
        if price_old != 0:
            distance_percentage = _fdiv(MathAbs(price_current - price_old), price_old) * 100
        if ThresholdPoints > 0:
            text = IntegerToString(distance_points) + 'p/' + IntegerToString(ThresholdPoints) + 'p'
        if ThresholdPercentage > 0:
            if text != '':
                text += ', '
            text += DoubleToString(distance_percentage, 2) + '%/' + DoubleToString(ThresholdPercentage, 2) + '%'
        if price_current > price_old:
            colour = Up_Color
        elif price_current < price_old:
            colour = Down_Color
    need_points_alert = False
    need_percentage_alert = False
    need_bigger_font = False
    if ThresholdPoints > 0 and distance_points >= ThresholdPoints:
        need_points_alert = True
    else:
        need_points_alert = False
        _s_OnCalculate_prev_need_points_alert = False
    if ThresholdPercentage > 0 and distance_percentage >= ThresholdPercentage:
        need_percentage_alert = True
    else:
        need_percentage_alert = False
        _s_OnCalculate_prev_need_percentage_alert = False
    if need_points_alert or need_percentage_alert:
        need_bigger_font = True
    if AlertBehaviror == ENUM_ALERT_BEHAVIOR_NONE or (((not EnableEmailAlerts) and (not EnableNativeAlerts)) and (not EnablePushAlerts)):
        need_points_alert = False
        need_percentage_alert = False
    else:
        _sw2 = AlertBehaviror
        if _sw2 == ENUM_ALERT_BEHAVIOR_CONSTANT:
            pass
        elif _sw2 == ENUM_ALERT_BEHAVIOR_SINGLE:
            if _s_OnCalculate_prev_need_points_alert:
                need_points_alert = False
            else:
                _s_OnCalculate_prev_need_points_alert = need_points_alert
            if _s_OnCalculate_prev_need_percentage_alert:
                need_percentage_alert = False
            else:
                _s_OnCalculate_prev_need_percentage_alert = need_percentage_alert
        elif _sw2 == ENUM_ALERT_BEHAVIOR_RESTRICTED:
            if (TimeCurrent() - _s_OnCalculate_prev_points_alert) < AlertTimeLimitForRestricted:
                need_points_alert = False
            else:
                _s_OnCalculate_prev_points_alert = TimeCurrent()
            if (TimeCurrent() - _s_OnCalculate_prev_percentage_alert) < AlertTimeLimitForRestricted:
                need_percentage_alert = False
            else:
                _s_OnCalculate_prev_percentage_alert = TimeCurrent()
        else:
            pass
    font_size = Font_Size
    if need_bigger_font:
        font_size += 4
    ShowObjects(text + ' (' + IntegerToString(Seconds) + 's)', Text_Object, colour, font_size, Corner_Position_Text, X_Position_Text, Y_Position_Text)
    if need_points_alert or need_percentage_alert:
        DoAlerts(need_points_alert, need_percentage_alert, distance_points, distance_percentage, time_ms, colour)
    return rates_total

def ShowObjects(text, text_obj, colour, size, corner_pos_text, x_pos_text, y_pos_text):
    if ObjectFind(0, text_obj) < 0:
        ObjectCreate(0, text_obj, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, text_obj, OBJPROP_CORNER, corner_pos_text)
        ObjectSetInteger(0, text_obj, OBJPROP_XDISTANCE, x_pos_text)
        ObjectSetInteger(0, text_obj, OBJPROP_YDISTANCE, y_pos_text)
        ObjectSetString(0, text_obj, OBJPROP_FONT, 'Verdana')
    ObjectSetInteger(0, text_obj, OBJPROP_COLOR, colour)
    ObjectSetString(0, text_obj, OBJPROP_TEXT, 'Momentum: ' + text)
    ObjectSetInteger(0, text_obj, OBJPROP_FONTSIZE, size)

def DoAlerts(need_points_alert, need_percentage_alert, distance_points, distance_percentage, time_ms, colour):
    direction = ""
    if colour == Up_Color:
        direction = 'Up'
    else:
        direction = 'Down'
    Text = 'Momentum (' + direction + ') of '
    if need_points_alert:
        Text += IntegerToString(distance_points) + 'p over ' + IntegerToString(Seconds) + 's > ' + IntegerToString(ThresholdPoints) + 'p threshold.'
    if need_percentage_alert:
        if need_points_alert:
            Text += ' and '
        Text += DoubleToString(distance_percentage, 2) + '% over ' + IntegerToString(Seconds) + 's > ' + DoubleToString(ThresholdPercentage, 2) + '% threshold.'
    if EnableNativeAlerts:
        Alert(Text)
    if EnableEmailAlerts:
        SendMail('FlexibleMomentum Alert on ' + Symbol(), Symbol() + ', ' + TimeToString(_int(_idiv(time_ms, 1000)), (TIME_DATE | TIME_MINUTES) | TIME_SECONDS) + ':' + StringFormat('%03i', time_ms - (_int(_idiv(time_ms, 1000)) * 1000)) + ' - ' + Text)
    if EnablePushAlerts:
        SendNotification(Symbol() + Text)

# ---- static local variables
_s_OnCalculate_syncing = False
_s_OnCalculate_not_enough_chart_data = False
_s_OnCalculate_waiting_for_ticks = False
_s_OnCalculate_prev_need_points_alert = False
_s_OnCalculate_prev_need_percentage_alert = False
_s_OnCalculate_prev_points_alert = 0
_s_OnCalculate_prev_percentage_alert = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FlexibleMomentum(_MQL5Indicator):
    name = 'FlexibleMomentum'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Seconds': 10,  # Number of seconds to calculate momentum
        'ThresholdPoints': 30,  # Threshold in points
        'ThresholdPercentage': 0.02,  # Threshold in percentage
        'DiscardIfOlder': 1,  # Discard calculations if ticks are older than N seconds
        'PriceToUse': _Choice({0: 'Ask', 1: 'Bid', 2: 'Midprice'}, default=1),  # PriceToUse: Which price to use?
        'AlertBehaviror': _Choice({0: 'No alerts', 1: 'Single alert until next breach', 2: 'Continuous alerts whenever condition is met', 3: 'Alert on condition but with time limit on next alert'}, default=0),
        'AlertTimeLimitForRestricted': 5,  # Alert time limit till next alert in seconds
        'EnableNativeAlerts': False,
        'EnableEmailAlerts': False,
        'EnablePushAlerts': False,
        'Font_Size': 8,  # Font size
        'X_Position_Text': 21,  # X distance for text
        'Y_Position_Text': 20,  # Y distance for text
        'Corner_Position_Text': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # Text corner
    }

