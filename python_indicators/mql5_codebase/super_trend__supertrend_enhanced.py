"""Super Trend — converted from MQL5: MQL5 Indicators/SuperTrend_Enhanced/Super Trend.mq5

Copyright: Copyright 2025, BENALI; Link: https://www.mql5.com/en/users/dahmi_benali; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, BENALI', 'link': 'https://www.mql5.com/en/users/dahmi_benali', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'UpTrend', 2: 'DownTrend'}, 'levels': [], 'description': [], 'name': 'Super Trend', 'source': 'MQL5 Indicators/SuperTrend_Enhanced/Super Trend.mq5', 'folder': 'SuperTrend_Enhanced', 'inputs': [{'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'int', 'default': 10, 'label': 'ATR Period', 'sinput': False}, {'mql': 'Multiplier', 'py': 'Multiplier', 'param': 'Multiplier', 'type': 'double', 'default': 3.0, 'label': 'Multiplier for SuperTrend', 'sinput': False}, {'mql': 'ShowChartInfo', 'py': 'ShowChartInfo', 'param': 'ShowChartInfo', 'type': 'bool', 'default': True, 'label': 'Display trend info on chart', 'sinput': False}, {'mql': 'InfoColor', 'py': 'InfoColor', 'param': None, 'type': 'color', 'default': 16777215, 'label': 'Text color', 'sinput': False}, {'mql': 'EnablePushNotification', 'py': 'EnablePushNotification', 'param': 'EnablePushNotification', 'type': 'bool', 'default': True, 'label': 'Enable mobile notification on trend change', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ATR_Period = _input('ATR_Period', 10)  # ATR Period
Multiplier = _input('Multiplier', 3.0)  # Multiplier for SuperTrend
ShowChartInfo = _input('ShowChartInfo', True)  # Display trend info on chart
InfoColor = _input('InfoColor', clrWhite)  # Text color
EnablePushNotification = _input('EnablePushNotification', True)  # Enable mobile notification on trend change
UpTrendBuffer = Arr(0, 0.0)
DownTrendBuffer = Arr(0, 0.0)
TrendBuffer = Arr(0, 0.0)
ATRBuffer = Arr(0, 0.0)
atr_handle = 0
lastTrendDirection = 0
trend_label_name = 'Trend_Label'
trend_value_name = 'Trend_Value'
trend_count_label = 'Trend_Count'

def OnInit():
    global atr_handle
    SetIndexBuffer(0, UpTrendBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DownTrendBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, TrendBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ATRBuffer, INDICATOR_CALCULATIONS)
    atr_handle = iATR(Symbol(), Period(), ATR_Period)
    if atr_handle == INVALID_HANDLE:
        Print('Failed to create ATR handle')
        return INIT_FAILED
    return INIT_SUCCEEDED

def TimeFrameToString(period):
    _sw1 = period
    if _sw1 == PERIOD_M1:
        return 'M1'
    elif _sw1 == PERIOD_M3:
        return 'M3'
    elif _sw1 == PERIOD_M5:
        return 'M5'
    elif _sw1 == PERIOD_M15:
        return 'M15'
    elif _sw1 == PERIOD_M30:
        return 'M30'
    elif _sw1 == PERIOD_H1:
        return 'H1'
    elif _sw1 == PERIOD_H4:
        return 'H4'
    elif _sw1 == PERIOD_D1:
        return 'D1'
    elif _sw1 == PERIOD_W1:
        return 'W1'
    elif _sw1 == PERIOD_MN1:
        return 'MN1'
    else:
        return 'Unknown'

def OnCalculate(rates_total, prev_calculated, begin, price):
    global lastTrendDirection
    if rates_total < (ATR_Period + 2):
        return 0
    close = Arr(0, 0.0)
    high = Arr(0, 0.0)
    low = Arr(0, 0.0)
    if CopyClose(Symbol(), Period(), 0, rates_total, close) <= 0:
        return 0
    if CopyHigh(Symbol(), Period(), 0, rates_total, high) <= 0:
        return 0
    if CopyLow(Symbol(), Period(), 0, rates_total, low) <= 0:
        return 0
    if CopyBuffer(atr_handle, 0, 0, rates_total, ATRBuffer) <= 0:
        return 0
    start = (ATR_Period if (prev_calculated == 0) else (prev_calculated - 1))
    if prev_calculated == 0:
        i = ATR_Period
        atr = ATRBuffer[i]
        hl2 = (high[i] + low[i]) / 2.0
        upperBand = hl2 - (Multiplier * atr)
        lowerBand = hl2 + (Multiplier * atr)
        TrendBuffer[i] = (1 if (close[i] > hl2) else -1)
        UpTrendBuffer[i] = (upperBand if (TrendBuffer[i] == 1) else EMPTY_VALUE)
        DownTrendBuffer[i] = (lowerBand if (TrendBuffer[i] == -1) else EMPTY_VALUE)
        start = i + 1
    for i in range(start, rates_total):
        if ATRBuffer[i] == 0:
            continue
        atr = ATRBuffer[i]
        hl2 = (high[i] + low[i]) / 2.0
        upperBand = hl2 - (Multiplier * atr)
        lowerBand = hl2 + (Multiplier * atr)
        if TrendBuffer[i - 1] == 1 and close[i - 1] > UpTrendBuffer[i - 1]:
            UpTrendBuffer[i] = MathMax(upperBand, UpTrendBuffer[i - 1])
        else:
            UpTrendBuffer[i] = upperBand
        if TrendBuffer[i - 1] == -1 and close[i - 1] < DownTrendBuffer[i - 1]:
            DownTrendBuffer[i] = MathMin(lowerBand, DownTrendBuffer[i - 1])
        else:
            DownTrendBuffer[i] = lowerBand
        if TrendBuffer[i - 1] == 1 and close[i] < UpTrendBuffer[i - 1]:
            TrendBuffer[i] = -1.0
        elif TrendBuffer[i - 1] == -1 and close[i] > DownTrendBuffer[i - 1]:
            TrendBuffer[i] = 1.0
        else:
            TrendBuffer[i] = TrendBuffer[i - 1]
        UpTrendBuffer[i] = (UpTrendBuffer[i] if (TrendBuffer[i] == 1) else EMPTY_VALUE)
        DownTrendBuffer[i] = (DownTrendBuffer[i] if (TrendBuffer[i] == -1) else EMPTY_VALUE)
    if EnablePushNotification and rates_total >= 3:
        current = _int(TrendBuffer[rates_total - 1])
        previous = _int(TrendBuffer[rates_total - 2])
        if current != previous and current != lastTrendDirection:
            msg = StringFormat('SuperTrend - %s [%s]: %s', Symbol(), TimeFrameToString(Period()), ('UP Trend Started' if (current == 1) else 'DOWN Trend Started'))
            SendNotification(msg)
            lastTrendDirection = current
    ShowTrendInfo(rates_total)
    return rates_total

def OnDeinit(reason):
    if ObjectFind(0, trend_label_name) != -1:
        ObjectDelete(0, trend_label_name)
    if ObjectFind(0, trend_value_name) != -1:
        ObjectDelete(0, trend_value_name)
    if ObjectFind(0, trend_count_label) != -1:
        ObjectDelete(0, trend_count_label)

def ShowTrendInfo(rates_total):
    if (not ShowChartInfo) or rates_total < 2:
        return
    last_index = rates_total - 1
    trend_dir = _int(TrendBuffer[last_index])
    trend_word = ('UP' if (trend_dir == 1) else 'DOWN')
    trend_color = (clrLime if (trend_dir == 1) else clrRed)
    trend_count = 1
    for j in range(last_index - 1, 0 - 1, -1):
        if _int(TrendBuffer[j]) == trend_dir:
            trend_count += 1
        else:
            break
    bars_text = 'Bars : ' + IntegerToString(trend_count)
    if ObjectFind(0, trend_label_name) == -1:
        ObjectCreate(0, trend_label_name, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, trend_label_name, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(0, trend_label_name, OBJPROP_XDISTANCE, 10)
        ObjectSetInteger(0, trend_label_name, OBJPROP_YDISTANCE, 20)
        ObjectSetInteger(0, trend_label_name, OBJPROP_FONTSIZE, 12)
        ObjectSetInteger(0, trend_label_name, OBJPROP_COLOR, InfoColor)
    ObjectSetString(0, trend_label_name, OBJPROP_TEXT, 'Trend :')
    if ObjectFind(0, trend_value_name) == -1:
        ObjectCreate(0, trend_value_name, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, trend_value_name, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(0, trend_value_name, OBJPROP_XDISTANCE, 60)
        ObjectSetInteger(0, trend_value_name, OBJPROP_YDISTANCE, 20)
        ObjectSetInteger(0, trend_value_name, OBJPROP_FONTSIZE, 12)
    ObjectSetInteger(0, trend_value_name, OBJPROP_COLOR, trend_color)
    ObjectSetString(0, trend_value_name, OBJPROP_TEXT, trend_word)
    if ObjectFind(0, trend_count_label) == -1:
        ObjectCreate(0, trend_count_label, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, trend_count_label, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(0, trend_count_label, OBJPROP_XDISTANCE, 10)
        ObjectSetInteger(0, trend_count_label, OBJPROP_YDISTANCE, 40)
        ObjectSetInteger(0, trend_count_label, OBJPROP_FONTSIZE, 12)
        ObjectSetInteger(0, trend_count_label, OBJPROP_COLOR, InfoColor)
    ObjectSetString(0, trend_count_label, OBJPROP_TEXT, bars_text)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SuperTrend(_MQL5Indicator):
    name = 'Super Trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATR_Period': 10,  # ATR Period
        'Multiplier': 3.0,  # Multiplier for SuperTrend
        'ShowChartInfo': True,  # Display trend info on chart
        'EnablePushNotification': True,  # Enable mobile notification on trend change
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

