"""CandleWicksDisplay — converted from MQL5: MQL5 Indicators/Candle Wicks Length Display Indicator MT5/CandleWicksDisplay.mq5

Displays the candle wicks' length above and below the candles.
Alerts when the candle's wick (shadow) reaches a certain length.
You can choose whether to use pips or %.
Email settings are under Tools->Options->Email.
Notifications settings are under Tools->Options->Notifications.

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ["Displays the candle wicks' length above and below the candles.", "Alerts when the candle's wick (shadow) reaches a certain length.", 'You can choose whether to use pips or %.', 'Email settings are under Tools->Options->Email.', 'Notifications settings are under Tools->Options->Notifications.'], 'name': 'CandleWicksDisplay', 'source': 'MQL5 Indicators/Candle Wicks Length Display Indicator MT5/CandleWicksDisplay.mq5', 'folder': 'Candle Wicks Length Display Indicator MT5', 'inputs': [{'mql': 'Units', 'py': 'Units', 'param': 'Units', 'type': 'int', 'default': 0, 'label': 'Standard pips or percentage points.', 'sinput': False}, {'mql': 'DisplayWickLimit', 'py': 'DisplayWickLimit', 'param': 'DisplayWickLimit', 'type': 'int', 'default': 5, 'label': 'DisplayWickLimit in standard pips or %.', 'sinput': False}, {'mql': 'DisplayHighWickColorBullish', 'py': 'DisplayHighWickColorBullish', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'DisplayHighWickColorBearish', 'py': 'DisplayHighWickColorBearish', 'param': None, 'type': 'color', 'default': 2237106, 'label': '', 'sinput': False}, {'mql': 'DisplayLowWickColorBullish', 'py': 'DisplayLowWickColorBullish', 'param': None, 'type': 'color', 'default': 3329330, 'label': '', 'sinput': False}, {'mql': 'DisplayLowWickColorBearish', 'py': 'DisplayLowWickColorBearish', 'param': None, 'type': 'color', 'default': 32768, 'label': '', 'sinput': False}, {'mql': 'UpperWickLimit', 'py': 'UpperWickLimit', 'param': 'UpperWickLimit', 'type': 'int', 'default': 10, 'label': 'UpperWickLimit in broker pips or % for alerts.', 'sinput': False}, {'mql': 'LowerWickLimit', 'py': 'LowerWickLimit', 'param': 'LowerWickLimit', 'type': 'int', 'default': 10, 'label': 'LowerWickLimit in broker pips or % for alerts.', 'sinput': False}, {'mql': 'WaitForClose', 'py': 'WaitForClose', 'param': 'WaitForClose', 'type': 'bool', 'default': True, 'label': "WaitForClose - Wait for a candle to close before checking wicks' length?", 'sinput': False}, {'mql': 'TopBottomPercent', 'py': 'TopBottomPercent', 'param': 'TopBottomPercent', 'type': 'int', 'default': 0, 'label': 'TopBottomPercent: Body within top/bottom percentage part.', 'sinput': False}, {'mql': 'LessThan', 'py': 'LessThan', 'param': 'LessThan', 'type': 'bool', 'default': False, 'label': 'LessThan: display wicks lower than DisplayWickLimit.', 'sinput': False}, {'mql': 'SoundAlert', 'py': 'SoundAlert', 'param': 'SoundAlert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'VisualAlert', 'py': 'VisualAlert', 'param': 'VisualAlert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EmailAlert', 'py': 'EmailAlert', 'param': 'EmailAlert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'NotificationAlert', 'py': 'NotificationAlert', 'param': 'NotificationAlert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertOnLimit', 'py': 'AlertOnLimit', 'param': 'AlertOnLimit', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertOnEqualTopBottomWicks', 'py': 'AlertOnEqualTopBottomWicks', 'param': 'AlertOnEqualTopBottomWicks', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'IgnoreAlertsOnFirstRun', 'py': 'IgnoreAlertsOnFirstRun', 'param': 'IgnoreAlertsOnFirstRun', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'FontFace', 'py': 'FontFace', 'param': None, 'type': 'string', 'default': 'Verdana', 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'MaxCandles', 'py': 'MaxCandles', 'param': 'MaxCandles', 'type': 'int', 'default': 500, 'label': '', 'sinput': False}, {'mql': 'UseRawPips', 'py': 'UseRawPips', 'param': 'UseRawPips', 'type': 'bool', 'default': False, 'label': 'UseRawPips: if true, will use points instead of pips.', 'sinput': False}, {'mql': 'ShowAverageWickSize', 'py': 'ShowAverageWickSize', 'param': 'ShowAverageWickSize', 'type': 'bool', 'default': False, 'label': 'Show average wick size', 'sinput': False}, {'mql': 'AvgCandles', 'py': 'AvgCandles', 'param': 'AvgCandles', 'type': 'int', 'default': 50, 'label': 'AvgBars: how many candles to calculate the average for.', 'sinput': False}, {'mql': 'AverageWickSizeColor', 'py': 'AverageWickSizeColor', 'param': None, 'type': 'color', 'default': 13882323, 'label': '', 'sinput': False}, {'mql': 'Corner', 'py': 'Corner', 'param': 'Corner', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Distance_X', 'py': 'Distance_X', 'param': 'Distance_X', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Distance_Y', 'py': 'Distance_Y', 'param': 'Distance_Y', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'DrawTextAsBackground', 'py': 'DrawTextAsBackground', 'param': 'DrawTextAsBackground', 'type': 'bool', 'default': False, 'label': 'DrawTextAsBackground: if true, the text will be drawn as background.', 'sinput': False}, {'mql': 'RemoveOldLabels', 'py': 'RemoveOldLabels', 'param': 'RemoveOldLabels', 'type': 'bool', 'default': False, 'label': 'RemoveOldLabels: Delete labels beyond MaxCandles?', 'sinput': False}, {'mql': 'ObjectPrefix', 'py': 'ObjectPrefix', 'param': None, 'type': 'string', 'default': 'CWLD-', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum PipsPerc
Pips = 0
Percentage = 1
_enum('PipsPerc', {0: 'Pips', 1: 'Percentage'})

# ---- inputs and global variables
Units = _input('Units', Pips)  # Standard pips or percentage points.
DisplayWickLimit = _input('DisplayWickLimit', 5)  # DisplayWickLimit in standard pips or %.
DisplayHighWickColorBullish = _input('DisplayHighWickColorBullish', clrRed)
DisplayHighWickColorBearish = _input('DisplayHighWickColorBearish', clrFireBrick)
DisplayLowWickColorBullish = _input('DisplayLowWickColorBullish', clrLimeGreen)
DisplayLowWickColorBearish = _input('DisplayLowWickColorBearish', clrGreen)
UpperWickLimit = _input('UpperWickLimit', 10)  # UpperWickLimit in broker pips or % for alerts.
LowerWickLimit = _input('LowerWickLimit', 10)  # LowerWickLimit in broker pips or % for alerts.
WaitForClose = _input('WaitForClose', True)  # WaitForClose - Wait for a candle to close before checking wicks' length?
TopBottomPercent = _input('TopBottomPercent', 0)  # TopBottomPercent: Body within top/bottom percentage part.
LessThan = _input('LessThan', False)  # LessThan: display wicks lower than DisplayWickLimit.
SoundAlert = _input('SoundAlert', False)
VisualAlert = _input('VisualAlert', False)
EmailAlert = _input('EmailAlert', False)
NotificationAlert = _input('NotificationAlert', False)
AlertOnLimit = _input('AlertOnLimit', False)
AlertOnEqualTopBottomWicks = _input('AlertOnEqualTopBottomWicks', False)
IgnoreAlertsOnFirstRun = _input('IgnoreAlertsOnFirstRun', True)
FontFace = _input('FontFace', 'Verdana')
FontSize = _input('FontSize', 10)
MaxCandles = _input('MaxCandles', 500)
UseRawPips = _input('UseRawPips', False)  # UseRawPips: if true, will use points instead of pips.
ShowAverageWickSize = _input('ShowAverageWickSize', False)  # Show average wick size
AvgCandles = _input('AvgCandles', 50)  # AvgBars: how many candles to calculate the average for.
AverageWickSizeColor = _input('AverageWickSizeColor', clrLightGray)
Corner = _input('Corner', CORNER_LEFT_UPPER)
Distance_X = _input('Distance_X', 3)
Distance_Y = _input('Distance_Y', 12)
DrawTextAsBackground = _input('DrawTextAsBackground', False)  # DrawTextAsBackground: if true, the text will be drawn as background.
RemoveOldLabels = _input('RemoveOldLabels', False)  # RemoveOldLabels: Delete labels beyond MaxCandles?
ObjectPrefix = _input('ObjectPrefix', 'CWLD-')
AlertDone = 0  # Time of the bar of the last alert.
Poin = 0.0  # Traditional point value.
CanDoAlerts = False  # Fuse to prevent alerts on initialization or timeframe change.

def OnInit():
    global CanDoAlerts, Poin
    if ShowAverageWickSize:
        ObjectCreate(ChartID(), ObjectPrefix + 'Upper', OBJ_LABEL, 0, 0, 0)
        ObjectSetString(ChartID(), ObjectPrefix + 'Upper', OBJPROP_TEXT, '')
        ObjectSetInteger(ChartID(), ObjectPrefix + 'Upper', OBJPROP_FONTSIZE, FontSize)
        ObjectSetString(ChartID(), ObjectPrefix + 'Upper', OBJPROP_FONT, FontFace)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'Upper', OBJPROP_COLOR, AverageWickSizeColor)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'Upper', OBJPROP_CORNER, Corner)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'Upper', OBJPROP_XDISTANCE, Distance_X)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'Upper', OBJPROP_YDISTANCE, Distance_Y)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'Upper', OBJPROP_BACK, DrawTextAsBackground)
        ObjectCreate(ChartID(), ObjectPrefix + 'Lower', OBJ_LABEL, 0, 0, 0)
        ObjectSetString(ChartID(), ObjectPrefix + 'Lower', OBJPROP_TEXT, '')
        ObjectSetInteger(ChartID(), ObjectPrefix + 'Lower', OBJPROP_FONTSIZE, FontSize)
        ObjectSetString(ChartID(), ObjectPrefix + 'Lower', OBJPROP_FONT, FontFace)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'Lower', OBJPROP_COLOR, AverageWickSizeColor)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'Lower', OBJPROP_CORNER, Corner)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'Lower', OBJPROP_XDISTANCE, Distance_X)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'Lower', OBJPROP_YDISTANCE, Distance_Y + 12)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'Lower', OBJPROP_BACK, DrawTextAsBackground)
        ObjectCreate(ChartID(), ObjectPrefix + 'All', OBJ_LABEL, 0, 0, 0)
        ObjectSetString(ChartID(), ObjectPrefix + 'All', OBJPROP_TEXT, '')
        ObjectSetInteger(ChartID(), ObjectPrefix + 'All', OBJPROP_FONTSIZE, FontSize)
        ObjectSetString(ChartID(), ObjectPrefix + 'All', OBJPROP_FONT, FontFace)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'All', OBJPROP_COLOR, AverageWickSizeColor)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'All', OBJPROP_CORNER, Corner)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'All', OBJPROP_XDISTANCE, Distance_X)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'All', OBJPROP_YDISTANCE, Distance_Y + 24)
        ObjectSetInteger(ChartID(), ObjectPrefix + 'All', OBJPROP_BACK, DrawTextAsBackground)
    Poin = Point()
    if (not UseRawPips) and (Point() == 1e-05 or Point() == 0.001):
        Poin *= 10
    if not WaitForClose:
        CanDoAlerts = False
    else:
        CanDoAlerts = True

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), ObjectPrefix)

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        RedrawVisibleWickLabels()

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    global AlertDone, CanDoAlerts
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    name = ""
    length = ""
    DoAlert = False
    index = 0
    if WaitForClose:
        index = 1
    counted_bars = prev_calculated
    if counted_bars > 0:
        counted_bars -= 1
    limit = rates_total - counted_bars
    if MaxCandles != 0 and limit > MaxCandles:
        limit = MaxCandles
    for i in range(0, limit):
        if TopBottomPercent > 0 and TopBottomPercent <= 100:
            percent = ((High[i] - Low[i]) * TopBottomPercent) / 100
            if not ((Open[i] >= NormalizeDouble(High[i] - percent, Digits()) and Close[i] >= NormalizeDouble(High[i] - percent, Digits())) or (Open[i] <= NormalizeDouble(Low[i] + percent, Digits()) and Close[i] <= NormalizeDouble(Low[i] + percent, Digits()))):
                continue
        if Units == Percentage and High[i] == Low[i]:
            continue
        if ((not LessThan) and ((Units == Pips and NormalizeDouble(High[i] - MathMax(Open[i], Close[i]), Digits()) >= NormalizeDouble(DisplayWickLimit * Poin, Digits())) or (Units == Percentage and (_fdiv(High[i] - MathMax(Open[i], Close[i]), High[i] - Low[i]) * 100) >= DisplayWickLimit))) or (LessThan and ((Units == Pips and NormalizeDouble(High[i] - MathMax(Open[i], Close[i]), Digits()) <= NormalizeDouble(DisplayWickLimit * Poin, Digits())) or (Units == Percentage and (_fdiv(High[i] - MathMax(Open[i], Close[i]), High[i] - Low[i]) * 100) <= DisplayWickLimit))):
            name = GenerateObjectName('Red-', Time[i])
            if Units == Pips:
                length = DoubleToString(MathRound(_fdiv(High[i] - MathMax(Open[i], Close[i]), Poin)), 0)
            elif Units == Percentage:
                length = DoubleToString(MathRound(_fdiv(High[i] - MathMax(Open[i], Close[i]), High[i] - Low[i]) * 100), 0)
            if ObjectFind(0, name) != -1:
                ObjectDelete(0, name)
            object_color = 0
            if Close[i] >= Open[i]:
                object_color = DisplayHighWickColorBullish
            else:
                object_color = DisplayHighWickColorBearish
            if object_color != clrNONE:
                ObjectCreate(0, name, OBJ_TEXT, 0, Time[i], High[i])
                ObjectSetString(0, name, OBJPROP_TEXT, length)
                ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
                ObjectSetString(0, name, OBJPROP_FONT, FontFace)
                ObjectSetInteger(0, name, OBJPROP_COLOR, object_color)
                visible_bars = _int(ChartGetInteger(0, CHART_VISIBLE_BARS))
                first_bar = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR))
                last_bar = first_bar - visible_bars + 1
                if i <= first_bar and i >= last_bar:
                    RedrawOneWickLabel(i, last_bar)
                ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_UPPER)
                ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
        else:
            name = GenerateObjectName('Red-', Time[i])
            if ObjectFind(0, name) != -1:
                ObjectDelete(0, name)
        if ((not LessThan) and ((Units == Pips and NormalizeDouble(MathMin(Open[i], Close[i]) - Low[i], Digits()) >= NormalizeDouble(DisplayWickLimit * Poin, Digits())) or (Units == Percentage and (_fdiv(MathMin(Open[i], Close[i]) - Low[i], High[i] - Low[i]) * 100) >= DisplayWickLimit))) or (LessThan and ((Units == Pips and NormalizeDouble(MathMin(Open[i], Close[i]) - Low[i], Digits()) <= NormalizeDouble(DisplayWickLimit * Poin, Digits())) or (Units == Percentage and (_fdiv(MathMin(Open[i], Close[i]) - Low[i], High[i] - Low[i]) * 100) <= DisplayWickLimit))):
            name = GenerateObjectName('Green-', Time[i])
            if Units == Pips:
                length = DoubleToString(MathRound(_fdiv(MathMin(Open[i], Close[i]) - Low[i], Poin)), 0)
            elif Units == Percentage:
                length = DoubleToString(MathRound(_fdiv(MathMin(Open[i], Close[i]) - Low[i], High[i] - Low[i]) * 100), 0)
            if ObjectFind(0, name) != -1:
                ObjectDelete(0, name)
            object_color = 0
            if Close[i] >= Open[i]:
                object_color = DisplayLowWickColorBullish
            else:
                object_color = DisplayLowWickColorBearish
            if object_color != clrNONE:
                ObjectCreate(0, name, OBJ_TEXT, 0, Time[i], Low[i])
                ObjectSetString(0, name, OBJPROP_TEXT, length)
                ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
                ObjectSetString(0, name, OBJPROP_FONT, FontFace)
                ObjectSetInteger(0, name, OBJPROP_COLOR, object_color)
                ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_UPPER)
                ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
        else:
            name = GenerateObjectName('Green-', Time[i])
            if ObjectFind(0, name) != -1:
                ObjectDelete(0, name)
    if RemoveOldLabels and MaxCandles > 0:
        ClearOldLabels()
    if ShowAverageWickSize:
        limit = rates_total
        if AvgCandles != 0 and limit > AvgCandles:
            limit = AvgCandles
        upper = 0.0
        lower = 0.0
        for i in range(0, limit):
            upper += High[i] - MathMax(Open[i], Close[i])
            lower += MathMin(Open[i], Close[i]) - Low[i]
        ObjectSetString(ChartID(), ObjectPrefix + 'Upper', OBJPROP_TEXT, 'Avg Upper: ' + DoubleToString(_fdiv(_fdiv(upper, limit), Poin), 1))
        ObjectSetString(ChartID(), ObjectPrefix + 'Lower', OBJPROP_TEXT, 'Avg Lower: ' + DoubleToString(_fdiv(_fdiv(lower, limit), Poin), 1))
        ObjectSetString(ChartID(), ObjectPrefix + 'All', OBJPROP_TEXT, 'Avg All: ' + DoubleToString(_fdiv(_fdiv(upper + lower, limit * 2), Poin), 1))
    if AlertDone == Time[index] or (counted_bars == 0 and (IgnoreAlertsOnFirstRun or index == 0)):
        if index != 0:
            AlertDone = Time[index]
        return rates_total
    if Units == Percentage and High[index] == Low[index]:
        return rates_total
    if AlertOnLimit:
        UpperPipsCondition = Units == Pips and (((not LessThan) and NormalizeDouble(High[index] - MathMax(Open[index], Close[index]), Digits()) >= NormalizeDouble(UpperWickLimit * Point(), Digits())) or (LessThan and NormalizeDouble(High[index] - MathMax(Open[index], Close[index]), Digits()) <= NormalizeDouble(UpperWickLimit * Point(), Digits())))
        UpperPercentageCondition = Units == Percentage and (((not LessThan) and (_fdiv(High[index] - MathMax(Open[index], Close[index]), High[index] - Low[index]) * 100) >= UpperWickLimit) or (LessThan and (_fdiv(High[index] - MathMax(Open[index], Close[index]), High[index] - Low[index]) * 100) <= UpperWickLimit))
        LowerPipsCondition = Units == Pips and (((not LessThan) and NormalizeDouble(MathMin(Open[index], Close[index]) - Low[index], Digits()) >= NormalizeDouble(LowerWickLimit * Point(), Digits())) or (LessThan and NormalizeDouble(MathMin(Open[index], Close[index]) - Low[index], Digits()) <= NormalizeDouble(LowerWickLimit * Point(), Digits())))
        LowerPercentageCondition = Units == Percentage and (((not LessThan) and (_fdiv(MathMin(Open[index], Close[index]) - Low[index], High[index] - Low[index]) * 100) >= LowerWickLimit) or (LessThan and (_fdiv(MathMin(Open[index], Close[index]) - Low[index], High[index] - Low[index]) * 100) <= LowerWickLimit))
        if (Close[index] >= Low[index] and DisplayHighWickColorBullish == clrNONE) or (Close[index] < Low[index] and DisplayHighWickColorBearish == clrNONE):
            UpperPipsCondition = False
            UpperPercentageCondition = False
        if (Close[index] >= Low[index] and DisplayLowWickColorBullish == clrNONE) or (Close[index] < Low[index] and DisplayLowWickColorBearish == clrNONE):
            LowerPipsCondition = False
            LowerPercentageCondition = False
        if ((UpperPipsCondition or UpperPercentageCondition) or LowerPipsCondition) or LowerPercentageCondition:
            DoAlert = True
        else:
            CanDoAlerts = True
        if DoAlert and CanDoAlerts:
            dir = ''
            if UpperPipsCondition or UpperPercentageCondition:
                dir = 'Upper'
            if LowerPipsCondition or LowerPercentageCondition:
                if dir == 'Upper':
                    dir += '+'
                dir += 'Lower'
            units = ''
            if Units == Pips:
                units = 'pips'
            if Units == Percentage:
                units = '%'
            if VisualAlert:
                Alert(dir + ' ' + units + ' wick limit reached!')
            if SoundAlert:
                PlaySound('alert.wav')
            if EmailAlert:
                SendMail('CandleWick Alert', Symbol() + ' ' + TimeToString(Time[index]) + ' ' + dir + ' ' + units + ' - wick limit reached!')
            if NotificationAlert:
                SendNotification(Symbol() + ' ' + TimeToString(Time[index]) + ' ' + dir + ' ' + units + ' - wick limit reached!')
            AlertDone = Time[index]
    if AlertOnEqualTopBottomWicks:
        EqualWicksCondition = (High[index] - MathMax(Open[index], Close[index])) == (MathMin(Open[index], Close[index]) - Low[index])
        if EqualWicksCondition:
            if ObjectFind(ChartID(), GenerateObjectName('Green-', Time[index])) < 0:
                return rates_total
            if VisualAlert:
                Alert(Symbol() + ' ' + TimeToString(Time[index]) + ' Upper wick equals lower wick!')
            if SoundAlert:
                PlaySound('alert.wav')
            if EmailAlert:
                SendMail('CandleWick Alert', Symbol() + ' ' + TimeToString(Time[index]) + ' Upper wick equals lower wick!')
            if NotificationAlert:
                SendNotification(Symbol() + ' ' + TimeToString(Time[index]) + '  Upper wick equals lower wick!')
            AlertDone = Time[index]
    return rates_total

def RedrawVisibleWickLabels():
    visible_bars = _int(ChartGetInteger(0, CHART_VISIBLE_BARS))
    first_bar = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR))
    last_bar = first_bar - visible_bars + 1
    for i in range(first_bar, last_bar - 1, -1):
        RedrawOneWickLabel(i, last_bar)

def RedrawOneWickLabel(i, last_bar):
    x = Box(0)
    y = Box(0)
    cw = Box(0)
    w = Box(0)
    h = Box(0)
    t = Box(0)
    p = Box(0.0)
    high = 0.0
    length = ""
    name = ""
    high = iHigh(None, 0, i)
    name = GenerateObjectName('Red-', iTime(None, Period(), i))
    if ObjectFind(0, name) == -1:
        return
    ChartTimePriceToXY(0, 0, iTime(None, Period(), last_bar), high, x, y)
    TextSetFont(FontFace, FontSize * -10)
    length = DoubleToString(MathRound(_fdiv(high - MathMax(iOpen(None, 0, i), iClose(None, 0, i)), Poin)), 0)
    TextGetSize(length, w, h)
    if (y.v - _int(h.v) - 2) < 0:
        if not ChartXYToTimePrice(0, x.v, y.v + h.v + 2, cw, t, p):
            Print('Error: ', GetLastError())
        diff = high - p.v
        p.v = high + diff
    else:
        ChartXYToTimePrice(0, x.v, y.v - h.v - 2, cw, t, p)
    ObjectSetDouble(0, name, OBJPROP_PRICE, p.v)

def GenerateObjectName(prefix, time):
    return ObjectPrefix + prefix + TimeToString(time)

def ClearOldLabels():
    if MaxCandles >= iBars(Symbol(), Period()):
        return
    objects_total = ObjectsTotal(0, -1, OBJ_TEXT)
    for i in range(objects_total - 1, 0 - 1, -1):
        object_name = ObjectName(0, i, -1, OBJ_TEXT)
        object_time = ObjectGetInteger(0, object_name, OBJPROP_TIME, 0)
        if object_time <= iTime(Symbol(), Period(), MaxCandles):
            ObjectDelete(0, object_name)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleWicksDisplay(_MQL5Indicator):
    name = 'CandleWicksDisplay'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Units': _Choice({0: 'Pips', 1: 'Percentage'}, default=0),  # Standard pips or percentage points.
        'DisplayWickLimit': 5,  # DisplayWickLimit in standard pips or %.
        'UpperWickLimit': 10,  # UpperWickLimit in broker pips or % for alerts.
        'LowerWickLimit': 10,  # LowerWickLimit in broker pips or % for alerts.
        'WaitForClose': True,  # WaitForClose - Wait for a candle to close before checking wicks' length?
        'TopBottomPercent': 0,  # TopBottomPercent: Body within top/bottom percentage part.
        'LessThan': False,  # LessThan: display wicks lower than DisplayWickLimit.
        'SoundAlert': False,
        'VisualAlert': False,
        'EmailAlert': False,
        'NotificationAlert': False,
        'AlertOnLimit': False,
        'AlertOnEqualTopBottomWicks': False,
        'IgnoreAlertsOnFirstRun': True,
        'FontSize': 10,
        'MaxCandles': 500,
        'UseRawPips': False,  # UseRawPips: if true, will use points instead of pips.
        'ShowAverageWickSize': False,  # Show average wick size
        'AvgCandles': 50,  # AvgBars: how many candles to calculate the average for.
        'Corner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=0),
        'Distance_X': 3,
        'Distance_Y': 12,
        'DrawTextAsBackground': False,  # DrawTextAsBackground: if true, the text will be drawn as background.
        'RemoveOldLabels': False,  # RemoveOldLabels: Delete labels beyond MaxCandles?
    }

