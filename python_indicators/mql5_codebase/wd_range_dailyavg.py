"""wd.Range_DailyAvg — converted from MQL5: MQL5 Indicators/wd.Range_DailyAvg/wd.Range_DailyAvg.mq5

Calculate the 'Average Daily Range' based on 20 days of historical upper-lower price data, to estimate today's price movements.
When the projected trend is upward, taking profit opportunities can be measure by configuring indicator properties with 'Estimated today price zone = Room_up'.
During downward trends, selling price levels and profit target can be measure using 'Estimated today price zone = Room_down'.
Copyright: Copyright © 2023, Karya Prima Rajasa Mediavestama.; Link: https://www.mql5.com/en/code/47117; Version: 2.23

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2023, Karya Prima Rajasa Mediavestama.', 'link': 'https://www.mql5.com/en/code/47117', 'version': '2.23', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ["Calculate the 'Average Daily Range' based on 20 days of historical upper-lower price data, to estimate today's price movements.", "When the projected trend is upward, taking profit opportunities can be measure by configuring indicator properties with 'Estimated today price zone = Room_up'.", "During downward trends, selling price levels and profit target can be measure using 'Estimated today price zone = Room_down'."], 'name': 'wd.Range_DailyAvg', 'source': 'MQL5 Indicators/wd.Range_DailyAvg/wd.Range_DailyAvg.mq5', 'folder': 'wd.Range_DailyAvg', 'inputs': [{'mql': 'showAverageDaysRangeInfo', 'py': 'showAverageDaysRangeInfo', 'param': 'showAverageDaysRangeInfo', 'type': 'bool', 'default': True, 'label': 'Display Average Range Information', 'sinput': False}, {'mql': 'RectColor', 'py': 'RectColor', 'param': None, 'type': 'color', 'default': 65535, 'label': "Today's price zone color", 'sinput': False}, {'mql': 'LineStyle', 'py': 'LineStyle', 'param': 'LineStyle', 'type': 'int', 'default': 1, 'label': 'Price zone style', 'sinput': False}, {'mql': 'LineWidth', 'py': 'LineWidth', 'param': 'LineWidth', 'type': 'int', 'default': 2, 'label': 'Price zone border width', 'sinput': False}, {'mql': 'Anchor', 'py': 'Anchor', 'param': 'Anchor', 'type': 'int', 'default': 0, 'label': 'Estimated today price zone', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_ANCHOR
Room_up = 0
Room_down = 1
_enum('ENUM_ANCHOR', {0: 'Room_up', 1: 'Room_down'})

# ---- inputs and global variables
showAverageDaysRangeInfo = _input('showAverageDaysRangeInfo', True)  # Display Average Range Information
RectColor = _input('RectColor', clrYellow)  # Today's price zone color
LineStyle = _input('LineStyle', STYLE_DASH)  # Price zone style
LineWidth = _input('LineWidth', 2)  # Price zone border width
Anchor = _input('Anchor', Room_up)  # Estimated today price zone
lowestPrice = 0.0  # Declare lowestPrice variable
highestPrice = 0.0  # Declare highestPrice variable
rectangleObjectName = 'Today Price Zone'

def OnInit():
    global highestPrice, lowestPrice
    avgDayRange = 0
    prevDayRange = 0
    avgRange02 = 0
    avgRange05 = 0
    avgRange10 = 0
    avgRange20 = 0
    if showAverageDaysRangeInfo:
        AverageDaysRangeInfo(avgDayRange, prevDayRange, avgRange02, avgRange05, avgRange10, avgRange20)
    sumRange02 = 0
    sumRange05 = 0
    sumRange10 = 0
    sumRange20 = 0
    for i in range(1, 20 + 1):
        dailyRange = _int(_fdiv(iHigh(None, PERIOD_D1, i) - iLow(None, PERIOD_D1, i), Point()))
        sumRange20 += dailyRange
        if i <= 2:
            sumRange02 += dailyRange
        if i <= 5:
            sumRange05 += dailyRange
        if i <= 10:
            sumRange10 += dailyRange
    avgRange02_2 = _idiv(sumRange02, MathMin(20, 2))
    avgRange05_2 = _idiv(sumRange05, MathMin(20, 5))
    avgRange10_2 = _idiv(sumRange10, MathMin(20, 10))
    avgRange20_2 = _idiv(sumRange20, 20)
    prevDayRange_2 = _int(_fdiv(iHigh(None, PERIOD_D1, 1) - iLow(None, PERIOD_D1, 1), Point()))
    avgDayRange_2 = _idiv(prevDayRange_2 + avgRange02_2 + avgRange05_2 + avgRange10_2 + avgRange20_2, 5)
    today = MqlDateTime()
    current_time = TimeCurrent()
    TimeToStruct(current_time, today)
    today.hour = 0
    today.min = 0
    today.sec = 0
    startday = StructToTime(today)
    endday = startday + (24 * 60 * 59)
    if Anchor == Room_down:
        shift = iBarShift(Symbol(), PERIOD_D1, endday, True)
        while shift >= iBarShift(Symbol(), PERIOD_D1, startday, True):
            highPrice = iHigh(Symbol(), PERIOD_D1, shift)
            if highPrice > highestPrice:
                highestPrice = highPrice
            shift -= 1
        endPriceLow = highestPrice - (avgDayRange_2 * Point())
        if ObjectCreate(0, 'Today Price Zone', OBJ_RECTANGLE, 0, startday, highestPrice, endday, endPriceLow):
            ObjectSetInteger(0, 'Today Price Zone', OBJPROP_SELECTABLE, False)
            ObjectSetInteger(0, 'Today Price Zone', OBJPROP_COLOR, RectColor)
            ObjectSetInteger(0, 'Today Price Zone', OBJPROP_STYLE, LineStyle)
            ObjectSetInteger(0, 'Today Price Zone', OBJPROP_WIDTH, LineWidth)
            ObjectSetString(0, 'Today Price Zone', OBJPROP_TEXT, IntegerToString(avgDayRange_2, 1))
    elif Anchor == Room_up:
        shift = iBarShift(Symbol(), PERIOD_D1, endday, True)
        while shift >= iBarShift(Symbol(), PERIOD_D1, startday, True):
            lowPrice = iLow(Symbol(), PERIOD_D1, shift)
            if lowestPrice == 0 or lowPrice < lowestPrice:
                lowestPrice = lowPrice
            shift -= 1
        endPriceHigh = lowestPrice + (avgDayRange_2 * Point())
        if ObjectCreate(0, 'Today Price Zone', OBJ_RECTANGLE, 0, startday, lowestPrice, endday, endPriceHigh):
            ObjectSetInteger(0, 'Today Price Zone', OBJPROP_SELECTABLE, False)
            ObjectSetInteger(0, 'Today Price Zone', OBJPROP_COLOR, RectColor)
            ObjectSetInteger(0, 'Today Price Zone', OBJPROP_STYLE, LineStyle)
            ObjectSetInteger(0, 'Today Price Zone', OBJPROP_WIDTH, LineWidth)
            ObjectSetString(0, 'Today Price Zone', OBJPROP_TEXT, IntegerToString(avgDayRange_2, 1))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, rectangleObjectName)
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not showAverageDaysRangeInfo:
        Comment('')
        return rates_total
    sumRange02 = 0.0
    sumRange05 = 0.0
    sumRange10 = 0.0
    sumRange20 = 0.0
    for i in range(1, 20 + 1):
        dailyRange = _int(_fdiv(iHigh(None, PERIOD_D1, i) - iLow(None, PERIOD_D1, i), Point()))
        sumRange20 += dailyRange
        if i <= 2:
            sumRange02 += dailyRange
        if i <= 5:
            sumRange05 += dailyRange
        if i <= 10:
            sumRange10 += dailyRange
    avgRange02 = _int(_fdiv(sumRange02, MathMin(20, 2)))
    avgRange05 = _int(_fdiv(sumRange05, MathMin(20, 5)))
    avgRange10 = _int(_fdiv(sumRange10, MathMin(20, 10)))
    avgRange20 = _int(sumRange20 / 20)
    prevDayRange = _int(_fdiv(iHigh(None, PERIOD_D1, 1) - iLow(None, PERIOD_D1, 1), Point()))
    avgDayRange = _idiv(prevDayRange + avgRange02 + avgRange05 + avgRange10 + avgRange20, 5)
    AverageDaysRangeInfo(avgDayRange, prevDayRange, avgRange02, avgRange05, avgRange10, avgRange20)
    return rates_total

def AverageDaysRangeInfo(avgDayRange, prevDayRange, avgRange02, avgRange05, avgRange10, avgRange20):
    text = 'Avg ranges: ' + _str(_int(avgDayRange)) + '\n'
    text += 'Prev01 day: ' + _str(_int(prevDayRange)) + '\n'
    text += 'Avg 02 day: ' + _str(_int(avgRange02)) + '\n'
    text += 'Avg 05 day: ' + _str(_int(avgRange05)) + '\n'
    text += 'Avg 10 day: ' + _str(_int(avgRange10)) + '\n'
    text += 'Avg 20 day: ' + _str(_int(avgRange20)) + '\n'
    Comment(text)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WdRangeDailyAvg(_MQL5Indicator):
    name = 'wd.Range_DailyAvg'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'showAverageDaysRangeInfo': True,  # Display Average Range Information
        'LineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # Price zone style
        'LineWidth': 2,  # Price zone border width
        'Anchor': _Choice({0: 'Room_up', 1: 'Room_down'}, default=0),  # Estimated today price zone
    }

