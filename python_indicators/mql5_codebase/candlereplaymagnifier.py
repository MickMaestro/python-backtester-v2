"""CandleReplayMagnifier — converted from MQL5: MQL5 Indicators/Candle Replay Magnifier/CandleReplayMagnifier.mq5

Visual replay magnifier for selected candles.
Draws an overlay of candles from a past date over current chart.
Highlight area auto-initialized; user selects replay date.
Copyright: Copyright 2025, ProtimeTrader; Link: https://www.mql5.com/en/users/protimetrader; Version: 1.05

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, ProtimeTrader', 'link': 'https://www.mql5.com/en/users/protimetrader', 'version': '1.05', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Visual replay magnifier for selected candles.', 'Draws an overlay of candles from a past date over current chart.', 'Highlight area auto-initialized; user selects replay date.'], 'name': 'CandleReplayMagnifier', 'source': 'MQL5 Indicators/Candle Replay Magnifier/CandleReplayMagnifier.mq5', 'folder': 'Candle Replay Magnifier', 'inputs': [{'mql': 'InpReplayDate', 'py': 'InpReplayDate', 'param': None, 'type': 'datetime', 'default': 0, 'label': 'Date to replay candle data from', 'sinput': False}, {'mql': 'InpMainZoneColor', 'py': 'InpMainZoneColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Highlight color for the main (current) zone', 'sinput': False}, {'mql': 'InpReplayZoneColor', 'py': 'InpReplayZoneColor', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Highlight color for the replay (historical) zone', 'sinput': False}, {'mql': 'InpBullColor', 'py': 'InpBullColor', 'param': None, 'type': 'color', 'default': 13959039, 'label': 'Color for bullish (up) replay candles', 'sinput': False}, {'mql': 'InpBearColor', 'py': 'InpBearColor', 'param': None, 'type': 'color', 'default': 13353215, 'label': 'Color for bearish (down) replay candles', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpReplayDate = _input('InpReplayDate', 0)  # Date to replay candle data from
InpMainZoneColor = _input('InpMainZoneColor', clrRed)  # Highlight color for the main (current) zone
InpReplayZoneColor = _input('InpReplayZoneColor', clrGreen)  # Highlight color for the replay (historical) zone
InpBullColor = _input('InpBullColor', clrAquamarine)  # Color for bullish (up) replay candles
InpBearColor = _input('InpBearColor', clrPink)  # Color for bearish (down) replay candles
m_OBJ_NAME_PREFIX = 'CRM_'
candles = Arr(0, None)
m_replayDate = 0
m_barRange = 0
m_zoneHigh = 0.0
m_zoneLow = 0.0
m_index = 0

class CCandleData(MqlObject):
    _q_fields = ('time', 'open', 'high', 'low', 'close')
    def __init__(self, *args):
        self.time = 0
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0
    def CCandleData(self, t, o, h, l, c):
        self.time = t
        self.open = o
        self.high = h
        self.low = l
        self.close = c

def OnInit():
    global m_barRange, m_replayDate
    m_barRange = 32
    m_replayDate = InpReplayDate
    if m_replayDate == 0:
        dt = MqlDateTime()
        TimeToStruct(TimeCurrent(), dt)
        dt.day -= 1
        dt.hour = 0
        dt.min = 0
        dt.sec = 0
        m_replayDate = StructToTime(dt)
        dayOfWeek = dt.day_of_week
        if dayOfWeek == 0:
            PrintFormat('[CandleReplay] Note: %s is a Sunday. Market may be closed or have missing candles.', TimeToString(m_replayDate, TIME_DATE))
        elif dayOfWeek == 6:
            PrintFormat('[CandleReplay] Note: %s is a Saturday. Market may be closed or have missing candles.', TimeToString(m_replayDate, TIME_DATE))
    if Period() >= PERIOD_D1:
        Alert('[CandleReplay]: This indicator is designed for intraday timeframes only. Please select a period lower than Daily.')
    DrawZone()
    if FetchReplayCandles():
        DrawReplayCandles()
    PrintFormat('[CandleReplay] Initialized.\nReplay Date: %s\nBar Range: %d bars', TimeToString(m_replayDate, TIME_DATE), m_barRange)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    totalObjects = ObjectsDeleteAll(0, m_OBJ_NAME_PREFIX)
    PrintFormat("[CandleReplay] Deleted %d chart objects with prefix '%s'.", totalObjects, m_OBJ_NAME_PREFIX)
    totalCandles = ArraySize(candles)
    for i in range(0, totalCandles):
        _delete(candles[i])
    ArrayResize(candles, 0)
    PrintFormat('[CandleReplay] Cleared %d candle data objects from memory.', totalCandles)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global m_barRange
    if prev_calculated != rates_total:
        ResizeZone()
        t1 = ObjectGetInteger(0, m_OBJ_REPLAY_ZONE, OBJPROP_TIME, 0)
        m_barRange = iBarShift(Symbol(), Period(), t1)
        if FetchReplayCandles():
            DrawReplayCandles()
    if high[rates_total - 1] > m_zoneHigh or low[rates_total - 1] < m_zoneLow:
        ResizeZone()
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global m_barRange
    if (id_ == CHARTEVENT_OBJECT_CHANGE or id_ == CHARTEVENT_OBJECT_DRAG) and sparam == m_OBJ_ZONE:
        t1 = ObjectGetInteger(0, m_OBJ_ZONE, OBJPROP_TIME, 0)
        m_barRange = iBarShift(Symbol(), Period(), t1)
        if not ResizeZone():
            Print('Failed to resize zone')
        for i in range(0, ArraySize(candles)):
            ObjectDelete(0, m_OBJ_BODY_PREFIX + IntegerToString(i))
        if FetchReplayCandles():
            DrawReplayCandles()

def DrawZone():
    global m_zoneHigh, m_zoneLow
    t1 = iTime(Symbol(), Period(), m_barRange)
    t2 = iTime(Symbol(), Period(), 0) + (iTime(Symbol(), Period(), 0) - t1)
    m_zoneHigh = iHigh(Symbol(), Period(), iHighest(Symbol(), Period(), MODE_HIGH, m_barRange + 1, 0))
    m_zoneLow = iLow(Symbol(), Period(), iLowest(Symbol(), Period(), MODE_LOW, m_barRange + 1, 0))
    if not CreateOrUpdateObjectZone(t1, t2, m_zoneHigh, m_zoneLow):
        return False
    CreateObjectReplayZone(t1, t2)
    return True

def ResizeZone():
    global m_zoneHigh, m_zoneLow
    t1 = iTime(Symbol(), Period(), m_barRange)
    t2 = iTime(Symbol(), Period(), 0) + (iTime(Symbol(), Period(), 0) - iTime(Symbol(), Period(), m_barRange))
    m_zoneHigh = iHigh(Symbol(), Period(), iHighest(Symbol(), Period(), MODE_HIGH, m_barRange + 1, 0))
    m_zoneLow = iLow(Symbol(), Period(), iLowest(Symbol(), Period(), MODE_LOW, m_barRange + 1, 0))
    if not CreateOrUpdateObjectZone(t1, t2, m_zoneHigh, m_zoneLow):
        PrintFormat("ResizeZone Error: Failed to update object '%s' on symbol %s (Period: %s, Range: %d bars)", m_OBJ_ZONE, Symbol(), EnumToString(Period(), 'ENUM_TIMEFRAMES'), m_barRange)
        return False
    ObjectSetInteger(0, m_OBJ_REPLAY_ZONE, OBJPROP_TIME, 0, t1)
    ObjectSetInteger(0, m_OBJ_REPLAY_ZONE, OBJPROP_TIME, 1, t2)
    return True

def FetchReplayCandles():
    global m_index
    rates = Arr(0, 0, factory=MqlRates)
    copied = 0
    targetDay = 0
    if OnSameDay():
        copied = CopyRates(Symbol(), Period(), 0, m_barRange, rates)
    else:
        zoneTime = MqlDateTime()
        zoneEnd = ObjectGetInteger(0, m_OBJ_ZONE, OBJPROP_TIME, 1)
        TimeToStruct(zoneEnd, zoneTime)
        replayTime = MqlDateTime()
        TimeToStruct(m_replayDate, replayTime)
        replayTime.hour = zoneTime.hour
        replayTime.min = zoneTime.min
        replayTime.sec = 0
        fullTime = StructToTime(replayTime)
        shift = iBarShift(Symbol(), Period(), fullTime, False)
        target = iTime(Symbol(), Period(), shift)
        targetStruct = MqlDateTime()
        TimeToStruct(target, targetStruct)
        targetDay = targetStruct.day
        startShift = iBarShift(Symbol(), Period(), target)
        copied = CopyRates(Symbol(), Period(), startShift, (m_barRange * 2) + 1, rates)
    if copied <= 0:
        PrintFormat('[CRM] Failed to fetch candle data. Bars copied: %d', copied)
        return False
    for i in range(0, ArraySize(candles)):
        _delete(candles[i])
    ArrayResize(candles, 0)
    for i in range(0, copied):
        rateTime = MqlDateTime()
        candleTime = rates[i].time
        TimeToStruct(candleTime, rateTime)
        replayDay = rateTime.day
        replayHour = rateTime.hour
        replayMin = rateTime.min
        currentStruct = MqlDateTime()
        TimeToStruct(iTime(Symbol(), Period(), 0), currentStruct)
        if (replayDay == targetDay and currentStruct.hour == replayHour) and currentStruct.min == replayMin:
            m_index = i
        candles[ArrayResize(candles, ArraySize(candles) + 1) - 1] = CCandleData(rates[i].time, rates[i].open, rates[i].high, rates[i].low, rates[i].close)
    if m_index < m_barRange and (not OnSameDay()):
        PrintFormat('[CRM] Failed to find matching replay index (m_index = %d, expected ≥ %d)', m_index, m_barRange)
        return False
    if ArraySize(candles) <= 0:
        PrintFormat('[CRM] Candle array is empty after fetch.')
        return False
    return True

def DrawReplayCandles():
    total = ArraySize(candles)
    if total == 0:
        return
    candle_width = PeriodSeconds()
    downwardShift = iOpen(Symbol(), Period(), 0) - (candles[0].low if OnSameDay() else candles[m_index].open)
    downwardShift = (0.0 if OnSameDay() else downwardShift)
    highPrice = candles[0].close + downwardShift
    lowPrice = candles[0].close + downwardShift
    for i in range(0, total - 1):
        t = TimeCurrent() - (PeriodSeconds() * (m_barRange - i))
        t_next = t + candle_width
        open = candles[i].open + downwardShift
        close = candles[i].close + downwardShift
        high = candles[i].high + downwardShift
        low = candles[i].low + downwardShift
        if high > highPrice:
            highPrice = high
        if low < lowPrice:
            lowPrice = low
        CreateObjectBody(i, t, t_next, open, close, high, low)
    ObjectSetDouble(0, m_OBJ_REPLAY_ZONE, OBJPROP_PRICE, 0, highPrice)
    ObjectSetDouble(0, m_OBJ_REPLAY_ZONE, OBJPROP_PRICE, 1, lowPrice)

def OnSameDay():
    selected = MqlDateTime()
    now = MqlDateTime()
    TimeToStruct(m_replayDate, selected)
    TimeToStruct(TimeCurrent(), now)
    return (selected.year == now.year and selected.mon == now.mon) and selected.day == now.day

def CreateOrUpdateObjectZone(t1, t2, high, low):
    if ObjectFind(0, m_OBJ_ZONE) < 0:
        if not ObjectCreate(0, m_OBJ_ZONE, OBJ_RECTANGLE, 0, t1, high, t2, low):
            return False
        ObjectSetInteger(0, m_OBJ_ZONE, OBJPROP_COLOR, InpMainZoneColor)
        ObjectSetInteger(0, m_OBJ_ZONE, OBJPROP_WIDTH, 1)
        ObjectSetInteger(0, m_OBJ_ZONE, OBJPROP_STYLE, STYLE_DASH)
        ObjectSetInteger(0, m_OBJ_ZONE, OBJPROP_BACK, False)
        ObjectSetInteger(0, m_OBJ_ZONE, OBJPROP_FILL, False)
        ObjectSetInteger(0, m_OBJ_ZONE, OBJPROP_SELECTABLE, True)
    else:
        if not ObjectSetInteger(0, m_OBJ_ZONE, OBJPROP_TIME, 1, t2):
            return False
        ObjectSetInteger(0, m_OBJ_ZONE, OBJPROP_TIME, 0, t1)
        ObjectSetDouble(0, m_OBJ_ZONE, OBJPROP_PRICE, 0, high)
        ObjectSetDouble(0, m_OBJ_ZONE, OBJPROP_PRICE, 1, low)
    return True

def CreateObjectReplayZone(t1, t2):
    ObjectCreate(0, m_OBJ_REPLAY_ZONE, OBJ_RECTANGLE, 0, t1, 0, t2, 0)
    ObjectSetInteger(0, m_OBJ_REPLAY_ZONE, OBJPROP_COLOR, InpReplayZoneColor)
    ObjectSetInteger(0, m_OBJ_REPLAY_ZONE, OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, m_OBJ_REPLAY_ZONE, OBJPROP_STYLE, STYLE_DASH)
    ObjectSetInteger(0, m_OBJ_REPLAY_ZONE, OBJPROP_BACK, False)
    ObjectSetInteger(0, m_OBJ_REPLAY_ZONE, OBJPROP_FILL, False)

def CreateObjectBody(i, t, t_next, open, close, high, low):
    name = m_OBJ_BODY_PREFIX + IntegerToString(i)
    top = MathMax(open, close)
    bottom = MathMin(open, close)
    barColor = (InpBullColor if (close >= open) else InpBearColor)
    direction = ('Bullish' if (close >= open) else 'Bearish')
    range_ = high - low
    volume = iVolume(Symbol(), Period(), i)
    tooltip = StringFormat('Time: %s\nOpen: %s\nHigh: %s\nLow: %s\nClose: %s\nRange: %s\nDirection: %s\nVolume: %ld', TimeToString(candles[i].time, TIME_DATE | TIME_MINUTES), DoubleToString(candles[i].open, Digits()), DoubleToString(candles[i].high, Digits()), DoubleToString(candles[i].low, Digits()), DoubleToString(candles[i].close, Digits()), DoubleToString(range_, 3), direction, volume)
    ObjectCreate(0, name, OBJ_RECTANGLE, 0, t, top, t_next, bottom)
    ObjectSetInteger(0, name, OBJPROP_COLOR, barColor)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, 1)
    ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(0, name, OBJPROP_BACK, True)
    ObjectSetInteger(0, name, OBJPROP_FILL, True)
    ObjectSetString(0, name, OBJPROP_TOOLTIP, tooltip)

# ---- global variables initialised from expressions
m_OBJ_ZONE = m_OBJ_NAME_PREFIX + 'Zone'
m_OBJ_REPLAY_ZONE = m_OBJ_NAME_PREFIX + 'ReplayZone'
m_OBJ_BODY_PREFIX = m_OBJ_NAME_PREFIX + 'Body_'


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleReplayMagnifier(_MQL5Indicator):
    name = 'CandleReplayMagnifier'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

